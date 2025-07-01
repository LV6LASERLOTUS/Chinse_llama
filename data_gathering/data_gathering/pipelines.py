# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re

class DataGatheringPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        paragraph:list = adapter.get('paragraph')
        spam:list = adapter.get('spam')
        print('======== This is the pipeline processing the paragraph ============')

        raw_text:str = ''.join(paragraph)
        raw_spam:str = ''.join(spam)

        # remove spam
        clean_text = raw_text.replace(raw_spam,'')
        # remove new lines
        clean_text = clean_text.replace('\n','')
        # remove url  https?:\/\/[^\s，。！？「」‘’“”：；、<>《》（）【】]+
        clean_text = re.sub('https?:\/\/[^\s，。！？「」‘’“”：；、<>《》（）【】]+','',clean_text)
        # remove english letter [A-Za-z]+[，]*
        clean_text = re.sub('[A-Za-z]+[，,]*','',clean_text)
        # remove empty braces  [\(<《（【]+[\s]*[\)>》）】]+
        clean_text = re.sub('[\(<《（【]+[\s]*[\)>》）】]+','',clean_text)
        
        
        adapter['paragraph'] = clean_text.strip()
        if 'spam' in adapter:
            del adapter['spam']

        return item
  