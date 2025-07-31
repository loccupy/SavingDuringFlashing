import sys

from PyQt5.QtWidgets import QApplication

from libs.config_profile_generic import read_profile_generic
from libs.ui import Ui

file_name_config_and_read = "config_and_read_files_1.xlsx"
file_name_read = "read_files.xlsx"


def func():
    app = QApplication(sys.argv)
    ex = Ui()
    ex.show()
    sys.exit(app.exec_())


def debug_file():
    read_profile_generic()


if __name__ == "__main__":
    func()
