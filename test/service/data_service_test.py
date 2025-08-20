from repository.data_repository import DataRepository
from service.data_service import DataService


def test_years_list():
    repository = DataRepository()
    service_instance = DataService(repository)
    data = service_instance.detail_level_data(2019, "United States")
    print(data)
