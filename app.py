from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Directory to store articles
ARTICLE_DIR = 'articles'

# Home Page (Guest Section)
@app.route('/')
def home():
    articles = []
    for article_file in os.listdir(ARTICLE_DIR):
        with open(os.path.join(ARTICLE_DIR, article_file), 'r') as f:
            articles.append(json.load(f))
    return render_template('home.html', articles=articles)

# Article Page (Guest Section)
@app.route('/article/<article_title>')
def article(article_title):
    article_file = f"{article_title}.json"
    with open(os.path.join(ARTICLE_DIR, article_file), 'r') as f:
        article = json.load(f)
    return render_template('article.html', article=article)

if __name__ == "__main__":
    app.run(debug=True)
