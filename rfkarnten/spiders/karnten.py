import scrapy
import re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from ..items import RfkarntenItem

pattern = r'(\r)?(\n)?(\t)?(\xa0)?'

class KarntenSpider(scrapy.Spider):
    name = 'karnten'

    start_urls = ['https://www.raiffeisen.at/ktn/rlb/de/meine-bank/presse_msm_moved/pressemeldungen.html',
                  'https://www.raiffeisen.at/ktn/rlb/de/meine-bank/veranstaltungen.html'
                  ]

    def parse(self, response):
        links = response.xpath(
            '//div[@class="component-content-box-teaser "]/div[@class="cta-wrapper"]//a/@href').getall()
        yield from response.follow_all(links, self.parse_article)
        archiv = response.xpath('//div[@class="container"]/div[@class="btn-wrapper"]//a/@href').get()
        if archiv:
            yield response.follow(archiv, self.parse)

    def parse_article(self, response):
        item = ItemLoader(RfkarntenItem())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//section[@class="component-page-title component-spacer"]//text()').getall()
        title = re.sub(pattern, "", ''.join(title).strip()).replace('       ', '-')
        content = response.xpath(
            '//div[@class="component-text rte "]//text()|//div[@class="text-wrapper rte"]//text()').getall()
        content = ''.join([text.strip('\n') for text in content if text.strip('\n')]).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)
        return item.load_item()