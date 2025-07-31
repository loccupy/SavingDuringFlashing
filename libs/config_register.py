from gurux_dlms.enums import DataType
from gurux_dlms.objects import GXDLMSRegister
import pandas as pd

from libs.connect import open_connection

REGISTERS_FOR_3PH = {
    'Согласованное_напряжение': GXDLMSRegister("1.0.0.6.4.255"),
    'Значение_отклонения_напряжения_для_провала': GXDLMSRegister("1.0.12.31.1.255"),
    'Значение_отклонения_напряжения_для_пропадания': GXDLMSRegister("1.0.12.39.1.255"),
    'Коэффициент_реактивной_мощности_Пороговое_значение_по_времени': GXDLMSRegister("1.0.131.44.0.255"),
    'Пороговое_значение_мощности_для_интервала_нормальных_нагрузок': GXDLMSRegister("1.0.15.35.128.255"),
    'Пороговое_значение_мощности_для_интервала_пиковых_нагрузок': GXDLMSRegister("1.0.15.35.130.255"),
    'Порог_отклонения_по_частоте': GXDLMSRegister("1.0.145.35.0.255"),
    'Значение_отклонения_напряжения_для_фиксации_перенапряжения': GXDLMSRegister("1.0.12.35.1.255"),
    'Порог_для_фиксации_коэффициента_несимметрии_напряжений': GXDLMSRegister("1.0.133.35.0.255"),  # ONLY 3PH
    'Коэффициент_несимметрии_по_обратной_последовательности': GXDLMSRegister("1.0.133.44.0.255"),  # ONLY 3PH
    'Порог_фиксации_магнитного_поля': GXDLMSRegister("1.0.164.51.3.255"),
    'Верхняя_граница_фиксации_температуры': GXDLMSRegister("0.0.135.190.0.255"),
    'Нижняя_граница_фиксации_температуры': GXDLMSRegister("0.0.135.190.1.255"),
    'Время_усреднения_температуры': GXDLMSRegister("0.0.135.190.2.255"),
}

set_register_value = {
    'Согласованное_напряжение': {
        'value': 222222
    },
    'Значение_отклонения_напряжения_для_провала': {
        'value': 7
    },
    'Значение_отклонения_напряжения_для_пропадания': {
        'value': 93
    },
    'Коэффициент_реактивной_мощности_Пороговое_значение_по_времени': {
        'value': 9
    },
    'Пороговое_значение_мощности_для_интервала_нормальных_нагрузок': {
        'value': 11000
    },
    'Пороговое_значение_мощности_для_интервала_пиковых_нагрузок': {
        'value': 15000
    },
    'Порог_отклонения_по_частоте': {
        'value': 2
    },
    'Значение_отклонения_напряжения_для_фиксации_перенапряжения': {
        'value': 15
    },
    'Порог_для_фиксации_коэффициента_несимметрии_напряжений': {
        'value': 2250
    },
    'Коэффициент_несимметрии_по_обратной_последовательности': {
        'value': 19
    },
    'Порог_фиксации_магнитного_поля': {
        'value': 15
    },
    'Верхняя_граница_фиксации_температуры': {
        'value': 44
    },
    'Нижняя_граница_фиксации_температуры': {
        'value': -44
    },
    'Время_усреднения_температуры': {
        'value': 900
    }
}


def read_register():
    # Открываем соединение
    reader = open_connection()
    if reader.deviceType == "1PH":
        dct_of_parameters = REGISTERS_FOR_3PH.copy()
        dct_of_parameters.pop('Порог_для_фиксации_коэффициента_несимметрии_напряжений')
        dct_of_parameters.pop('Коэффициент_несимметрии_по_обратной_последовательности')
    else:
        dct_of_parameters = REGISTERS_FOR_3PH.copy()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Читаем данные для конкретного пуша
        for key, value in dct_of_parameters.items():

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

        print("Считаны параметры конфигурируемых регистров")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['Value'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_registers():
    reader = open_connection()
    try:
        if reader.deviceType == "1PH":
            dct_of_parameters = REGISTERS_FOR_3PH.copy()
            dct_of_parameters.pop('Порог_для_фиксации_коэффициента_несимметрии_напряжений')
            dct_of_parameters.pop('Коэффициент_несимметрии_по_обратной_последовательности')
        else:
            dct_of_parameters = REGISTERS_FOR_3PH.copy()
        for key, data in dct_of_parameters.items():
            try:
                data_type = reader.readType(data, 2)
                if data_type == 0:
                    data_type = DataType.STRING
                data.value = set_register_value[key]['value']
                data.setDataType(2, data_type)
                reader.write(data, 2)
                print(f"Успешно записан параметр: {key}")
            except Exception as e:
                print(f"Ошибка при записи параметра {key}: {e}")

        reader.close()

        df = read_register()
        return df
    except Exception as e:
        print(f"Ошибка на этапе конфигурации регистров: {e}")
        reader.close()
