from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_movies(title):
    con = sqlite3.connect("database.sqlite")
    cur = con.cursor()
    # run the query -- it's been updated to include title 
    # and to use the "like" operator
    cur.execute("""
        SELECT tid, title, type, year, runtime, genres
        FROM title
        WHERE title like ?
        """, ("%"+str(title)+"%",))

    # get the results as a list
    results = list(cur)
    # disconnect from the database
    con.close()
    # display the results (using column indexes)
    return results


@app.route("/", strict_slashes=False)
@app.route("/<title>", strict_slashes=False)
def list_movies(title="%"):
    # template = "template.html"
    # template = "simple.html"
    # template = "basic.html"
    movie_search_results = get_movies(title)
    query = title
    if title == "%":
        query = "All"
    output = query
    line_break = "<br>"
    for movie in movie_search_results:
        movie_title = movie[1]
        output = output + line_break + movie_title
    #return render_template(template, query=query, 
    #                       movies=movie_search_results)
    # return f"{query}<br>{'<br>'.join([movie[1] for movie in movie_search_results])}"
    return output
