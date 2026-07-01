# Google News RSS Scraper

A Flask web application that searches Google News RSS by keyword and country, then displays the latest news articles in a clean web interface.

## Features

- Search Google News by keyword
- Select any available country
- Automatic locale generation (hl, gl, ceid)
- Retrieves articles published within the last 24 hours
- Displays:
  - Article title
  - Source
  - Publication date
  - Original article link
- Stores recent search history
- Saves search results in SQLite using SQLAlchemy
- Responsive Bootstrap interface

---

## Technologies

- Python 3
- Flask
- SQLAlchemy
- SQLite
- BeautifulSoup4
- Requests
- Bootstrap 4
- PyCountry

---

## Project Structure

```
project/
│
├── app.py                 # Flask application
├── scrapper_news.py       # Google News RSS parser
├── templates/
│   └── index.html
├── instance/
│   └── site.db
└── requirements.txt
```

---

## How It Works

1. The user enters a search keyword.
2. The user selects a country.
3. The application automatically builds the correct Google News locale.
4. A request is sent to the Google News RSS endpoint.
5. XML is parsed using BeautifulSoup.
6. Results are stored in SQLite.
7. Search history and latest results are displayed on the page.

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/news-scraper-flask.git
cd news-scraper-flask
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## Example

Search:

```
Python
Country: United States
```

The application returns the latest Google News articles related to Python from the selected country.

---

## Future Improvements

- Pagination
- Export results to CSV
- Save favorite searches
- Background scheduled updates
- Docker support
- PostgreSQL support
- REST API

---

## Author

Developed by **Vlad Vise**