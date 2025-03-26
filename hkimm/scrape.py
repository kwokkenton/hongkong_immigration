# import relevant packages
import logging
import time
from datetime import date

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# These were determined empirically
headers = [
    "Date",
    "Control Point",
    "Hong Kong Residents_Arrival",
    "Mainland Visitors_Arrival",
    "Other Visitors_Arrival",
    "Hong Kong Residents_Departure",
    "Mainland Visitors_Departure",
    "Other Visitors_Departure",
]

# Number of header and footer rows to skip
N_SKIP_HEAD_ROWS = 5
N_SKIP_END_ROWS = 1


class Scraper:
    def __init__(self, N_tries=5, time_delay_s_linear=0.05):
        # N_tries is the number of times to repeat scraping
        # time_delay_s_linear is the time in seconds to wait between trying to scrape again
        options = Options()
        options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=options)
        self.N_tries = N_tries
        self.time_delay_s_linear = time_delay_s_linear

    def get_df(self, day: date):
        date_string = day.strftime("%Y%m%d")
        url = "https://www.immd.gov.hk/eng/facts/passenger-statistics.html?d={}.html".format(
            date_string
        )
        for i in range(self.N_tries):
            try:
                self.driver.get(url)
                time.sleep(self.time_delay_s_linear * (i + 1))
                df = self._get_df_from_URL(day)
                return df
            except (AttributeError, KeyError):
                logger.info(f"Retrying scrape {i+1}th time.")
                continue

        logger.info(f"Scraping for {day} failed.")
        return None
        

    def _get_df_from_URL(self, day: date):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        passenger_table = soup.find("table", class_="table-passengerTrafficStat")
        table = []

        # Skip header rows and footer rows
        for row in passenger_table.find_all("tr")[N_SKIP_HEAD_ROWS:-N_SKIP_END_ROWS]:
            table = append_row(row, table, day)
        df = pd.DataFrame(table)
        df_final = format_df(df)
        return df_final

    def __del__(self):
        logger.debug("Driver deleted.")
        self.driver.quit()


def append_row(row, table: list, day: date):
    """extracts data from one row of the web table and adds it to the big table"""

    # since format of the website is the same, can index locations corresponding to headers
    col_slices = [5, 6, 7, 10, 11, 12]

    row_data = row.find_all("td")

    # extract control point
    control_pt = row_data[3].get_text()
    # extract number data

    entry = {
        "date": day,
        "control_point": control_pt,
    }
    for s, tag in zip(col_slices, headers[2:]):
        num = row_data[s].get_text()
        num = int(num.replace(",", ""))
        entry[tag] = num
    # appends row entry to big table
    table.append(entry)
    return table


def format_df(df: pd.DataFrame):
    """Turns dataframe into upload-ready melted format.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        _type_: _description_
    """
    id_vars = ["date", "control_point"]
    new_vars = ["identity", "direction"]
    df_melted = df.melt(id_vars=id_vars, var_name="combined", value_name="value")

    # Split the combined column into two separate columns
    df_melted[["identity", "direction"]] = df_melted["combined"].str.split(
        "_", expand=True
    )
    df_melted = df_melted[id_vars + new_vars + ["value"]]
    df_arrivals = df_melted[df_melted.direction == "Arrival"].rename(
        columns={"value": "arrivals"}
    )
    df_departures = df_melted[df_melted.direction == "Departure"].rename(
        columns={"value": "departures"}
    )

    df_final = pd.merge(
        df_arrivals.drop("direction", axis=1),
        df_departures.drop("direction", axis=1),
        how="left",
        on=id_vars + [new_vars[0]],
    )
    return df_final
