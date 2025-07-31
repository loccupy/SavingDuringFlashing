import pandas as pd
from gurux_dlms.enums import DataType

from gurux_dlms.objects import GXDLMSData

from libs.connect import open_connection

set_data_value = {
    # Коэффициенты трансформации
    'trans_cof_active_power': 3000,
    'trans_cof_reactive_power': 3000,

    # Коэффициенты трансформации тока и напряжения
    'current_trans_ratio': 23,
    'voltage_trans_ratio': 24,

    # Тарифы и интервалы
    'emergency_tariff': 3,
    'integration_interval_1': 15,
    'integration_interval_2': 30,

    # Фильтрация и импульсные выходы
    'push_filter': 0,
    'pulse_output_1_mode': 108,
    'pulse_output_2_mode': 7,
    'master_slave_mode': 74,

    # Параметры GSM-модуля
    'usd_balance': "12345",

    # Параметры, отсутствующие в старых прошивках
    'switch_simholder_esim': 2,
    'switch_connect_type': 2,
    'switch_gsm_rf': 1,
    'reason_push_1': 2,
    'reason_push_2': 3,
    'reason_push_3': 2,
    'internal_antenna': 1,
    'multi_sim': 93,

    # APN настройки
    'apn_user_name_1': 'apn-user-name-11',
    'apn_user_name_2': 'apn-user-name-22',
    'apn_user_name_3': 'apn-user-name-33',
    'apn_user_name_4': 'apn-user-name-44',
    'apn_user_name_5': 'apn-user-name-55',
    'apn_user_name_6': 'apn-user-name-66',
    'apn_password_1': 'apn-password-11',
    'apn_password_2': 'apn-password-22',
    'apn_password_3': 'apn-password-33',
    'apn_password_4': 'apn-password-44',
    'apn_password_5': 'apn-password-55',
    'apn_password_6': 'apn-password-66',

    # FTP
    "ftp_destination_address": "192.168.14.13:21",
    "ftp_user_name": "FtpNameForTest",
    "ftp_user_password": "FtpPassForTest",
    "ftp_user_path": "/FtpPathForTest/",

    # Display
    "mode_of_the_display": 6
}

