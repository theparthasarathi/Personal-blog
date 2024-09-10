from flask import Flask, render_template, request, redirect, url_for, session
import os, json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'yoursecretkey'

ARTICLES_DIR = 'articles/'

# Ensure the articles directory exists
if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

# Function to read all articles from the filesystem
def load_articles():
    articles = []
    for filename in os.listdir(ARTICLES_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(ARTICLES_DIR, filename), 'r') as file:
                article = json.load(file)
                # Ensure each article has a date_time field
                if 'date_time' in article:
                    articles.append(article)
    return articles

# Home Page: Displays the list of articles
@app.route('/')
def home():
    articles_data = load_articles()  # Loading articles from filesystem
    return render_template('home.html', articles=articles_data)

# Article Page: Displays a single article
@app.route('/article/<filename>')
def article(filename):
    filepath = os.path.join(ARTICLES_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            article = json.load(file)
        return render_template('article.html', article=article)
    else:
        return 'Article not found', 404

# Admin: Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'let_me_in':
            session['admin'] = True
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid credentials', 403
    return render_template('login.html')

# Dashboard: List of articles and admin actions
@app.route('/dashboard')
def dashboard():
    if 'admin' in session:
        articles_data = load_articles()
        return render_template('dashboard.html', articles=articles_data)
    else:
        return redirect(url_for('login'))

# Add Article Page
@app.route('/add', methods=['GET', 'POST'])
def add_article():
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        article = {
            'title': title,
            'content': content,
            'date_time': date_time
        }

        filename = date_time.replace(' ', '_').replace(':', '-') + '.json'
        filepath = os.path.join(ARTICLES_DIR, filename)

        with open(filepath, 'w') as file:
            json.dump(article, file)

        return redirect(url_for('dashboard'))
    
    return render_template('add_article.html')

# Edit Article Page
@app.route('/edit/<filename>', methods=['GET', 'POST'])
def edit_article(filename):
    if 'admin' not in session:
        return redirect(url_for('login'))
    
    filepath = os.path.join(ARTICLES_DIR, filename)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        with open(filepath, 'r') as file:
            article = json.load(file)
        
        # Preserve the original date_time if present
        date_time = article.get('date_time', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        article = {
            'title': title,
            'content': content,
            'date_time': date_time
        }

        with open(filepath, 'w') as file:
            json.dump(article, file)

        return redirect(url_for('dashboard'))

    # Load article for editing
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            article = json.load(file)
        return render_template('edit_article.html', article=article)
    else:
        return 'Article not found', 404

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
