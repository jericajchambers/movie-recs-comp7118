from flask import Flask, render_template, redirect, url_for, request
from main import load_data, predict_rating, get_personal_list, make_table, THRESHOLD

app = Flask(__name__)
users = load_data("data/list_users")
movies = load_data("data/list_movies")
tags = load_data("data/list_tags")

@app.route('/', methods = ['POST', 'GET'])
def index():
    rating = "Rating"
    if request.method == "POST":
        req = request.form
        userid = req["userid"]
        rec = req["rec"]
        if rec == "Predict Rating":
            try:
                movieid = req["movieid"]
                title = movies[movieid].title
                link = "https://www.imdb.com/title/tt" + movies[movieid].link
                rating = predict_rating(userid, movieid, users, movies, tags)
                if type(rating) is list:
                    message1 = "You've already seen "
                    if rating[0] >= THRESHOLD:
                        message2 = ", and you seemed to like it!"
                    else:
                        message2 = ", but you didn't really like it all that much!"
                    return render_template("index.html", rating = rating[0], title = title, link = link, message1 = message1, message2 = message2, threshold = THRESHOLD)
                else:
                    message2 = "!"
                    if rating >= THRESHOLD:
                        message1 = "You'd probably like "
                    else:
                        message1 = "You probably wouldn't like "
                    return render_template("index.html", rating = rating, title = title, link = link, message1 = message1, message2 = message2, threshold = THRESHOLD)
            except Exception as e:
                print(str(e))
                return render_template("index.html", error = "You must provide a VALID UserID and/or MovieID", rating = rating)
        elif rec == "Get A Personalized Movie Recommendation List":
            try:
                personal = get_personal_list(userid, users, movies, tags)
                return render_template("recommendations.html", userid = userid, personal = personal)
            except Exception as e:
                print(str(e))
                return render_template("index.html", error = "You must provide a VALID UserID", rating = rating)
        elif rec == "Clear":
            return redirect(url_for('index'))
    return render_template("index.html", rating = rating)

@app.route('/idlist', methods = ['POST', 'GET'])
def idlist():
    if request.method == "POST":
        req = request.form
        letter = req["letter"]
        table = make_table(letter, movies)
        return render_template("idlist.html", table = table)
    return render_template("idlist.html")

if __name__ == '__main__': 
	app.run(debug = True)