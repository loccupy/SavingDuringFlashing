from gurux_dlms.enums import DataType
from gurux_dlms.objects import GXDLMSRegister
import pandas as pd

from libs.connect import open_connection

READ_REGISTERS_TT = {
    "1.0.1.29.0.255": GXDLMSRegister("1.0.1.29.0.255"),
    "1.0.2.29.0.255": GXDLMSRegister("1.0.2.29.0.255"),
    "1.0.3.29.0.255": GXDLMSRegister("1.0.3.29.0.255"),
    "1.0.4.29.0.255": GXDLMSRegister("1.0.4.29.0.255"),
    "1.0.1.30.0.255": GXDLMSRegister("1.0.1.30.0.255"),
    "1.0.2.30.0.255": GXDLMSRegister("1.0.2.30.0.255"),
    "1.0.3.30.0.255": GXDLMSRegister("1.0.3.30.0.255"),
    "1.0.4.30.0.255": GXDLMSRegister("1.0.4.30.0.255"),
    "1.0.1.8.0.255": GXDLMSRegister("1.0.1.8.0.255"),
    "1.0.21.8.0.255": GXDLMSRegister("1.0.21.8.0.255"),
    "1.0.41.8.0.255": GXDLMSRegister("1.0.41.8.0.255"),
    "1.0.61.8.0.255": GXDLMSRegister("1.0.61.8.0.255"),
    "1.0.1.8.1.255": GXDLMSRegister("1.0.1.8.1.255"),
    "1.0.1.8.2.255": GXDLMSRegister("1.0.1.8.2.255"),
    "1.0.1.8.3.255": GXDLMSRegister("1.0.1.8.3.255"),
    "1.0.1.8.4.255": GXDLMSRegister("1.0.1.8.4.255"),
    "1.0.2.8.0.255": GXDLMSRegister("1.0.2.8.0.255"),
    "1.0.22.8.0.255": GXDLMSRegister("1.0.22.8.0.255"),
    "1.0.42.8.0.255": GXDLMSRegister("1.0.42.8.0.255"),
    "1.0.62.8.0.255": GXDLMSRegister("1.0.62.8.0.255"),
    "1.0.2.8.1.255": GXDLMSRegister("1.0.2.8.1.255"),
    "1.0.2.8.2.255": GXDLMSRegister("1.0.2.8.2.255"),
    "1.0.2.8.3.255": GXDLMSRegister("1.0.2.8.3.255"),
    "1.0.2.8.4.255": GXDLMSRegister("1.0.2.8.4.255"),
    "1.0.3.8.0.255": GXDLMSRegister("1.0.3.8.0.255"),
    "1.0.23.8.0.255": GXDLMSRegister("1.0.23.8.0.255"),
    "1.0.43.8.0.255": GXDLMSRegister("1.0.43.8.0.255"),
    "1.0.63.8.0.255": GXDLMSRegister("1.0.63.8.0.255"),
    "1.0.3.8.1.255": GXDLMSRegister("1.0.3.8.1.255"),
    "1.0.3.8.2.255": GXDLMSRegister("1.0.3.8.2.255"),
    "1.0.3.8.3.255": GXDLMSRegister("1.0.3.8.3.255"),
    "1.0.3.8.4.255": GXDLMSRegister("1.0.3.8.4.255"),
    "1.0.4.8.0.255": GXDLMSRegister("1.0.4.8.0.255"),
    "1.0.24.8.0.255": GXDLMSRegister("1.0.24.8.0.255"),
    "1.0.44.8.0.255": GXDLMSRegister("1.0.44.8.0.255"),
    "1.0.64.8.0.255": GXDLMSRegister("1.0.64.8.0.255"),
    "1.0.4.8.1.255": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.2.255": GXDLMSRegister("1.0.4.8.2.255"),
    "1.0.4.8.3.255": GXDLMSRegister("1.0.4.8.3.255"),
    "1.0.4.8.4.255": GXDLMSRegister("1.0.4.8.4.255"),
    "1.0.1.8.0.101": GXDLMSRegister("1.0.1.8.0.101"),
    "1.0.1.8.1.101": GXDLMSRegister("1.0.1.8.1.101"),
    "1.0.1.8.2.101": GXDLMSRegister("1.0.1.8.2.101"),
    "1.0.1.8.3.101": GXDLMSRegister("1.0.1.8.3.101"),
    "1.0.1.8.4.101": GXDLMSRegister("1.0.1.8.4.101"),
    "1.0.2.8.0.101": GXDLMSRegister("1.0.2.8.0.101"),
    "1.0.2.8.1.101": GXDLMSRegister("1.0.2.8.1.101"),
    "1.0.2.8.2.101": GXDLMSRegister("1.0.2.8.2.101"),
    "1.0.2.8.3.101": GXDLMSRegister("1.0.2.8.3.101"),
    "1.0.2.8.4.101": GXDLMSRegister("1.0.2.8.4.101"),
    "1.0.3.8.0.101": GXDLMSRegister("1.0.3.8.0.101"),
    "1.0.3.8.1.101": GXDLMSRegister("1.0.3.8.1.101"),
    "1.0.3.8.2.101": GXDLMSRegister("1.0.3.8.2.101"),
    "1.0.3.8.3.101": GXDLMSRegister("1.0.3.8.3.101"),
    "1.0.3.8.4.101": GXDLMSRegister("1.0.3.8.4.101"),
    "1.0.4.8.0.101": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.1.101": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.2.101": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.3.101": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.4.101": GXDLMSRegister("1.0.4.8.1.255")
}

