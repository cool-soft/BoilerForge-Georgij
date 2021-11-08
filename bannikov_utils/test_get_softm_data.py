from bannikov_utils.data_services.get_softm_data import get_data_from_server


def main():
    # список котельных
    # method=ai_getBoilers
    params = {"method": "ai_getBoilers"}
    boilers = get_data_from_server(params=params)
    print(boilers)

    # данные по тепловычислителям
    # method=ai_getMeterData&argument={"meter_id":1,"start":"2021-10-14 00:00:00","end":"2021-10-15 00:00:00"}
    # https://chern.agt.town/json/?method=ai_getMeterData&argument=%7B%22meter_id%22:1,%22start%22:%222021-10-14%2000:00:00%22,%22end%22:%222021-10-15%2000:00:00%22%7D
    meter_id = 144
    start_date = "2021-10-14 00:00:00"
    end_date = "2021-10-18 00:00:00"
    arguments = '{"meter_id":' + str(meter_id) + ',"start":"' + start_date + '","end":"' + end_date + '"}'
    params = {"method": "ai_getMeterData",
              "argument": arguments}
    temperatures = get_data_from_server(params=params)
    print(temperatures)

    # список активных тепловычислителей
    # https://chern.agt.town/json/?method=ai_getMeters&argument={"boiler_id":1}
    boiler_id = 1
    arguments = '{"boiler_id":' + str(boiler_id) + '}'
    params = {"method": "ai_getMeters",
              "argument": arguments}
    meter_devices = get_data_from_server(params=params)
    print(meter_devices)
    print(len(meter_devices))


if __name__ == '__main__':
    main()
