import pickle
from Classes import User, Movie
from Classes import Movie

#if a user's rating of a movie is >= THRESHOLD, then they liked that movies
#if relavance of tag >= THRESHOLD*2/10, then then the tag is relevant 
THRESHOLD = 3.5 

def load_data(file): 
    db_file = open(file, 'rb')      
    db = pickle.load(db_file) 
    db_file.close()
    return db

def predict_rating(userid, movieid, users, movies, tags):
    u = users[userid]
    if movieid in u.liked_movies:
        return [u.liked_movies[movieid], movies[movieid].title]
    if movieid in u.disliked_movies:
        return [u.disliked_movies[movieid], movies[movieid].title]
    rated_movie = movies[movieid]
    mov_count = 0
    tag_count = 0
    total_tags = 0
    for mov in u.liked_movies:
        seen_movie = movies[mov]
        for r in rated_movie.genres:
            if r in seen_movie.genres:
                mov_count = mov_count + u.liked_movies[mov]
        for t in rated_movie.liked_tags:
            if t in seen_movie.liked_tags or t in u.liked_tags:
                tag_count = tag_count + float(rated_movie.liked_tags[t])
            total_tags = total_tags + 1
    for mov in u.disliked_movies:
        seen_movie = movies[mov]
        for t in rated_movie.disliked_tags:
            if t in seen_movie.disliked_tags or t in u.disliked_tags:
                tag_count = tag_count - float(rated_movie.disliked_tags[t])
            total_tags = total_tags + 1
    mv = mov_count / (len(u.liked_movies) + len(u.disliked_movies))
    tg = tag_count / (total_tags if total_tags > 0 else 1)
    rating = round(mv + tg, 2)
    return rating

def get_personal_list(userid, users, movies, tags):
    arr = []
    u = users[userid]
    for m in movies:
        if m not in u.liked_movies and m not in u.disliked_movies:
            rating = predict_rating(userid, m, users, movies, tags)
            if rating >= 5:
                link = "https://www.imdb.com/title/tt" + movies[m].link
                arr.append([movies[m].title, m, link, rating])
    return sorted(arr, key = lambda x: x[3], reverse = True)

def make_table(letter, movies):
    table = []
    for m in movies:
        title = movies[m].title
        if title[0] == letter or (letter == "#" and title[0].isdigit()):
            table.append([title, m])
    return sorted(table, key=lambda x: x[0])

def main():
    u = load_data("data/list_users")
    m = load_data("data/list_movies")
    t = load_data("data/list_tags")
    userid = "1245"
    movieid = "3"
    print(predict_rating(userid, movieid, u, m, t))
    print(get_personal_list(userid, u, m, t))
    print(make_table("#", m))

if __name__ == "__main__":
    main()