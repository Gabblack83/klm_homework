from functools import cache

import pandas as pd

from common.conventions import DATA_FOLDER
from common.logger import get_logger
from exceptions.user_defined_exceptions import DataException
from repository.base_data_repository import BaseDataRepository


class DataRepository(BaseDataRepository):
    def __init__(self):
        self.aviation_data: pd.DataFrame = self._load_aviation_data()
        self.country_data: pd.DataFrame = self._load_country_data()
        self.continent_data: pd.DataFrame = self._load_continent_data()
        self.logger = get_logger()

    def _load_aviation_data(self) -> pd.DataFrame:
        raw_dataframe = pd.read_csv(DATA_FOLDER.joinpath(
            "AviationData_SSC_case_Ranbir.csv"), sep=",", encoding="utf-8", encoding_errors="replace")
        raw_dataframe["Year"] = raw_dataframe["Event.Date"].str[:4]
        return raw_dataframe

    def _load_country_data(self):
        return pd.read_csv(DATA_FOLDER.joinpath(
            "country-centroids.csv"), sep=",", encoding="utf-8", encoding_errors="replace")

    def _load_continent_data(self):
        return pd.read_csv(DATA_FOLDER.joinpath(
            "country-and-continent-codes-list-csv.csv"), sep=",", encoding="utf-8", encoding_errors="replace")

    @cache
    def get_years_list(self) -> pd.DataFrame:

        try:
            return self.aviation_data[["Year"]].drop_duplicates() \
                .sort_values(by="Year", ascending=False) \
                .reset_index(drop=True)
        except Exception:
            self.logger.exception("Problem during unique year list gathering")
            raise DataException()

    def get_continent_level_aggregated_data(self, year: int) -> pd.DataFrame:

        try:
            filtered_aviation_data = self.aviation_data[self.aviation_data["Year"] == str(year)][[
                "Country", "Longitude", "Latitude", "Total.Fatal.Injuries", "Total.Serious.Injuries",
                "Total.Minor.Injuries", "Total.Uninjured"]]
            filtered_aviation_data = filtered_aviation_data.dropna(subset=["Longitude", "Latitude"])

            country_dataframe = self.country_data[["Country", "Two_Letter_Country_Code"]]

            continent_dataframe = self.continent_data[
                ["Continent_Name", "Two_Letter_Country_Code", "latitude", "longitude"]]

            aviation_country_joined = pd.merge(
                filtered_aviation_data, country_dataframe, on="Country", how="inner")

            aviation_continent_joined = pd.merge(
                aviation_country_joined, continent_dataframe, on="Two_Letter_Country_Code", how="inner")[
                ["Continent_Name", "latitude", "longitude", "Total.Fatal.Injuries", "Total.Serious.Injuries",
                 "Total.Minor.Injuries",
                 "Total.Uninjured"]]

            aggregated_aviation_data_on_continent_level = aviation_continent_joined.groupby(
                ["Continent_Name", "latitude", "longitude"]).agg({
                "Total.Fatal.Injuries": "sum",
                "Total.Serious.Injuries": "sum",
                "Total.Minor.Injuries": "sum",
                "Total.Uninjured": "sum",
                "Continent_Name": "count"
            }).rename(columns={"Continent_Name": "Total.Incident.Count"}).reset_index()

            return aggregated_aviation_data_on_continent_level

        except Exception:
            self.logger.exception("Problem loading continent level aggregated data")
            raise DataException()

    def get_country_level_aggregated_data(self, year: int, continent: str) -> pd.DataFrame:
        try:
            filtered_aviation_data = self.aviation_data[self.aviation_data["Year"] == str(year)][[
                "Country", "Longitude", "Latitude", "Total.Fatal.Injuries", "Total.Serious.Injuries",
                "Total.Minor.Injuries", "Total.Uninjured"]]
            filtered_aviation_data = filtered_aviation_data.dropna(subset=["Longitude", "Latitude"])

            country_dataframe = self.country_data[["Country", "Two_Letter_Country_Code", "latitude", "longitude"]]

            continent_dataframe = self.continent_data[
                ["Continent_Name", "Two_Letter_Country_Code"]][
                self.continent_data["Continent_Name"] == continent]

            aviation_country_joined = pd.merge(
                filtered_aviation_data, country_dataframe, on="Country", how="inner")

            aviation_continent_joined = pd.merge(
                aviation_country_joined, continent_dataframe, on="Two_Letter_Country_Code", how="inner")[
                ["Continent_Name", "Country", "latitude", "longitude", "Total.Fatal.Injuries", "Total.Serious.Injuries",
                 "Total.Minor.Injuries",
                 "Total.Uninjured"]]

            aggregated_aviation_data_on_country_level = aviation_continent_joined.groupby(
                ["Continent_Name", "Country", "latitude", "longitude"]).agg({
                "Total.Fatal.Injuries": "sum",
                "Total.Serious.Injuries": "sum",
                "Total.Minor.Injuries": "sum",
                "Total.Uninjured": "sum",
                "Country": "count"
            }).rename(columns={"Country": "Total.Incident.Count"}).reset_index()

            return aggregated_aviation_data_on_country_level

        except Exception:
            self.logger.exception("Problem loading country level aggregated data")
            raise DataException()

    def get_detail_level_data(self, year: int, country: str) -> pd.DataFrame:
        try:
            filtered_aviation_data = self.aviation_data[
                (self.aviation_data["Year"] == str(year))
                & (self.aviation_data["Country"] == str(country))
            ][["Country", "Longitude", "Latitude", "Event.Date", "Location", "Make", "Model", "Total.Fatal.Injuries",
               "Total.Serious.Injuries", "Total.Minor.Injuries", "Total.Uninjured"]]
            filtered_aviation_data = filtered_aviation_data.dropna(subset=["Longitude", "Latitude"])
            filtered_aviation_data["Location"] = filtered_aviation_data["Location"].fillna("")
            filtered_aviation_data["Event.Date"] = filtered_aviation_data["Event.Date"].fillna("")
            filtered_aviation_data["Total.Fatal.Injuries"] = filtered_aviation_data["Total.Fatal.Injuries"].fillna(0)
            filtered_aviation_data["Total.Serious.Injuries"] = \
                filtered_aviation_data["Total.Serious.Injuries"].fillna(0)
            filtered_aviation_data["Total.Minor.Injuries"] = filtered_aviation_data["Total.Minor.Injuries"].fillna(0)
            filtered_aviation_data["Total.Uninjured"] = filtered_aviation_data["Total.Uninjured"].fillna(0)

            return filtered_aviation_data

        except Exception:
            self.logger.exception("Problem loading detail level data")
            raise DataException()
