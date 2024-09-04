#!/usr/bin/env python3

import json
import os
import sys


fixes = {'/Volumes/media/karaoke/Karaoke Collection Part 6 MP3+CDG RAR Archive': []}

split_fixes = {
    '5th Dimension - Aquarius - Let The Sunshine In': {
        'artist': '5th Dimension',
        'title': 'Aquarius - Let The Sunshine In'
    },
    'Anne - Lie Ryde - En San Karl': {
        'artist': 'Anne-Lie Rydé',
        'title': 'En Sån Karl'
    },
    'Blues Brothers - 634 - 5789': {
        'artist': 'Blues Brothers',
        'title': '634-5789'
    },
    "Martine St - Clair - Ce Soir L'amour Est Dans Tes Yeux": {
        'artist': 'Martine St-Clair',
        'title': "Ce Soir L'amour Est Dans Tes Yeux"
    },
    'Michele Torr - Emmene - Moi Danser Ce Soir': {
        'artist': 'Michèle Torr',
        'title': 'Emmène moi danser ce soir'
    },
    "Mike Brent - Laisse - Moi T'aimer": {
        'artist': 'Mike Brent',
        'title': "Laisse-Moi T'aimer"
    },
    'Mylene Farmer - Déshabillez - Moi': {
        'artist': 'Mylene Farmer',
        'title': 'Déshabillez-Moi'
    },
    "Haim - Don't Save Me - (BBC Sound Of 2013 Winners)": {
        'artist': 'Haim',
        'title': "Don't Save Me - (BBC Sound Of 2013 Winners)"
    },
    'X - Models  -  Två Av Oss': {
        'artist': 'X Models',
        'title': 'Två Av Oss'
    },
    "Boney M - Mary's Boy Child - Oh My Lord": {
        'artist': 'Boney M',
        'title': "Mary's Boy Child - Oh My Lord"
    },
    'Robin Thicke Ft. - Kendrick Lamar - Give It 2 U': {
        'artist': 'Robin Thicke Ft. Kendrick Lamar',
        'title': 'Give It 2 U'
    },
    '': {
        'artist': '',
        'title': ''
    },
    '': {
        'artist': '',
        'title': ''
    },
    '': {
        'artist': '',
        'title': ''
    },
    '': {
        'artist': '',
        'title': ''
    },
    '': {
        'artist': '',
        'title': ''
    },
    '': {
        'artist': '',
        'title': ''
    },

}


class KaraokeSong:
    def __init__(self, path, root):
        self.good = False
        self.path = path
        self.root = root
        directory, name = os.path.split(path)
        if self.is_first_karaoke_collection():
            print('x')
            if name.endswith(' [Karaoke]') or name.endswith(' [karaoke]'):
                name = name[:-len(' [Karaoke]')]
                try:
                    artist, title = name.split(' - ')
                except ValueError:
                    if name in split_fixes:
                        artist = split_fixes[name]['artist']
                        title = split_fixes[name]['title']
                    else:
                        print(f'Cannot split:    "{name}"')

                self.artist = artist
                self.title = title
                self.good = True
            else:
                print(f'Unusual - name: {name}, dir={directory}')
            pass
        else:
            print('I do not know how to parse this right now')

    def is_first_karaoke_collection(self):
        # return self.root.startswith('/Volumes/media/karaoke/')
        return self.root == '/Volumes/media/karaoke'

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'KaraokeSong(path={self.path}, root={self.root})'


def title_sort_key(key):
    prefixes = ('A', 'The')
    for prefix in prefixes:
        spaced_prefix = prefix + ' '
        if key.startswith(spaced_prefix):
            rest = key[len(spaced_prefix):]
            return f'{rest}, {prefix}'
    return key


def build_struct(songs):
    return [{'artist': x.artist, 'title': x.title} for x in songs]


def process(path):
    # store base_name -> (CDGPresenceFlag, MP3PresenceFlag)
    songs = {}
    unknowns = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.cdg'):
                base_filename = file[:-len('.cdg')]
                full_path = os.path.join(root, base_filename)
                if full_path not in songs:
                    songs[full_path] = [False, False]
                songs[full_path][0] = True
            elif file.endswith('.mp3'):
                base_filename = file[:-len('.mp3')]
                full_path = os.path.join(root, base_filename)
                if full_path not in songs:
                    songs[full_path] = [False, False]
                songs[full_path][1] = True
            else:
                full_path = os.path.join(root, file)
                unknowns.append(full_path)

    complete_songs = [KaraokeSong(k, path) for k, v in songs.items() if v == [True, True]]
    print(f'Found {len(complete_songs)} complete songs and {len(unknowns)} unknown files.')
    good_songs = [x for x in complete_songs if x.good]
    print(f'Good songs: {len(good_songs)}')
    # create a Markdown file with artists alphabetical
    songs_by_artist = {}
    for song in good_songs:
        if song.artist not in songs_by_artist:
            songs_by_artist[song.artist] = []
        songs_by_artist[song.artist].append(song)
    json_struct = build_struct(good_songs)
    with open('/Users/sean/songs.json', 'w') as f:
        f.write(json.dumps(json_struct))
    with open('/Users/sean/songs-by-artist.md', 'w') as f:
        for artist in sorted(songs_by_artist.keys(), key=title_sort_key):
            f.write(f'# {artist}\n')
            song_titles = [x.title for x in songs_by_artist[artist]]
            ordered_song_titles = sorted(song_titles, key=title_sort_key)
            for title in ordered_song_titles:
                f.write(f'- {title}\n')
            f.write('\n\n')
            # self.path
            # self.title
            # self.artist
            pass
        print('First song:', complete_songs[0])


def main(args):
    # path1 = '/Volumes/media/karaoke/Karaoke Collection Part 6 MP3+CDG RAR Archive'
    path1 = '/Volumes/media/karaoke'
    # path1 = '/volume1/media/karaoke/Karaoke Collection Part 6 MP3+CDG RAR Archive'
    base_dirs = [path1]
    for path in base_dirs:
        process(path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
