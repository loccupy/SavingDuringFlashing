from gurux_dlms.objects import GXDLMSGprsSetup
import pandas as pd

from libs.connect import open_connection

set_gprs_value = {
    "gprs_1": "gprs-for-test-1",
    "gprs_2": "gprs-for-test-2",
    "gprs_3": "gprs-for-test-3",
    "gprs_4": "gprs-for-test-4",
    "gprs_5": "gprs-for-test-5",
    "gprs_6": "gprs-for-test-6"
}

CONFIG_FOR_GPRS = {
    'gprs_1': GXDLMSGprsSetup('0.0.25.4.0.255'),
    'gprs_2': GXDLMSGprsSetup('0.1.25.4.0.255'),
    'gprs_3': GXDLMSGprsSetup('0.2.25.4.0.255'),
    'gprs_4': GXDLMSGprsSetup('0.3.25.4.0.255'),
    'gprs_5': GXDLMSGprsSetup('0.4.25.4.0.255'),
    'gprs_6': GXDLMSGprsSetup('0.5.25.4.0.255')
}

def check_version(flagg):
    try:
        list_new_object = [
                            'gprs_2',
                            'gprs_3',
                            'gprs_4',
                            'gprs_5',
                            'gprs_6'
                           ]

        dct_of_parameters = CONFIG_FOR_GPRS.copy()
        if flagg is True:
            for key in list_new_object:
                dct_of_parameters.pop(key)
        return dct_of_parameters
    except Exception as e:
        print(f"Произошла ошибка на этапе проверки флага новый/старый счечтик для объектов класса Data: {e}")


def read_gprs(flag):
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        dct_of_parameters = check_version(flag)
        # Формируем ключ с названием и значением
        key = "gprs"
        key_with_value = key + " >> " + GXDLMSGprsSetup().getValues()[0]
        for key, value in dct_of_parameters.items():
            try:
                result[key + " >> " + value.getValues()[0]] = reader.read(value, 2)
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key + " >> " + value.getValues()[0]] = "Ошибка чтения"

        print("Считаны параметры GPRS")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['GPRS name'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_gprs(flag):
    reader = open_connection()
    try:
        dct_of_parameters = check_version(flag)
        for key, value in set_gprs_value.items():
            try:
                try:
                    data = dct_of_parameters[key]
                except KeyError:
                    continue
                data.apn = value
                reader.write(data, 2)

                print(f"Успешно записан параметр: gprs >> {key}")
            except Exception as e:
                print(f"Ошибка при записи параметра {key} со значением {value}: {e}")

        reader.close()

        df = read_gprs(flag)
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации gprs: {e}")
        reader.close()
