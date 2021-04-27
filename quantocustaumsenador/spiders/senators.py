import scrapy
from scrapy.spiders import CrawlSpider
from ..items import SenatorItem

class SenatorsSpider(CrawlSpider):
    name = 'senators'
    base_url = 'https://www25.senado.leg.br/web/transparencia/sen/em-exercicio/-/e/por-nome'

    def __init__(self):
        pass

    def start_requests(self):
        yield scrapy.Request(url=self.base_url,
                             callback=self.parse_senators_list)

    def parse_senators_list(self, response):
        """
        This function collects all the senators and it's basic informations.
        """

        senators_list = response.xpath('//*[contains(@id,"senadoresemexercicio-tabela-senadores")]/tbody/tr')

        for senator in senators_list:
            meta = { 
                'url' : senator.xpath('td[1]/a/@href').extract_first(),
                'name' : senator.xpath('td[1]/a/text()').extract_first(),
                'party' : senator.xpath('td[2]//text()').extract_first(),
                'fu' : senator.xpath('td[3]//text()').extract_first(),
                'period' : senator.xpath('td[4]//text()').extract_first(),
                'phones' : senator.xpath('td[5]//text()').extract_first(),
                'email' : senator.xpath('td[6]//text()').extract_first()
            }
            
            yield scrapy.Request(url=meta.get('url'),
                                 meta=meta,
                                 callback=self.parse_senator_page)

    def parse_senator_page(self, response):
        """
        It's also needed to grab the senator address, so this function does it.
        """

        senator = SenatorItem()
        
        senator['url'] = response.meta.get('url')
        senator['name']  = response.meta.get('name')
        senator['party'] = response.meta.get('party')
        senator['fu'] = response.meta.get('fu')
        senator['period'] = response.meta.get('period')
        senator['phones'] = response.meta.get('phones')
        senator['email'] = response.meta.get('email')
        senator['address'] = response.xpath('//div[contains(@class,"dadosPessoais")]/dl/dd[4]//text()').extract_first().strip()
        
        yield senator