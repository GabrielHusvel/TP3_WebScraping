import scrapy

class NoticiasSpider(scrapy.Spider):
    name = "noticias"
    allowed_domains = ["difusoranews.com"]

    # Categorias e número de páginas
    categories = [
        'bem-estar', 'cultura', 'economia', 'educacao', 'entretenimento', 
        'esportes', 'maranhao', 'mundo', 'policia', 'politica', 
        'oportunidade', 'tecnologia'
    ]
    
    # Gera URLs para todas as páginas de todas as categorias
    start_urls = [
        f'https://difusoranews.com/{category}/page/{x}/'
        for category in categories
        for x in range(1, 11)  # 10 páginas por categoria
    ]

    def parse(self, response):
        # Seleciona todos os artigos na página
        articles = response.css('article')

        for article in articles:
            yield {
                'category': response.url.split('/')[3],  # Extrai a categoria da URL
                'title': article.css('h3 a::text').get(),
                'link': article.css('h3 a::attr(href)').get(),
                'summary': article.css('p.text-secondary-700::text').get(),
                'date': article.css('span.text-sm.inline-block::text').get()
            }
