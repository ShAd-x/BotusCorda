import nextcord
from nextcord import Interaction

class AddUserToTicket(nextcord.ui.Modal):
    def __init__(self, channel):
        super().__init__(
            "Ajouter un utilisateur",
            timeout=60,
        )
        self.channel = channel
        self.user = nextcord.ui.TextInput(
            label="ID de l'utilisateur",
            placeholder="ID de l'utilisateur (Entier)",
            min_length=2,
            max_length=30,
            required=True,
        )
        self.add_item(self.user)

    async def callback(self, interaction: Interaction):
        user = interaction.guild.get_member(int(self.user.value))
        
        if user is None:
            return await interaction.edit_original_message(content="Cet utilisateur n'existe pas.")
        
        await self.channel.set_permissions(user, read_messages=True)
        await interaction.send(content=f"L'utilisateur {user.mention} a été ajouté au ticket.")