import sqlite3
import requests    #importing requests will allow us to send http requests
from bs4 import BeautifulSoup    #used to parse html / xml

conn = sqlite3.connect("songlist.db")
cur = conn.cursor()

f = open('dj_token.txt', 'r')
token = f.read()

class Search():
    def __init__(self,cols="songID, name, artist",conds="year>1900"):
        self.cols = cols
        self.conds = conds
        self.songSearch()
    
    def songSearch(self):
        cur.execute("""Select {0} From allSongs where {1}""".format(self.cols,self.conds))
        self.info = cur.fetchall()

class Song():
    '''Song object
    
    Parameters
    ----------
    Song title : str
        Full title of song as determined by database search.
    
    Attributes
    ----------
    songID: int
        unique integer identifier
    name: str
        name of the song
    artist: str
        artist of the song
    genre: str
        2 letter genre identifier
    year: int
        year song was produced
    duration: int
        how long, in seconds, the song lasts
    wordCount: int
        number of words in the song
    '''
    
    def __init__(self, songID):
        self.songID = songID
        self.info()
        self.request_song_info()
        pass
    
    def info(self):
        cur.execute("""Select name, artist, genre,
        year, duration, wordCount From allSongs where songID={}""".format(self.songID))
        info = cur.fetchall()[0]
        self.name = info[0]
        self.artist = info[1]
        self.genre = info[2]
        self.year = info[3]
        self.duration = info[4]
        self.wordCount = info[5]
    
    def request_song_info(self):
        """"""
        song_title = self.name
        artist_name = self.artist
        base_url = 'https://api.genius.com'
        headers = {'Authorization': 'Bearer ' + token}
        search_url = base_url + '/search'
        data = {'q': song_title + ' ' + artist_name}
        response = requests.get(search_url, data=data, headers=headers)
        json = response.json()
        self.genius_name = json['response']['hits'][0]['result']['full_title']
        self.url = json['response']['hits'][0]['result']['url']    
    
    def lyrics(self):
        page = requests.get(self.url)
        html = BeautifulSoup(page.text, 'html.parser')
        self.lyrics_out = html.find('div', class_='lyrics').get_text()
        print(self.lyrics_out)
        
    def play(self,lyrics=False):
        pass
        # Play the song audio.
