import os
import random

from gig import Ent, EntType, GIGTable
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from utils import Log, Time, TimeFormat

log = Log('ExcelResultsXlsx')


def random_float(min_value, max_value):
    return random.random() * (max_value - min_value) + min_value


class ElectionResultsXlsx:
    PARTY_IDS = [
        'SJB',
        'NPP',
        'UNP',
        'SLPP',
    ]
    GIG_TABLE_ELECTION_2020 = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )

    def __init__(self, xlsx_path: str):
        self.xlsx_path = xlsx_path

    @staticmethod
    def add_header(ws):
        ws.append(
            [
                'pd_id',
                'ed_name',
                'pd_name',
                "",
                'result_time',
                "",
                'electors',
                'polled',
                'rejected',
                'valid',
                "",
            ]
            + ElectionResultsXlsx.PARTY_IDS
        )

    @staticmethod
    def add_statistics(row, electors_previous):
        row.append("")

        result_time = TimeFormat('%Y-%m-%d %H:%M').format(
            Time(Time.now().ut - random.random() * 3600 * 12)
        )
        row.append(result_time)
        row.append("")

        electors = int(electors_previous * random_float(1, 1.1))
        polled = int(electors * random_float(0.6, 0.9))
        rejected = int(polled * random_float(0.01, 0.03))
        valid = polled - rejected
        row.extend([electors, polled, rejected, valid])
        row.append("")

        party_weight = [
            random_float(0.1, 0.5) for _ in ElectionResultsXlsx.PARTY_IDS
        ]
        total_weight = sum(party_weight)

        for i, _ in enumerate(ElectionResultsXlsx.PARTY_IDS):
            p_party = 0.95 * party_weight[i] / total_weight
            row.append(int(valid * p_party))
        row.append("")

    @staticmethod
    def add_eds(ws):
        eds = Ent.list_from_type(EntType.ED)
        election_2020_idx = (
            ElectionResultsXlsx.GIG_TABLE_ELECTION_2020.remote_data_idx
        )
        for ed in eds:
            postal_pd_id = ed.id + 'P'
            data = election_2020_idx[postal_pd_id]
            electors_2020 = int(round(float(data['electors']), 0))

            row = [
                postal_pd_id[3:],
                ed.name,
                'Postal - ' + ed.name,
            ]
            ElectionResultsXlsx.add_statistics(row, electors_2020)

            ws.append(row)

    @staticmethod
    def add_pds(ws):
        pds = Ent.list_from_type(EntType.PD)
        for pd in pds:
            ed_id = pd.id[:-1]
            ed = Ent.from_id(ed_id)
            electors_2020 = int(
                round(
                    pd.gig(
                        ElectionResultsXlsx.GIG_TABLE_ELECTION_2020
                    ).electors,
                    0,
                )
            )
            row = [
                pd.id[3:],
                ed.name,
                pd.name,
            ]
            ElectionResultsXlsx.add_statistics(row, electors_2020)

            ws.append(row)

    @staticmethod
    def fix_column_widths(ws):
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    cell_value = str(cell.value)
                    if cell_value.startswith('='):
                        continue
                    if len(cell_value) > max_length:
                        max_length = len(str(cell.value))
                except BaseException:
                    pass
            adjusted_width = max_length
            ws.column_dimensions[column_letter].width = max(8, adjusted_width)

    @staticmethod
    def format_columns(ws):
        number_format = '#,##0'
        for col in ws.iter_cols(min_col=4):
            for cell in col:
                cell.number_format = number_format

        col_result_time = 5
        for col in ws.iter_cols(
            min_col=col_result_time, max_col=col_result_time
        ):
            for cell in col:
                cell.number_format = 'yyyy-mm-dd hh-mm'

    @staticmethod
    def format_cells(
        ws,
    ):
        fill = PatternFill(
            start_color="000088", end_color="000088", fill_type="solid"
        )
        font = Font(color="FFFFFF")
        for cell in ws[1]:
            cell.fill = fill
            cell.font = font

    @staticmethod
    def freeze(ws):
        ws.freeze_panes = 'A2'

    @staticmethod
    def build(date):
        xlsx_path = os.path.join('data', f'election-{date}.xlsx')
        log.debug(f'Building {xlsx_path}...')
        wb = Workbook()
        ws = wb.active
        ws.title = 'results'

        ElectionResultsXlsx.add_header(ws)
        ElectionResultsXlsx.add_eds(ws)
        ElectionResultsXlsx.add_pds(ws)

        ElectionResultsXlsx.format_columns(ws)
        ElectionResultsXlsx.fix_column_widths(ws)
        ElectionResultsXlsx.format_cells(ws)
        ElectionResultsXlsx.freeze(ws)

        wb.save(xlsx_path)
        log.info(f'Wrote {xlsx_path}')

        return ElectionResultsXlsx(xlsx_path)

    @staticmethod
    def load(date):
        xlsx_path = os.path.join('data', f'election-{date}.xlsx')
        if os.path.exists(xlsx_path) and False:
            log.warning(f'{xlsx_path} exists')
            return ElectionResultsXlsx(xlsx_path)

        return ElectionResultsXlsx.build(date)

    @property
    def data_list(self) -> list[dict]:
        wb = Workbook()
        ws = wb.active
        ws = wb['results']
        data_list = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            data = {
                'pd_id': row[0],
                'ed_name': row[1],
                'pd_name': row[2],
                # 2 spaces
                'result_time': row[5],
                'electors': row[6],
                'polled': row[7],
                'rejected': row[8],
                'valid': row[9],
            }
            for i, party_id in enumerate(ElectionResultsXlsx.PARTY_IDS):
                data[party_id] = row[10 + i]
        return data_list


if __name__ == '__main__':
    ElectionResultsXlsx.load(
        '2024-09-21',
    )
