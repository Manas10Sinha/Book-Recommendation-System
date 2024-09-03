from flask import Flask, render_template, request
import pickle

import numpy as np

import pandas as pd

popular_dict = pickle.load(open('popular_dict.pkl','rb'))
popular = pd.DataFrame(popular_dict)

pt = pickle.load(open('pt.pkl','rb'))
pt = pd.DataFrame(pt)

books = pickle.load(open('books.pkl','rb'))
books = pd.DataFrame(books)

similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
similarity_scores = pd.DataFrame(similarity_scores)

#popular_df = pickle.load(open('popular.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular['Book-Title'].values),
                           author = list(popular['Book-Author'].values),
                           image = list(popular['Image-URL-M'].values),
                            Votes= list(popular['num_ratings'].values),
                            Rating = list(popular['avg_ratings'].values)
                            )

@app.route('/recommend')
def recommend_ui():
    return render_template('recom.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    print(123)
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    return render_template("recom.html",data=data)

if __name__ == '__main__':
    app.run(debug=True)

