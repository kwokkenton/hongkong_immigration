import logging
from datetime import date

from tqdm import tqdm

from .postgres import NeonDatabase
from .scrape import Scraper
from .utils import get_date_list

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _upload_single(scraper: Scraper, database: NeonDatabase, day: date):
    success = False

    df = scraper.get_df(day)
    if df is not None:
        database.upload_df_to_neon(df)
        success = True
        return success
    else:
        return success


def scrape_and_upload(start: date, connection_string: str, end: date = None):
    """Scrape and upload to database between specified dates.

    Leaving end date as null only scrapes a single day.

    Args:
        start (date): Start date to process
        end (Optional: date): end date to process
    """
    if end == None:
        end = start

    scraper = Scraper()
    database = NeonDatabase(connection_string)

    date_list = get_date_list(start, end)
    for day in tqdm(date_list):
        _upload_single(scraper, database, day)
