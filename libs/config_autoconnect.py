import datetime
import random

from libs.GXDLMSAutoConnect import GXDLMSAutoConnect
import pandas as pd

from libs.GXDateTime import GXDateTime
from libs.connect import open_connection

set_autoconnect_value = {
    "mode": 104,
    "repetitions": random.randint(1, 20),
    "repetitionDelay": random.randint(240, 3600),
    "callingWindow": (GXDateTime(f"*.*.* 11:{random.randint(0, 30)}:55", '%m.%d.%y %H:%M:%S'),
                      GXDateTime(f"*.*.* 18:{random.randint(40, 59)}:56", '%m.%d.%y %H:%M:%S')),
    "destinations": [f"0.0.0.0:{random.randint(1, 9999)}", f"255.255.255.255:{random.randint(1, 9999)}",
                     f"255.255.255.255:{random.randint(1, 9999)}", f"127.0.0.1:{random.randint(1, 9999)}"]
}

def read_calling_window(reader, index):
    result = "None"
    try:
        result = reader.read(GXDLMSAutoConnect(), 5)[0][index]
        return result
    except:
        return result

def read_autoconnect():
    # Открываем соединение
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Формируем ключ с названием и значением
        key = "autoconnect"
        key_with_value = key + " >> " + GXDLMSAutoConnect().getValues()[0]
        try:
            values = [
                reader.read(GXDLMSAutoConnect(), 2),
                reader.read(GXDLMSAutoConnect(), 3),
                reader.read(GXDLMSAutoConnect(), 4),
                read_calling_window(reader, 0),
                read_calling_window(reader, 1),
                reader.read(GXDLMSAutoConnect(), 6)
            ]

            result[key_with_value] = values
        except Exception as e:
            print(f"Ошибка при чтении данных: {e}")
            result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры автоконнектов")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['mode', 'repetitions', 'repetitionDelay',
                                                                     "callingWindow:start", "callingWindow:end",
                                                                     'destinations'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_autoconnect():
    reader = open_connection()
    try:
        data = GXDLMSAutoConnect()

        data.mode = set_autoconnect_value['mode']
        data.repetitions = set_autoconnect_value['repetitions']
        data.repetitionDelay = set_autoconnect_value['repetitionDelay']
        data.callingWindow = [set_autoconnect_value['callingWindow']]
        data.destinations = set_autoconnect_value['destinations']
        i = 2
        for key, value in set_autoconnect_value.items():
            try:
                reader.write(data, i)

                print(f"Успешно записан параметр: autoconnect >> {key}")
            except Exception as e:
                print(f"Ошибка при записи параметра {key} со значением {value}: {e}")
            i += 1

        reader.close()

        df = read_autoconnect()
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации автоконнекта: {e}")
        reader.close()
