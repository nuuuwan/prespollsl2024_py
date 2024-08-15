import os

from prespollsl2024 import ElectionResultsXlsx

if __name__ == '__main__':
    xlsx_path = os.path.join('data', f'prespollsl2024.xlsx')
    erx = ElectionResultsXlsx.load(xlsx_path)

    erx.validate()

    erx.write_json()
    erx.write_js()
