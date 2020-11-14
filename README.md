# NewspaperScraper

#### Scraper.py
Contains scripts to scrape National Newspaper

  1. The Hindu
  2. The Pioneer
  3. The Times of India
  4. The News Minute
  5. The Indian Express
  6. The Economic Times

And Regional Newspaper

  1. The Incredible Orissa
  2. The Assam Tribune
  3. The Kasmir Observer
  4. The Deccan Herald
  5. The Deccan Chronicles

#### Download-Articles.py
Includes the script to download all the articles used by GDELT as the source to
perform event identificaiton for Karnataka (State of India) for year 2019

#### india_karnataka_with_districts_2019.csv
Data which contains all the events happened in Karnataka as of year 2019 recorded
by GDELT with geocodded to the corresponding districts

The Geocooding was done by using the India district level shape file which can be
accessed from [ArcGIS Hub](https://hub.arcgis.com/datasets/2b37b84e67374fb98577c20ef8be6c62_0).

QGIS was used to geocode the gdelt events to corresponding districts.
