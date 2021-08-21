import argparse
import datetime


def daily_valid_dates():
    """Returns valid daily dates for spotify chart site"""

    start_date = datetime.datetime(2017, 1, 1).date()

    max_date = datetime.datetime.now().date()

    dates = [start_date]

    week_delta = datetime.timedelta(days=1)

    while start_date < max_date:
        start_date += week_delta
        dates.append(start_date)

    date_strings = [i.strftime("%Y-%m-%d") for i in dates]

    date_strings.append("latest")

    return date_strings


def weekly_valid_dates():
    """Returns valid weekly dates for spotify chart site"""

    start_date = datetime.datetime(2016, 12, 29).date()

    max_date = datetime.datetime.now().date()

    dates = [start_date]

    week_delta = datetime.timedelta(days=7)

    while start_date < max_date:
        start_date += week_delta
        dates.append(start_date)

    date_strings = [i.strftime("%Y-%m-%d") for i in dates]

    date_strings.append("latest")

    return date_strings


def user_args():
    """This function is used to control flow via main.py and DAGs"""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--chart",
        # "--chart",
        type=str,
        # expand list as needed
        choices=["daily", "weekly"],
        required=True,
        help="Choose either daily or weekly to pull that specific chart",
    )
    parser.add_argument(
        "--date",
        # "--date",
        type=str,
        # expand list as needed
        # choices=["latest", daily_valid_dates(), weekly_valid_dates()],
        required=True,
        help=f"""Select a date or choose latest. Dates can be as follows:
            string: latest (use for most up-to-date chart)
            daily: Any day in yyyy-mm-dd format
            weekly: Every thursday starting from 2016-12-29
        """,
    )
    args = parser.parse_args()

    chart = args.chart.lower()

    date_string = args.date.lower()

    return chart, date_string
