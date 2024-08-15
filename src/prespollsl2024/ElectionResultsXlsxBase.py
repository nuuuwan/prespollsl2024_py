import random
from functools import cached_property

from openpyxl import load_workbook
from utils import JSONFile, Log

log = Log('ExcelResultsXlsx')


def random_float(min_value, max_value):
    return random.random() * (max_value - min_value) + min_value


class ElectionResultsXlsxBase:
    def __init__(self, xlsx_path: str):
        self.xlsx_path = xlsx_path

    @cached_property
    def data_list(self) -> list[dict]:
        wb = load_workbook(self.xlsx_path)
        ws = wb['results']
        data_list = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            data = {
                'pd_id': row[0],
                'ed_name': row[1],
                'pd_name': row[2],
                # space
                'result_time': row[4],
                # space
                'electors': row[6],
                'polled': row[7],
                'rejected': row[8],
                'valid': row[9],
                # space
            }
            for i, party_id in enumerate(self.PARTY_IDS):
                data[party_id] = row[11 + i]
            data_list.append(data)
        return data_list

    def write_json(
        self,
    ):
        json_path = self.xlsx_path[:-5] + '.json'
        JSONFile(json_path).write(self.data_list)
        n = len(self.data_list)
        log.info(f'Wrote {n} rows to {json_path}')
        return json_path
