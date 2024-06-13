import os
import json

files_to_make = ["links.json", "reminders.json", "role_mappings.json", "config.json", "discord_key.json", "WelcomeUsers.json", "JURISDICTION.json"]

for file in files_to_make:
    os.system(f"mkdir ./Settings && touch {file}")
    print(f"Setup: Created {file}")