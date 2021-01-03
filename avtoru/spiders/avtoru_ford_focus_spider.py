# команда для запуска
# scrapy runspider /home/ivan/WORK/PYTHON/studying/scrapy_spiders/avtoru/avtoru/spiders/avtoru_ford_focus_spider.py
import os
import json
from scrapy import Request, Spider

url = 'https://auto.ru/-/ajax/desktop/listing/'

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "x-client-app-version": "6a285e532e",
    "x-page-request-id": "cbe735001ff05851bcd7153dc9ae8757",
    "x-client-date": "1609426263168",
    "x-csrf-token": "c230e8fe77024f3cbbf78395517d962a26e8246b09abb4b3",
    "x-requested-with": "fetch",
    "content-type": "application/json",
    "Origin": "https://auto.ru",
    "Connection": "keep-alive"
}

cookies = {
    "suid": "77bd90fab638c56c52fed3bd1ac66ac6.cb5c60d6bb8956a294e89a9e8ce8547a",
    "_ym_uid": "1605109755115538393",
    "_ym_d": "1609426187",
    "_ga": "GA1.2.55464298.1605109755",
    "_gac_UA-11391377-1": "1.1605109755.CjwKCAiAtK79BRAIEiwA4OskBqPVnLnE-OWPLXbkgfUNeb4XgixIxgDCKRbWiBzHJOxBRxSVMETIHBoC0ykQAvD_BwE",
    "autoru_sid": "a%3Ag5fe99b3f2tf6sn7vb53sei0aiup64ld.c3ade127741b13be8a41b77c95f4ee91%7C1609145151594.604800.QsRVJgb1b5HzJSDwv3sHRg.6U_498i3OYWx-fkBXKRd1frxHLR-0t76ZgHcmfc9wmg",
    "autoruuid": "g5fe99b3f2tf6sn7vb53sei0aiup64ld.c3ade127741b13be8a41b77c95f4ee91",
    "yuidcs": "1",
    "yuidlt": "1",
    "yandexuid": "3665367171600804463",
    "my": "YwA%3D",
    "crookie": "4TyVX0tNkf81LyAMnmu6cjjflhyPkMVOJGnJ1rAanVRrJfyn6eHUVWSKJApmPOBomrOMZIeYhe6A6wnAgg8CT3dua4c=",
    "cmtchd": "MTYwOTE0NTE1NjI2Mg==",
    "bltsr": "1",
    "proven_owner_popup": "closed",
    "counter_ga_all7": "1",
    "_gid": "GA1.2.363253879.1609340139",
    "tmr_reqNum": "5",
    "tmr_lvid": "cb9e1d747401cae47e2b3bd643704e98",
    "tmr_lvidTS": "1609341919716",
    "mindboxDeviceUUID": "90adeabe-5b8b-4585-a307-0df252c34f88",
    "directCrm-session": "%7B%22deviceGuid%22%3A%2290adeabe-5b8b-4585-a307-0df252c34f88%22%7D",
    "_csrf_token": "c230e8fe77024f3cbbf78395517d962a26e8246b09abb4b3",
    "from_lifetime": "1609426183537",
    "from": "direct",
    "gdpr": "0",
    "mmm-search-accordion-is-open-cars": "%5B0%5D",
    "listing_view_session": "{}",
    "listing_view": "%7B%22output_type%22%3Anull%2C%22version%22%3A1%7D",
    "_ym_isad": "1",
    "X-Vertis-DC": "sas",
    "_ym_visorc_22753222": "b",
    "_ym_visorc_260035": "w"
}

body = '''{"displacement_from":2000,
           "displacement_to":2000,
           "catalog_filter":[{"mark":"FORD","model":"FOCUS","generation":"2306579"}],
           "transmission":["ROBOT","AUTOMATIC"],
           "body_type_group":["SEDAN"],
           "engine_group":["GASOLINE"],
           "section":"all",
           "category":"cars",
           "page":1,
           "output_type":"list"}
       '''


class AvtoruSpider(Spider):
    name = "avtoru"
    pages = 1
    def start_requests(self):

        yield Request(url=url,
                      method='POST',
                      dont_filter=True,
                      cookies=cookies,
                      headers=headers,
                      body=body,
                      callback=self.parse_first)

    def parse_first(self, response):
        filename = '/home/ivan/WORK/PYTHON/studying/scrapy_spiders/avtoru/responses/ford_focus/response_page_1.json'
        with open(filename, 'wb') as f:
            f.write(response.body)
            self.pages = json.loads(response.body)['pagination']['total_page_count']
            print(f'\n<<< Number of processed pages: {self.pages} >>>\n')

        for page in range(2, self.pages + 1):
            yield Request(url=url,
                          method='POST',
                          dont_filter=True,
                          cookies=cookies,
                          headers=headers,
                          body=body.replace('"page":1', f'"page":{page}'),
                          callback=self.parse,
                          cb_kwargs=dict(page=page))

    def parse(self, response, page):
        filename = f'/home/ivan/WORK/PYTHON/studying/scrapy_spiders/avtoru/responses/ford_focus/response_page_{page}.json'
        with open(filename, 'wb') as f:
            f.write(response.body)