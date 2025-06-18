import scrapy
from pathlib import Path
import json

class UdnSpiderSpider(scrapy.Spider):
    name = "udn_spider"
    
    #Ajax api: https://udn.com/api/more?page=0&id=&channelId=1&cate_id=0&type=breaknews

    start_urls = [
        "https://udn.com/api/more?page=0&id=&channelId=1&cate_id=0&type=breaknews",
        "https://udn.com/api/more?page=1&id=&channelId=1&cate_id=0&type=breaknews",
        "https://udn.com/api/more?page=2&id=&channelId=1&cate_id=0&type=breaknews"
    ]

    def parse(self, response):
        BASE_URL = "https://udn.com"
        raw_bytes = response.body
        Path('./raw_data/response.json').write_bytes(raw_bytes)
        json_data= json.loads(raw_bytes)

        article_urls=[]
        for article in json_data["lists"]:
            full_url = BASE_URL + article["titleLink"]
            article_urls.append(full_url)
        
        print("============ Retrieving Article ===============")
        
        for url in article_urls:
            yield scrapy.Request(url, callback=self.parse_article)
            break
    
    def parse_article(self, response):
        yield {
            "title": response.xpath('//*[@class="article-content__title"]/text()').get(),
            "paragraph":response.xpath('//*[@class="article-content"]//p/text()').getall()
        }


  
