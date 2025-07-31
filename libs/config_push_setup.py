import random

# from gurux_dlms.objects import GXDLMSPushSetup
import pandas as pd

from libs.GXDLMSPushSetup import GXDLMSPushSetup
from libs.GXDateTime import GXDateTime

from gurux_dlms.objects.enums import ServiceType

# import GXDLMSPushSetup
# from libs.GXDateTime import GXDateTime
from libs.connect import open_connection

PUSHES = {
    'push_1': GXDLMSPushSetup("0.0.25.9.0.255"),
    'push_2': GXDLMSPushSetup("0.1.25.9.0.255"),
    'push_3': GXDLMSPushSetup("0.2.25.9.0.255")
}

set_push_value = {
    'push_1': {
        'service': ServiceType.UDP,
        'destination': f"122.122.122.122:{random.randint(1, 9999)}",
        'randomisationStartInterval': random.randint(1, 9999),
        'numberOfRetries': random.randint(1, 100),
        'repetitionDelay': 303,
        'communicationWindow': (GXDateTime(f"*.*.* 11:{random.randint(0, 30)}:00", '%m.%d.%y %H:%M:%S'),
                                GXDateTime(f"*.*.* 11:{random.randint(40, 59)}:00", '%m.%d.%y %H:%M:%S'))
    },
    'push_2': {
        'service': ServiceType.UDP,
        'destination': f"222.222.222.222:{random.randint(1, 9999)}",
        'randomisationStartInterval': random.randint(1, 9999),
        'numberOfRetries': random.randint(1, 100),
        'repetitionDelay': 302,
        'communicationWindow': (GXDateTime(f"*.*.* 00:{random.randint(0, 30)}:00", '%m.%d.%y %H:%M:%S'),
                                GXDateTime(f"*.*.* 22:{random.randint(40, 59)}:59", '%m.%d.%y %H:%M:%S'))
    },
    'push_3': {
        'service': ServiceType.UDP,
        'destination': f"222.222.222.222:{random.randint(1, 9999)}",
        'randomisationStartInterval': random.randint(1, 1000),
        'numberOfRetries': random.randint(1, 100),
        'repetitionDelay': 301,
        'communicationWindow': (GXDateTime(f"*.*.* 23:{random.randint(0, 30)}:00", '%m.%d.%y %H:%M:%S'),
                                GXDateTime(f"*.*.* 06:{random.randint(40, 59)}:59", '%m.%d.%y %H:%M:%S'))
    }
}


def read_push():
    reader = open_connection()
    try:
        # Создаем словарь для хранения результатов
        result = {}

        # Читаем данные для конкретного пуша
        for key, value in PUSHES.items():

            # Формируем ключ с названием и значением
            key_with_value = key + " >> " + value.getValues()[0]

            # Читаем несколько параметров
            try:
                # Создаем список значений
                values = [
                    reader.read(value, 3)[0],
                    reader.read(value, 3)[1],
                    reader.read(value, 5),
                    reader.read(value, 6),
                    reader.read(value, 7),
                    (reader.read(value, 4)[0][0].toFormatString(), reader.read(value, 4)[0][1].toFormatString())
                ]
                # Сохраняем значения
                result[key_with_value] = values
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key_with_value] = "Ошибка чтения"

        print("Считаны параметры пушей")
        # Закрываем соединение
        reader.close()

        # Создаем DataFrame
        df = pd.DataFrame.from_dict(result, orient='index', columns=['service', 'destination', 'randomisation',
                                                                     'number_of_retries', 'repetition_delay',
                                                                     'communicationWindow'])

        return df
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        reader.close()


def config_pushes():
    reader = open_connection()
    try:
        for key, data in PUSHES.items():
            data.service = set_push_value[key]['service']
            data.destination = set_push_value[key]['destination']
            data.randomisationStartInterval = set_push_value[key]['randomisationStartInterval']
            data.numberOfRetries = set_push_value[key]['numberOfRetries']
            data.repetitionDelay = set_push_value[key]['repetitionDelay']
            data.communicationWindow = [(set_push_value[key]['communicationWindow'])]
            for i in [3, 4, 5, 6, 7]:
                try:
                    reader.write(data, i)
                    print(f"Успешно записан параметр: {key} под индексом {i}")
                except Exception as e:
                    print(f"Ошибка при записи параметра {key} под индексом {i}: {e}")

        reader.close()

        df = read_push()
        return df
    except Exception as e:
        print(f"Ошибка на этапе конфигурации пушей: {e}")
        reader.close()
