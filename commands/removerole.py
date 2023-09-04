import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, Role

class RemoveRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="removerole", description="Supprimer un rôle des rôles pouvant voir les tickets.", guild_ids=[int(os.getenv("DISCORD_TEST_ID"))])
    async def remove_role(self, interaction: Interaction, role: Role):
        async with self.bot.db.cursor() as cursor:
            # Vérifier si le rôle existe (role et guild)
            await cursor.execute("SELECT role_id FROM roles WHERE role_id = ? AND guild_id = ?", (role.id, interaction.guild.id))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("DELETE FROM roles WHERE role_id = ? AND guild_id = ?", (role.id, interaction.guild.id))
                await interaction.send(f"Le rôle {role.mention} a été supprimé des rôles pouvant voir les tickets.", ephemeral=True)
            else:
                await interaction.send(f"Le rôle {role.mention} n'est pas présent dans les rôles pouvant voir les tickets.", ephemeral=True)
        await self.bot.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(RemoveRole(bot))