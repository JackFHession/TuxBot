from utils.utils import *

import nextcord
from nextcord import FFmpegPCMAudio
from nextcord.ext import commands
import asyncio
import json
import glob

from AI.Inverter import *
from AI.ThirdParty import *
from AI.IntentClassifier import *

class Discord:
    def __init__(self):
        self.discordintents = nextcord.Intents.default()
        self.discordintents.message_content = True
        self.discordintents.reactions = True

        self.prefix = "!"

        self.client = commands.Bot(command_prefix=self.prefix, intents=self.discordintents)
#        self.client.event(self.on_member_join)

        with open("./long_term_memory/Discord_API.json") as file:
            data = json.load(file)
        
        self.Settings = read_json("./long_term_memory/Settings.json")

        self.API_Key = data.get("API_Key")

        self.Responder = Inverter()
        self.AI = Classifier()
        self.Eureka = Eureka_Connect()

        self.UIName = self.Settings.get("UIName")

    def activate_bot(self):
        @self.client.event
        async def on_message(message):
            if message.author == self.client.user:
                return
            
            if self.UIName.lower() in message.content.lower() or message.guild is None or (message.reference and message.reference.resolved.author == self.client.user):
                await message.channel.trigger_typing()

                sentence = message.content
                try:
                    ResponseOutput = self.Eureka.send_request(sentence)
                except:
                    ResponseOutput = self.Responder.invert_phrase(sentence)
                    if ResponseOutput == "Null.":
                        ResponseOutput = random.choice(intent_class["responses"])
                
                await message.reply(ResponseOutput)
        
        print(f"Logged in.")
        self.client.run(self.API_Key)