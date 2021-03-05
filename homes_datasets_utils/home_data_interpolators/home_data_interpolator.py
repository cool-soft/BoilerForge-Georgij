
import pandas as pd


class HomeDataInterpolator:
    def interpolate_boiler_data(self,
                                home_df: pd.DataFrame,
                                start_datetime=None,
                                end_datetime=None,
                                inplace=False) -> pd.DataFrame:
        raise NotImplementedError
