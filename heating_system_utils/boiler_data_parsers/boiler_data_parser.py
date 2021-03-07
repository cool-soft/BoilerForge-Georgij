from typing import Union, IO

import pandas as pd


class BoilerDataParser:

    def parse(self, boiler_data: Union[str, IO]) -> pd.DataFrame:
        raise NotImplementedError
