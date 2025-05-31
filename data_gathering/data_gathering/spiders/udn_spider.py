import scrapy


class UdnSpiderSpider(scrapy.Spider):
    name = "udn_spider"
    allowed_domains = ["udn.com"]
    #https://udn.com/news/breaknews/1/0#breaknews
    start_urls = ["https://udn.com/news/breaknews/1/0#breaknews"]

    def parse(self, response):
        for link in response.xpath('//*[@class="story-list__text"]//a/@href'):
            yield response.follow(link,self.parse_article)

    def parse_article(self, response):
        yield {
            "title": response.xpath('//*[@class="article-content__title"]/text()').get(),
            "paragraph":response.xpath('//*[@class="article-content"]//p/text()').getall()
        }


  
