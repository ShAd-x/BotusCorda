import nextcord
from nextcord import Interaction, ButtonStyle, Color
from views.AddUserToTicket import AddUserToTicket 
from views.RemoveUserFromTicket import RemoveUserFromTicket

class TicketSettings(nextcord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
    
    @nextcord.ui.button(
        emoji='➕',
        label='Ajouter un utilisateur',
        style=ButtonStyle.green,
        custom_id='ticket_settings_add_user'
    )

    async def add_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(AddUserToTicket(interaction.channel))

    @nextcord.ui.button(
        emoji='🗑️',
        label='Supprimer un utilisateur',
        style=ButtonStyle.gray,
        custom_id='ticket_settings_remove_user'
    )

    async def remove_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(RemoveUserFromTicket(interaction.channel))

    @nextcord.ui.button(
        emoji='🔒',
        label='Fermer le ticket',
        style=ButtonStyle.red,
        custom_id='ticket_settings_close'
    )

    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message('Fermeture du ticket en cours...', ephemeral=True)
        await interaction.channel.delete(reason='Ticket fermé.')

        # Logs
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id FROM log_channels WHERE guild_id = ?", (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                logChannel = interaction.guild.get_channel(data[0])
                embed = nextcord.Embed(
                    title="Ticket fermé",
                    description=f"Le ticket '{interaction.channel.name}' {f'dans la catégorie #{interaction.channel.category.name}' if interaction.channel.category else ''} a été fermé par {interaction.user.mention}.",
                    color=Color.red(),
                    timestamp=nextcord.utils.utcnow()
                )
                await logChannel.send(embed=embed)
