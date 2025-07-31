from gurux_dlms.objects import GXDLMSLimiter
import pandas as pd

from libs.connect import open_connection

LIMITERS = {
    'limiter_1': GXDLMSLimiter("0.0.17.0.0.255"),
    'limiter_2': GXDLMSLimiter("0.0.17.0.1.255"),
    'limiter_3': GXDLMSLimiter("0.0.17.0.2.255"),
    'limiter_4': GXDLMSLimiter("0.0.17.0.3.255"),
    'limiter_5': GXDLMSLimiter("0.0.17.0.4.255"),
    'limiter_6': GXDLMSLimiter("0.0.17.0.5.255")
}

set_limiters_value = {
    'limiter_1': {
        'thresholdActive': 259999,
        'minOverThresholdDuration': 77,
        'minUnderThresholdDuration': 78
    },
    'limiter_2': {
        'thresholdActive': 599,
        'minOverThresholdDuration': 123
    },
    'limiter_3': {
        'thresholdActive': 288888,
        'minOverThresholdDuration': 77,
        'minUnderThresholdDuration': 78
    },
    'limiter_4': {
        'thresholdActive': 1,
        'minOverThresholdDuration': 77,
        'minUnderThresholdDuration': 78
    },
    'limiter_5': {
        'thresholdActive': 49,
        'minOverThresholdDuration': 77
    },
    'limiter_6': {
        'thresholdActive': 99,
        'minOverThresholdDuration': 177,
        'minUnderThresholdDuration': 178
    }
}


def read_limiter():
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Читаем данные для конкретного лимитёра
        for key, value in LIMITERS.items():
            # Формируем ключ с названием и значением
            key_with_value = key + " >> " + value.getValues()[0]
            device_type = reader.deviceType

            # Читаем несколько параметров
            try:
                # Создаем список значений
                if key in ["limiter_1", "limiter_3", "limiter_4", "limiter_6"]:
                    values = [
                        reader.read(value, 3),
                        reader.read(value, 6),
                        reader.read(value, 7)
                    ]
                elif key == "limiter_2" or (key == "limiter_5" and device_type == "1PH"):
                    values = [
                        reader.read(value, 3),
                        reader.read(value, 6),
                        "None"
                    ]
                else:
                    continue

                # Сохраняем значения
                result[key_with_value] = values
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры лимитеров")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['thresholdActive', 'minOverThresholdDuration',
                                                                     'minUnderThresholdDuration'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


# not for TT
def config_limiters():
    reader = open_connection()
    try:
        device_type = reader.deviceType
        for key, data in LIMITERS.items():
            try:
                if key in ["limiter_1", "limiter_3", "limiter_4", "limiter_6"]:
                    for i in [3, 6, 7]:
                        data_type = reader.readType(data, i)
                        if i == 3:
                            data.thresholdActive = set_limiters_value[key]['thresholdActive']
                        elif i == 6:
                            data.minOverThresholdDuration = set_limiters_value[key]['minOverThresholdDuration']
                        else:
                            data.minUnderThresholdDuration = set_limiters_value[key]['minUnderThresholdDuration']
                        data.setDataType(i, data_type)
                        reader.write(data, i)
                elif key == "limiter_2" or (key == "limiter_5" and device_type == "1PH"):
                    for i in [3, 6]:
                        data_type = reader.readType(data, i)
                        if i == 3:
                            data.thresholdActive = set_limiters_value[key]['thresholdActive']
                        elif i == 6:
                            data.minOverThresholdDuration = set_limiters_value[key]['minOverThresholdDuration']
                        data.setDataType(i, data_type)
                        reader.write(data, i)
                else:
                    continue
                print(f"Успешно записан параметр: {key}")
            except Exception as e:
                print(f"Ошибка при записи параметра {key}: {e}")

        reader.close()

        df = read_limiter()
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации лимитеров: {e}")
        reader.close()
