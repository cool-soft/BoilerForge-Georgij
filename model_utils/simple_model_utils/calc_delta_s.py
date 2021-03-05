
from datetime import datetime
from config import (
    PREDICTED_BOILER_TEMP_PATH,
    BOILER_PREPROCESSED_DATASET_PATH
)
from scipy.integrate import trapz
from heating_system.dataset_utils.dataset_io import load_dataset

if __name__ == '__main__':
    min_date = datetime(2019, 2, 5)
    max_date = datetime(2019, 4, 30)

    predicted_boiler_t = load_dataset(PREDICTED_BOILER_TEMP_PATH, min_date, max_date)
    real_boiler_t = load_dataset(BOILER_PREPROCESSED_DATASET_PATH, min_date, max_date)

    predicted_s = trapz(predicted_boiler_t["t1"].to_numpy())
    real_s = trapz(real_boiler_t["t1"].to_numpy())

    print(predicted_s, real_s, predicted_s/real_s)
