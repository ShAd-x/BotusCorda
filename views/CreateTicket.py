import nextcord
from nextcord import Interaction, Embed, ButtonStyle, PermissionOverwrite
from views.TicketSettings import TicketSettings

class CreateTicket(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @nextcord.ui.button(
        label='Créer un ticket',
        style=ButtonStyle.blurple,
        custom_id='create_ticket'
    )

    async def create_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        msg = await interaction.response.send_message('Création du ticket en cours...', ephemeral=True)

        # Permissions du channel du ticket
        overwrites = {
            interaction.guild.default_role: PermissionOverwrite(read_messages=False),
            interaction.guild.me: PermissionOverwrite(read_messages=True),
        }

        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT role_id FROM roles WHERE guild_id = ?", (interaction.guild.id,))
            dataRoles = await cursor.fetchall()
            if dataRoles:
                for role_id in dataRoles:
                    overwrites[interaction.guild.get_role(role_id[0])] = PermissionOverwrite(read_messages=True)

            await cursor.execute("SELECT category_id FROM categories WHERE message_id = ? AND guild_id = ?", (interaction.message.id, interaction.guild.id,))
            category = await cursor.fetchone()
            category = interaction.guild.get_channel(category[0]) if category else None
            # Si la catégorie n'existe pas, on supprime de la base de données
            if not category:
                await cursor.execute("DELETE FROM categories WHERE message_id = ? AND guild_id = ?", (interaction.message.id, interaction.guild.id))
            await self.bot.db.commit()

        # Créer le channel
        channel = await interaction.guild.create_text_channel(
            f'ticket-{interaction.user.display_name}',
            category=category,
            overwrites=overwrites
        )
        # Prévenir l'utilisateur que le ticket a été créé
        await msg.edit(content=f'Votre ticket a été créé dans {channel.mention} !')

        # Envoyer un message dans le channel du ticket
        embed = Embed(
            title="Ticket créé avec succès",
            description="Un membre du staff va s'occuper de vous.",
            timestamp=interaction.created_at,
        )
        await channel.send(f"{interaction.user.mention}", embed=embed, view=TicketSettings(self.bot))

        # Logs
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id FROM log_channels WHERE guild_id = ?", (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                logChannel = interaction.guild.get_channel(data[0])
                embed = Embed(
                    title="Ticket créé",
                    description=f"Un ticket a été créé par {interaction.user.mention} ({channel.name})\n\n=> {channel.mention}",
                    timestamp=interaction.created_at,
                    color=0x00ff00
                )
                await logChannel.send(embed=embed)

                #  Si la catégorie n'existe pas on prévient le staff dans le channel de logs
                if not category:
                    # Get every roles admin on the guild
                    roles = [role for role in interaction.guild.roles if role.permissions.administrator]
                    roles = " ".join([role.mention for role in roles])
                    await logChannel.send(f"{roles}")
                    
                    embed = Embed(
                        title="Erreur",
                        description=f"La catégorie de salon prédéfinie pour cette catégorie de ticket n'existe pas (salon {interaction.channel.mention}).\nLe ticket a été créé dans {channel.mention} sans catégorie.",
                        timestamp=interaction.created_at,
                        color=0xff0000
                    )
                    await logChannel.send(embed=embed)
