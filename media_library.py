from get_cache_itunes_data import *
import json
import requests


# Class Definitions

class Media(object):
    def __init__(self, media_dictionary):
        self.dictionary = media_dictionary
        self.title = media_dictionary.get("trackName", "None")
        self.author = media_dictionary.get("artistName", "None")
        self.authorid = media_dictionary.get("artistId")
        self.itunes_URL = media_dictionary.get("trackViewUrl", "None")
        self.itunes_id = media_dictionary.get("trackId", "None")

    def __str__(self):
        return "{} by {}".format(self.title, self.author)

    def __repr__(self):
        return "ITUNES MEDIA: {}".format(self.itunes_id)

    def table_rep(self):
        self.rep_diction = {}
        self.rep_diction["title"] = self.title
        self.rep_diction["itunes_URL"] = self.itunes_URL
        self.rep_diction["itunes_id"] = self.itunes_id
        return self.rep_diction

    def author_rep(self, again=False):
        # Make request for artist info
        # Caching this will speed it up! :)
        if not again:
            baseurl = "https://itunes.apple.com/lookup"
            params = {"id":self.authorid}
            resp_data = json.loads(requests.get(baseurl, params=params).text)
            # print(resp_data)
            infodiction = {}
            infodiction["name"] = self.author
            infodiction["primary_genre"] = "None"
            if resp_data["resultCount"] > 0:
                infodiction["primary_genre"] = resp_data["results"][0]["primaryGenreName"]
        else:
            infodiction["name"] = "None available"
            infodiction["primary_genre"] = "None"
        return infodiction

    def __len__(self):
        return 0

    def __contains__(self, entry):
        if entry in self.title:
            return True

# Class Song
class Song(Media):
    def __init__(self, item):
        super().__init__(item)
        self.album = item.get("collectionName", "None")
        self.track_number = item.get("trackNumber", "None")
        self.genre = item.get("primaryGenreName", "None")
        self.militime = item.get("trackTimeMillis", 0)


    def __len__(self):
        self.militime = int(self.militime)
        seconds = (self.militime/1000)%60
        seconds = int(seconds)
        minutes = (self.militime/(1000*60))%60
        minutes = int(minutes)
        hours = (self.militime/(1000*60*60))%24
        hours = int(hours)

        minute = int(self.militime/(1000))
        return minute

    def table_rep(self):
        super().table_rep()
        self.rep_diction["album"] = self.album
        self.rep_diction["trackNum"] = self.track_number
        self.rep_diction["genre"] = self.genre
        self.rep_diction["minutes"] = self.__len__()
        return self.rep_diction

# Class Movie
class Movie(Media):
    def __init__(self, item):
        super().__init__(item) #allows me to access attributes of the parent
        self.rating = item.get("contentAdvisoryRating", "None")
        self.genre = item.get("primaryGenreName", "None")
        self.description = item.get("longDescription", "None")
        self.militime = item.get("trackTimeMillis", 0)

    def table_rep(self):
        super().table_rep()
        self.rep_diction["rating"] = self.rating
        self.rep_diction["genre"] = self.genre
        self.rep_diction["description"] = self.description
        self.rep_diction["minutes"] = self.__len__()
        self.rep_diction["wordsInTitle"] = self.title_words_num()
        return self.rep_diction

    def __len__(self):
        self.militime = int(self.militime)
        seconds = (self.militime/1000)%60
        seconds = int(seconds)
        minutes = (self.militime/(1000*60))%60
        minutes = int(minutes)
        hours = (self.militime/(1000*60*60))%24
        hours = int(hours)

        minute = int(self.militime/(1000*60))
        return minute

    def title_words_num(self):
        if self.description == "None":
            return 0
        else:
            splitDescription = self.description.split()
            lengthDescription = len(splitDescription)
            return lengthDescription
