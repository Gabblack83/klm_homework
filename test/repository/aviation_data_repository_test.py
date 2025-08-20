from repository.data_repository import DataRepository


def test_this():
    instance = DataRepository()
    print(instance.get_detail_level_data(2019, "United States"))
