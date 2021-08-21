import logging
import pandas as pd
from datetime import datetime
from concurrent.futures.thread import ThreadPoolExecutor


from clean.html_to_df import html_parser
from scrape.spotify_scraper import spotify_countries, web_scraper
from userargs.arguments import user_args, weekly_valid_dates, daily_valid_dates
from output.output_helper import output_path


# getting a logger
logger = logging.getLogger()


def spotify_chart_scraper(chart, chart_date):
    """This is the main entry point function for all modules"""

    start_time = datetime.now()

    logger.info(f"Scraping new Spotify top 200 {chart} chart data to csv")

    # getting territories
    territories = spotify_countries()

    # getting links
    if chart == "daily":
        if chart_date not in daily_valid_dates():
            raise ValueError(
                f"Daily chart date {chart_date} not valid. Please check help for valid dates"
            )
        links = {}
        for key, value in territories.items():
            links[
                key
            ] = f"https://spotifycharts.com/regional/{value}/daily/{chart_date}"

    elif chart == "weekly":
        if chart_date not in weekly_valid_dates():
            raise ValueError(
                f"Weekly chart date {chart_date} not valid. Please check help for valid dates"
            )
        links = {}
        for key, value in territories.items():
            links[
                key
            ] = f"https://spotifycharts.com/regional/{value}/weekly/{chart_date}"

    logger.info("Getting HTML data for countries")

    # getting HTML data
    html_data = {}
    with ThreadPoolExecutor() as ex:
        for key, value in links.items():
            html_data[key] = ex.submit(web_scraper, key, value)

    logger.info("HTML data gathered successfully")

    # parsing data
    dataframes = []
    for key, value in html_data.items():
        try:
            # parsing html to df
            df = html_parser(value.result(), key, chart, chart_date)

            logger.info(f"{key} DataFrame shape: {df.shape}")

            # adding to list of dataframes
            dataframes.append(df)
        except:
            logger.warning(f"{key} could not be parsed properly. Chart may not exist")
            continue

    logger.info("Creating final DataFrame")

    # creating one dataframe
    df = pd.concat(dataframes)

    logger.info("DataFrame successfully created")

    # sending to csv
    df.to_csv(output_path(f"spotify_top_200_{chart}_{chart_date}"), index=False)

    logger.info("Script complete. Check downloads folder for output")
    logger.info(f"Script completed in {datetime.now() - start_time}")


if __name__ == "__main__":

    # getting user args
    chart_option, chart_date = user_args()

    logging.basicConfig(
        format="%(asctime)s - %(project)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

    # used to pull in project code to log message
    old_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = old_factory(*args, **kwargs)
        record.project = chart_option
        return record

    logging.setLogRecordFactory(record_factory)

    spotify_chart_scraper(chart_option, chart_date)
