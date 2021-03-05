import config
from heating_system.model_utils.model_metrics import relative_error

# noinspection PyShadowingNames
from heating_system.simple_model_utils.temp_correlation_table_generator import TempCorrelationTableGenerator

if __name__ == '__main__':
    model_name = "multi_lstm_2020-09-14-21.22.12"
    smooth_size = 2
    window_size = 5
    custom_models_objects = {
        "relative_error": relative_error,
    }
    temp_step = 0.1

    optimizer = TempCorrelationTableGenerator()
    optimizer.set_smooth_size(smooth_size)
    optimizer.set_window_size(window_size)
    optimizer.set_parent_model_name(model_name)
    optimizer.set_custom_models_objects(custom_models_objects)
    optimizer.set_temp_step(temp_step)

    optimizer.start_optimization()

    print(f"Saving temp correlation table to {config.TEMP_CORRELATION_TABLE_PATH}")
    temp_correlation_table = optimizer.get_temp_correlation_table()
    temp_correlation_table.to_pickle(config.TEMP_CORRELATION_TABLE_PATH)
