
import pandas as pd


class HomeDataInterpolator:
    def interpolate_data(self,
                         df: pd.DataFrame,
                         start_datetime=None,
                         end_datetime=None,
                         inplace=False) -> pd.DataFrame:
        raise NotImplementedError
