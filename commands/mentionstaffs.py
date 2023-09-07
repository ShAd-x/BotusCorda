import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, SlashOption

class MentionStaffs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="mentionstaffs",
        description="Les rôles ayant le droit de voir les tickets doivent-ils être notifiés ?",
        guild_ids=[int(os.getenv("DISCORD_TEST_ID"))]
    )
    async def mention_staffs(self, interaction: Interaction, number: int = SlashOption(
        name="choix",
        description="Les rôles ayant le droit de voir les tickets doivent-ils être notifiés ?",
        choices={"Oui (Notifications)": 1, "Non (Pas de notifications)": 0},
    )):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT notification FROM notifications WHERE guild_id = ?", (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE notifications SET notification = ? WHERE guild_id = ?", (number, interaction.guild.id))
            else:
                await cursor.execute("INSERT INTO notifications (notification, guild_id) VALUES (?, ?)", (number, interaction.guild.id))
            await interaction.send(f"Les rôles ayant le droit de voir les tickets {'seront notifiés' if number else 'ne seront pas notifiés'}.", ephemeral=True)
        await self.bot.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(MentionStaffs(bot))