from flask import Flask, url_for, render_template, request, redirect, flash
import sqlite3
import matplotlib.pyplot as plt
from sent_pre import preprocess_input, model

app = Flask(__name__)
app.config['DATABASE'] = 'instance/app.db'
app.secret_key = 'lol'

def get_db():
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


@app.route("/")
def hello_world():
    return render_template("hello.html")

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
    
@app.route('/dashboard', methods=['POST'])
def show_dashboard():
    if request.form['username'] == 'admin' and request.form['password'] == 'admin':
        sents = ""
        db = get_db()
        cursor = db.cursor()
        column_name = 'sentiment'
        table_name = 'reviews'
        query = f"SELECT {column_name} FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            sents += f"{row[column_name]} "

        db.close()

        labels = 'Positive', 'Negative'
        pos_count = sents.count('positive')
        neg_count = sents.count('negative')
        total = pos_count + neg_count
        sizes = [pos_count, neg_count]

        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
        ax1.axis('equal')

        plt.savefig('static/images/fin.png')

        return render_template('dashboard.html', total_reviews=total, positive_reviews=pos_count, negative_reviews=neg_count)
    return f'Wrong credentials!'

@app.route('/rate')
def rate():
    return render_template('review.html')

@app.route('/submit-review', methods=['POST'])
def insert_into_db():
    review = request.form['review']
    token = preprocess_input(review)
    prediction = model.predict(token)

    sentiment = 'positive' if prediction[0] > 0.5 else 'negative'

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO reviews (review_text, sentiment) VALUES (?, ?)
    """, (review, sentiment))
    db.commit()
    db.close()

    return render_template('thanks.html')