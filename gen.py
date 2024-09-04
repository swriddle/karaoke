#!/usr/bin/env python3

import json
import os
import re
import sys

# group: ('Sum 41', 'SC Karaoke] - Still Waiting')
# Cannot split:    "Sum 41"

# group: ('Jeff Carson', 'SC Karaoke] - I Can Only Imagine')

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
    'Aloe Blacc - I Nee - Dollar': {
        'artist': 'Aloe Blacc',
        'title': 'I Need A Dollar'
    },
    'Anne - Marie - Then': {
        'artist': 'Anne-Marie',
        'title': 'Then'
    },
    'Baby Face - Medley -  Hail, Hail  Alabama Jubileee': {
        'artist': 'Baby Face',
        'title': 'Medley -  Hail, Hail  Alabama Jubilee'
    },
    'Baila Esta Cumbia - Selena - Selena': {
        'artist': 'Selena',
        'title': 'Baila Esta Cumbia'
    },
    'Beyonce - C - Tdown': {
        'artist': 'Beyonce',
        'title': 'Countdown'
    },
    'ABBA - (Medley) Waterloo+Dancing Queen+Take A Chance On Me+Super Troup': {
        'artist': 'ABBA',
        'title': '(Medley) Waterloo+Dancing Queen+Take A Chance On Me+Super Troup'
    },
    "Bhk066-12 - Nico & Vinz & Kid Ink & Bebe Rex - That's How You Know": {
        'artist': "Nico & Vinz & Kid Ink & Bebe Rex",
        'title': "That's How You Know"
    },
    'Black Lab - Sleeps - H Angels': {
        'artist': 'Black Lab',
        'title': 'Sleeps With Angels'
    },
    'Blue - I Can (eurovision 2011 - United Kingdom)': {
        'artist': 'Blue',
        'title': 'I Can (Eurovision 2011 - United Kingdom)'
    },
    'Carmen, Marie - Donne - Toi': {
        'artist': 'Marie Carmen',
        'title': 'Donne-Toi'
    },
    'Cast Of Rent - Rent - Seasons Of Love': {
        'artist': 'Rent',
        'title': 'Seasons Of Love'
    },
    'Cher Lloyd Ft Mike Posner - W - Ur Love': {
        'artist': 'Cher Lloyd Ft Mike Posner',
        'title': 'With Ur Love'
    },
    'Coldplay - P - Dise': {
        'artist': 'Coldplay',
        'title': 'Paradise'
    },
    'David Nail - Kiss You Tonight - W V Backing': {
        'artist': 'David Nail',
        'title': 'Kiss You Tonight (w/ vocal backing)'
    },
    'Dean Martin - Rudolph, The Red - Nosed Reindeer': {
        'artist': 'Dean Martin',
        'title': 'Rudolph, The Red-Nosed Reindeer'
    },
    'Die Wilden Buben - Dj Corona - Herzilein (Lass Mich Rein)': {
        'artist': 'Die Wilden Buben ft. DJ Corona',
        'title': 'Herzilein (Lass Mich Rein)'
    },
    "DN10-00 - Emma - Du er den som jeg vil ha'": {
        'artist': "Emma Thorsteinsson",
        'title': "Du er den som jeg vil ha'"
    },
    'DN12-00 - Thomas Helmig - Det Er Mig Der Står Herude Og Banker På': {
        'artist': 'Thomas Helmig',
        'title': 'Det Er Mig Der Står Herude Og Banker På'
    },
    'DN14-00 - Sanne Salomonsen & Anne Linnet - Den jeg elsker, elsker jeg': {
        'artist': 'Sanne Salomonsen & Anne Linnet',
        'title': 'Den jeg elsker, elsker jeg'
    },
    "DN20-00 - Gustav Winkler - Gem Et Lille Smil Til Det Blir' Gråvejr": {
        'artist': "Gustav Winkler",
        'title': "Gem Et Lille Smil Til Det Blir' Gråvejr"
    },
    'Dschungel Stars - Ich Bin Ein Star - Holt Mich Hier Raus': {
        'artist': 'Dschungel Stars',
        'title': 'Ich Bin Ein Star - Holt Mich Hier Raus'
    },
    'Eric Lapointe - Deux Fois La Meme Histoire Midi - Inconnu': {
        'artist': 'Eric Lapointe',
        'title': 'Deux Fois La Meme Histoire'
    },
    'Eric Lapointe - La Bartendresse Version 2 - Rene': {
        'artist': 'Eric Lapointe',
        'title': 'La Bartendresse'
    },
    "Eric Lapointe - Qu'est - Ce Que Ca Peut Ben Faire - Planete": {
        'artist': "Eric Lapointe",
        'title': "Qu'est - Ce Que Ca Peut Ben Faire - Planete"
    },
    'Eric Lapointe - Reste La - Jdk': {
        'artist': 'Eric Lapointe',
        'title': 'Reste Là'
    },
    'Fifth Dimension - Aquarius - Let The Sunshine In': {
        'artist': 'Fifth Dimension',
        'title': 'Aquarius - Let The Sunshine In'
    },
    'Foo Fighters - What Did You Do - God As My Witness': {
        'artist': 'Foo Fighters',
        'title': 'What Did You Do? / God As My Witness'
    },
    "France D'amour - J'entends Ta Voix - Izzy": {
        'artist': "France D'amour",
        'title': "J'entends Ta Voix"
    },
    "France D'amour - Mon Frere - Jukebox": {
        'artist': "France D'amour",
        'title': "Mon Frere"
    },
    "France Gall - Musique - Kom Fou": {
        'artist': "France Gall",
        'title': "Musique"
    },
    "France Gall - Sacre Charlemagne - Bros": {
        'artist': "France Gall",
        'title': "Sacre Charlemagne"
    },
    "Francine Raymond - Vivre Avec Celui Qu'on Aime - Kebek": {
        'artist': "Francine Raymond",
        'title': "Vivre Avec Celui Qu'on Aime"
    },
    "Francis Cabrel - Elle Ecoute Pousser Les Fleurs - Cdk": {
        'artist': "Francis Cabrel",
        'title': "Elle Ecoute Pousser Les Fleurs"
    },
    "Francis Cabrel - La Dame De Haute Savoie - Mariobros - Dvd": {
        'artist': "Francis Cabrel",
        'title': "La Dame De Haute Savoie"
    },
    "Francis Cabrel - Les Chevaliers Cathares - M00ndust": {
        'artist': "Francis Cabrel",
        'title': "Les Chevaliers Cathares"
    },
    "Frank Michael - Dites Lui Que Je L'aime - Rene": {
        'artist': "Frank Michael",
        'title': "Dites Lui Que Je L'aime"
    },
    "Frank Michael - Toutes Les Femmes Sont Belles - Rene": {
        'artist': "Frank Michael",
        'title': "Toutes Les Femmes Sont Belles"
    },
    "Frankie - Valli - Grease": {
        'artist': "Frankie Valli",
        'title': "Grease"
    },
    "G - Eazy and Halsey - Him & I": {
        'artist': "G-Eazy and Halsey",
        'title': "Him & I"
    },
    "Garou - Ne Me Parlez Plus D'elle - Cdk": {
        'artist': "Garou",
        'title': "Ne Me Parlez Plus D'elle"
    },
    "Gigi D'Alessio & A. Tatangelo - Un Nuovo Bacio - Canta Anna": {
        'artist': "Gigi D'Alessio & A. Tatangelo",
        'title': "Un Nuovo Bacio"
    },
    "Ginette Reno - Comment Te Dire - Gentil Dauphin": {
        'artist': "Ginette Reno",
        'title': "Comment Te Dire"
    },
    "Giuseppe Verdi - La Traviata - Libiamo Nei Lieti Calici": {
        'artist': "Giuseppe Verdi",
        'title': "Libiamo Nei Lieti Calici (from La Traviata)"
    },
    "Gym Class Heroes Ft Adam Levine - S - Eo Hearts": {
        'artist': "Gym Class Heroes Ft. Adam Levine",
        'title': "Stereo Hearts"
    },
    "HSKPS02-0016 - Atlantic Star - Always": {
        'artist': "Atlantic Starr",
        'title': "Always"
    },
    "HSKPS03-0107 - Bobby Darin - Mack The Knife": {
        'artist': "Bobby Darin",
        'title': "Mack the Knife"
    },
    "HSKPS03-0117 - Lou Rawls - You'll Never Find": {
        'artist': "Lou Rawls",
        'title': "You'll Never Find Another Love Like Mine"
    },
    "HSKPS03-0161 - Buddy Holly - Oh Boy": {
        'artist': "Buddy Holly",
        'title': "Oh Boy"
    },
    "HSKPS03-0167 - Madonna - Like A Virgin": {
        'artist': "Madonna",
        'title': "Like A Virgin"
    },
    "HSKPS03-0196 - Madonna - Crazy For You": {
        'artist': "Madonna",
        'title': "Crazy For You"
    },
    "HSKPS03-0206 - Dion & The Belmonts - Wanderer": {
        'artist': "Dion & The Belmonts",
        'title': "Wanderer"
    },
    "HTG1008-18 - Nelly & Kelly Rowland - Dilemma": {
        'artist': "Nelly & Kelly Rowland",
        'title': "Dilemma"
    },
    "James Morrison - I - N't Let You Go": {
        'artist': "James Morrison",
        'title': "I Won't Let You Go"
    },
    "Jethro Tull - Thick As A Brick - Fixed": {
        'artist': "Jethro Tull",
        'title': "Thick As A Brick"
    },
    "Josh Dubovie - That Sounds Good To Me (eurovision 2010 - United Kingdom)": {
        'artist': "Josh Dubovie",
        'title': "That Sounds Good To Me (Eurovision 2010 - United Kingdom)"
    },
    "Kasey Chambers - Kasey Chambers - Hollywood": {
        'artist': "Kasey Chambers",
        'title': "Hollywood"
    },
    "Kelly Clarkson - M - Now It All": {
        'artist': "Kelly Clarkson",
        'title': "Mr. Know It All"
    },
    "Labrinth Ft Tinie Tempah - E - Hquake": {
        'artist': "Labrinth ft. Tinie Tempah",
        'title': "Earthquake"
    },
    "Laidback Luke Ft Example - N - Ral Disaster": {
        'artist': "Laidback Luke ft. Example",
        'title': "Natural Disaster"
    },
    "Laisse - Moi Revenir Sur Terreginette Reno - Jukebox": {
        'artist': "Ginette Reno",
        'title': "Laisse-Moi Revenir Sur Terre"
    },
    "Lana Del Rey - V - O Games": {
        'artist': "Lana Del Rey",
        'title': "Video Games"
    },
    "Les Bels - Air - Susie Darling": {
        'artist': "Les Bel Air",
        'title': "Susie Darling"
    },
    "Lmfao - S - And I Know It": {
        'artist': "LMFAO",
        'title': "Sexy and I Know It"
    },
    "Mana - Ruben Blades - Sabanas Frias": {
        'artist': "Sábanas Frías ft. Rubén Blades",
        'title': "Maná"
    },
    "Marie - Denise Pelletier - Entre Moi Et Lui": {
        'artist': "Marie Denise Pelletier",
        'title': "Entre Moi Et Lui"
    },
    "Matt Cardle - R - For Your Life": {
        'artist': "Matt Cardle",
        'title': "Run For Your Life"
    },
    "Me & My Shadow - Moonlight & Roses - You Were Meant - My Sunshine - Medley": {
        'artist': "Max Bygraves",
        'title': "Me & My Shadow - Moonlight & Roses - You Were Meant - My Sunshine - Medley"
    },
    "Moi Ma Chance - Les Bb - Donne": {
        'artist': "Les BB",
        'title': "Donne-moi ma chance"
    },
    "Mya - Mya - Case Of The Ex (Whatcha Gonna Do)": {
        'artist': "Mya",
        'title': "Case Of The Ex (Whatcha Gonna Do)"
    },
    "Olaf Henning - Laatbleujers - Der Jungfrauenchor": {
        'artist': "Olaf Henning - Laatbleujers",
        'title': "Der Jungfrauenchor"
    },
    "Peter Wackel - Criss Tuxi - Manchmal Möchte Ich Schon Mit Dir": {
        'artist': "Peter Wackel",
        'title': "Manchmal Möchte Ich Schon Mit Dir"
    },
    "Rent - Rent - Seasons Of Love": {
        'artist': "Rent",
        'title': "Seasons Of Love"
    },
    "Rent - Rent B'ground Vox - Seasons Of Love": {
        'artist': "Rent",
        'title': "Seasons of Love (background vocals)"
    },
    "Rent - Seasons Of Love - T": {
        'artist': "Rent",
        'title': "Seasons of Love"
    },
    "Rihanna Ft Calvin Harris - W - Ound Love": {
        'artist': "Rihanna ft. Calvin Harris",
        'title': "We Found Love"
    },
    "Rizzle Kicks - W - I Was A Youngster": {
        'artist': "Rizzle Kicks",
        'title': "When I Was A Youngster"
    },
    "Rush - Fly By Night - In the Mood": {
        'artist': "Rush",
        'title': "Fly By Night / In the Mood"
    },
    "Sak Noel - L - People": {
        'artist': "Sak Noel",
        'title': "Loca People"
    },
    "Scottish Traditional - Loch Lomond - Run Rig": {
        'artist': "Scottish Traditional",
        'title': "Loch Lomond (Runrig song)"
    },
    "Shy'm - Victoire - Akella": {
        'artist': "Shy'm",
        'title': "Victoire"
    },
    "Silento - Watch Me (Whip - Nae Nae)": {
        'artist': "Silentó",
        'title': "Watch Me (Whip/Nae Nae)"
    },
    "Slim Harpo - I'm A King Bee - Backdoor Man (Medley)": {
        'artist': "Slim Harpo",
        'title': "I'm A King Bee / Backdoor Man (Medley)"
    },
    "Star Academie - Wilfred Lebouthillier - Amene - Toi Chez - Nous Mlv# 2": {
        'artist': "Wilfred Lebouthillier",
        'title': "Amene-Toi Chez-Nous"
    },
    "Star Academie 2003 - Dave - Quelle Belle Vie - C.V.": {
        'artist': "Star Academie",
        'title': "Quelle Belle Vie"
    },
    "Star Academie 2004 - La Gang - C'est Ta Chance - Gentil Dauphin": {
        'artist': "La Gang",
        'title': "C'est Ta Chance"
    },
    "Star Academie 2004 - La Gang - C'est Ta Chance-Gentil Dauphin": {
        'artist': "La Gang",
        'title': "C'est Ta Chance"
    },
    "Star Academie 2005 - L'etoile D'amerique - Mc - Rocky": {
        'artist': "Star Academie",
        'title': ""
    },
    "Star Académie - 1000 Coeurs Debout - Akella": {
        'artist': "Star Academie",
        'title': "1000 Coeurs Debout"
    },
    "Star Académie 2004 - Le Soleil Emmene Au Soleil - Véronique": {
        'artist': "Véronique",
        'title': "Le Soleil Emmene Au Soleil"
    },
    "Sugarland - Sugarland - Baby Girl": {
        'artist': "Sugarland",
        'title': "Baby Girl"
    },
    "Superchick - Stand In The Rain - W. V. Backing": {
        'artist': "Superchick",
        'title': "Stand In The Rain (w/ vocal backing)"
    },
    "Temptations - Rudolph The Red - Nosed Reindeer": {
        'artist': "Temptations",
        'title': "Rudolph The Red-Nosed Reindeer"
    },
    "Traditional - New Year's Eve Song - Auld Lang Syne": {
        'artist': "Traditional",
        'title': "Auld Lang Syne"
    },
    "Tu178-11 - La Vie En Rose (French) - Piaf, Edith": {
        'artist': "Edith Piaf",
        'title': "La Vie En Rose"
    },
    "Vasco Rossi - Medley Rock - C'è Chi Dice No-La Strega-Delusa": {
        'artist': "",
        'title': ""
    },
    "VS11-04 - Fifth Harmony - Angel": {
        'artist': "Fifth Harmony",
        'title': "Angel"
    },
    "Whitney -Houston - Greatest - Ve Of All": {
        'artist': "Whitney Houston",
        'title': "Greatest Love of All"
    },
    "Will To Power - Will To Power - Baby, I Love Your Way, Freebird Medley": {
        'artist': "",
        'title': ""
    },
    "Yusuf - Cat Stevens - Roadsinger": {
        'artist': "Cat Stevens/Yusuf Islam",
        'title': "Roadsinger"
    },
    "Zkl019-24 - Shakin' Stevens - I'll Be Home This Christmas": {
        'artist': "Shakin' Stevens",
        'title': "I'll Be Home This Christmas"
    },
    "ZKL019-24 - Shakin' Stevens - I'll Be Home This Christmas": {
        'artist': "Shakin' Stevens",
        'title': "I'll Be Home This Christmas"
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
            r1 = re.compile(r'^(.*) \[(.*)\]?$')
            # r2 = re.compiler(r'^[^[]]$')
            m1 = re.match(r1, name)
            # m2 = re.match(r2, name)
            square_brace_in_name = '[' in name

            if m1 is not None:
                print('group:', m1.groups())
                name, self.catalog = m1.groups()
            elif square_brace_in_name:
                self.catalog = None
            else:
                print(f'Unusual - name: {name}, dir={directory}')
                return

            try:
                artist, title = name.split(' - ')
            except ValueError:
                if name in split_fixes:
                    artist = split_fixes[name]['artist']
                    title = split_fixes[name]['title']
                else:
                    print(f'Cannot split:    "{name}"')
                    artist = 'foo'
                    title = 'bar'

            self.artist = artist
            self.title = title
            self.good = True

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
    path1 = '/Volumes/media/karaoke'
    path2 = '/Volumes/media/karaoke2'
    base_dirs = [path2]
    for path in base_dirs:
        process(path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
