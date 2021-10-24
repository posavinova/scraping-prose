## Crawler for *www.proza.ru*

Start the spider from its root directory with the following command: 
```shell
$ scrapy crawl stories
```
***

To specify which sections to scrape set desired value for `start_urls` in`stories_spider.py` file.
```python
topic = "02"
start_urls = [f"https://proza.ru/texts/list.html?topic={topic}"]
```

>####*List of web-site's topics:*
>- *05* - миниатюры
>- *21* - новеллы 
>- *02* - рассказы
>- *30* - репортажи
>- *01* - повести
>- *04* - романы
>- *13* - драматургия
>- *07* - детективы
>- *23* - приключения
>- *06* - фантастика
>- *24* - фэнтези
>- *25* - ужасы
>- *26* - киберпанк
>- *03* - эротическая проза
>- *08* - юмористическая проза
>- *16* - ироническая проза
>- *09* - фельетоны
>- *27* - анекдоты
>- *28* - байки
>- *31* - история и политика
>- *10* - литературоведение
>- *32* - естествознание
>- *11* - публицистика
>- *33* - философия
>- *34* - религия
>- *35* - мистика
>- *18* - мемуары
>- *12* - критические статьи
>- *41* - литературные обзоры
>- *42* - музыкальные и кинообзоры
>- *17* - литература для детей
>- *51* - рассказы о детях
>- *52* - сказки
>- *50* - детское творчество
>- *39* - стихи
>- *43* - стихотворения в прозе
>- *15* - литературные переводы
>- *44* - проза на других языках

### Database storing

A pipeline for saving scraped literary pieces to SQLite database is enabled.
```python
CONNECTION_STRING = "sqlite:///proza_ru.db"
```
DB schema:

![db_schema](images\db_schema.png)
***
Test database file with 4k short stories is among the project files (`proza_ru_short_stories.db`)
***
* __Scrapy__ - https://docs.scrapy.org/
* __SQLAlchemy__ - https://docs.sqlalchemy.org/
