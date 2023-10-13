from scraper.bleacher_report_scraper import scrape
import time

if __name__ == '__main__':
    while True:
        scrape()
        print('### waiting... ###')
        time.sleep(60 * 60 * 24)