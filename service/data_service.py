from typing import Any

from common.logger import get_logger
from exceptions.user_defined_exceptions import DataException, ServiceException
from repository.base_data_repository import BaseDataRepository


class DataService:
    def __init__(self, data_repository: BaseDataRepository):
        self.data_repository = data_repository
        self.logger = get_logger()

    def years_list(self) -> dict[str, list[int]]:
        try:
            years_df = self.data_repository.get_years_list()
            return {"yearList": years_df["Year"].tolist()}
        except DataException as de:
            raise de
        except Exception:
            self.logger.exception("Problem turning years list data to dictionary")
            raise ServiceException()

    def continent_level_aggregation_data(self, year: int) -> list[dict[str, Any]]:
        try:
            continent_level_df = self.data_repository.get_continent_level_aggregated_data(year)
            renamed_continent_level_df = continent_level_df.rename(columns={
                "Continent_Name": "continentName",
                "Total.Fatal.Injuries": "totalFatalities",
                "Total.Serious.Injuries": "totalSeriousInjuries",
                "Total.Minor.Injuries": "totalMinorInjuries",
                "Total.Uninjured": "totalUninjured",
                "Total.Incident.Count": "totalIncidentCount"})
            return renamed_continent_level_df.to_dict(orient="records")
        except DataException as de:
            raise de
        except Exception:
            self.logger.exception("Problem turning continent level data to dictionary")
            raise ServiceException()

    def country_level_aggregation_data(self, year: int, continent: str) -> list[dict[str, Any]]:
        try:
            country_level_df = self.data_repository.get_country_level_aggregated_data(year, continent)
            renamed_country_level_df = country_level_df.rename(columns={
                "Country": "countryName",
                "Continent_Name": "continentName",
                "Total.Fatal.Injuries": "totalFatalities",
                "Total.Serious.Injuries": "totalSeriousInjuries",
                "Total.Minor.Injuries": "totalMinorInjuries",
                "Total.Uninjured": "totalUninjured",
                "Total.Incident.Count": "totalIncidentCount"})
            return renamed_country_level_df.to_dict(orient="records")
        except DataException as de:
            raise de
        except Exception:
            self.logger.exception("Problem turning country level data to dictionary")
            raise ServiceException()

    def detail_level_data(self, year: int, country: str) -> list[dict[str, Any]]:
        try:
            detail_level_df = self.data_repository.get_detail_level_data(year, country)
            detail_level_df["aircraftModel"] = detail_level_df["Make"] + " - " + detail_level_df["Model"]
            renamed_detail_level_df = detail_level_df.rename(columns={
                "Country": "countryName",
                "Longitude": "longitude",
                "Latitude": "latitude",
                "Event.Date": "date",
                "Location": "location",
                "Total.Fatal.Injuries": "totalFatalities",
                "Total.Serious.Injuries": "totalSeriousInjuries",
                "Total.Minor.Injuries": "totalMinorInjuries",
                "Total.Uninjured": "totalUninjured"})
            return renamed_detail_level_df.to_dict(orient="records")
        except DataException as de:
            raise de
        except Exception:
            self.logger.exception("Problem turning country level data to dictionary")
            raise ServiceException()