CONFIG_FOR_DATA = {
    # Коэффициенты трансформации
    'trans_cof_active_power': GXDLMSData('1.0.0.3.3.255'),  # Коэффициент трансформации активной мощности
    'trans_cof_reactive_power': GXDLMSData('1.0.0.3.4.255'),  # Коэффициент трансформации реактивной мощности

    # Коэффициенты трансформации тока и напряжения
    'current_trans_ratio': GXDLMSData('1.0.0.4.2.255'),  # Коэффициент трансформации тока
    'voltage_trans_ratio': GXDLMSData('1.0.0.4.3.255'),  # Коэффициент трансформации напряжения

    # Тарифы и интервалы
    'emergency_tariff': GXDLMSData('0.0.96.5.131.255'),  # Чрезвычайный тариф
    'integration_interval_1': GXDLMSData('1.0.0.8.4.255'),  # Интервал интеграции 1
    'integration_interval_2': GXDLMSData('1.0.0.8.5.255'),  # Интервал интеграции 2

    # Параметры GSM-модуля
    'usd_balance': GXDLMSData('0.0.2.164.8.255'),  # Баланс USSD

    # Фильтрация и импульсные выходы
    'push_filter': GXDLMSData('0.0.97.98.10.255'),  # Фильтр push-уведомлений
    'pulse_output_1_mode': GXDLMSData('0.0.96.4.2.255'),  # Режим импульсного выхода 1
    'pulse_output_2_mode': GXDLMSData('0.1.96.4.2.255'),  # Режим импульсного выхода 2
    'master_slave_mode': GXDLMSData('0.0.164.164.0.255'),  # Режим мастер-слейв

    # Параметры, отсутствующие в старых прошивках
    'switch_simholder_esim': GXDLMSData('0.0.2.164.12.255'),  # Нет на старых прошивках
    'switch_connect_type': GXDLMSData('0.0.2.164.13.255'),  # Нет на старых прошивках
    'switch_gsm_rf': GXDLMSData('0.0.2.164.14.255'),  # Нет на старых прошивках
    'internal_antenna': GXDLMSData('0.0.2.164.15.255'),  # Нет на старых прошивках
    'multi_sim': GXDLMSData('0.1.164.164.0.255'),  # Нет на старых прошивках
    'reason_push_1': GXDLMSData('0.0.96.5.134.255'),  # Нет на старых прошивках
    'reason_push_2': GXDLMSData('0.1.96.5.134.255'),  # Нет на старых прошивках
    'reason_push_3': GXDLMSData('0.2.96.5.134.255'),  # Нет на старых прошивках

    # APN
    'apn_user_name_1': GXDLMSData('0.0.99.13.166.255'),
    'apn_password_1': GXDLMSData('0.0.99.13.167.255'),
    'apn_user_name_2': GXDLMSData('0.1.99.13.166.255'),
    'apn_password_2': GXDLMSData('0.1.99.13.167.255'),
    'apn_user_name_3': GXDLMSData('0.2.99.13.166.255'),
    'apn_password_3': GXDLMSData('0.2.99.13.167.255'),
    'apn_user_name_4': GXDLMSData('0.3.99.13.166.255'),
    'apn_password_4': GXDLMSData('0.3.99.13.167.255'),
    'apn_user_name_5': GXDLMSData('0.4.99.13.166.255'),
    'apn_password_5': GXDLMSData('0.4.99.13.167.255'),
    'apn_user_name_6': GXDLMSData('0.5.99.13.166.255'),
    'apn_password_6': GXDLMSData('0.5.99.13.167.255'),

    # FTP
    "ftp_destination_address": GXDLMSData("0.0.2.164.1.255"),
    "ftp_user_name": GXDLMSData("0.0.2.164.2.255"),
    "ftp_user_password": GXDLMSData("0.0.2.164.3.255"),
    "ftp_user_path": GXDLMSData("0.0.2.164.4.255"),

    # Display
    "mode_of_the_display": GXDLMSData("0.0.96.4.1.255")
}


def check_version(flagg):
    try:
        list_new_object = ['switch_simholder_esim',
                           'switch_connect_type',
                           'switch_gsm_rf',
                           'internal_antenna',
                           'multi_sim',
                           'reason_push_1',
                           'reason_push_2',
                           'reason_push_3',
                           'apn_user_name_2',
                           'apn_password_2',
                           'apn_user_name_3',
                           'apn_password_3',
                           'apn_user_name_4',
                           'apn_password_4',
                           'apn_user_name_5',
                           'apn_password_5',
                           'apn_user_name_6',
                           'apn_password_6'
                           ]

        dct_of_parameters = CONFIG_FOR_DATA.copy()
        if flagg is True:
            for key in list_new_object:
                dct_of_parameters.pop(key)
        return dct_of_parameters
    except Exception as e:
        print(f"Произошла ошибка на этапе проверки флага новый/старый счечтик для объектов класса Data: {e}")


def read_data(flag):
    reader = open_connection()
    try:
        result = {}

        dct_of_parameters = check_version(flag)

        for key, value in dct_of_parameters.items():
            try:
                result[key + " >> " + value.getValues()[0]] = reader.read(value, 2)
            except Exception as e:
                print(f"Ошибка при чтении данных: {e}")
                result[key + " >> " + value.getValues()[0]] = "Ошибка чтения"

        print("Считаны параметры всех объектов Data")
        reader.close()

        df = pd.DataFrame.from_dict(result, orient='index', columns=['Значение'])

        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе чтения объектов класса Data: {e}")
        reader.close()


def config_data(flag):
    reader = open_connection()
    try:
        dct_of_parameters = check_version(flag)

        for key, data in dct_of_parameters.items():
            try:
                data_type = reader.readType(data, 2)
                if data_type == 0:
                    data_type = DataType.STRING
                data.value = set_data_value[key]
                data.setDataType(2, data_type)
                reader.write(data, 2)
                print(f"Успешно записан параметр: {key}")
            except Exception as e:
                print(f"Ошибка при записи параметра {key}: {e}")

        reader.close()

        df = read_data(flag)
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации объектов класса Data: {e}")
        reader.close()
