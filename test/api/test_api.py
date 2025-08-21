from unittest.mock import patch, MagicMock

import pytest
from flask.testing import FlaskClient

from app import app
from common.api_helpers import ApiResponse
from exceptions.user_defined_exceptions import ServiceException
from service.data_service import DataService

# Make sure that LOCAL_DEV_ENV parameter is not set to True!


@pytest.fixture
def client() -> FlaskClient:
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_static_files_happy_path(client):
    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == ApiResponse.OK.value


def test_get_static_files_missing_file(client):
    # Act
    response = client.get("/test")

    # Assert
    assert response.status_code == 404


@patch.object(DataService, "years_list", return_value={})
def test_get_year_list_happy_path(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_year_list")

    # Assert
    assert response.status_code == ApiResponse.OK.value
    assert response.json == {}
    assert service_mock.called


@patch.object(DataService, "years_list", side_effect=[ServiceException])
def test_get_year_list_throws_error(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_year_list")

    # Assert
    assert response.status_code == ApiResponse.SERVER_ERROR.value
    assert response.json is None
    assert service_mock.called


@patch.object(DataService, "continent_level_aggregation_data", return_value=[])
def test_get_continent_level_aggregation_happy_path(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_continent_level_aggregation/?year=2019")

    # Assert
    assert response.status_code == ApiResponse.OK.value
    assert response.json == []
    assert service_mock.called


@patch.object(DataService, "continent_level_aggregation_data", return_value=[])
def test_get_continent_level_aggregation_validation_error_missing_year(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_continent_level_aggregation/")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "continent_level_aggregation_data", return_value=[])
def test_get_continent_level_aggregation_validation_error_malformed_year(service_mock: MagicMock, client):
    # Arrange
    malformed_year = "twenty nineteen"

    # Act
    response = client.get(f"/api/get_continent_level_aggregation/?year={malformed_year}")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "continent_level_aggregation_data", side_effect=[ServiceException])
def test_get_continent_level_aggregation_throws_error(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_continent_level_aggregation/?year=2019")

    # Assert
    assert response.status_code == ApiResponse.SERVER_ERROR.value
    assert response.json is None
    assert service_mock.called


@patch.object(DataService, "country_level_aggregation_data", return_value=[])
def test_get_country_level_aggregation_happy_path(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_country_level_aggregation/?year=2019&continent=Africa")

    # Assert
    assert response.status_code == ApiResponse.OK.value
    assert response.json == []
    assert service_mock.called


@patch.object(DataService, "country_level_aggregation_data", return_value=[])
def test_get_country_level_aggregation_validation_error_missing_params(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_country_level_aggregation/")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "country_level_aggregation_data", return_value=[])
def test_get_country_level_aggregation_validation_error_malformed_year(service_mock: MagicMock, client):
    # Arrange
    malformed_year = "twenty nineteen"

    # Act
    response = client.get(f"/api/get_country_level_aggregation/?year={malformed_year}&continent=Africa")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "country_level_aggregation_data", side_effect=[ServiceException])
def test_get_country_level_aggregation_throws_error(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_country_level_aggregation/?year=2019&continent=Africa")

    # Assert
    assert response.status_code == ApiResponse.SERVER_ERROR.value
    assert response.json is None
    assert service_mock.called


@patch.object(DataService, "detail_level_data", return_value=[])
def test_get_detail_level_happy_path(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_detail_level/?year=2019&country=Africa")

    # Assert
    assert response.status_code == ApiResponse.OK.value
    assert response.json == []
    assert service_mock.called


@patch.object(DataService, "detail_level_data", return_value=[])
def test_get_detail_level_validation_error_missing_params(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_detail_level/")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "detail_level_data", return_value=[])
def test_get_detail_level_validation_error_malformed_year(service_mock: MagicMock, client):
    # Arrange
    malformed_year = "twenty nineteen"

    # Act
    response = client.get(f"/api/get_detail_level/?year={malformed_year}&country=Africa")

    # Assert
    assert response.status_code == ApiResponse.BAD_REQUEST.value
    assert response.json is None
    assert not service_mock.called


@patch.object(DataService, "detail_level_data", side_effect=[ServiceException])
def test_get_detail_level_throws_error(service_mock: MagicMock, client):
    # Act
    response = client.get("/api/get_detail_level/?year=2019&country=Africa")

    # Assert
    assert response.status_code == ApiResponse.SERVER_ERROR.value
    assert response.json is None
    assert service_mock.called
