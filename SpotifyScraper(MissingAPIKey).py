import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

# davidcorcoran7 user Information
clientID = "f56a0a221a36493099730be85873126a"
clientSecret = "52a7420b9ae64e0fbe137712dff96949"
userID = "david.corcoran7"

client_credentials_manager = SpotifyClientCredentials(client_id= clientID,
                                                      client_secret=clientSecret)

# Allow spotipy to read top tracks info
scope = "user-top-read"

# Set up Spotify OAuth with your client ID, Client Secret, and Redirect URI
sp_oauth = SpotifyOAuth(client_id = clientID,
                        client_secret = clientSecret,
                        redirect_uri = 'https://www.google.com/',
                        scope = scope)

# Get an access token
token_info = sp_oauth.get_access_token() # If access token exists, write token_info = sp.oauth.get_access_token(), if not then token_info = sp_oauth.get_cached_token()
access_token = token_info['access_token']


#Relay error if token not found
if not access_token:
    print("Access token not found")

# Create a Spotipy instance with the access token
sp = spotipy.Spotify(auth = access_token)

# Constants for printing and filtering
timeRanges = ["short_term", "medium_term", "long_term"]
timeRangeMeaning = ["4 weeks", "6 months", "Account Lifetime"]
titles = ["SONG", "ARTIST"]

spacing = 35
numTracks = 25

#Search eachtime frame for top tracks
for timeRange in timeRanges:
    # Search current timframe for top tracks
    topTracks = sp.current_user_top_tracks(limit = numTracks, time_range = timeRange)["items"]

    # Print timeframe titles
    print(f"Top Tracks Over {timeRangeMeaning[timeRanges.index(timeRange)]}")
    print(f"{'':-<50}")
    print(f"{titles[0]:<{spacing}}{titles[1]}")
    print(f"{'':-<50}")

    # Keep list of all tracks/artists
    topTrackNames = []
    topTrackArtists = []

    # Pull out track names and artists into lists
    for track in topTracks:
        trackName = track["name"]
        topTrackNames.append(trackName)
        trackArtistID = track["artists"][0]["id"]
        trackArtist = sp.artist(trackArtistID)["name"]
        topTrackArtists.append(trackArtist)

    # Splice track names and artists if their lengths are large for formatting, then print
    for i in range(len(topTrackNames)):
        trackName = topTrackNames[i]
        if len(trackName)> 30:
            trackName = trackName[0:27] + "..."

        trackArtist = topTrackArtists[i]
        if len(trackArtist)> 30:
            trackArtist = trackArtist[0:27] + "..."

        print(f"{trackName: <35}{trackArtist}")

    # Maintaining spacing between timeframes
    print()