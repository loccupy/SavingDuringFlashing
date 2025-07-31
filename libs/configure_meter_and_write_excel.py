from libs.config_data import config_data
from libs.connect import open_connection
from libs.config_active_calendar import config_active_calendar
from libs.config_autoconnect import config_autoconnect
from libs.config_disconnect import config_disconnect
from libs.config_gprs import config_gprs
from libs.config_limiters import config_limiters
from libs.config_profile_generic import config_profile_generic
from libs.config_push_setup import config_pushes
from libs.config_register import config_registers
from libs.merge_excel import merge_excel_files
from libs.read_not_conf_registers import read_not_config_registers


def configure_meter_and_write_excel(file_name_config_and_read, flag):
    reader = open_connection()
    try:
        device_type = reader.deviceType
        print(f"Считан тип счетчика - {device_type}")
        reader.close()

        if device_type == "TT":
            df_for_data = config_data(flag)
            df_for_autoconnect = config_autoconnect()
            df_for_gprs = config_gprs(flag)
            df_for_pushes = config_pushes()
            df_for_profile_generic = config_profile_generic()
            df_for_registers = config_registers()
            df_for_active_calendar = config_active_calendar()
            df_for_not_config_registers = read_not_config_registers()

            files = [[df_for_data, "data"],
                     [df_for_autoconnect, "autoconnect"],
                     [df_for_gprs, "gprs"],
                     [df_for_pushes, "push"],
                     [df_for_profile_generic, "profile_generic"],
                     [df_for_registers, "register"],
                     [df_for_active_calendar, "calendar"],
                     [df_for_not_config_registers, "not_conf_register"]]

            merge_excel_files(files, file_name_config_and_read)

            print("Счетчик успешно сконфигурирован как ТТ")
        else:
            df_for_data = config_data(flag)
            df_for_autoconnect = config_autoconnect()
            df_for_gprs = config_gprs(flag)
            df_for_pushes = config_pushes()
            df_for_profile_generic = config_profile_generic()
            df_for_registers = config_registers()
            df_for_active_calendar = config_active_calendar()
            df_for_limiters = config_limiters()
            df_for_disconnect = config_disconnect()
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

            merge_excel_files(files, file_name_config_and_read)

            print("Счетчик успешно сконфигурирован как 1ph или 3ph")
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации и создания excel файла: {e}")
        reader.close()
