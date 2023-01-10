import lyricsgenius
import random
import tweepy

# Dictionary containing Twitter API keys and access tokens
keys = {
    'CONSUMER_API_KEY': 'RbpoSsPXso8M5xN6gkQ5tMcTI',
    'CONSUMER_API_SECRET_KEY': 'qis9rGl2C7QpPpWDwianyG7Jbs15mgggzvIbOJEJ41bnZH11ab',
    'ACCESS_TOKEN': '1606516155035828225-woHELP3iVUreEwD4cpVx8CF7L55Oqy',
    'ACCESS_TOKEN_SECRET': 'Mb4DPrCW8T7VGhWOa9u92lYlMSYcoDp09P2j5R9luVafE'

}

# List of Bladee songs
all_songs = ["Be Nice 2 Me", "Obedient", "I’m Goofy", "Hotel Breakfast", "Sugar", "Who Goes There", "Decay",
             "Into Dust", "Lovenote", "Mallwhore FreEestyle", "For You", "Gatekeeper", "Lordship", "So What",
             "Gotham City", "Vanilla Sky", "Reality Surf", "Topman", "deletee (intro)", "Romeo", "Dumpster Baby",
             "Bloodveil / Stillborn",
             "Skin",
             "Best Buy",
             "unreal",
             "Side by Side",
             "Trash Star",
             "Rip",
             "Frosty the Snowman",
             "I Think...",
             "SmartWater",
             "Waster",
             "Noblest Strive",
             "Hero of My Story 3style3",
             "Wrist Cry",
             "Nike Just Do It",
             "Apple",
             "Steve Jobs",
             "Special Place",
             "Missing Person",
             "1D",
             "Westfield",
             "College Boy",
             "Cherry Bracelets",
             "Plastic Surgery",
             "Golden Boy",
             "Close",
             "Psycho",
             "Blood Rain",
             "Puppet Master",
             "Anything",
             "It Suxx",
             "Keys to the City",
             "shadowface",
             "Thee 9 Is Up",
             "OKK",
             "Doorman",
             "Jaws",
             "Let’s Ride",
             "Trendy",
             "Knightsbridge",
             "Redlight Moments",
             "Wickr Man",
             "Fake News",
             "The Fool Intro",
             "Xd Out",
             "For Nothing",
             "Hex",
             "Cartier’god Icedancer (Intermission)",
             "Inside Out",
             "WALLET WONT FOLD",
             "50SACINMYSOCIDGAF",
             "DRAIN STORY",
             "Butterfly",
             "LOVESTORY",
             "D-925",
             "safehouse",
             "BBY",
             "Mean Girls",
             "Botox Lips",
             "Rain Check",
             "WONDERLAND",
             "Under Your Spell",
             "Subaru",
             "Like a Virgin",
             "Sick",
             "No Life Left",
             "7-Eleven",
             "MJ",
             "Linkdin",
             "spellbound",
             "Cover Up",
             "Backstr€€t Boys",
             "Wings in Motion",
             "ICARUS 3REESTYLE",
             "Innocent of All Things",
             "That Thing You Do",
             "Numb/Beverly Hills",
             "Im Not Tired",
             "Valerie",
             "Don’t Worry",
             "It Girl",
             "Suffocation",
             "DG Jeans",
             "MERRY-GO-ROUND",
             "everlasting flames",
             "Oh Well",
             "Only One",
             "Carwash",
             "Inspiration Comes",
             "Destroy Me",
             "I AM SLOWLY BUT SURELY LOSING HOPE",
             "Swan Lake",
             "desiree",
             "HAHAH",
             "I Want It That Way",
             "facetime",
             "DiSASTER PRELUDE",
             "Birdbath",
             "2beloved",
             "My Magic Is Strong",
             "RAIN3OW STAR (LOVE IS ALL)",
             "UNDERSTATEMENT",
             "IMAGINARY",
             "Scarecrows",
             "Ghost Hands",
             "I.E.E.",
             "Bladeecity",
             "Insect",
             "The Silent Boy Cries (Ripsquadd Outro)",
             "NOTHINGG",
             "FML",
             "OXYGEN",
             "Search True",
             "4am",
             "OPEN SYMBOLS (PLAY)  BE IN YOUR MIND",
             "Dragonfly",
             "freeze",
             "Finder",
             "DNA RAIN",
             "BLUE CRUSH ANGEL",
             "100s",
             "EVERY MOMENT SPECIAL",
             "Feel Like",
             "Exstasia",
             "DRESDEN ER",
             "Wett (Water2)",
             "She’s Always Dancing",
             "MIRROR (HYMN) (INTRO)",
             "upgrade enabled",
             "Anywhere",
             "Velociraptor",
             "ITS OK TO NOT BE OK",
             ]


def get_raw_lyrics():
    # Set the access token for the Genius API client
    genius_client_access_token = "d7f9UAnW4NyR7aB8SkI2x4EgGsJeDiRD2ZDV5VhR3hwpms3tNmbuVpIG-lHIC-VO"

    # Initialize the Genius API client
    genius = lyricsgenius.Genius(genius_client_access_token)

    # Select a random song from the list of Bladee songs
    random_song_title = random.choice(all_songs)

    # Search for and retrieve the lyrics for the selected song using the Genius API
    lyrics = genius.search_song(random_song_title, "Bladee").lyrics

    # Convert the song title to all uppercase
    song = random_song_title.upper()

    # Return the lyrics and song title
    return lyrics, song


def get_tweet_from(lyrics):
    # Split the lyrics into a list of lines
    lines = lyrics.split('\n')

    # Replace empty lines and lines containing brackets with a placeholder string
    for index in range(len(lines)):
        if lines[index] == "" or "[" in lines[index]:
            lines[index] = "XXX"

    # Remove the placeholder strings from the list
    lines = [i for i in lines if i != "XXX"]

    # Select a random index from the list of lines
    random_num = random.randrange(0, len(lines) - 1)

    # Check if the selected line contains the "You might also like" string
    if "You might also like" in lines[random_num]:
        # If it does, remove the string and all the following characters from the line
        lines[random_num] = lines[random_num][:lines[random_num].index("You might also like")]

    # Check if the line following contains the "You might also like" string
    if "You might also like" in lines[random_num + 1]:
        # If it does, remove the string and all the following characters from the line
        lines[random_num + 1] = lines[random_num + 1][:lines[random_num + 1].index("You might also like")]

    # Construct the tweet by combining the line at the selected index with the line following it
    tweet = lines[random_num] + "\n" + lines[random_num + 1]

    # Replace backslashes in the tweet with nothing
    tweet = tweet.replace("\\", "")

    # Return the constructed tweet
    return tweet


def handler(event, context):
    # Initialize the Twitter API client using the provided keys and access tokens
    auth = tweepy.OAuthHandler(
        keys['CONSUMER_API_KEY'],
        keys['CONSUMER_API_SECRET_KEY']
    )
    auth.set_access_token(
        keys['ACCESS_TOKEN'],
        keys['ACCESS_TOKEN_SECRET']
    )
    api = tweepy.API(auth)

    # Retrieve the lyrics and song title for a random Bladee song
    lyrics, song = get_raw_lyrics()

    # Construct a tweet from the retrieved lyrics
    tweet = get_tweet_from(lyrics)

    # Tweet the constructed tweet
    status = api.update_status(tweet)

    # Return the tweet
    return tweet
