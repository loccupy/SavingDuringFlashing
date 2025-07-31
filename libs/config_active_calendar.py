import pandas as pd
from libs.GXDateTime import GXDateTime

from libs.GXDLMSActivityCalendar import GXDLMSActivityCalendar

from libs.connect import open_connection

CONFIG_FOR_ACTIVITY_CALENDAR = {
    'ActivityCalendar': GXDLMSActivityCalendar('0.0.13.0.0.255'),
}


def read_active_calendar():
    reader = open_connection()
    try:
        result = {}

        data = CONFIG_FOR_ACTIVITY_CALENDAR['ActivityCalendar']

        result['Active Calendar Name'] = reader.read(data, 2)
        result['Active Season Profile'] = [i.__str__() for i in reader.read(data, 3)]
        result['Active Week Profile Table'] = [i.__str__() for i in reader.read(data, 4)]
        result['Active Day Profile Table'] = [i.__str__() for i in reader.read(data, 5)]
        result['Passive Calendar Name'] = reader.read(data, 6)
        result['Passive Season Profile'] = [i.__str__() for i in reader.read(data, 7)]
        result['Passive Week Profile Table'] = [i.__str__() for i in reader.read(data, 8)]
        result['Passive Day Profile Table'] = [i.__str__() for i in reader.read(data, 9)]
        result['Time'] = reader.read(data, 10).__str__()

        print("Считаны параметры тарифного расписания")
        reader.close()

        df = pd.DataFrame.from_dict(result, orient='index', columns=['Value'])
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе чтения тарифного расписания: {e}")
        reader.close()


def config_active_calendar():
    reader = open_connection()
    try:
        try:
            calendar = GXDLMSActivityCalendar()
            reader.add_day_profile(calendar, day_count=4, interval_count=4)
            reader.add_week_profile(calendar, week_count=4)
            reader.write(calendar, 9)
            reader.write(calendar, 8)
            reader.add_season_profile(calendar, season_count=4)
            reader.write(calendar, 7)
            # reader.activate_passive_calendar()
            print(f"Успешно записано активировано расписание")
        except Exception as e:
            print(f"Ошибка при активации расписания: {e}")

        try:
            calendar = GXDLMSActivityCalendar()
            reader.add_day_profile(calendar, day_count=4, interval_count=4)
            reader.add_week_profile(calendar, week_count=4)
            reader.write(calendar, 9)
            reader.write(calendar, 8)
            reader.add_season_profile(calendar, season_count=4)
            reader.write(calendar, 7)
            print(f"Успешно записано пассивное расписание")
        except Exception as e:
            print(f"Ошибка при записи пассивного расписания: {e}")

        try:
            calendar = GXDLMSActivityCalendar()
            time = GXDateTime("01.01.2026 00:00:00", '%m.%d.%Y %H:%M:%S')
            calendar.time = time
            reader.write(calendar, 10)
            print(f"Успешно записано дата активации пассивного календаря")
        except Exception as e:
            print(f"Ошибка при записи даты активации пассивного календаря: {e}")

        reader.close()

        df = read_active_calendar()
        return df
    except Exception as e:
        print(f"Произошла ошибка на этапе конфигурации тарифного расписания: {e}")
        reader.close()
