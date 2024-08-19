from AI.Inverter import *
from AI.ThirdParty import *
from AI.IntentClassifier import *

from server_internals.server import *
from server_internals.discord_bot import *

if __name__ == "__main__":

    port = 2041

    if len(sys.argv) > 1:
        mode = sys.argv[1]
    else:
        mode = input("Mode (server/discord): ")

    if mode.lower() == "server":
        start_server(port)
    elif mode.lower() == "discord":
        Bot = Discord()
        Bot.activate_bot()