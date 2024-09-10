from flask import Flask, render_template, request, redirect, url_for, session
import os
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# Function to get articles from the filesystem
def get_articles():
    articles = []
    articles_dir = 'articles'
    for filename in os.listdir(articles_dir):
        if filename.endswith('.json'):
            filepath = os.path.join(articles_dir, filename)
            with open(filepath, 'r') as file:
                article = json.load(file)
                articles.append(article)
    return articles

# Home page route
@app.route('/')
def home():
    articles = get_articles()
    return render_template('home.html', articles=articles)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple user authentication (change it to a more secure way for production)
        if username == 'admin' and password == 'password':  # Hardcoded for now
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

# Dashboard route (Admin area)
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    articles = get_articles()
    return render_template('dashboard.html', articles=articles)

# Admin route to add articles
@app.route('/admin/add', methods=['GET', 'POST'])
def add_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time

        # Save the new article as a JSON file
        new_article = {
            'id': len(get_articles()) + 1,
            'title': title,
            'content': content,
            'date': date
        }
        filepath = os.path.join('articles', f'article_{new_article["id"]}.json')
        with open(filepath, 'w') as file:
            json.dump(new_article, file)

        return redirect(url_for('dashboard'))

    return render_template('add_article.html')

# Route to edit an article
@app.route('/admin/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    articles = get_articles()
    article = next((article for article in articles if article['id'] == article_id), None)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Update the date to the current time

        # Update the article
        article['title'] = title
        article['content'] = content
        article['date'] = date

        filepath = os.path.join('articles', f'article_{article_id}.json')
        with open(filepath, 'w') as file:
            json.dump(article, file)

        return redirect(url_for('dashboard'))

    if article:
        return render_template('edit_article.html', article=article)
    return "Article not found", 404

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

# Route to view a single article
@app.route('/article/<int:article_id>')
def view_article(article_id):
    articles = get_articles()
    article = next((article for article in articles if article['id'] == article_id), None)
    if article:
        return render_template('article.html', article=article)
    return "Article not found", 404

if __name__ == '__main__':
    app.run(debug=True)
