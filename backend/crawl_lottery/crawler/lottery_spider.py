import scrapy
import datetime
from pymongo.database import Database
import scrapy.http
import crawler.constants as constants

class LotterySpider(scrapy.Spider):
    name = 'lottery_spider'
    
    def __init__(self, channels: list[str], date: datetime.datetime, db: Database, *args, **kwargs):
        super(LotterySpider, self).__init__(*args, **kwargs)
        self.channels = channels
        self.date = date
        self.db = db
        self.start_urls = self.generate_urls()

    def generate_urls(self):
        urls = []
        for channel in self.channels:
            
            formatted_date = self.date.strftime('%d-%m-%Y')

            url1 = constants.minh_ngoc_channel_urls[channel].replace("{date}", formatted_date)
            url2 = constants.kqxs_channel_urls[channel].replace("{date}", formatted_date)
            url3 = constants.xskt_channel_urls[channel].replace("{date}", formatted_date)
            # url1 = f'https://www.xoso.net/getkqxs/{channel}/{self.date}.js'
            # url2 = f'https://www.kqxs.vn/mien-trung/xo-so-{channel}?date={self.date}'
            # url3 = f'https://xskt.com.vn/xs{channel}/ngay-{self.date}'
            urls.append([url1, url2, url3])  # Group URLs for each channel
        return urls

    def start_requests(self):
        for url_group in self.start_urls:
            yield scrapy.Request(url=url_group[0], callback=self.parse, errback=self.handle_error, meta={'url_group': url_group, 'index': 0})

    def handle_error(self, failure):
        url_group = failure.request.meta['url_group']
        index = failure.request.meta['index']
        if index + 1 < len(url_group):
            next_url = url_group[index + 1]
            yield scrapy.Request(url=next_url, callback=self.parse, errback=self.handle_error, meta={'url_group': url_group, 'index': index + 1})

    def parse(self, response: scrapy.http.Response):
        # Simulate parsing of lottery data from the URL and structure it
        response.meta
        data = {
            'station': 'example-station',
            'date': self.date,
            'results': [
                {'prize': 'First', 'numbers': ['123456']},
                {'prize': 'Second', 'numbers': ['654321', '789012']}
            ]
        }
        # Store the parsed data in MongoDB
        self.db.kq_lottery.insert_one(data)

        

    

    
