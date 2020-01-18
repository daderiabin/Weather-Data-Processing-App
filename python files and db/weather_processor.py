"""Handling User Input For The Project by Danylo Deriabin."""
from scrape_weather import WeatherScraper
from db_operations import DBOperations
from plot_operations import PlotOperations
import datetime as date
import urllib.request

# Assign Local Variables
now = date.datetime.now()
c_y = int(now.year)
c_m = int(now.month)

# Create Instances of Imported Classes
scraper = WeatherScraper()
db = DBOperations()
plot = PlotOperations()


def reset(scr):
    """Reset The Scraper To Defaults."""
    scr.isNumber = False
    scr.toSkip = False
    scr.inRow = False
    scr.isTarget = False
    scr.isHeader = False
    scr.td_counter = 0
    scr.th_counter = 0
    scr.date = ''
    scr.min = ''
    scr.max = ''
    scr.mean = ''
    scr.weather = {}
    scr.daily_temp = {}
    scr.dates = []
    scr.daily_temps = []


def option_one():
    """Handle Option One."""
    scraped_data = {}
    db.creator()
    for y in range(c_y, 1800, -1):
        if y == c_y:
            m_range = range(c_m, 0, -1)
        else:
            m_range = range(12, 0, -1)

        print("Processing " + str(y) + "...")
        for m in m_range:
            reset(scraper)
            with urllib.request.urlopen('https://climate.weather.gc.ca/climate_data/daily_data_e.html?StationID=27174&timeframe=2&StartYear=1840&EndYear=2018&Day=1&Year=' + str(y) + '&Month=' + str(m)) as resp:
                html = str(resp.read())
            scraper.feed(html)
            if scraper.MON != m:
                break
            else:
                scraped_data.update(scraper.weather)

        if scraper.YR != y:
            print("Year out of range.")
            break

    print("Inserting data to the DB...")
    db.inserter(scraped_data)
    print("Finished inserting data.")


def option_two(y1, y2):
    """Handle Option Two."""
    plot_data = {}

    if y1 > y2:
        years = range(y2, y1 + 1, 1)
    elif y2 > y1:
        years = range(y1, y2 + 1, 1)

    for m in range(1, 13):
        for y in years:
            row = db.reader(int(y), int(m))
            for k in row.keys():
                if k in plot_data.keys():
                    for v in row.values():
                        plot_data[k] = plot_data[k] + v
                else:
                    plot_data.update(row)

    plot.builder(plot_data, str(y1), str(y2))


while True:
    print("\nSelect one of the following options:")
    print("(1) Download a full set of weather data")
    print("(2) Build a plot for a year range of interest")
    print("(3) Exit")
    inp = input("Enter your selection: ")

    if inp.isdigit() is False:
        print("\n Input should be numeric! \n")
        continue
    elif int(inp) != 1 and int(inp) != 2 and int(inp) != 3:
        print("\n Wrong option number entered. Enter 1, 2 or 3. \n")
        continue
    else:
        inp = int(inp)

        if inp == 3:
            print("Goodbye!")
            break
        elif inp == 1:
            option_one()
            print("Data Scraped and DB Created.")
        elif inp == 2:
            if db.isEmpty() is True:
                print("\nMissing some data. Select option 1 and try again.\n")
                continue
            else:
                while True:
                    print("Enter a year range in a 4 digit format:")
                    y1 = input(" From:")
                    y2 = input(" To:")
                    if y1.isdigit() is False or y2.isdigit() is False:
                        print("Warning: Enter years as numbers.")
                        continue
                    elif db.checkYear(y1) is False or db.checkYear(y2) is False:
                        print("Warning: Years out of range.")
                        continue
                    elif int(y1) == int(y2):
                        print("Warning: Enter two different years.")
                        continue
                    else:
                        option_two(int(y1), int(y2))
                    break
            continue
