import logging
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen


# getting a logger
logger = logging.getLogger(__name__)


def spotify_countries():
    """This function scrapes the chart report for available countries"""

    logger.info("Getting HTML data for Spotify countries")

    # submitting request
    req = Request(
        "https://spotifycharts.com/regional/",
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    # opening page
    page = urlopen(req)

    logger.info("Parsing HTML data for Spotify countries")

    # parsing for countries
    soup = bs(page.read().decode(), "html.parser")
    countries = {}
    ctys = soup.find("ul").findAll("li")
    for cty in ctys:
        countries[cty.get_text()] = cty["data-value"]

    logger.info("HTML data for Spotify countries parsed successfully")

    return countries


def web_scraper(country, url):
    """This function scrapes the data into html for future processing"""

    logger.info(f"Getting HTML data for Spotify {country} chart data")

    # submitting request and reading data
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    page = urlopen(req)
    chart_data = page.read().decode()

    logger.info(f"HTML data for Spotify {country} chart data successfully gathered")

    return chart_data
