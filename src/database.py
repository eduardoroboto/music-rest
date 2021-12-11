
# User = {'id': 0, 'username': "", 'email': "", 'password': "", 'playlist': []}
# Music = {'id': 0, 'artist': "", 'album': "", 'name': "", 'tags': []}
# PlayList = {'id': 0, 'name': "", 'user_id': 0, 'musics_list': []}

# db = {'users': {}, 'musics': {}, 'playlists': {}}

class Database:
    def __init__(self):
        self.users = {}
        self.musics = {}
        self.playlists = {}

    def init_db(self):
        ed = {'username': 'Ed', 'email': 'ed@ed.com', "password": "123"}
        bb = {'username': 'bb', 'email': 'bb@bb.com', 'password': "321"}
        get_lucky = {'artist': "Daft Punk", 'album': "RAM", 'name': "Get Lucky"}
        favorites = {'name': "My Favorites", 'user_id': 0, 'musics_list': [0]}
        daft = {'name': "The Best Of Daft Punk", 'user_id': 0, 'musics_list': [0]}

        self.add_new_user(ed, bb)
        self.add_new_music(get_lucky)
        self.add_new_playlists(favorites, daft)

    def add_new_user(self, *argv):
        for user in argv:
            if len(self.users) == 0:
                self.users[0] = user
                user['id'] = 0
                user['playlists'] = []
            else:
                index = max(self.users.keys()) + 1
                self.users[index] = user
                user['id'] = index
                user['playlists'] = []

    def add_new_music(self, *argsv):
        for music in argsv:
            if len(self.musics) == 0:
                self.musics[0] = music
                music['id'] = 0
            else:
                index = max(self.musics.keys()) + 1
                self.musics[index] = music
                music['id'] = index

    def add_new_playlists(self, *argv):
        for playlist in argv:
            if len(self.playlists) == 0:
                self.playlists[0] = playlist
                playlist['id'] = 0
                self.users[playlist['user_id']]['playlists'].append(0)
            else:
                index = max(self.playlists.keys()) + 1
                self.playlists[index] = playlist
                playlist['id'] = index
                self.users[playlist['user_id']]['playlists'].append(index)

    def update_user(self, user, user_id):
        for key in user.keys():
            self.users[user_id][key] = user[key]

    def update_music(self, music, music_id):
        for key in music.keys():
            self.musics[music_id][key] = music[key]

    def update_playlist(self, playlist, playlist_id):
        for key in playlist.keys():
            self.playlists[playlist_id][key] = playlist[key]

    def remove_user(self, user_id):
        if len(self.users[user_id]['playlists']) > 0:
            for playlist_id in self.users[user_id]['playlists']:
                self.playlists.pop(playlist_id)
        self.users.pop(user_id)

    def remove_music(self, music_id):
        for playlist in self.playlists.values():
            if music_id in playlist['musics_list']:
                playlist['musics_list'] = [music for music in playlist['musics_list'] if music != music_id]
        self.musics.pop(music_id)

    def remove_playlist(self, playlist_id):
        user_id = self.playlists[playlist_id]['user_id']
        self.users[user_id]['playlists'].remove(playlist_id)
        self.playlists.pop(playlist_id)


db = Database()
db.init_db()
