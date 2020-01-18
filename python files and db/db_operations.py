"""Database For The Project by Danylo Deriabin."""
import sqlite3


class DBOperations():
    """DB Operations Class."""

    def creator(self):
        """Initialize DB and create the table."""
        conn = sqlite3.connect("weather.sqlite")
        cur = conn.cursor()
        sql = """create table if not exists samples
                    (id integer primary key autoincrement not null,
                     sample_date text not null,
                     location text not null,
                     max_temp real not null,
                     min_temp real not null,
                     avg_temp real not null);"""
        cur.execute(sql)
        cur.close()
        conn.close()

    def isEmpty(self):
        """Check if table is empty."""
        conn = sqlite3.connect("weather.sqlite")
        cur = conn.cursor()
        try:
            cur.execute("SELECT count(*) FROM samples;")
            if cur.fetchall() == []:
                return True
            else:
                return False
        except:
            return True

        cur.close()
        conn.close()

    def checkYear(self, year):
        """Check if year exists in the DB."""
        y = str(year) + '-%%-%%'
        yr = (y,)
        conn = sqlite3.connect("weather.sqlite")
        cur = conn.cursor()
        sql = 'select avg_temp from samples where sample_date like ?'
        cur.execute(sql, yr)
        if cur.fetchall() == []:
            return False
        else:
            return True
        cur.close()
        conn.close()

    def inserter(self, dict):
        """Insert data to the DB."""
        conn = sqlite3.connect("weather.sqlite")
        cur = conn.cursor()
        q1 = 'delete from samples'
        cur.execute(q1)
        sql = """insert into samples
                    (sample_date, location, max_temp, min_temp, avg_temp)
                    values (?, ?, ?, ?, ?);"""

        for key, value in dict.items():
            location = 'Winnipeg, MB'
            data = (key, location)

            for k, v in value.items():
                data = data + (v,)

            cur.execute(sql, data)
            conn.commit()

        cur.close()
        conn.close()

    def reader(self, year, month):
        """Read rows from the DB."""
        d = str(year) + '-' + str(month) + '-%%'
        date = (d,)
        temp = []
        conn = sqlite3.connect("weather.sqlite")
        cur = conn.cursor()
        sql = 'select avg_temp from samples where sample_date like ?'

        for row in cur.execute(sql, date):
            for v in row:
                temp.append(v)

        temps = {month: temp}
        return temps

        cur.close()
        conn.close()


if __name__ == '__main__':
    db = DBOperations()
    db.creator()
