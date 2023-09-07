import nextcord, os
from nextcord.ext import commands
from nextcord import Interaction, ChannelType, SlashOption
from nextcord.abc import GuildChannel

class LogChannel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="logchannel", description="Définir le salon ou les logs seront inscrits", guild_ids=[int(os.getenv("DISCORD_TEST_ID"))])
    async def log_channel(self, interaction: Interaction, channel: GuildChannel = SlashOption(
        channel_types=[ChannelType.text],
        description="Le salon ou les logs seront inscrits",
    )):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT channel_id FROM log_channels WHERE guild_id = ?", (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE log_channels SET channel_id = ? WHERE guild_id = ?", (channel.id, interaction.guild.id))
            else:
                await cursor.execute("INSERT INTO log_channels (channel_id, guild_id) VALUES (?, ?)", (channel.id, interaction.guild.id))
            await interaction.send(f"Le salon {channel.mention} vient d'être défini comme salon de logs.", ephemeral=True)
        await self.bot.db.commit()

def setup(bot: commands.Bot):
    bot.add_cog(LogChannel(bot))