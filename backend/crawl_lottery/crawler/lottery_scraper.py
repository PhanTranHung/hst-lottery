from time import time
from typing import Optional
import datetime
import re

import httpx
from loguru import logger as log
from parsel import Selector
from crawler import constants


http_client = httpx.Client(timeout=httpx.Timeout(10.0))
STOCK_CACHE = {}
CACHE_TIME = 10

def get_scrape_url(dict_channel_urls: dict[str, str], channel: str, date: datetime.datetime) -> str:
    formatted_date = date.strftime('%d-%m-%Y')
    scrape_url = dict_channel_urls[channel].replace("{date}", formatted_date)
    return scrape_url

# async def scrape_yahoo_finance(symbol):
#     """scrapes stock data from yahoo finance"""


#     log.info(f"{symbol}: scraping data")
#     response = await stock_client.get(
#         f"https://finance.yahoo.com/quote/{symbol}?p={symbol}"
#     )
#     sel = Selector(response.text)
#     parsed = {}
#     for row in sel.xpath(
#         '//div[re:test(@data-test,"(left|right)-summary-table")]//td[@data-test]'
#     ):
#         label = row.xpath("@data-test").get().split("-value")[0].lower()
#         value = " ".join(row.xpath(".//text()").getall())
#         parsed[label] = value
#     parsed["price"] = sel.css(
#         f'fin-streamer[data-field="regularMarketPrice"][data-symbol="{symbol}"]::attr(value)'
#     ).get()
#     parsed["_scraped_on"] = time()
#     STOCK_CACHE[symbol] = parsed
#     return parsed

def scrape_minh_ngoc(channel: str, date: datetime.datetime):
    scrape_url = get_scrape_url(constants.minh_ngoc_channel_urls, channel, date)
    response = http_client.get(scrape_url)
    response_text = response.text

    match = re.search(r'<div class="box_kqxs_mini">(.*?)</div>\'\);', response_text, re.DOTALL)

    if not match:
        raise ValueError("Failed to extract lottery results from the response.")

    extracted_content = match.group(1)
    sel = Selector(extracted_content)
    
    td_tags = sel.css("div.content tr:nth-child(n + 2) td:nth-child(2)").getall()

    for td in td_tags:
        print(td)

    # print("=========")
    # print(response.text)
    
    

