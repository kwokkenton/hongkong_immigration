import os
from datetime import date, timedelta

from dotenv import load_dotenv

from hkimm.upload import scrape_and_upload

# Load database url
if os.path.exists(".env"):
    # Load .env file
    load_dotenv()
    # Get the connection string from the environment variable
    connection_string = os.getenv("DATABASE_URL")
# On access using GitHub secrets
else:
    connection_string = os.environ["DATABASE_URL"]

day_to_scrape = date.today() - timedelta(days=1)
print(f"For {day_to_scrape}")
scrape_and_upload(day_to_scrape, connection_string)
