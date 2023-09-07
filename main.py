import os, aiosqlite
from nextcord.ext import commands
from nextcord import Intents, Activity, ActivityType
from dotenv import load_dotenv
from views.CreateTicket import CreateTicket
from views.TicketSettings import TicketSettings

load_dotenv(".env")

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persistent_views_added = False

    async def on_ready(self):
        if not self.persistent_views_added:
            # Créer la base de données
            self.db = await aiosqlite.connect("tickets.sqlite")
            async with self.db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role_id INTEGER, guild_id INTEGER)")
                # Remove categories table
                # await cursor.execute("DROP TABLE IF EXISTS categories")
                await cursor.execute("CREATE TABLE IF NOT EXISTS categories (message_id INTEGER, category_id INTEGER, guild_id INTEGER)")
                await cursor.execute("CREATE TABLE IF NOT EXISTS log_channels (channel_id INTEGER, guild_id INTEGER)")
                await cursor.execute("CREATE TABLE IF NOT EXISTS notifications (notification BOOL, guild_id INTEGER)")

                # Todo: better system to clear not existing guilds, not existing channels, not existing roles, etc...
            print("Connected to database.")

            self.add_view(CreateTicket(self))
            self.add_view(TicketSettings(self))
            self.persistent_views_added = True
            print("Added persistent view to bot.")

        await self.change_presence(
            activity=Activity(
                name=f"{len(self.guilds)} serveurs",
                type=ActivityType.watching,
            )
        )
        print(f"{self.user} has connected to Discord!")

bot = Bot(intents = Intents.all())

# Load every commands in the commands folder
for file in os.listdir("commands"):
    if file.endswith(".py"):
        bot.load_extension(f"commands.{file[:-3]}")
    
bot.run(os.getenv("TOKEN"))