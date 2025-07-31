from gurux_dlms.objects import GXDLMSDisconnectControl
import pandas as pd

from libs.connect import open_connection

DISCONNECT_MODE = {
    'mode': GXDLMSDisconnectControl("0.0.96.3.10.255")
}

set_disconnect_value = {
    'mode': 1
}


def read_disconnect():
    # Открываем соединение
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Формируем ключ с названием и значением
        key_with_value = "mode" + " >> " + DISCONNECT_MODE["mode"].getValues()[0]

        # Читаем несколько параметров
        try:
            value = reader.read(DISCONNECT_MODE["mode"], 4)
            # Сохраняем значения
            result[key_with_value] = value
        except Exception as e:
            print(f"Ошибка при чтении данных: {e}")
            result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры дисконнекта")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['mode'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_disconnect():
    reader = open_connection()
    try:
        data = DISCONNECT_MODE["mode"]
        try:
            data.controlMode = set_disconnect_value["mode"]
            reader.write(data, 4)
            print(f"Успешно записан параметр: DisconnectControl >> mode")
        except Exception as e:
            print(f"Ошибка при записи параметра DisconnectControl >> mode: {e}")

        reader.close()

        df = read_disconnect()
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации дисконнекта: {e}")
        reader.close()
