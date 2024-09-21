    # def start_requests(self) -> Iterable[scrapy.Request]:
    #     return super().start_requests()

    # def parse(self, response):
    #     item = PokemonscraperItem()
    #     for tag in response.css('ul.products > li'):
    #         item['name'] = tag.css('a > h2::text').get()
    #         item['price'] = float(tag.css('a > span.price > span::text').get())
    #         item['link'] = tag.css('a::attr(href)').get()
    #         yield item
import scrapy

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com']

    def parse(self, response):
        books = response.css('article.product_pod')
        for book in response.css('article.product_pod'):
            yield {
                'title': book.css('h3 a::attr(title)').get(),
                'price': book.css('p.price_color::text').get(),
                'availability': book.css('p.instock.availability::text').re_first('\S+'),
                'rating': book.css('p.star-rating::attr(class)').re_first('star-rating (\w+)'),
                'link': book.css('h3 a::attr(href)').get()
            }

        # Segue para a próxima página
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

