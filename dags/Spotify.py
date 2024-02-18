import spotipy
import spotipy.util as util
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Spotify:

    def __init__(self):
        self.CLIENT_ID = config['CREDENCIAIS']['CLIENT_ID']
        self.CLIENT_SECRET = config['CREDENCIAIS']['CLIENT_SECRET']
        self.USERNAME = config['CREDENCIAIS']['USERNAME']
        self.SCOPE = config['CREDENCIAIS']['SCOPE']
        self.REDIRECT_URL = config['CREDENCIAIS']['REDIRECT_URL']
        token = util.prompt_for_user_token(client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET, username=self.USERNAME, scope=self.SCOPE, redirect_uri=self.REDIRECT_URL)
        self.spot = spotipy.Spotify(auth=token)

    def get_artist_id(self, name: str):
        '''
            Description: 
                - Return the artist id based on their name

            Parameters: 
                - name: name of the artist
        '''
        busca = self.spot.search(name)
        items = busca['tracks']['items']
        return items
        
    def get_artist_albums(self, id: str):
        '''
            Description: 
                - Return the albums of an artist based on their id

            Parameters: 
                - id: id of the artist
        '''
        albuns_do_artista = self.spot.artist_albums(id)
        albuns = albuns_do_artista['items']
        return albuns
    
    def get_related_artists(self, id: str):
        '''
            Description: 
                - Return the related artists and their popularity based on the artist id

            Parameters: 
                - id: id of the artist
        '''
        related = self.spot.artist_related_artists(id)['artists']
        return related
    
    def get_top_tracks(self, id: str, country: str):
        '''
            Description: 
                - Return the artist's top tracks on the desired country

            Parameters: 
                - id: id of the artist
                - country: name of the country
        '''
        top = self.spot.artist_top_tracks(id, country)['tracks']
        return top
    
    def get_user_playlists(self):
        '''
            Description: 
                - Return the names of the playlists of the current user
        '''
        playlists = self.spot.current_user_playlists()['items']
        return playlists
        
    def get_user_top_tracks(self, ti, **kwargs):
        '''
            Description: 
                - Get the most heard tracks by the user
        '''
        top_tracks = self.spot.current_user_top_tracks(limit=kwargs['limit'], offset=0,time_range=kwargs['time_range'])['items']  
        ti.xcom_push(key='user_top_tracks', value=top_tracks)         

    def get_recommendations(self):
        '''
            Description: 
                - Based on the most heard songs of the user, get the recommended songs
        '''
        tracks = self.get_user_top_tracks()['uri']
        recommendations=[]

        for track in tracks:
            recommended_songs = self.spot.recommendations(seed_tracks=[track])['tracks']
            for song in recommended_songs:
                recommendations.append((song['name'],song['id']))

        return recommendations