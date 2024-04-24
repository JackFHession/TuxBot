import nextcord
from nextcord import FFmpegPCMAudio
from nextcord.ext import commands
import asyncio
import json
from Utilities.functions import loadconfig, cprogram, DoFunction, mp3_tts, DeployFunction
import glob

class DiscordBot:
    def __init__(self):
        config = loadconfig("Settings/config.json")
        key = loadconfig("Settings/discord_key.json")
        servers = loadconfig("Settings/JURISDICTION.json")
        self.roles_mapping = loadconfig("Settings/role_mappings.json")

        self.key = key.get("DiscordAPI")
        self.prefix = config.get("Command_Prefix")
        self.UIName = config.get("UIName")
        self.disallowed_words = config.get("disallowed-words")
        self.warning_message = config.get("warning_message")
        self.authorised_users = config.get("Authorised_Users")
        self.incoming_servers = servers.get("servers")
        self.port = config.get("default-port")

        self.discordintents = nextcord.Intents.default()
        self.discordintents.message_content = True
        self.discordintents.reactions = True

        self.client = commands.Bot(command_prefix='/', intents=self.discordintents)

    def activate_bot(self):
        @self.client.event
        async def on_message(message):
            if str(message.guild) in self.incoming_servers:
                sentence_words = message.content
                for word in self.disallowed_words:
                    if word in sentence_words:
                        await message.delete()
                        response = await message.channel.send(self.warning_message)
                        await asyncio.sleep(4)
                        await response.delete()
                        break

            if self.prefix in message.content:
                user = message.author
                roles_mapping = self.role_mappings
                for role_keyword, role_name in roles_mapping.items():
                    if role_keyword in message.content:
                        try:
                            role = nextcord.utils.get(message.guild.roles, name=role_name)
                            await user.add_roles(role)
                            response = await message.reply(f"You now have the {role_name} rank!")
                            await asyncio.sleep(1)
                        except Exception as error:
                            response = await message.reply(f"Error: {error}")
                        await asyncio.sleep(4)
                        await message.delete()
                        await response.delete()
                        break

            if self.UIName.lower() in message.content.lower() or message.guild is None or (message.reference and message.reference.resolved.author == self.client.user):
                await message.channel.trigger_typing()

                sentence = message.content
                if message.author == self.client.user:
                    return

                cprogram(f'./Utilities/send_request http://localhost:{self.port} "{sentence}"')
                await asyncio.sleep(2)

                with open("./short_term_memory/output.txt", "r") as f:
                    ResponseOutput = f.read()

                with open("./short_term_memory/current_class.json", "r") as f:
                    intent_class = json.load(f)
                
                if intent_class.get("tag") == "sherlock":
                    results = ""
                    DeployFunction(intent_class)
                    file_paths = glob.glob("./Utilities/*.txt")
                    for file_path in file_paths:
                        with open(file_path, "r") as file:
                            results += file.read()
                            await message.reply(results)
                else:
                    DoFunction(intent_class)
                    await message.reply(ResponseOutput)

                try:
                    if message.guild.voice_client is None:
                        self.channel = nextcord.utils.get(message.guild.voice_channels, id=int('723270333523558455'))
                        self.vc = await self.channel.connect()
                except Exception as error:
                    print(f"{error}")

                try:
                    mp3_tts(ResponseOutput)
                    audio_source = FFmpegPCMAudio('./AudioFiles/output.mp3')
                    self.vc.play(audio_source, after=lambda e: print('done', e))
                except Exception as e:
                    print(f"Failed to join voice channel: {e}")

            await asyncio.sleep(2)

        print(f"Logged in.")
        self.client.run(self.key)
