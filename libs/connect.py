from libs.GXSettings import GXSettings
from libs.GXDLMSReader import GXDLMSReader

COM = "COM3"
BAUDRATE = 115200


def open_connection():
    settings = GXSettings()
    try:
        settings.getParameters("COM", COM,
                               password="1234567898765432",
                               authentication="High",
                               serverAddress=16,
                               logicalAddress=1,
                               clientAddress=48,
                               baudRate=BAUDRATE)

        reader = GXDLMSReader(settings.client, settings.media, settings.trace, settings.invocationCounter)
        settings.media.open()
        reader.initializeConnection()
        print("Счетчик подключен")
        return reader
    except Exception as e:
        settings.media.close()
        print(f"Ошибка на этапе подключения к счетчику: {e}")
        raise
