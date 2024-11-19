import lyricsgenius
import random
import tweepy
import os

# Fetch a random song by searching for an artist
def fetch_random_song(genius, artist):
    artist_data = genius.search_artist(artist, max_songs=20)
    if artist_data:
        song = random.choice(artist_data.songs) 
        return {"title": song.title, "artist": artist_data.name}
    return None

# Fetch raw lyrics using the Genius API
def get_raw_lyrics(genius, artist, song_title):
    song = genius.search_song(song_title, artist)
    if song:
        return song.lyrics
    return None

# Process lyrics to create a post
def get_tweet_from(lyrics):
    if not lyrics:
        return None
    # Clean up the lyrics
    lines = [line.strip() for line in lyrics.split("\n") if line and "[" not in line]
    if len(lines) < 2:
        return None
    # Select two random consecutive lines for the post
    random_index = random.randint(0, len(lines) - 2)
    return f"{lines[random_index]}\n{lines[random_index + 1]}"

# X authentication and posting
def tweet_lyrics(api, tweet_content):
    try:
        api.update_status(tweet_content)
        print("Tweet posted successfully!")
    except tweepy.TweepError as e:
        print(f"Error posting tweet: {e}")

# Main function to run the bot
def main():
    genius_api_token = os.getenv("GENIUS_API_TOKEN")
    twitter_consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    twitter_consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    if not all([genius_api_token, twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_token_secret]):
        print("Error: Missing one or more required API keys. Please set them as environment variables.")
        return

    genius = lyricsgenius.Genius(genius_api_token)

    artists = ["Taylor Swift", "Ed Sheeran", "Adele", "Drake", "Beyoncé"]
    selected_artist = random.choice(artists)

    song_data = fetch_random_song(genius, selected_artist)

    if song_data:
        lyrics = get_raw_lyrics(genius, song_data["artist"], song_data["title"])
        tweet_content = get_tweet_from(lyrics)

        if tweet_content:
            auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
            auth.set_access_token(twitter_access_token, twitter_access_token_secret)
            api = tweepy.API(auth)

            tweet_lyrics(api, tweet_content)
        else:
            print("Unable to generate a tweet from the lyrics.")
    else:
        print("Unable to fetch song data. Please try again.")

if __name__ == "__main__":
    main()
