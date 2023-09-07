import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, Embed, CategoryChannel, SlashOption
from views.CreateTicket import CreateTicket

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="setup", description="Envoie l'embed de création de ticket.", guild_ids=[int(os.getenv("DISCORD_TEST_ID"))])
    async def setup_tickets(self, interaction: Interaction, category : CategoryChannel = SlashOption(
        description="La catégorie ou les tickets seront créés.",
    )):
        # On envoie un message pour dire que l'embed est en cours d'envoi
        msg = await interaction.response.send_message("Envoi de l'embed de création de ticket...", ephemeral=True)
        # On envoie l'embed
        embed = Embed(
            title="Créer un ticket",
            description=f"Cliquez sur le bouton ci-dessous pour créer un ticket.\n\nLe ticket sera créé dans la catégorie #{category.name}.",
            color=0x00ff00,
            timestamp=interaction.created_at
        )
        message = await interaction.channel.send(embed=embed, view=CreateTicket(self.bot))
        # On édite le message pour dire que l'embed a été envoyé
        await msg.edit(content="L'embed de création de ticket a été envoyé.")
        # On supprime le message après 5 secondes
        await msg.delete(delay=5)

        # On ajoute le message et la catégorie dans la base de données
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("INSERT INTO categories (message_id, category_id, guild_id) VALUES (?, ?, ?)", (message.id, category.id, interaction.guild.id))
        await self.bot.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(Setup(bot))