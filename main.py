import os
import discord
import requests

TOKEN = os.environ['TOKEN']

# a basic intents object to start, then edit
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# create the bot
client = discord.Client(intents=intents)


# when it logs on
@client.event
async def on_ready():
  print(f'{client.user} is now online!')


# when a message appears
@client.event
async def on_message(message):
  #print(message.content)

  #to break the loop
  if (message.author == client.user):
    return

  if (message.content.startswith('!')):
    spell = clean(message.content)
    site = 'http://dnd5e.wikidot.com/spell:' + spell.lower()
    
    #await message.channel.send( site )

    response = requests.get(site)

    phrase = '<div class="content-separator" style="display: none:"></div>'

    wording_start = response.text.find( phrase ) - 1

    #print( response.text[wording_start:wording_start + 2000] )

    #print( '\n' )

    wording_end = response.text.find( phrase, wording_start + len(phrase) + 1 )

    #print( "Wording start: ", wording_start )
    #print( "Wording end: ", wording_end )

    wording = remove_html( response.text[wording_start:wording_end] )

    parts = ( len(wording)//2000 ) + 1

    # if there is no spell to find
    if ( len(wording) == 1 ):
      await message.channel.send( 'No spell named: "' + message.content[1:] + '" found.')
    else:
      # print the spell name
      await message.channel.send( '***' + message.content[1:].upper() + '***' )
      for i in range(parts):
        try:
          await message.channel.send( wording [ (i*2000):(i+1)*2000 ] ) 
            
        except:
          pass  
    

def clean(string):

  cleaned = str()

  for char in string:
    if (char in ' -/'):
      cleaned += '-'

    if (char.isalpha()):
      cleaned += str(char)

  return cleaned


def remove_html(source):

  ignore = False
  multi_space = False

  wording = ''

  for char in source:
    # ignore tags
    if (char in '<'):
      ignore = True
      
    # read other things
    if not ignore:
      # ampersands are weird
      if (char in '&'):
        wording += '\n'
        ignore = True

      else:
        # avoid wasting characters on spaces
        if (char in ' ') and (multi_space):
          pass
          
        else:
          wording += char
          multi_space = False

    # stop ignoring because tag ended
    if (char in '>;'):
      ignore = False
    
    # ignore multiple spaces
    elif (char in ' '):
      multi_space = True

  return wording

# always needed at the end
client.run(TOKEN)
