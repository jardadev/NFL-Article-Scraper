from utils.scrape_br import BrScraper
import time

# Scrape will execute every 24 hours
time_interval = 86400
while True:
    BrScraper.scrape_br()
    time.sleep(time_interval)