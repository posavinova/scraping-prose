# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from proza_scraping.models import (
    Story,
    Meta,
    Author,
    db_connect,
    create_table,
)


class EmptyArticlesPipeline:
    def process_item(self, item, spider):
        if item.get("text") is None:
            raise DropItem(f"Unfilled article found: {item.get('title')}")
        else:
            return item


class DuplicatesPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        exist_story = (
            session.query(Story).filter_by(title=item.get("title")).first()
        )
        session.close()
        if exist_story is not None:
            raise DropItem(f"Duplicate article found: {item.get('title')}")
        else:
            return item


class SaveStoriesPipeline:
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        story = Story()
        meta = Meta()
        author = Author()

        story.title = item.get("title")
        story.text = item.get("text")

        meta.date = item.get("date")
        meta.link = item.get("link")

        author.name = item.get("author")
        author.link = item.get("author_link")

        exist_meta = session.query(Meta).filter_by(link=meta.link).first()
        if exist_meta is not None:
            story.meta = exist_meta
        else:
            story.meta = meta

        exist_author = session.query(Author).filter_by(name=author.name).first()
        if exist_author is not None:
            meta.author = exist_author
        else:
            meta.author = author

        try:
            session.add(story)
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

        return item
