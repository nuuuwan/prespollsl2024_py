import os

from prespollsl2024 import ElectionResultsXlsx

if __name__ == '__main__':
    xlsx_path = os.path.join('data', f'prespollsl2024.xlsx')
    erx = ElectionResultsXlsx.load(xlsx_path)
    json_path = erx.write_json()
    js_path = erx.write_js()

    os.startfile(json_path)
    os.startfile(xlsx_path)
    os.startfile(js_path)
