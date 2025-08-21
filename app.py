import os

from dotenv import load_dotenv
from flask import Flask, send_file, request

from build_vue.build import build_vue
from common.api_helpers import ApiResponse, send_response, error_handler
from common.conventions import VUE_STATIC_FOLDER
from repository.base_data_repository import BaseDataRepository
from repository.data_repository import DataRepository
from service.data_service import DataService

app = Flask(__name__)

load_dotenv()
LOCAL_DEV_ENV: bool = os.getenv("LOCAL_DEV_ENV") == "True"
data_repository: BaseDataRepository = DataRepository()
data_service = DataService(data_repository)


@app.route("/", defaults={"folder": "", "file_name": "index.html"}, methods=["GET"])
@app.route("/<folder>/<file_name>", methods=["GET"])
def get_static_files(folder: str, file_name):
    if LOCAL_DEV_ENV and file_name == "index.html":
        build_vue()

    static_file = VUE_STATIC_FOLDER.joinpath(folder).joinpath(file_name)
    if os.path.exists(static_file) and os.path.isfile(static_file):
        return send_file(static_file)


@app.route("/api/get_year_list", methods=["GET"])
@error_handler
def get_year_list():
    return send_response(ApiResponse.OK, data_service.years_list())


@app.route("/api/get_continent_level_aggregation/", methods=["GET"])
@error_handler
def get_continent_level_aggregation():
    year_string: str = request.args.get("year", None)

    if year_string is None:
        return send_response(ApiResponse.BAD_REQUEST, "year parameter must no be missing")

    try:
        year = int(year_string)
    except ValueError:
        return send_response(ApiResponse.BAD_REQUEST, "year parameter should be a valid integer")

    return send_response(ApiResponse.OK, data_service.continent_level_aggregation_data(year=year))


@app.route("/api/get_country_level_aggregation/", methods=["GET"])
@error_handler
def get_country_level_aggregation():
    year_string: str = request.args.get("year", None)
    continent: str = request.args.get("continent", None)

    if year_string is None or continent is None:
        return send_response(ApiResponse.BAD_REQUEST, "a parameter is missing")

    try:
        year = int(year_string)
    except ValueError:
        return send_response(ApiResponse.BAD_REQUEST, "year parameter should be a valid integer")

    return send_response(ApiResponse.OK, data_service.country_level_aggregation_data(year=year, continent=continent))


@app.route("/api/get_detail_level/", methods=["GET"])
@error_handler
def get_detail_level():
    year_string: str = request.args.get("year", None)
    country: str = request.args.get("country", None)

    if year_string is None or country is None:
        return send_response(ApiResponse.BAD_REQUEST, "a parameter is missing")

    try:
        year = int(year_string)
    except ValueError:
        return send_response(ApiResponse.BAD_REQUEST, "year parameter should be a valid integer")

    return send_response(ApiResponse.OK, data_service.detail_level_data(year=year, country=country))


if __name__ == "__main__":
    if LOCAL_DEV_ENV:
        build_vue()
    app.run(host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", 8001)))
