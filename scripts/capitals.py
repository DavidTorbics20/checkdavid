"""A single-use-script to get the capitals of every country around the world
and save it into a database. The website I will be using to get the cities is
https://www.worlddata.info/capital-cities.php"""

import sqlalchemy as sql
from bs4 import BeautifulSoup
import requests


class CityCollector:
    """This class collects all the capital cities around the world and saves
    them in to a database."""
    def __init__(self) -> None:
        self.engine = sql.create_engine("sqlite:///database/cities_around_" +
                                        "the_world", echo=True)
        metadata = sql.MetaData()
        self.emp = sql.Table('cities_and_countries.db', metadata,
                             sql.Column("Id", sql.Integer,
                                        sql.Sequence('seq_reg_id',
                                                     start=1,
                                                     increment=1),
                                        primary_key=True),
                             sql.Column('Country', sql.String(255),
                                        nullable=False),
                             sql.Column('City', sql.String(255),
                                        nullable=False))

        metadata.create_all(self.engine)
        self.get_capitals()

    def get_capitals(self):
        """Scrape the website and get every country and their
        capital cities."""
        url = "https://www.worlddata.info/capital-cities.php"
        page = requests.get(url)
        pagetext = page.text

        soup = BeautifulSoup(pagetext, 'html.parser')
        cityList = []
        countryList = []
        counter = 0

        for row in soup.find_all('tr'):
            for col in row.find_all('td'):
                if counter == 0:
                    countryList.append(col.text)
                elif counter == 1:
                    cityList.append(col.text)
                elif counter == 2:
                    counter = 0
                    break

                counter += 1

        self.save_capilats(cityList, countryList)

    def save_capilats(self, cityList, countryList):
        """Save the every city and countrly from the two lists into a table."""
        connection = self.engine.connect()
        counter = 0

        for country, city in zip(countryList, cityList):
            query = sql.insert(self.emp).values(Id=counter,
                                                Country=country,
                                                City=city)
            Result = connection.execute(query)  # noqa: F841
            counter += 1


if __name__ == "__main__":
    cc = CityCollector()
    cc.get_capitals()
