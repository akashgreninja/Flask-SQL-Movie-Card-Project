

from decimal import Decimal
from tkinter import Button
from django.forms import DecimalField
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
db=Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies-prime-halifax-final.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Movie(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.String(13),  nullable=False)
    description= db.Column(db.String(80),  nullable=False)
    rating = db.Column(db.String(80),  nullable=True)
    ranking= db.Column(db.String(80), nullable=True)
    review=db.Column(db.String(80),  nullable=True)
    img_url=db.Column(db.String(80),  nullable=False)

db.create_all()

class Visform(FlaskForm):
        rating = StringField("Your Rating Out of 10 e.g. 7.5")
        review = StringField("Your Review")
        submit = SubmitField("Done")

class formformovie(FlaskForm):
    movies=StringField("enter the movie")
    enter=SubmitField("click")        
# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )

# db.session.add(new_movie)
# db.session.commit()







@app.route("/")
def home():
    content = Movie.query.order_by(Movie.rating).all()
    # print(content)
    for i in range(len(content)):
        content[i].ranking=len(content)-i
    db.session.commit()
    return render_template("index.html" ,content=content)
    

@app.route("/add",methods=["POST","GET"])
def add():

    add_movie=formformovie()
    if add_movie.validate_on_submit():
        data=add_movie.movies.data
        headers={
        "query":{data},
         }
        request_1=requests.get("https://api.themoviedb.org/3/search/movie?api_key=131ff55d14f13fb83bfb1c3cc05dc71f",params=headers)
        data=request_1.json()
        send_data=data['results']
        return render_template("select.html",send_data=send_data)

        
    return render_template("add.html",form=add_movie)

@app.route("/edit",methods=["POST","GET"])
def edit():
    form = Visform()
    movie_id = request.args.get("id")

  
    moviee=Movie.query.get(movie_id)
    if form.validate_on_submit():
        
        moviee.rating=float(form.rating.data)
        moviee.review=form.review.data
        db.session.commit()  
        return redirect(url_for('home'))
    
    return render_template("edit.html",form=form)

@app.route("/delete")
def delete():
    get_id=request.args.get("id")
    to_delete=Movie.query.get(get_id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/update")
def update():
    get_title=request.args.get("title")
    headers={
    "query":get_title,
    }
    request_1=requests.get("https://api.themoviedb.org/3/search/movie?api_key=131ff55d14f13fb83bfb1c3cc05dc71f",params=headers)
    data=request_1.json()
    send_data=data['results']
    
    title_1=send_data[0]['original_title'].split("-")[0]
    review_1=send_data[0]['overview']
    year_1=send_data[0]['release_date']
    img_url_1=send_data[0]['poster_path']
    rating_1=send_data[0]['vote_average']

    new_list = Movie(
    title=title_1,
    year=year_1,
    description=review_1,
    rating=rating_1,
    img_url=f"https://image.tmdb.org/t/p/w500/{img_url_1}"
    )
    db.session.add(new_list)
    db.session.commit()
    return redirect(url_for("home"))


    
    # print(send_data)




if __name__ == '__main__':
    app.run(debug=True)
