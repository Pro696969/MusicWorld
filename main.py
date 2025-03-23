import mysql.connector
from faker import Faker
import random

class MusicDatabasePopulator:
    def __init__(self):
        self.fake = Faker()
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password123',
            database='DBT25_A1_PES2UG22CS281_Krishna'
        )
        self.cursor = self.connection.cursor(dictionary=True)
        
    def populate_artists(self):
        artists = []
        for _ in range(10000):
            artist = {
                "Name": self.fake.name(),
                "Country": self.fake.country(),
                "BirthYear": random.randint(1950, 2005),
                "Biography": self.fake.text(max_nb_chars=500),
            }
            artists.append(artist)

        query = """
        INSERT INTO Artists (Name, Country, BirthYear, Biography) 
        VALUES (%(Name)s, %(Country)s, %(BirthYear)s, %(Biography)s)
        """

        try:
            # Execute batch insert
            self.cursor.executemany(query, artists)
            self.connection.commit()
            print(f"Successfully inserted {len(artists)} artists.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            self.cursor.close()

    def populate_genres(self):
        # Predefined genres with some hierarchy
        genres = [
            {'Name': 'Rock', 'Description': 'Guitar-driven music', 'ParentGenre': None},
            {'Name': 'Alternative Rock', 'Description': 'Experimental rock style', 'ParentGenre': 1},
            {'Name': 'Pop', 'Description': 'Popular contemporary music', 'ParentGenre': None},
            {'Name': 'Electronic Pop', 'Description': 'Pop music with electronic elements', 'ParentGenre': 3},
            {'Name': 'Hip Hop', 'Description': 'Rhythmic vocal music', 'ParentGenre': None},
            {'Name': 'Jazz', 'Description': 'Improvisational music', 'ParentGenre': None},
            {'Name': 'Blues', 'Description': 'Soulful and melancholic music', 'ParentGenre': None},
            {'Name': 'Classical', 'Description': 'Orchestral and instrumental music', 'ParentGenre': None},
            {'Name': 'Country', 'Description': 'Folk and western music', 'ParentGenre': None},
            {'Name': 'Reggae', 'Description': 'Jamaican music with a rhythmic style', 'ParentGenre': None},
            {'Name': 'Metal', 'Description': 'Heavy and aggressive music', 'ParentGenre': 1},
            {'Name': 'Punk Rock', 'Description': 'Fast-paced and rebellious rock', 'ParentGenre': 1},
            {'Name': 'R&B', 'Description': 'Rhythm and blues music', 'ParentGenre': None},
            {'Name': 'Soul', 'Description': 'Emotional and expressive music', 'ParentGenre': 13},
            {'Name': 'Funk', 'Description': 'Groovy and rhythmic music', 'ParentGenre': 13},
            {'Name': 'Disco', 'Description': 'Dance music with a steady beat', 'ParentGenre': 3},
            {'Name': 'Techno', 'Description': 'Electronic dance music', 'ParentGenre': 4},
            {'Name': 'House', 'Description': 'Electronic dance music with a repetitive beat', 'ParentGenre': 4},
            {'Name': 'Trance', 'Description': 'Electronic dance music with a hypnotic rhythm', 'ParentGenre': 4},
            {'Name': 'Dubstep', 'Description': 'Electronic dance music with heavy bass', 'ParentGenre': 4},
            {'Name': 'Folk', 'Description': 'Traditional and cultural music', 'ParentGenre': None},
            {'Name': 'Indie', 'Description': 'Independent and non-mainstream music', 'ParentGenre': None},
            {'Name': 'Grunge', 'Description': 'Alternative rock with a dirty sound', 'ParentGenre': 1},
            {'Name': 'Ska', 'Description': 'Jamaican music with a fast beat', 'ParentGenre': 10},
            {'Name': 'Reggaeton', 'Description': 'Latin music with a reggaeton beat', 'ParentGenre': 10},
            {'Name': 'K-Pop', 'Description': 'Korean pop music', 'ParentGenre': 3},
            {'Name': 'Latin Pop', 'Description': 'Latin music with pop elements', 'ParentGenre': 3},
            {'Name': 'Synthwave', 'Description': 'Electronic music with a retro sound', 'ParentGenre': 4},
            {'Name': 'Ambient', 'Description': 'Atmospheric and relaxing music', 'ParentGenre': 4},
            {'Name': 'Gospel', 'Description': 'Christian religious music', 'ParentGenre': None},
            {'Name': 'Opera', 'Description': 'Dramatic and theatrical classical music', 'ParentGenre': 8},
            {'Name': 'Bluegrass', 'Description': 'American roots music with a fast tempo', 'ParentGenre': 7},
            {'Name': 'New Age', 'Description': 'Relaxing and meditative music', 'ParentGenre': None},
            {'Name': 'World', 'Description': 'Music from various cultures around the world', 'ParentGenre': None}
        ]

        query = """
        INSERT INTO Genres (Name, Description, ParentGenre) 
        VALUES (%(Name)s, %(Description)s, %(ParentGenre)s)
        """
        
        self.cursor.executemany(query, genres)
        self.connection.commit()
        print(f"Inserted {len(genres)} genres")

    def populate_artist_genres(self):
        # Get all artist IDs and genre IDs
        self.cursor.execute("SELECT ArtistID FROM Artists")
        artists = self.cursor.fetchall()
        
        self.cursor.execute("SELECT GenreID FROM Genres")
        genres = self.cursor.fetchall()

        # Create artist-genre relationships
        artist_genres = []
        for artist in artists:
            # Each artist gets 1-3 genres
            num_genres = random.randint(1, 3)
            artist_genre_entries = random.sample(genres, num_genres)
            
            for genre in artist_genre_entries:
                artist_genres.append({
                    'ArtistID': artist['ArtistID'],
                    'GenreID': genre['GenreID']
                })

        query = """
        INSERT INTO ArtistGenres (ArtistID, GenreID) 
        VALUES (%(ArtistID)s, %(GenreID)s)
        """
        
        self.cursor.executemany(query, artist_genres)
        self.connection.commit()
        print(f"Inserted {len(artist_genres)} artist-genre relationships")

    def populate_albums(self, num_albums=5000):
        # Get artist IDs to link albums
        self.cursor.execute("SELECT ArtistID FROM Artists")
        artists = self.cursor.fetchall()

        albums = []
        for _ in range(num_albums):
            artist = random.choice(artists)
            album = {
                'Title': self.fake.catch_phrase(),
                'MainArtistID': artist['ArtistID'],
                'ReleaseDate': self.fake.date_between(start_date='-30y', end_date='today'),
                'Label': self.fake.company(),
                'TotalTracks': random.randint(8, 15),
                'AlbumType': random.choice([
                    'Studio', 'Live', 'Compilation', 'EP', 'Single', 
                    'Mixtape', 'Remix', 'Soundtrack', 'Tribute', 
                    'Box Set', 'Demo', 'Holiday', 'Concept', 'Split'
                ]),
                'CoverArtURL': f"https://example.com/covers/{self.fake.uuid4()}.com"
            }
            albums.append(album)

        query = """
        INSERT INTO Albums 
        (Title, MainArtistID, ReleaseDate, Label, TotalTracks, AlbumType, CoverArtURL) 
        VALUES 
        (%(Title)s, %(MainArtistID)s, %(ReleaseDate)s, %(Label)s, 
         %(TotalTracks)s, %(AlbumType)s, %(CoverArtURL)s)
        """
        
        self.cursor.executemany(query, albums)
        self.connection.commit()
        print(f"Inserted {len(albums)} albums")

    def populate_tracks(self):
        # Get album IDs to link tracks
        self.cursor.execute("SELECT AlbumID, TotalTracks FROM Albums")
        albums = self.cursor.fetchall()

        tracks = []
        for album in albums:
            for _ in range(album['TotalTracks']):
                track = {
                    'Title': self.fake.catch_phrase(),
                    'Duration': f"{random.randint(2,5)}:{random.randint(0,59):02d}",
                    'BPM': random.randint(60, 180),
                    'MoodTags': random.choice(['Happy', 'Sad', 'Anger', 'Energetic', 'Calm', 'Romantic', 'Melancholic', 'Uplifting', 'Aggressive', 'Relaxing', 'Mysterious']),
                    'Explicit': random.choice([True, False]),
                    'LyricsURL': f"https://example.com/lyrics/{self.fake.uuid4()}.txt",
                    'AlbumID': album['AlbumID']
                }
                tracks.append(track)

        query = """
        INSERT INTO Tracks 
        (Title, Duration, BPM, MoodTags, Explicit, LyricsURL, AlbumID) 
        VALUES 
        (%(Title)s, %(Duration)s, %(BPM)s, %(MoodTags)s, 
         %(Explicit)s, %(LyricsURL)s, %(AlbumID)s)
        """
        
        self.cursor.executemany(query, tracks)
        self.connection.commit()
        print(f"Inserted {len(tracks)} tracks")

    def populate_collaborations(self):
        # Get artist and track IDs
        self.cursor.execute("SELECT ArtistID FROM Artists")
        artists = self.cursor.fetchall()
        
        self.cursor.execute("SELECT TrackID FROM Tracks")
        tracks = self.cursor.fetchall()

        collaborations = []
        for track in tracks:
            # Random number of collaborators per track
            num_collabs = random.randint(0, 3)
            collab_artists = random.sample(artists, num_collabs)
            
            for artist in collab_artists:
                collaboration = {
                    'TrackID': track['TrackID'],
                    'ArtistID': artist['ArtistID'],
                    'Role': random.choice([
                        'Featured Artist', 'Producer', 
                        'Background Vocals', 'Songwriter'
                    ])
                }
                collaborations.append(collaboration)

        query = """
        INSERT INTO Collaborations 
        (TrackID, ArtistID, Role) 
        VALUES 
        (%(TrackID)s, %(ArtistID)s, %(Role)s)
        """
        
        self.cursor.executemany(query, collaborations)
        self.connection.commit()
        print(f"Inserted {len(collaborations)} collaborations")
    
    def populate_playlists(self, num_playlists=1000):
        """
        Populate Playlists table with random data
        """
        # Get all track IDs
        self.cursor.execute("SELECT TrackID FROM Tracks")
        all_tracks = self.cursor.fetchall()

        # Predefined playlist name templates
        playlist_name_templates = [
            "{mood} {genre} Vibes",
            "Top {genre} Hits",
            "{mood} Mix",
            "Best of {genre}",
            "{occasion} Playlist"
        ]

        # Possible moods and occasions
        moods = ['Chill', 'Energetic', 'Romantic', 'Workout', 'Relaxing']
        genres = ['Rock', 'Pop', 'Hip Hop', 'Electronic', 'Jazz']
        occasions = ['Road Trip', 'Party', 'Study', 'Workout', 'Dinner']

        playlists = []
        for _ in range(num_playlists):
            # Randomly choose a track for the playlist
            # random_track = random.choice(all_tracks)
            num_tracks = random.randint(10, 30)
            playlist_tracks = random.sample(all_tracks, num_tracks)
            
            # Convert track IDs to comma-separated string
            tracks_string = ','.join(str(track['TrackID']) for track in playlist_tracks)
            
            # Choose a primary track (first track in the list)
            primary_track = playlist_tracks[0]['TrackID']

            # Randomly choose a template and fill it
            template = random.choice(playlist_name_templates)
            name_params = {
                'mood': random.choice(moods),
                'genre': random.choice(genres),
                'occasion': random.choice(occasions)
            }
            
            playlist = {
                'Name': template.format(**name_params),
                'TrackID': primary_track,
                'Creator': self.fake.name(),
                'CreationDate': self.fake.date_between(start_date='-5y', end_date='today'),
                'Description': self.fake.sentence(),
                'IsPublic': random.choice([True, False]),
                # Placeholder for PlaylistTracks - using comma-separated TrackIDs
                'PlaylistTracks': tracks_string
            }
            playlists.append(playlist)

        query = """
        INSERT INTO Playlists 
        (Name, TrackID, Creator, CreationDate, Description, IsPublic, PlaylistTracks) 
        VALUES 
        (%(Name)s, %(TrackID)s, %(Creator)s, %(CreationDate)s, %(Description)s, %(IsPublic)s, %(PlaylistTracks)s)
        """
        
        self.cursor.executemany(query, playlists)
        self.connection.commit()
        print(f"Inserted {len(playlists)} playlists")

        

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

def main():
    populator = MusicDatabasePopulator()
    
    # Populate tables in order
    # populator.populate_artists()
    # populator.populate_genres()
    # populator.populate_artist_genres()
    # populator.populate_albums()
    # populator.populate_tracks()
    # populator.populate_collaborations()
    # populator.populate_playlists()
    
    
    populator.close_connection()

if __name__ == "__main__":
    main()