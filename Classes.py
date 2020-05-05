class User:
    def __init__(self, liked_movies, disliked_movies, liked_tags, disliked_tags):
        self.liked_movies = liked_movies
        self.disliked_movies = disliked_movies
        self.liked_tags = liked_tags
        self.disliked_tags = disliked_tags
    def __str__(self):
        return str(self.liked_movies) + ", " + str(self.disliked_movies) + ", " + str(self.liked_tags) + ", " + str(self.disliked_tags)

class Movie:
    def __init__(self, title, genres, liked_tags, disliked_tags, link):
        self.title = title
        self.genres = genres
        self.liked_tags = liked_tags
        self.disliked_tags = disliked_tags
        self.link = link
    def __str__(self):
        return self.title + ", " + str(self.genres) + ", " + str(self.liked_tags) + ", " + str(self.disliked_tags) + ", " + self.link