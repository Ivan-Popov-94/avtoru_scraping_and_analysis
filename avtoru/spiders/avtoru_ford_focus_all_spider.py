# How to use this spider

# Fill out search form on avto.ru as you want
# Call Toggle Tools ( Ctrl + Shift + I)
# Press  button "Показать xxx предложений" on site page
# On Tab "Network" (Toggle Tools) look for URL
#   https://auto.ru/-/ajax/desktop/listing/
# Copy JSON request from the right for this POST request (Request tab)
# Past this to file project_path/request_data/body.json
# If don't work, try set ROBOTSTXT_OBEY = False in settings.py
# Comand for run script
# scrapy runspider project_path/avtoru/spiders/avtoru_ford_focus_all_spider.py

import json
from pathlib import Path
import os
from scrapy import Request, Spider

url = 'https://auto.ru/-/ajax/desktop/listing/'
request_data = {'headers': '', 'cookies': '', 'body': ''}
project_path = Path(__file__).parents[2]

for k in request_data.keys():
    with open(os.path.join(project_path, f'request_data/{k}.json'), 'r') as f:
        request_data[k] = json.load(f)
request_data['body']['page'] = 1
request_data['body'] = json.dumps(request_data['body'])


class AvtoruSpider(Spider):
    name = os.path.basename(__file__)[:-3]
    pages = 1
    response_path = os.path.join(project_path, f'responses/{name}')
    request_kwargs = {'url': url,
                      'method': 'POST',
                      'dont_filter': True,
                      'cookies': request_data['cookies'],
                      'headers': request_data['headers']
                      }

    def start_requests(self):

        yield Request(**self.request_kwargs,
                      body=request_data['body'],
                      callback=self.parse_first)

    def parse_first(self, response):
        if not os.path.exists(self.response_path):
            os.mkdir(self.response_path)
        filename = os.path.join(self.response_path, 'response_page_1.json')
        with open(filename, 'wb') as f:
            f.write(response.body)
            self.pages = json.loads(response.body)[
                'pagination']['total_page_count']
            print(f'\n<<< Number of processed pages: {self.pages} >>>\n')

        for page in range(2, self.pages + 1):
            yield Request(**self.request_kwargs,
                          body=request_data['body'].replace('"page": 1',
                                                            f'"page":{page}'),
                          callback=self.parse,
                          cb_kwargs=dict(page=page))

    def parse(self, response, page):
        filename = os.path.join(self.response_path,
                                f'response_page_{page}.json')
        with open(filename, 'wb') as f:
            f.write(response.body)
