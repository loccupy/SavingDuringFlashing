from libs import config_data
from libs.config_active_calendar import read_active_calendar
from libs.config_autoconnect import read_autoconnect
from libs.config_data import read_data
from libs.config_disconnect import read_disconnect
from libs.config_gprs import read_gprs
from libs.config_limiters import read_limiter
from libs.config_profile_generic import read_profile_generic
from libs.config_push_setup import read_push
from libs.config_register import read_register
from libs.connect import open_connection

from libs.merge_excel import merge_excel_files
from libs.read_not_conf_registers import read_not_config_registers


def read_configuration_and_write_excel(file_name_read, flag):
    try:
        reader = open_connection()
        device_type = reader.deviceType
        print(f"Считан тип счетчика - {device_type}")
        reader.close()

        if device_type == "TT":
            df_for_data = read_data(flag)
            df_for_autoconnect = read_autoconnect()
            df_for_gprs = read_gprs(flag)
            df_for_pushes = read_push()
            df_for_profile_generic = read_profile_generic()
            df_for_registers = read_register()
            df_for_active_calendar = read_active_calendar()
            df_for_not_config_registers = read_not_config_registers()

            files = [[df_for_data, "data"],
                     [df_for_autoconnect, "autoconnect"],
                     [df_for_gprs, "gprs"],
                     [df_for_pushes, "push"],
                     [df_for_profile_generic, "profile_generic"],
                     [df_for_registers, "register"],
                     [df_for_active_calendar, "calendar"],
                     [df_for_not_config_registers, "not_conf_register"]]

            merge_excel_files(files, file_name_read)

            print("Конфигурация счетчика успешно считана")
        else:
            df_for_data = read_data(flag)
            df_for_autoconnect = read_autoconnect()
            df_for_gprs = read_gprs(flag)
            df_for_pushes = read_push()
            df_for_profile_generic = read_profile_generic()
            df_for_registers = read_register()
            df_for_active_calendar = read_active_calendar()
            df_for_limiters = read_limiter()
            df_for_disconnect = read_disconnect()
            df_for_not_config_registers = read_not_config_registers()

            files = [[df_for_data, "data"],
                     [df_for_limiters, "limiters"],
                     [df_for_autoconnect, "autoconnect"],
                     [df_for_gprs, "gprs"],
                     [df_for_disconnect, "disconnect"],
                     [df_for_pushes, "push"],
                     [df_for_profile_generic, "profile_generic"],
                     [df_for_registers, "register"],
                     [df_for_active_calendar, "calendar"],
                     [df_for_not_config_registers, "not_conf_register"]]

            merge_excel_files(files, file_name_read)

            print("Конфигурация счетчика успешно считана")

    except Exception as e:
        print(f"Произошла ошибка на этапе считывания всех конфигураций: {e}")
        raise
