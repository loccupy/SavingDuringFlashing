from tqdm import tqdm
import pandas as pd


def merge_excel_files(files, output_file):
    try:
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            # Используем tqdm для отображения прогресса
            for i, file in enumerate(tqdm(files, desc="Объединение файлов")):

                center_wrap_format = writer.book.add_format({
                    'text_wrap': True,
                    'align': 'center',
                    'valign': 'center'
                })

                # df = file
                sheet_name = f'{file[1]}'
                file[0].to_excel(writer, index=True, index_label='Параметр', sheet_name=sheet_name)

                # Получаем worksheet для текущего листа
                worksheet = writer.sheets[sheet_name]

                # Устанавливаем фиксированную ширину для столбцов A-D (1-4)
                for col_num in range(7):  # 4 столбца (A-D)
                    worksheet.set_column(col_num, col_num, 40, center_wrap_format)  # Ширина 40

    except Exception as e:
        print(f"Произошла ошибка при формировании excel файла: {e}")
    else:
        print(f"Файлы успешно объединены в {output_file}")