READ_REGISTERS_1PH = {
    "1.0.1.29.0.255": GXDLMSRegister("1.0.1.29.0.255"),
    "1.0.2.29.0.255": GXDLMSRegister("1.0.2.29.0.255"),
    "1.0.3.29.0.255": GXDLMSRegister("1.0.3.29.0.255"),
    "1.0.4.29.0.255": GXDLMSRegister("1.0.4.29.0.255"),
    "1.0.1.30.0.255": GXDLMSRegister("1.0.1.30.0.255"),
    "1.0.2.30.0.255": GXDLMSRegister("1.0.2.30.0.255"),
    "1.0.3.30.0.255": GXDLMSRegister("1.0.3.30.0.255"),
    "1.0.4.30.0.255": GXDLMSRegister("1.0.4.30.0.255"),
    "1.0.1.8.0.255": GXDLMSRegister("1.0.1.8.0.255"),
    "1.0.1.8.1.255": GXDLMSRegister("1.0.1.8.1.255"),
    "1.0.1.8.2.255": GXDLMSRegister("1.0.1.8.2.255"),
    "1.0.1.8.3.255": GXDLMSRegister("1.0.1.8.3.255"),
    "1.0.1.8.4.255": GXDLMSRegister("1.0.1.8.4.255"),
    "1.0.2.8.0.255": GXDLMSRegister("1.0.2.8.0.255"),
    "1.0.2.8.1.255": GXDLMSRegister("1.0.2.8.1.255"),
    "1.0.2.8.2.255": GXDLMSRegister("1.0.2.8.2.255"),
    "1.0.2.8.3.255": GXDLMSRegister("1.0.2.8.3.255"),
    "1.0.2.8.4.255": GXDLMSRegister("1.0.2.8.4.255"),
    "1.0.3.8.0.255": GXDLMSRegister("1.0.3.8.0.255"),
    "1.0.3.8.1.255": GXDLMSRegister("1.0.3.8.1.255"),
    "1.0.3.8.2.255": GXDLMSRegister("1.0.3.8.2.255"),
    "1.0.3.8.3.255": GXDLMSRegister("1.0.3.8.3.255"),
    "1.0.3.8.4.255": GXDLMSRegister("1.0.3.8.4.255"),
    "1.0.4.8.0.255": GXDLMSRegister("1.0.4.8.0.255"),
    "1.0.4.8.1.255": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.2.255": GXDLMSRegister("1.0.4.8.2.255"),
    "1.0.4.8.3.255": GXDLMSRegister("1.0.4.8.3.255"),
    "1.0.4.8.4.255": GXDLMSRegister("1.0.4.8.4.255"),
    "1.0.1.8.0.101": GXDLMSRegister("1.0.1.8.0.101"),
    "1.0.1.8.1.101": GXDLMSRegister("1.0.1.8.1.101"),
    "1.0.1.8.2.101": GXDLMSRegister("1.0.1.8.2.101"),
    "1.0.1.8.3.101": GXDLMSRegister("1.0.1.8.3.101"),
    "1.0.1.8.4.101": GXDLMSRegister("1.0.1.8.4.101"),
    "1.0.2.8.0.101": GXDLMSRegister("1.0.2.8.0.101"),
    "1.0.2.8.1.101": GXDLMSRegister("1.0.2.8.1.101"),
    "1.0.2.8.2.101": GXDLMSRegister("1.0.2.8.2.101"),
    "1.0.2.8.3.101": GXDLMSRegister("1.0.2.8.3.101"),
    "1.0.2.8.4.101": GXDLMSRegister("1.0.2.8.4.101"),
    "1.0.3.8.0.101": GXDLMSRegister("1.0.3.8.0.101"),
    "1.0.3.8.1.101": GXDLMSRegister("1.0.3.8.1.101"),
    "1.0.3.8.2.101": GXDLMSRegister("1.0.3.8.2.101"),
    "1.0.3.8.3.101": GXDLMSRegister("1.0.3.8.3.101"),
    "1.0.3.8.4.101": GXDLMSRegister("1.0.3.8.4.101"),
    "1.0.4.8.0.101": GXDLMSRegister("1.0.4.8.0.101"),
    "1.0.4.8.1.101": GXDLMSRegister("1.0.4.8.1.101"),
    "1.0.4.8.2.101": GXDLMSRegister("1.0.4.8.2.101"),
    "1.0.4.8.3.101": GXDLMSRegister("1.0.4.8.3.101"),
    "1.0.4.8.4.101": GXDLMSRegister("1.0.4.8.4.101")
}

