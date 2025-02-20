import requests
import base64

CLIENT_ID = 'db1e53dfbfdc4ebe83c39a8bc7ec1d81'
CLIENT_SECRET = '3d68bcd2b43942a4ac3bc2e4031120ba'


def get_access_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode('utf-8'),
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    auth_data = {'grant_type': 'client_credentials'}

    response = requests.post(auth_url, headers=auth_header, data=auth_data)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print("Error fetching access token")
        return None


def get_artist_data(artist_id, access_token):
    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(artist_url, headers=headers)

    if response.status_code == 200:
        artist_data = response.json()
        name = artist_data['name']
        popularity = artist_data['popularity']
        followers = artist_data['followers']['total']

        print(f"Artist: {name}")
        print(f"Popularity: {popularity}")
        print(f"Followers: {followers}")
        print(f"Genres: {', '.join(artist_data['genres'])}")
    else:
        print("Error fetching artist data")


def get_top_tracks(artist_id, access_token):
    top_tracks_url = f'https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(top_tracks_url, headers=headers)

    if response.status_code == 200:
        top_tracks_data = response.json()
        print("-" * 40)
        for track in top_tracks_data['tracks']:
            track_name = track['name']
            track_popularity = track['popularity']
            track_id = track['id']

            print(f"Track: {track_name}")
            print(f"Popularity: {track_popularity}")
            print(f"Track ID: {track_id}")
            print("-" * 40)
    else:
        print("Error fetching top tracks")


artist_id = '2MC67O2xkG8buXrq1cRGCN'
access_token = get_access_token()
if access_token:
    get_artist_data(artist_id, access_token)
    get_top_tracks(artist_id, access_token)
