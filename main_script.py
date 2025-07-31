import sys

from PyQt5.QtWidgets import QApplication

from libs.config_profile_generic import read_profile_generic
from libs.config_push_setup import read_push
from libs.read_not_conf_registers import read_not_config_registers
from libs.ui import Ui

file_name_config_and_read = "config_and_read_files_1.xlsx"
file_name_read = "read_files.xlsx"


def func():
    app = QApplication(sys.argv)
    ex = Ui()
    ex.show()
    sys.exit(app.exec_())

    # # config_active_calendar()
    # read_data(flag=True)


def debug_file():
    # read_push()
    # config_pushes()
    # config_disconnect()
    # config_autoconnect()
    # print(read_active_calendar())
    # config_active_calendar()
    # read_not_config_registers()
    read_profile_generic()


if __name__ == "__main__":
    func()
