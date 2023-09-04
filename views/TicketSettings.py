import nextcord
from nextcord import Interaction, ButtonStyle
from views.AddUserToTicket import AddUserToTicket 
from views.RemoveUserFromTicket import RemoveUserFromTicket

class TicketSettings(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @nextcord.ui.button(
        label='Ajouter un utilisateur',
        style=ButtonStyle.green,
        custom_id='ticket_settings_add_user'
    )

    async def add_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(AddUserToTicket(interaction.channel))

    @nextcord.ui.button(
        label='Supprimer un utilisateur',
        style=ButtonStyle.gray,
        custom_id='ticket_settings_remove_user'
    )

    async def remove_user(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_modal(RemoveUserFromTicket(interaction.channel))

    @nextcord.ui.button(
        label='Fermer le ticket',
        style=ButtonStyle.red,
        custom_id='ticket_settings_close'
    )

    async def close_ticket(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.response.send_message('Fermeture du ticket en cours...', ephemeral=True)
        await interaction.channel.delete(reason='Ticket fermé.')
