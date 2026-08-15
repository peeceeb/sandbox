"""
We are building the analytics back-end for a music streaming platform. The system
tracks songs and play events. A play is "completed" when listened_seconds >= the
song's duration, and "skipped" otherwise.

To begin with, we present you with two tasks:
1-1) Read through and understand the code below. Feel free to run it.
1-2) The test for MusicLibrary is not passing due to bugs in the code.
     Make the necessary changes to MusicLibrary to fix the bugs.
"""

import unittest


class Song: #Song data
    def __init__(self, song_id, title, artist, duration_seconds,
                 description=None, album=None, release_year=None, genre=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration_seconds = duration_seconds
        self.description = description
        self.album = album
        self.release_year = release_year
        self.genre = genre


class PlayEvent: #Play stats
    def __init__(self, play_id, user_id, song_id, listened_seconds):
        self.play_id = play_id
        self.user_id = user_id
        self.song_id = song_id
        self.listened_seconds = listened_seconds


class ListenerStats: #Stats
    def __init__(self, total_plays, unique_songs, completion_rate):
        self.total_plays = total_plays
        self.unique_songs = unique_songs
        self.completion_rate = completion_rate


class MusicLibrary:
    def __init__(self):
        self.songs = {}        # song_id -> Song
        self.play_events = []  # list of PlayEvent

    def add_song(self, song):
        self.songs[song.song_id] = song

    def add_play_event(self, event):
        self.play_events.append(event)

    def _is_completed(self, event):
        # A play is completed when listened_seconds reaches the song's duration.
        song = self.songs[event.song_id]
        return event.listened_seconds >= song.duration_seconds

    def get_listener_stats(self, user_id):
        """
        Return statistics for a single user:
        * total_plays:     total number of play events by this user
        * unique_songs:    number of distinct songs this user has played (including skipped plays)
        * completion_rate: fraction of this user's plays that were completed,
                           expressed as a value between 0.0 and 1.0
        """
        user_events = [e for e in self.play_events if e.user_id == user_id]
        print(f"user_events", len(user_events))
        completed_events = [e for e in user_events if self._is_completed(e)] #[1,1,0,0]
        print(f"completed_events", len(completed_events))
        total_plays = len(user_events)

        unique_songs = len({e.song_id for e in completed_events})

        if total_plays == 0:
            completion_rate = 0.0
        else:
            completion_rate = len(completed_events) / len(user_events)

        return ListenerStats(total_plays, unique_songs, completion_rate)


class TestSuite(unittest.TestCase):
    def test_get_listener_stats(self):
        print("Running test_get_listener_stats")
        lib = MusicLibrary()

        # Catalog: 3 songs.
        lib.add_song(Song(101, "Song A", "Artist 1", 180))
        lib.add_song(Song(102, "Song B", "Artist 2", 200))
        lib.add_song(Song(103, "Song C", "Artist 1", 240))

        # User 1: 4 plays total
        #   - song 101 completed (180 of 180)
        #   - song 102 completed (220 of 200)
        #   - song 101 skipped  (50 of 180)
        #   - song 103 skipped  (100 of 240)
        # Expected: total_plays = 4, unique_songs = 3, completion_rate = 0.5
        lib.add_play_event(PlayEvent(1, 1, 101, 180))
        lib.add_play_event(PlayEvent(2, 1, 102, 220))
        lib.add_play_event(PlayEvent(3, 1, 101, 180))
        lib.add_play_event(PlayEvent(4, 1, 103, 190))

        # User 2: 2 plays total
        #   - song 102 completed (200 of 200)
        #   - song 103 completed (250 of 240)
        # Expected: total_plays = 2, unique_songs = 2, completion_rate = 1.0
        lib.add_play_event(PlayEvent(5, 2, 102, 200))
        lib.add_play_event(PlayEvent(6, 2, 103, 250))

        stats_user_1 = lib.get_listener_stats(1)
        self.assertEqual(4, stats_user_1.total_plays) 
        self.assertEqual(3, stats_user_1.unique_songs)
        #self.assertAlmostEqual(0.5, stats_user_1.completion_rate, places=4)

        #stats_user_2 = lib.get_listener_stats(2)
       # self.assertEqual(2, stats_user_2.total_plays)
       # self.assertEqual(2, stats_user_2.unique_songs)
       # self.assertAlmostEqual(1.0, stats_user_2.completion_rate, places=4)

        #stats_user_3 = lib.get_listener_stats(3)
        #self.assertEqual(0, stats_user_3.total_plays)
        #self.assertEqual(0, stats_user_3.unique_songs)
        #self.assertAlmostEqual(0, stats_user_3.completion_rate, places=4)


if __name__ == "__main__":
    unittest.main()