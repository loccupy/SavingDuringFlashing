import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QHBoxLayout, \
    QCheckBox, QGroupBox, QListWidget, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtGui import QTextCursor, QIntValidator

from libs import connect
from libs.compare_files import compare_excel_files
from libs.configure_meter_and_write_excel import configure_meter_and_write_excel
from libs.read_configuration_and_write_excel import read_configuration_and_write_excel


class EmittingStream(QObject):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass  # Необходимо для совместимости с sys.stdout


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.applyDarkTheme()

        self.layout = QVBoxLayout(self)

        self.input_section = QVBoxLayout()

        self.button_group1 = QHBoxLayout()

        self.read_config_in_excel = QPushButton('Считать и записать в excel', self)
        self.read_config_in_excel.clicked.connect(self.read_config)

        self.write_and_read_config_in_excel = QPushButton('Сконфигурировать, считать и записать в excel', self)
        self.write_and_read_config_in_excel.clicked.connect(self.write_config)

        # Добавляем кнопки в горизонтальные группы
        self.button_group1.addWidget(self.read_config_in_excel)
        self.button_group1.addWidget(self.write_and_read_config_in_excel)

        self.add_files = QPushButton('Добавить файлы для сравнения', self)
        self.add_files.clicked.connect(self.addFiles)

        self.compare = QPushButton('Сравнить файлы', self)
        self.compare.clicked.connect(self.compare_files)

        self.fileListWidget = QListWidget(self)
        self.fileListWidget.setFixedSize(900, 100)

        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)  # Запрещаем редактирование
        self.redirect_stdout()
        self.stream.textWritten.connect(self.on_text_written)

        self.create_fields_for_connect()

        self.layout.addLayout(self.input_section)
        self.layout.addLayout(self.button_group1)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.add_files)
        self.layout.addWidget(self.fileListWidget)
        self.layout.addWidget(self.compare)

        self.setLayout(self.layout)
        self.setWindowTitle('Проверка сохранения параметров')
        # Устанавливаем минимальный размер
        self.setMinimumSize(300, 530)

    def read_config(self):
        try:
            flag = self.checkbox.isChecked()
            if self.main_com_port_field.text() == "":
                QMessageBox.warning(self, "Ошибка", "Введите номер COM порта соединения!")
                return
            else:
                connect.COM = "COM" + self.main_com_port_field.text()
            try:
                connect.BAUDRATE = int(self.main_speed_field.text())
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", "Введите скорость соединения!")
                return

            file_name_read = self.showDialog() + ".xlsx"
            read_configuration_and_write_excel(file_name_read, flag)
        except Exception as e:
            print(e)
            return

    def write_config(self):
        try:
            flag = self.checkbox.isChecked()
            if self.main_com_port_field.text() == "":
                QMessageBox.warning(self, "Ошибка", "Введите номер COM порта соединения!")
                return
            else:
                connect.COM = "COM" + self.main_com_port_field.text()
            try:
                connect.BAUDRATE = int(self.main_speed_field.text())
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", "Введите скорость соединения!")
                return

            file_name_read = self.showDialog() + ".xlsx"
            configure_meter_and_write_excel(file_name_read, flag)
        except Exception as e:
            print(e)
            return

    def compare_files(self):
        if not self.fileListWidget:
            QMessageBox.warning(self, "Ошибка", "Файлы для сравнения не выбраны!")
            return
        file_1 = self.fileListWidget.item(0).text()
        file_2 = self.fileListWidget.item(1).text()

        output_file = self.showDialog() + ".xlsx"

        compare_excel_files(file_1, file_2, output_file)

    def create_fields_for_connect(self):
        self.master_meter_section = QGroupBox("Настройки подключения")
        master_layout = QVBoxLayout()

        main_connection_section = QHBoxLayout()

        # Поле для скорости основного соединения
        self.main_speed_field = QLineEdit()
        self.main_speed_field.setPlaceholderText("Введите скорость соединения")
        self.main_speed_field.setValidator(QIntValidator())  # Добавляем валидацию только для чисел
        self.main_speed_field.setAlignment(Qt.AlignCenter)

        # Поле для com-port основного соединения
        self.main_com_port_field = QLineEdit()
        self.main_com_port_field.setPlaceholderText("Введите номер COM порта соединения")
        self.main_com_port_field.setValidator(QIntValidator())
        self.main_com_port_field.setAlignment(Qt.AlignCenter)

        self.checkbox = QCheckBox("Старая прошивка")

        main_connection_section.addWidget(self.checkbox)
        main_connection_section.addWidget(self.main_speed_field)
        main_connection_section.addWidget(self.main_com_port_field)

        # Добавляем секции в основной макет
        master_layout.addLayout(main_connection_section)

        # Устанавливаем макет для секции
        self.master_meter_section.setLayout(master_layout)

        # Добавляем секцию в основной макет
        self.input_section.addWidget(self.master_meter_section)

        # Добавляем отступы между элементами
        master_layout.setSpacing(10)

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Диалог ввода', 'Назовите файл:')
        if ok:
            return text

    def addFiles(self):
        # Открытие диалогового окна выбора файлов
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Выберите Excel файлы",
            "",
            "Excel файлы (*.xlsx)"
        )

        # Проверяем количество выбранных файлов
        if len(files) > 2:
            QMessageBox.warning(self, "Ошибка", "Можно выбрать только 2 файла")
            return

        # Проверка, были ли выбраны файлы
        if files:
            for file in files:
                # Проверяем расширение файла
                if not file.lower().endswith('.xlsx'):
                    QMessageBox.warning(self, "Ошибка", "Выбран недопустимый файл. Разрешены только файлы Excel")
                    continue

                # Добавляем файл в список
                self.fileListWidget.addItem(file)

                if len(self.fileListWidget) > 2:
                    self.fileListWidget.clear()
                    QMessageBox.warning(self, "Ошибка", "Можно выбрать только 2 файла, попробуйте еще раз")
                    return

        else:
            self.statusBar().showMessage("Файлы не выбраны")

    def redirect_stdout(self):
        self.stream = EmittingStream()
        sys.stdout = self.stream
        sys.stderr = self.stream

    def on_text_written(self, text):
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()
        QApplication.processEvents()

    def applyDarkTheme(self):
        # Определяем стили для темной темы
        dark_stylesheet = """
        QWidget {
            background-color: #2c313c;
            color: #ffffff;
        }

        QLineEdit {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px;
        }

        QLineEdit:focus {
            border: 1px solid #61dafb;
        }

        QPushButton {
            background-color: #363d47;
            color: #ffffff;
            border: 1px solid #444950;
            border-radius: 4px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #444950;
        }

        QPushButton:pressed {
            background-color: #2c313c;
        }
        """

        # Применяем стиль к приложению
        self.setStyleSheet(dark_stylesheet)
