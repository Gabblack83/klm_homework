import pandas as pd
import pytest

from exceptions.user_defined_exceptions import DataException
from repository.data_repository import DataRepository


@pytest.fixture
def instance():
    return DataRepository()


def test_get_years_list_happy_path(instance):
    # Act
    years_list = instance.get_years_list()

    # Assert
    assert years_list is not None
    assert isinstance(years_list, pd.DataFrame)
    assert 0 not in years_list.shape


def test_get_years_list_throws_error(instance):
    # Arrange
    instance.aviation_data = None  # to provoke a NullPointerException / ValueError

    # Act / Assert
    with pytest.raises(DataException):
        instance.get_years_list()


def test_get_continent_level_aggregated_data_happy_path(instance):
    # Arrange
    valid_year = 2019

    # Act
    data = instance.get_continent_level_aggregated_data(valid_year)

    # Assert
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert 0 not in data.shape


def test_get_continent_level_aggregated_data_returns_empty_dataframe(instance):
    # Arrange
    invalid_year = 2222

    # Act
    data = instance.get_continent_level_aggregated_data(invalid_year)

    # Assert
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert 0 in data.shape


def test_get_continent_level_aggregated_data_throws_error(instance):
    # Arrange
    instance.aviation_data = None  # to provoke a NullPointerException / ValueError
    valid_year = 2019

    # Act / Assert
    with pytest.raises(DataException):
        instance.get_continent_level_aggregated_data(valid_year)


def test_get_country_level_aggregated_data_happy_path(instance):
    # Arrange
    valid_year = 2019
    valid_continent = "Africa"

    # Act
    data = instance.get_country_level_aggregated_data(valid_year, valid_continent)

    # Assert
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert 0 not in data.shape


def test_get_country_level_aggregated_data_returns_empty_dataframe(instance):
    # Arrange
    valid_year = 2019
    invalid_year = 2222
    valid_continent = "Africa"
    invalid_continent = "Afrika"

    # Act
    data_with_wrong_continent = instance.get_country_level_aggregated_data(valid_year, invalid_continent)
    data_with_wrong_year = instance.get_country_level_aggregated_data(invalid_year, valid_continent)

    # Assert
    assert data_with_wrong_continent is not None and data_with_wrong_year is not None
    assert isinstance(data_with_wrong_continent, pd.DataFrame) and isinstance(data_with_wrong_year, pd.DataFrame)
    assert 0 in data_with_wrong_continent.shape and 0 in data_with_wrong_year.shape


def test_get_country_level_aggregated_data_throws_error(instance):
    # Arrange
    instance.aviation_data = None  # to provoke a NullPointerException / ValueError

    valid_year = 2019
    valid_continent = "Africa"

    # Act / Assert
    with pytest.raises(DataException):
        instance.get_country_level_aggregated_data(valid_year, valid_continent)


def test_get_detail_level_data_happy_path(instance):
    # Arrange
    valid_year = 2019
    valid_country = "United States"

    # Act
    data = instance.get_detail_level_data(valid_year, valid_country)

    # Assert
    assert data is not None
    assert isinstance(data, pd.DataFrame)
    assert 0 not in data.shape


def test_get_detail_level_data_returns_empty_dataframe(instance):
    # Arrange
    valid_year = 2019
    invalid_year = 2222
    valid_country = "United States"
    invalid_country = "NoMensLand"

    # Act
    data_with_wrong_country = instance.get_detail_level_data(valid_year, invalid_country)
    data_with_wrong_year = instance.get_detail_level_data(invalid_year, valid_country)

    # Assert
    assert data_with_wrong_country is not None and data_with_wrong_year is not None
    assert isinstance(data_with_wrong_country, pd.DataFrame) and isinstance(data_with_wrong_year, pd.DataFrame)
    assert 0 in data_with_wrong_country.shape and 0 in data_with_wrong_year.shape


def test_get_detail_level_data_throws_error(instance):
    # Arrange
    instance.aviation_data = None  # to provoke a NullPointerException / ValueError

    valid_year = 2019
    valid_country = "United States"

    # Act / Assert
    with pytest.raises(DataException):
        instance.get_detail_level_data(valid_year, valid_country)


