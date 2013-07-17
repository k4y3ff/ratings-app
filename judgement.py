from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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

    



@app.route("/user_list")
def user_list():
    
    user_list = model.session.query(model.User).limit(5).all()
    
    return render_template("user_list.html", users = user_list)


@app.route("/user_profile", methods = ['GET','POST'])
def login():

    user_id = request.args.get("id")

    user = model.session.query(model.User).get(user_id)

    return render_template("user_profile.html", user = user)
    
if __name__ == "__main__":
    app.run(debug = True)