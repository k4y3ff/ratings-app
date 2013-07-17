from flask import Flask, render_template, redirect, request, session, g
import model

app = Flask(__name__)
Flask.secret_key = "khkeyjlhgchxf;oygfgfklugifxghjgcx"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html", error="")

    elif request.method == "POST":
        email= request.form["email"]
        password= request.form["password"]

        existing_user = model.session.query(model.User).filter_by(email = email, password = password).first()

        if existing_user:
            session['user_id'] = existing_user.id
            return redirect("user_profile?id=" +str(existing_user.id))
        else:
            return render_template("login.html", error="Incorrect username/password; Register if new user")

@app.route("/logout")
def logout():
    session.pop('user_id', None)

    return redirect("/")

@app.route("/movie")
def movie():
    
    movie_id = request.args.get("movie_id")
    movie = model.session.query(model.Movie).get(movie_id)

    if 'user_id' in session:
        user_id = session['user_id']
        rating = model.session.query(model.Rating).filter_by(user_id = user_id, movie_id = movie_id).first()
    else:
        rating = "Must Log Into Account to See Ratings"

    if rating != None and rating != "Must Log Into Account to See Ratings":
        return render_template("movie.html", movie = movie, rating = rating.rating)
    else:
        return render_template("movie.html", movie = movie, rating = "Not Rated")

@app.route("/movie_list")
def movie_list():

    movie_list = model.session.query(model.Movie).limit(20).all()

    return render_template("movie_list.html", movie_list= movie_list)

@app.route("/new_user", methods =['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("new_user.html", error = "")

    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]
        zipcode = request.form["zipcode"]

        existing_dup_users = model.session.query(model.User).filter_by(email = email).first()

        if existing_dup_users == None:
            user = model.session.add(model.User(email = email, password = password,
                                          age = age,
                                          zipcode = zipcode))

            model.session.commit()

            user = model.session.query(model.User).filter_by(email = email).first()

            return redirect("user_profile?id=" + str(user.id))

        else:
            return render_template("new_user.html", error = "Account with associated email already exists.")

@app.route("/update_rating", methods=['GET','POST'])
def update_rating():

    if request.method == "POST":
        rating = request.form["rating"]
        movie_id= request.form["movie_id"]

    user_id = session['user_id']

    current_rating = model.session.query(model.Rating).filter_by(movie_id= movie_id, user_id = user_id).first()
    
    if current_rating != None:
        current_rating.rating = rating
        model.session.update(current_rating.rating)
        model.session.commit()
    else:
        model.session.add(model.Rating(movie_id = movie_id, user_id = user_id, rating = rating))
        model.session.commit()

    return redirect("/movie?movie_id="+str(movie_id))


@app.route("/user_list")
def user_list():
    
    user_list = model.session.query(model.User).limit(5).all()
    
    return render_template("user_list.html", users = user_list)


@app.route("/user_profile", methods = ['GET','POST'])
def user_profile():

    user_id = request.args.get("id")

    user = model.session.query(model.User).get(user_id)

    return render_template("user_profile.html", user = user)


    
if __name__ == "__main__":
    app.run(debug = True)