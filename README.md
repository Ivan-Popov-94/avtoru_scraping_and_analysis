# avtoru_scraping_and_analysis 
Scrapy spider for scraping data (sale ads) from avto.ru 


## How to use spider 
 
- Fill out search form on avto.ru as you want 
- Call Toggle Tools ( Ctrl + Shift + I) 
- Press  button "Показать xxx предложений" on site page 
- On Tab "Network" (Toggle Tools) look for URL 
-   https://auto.ru/-/ajax/desktop/listing/ 
- Copy JSON request from the right for this POST request (Request tab) 
- Past this to file project_path/request_data/body.json 
 
- If don't work, try set ROBOTSTXT_OBEY = False in settings.py 
 
- Comand for run script (from project_path directory) 
- scrapy runspider project_path/avtoru/spiders/spider_name.py 
