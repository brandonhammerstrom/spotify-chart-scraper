# Spotify Top 200 Charts Scraper

This script scrapes the Spotify top 200 charts website found at the [link](https://spotifycharts.com/regional) for both daily and weekly feeds. The scraped data is then returned as a single csv file with all territories reported by Spotify in `~/Downloads/`. 

# Charts
* Top 200 songs daily/weekly for all territories
* Daily is calculated every day by Spotify
    * **Note:** if calling `latest` the chart pulled will be for the day prior as new charts are added one day behind
* Weekly is calculated every Thursday by Spotify
    * **Note:** if calling `latest` the chart pulled will be for last Thursday's date unless today happens to be Thursday

# Requirements
* Check `requirements.txt` file for non standard lib Python packages

# How To Run
1. Clone the repo to your local machine
2. Open a terminal
3. Enter command `$ python main.py --chart {daily, weekly} --date {latest, YYYY-MM-DD}`
    * EX: `$ python main.py --chart daily --date 2021-08-01`
    * EX: `$ python main.py --chart weekly --date latest`
    * **Note:** choose only `daily` or `weekly` depending on what chart you want to pull
    * If you have issues type `$ python main.py -h` to see the help menu
4. Script will run for all territories reported by Spotify, parse the data, and download to a single csv filem

