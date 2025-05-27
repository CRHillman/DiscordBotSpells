from homebrew import *
import requests

def remove_html( source ):

	ignore = False
	multi_space = False

	wording = ''

	for char in source:
		# ignore tags
		if ( char in '<' ):
			ignore = True

		# read other things
		if not ignore:
			# ampersands are weird
			if ( char in '&' ):
				wording += '\n'
				ignore = True

			else:
				# avoid wasting characters on spaces
				if ( char in ' ' ) and ( multi_space ):
					pass

				else:
					wording += char
					multi_space = False

		# stop ignoring because tag ended
		if ( char in '>;' ):
			ignore = False

		# ignore multiple spaces
		elif ( char in ' ' ):
			multi_space = True

	return wording


def add_styling( source ):

	replacements = [
		( "<strong>", '**' ), 
		( "</strong>", '**' ), 
		( "&quot;", '"' )
	]

	styled = source

	for old, new in replacements:
		styled = styled.replace( old, new )

	return styled


def clean( string ):
	'''
	Converts spaces, dashes, and slashes into hyphens
	'''
	cleaned = str()

	for char in string:
		if ( char in ' -/' ):
			cleaned += '-'

		if ( char.isalpha() ):
			cleaned += str( char )

	return cleaned


async def get_spell(message):
    spell = clean( message.content ).lower()

    try:
        wording = blairs[spell]
        # break into message-sized pieces
        parts = ( len( wording ) // 2000 ) + 1

        # print spell name
        await message.channel.send( '***' + message.content[1:].upper() + '***' )

        # send all the pieces
        for i in range( parts ):
            try:
                await message.channel.send( wording[( i * 2000 ):( i + 1 ) * 2000] )

            except:
                pass
        return

    except KeyError:
        pass

    site = 'http://dnd5e.wikidot.com/spell:' + spell

    #await message.channel.send(	site	)

    response = requests.get( site )

    phrase = '<div class="content-separator" style="display: none:"></div>'

    wording_start = response.text.find( phrase ) - 1

    wording_end = response.text.find( phrase, wording_start + len( phrase ) + 1 )

    #print(	"Wording start: ", wording_start	)
    #print(	"Wording end: ", wording_end	)

    wording = add_styling( response.text[wording_start:wording_end] )

    wording = remove_html( wording )

    # break into message-sized pieces
    parts = ( len( wording ) // 2000 ) + 1

    # if there is no spell to find
    if ( len( wording ) == 1 ):
        await message.channel.send( 'No spell named: "' + message.content[1:] + '" found.' )

    else:
        # print the spell name
        await message.channel.send( '***' + message.content[1:].upper() + '***' )
        for i in range( parts ):
            # send all the pieces
            try:
                await message.channel.send( wording[( i * 2000 ):( i + 1 ) * 2000] )

            except:
                pass