READ_REGISTERS_3PH = {
    "1.0.1.29.0.255": GXDLMSRegister("1.0.1.29.0.255"),
    "1.0.2.29.0.255": GXDLMSRegister("1.0.2.29.0.255"),
    "1.0.3.29.0.255": GXDLMSRegister("1.0.3.29.0.255"),
    "1.0.4.29.0.255": GXDLMSRegister("1.0.4.29.0.255"),
    "1.0.1.30.0.255": GXDLMSRegister("1.0.1.30.0.255"),
    "1.0.2.30.0.255": GXDLMSRegister("1.0.2.30.0.255"),
    "1.0.3.30.0.255": GXDLMSRegister("1.0.3.30.0.255"),
    "1.0.4.30.0.255": GXDLMSRegister("1.0.4.30.0.255"),
    "1.0.1.8.0.255": GXDLMSRegister("1.0.1.8.0.255"),
    "1.0.21.8.0.255": GXDLMSRegister("1.0.21.8.0.255"),
    "1.0.41.8.0.255": GXDLMSRegister("1.0.41.8.0.255"),
    "1.0.61.8.0.255": GXDLMSRegister("1.0.61.8.0.255"),
    "1.0.1.8.1.255": GXDLMSRegister("1.0.1.8.1.255"),
    "1.0.1.8.2.255": GXDLMSRegister("1.0.1.8.2.255"),
    "1.0.1.8.3.255": GXDLMSRegister("1.0.1.8.3.255"),
    "1.0.1.8.4.255": GXDLMSRegister("1.0.1.8.4.255"),
    "1.0.2.8.0.255": GXDLMSRegister("1.0.2.8.0.255"),
    "1.0.22.8.0.255": GXDLMSRegister("1.0.22.8.0.255"),
    "1.0.42.8.0.255": GXDLMSRegister("1.0.42.8.0.255"),
    "1.0.62.8.0.255": GXDLMSRegister("1.0.62.8.0.255"),
    "1.0.2.8.1.255": GXDLMSRegister("1.0.2.8.1.255"),
    "1.0.2.8.2.255": GXDLMSRegister("1.0.2.8.2.255"),
    "1.0.2.8.3.255": GXDLMSRegister("1.0.2.8.3.255"),
    "1.0.2.8.4.255": GXDLMSRegister("1.0.2.8.4.255"),
    "1.0.3.8.0.255": GXDLMSRegister("1.0.3.8.0.255"),
    "1.0.23.8.0.255": GXDLMSRegister("1.0.23.8.0.255"),
    "1.0.43.8.0.255": GXDLMSRegister("1.0.43.8.0.255"),
    "1.0.63.8.0.255": GXDLMSRegister("1.0.63.8.0.255"),
    "1.0.3.8.1.255": GXDLMSRegister("1.0.3.8.1.255"),
    "1.0.3.8.2.255": GXDLMSRegister("1.0.3.8.2.255"),
    "1.0.3.8.3.255": GXDLMSRegister("1.0.3.8.3.255"),
    "1.0.3.8.4.255": GXDLMSRegister("1.0.3.8.4.255"),
    "1.0.4.8.0.255": GXDLMSRegister("1.0.4.8.0.255"),
    "1.0.24.8.0.255": GXDLMSRegister("1.0.24.8.0.255"),
    "1.0.44.8.0.255": GXDLMSRegister("1.0.44.8.0.255"),
    "1.0.64.8.0.255": GXDLMSRegister("1.0.64.8.0.255"),
    "1.0.4.8.1.255": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.2.255": GXDLMSRegister("1.0.4.8.2.255"),
    "1.0.4.8.3.255": GXDLMSRegister("1.0.4.8.3.255"),
    "1.0.4.8.4.255": GXDLMSRegister("1.0.4.8.4.255"),
    "1.0.1.8.0.101": GXDLMSRegister("1.0.1.8.0.101"),
    "1.0.1.8.1.101": GXDLMSRegister("1.0.1.8.1.101"),
    "1.0.1.8.2.101": GXDLMSRegister("1.0.1.8.2.101"),
    "1.0.1.8.3.101": GXDLMSRegister("1.0.1.8.3.101"),
    "1.0.1.8.4.101": GXDLMSRegister("1.0.1.8.4.101"),
    "1.0.2.8.0.101": GXDLMSRegister("1.0.2.8.0.101"),
    "1.0.2.8.1.101": GXDLMSRegister("1.0.2.8.1.101"),
    "1.0.2.8.2.101": GXDLMSRegister("1.0.2.8.2.101"),
    "1.0.2.8.3.101": GXDLMSRegister("1.0.2.8.3.101"),
    "1.0.2.8.4.101": GXDLMSRegister("1.0.2.8.4.101"),
    "1.0.3.8.0.101": GXDLMSRegister("1.0.3.8.0.101"),
    "1.0.3.8.1.101": GXDLMSRegister("1.0.3.8.1.101"),
    "1.0.3.8.2.101": GXDLMSRegister("1.0.3.8.2.101"),
    "1.0.3.8.3.101": GXDLMSRegister("1.0.3.8.3.101"),
    "1.0.3.8.4.101": GXDLMSRegister("1.0.3.8.4.101"),
    "1.0.4.8.0.101": GXDLMSRegister("1.0.4.8.0.101"),
    "1.0.4.8.1.101": GXDLMSRegister("1.0.4.8.1.255"),
    "1.0.4.8.2.101": GXDLMSRegister("1.0.4.8.2.255"),
    "1.0.4.8.3.101": GXDLMSRegister("1.0.4.8.3.255"),
    "1.0.4.8.4.101": GXDLMSRegister("1.0.4.8.4.255")
}


def read_not_config_registers():
    # Открываем соединение
    reader = open_connection()
    try:
        device_type = reader.deviceType
        if device_type == "1PH":
            working_dictionary = READ_REGISTERS_1PH
        elif device_type == "3PH":
            working_dictionary = READ_REGISTERS_3PH
        elif device_type == "TT":
            working_dictionary = READ_REGISTERS_TT
        else:
            print("Тип счетчика определен некорректно при считывании НЕ конфигурируемых регистров!!")
            raise Exception

        # Создаем словарь для хранения результатов
        result = {}

        # Читаем данные для конкретного пуша
        for key, value in working_dictionary.items():

            # Формируем ключ с названием и значением
            key_with_value = key + " >> " + value.getValues()[0]

            # Читаем несколько параметров
            try:
                # Создаем список значений
                values = [
                    reader.read(value, 2)
                ]
                # Сохраняем значения
                result[key_with_value] = values
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры НЕ конфигурируемых регистров")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['Value'])

        return df
    except Exception as e:
        print(f"Произошла ошибка при считывании НЕ конфигурируемых регистров: {e}")
        reader.close()
