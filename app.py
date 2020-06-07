from flask import Flask, render_template, session
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = "someth1ng super secret and maybe eben rand0m"


# with thanks to https://overiq.com/flask-101/sessions-in-flask/#how-to-read-write-and-delete-session-data
@app.route("/", strict_slashes=False)
@app.route("/hi", strict_slashes=False)
def hi():
    return "HELLO! Total visits: ¯\_(ツ)_/¯"


@app.route("/hello", strict_slashes=False)
def hello():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1
    else:
        session['visits'] = 1  # setting session data
    return "HELLO! Total visits: {}".format(session.get('visits'))


def get_movies(title):
    con = sqlite3.connect("database.sqlite")
    cur = con.cursor()
    # run the query -- it's been updated to include title
    # and to use the "like" operator
    cur.execute("""
        SELECT tid, title, type, year, runtime, genres
        FROM title
        WHERE title like ?
        ORDER by title
        """, ("%"+str(title)+"%",))

    # get the results as a list
    results = list(cur)
    # disconnect from the database
    con.close()
    # display the results (using column indexes)
    return results


@app.route("/movies", strict_slashes=False)
@app.route("/movies/<title>", strict_slashes=False)
def list_movies(title="%"):
    movie_search_results = get_movies(title)
    query = title
    if title == "%":
        query = "All"
    
    ##################################
    # below this line is the code for the sort of ugly starting version
    output = query
    line_break = "<br>"
    for movie in movie_search_results:
        movie_title = movie[1]
        output = output + line_break + movie_title
    return output
    
    ##################################
    # this next section is the code for the "next steps" versions
    # 1. you can choose which of the templates you want to use and un-comment that line
    # 2. and you should also uncomment the 2 lines that begin with "return render_template"
    # template = "template.html"
    # template = "simple.html"
    # template = "basic.html"
    # return render_template(template, query=query,
    #                      movies=movie_search_results)
