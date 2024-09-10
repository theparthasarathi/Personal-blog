# Personal Blog Project

This is a simple personal blog application where users can read articles, and the admin (you) can add, edit, or delete articles. The blog uses the filesystem to store articles as JSON files, and basic authentication is implemented to protect the admin section.

## Features

- **Guest Section**:
  - **Home Page**: Displays the list of all published articles.
  - **Article Page**: Displays the content of a single article, along with the date and time of publication.
  
- **Admin Section**:
  - **Dashboard**: Displays all articles with options to add, edit, or delete articles.
  - **Add Article Page**: Allows the admin to add a new article with a title, content, and the current date and time.
  - **Edit Article Page**: Allows the admin to edit the title, content, and date of an existing article.

## Admin Credentials

- **Username**: `admin`
- **Password**: `let_me_in`

These credentials are hardcoded in the application for simplicity. You can change them by editing the `app.py` file in the login route.

## Project Structure

- **Backend**: Flask is used to handle the routing, form submissions, and authentication.
- **Frontend**: HTML and CSS are used to render the pages. No JavaScript is used in this project.
- **Storage**: Articles are stored as JSON files in the `articles/` directory on the filesystem.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/personal-blog.git
    cd personal-blog
    ```

2. Install dependencies:

    ```bash
    pip install flask
    ```

3. Run the application:

    ```bash
    python app.py
    ```

4. Open your browser and navigate to `http://127.0.0.1:5000/`.

## Usage

- Navigate to the home page to see a list of all articles.
- Click on an article to view its full content.
- Admin login: Go to `/login` and log in with the admin credentials to access the dashboard.
- From the dashboard, you can add new articles, edit existing ones, or delete them.

## Future Improvements

- Add user comments functionality.
- Implement categories and tags for articles.
- Introduce a search feature to filter articles by title or content.
- Switch to a database (like SQLite or PostgreSQL) for better scalability.

