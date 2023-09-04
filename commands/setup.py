import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, Embed
from views.CreateTicket import CreateTicket

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setup", description="Envoie l'embed de création de ticket.", guild_ids=[int(os.getenv("DISCORD_TEST_ID"))])
    async def setup_tickets(self, interaction: Interaction):
        # On envoie un message pour dire que l'embed est en cours d'envoi
        msg = await interaction.response.send_message("Envoi de l'embed de création de ticket...", ephemeral=True)
        # On envoie l'embed
        embed = Embed(title="Créer un ticket", description="Cliquez sur le bouton ci-dessous pour créer un ticket.", color=0x00ff00)
        await interaction.channel.send(embed=embed, view=CreateTicket(self.bot))
        # On édite le message pour dire que l'embed a été envoyé
        await msg.edit(content="L'embed de création de ticket a été envoyé.")
        # On supprime le message après 5 secondes
        await msg.delete(delay=5)

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))