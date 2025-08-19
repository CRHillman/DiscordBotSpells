import os
import discord
import requests
from homebrew import blairs
from dotenv import load_dotenv
from initiative_tracker import InitiativeTracker
from spell_retriever import get_spell

# load the environment variables
load_dotenv()

TOKEN = os.environ['TOKEN']

COMMANDS = [
    '* !init `<number>`\nStart a new initiative tracker for `<number>` participants. The bot will collect the previous `<number>` valid initiative entries from the channel (ignoring lines starting with `!`).',
    '* !add `<name>`: `<initiative_value>`\nAdd a participant to the initiative tracker with the specified initiative value.',
    '* !remove `<name>` or !rm `<name>`\nRemove a participant by `<name>` from the initiative tracker.',
    '* !swap `<name1>` | `<name2>` or !switch `<name1>` | `<name2>`\nSwap the initiative label, but not value, of two participants.',
    '* !help\nList all available commands.',
	"* !`<spell_name>`\nRetrieve a spell by name from the homebrew database, then the D&D wiki. Spaces and dashes are equivalent, and apostrophes are ignored: so `Tenser's Transformation`, and `tensers-transformation` are correct commands.",
]

# a basic intents object to start, then edit
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# create the bot
client = discord.Client( intents=intents )
init_tracker = InitiativeTracker()

# when it logs on
@client.event
async def on_ready():
	print( f'{client.user} is now online!' )


# when a message appears
@client.event
async def on_message( message ):
	# print( message.content )

	# to break the loop
	if ( message.author == client.user ):
		return

	if ( message.content.startswith( '!' ) ):
		if message.content.startswith('!init '):
			try:
				init_tracker.clear()  # Clear previous entries before starting a new initiative tracker
				msg = await init_tracker.new_initiative( message )
				# print the tracker
				await message.channel.send(msg + str(init_tracker))
			except (IndexError, ValueError):
				await message.channel.send('Please provide a valid number after !init.')

		elif message.content.startswith('!add '):
			try:
				# Usage: !add <name>: <initiative_value>
				parts = message.content[len('!add '):].split(':', 1)
				if len(parts) != 2:
					raise ValueError
				name = parts[0].strip()
				value = int(parts[1].strip())
    
				if not name:
					raise ValueError
 
				init_tracker.add(name, value)
    
    			# print the tracker
				await message.channel.send(init_tracker)
    
			except Exception as e:
				print(f'Error adding initiative: {e}')
				await message.channel.send('Usage: !add <name>: <initiative_value>')
    
		elif message.content.startswith('!remove') or message.content.startswith('!rm'):
			try:
				# Usage: !remove <name> or !rm <name>
				if message.content.startswith('!remove '):
					name = message.content[len('!remove '):].strip()
     
				elif message.content.startswith('!rm '):
					name = message.content[len('!rm '):].strip()
     
				else:
					raise IndexError
 
				if not name:
					raise IndexError
 
				init_tracker.remove(name)
    
				# print the tracker
				await message.channel.send(init_tracker)
    
			except IndexError:
				await message.channel.send('Usage: !remove <name> or !rm <name>')

		elif message.content.startswith('!swap') or message.content.startswith('!switch'):
			try:
				# Usage: !swap <name1> | <name2> or !switch <name1> | <name2>
				if message.content.startswith('!swap '):
					args = message.content[len('!swap '):].split('|', 1)
     
				elif message.content.startswith('!switch '):
					args = message.content[len('!switch '):].split('|', 1)
     
				else:
					raise IndexError

				if len(args) != 2:
					raise IndexError

				name1 = args[0].strip()
				name2 = args[1].strip()

				if not name1 or not name2:
					raise IndexError

				init_tracker.swap(name1, name2)
    
				# print the tracker
				await message.channel.send(init_tracker)

			except IndexError:
				await message.channel.send('Usage: !swap <name1> | <name2> or !switch <name1> | <name2>')
   
		elif message.content.startswith('!help'):
			# print the commands
			commands_message = 'Available commands:\n'
			for command in COMMANDS:
				commands_message += f'{command}\n'

			await message.channel.send(commands_message)

		else:
			await get_spell( message )

# always needed at the end
client.run( TOKEN )
