import csv
import pickle
from Classes import User, Movie
from main import THRESHOLD


def populate_users(ratings_file, tags_file, thresh):
    users = {}
    movies = open(ratings_file, encoding = "utf8")
    tags = open(tags_file, encoding = "utf8")
    movies_r = csv.reader(movies)
    tags_r = csv.reader(tags)
    next(tags_r)
    current_movies = next(movies_r)
    current_tags = next(tags_r)
    stay = True
    stay2 = True
    i = int(current_movies[0])
    while stay:
        arr_movies_l = {}
        arr_movies_d = {}
        arr_liked_tags = []
        arr_disliked_tags = []
        while int(current_movies[0]) == i and stay:
            if float(current_movies[2]) >= thresh:
                arr_movies_l[current_movies[1]] = float(current_movies[2])
            else:
                arr_movies_d[current_movies[1]] = float(current_movies[2])
            try:
                current_movies = next(movies_r)
            except:
                stay = False
        while int(current_tags[0]) == i and stay2:
            if current_tags[1] in arr_movies_l:
                arr_liked_tags.append(current_tags[2])
            else:
                arr_disliked_tags.append(current_tags[2])
            try:
                current_tags = next(tags_r)
            except:
                stay2 = False
        users[str(i)] = User(arr_movies_l, arr_movies_d, arr_liked_tags, arr_disliked_tags)
        i = int(current_movies[0])
    tags.close()
    movies.close()
    return users

def populate_movies(movies_file, scores_file, links_file, thresh):
    movies = {}
    movies_f = open(movies_file, encoding = "utf8")
    scores = open(scores_file, encoding = "utf8")
    links = open(links_file, encoding = "utf8")
    movies_r = csv.reader(movies_f)
    scores_r = csv.reader(scores)
    links_r = csv.reader(links)
    next(movies_r)
    next(scores_r)
    next(links_r)
    current_movies = next(movies_r)
    current_scores = next(scores_r)
    current_links = next(links_r)
    stay = True
    stay2 = True
    i = int(current_movies[0])
    while stay:
        arr_liked_tags = {}
        arr_disliked_tags = {}
        while int(current_scores[0]) == i and stay2:
            if float(current_scores[2]) >= (thresh * 2 / 10):
                arr_liked_tags[current_scores[1]] = current_scores[2]
            else:
                arr_disliked_tags[current_scores[1]] = current_scores[2]
            try:
                current_scores = next(scores_r)
            except:
                stay2 = False
        genres = [temp for temp in current_movies[2].split("|")]
        movies[current_movies[0]] = Movie(current_movies[1], genres, arr_liked_tags, arr_disliked_tags, current_links[1])
        try:
            current_movies = next(movies_r)
            current_links = next(links_r)
        except:
            stay = False
        i = int(current_movies[0])
    links.close()
    scores.close()
    movies_f.close()
    return movies
def populate_tags(tags_file):
    tags = {}
    tags_f = open(tags_file, encoding="utf8")
    tags_r = csv.reader(tags_f)
    next(tags_r)
    current_tags = next(tags_r)
    stay = True
    while stay:
        tags[current_tags[1]] = current_tags[0]
        try:
            current_tags = next(tags_r)
        except:
            stay = False
    return tags

def store_data(file, cucumber):  
    gl_users = open(file, "wb")
    pickle.dump(cucumber, gl_users)
    gl_users.close()

def populate_pickles():
    users = populate_users("ml-latest/ratings.csv", "ml-latest/tags.csv", THRESHOLD)
    store_data("data/list_users", users)
    movies = populate_movies("ml-latest/movies.csv", "ml-latest/genome-scores.csv", "ml-latest/links.csv", THRESHOLD)
    store_data("data/list_movies", movies)
    tags = populate_tags("ml-latest/genome-tags.csv")
    store_data("data/list_tags", tags)

if __name__ == "__main__":  
    populate_pickles()
    

