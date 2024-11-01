import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from statistics import mode

SpotipyURL = "https://spotipy.readthedocs.io/en/2.22.1/"
SpotifyForDevelopersWebsite = "https://developer.spotify.com/"

# davidcorcoran7 user Information
clientID = "insert_client_ID"
clientSecret = "insert_client_Secret"
userID = "insert_user_ID"

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
#token_info = sp_oauth.get_cached_token()
access_token = token_info['access_token']

#Relay error if token not found
if not access_token:
    print("Access token not found")

# Create a Spotipy instance with the access token
sp = spotipy.Spotify(auth = access_token)

#global variable used to keep the program running if the user wants to look at further data
selectedTimeRange = ""

# Function prompting the user to select the time period that the program will pull from
# If the input is incorrect, it will default to All-Time
def inputTimeRange():
    print("")
    timeRange = input("Look at song data from 4 weeks, 6 months, or all time?  ")
    short = ["4", "4 weeks", "4 Weeks", "4 WEEKS", "4weeks", "4Weeks", "4WEEKS"]
    medium = ["6", "6 months", "6 Months", "6 MONTHS", "6months", "6Months", "6MONTHS"]

    if timeRange in short:
        globals()["selectedTimeRange"] = "short_term"
    elif timeRange in medium:
        globals()["selectedTimeRange"] = "medium_term"
    else:
        globals()["selectedTimeRange"] = "long_term"


# Function to ask for user input time period selection
def printTracks(timeRange):

    # The number of tracks that will be printed and analyzed
    numTracks = 25

    # API call to pull user top tracks
    topTracks = sp.current_user_top_tracks(limit = numTracks, time_range = timeRange)["items"]

    # Constants for printing and filtering
    spacing = 35
    titles = ["SONG", "ARTIST"]
    timeRanges = ["short_term", "medium_term", "long_term"]
    timeRangeMeaning = ["4 weeks", "6 months", "Account Lifetime"]

    # Print timeframe titles
    print("")
    print(f"Top Tracks Over {timeRangeMeaning[timeRanges.index(timeRange)]}")
    print(f"{'':-<50}")
    print(f"{titles[0]:<{spacing}}{titles[1]}")
    print(f"{'':-<50}")

    # Lists to hold all pulled tracks/artists
    topTrackNames = []
    topTrackArtists = []

    # Pull out track names and artists and place them into lists
    for track in topTracks:
        trackName = track["name"]
        topTrackNames.append(trackName)
        trackArtistID = track["artists"][0]["id"]
        trackArtist = sp.artist(trackArtistID)["name"]
        topTrackArtists.append(trackArtist)

    # Splice track names and artists if their lengths are too large for formatting, then print
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

def trackData(timeRange):
    # The number of tracks that will be printed and analyzed
    numTracks = 25

    # API call to pull user top tracks
    topTracks = sp.current_user_top_tracks(limit = numTracks, time_range = timeRange)["items"]

    # Keep list of all tracks/artists
    topTrackRuntimes = []
    topTrackArtists = []

    # Pull out song runtimes and artists and add to respective lists
    for track in topTracks:
        runtime = track["duration_ms"] / 1000
        topTrackRuntimes.append(runtime)

        trackArtistID = track["artists"][0]["id"]
        trackArtist = sp.artist(trackArtistID)["name"]
        topTrackArtists.append(trackArtist)

    # Calculate and print average song runtime
    totalRuntime = 0
    for runtime in topTrackRuntimes:
        totalRuntime += runtime
    averageRuntime = totalRuntime/numTracks
    print("Average Song Runtime: " + str(averageRuntime) + " seconds")

    # Calculate and print the most listened to artist from selection
    mostListenedArtist = mode(topTrackArtists)

    mostListenedArtistCount = 0
    for artists in topTrackArtists:
        if artists == mostListenedArtist:
            mostListenedArtistCount += 1
        else:
            pass

    print("Most Popular Artist: " + mostListenedArtist + " - " + str(mostListenedArtistCount) + "/" + str(numTracks) + " Top Songs")

    # Maintaining spacing
    print()


# Function to prompt the user to search a different time period or exit the program
def reentry():
    result = input("Look at more data? Yes/No  ")
    yesOptions = ["Yes", "yes", "YES", ""]
    if result in yesOptions:
        globals()["active"] = True
    else:
        globals()["active"] = False

# Main function for organization
active = True
def main():
    while globals()["active"] == True:
        inputTimeRange()
        printTracks(selectedTimeRange)
        trackData(selectedTimeRange)
        reentry()
main()
    