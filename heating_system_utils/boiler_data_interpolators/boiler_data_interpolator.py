
import pandas as pd


class BoilerDataInterpolator:
    def interpolate_data(self,
                         boiler_df: pd.DataFrame,
                         start_datetime=None,
                         end_datetime=None,
                         inplace=False) -> pd.DataFrame:
        raise NotImplementedError
