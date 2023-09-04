import os, aiosqlite
from nextcord.ext import commands
from nextcord import Intents
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
            self.add_view(CreateTicket(self))
            self.add_view(TicketSettings())
            self.persistent_views_added = True
            print("Added persistent view to bot.")
            # Créer la base de données
            self.db = await aiosqlite.connect("tickets.sqlite")
            async with self.db.cursor() as cursor:
                await cursor.execute("CREATE TABLE IF NOT EXISTS roles (role_id INTEGER, guild_id INTEGER)")
            print("Connected to database.")
        print(f"{self.user} has connected to Discord!")

bot = Bot(intents = Intents.all())

# Load every commands in the commands folder
for file in os.listdir("commands"):
    if file.endswith(".py"):
        bot.load_extension(f"commands.{file[:-3]}")
    
bot.run(os.getenv("TOKEN"))