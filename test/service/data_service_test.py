import types

import pandas as pd
import pytest

from exceptions.user_defined_exceptions import DataException, ServiceException
from repository.base_data_repository import BaseDataRepository
from service.data_service import DataService


class DataRepositoryMock(BaseDataRepository):
    def get_years_list(self):
        pass

    def get_continent_level_aggregated_data(self, year: int):
        pass

    def get_country_level_aggregated_data(self, year: int, continent: str):
        pass

    def get_detail_level_data(self, year: int, country: str):
        pass


@pytest.fixture
def instance():
    return DataService(DataRepositoryMock())


def test_years_list_happy_path(instance):
    # Arrange
    years_list_data_frame = pd.DataFrame({"Year": [2019, 2018, 2017]})
    instance.data_repository.get_years_list = \
        types.MethodType(lambda self: years_list_data_frame, instance.data_repository.get_years_list)

    # Act
    data = instance.years_list()

    # Assert
    assert data is not None
    assert isinstance(data, dict)
    assert isinstance(data.get("yearList"), list)
    assert len(data.get("yearList")) == 3


def test_years_list_throws_error(instance):
    # Arrange
    instance.data_repository.get_years_list = \
        types.MethodType(lambda self: DataException(), instance.data_repository.get_years_list)

    # Act / Assert
    with pytest.raises(ServiceException):
        instance.years_list()


def test_continent_level_aggregation_data_happy_path(instance):
    # Arrange
    valid_year = 2019
    data_frame = pd.DataFrame({"Continent_Name": ["Africa"], "Total.Fatal.Injuries": [1.0],
                               "Total.Serious.Injuries": [2.0], "Total.Minor.Injuries": [1.0],
                               "Total.Uninjured": [0], "Total.Incident.Count": [1.0]})
    instance.data_repository.get_continent_level_aggregated_data = \
        types.MethodType(lambda self, year: data_frame,
                         instance.data_repository.get_continent_level_aggregated_data)

    # Act
    data = instance.continent_level_aggregation_data(valid_year)

    # Assert
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 1
    for key in ["continentName", "totalFatalities", "totalSeriousInjuries",
                "totalMinorInjuries", "totalUninjured",  "totalIncidentCount"]:
        assert key in data[0].keys()


def test_continent_level_aggregation_data_throws_error(instance):
    # Arrange
    valid_year = 2019
    instance.data_repository.get_continent_level_aggregated_data = \
        types.MethodType(lambda self, year: DataException,
                         instance.data_repository.get_continent_level_aggregated_data)

    # Act / Assert
    with pytest.raises(ServiceException):
        instance.continent_level_aggregation_data(valid_year)


def test_country_level_aggregation_data_happy_path(instance):
    # Arrange
    valid_year = 2019
    valid_continent = "Africa"
    data_frame = pd.DataFrame({"Country": ["United States"], "Continent_Name": ["Africa"],
                               "Total.Fatal.Injuries": [1.0], "Total.Serious.Injuries": [2.0],
                               "Total.Minor.Injuries": [1.0], "Total.Uninjured": [0], "Total.Incident.Count": [1.0]})
    instance.data_repository.get_country_level_aggregated_data = \
        types.MethodType(lambda self, year, continent: data_frame,
                         instance.data_repository.get_country_level_aggregated_data)

    # Act
    data = instance.country_level_aggregation_data(valid_year, valid_continent)

    # Assert
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 1
    for key in ["countryName", "continentName", "totalFatalities", "totalSeriousInjuries",
                "totalMinorInjuries", "totalUninjured",  "totalIncidentCount"]:
        assert key in data[0].keys()


def test_country_level_aggregation_data_throws_error(instance):
    # Arrange
    valid_year = 2019
    valid_continent = "Africa"
    instance.data_repository.get_country_level_aggregated_data = \
        types.MethodType(lambda self, year, continent: DataException,
                         instance.data_repository.get_country_level_aggregated_data)

    # Act / Assert
    with pytest.raises(ServiceException):
        instance.country_level_aggregation_data(valid_year, valid_continent)


def test_detail_level_data_happy_path(instance):
    # Arrange
    valid_year = 2019
    valid_country = "United States"
    data_frame = pd.DataFrame({"Country": ["United States"], "Longitude": [12.2345], "Latitude": [-10.2223],
                               "Event.Date": ["2019.10.12"], "Location": ["Budapest"], "Make": ["Cessna"],
                               "Model": ["P 321"], "Total.Fatal.Injuries": [1.0], "Total.Serious.Injuries": [2.0],
                               "Total.Minor.Injuries": [1.0], "Total.Uninjured": [0], "Total.Incident.Count": [1.0]})
    instance.data_repository.get_detail_level_data = \
        types.MethodType(lambda self, year, country: data_frame,
                         instance.data_repository.get_detail_level_data)

    # Act
    data = instance.detail_level_data(valid_year, valid_country)

    # Assert
    assert data is not None
    assert isinstance(data, list)
    assert len(data) == 1
    for key in ["countryName", "longitude", "latitude", "date", "location", "aircraftModel",
                "totalFatalities", "totalSeriousInjuries", "totalMinorInjuries", "totalUninjured"]:
        assert key in data[0].keys()
    assert data[0].get("aircraftModel") == "Cessna - P 321"


def test_detail_level_data_throws_error(instance):
    # Arrange
    valid_year = 2019
    valid_country = "United States"
    instance.data_repository.get_detail_level_data = \
        types.MethodType(lambda self, year, continent: DataException,
                         instance.data_repository.get_detail_level_data)

    # Act / Assert
    with pytest.raises(ServiceException):
        instance.detail_level_data(valid_year, valid_country)

