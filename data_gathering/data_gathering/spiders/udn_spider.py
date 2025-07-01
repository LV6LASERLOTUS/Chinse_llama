import scrapy
from pathlib import Path
from data_gathering.items import DataGatheringItem
import json

class UdnSpider(scrapy.Spider):
    name = "udn_spider"
    
    #Ajax api: https://udn.com/api/more?page=0&id=&channelId=1&cate_id=0&type=breaknews

    start_urls = [
        "https://udn.com/api/more?page=0&id=&channelId=1&cate_id=0&type=breaknews",
        # "https://udn.com/api/more?page=1&id=&channelId=1&cate_id=0&type=breaknews",
        # "https://udn.com/api/more?page=2&id=&channelId=1&cate_id=0&type=breaknews"
    ]

    def parse(self, response):
        BASE_URL = "https://udn.com"
        raw_bytes = response.body
        Path('./raw_data/urls.json').write_bytes(raw_bytes)
        json_data= json.loads(raw_bytes)

        article_urls=[]
        for article in json_data["lists"]:
            full_url = BASE_URL + article["titleLink"]
            article_urls.append(full_url)

        print(f"============ Retrieving Article {len(article_urls)}===============")
        
        for url in article_urls:
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        item = DataGatheringItem()
        item['article_url'] = response.url
        item['title'] = response.xpath('//*[@class="article-content__title"]/text()').get()
        item['paragraph'] = response.xpath('//div[@class="article-content__paragraph"]//p/text()').getall() 
        item['spam'] = response.xpath('//div[@class="story-list__news"]//p/text()').getall()
        yield item

  
