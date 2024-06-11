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
        self.servers = loadconfig("Settings/JURISDICTION.json")
        self.roles_mapping = loadconfig("Settings/role_mappings.json")

        self.key = key.get("DiscordAPI")
        self.prefix = config.get("Command_Prefix")
        self.UIName = config.get("UIName")
        self.disallowed_words = config.get("disallowed-words")
        self.warning_message = config.get("warning_message")
        self.authorised_users = config.get("Authorised_Users")
        self.incoming_servers = self.servers.get("servers")
        self.port = config.get("default-port")

        self.discordintents = nextcord.Intents.default()
        self.discordintents.message_content = True
        self.discordintents.reactions = True

        self.client = commands.Bot(command_prefix=self.prefix, intents=self.discordintents)
        self.client.event(self.on_member_join)
    
    def authorise_guild(self, message):
        with open("./Settings/JURISDICTION.json", "w+") as jurisfile:
            self.servers["servers"].append(str(message.guild))
            json.dump(self.servers, jurisfile, indent=4)

    def welcome_users(self, message):
        with open("./Settings/WelcomeUsers.json", "w+") as welcomefile:
            welcomelist = json.load(welcomefile)
            welcomelist["servers"].append(str(message.guild))
            json.dump(welcomelist, welcomefile, indent=4)
        
    async def on_member_join(self, member):
            if str(member.guild) in self.welcomelist:
                welcome_message = f"Welcome to {member.guild.name}, {member.mention}!"
                channel = member.guild.system_channel
                if channel is not None:
                    await default_channel.send(welcome_message)

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

            if str(self.prefix) in str(message.content):
                commandmessage = str(message.content.lower())

                if "authorise" in commandmessage:
                        if message.author.guild_permissions.administrator:
                            self.authorise_guild(message)
                            await message.reply(f"{str(message.guild)} has now been added to my list of authorised servers.")
                
                elif "create link" in commandmessage:
                        print("Understood.")
                        if message.author.guild_permissions.administrator:
                            server = message.guild
                            commandmessage = commandmessage.replace(self.prefix, "")
                            linkid = commandmessage.replace("create link ", "")
                            print(linkid)
                            with open("./long_term_memory/links.json", "r") as linkfile:
                                existing_links = json.load(linkfile)
                                for link in existing_links["links"]:
                                    print(link)
                                    if link.get("link_id") in str(linkid):
                                        link["channels"].append(message.channel)
                                        print(link)
                                        break
                            with open("./long_term_memory/links.json", "w") as linkfile:
                                json.dump(existing_links, linkfile, indent=4)
        
                elif "welcome-users" in commandmessage:
                        if message.author.guild_permissions.administrator:
                            self.welcome_users(message)
                            await message.reply(f"{str(message.guild)} has been added to the list of servers which I should welcome new users to.")
    
                if str(message.guild) in self.incoming_servers:
                    user = message.author
                    roles_mapping = self.roles_mapping
                    if "role" in commandmessage:
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
                    elif "clear" in message.content.lower():
                        if message.author.guild_permissions.manage_messages:
                            try:
                                fullcommand = str(message.content.lower())
                                amount = fullcommand.replace(f"{self.prefix}", "")
                                amount = amount.replace("clear", "")
                                amount = amount.replace(" ", "")
                                intamount = int(amount)
                                await message.channel.purge(limit=intamount + 1)
                                await message.channel.send(f"{amount} messages deleted by {message.author.mention}")
                            except ValueError:
                                await message.channel.send("Please provide a valid number of messages to delete.")
                        else:
                            await message.channel.send("You don't have permission to delete messages.")
                else:
                    await message.reply("I am not permitted to perform administrative actions in this guild.")

            elif self.UIName.lower() in message.content.lower() or message.guild is None or (message.reference and message.reference.resolved.author == self.client.user):
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
