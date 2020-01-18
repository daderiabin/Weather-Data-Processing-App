"""Weather Data Scraper For The Project by Danylo Deriabin."""

from html.parser import HTMLParser


class WeatherScraper(HTMLParser):
    """Scrape a web page."""

    YR = 0
    MON = 0
    isSelected = False
    isNumber = False
    toSkip = False
    inRow = False
    isTarget = False
    isHeader = False
    td_counter = 0
    th_counter = 0
    date = ''
    min = ''
    max = ''
    mean = ''
    weather = {}
    daily_temp = {}
    dates = []
    daily_temps = []

    def handle_starttag(self, tag, attrs):
        """Find a start tag."""
        if tag == 'option':
            for attr in attrs:
                if 'selected' in attr:
                    self.isSelected = True

        if tag == 'tr':
            self.inRow = True
            self.toSkip = False
        elif self.inRow is True:
            if tag == 'th':
                if self.th_counter > 1:
                    self.th_counter = 0
                    self.inRow = False
                else:
                    self.th_counter = self.th_counter + 1
                    self.isHeader = True
            if tag == 'td':
                if self.td_counter == 3:
                    self.td_counter = 0
                    self.inRow = False
                else:
                    self.td_counter = self.td_counter + 1
                    self.isTarget = True

    def handle_endtag(self, tag):
        """Find an end tag."""
        if tag == 'option':
            self.isSelected = False

        if tag == 'tr':
            self.inRow = False
            self.th_counter = 0
        elif self.inRow is True:
            if tag == 'th':
                self.isHeader = False
            if tag == 'td':
                self.isTarget = False

    def handle_data(self, data):
        """Find data within tags."""
        if self.isSelected is True:
            if data.isdecimal():
                self.YR = int(data)
            else:
                self.MON = int(getMonth(data))

        if self.isHeader is True:
            if 'Sum' in str(data) or 'Avg' in str(data) or 'Xtrm' in str(data):
                self.toSkip = True
            if data.isdecimal():
                self.date = str(self.YR) + '-' + str(self.MON) + '-' + str(data)
                self.dates.append(self.date)
        elif self.isTarget is True:
            if isNumber(data) is True:
                if self.toSkip is False:
                    if 'LegendM' in data or '\xa0' in data:
                        data = 0

                    if self.max == '' or self.min == '' or self.mean == '':
                        if self.td_counter == 1:
                            self.max = data
                        elif self.td_counter == 2:
                            self.min = data
                        elif self.td_counter == 3:
                            self.mean = data

                    if self.max != '' and self.min != '' and self.mean != '':
                        self.daily_temp = {'Max': self.max,
                                           'Min': self.min,
                                           'Mean': self.mean}
                        if self.daily_temp not in self.daily_temps:
                            self.daily_temps.append(self.daily_temp)

                        self.max = ''
                        self.min = ''
                        self.mean = ''
                        self.date = ''

        self.weather = dict(zip(self.dates, self.daily_temps))


def isNumber(data):
    """Check if data is numeric."""
    try:
        if 'LegendM' in data or '\xa0' in data:
            return True
        else:
            float(data)
            return True
    except ValueError:
        return False


def getMonth(data):
    """Get a month number."""
    months = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5,
              'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
              'November': 11, 'December': 12}
    return months[data]


if __name__ == '__main__':
    scr = WeatherScraper()
