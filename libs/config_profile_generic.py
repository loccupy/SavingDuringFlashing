from gurux_dlms.objects import GXDLMSProfileGeneric, GXDLMSData, GXDLMSCaptureObject
import pandas as pd

from libs.connect import open_connection

PROFILES = {
    'display': GXDLMSProfileGeneric("0.0.21.0.1.255"),
    'load_profile_1': GXDLMSProfileGeneric("1.0.99.1.0.255"),
    'load_profile_2': GXDLMSProfileGeneric("1.0.99.2.0.255"),
}

set_profile_generic_value = {
    'display': {
        'captureObjects': [(GXDLMSData("0.0.0.9.1.255"), GXDLMSCaptureObject(2, 0)),
                           (GXDLMSData("0.0.0.9.2.255"), GXDLMSCaptureObject(2, 0)),
                           (GXDLMSData("0.0.96.1.0.255"), GXDLMSCaptureObject(2, 0))],
        'capturePeriod': 7
    },
    'load_profile_1': {
        'captureObjects': None,
        'capturePeriod': 900
    },
    'load_profile_2': {
        'captureObjects': None,
        'capturePeriod': 1800
    }
}


def read_profile_generic():
    # Открываем соединение
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Читаем данные для конкретного пуша
        for key, value in PROFILES.items():

            # Формируем ключ с названием и значением
            key_with_value = key + " >> " + value.getValues()[0]

            # Читаем несколько параметров
            try:
                # Создаем список значений
                values = [
                    reader.read(value, 4),
                    [i[0].logicalName for i in reader.read(value, 3)]
                ]
                # Сохраняем значения
                result[key_with_value] = values
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры Profile Generic")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['capturePeriod', 'captureObjects'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_profile_generic():
    reader = open_connection()
    try:
        for key, data in PROFILES.items():

            data.captureObjects = set_profile_generic_value[key]['captureObjects']
            data.capturePeriod = set_profile_generic_value[key]['capturePeriod']

            for i in [3, 4]:
                if key in ['load_profile_1', 'load_profile_2'] and i == 3:
                    continue
                try:
                    reader.write(data, i)
                    print(f"Успешно записан параметр: {key} под индексом {i}")
                except Exception as e:
                    print(f"Ошибка при записи параметра {key} под индексом {i}: {e}")

        reader.close()

        df = read_profile_generic()
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации профилей: {e}")
        reader.close()
