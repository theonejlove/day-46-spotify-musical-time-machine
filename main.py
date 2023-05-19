from datetime import date
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_SECRET"],
        show_dialog=True,
        cache_path="token.txt",
    )
)

user_id = sp.current_user()["id"]
date_input = input("Which year do you want to travel to? Type the date in a YYYY-MM-DD format: ")

URL = f"https://www.billboard.com/charts/hot-100/{date_input}/"

response = requests.get(URL)
site_html = response.text

soup = BeautifulSoup(site_html, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

song_uris = []
year = date_input.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pass

new_playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False,
                                       collaborative=False, description="a project")
sp.playlist_add_items(playlist_id=new_playlist["id"], items=song_uris)


