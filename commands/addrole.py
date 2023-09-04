import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, Role

class AddRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="addrole", description="Ajouter un rôle aux rôles pouvant voir les tickets.", guild_ids=[int(os.getenv("DISCORD_TEST_ID"))])
    async def add_role(self, interaction: Interaction, role: Role):
        async with self.bot.db.cursor() as cursor:
            # Vérifier si le rôle existe déjà (role et guild)
            await cursor.execute("SELECT role_id FROM roles WHERE role_id = ? AND guild_id = ?", (role.id, interaction.guild.id))
            data = await cursor.fetchone()
            if data:
                await interaction.send(f"Le rôle {role.mention} est déjà présent dans les rôles pouvant voir les tickets.", ephemeral=True)
            else:
                await cursor.execute("INSERT INTO roles (role_id, guild_id) VALUES (?, ?)", (role.id, interaction.guild.id))
                await interaction.send(f"Le rôle {role.mention} a été ajouté aux rôles pouvant voir les tickets.", ephemeral=True)
        await self.bot.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(AddRole(bot))