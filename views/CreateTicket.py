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
            data = await cursor.fetchall()
            if data:
                for role_id in data:
                    overwrites[interaction.guild.get_role(role_id[0])] = PermissionOverwrite(read_messages=True)


        # Créer le channel
        channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.display_name}', overwrites=overwrites)
        # Prévenir l'utilisateur que le ticket a été créé
        await msg.edit(content=f'Votre ticket a été créé dans {channel.mention} !')

        # Envoyer un message dans le channel du ticket
        embed = Embed(
            title="Ticket créé avec succès",
            description="Un membre du staff va s'occuper de vous.",
            timestamp=nextcord.utils.utcnow(),
        )
        await channel.send(f"{interaction.user.mention}", embed=embed, view=TicketSettings())
