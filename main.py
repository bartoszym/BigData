import matplotlib.pyplot as plt
import pandas as pd
import wordcloud

from mongo_connection import MongoDBClient
from scraping import OLXScraper


def scrap_olx():
    olx_scrapper = OLXScraper(
        "https://www.olx.pl/motoryzacja/samochody/q-octavia-II/?page=1", 20
    )
    offers_dict = olx_scrapper.get_offers_list()
    print(offers_dict)
    mongo_client = MongoDBClient("BigData")
    mongo_client.insert_list_to_mongo("cars", offers_dict)


def get_from_db():
    mongo_client = MongoDBClient("BigData")
    return mongo_client.get_objects_from_collection("cars")


def create_price_per_year(cars_df):
    calculated = cars_df.groupby(["production_year"])["price [zł]"].mean()
    plt.figure()
    calculated.plot(x="production year", y="price")
    plt.ticklabel_format(axis="y", style="plain")
    plt.title("Mean price according to year")
    plt.show()


def create_mileage_per_year(cars_df):
    calculated = cars_df.groupby(["production_year"])["mileage [km]"].mean()
    plt.figure()
    calculated.plot(x="production year", y="price")
    plt.ticklabel_format(axis="y", style="plain")
    plt.title("Mean mileage according to year")
    plt.show()


def create_wordcloud(cars_df):
    counted = cars_df.groupby(["location"])["location"].count()
    counted_dict = counted.to_dict()
    print(counted_dict)
    word_cloud = wordcloud.WordCloud(width=800, height=800).generate_from_frequencies(
        counted_dict
    )
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


def main():
    # scrap_olx()
    cars = get_from_db()
    cars_df = pd.DataFrame(cars)
    cars_df["production_year"] = pd.to_numeric(cars_df["production_year"])
    cars_df["mileage [km]"] = pd.to_numeric(cars_df["mileage [km]"])
    cars_df["price [zł]"] = pd.to_numeric(cars_df["price [zł]"])
    # create_price_per_year(cars_df)
    # create_mileage_per_year(cars_df)
    create_wordcloud(cars_df)


if __name__ == "__main__":
    main()
