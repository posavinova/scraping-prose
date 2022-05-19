import scrapy
from itemloaders import ItemLoader
from proza_scraping.items import StoriesItem


class StoriesSpider(scrapy.Spider):
    name = "stories"

    allowed_domains = ["proza.ru"]

    topic = "02"
    start_urls = [f"https://proza.ru/texts/list.html?topic={topic}"]

    def parse(self, response, **kwargs):
        stories = response.css("index > ul li")
        for story in stories:
            loader = ItemLoader(item=StoriesItem(), selector=story)
            loader.add_css("title", "li a.poemlink::text")
            loader.add_css("link", "li a.poemlink::attr(href)")
            loader.add_css("author", "li a.authorlink::text")
            loader.add_css("author_link", "li a.authorlink::attr(href)")
            loader.add_css("date", "small::text")

            stories_item = loader.load_item()

            story_url = story.css("li a.poemlink::attr(href)").get()

            yield response.follow(story_url, self.parse_story, cb_kwargs={"stories_item": stories_item})

        pages = response.css("a[href*='start']::attr(href)").getall()
        for page in pages:
            yield response.follow(page, self.parse)

        prev_day = response.css("div.textlink > a:nth-child(1)::attr(href)").get()

        yield response.follow(prev_day, self.parse)

    def parse_story(self, response, stories_item):
        loader = ItemLoader(item=stories_item, response=response, selector=response)

        loader.add_css("text", "div.text::text")
        yield loader.load_item()
