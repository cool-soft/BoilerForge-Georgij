from typing import Union, IO

import pandas as pd


class BoilerDataParser:

    def parse_boiler_data(self, boiler_data: Union[str, IO]) -> pd.DataFrame:
        raise NotImplementedError
