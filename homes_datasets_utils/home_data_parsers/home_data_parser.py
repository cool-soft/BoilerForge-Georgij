from typing import Union, IO

import pandas as pd


class HomeDataParser:

    def parse_home_data(self, home_data: Union[str, IO]) -> pd.DataFrame:
        raise NotImplementedError
