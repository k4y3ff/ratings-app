from datetime import datetime
import model
import csv
import unicodedata

def load_users(session):

    f = open("seed_data/u.user")
    txt =f.readlines()

    for line in txt:
        input_list = line.split("|")
        
        if input_list[-1][-1] == "\n":
            input_list[-1] = input_list[-1][:-1]

        user = model.User(id = input_list[0], age = input_list[1], zipcode = input_list[4])
        session.add(user)

    session.commit()


def load_movies(session):

    f = open("seed_data/u.item")
    txt = f.readlines()

    for line in txt:
        input_list = line.split("|")

        if input_list[-1][-1] == "\n":
            input_list[-1] = input_list[-1][:-1]

        title = input_list[1] 
        title = title.decode('latin-1')
        
        if input_list[2] != "":
            date_time = datetime.strptime(input_list[2], '%d-%b-%Y')
            movie = model.Movie(id = input_list[0], name = title, 
                                         released_at = date_time, 
                                         imdb_url = input_list[4])
        else:
            movie = model.Movie(id = input_list[0], name = input_list[1], imdb_url = input_list[4])

        session.add(movie)

    session.commit()


def load_ratings(session):
    
    f = open("seed_data/u.data")
    txt = f.readlines()

    for line in txt:
        input_list = line.split()
        
        rating = model.Rating(movie_id = input_list[1], user_id = input_list[0], rating = input_list[2])

        session.add(rating)

    session.commit()


def main(session):    
    
    # load_users(session)
    # load_movies(session)
    # load_ratings(session)

    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
