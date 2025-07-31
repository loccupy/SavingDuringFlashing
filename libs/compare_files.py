import pandas as pd
from xlsxwriter import Workbook


def compare_excel_files(file1, file2, output_file):
    try:
        writer = pd.ExcelWriter(output_file, engine='xlsxwriter')

        center_wrap_format = writer.book.add_format({
            'text_wrap': True,
            'align': 'center',
            'valign': 'center'
        })

        dfs1 = pd.read_excel(file1, sheet_name=None, index_col=0)
        dfs2 = pd.read_excel(file2, sheet_name=None, index_col=0)

        for sheet_name in dfs1.keys():
            if sheet_name in dfs2:
                df1 = dfs1[sheet_name]
                df2 = dfs2[sheet_name]

                if list(df1.columns) != list(df2.columns):
                    print(f"Листы {sheet_name} имеют разные столбцы")
                    continue

                diff = df1.ne(df2)
                differences = pd.concat(
                    [
                        df1.where(diff, other=pd.NA).unstack().dropna(),
                        df2.where(diff, other=pd.NA).unstack().dropna()
                    ],
                    axis=1,
                    keys=[f'{file1}', f'{file2}']
                )
                if not differences.empty:
                    differences.to_excel(writer, sheet_name=f'Diff_{sheet_name}')

                    worksheet = writer.sheets[f'Diff_{sheet_name}']
                    max_cols = 4
                    for col_num in range(max_cols):
                        worksheet.set_column(col_num, col_num, 40, center_wrap_format)
            else:
                print(f"Лист {sheet_name} отсутствует в одном из файлов")

        writer.close()
    except Exception as e:
        print(f"Ошибка на этапе сравнения файлов: {e}")
