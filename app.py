from flask import Flask, redirect, render_template, request, url_for, session
from flask_sqlalchemy import SQLAlchemy
from scrapper_news import get_news
import pycountry

app = Flask(__name__)  # создаем экземпляр приложения Flask
app.config["SECRET_KEY"] = "dev-secret-key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # настраиваем базу данных SQLite
db = SQLAlchemy(app)  # создаем экземпляр SQLAlchemy для работы с базой


GOOGLE_NEWS_LANGUAGE_EXCEPTIONS = {
    "UA": "uk",      # Ukraine
    "US": "en",      # United States
    "GB": "en",      # United Kingdom
    "AU": "en",      # Australia
    "CA": "en",      # Canada
    "NZ": "en",      # New Zealand
    "IE": "en",      # Ireland

    "NO": "no",      # Norway
    "SE": "sv",      # Sweden
    "DK": "da",      # Denmark
    "GR": "el",      # Greece
    "JP": "ja",      # Japan
    "KR": "ko",      # South Korea
    "CN": "zh-CN",   # China
    "TW": "zh-TW",   # Taiwan

    "BR": "pt-BR",   # Brazil
    "PT": "pt-PT",   # Portugal

    "CZ": "cs",      # Czechia
    "EE": "et",      # Estonia
    "SI": "sl",      # Slovenia
    "IL": "he",      # Israel
    "IN": "en",      # India
    "ZA": "en",      # South Africa

    "CH": "de",      # Switzerland, выбрали немецкий как дефолт
    "BE": "fr",      # Belgium, выбрали французский как дефолт
}

def get_country_list():
    countries = []

    for country in pycountry.countries:
        countries.append({
            "code": country.alpha_2,
            "name": country.name
        })

    return sorted(countries, key=lambda country: country["name"])


def build_locale(country_code):
    country_code = country_code.upper()

    if country_code in GOOGLE_NEWS_LANGUAGE_EXCEPTIONS:
        language = GOOGLE_NEWS_LANGUAGE_EXCEPTIONS[country_code]
    else:
        language = country_code.lower()

    ceid_language = language.split("-")[0]

    return {
        "hl": language,
        "gl": country_code,
        "ceid": f"{country_code}:{ceid_language}"
    }


class Article(db.Model):  #  таблица Article для хранения поисковых запросов
    id = db.Column(db.Integer, primary_key=True)
    search_query = db.Column(db.String(20), nullable=False)  #  поисковый запрос

    def __repr__(self):  # метод для представления объекта Article в виде строки
        return f"Article('{self.id}', '{self.search_query}')"  # возвращаем строковое представление объекта Article


class Results(db.Model):  #  таблица Results для хранения результатов поиска
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  #  название статьи
    date = db.Column(db.String(20), nullable=False)  #  дата статьи
    link = db.Column(db.String(300), nullable=False)  #  ссылка на статью
    source = db.Column(db.String(300), nullable=False)  #  источник статьи
    search_query = db.Column(db.String(100), nullable=False)  #  поисковый запрос, связанный с результатом

    def __repr__(self):  # метод для представления объекта Results в виде строки
        return f"Results('{self.id}', '{self.title}', '{self.date}', '{self.source}')"  # возвращаем строковое представление объекта Results


# функция для сохранения поискового запроса в базе данных
def save_article(search_query):  
    article = Article(search_query=search_query)  #  создаем новый объект Article с поисковым запросом
    db.session.add(article)  #  добавляем объект Article в сессию базы данных
    db.session.commit()  #  сохраняем изменения в базе данных
    old_articles = Article.query.order_by(Article.id.desc()).offset(3).all()

    for old_article in old_articles:
        db.session.delete(old_article)

    db.session.commit()

# функция для сохранения результатов поиска в базе данных
def save_results(search_query, locale):
    Results.query.delete()

    news = get_news(search_query, locale)

    for item in news:
        result = Results(
            title=item["title"],
            date=item["date"],
            link=item["link"],
            source=item["source"],
            search_query=search_query
        )

        db.session.add(result)

    db.session.commit()


# функция для получения всех статей из базы данных
def get_articles():
    return Article.query.order_by(Article.id).all()  #  получаем все объекты Article из базы данных
    

# функция для получения всех результатов из базы данных
def get_results():
    return Results.query.order_by(Results.id).all()  #  получаем все объекты Results из базы данных

# определяем маршрут для главной страницы
@app.route("/", methods=['GET', 'POST'])  #  маршрут для главной страницы, поддерживающий GET и POST запросы
def index():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        country_code = request.form.get("country")
        if search_query and country_code:
            search_query = search_query.strip()
            session["country"] = country_code  # сохраняем выбранную страну в сессии
            locale = build_locale(country_code)
            try:
                save_article(search_query)  #  сохраняем поисковый запрос в базе данных
                save_results(search_query, locale)  #  сохраняем результаты поиска в базе данных
            except Exception as e:
                db.session.rollback()
                print("ERROR:", e)
        return redirect(url_for("index"))  #  перенаправляем пользователя обратно на главную страницу после обработки POST запроса
    return render_template('index.html', articles=get_articles(), results=get_results(), countries=get_country_list(), selected_country=session.get('country'))  #  рендерим шаблон и передаем статьи и результаты



def clear_tables_on_startup():
    Article.query.delete()
    Results.query.delete()
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        clear_tables_on_startup()

    app.run(debug=True)