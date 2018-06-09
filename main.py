import discord
import asyncio
import configparser

# Read config File
config = configparser.ConfigParser()
config.read('config.ini')

token = config['general']['token'] #read unique token from config file
scripts_items = config.items('scripts') #read list of scripts and file locations from config file

scripts_names = []
scripts_content = []

for key, script in scripts_items:
    templist = []
    f = open(script)
    for line in f:
        templist.append(line.rstrip())
    f.close()
    scripts_names.append(key)
    scripts_content.append(list(filter(None, templist)))

scripts = dict(zip(scripts_names, scripts_content)) #zip script names and scripts together and format into dict

client = discord.Client()

help_message = 'To use, type "!script MOVIENAME". The following movies are available: {}'.format(scripts_names)
error_message = 'That command is invalid. Please type "!script help" for a list of titles available.'
send_error = 'User is not able to recieve messages from me'


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Shrek SuperSlam'))

@client.event
async def on_message(message):
    if message.content.startswith('!script'):
        command = message.content[len('!script'):].strip()
        if command.lower() == 'help':
            await client.send_message(message.channel, help_message)
        elif command in scripts_names:
            for line in scripts[command]:
                if line:
                    await client.send_message(message.author, line)
                    await asyncio.sleep(1)
        else:
            await client.send_message(message.author, error_message)

client.run(token)
#end
