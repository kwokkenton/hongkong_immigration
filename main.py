from datetime import date, timedelta

from hkimm.upload import scrape_and_upload

day_to_scrape = date.today() - timedelta(days=1)
print(f'For {day_to_scrape}') 
scrape_and_upload(day_to_scrape)
