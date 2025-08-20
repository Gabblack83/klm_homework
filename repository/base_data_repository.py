from abc import ABC, abstractmethod

import pandas as pd


class BaseDataRepository(ABC):

    @abstractmethod
    def get_years_list(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_continent_level_aggregated_data(self, year: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_country_level_aggregated_data(self, year: int, continent: str) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_detail_level_data(self, year: int, country: str) -> pd.DataFrame:
        pass
