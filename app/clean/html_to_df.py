import logging
import pandas as pd
import datetime
from bs4 import BeautifulSoup


# getting a logger
logger = logging.getLogger(__name__)


def html_parser(html, country, chart, chart_date):
    """This function parses the html returned by Spotify
    chart links and returns a DataFrame"""

    logger.info(f"Parsing HTML data for Spotify {country} chart data")

    # empty list for final data
    data = []

    # for getting the header from the HTML file
    list_header = []
    soup = BeautifulSoup(html, "html.parser")
    header = soup.find_all("table")[0].find("tr")

    for items in header:
        try:
            list_header.append(items.get_text())
        except:
            continue

    # getting HTML data
    HTML_data = soup.find_all("table")[0].find_all("tr")[1:]

    for element in HTML_data:
        sub_data = []
        for sub_element in element:
            try:
                sub_data.append(sub_element.get_text())
            except:
                continue
        data.append(sub_data)

    logger.info(f"HTML data parsed for Spotify {country} chart data")
    logger.info(f"Converting to DataFrame for Spotify {country} chart data")

    # adding extra values to list_header
    list_header.append("col_1")
    list_header.append("col_2")

    # updating column headers
    list_header[0] = "col_1"
    list_header[1] = "position"
    list_header[2] = "col_3"
    list_header[3] = "title"
    list_header[4] = "streams"

    # converting to df
    df = pd.DataFrame(data=data, columns=list_header)

    # dropping columns not needed
    df.drop(columns=["col_1", "col_3"], inplace=True)

    # fixing "\n"
    df["title"].replace(r"\n", " ", inplace=True, regex=True)

    # fixing spaces at end and beginning of string
    df["title"] = df["title"].str.strip()

    # fixing title and artist
    df["artist"] = df["title"].str.split(" by").str[1]
    df["title"] = df["title"].str.split(" by").str[0]

    # adding in terrtiory
    df["territory"] = country

    # adding chart date
    if chart == "daily":
        if chart_date == "latest":
            df["chart_date"] = datetime.datetime.now().date()
        else:
            df["chart_date"] = datetime.datetime.strptime(chart_date, "%Y-%m-%d").date()

    elif chart == "weekly":
        if chart_date == "latest":
            # getting date number
            thursday = 3
            current_date = datetime.datetime.now().date()
            day_number = datetime.datetime.weekday(current_date)
            # checking dates and updating df accordingly
            if day_number > thursday:
                week_delta = datetime.timedelta(days=day_number - thursday)
                thursday_date = current_date - week_delta
                df["chart_date"] = thursday_date
            elif day_number < thursday:
                week_delta = datetime.timedelta(days=thursday - day_number)
                thursday_date = (current_date + week_delta) - datetime.timedelta(days=7)
                df["chart_date"] = thursday_date
            elif day_number == thursday:
                df["chart_date"] = current_date
        else:
            df["chart_date"] = datetime.datetime.strptime(chart_date, "%Y-%m-%d").date()

    # adding chart pulled date
    df["chart_data_pulled_date"] = datetime.datetime.now().date()

    # fixing order
    df = df[
        [
            "position",
            "title",
            "artist",
            "streams",
            "territory",
            "chart_date",
            "chart_data_pulled_date",
        ]
    ]

    logger.info(f"DataFrame created successfully for Spotify {country} chart data")

    return df
