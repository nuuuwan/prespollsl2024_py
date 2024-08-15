import os
import random

from gig import Ent, EntType, GIGTable
from openpyxl import Workbook
from utils import Log, Time, TimeFormat

from utils_future import XLSXUtils

log = Log('ExcelResultsXlsx')


def random_float(min_value, max_value):
    return random.random() * (max_value - min_value) + min_value


class ElectionResultsXlsxBuild:
    PARTY_IDS = [
        'SJB',
        'NPP',
        'UNP',
        'SLPP',
    ]
    GIG_TABLE_ELECTION_2020 = GIGTable(
        'government-elections-parliamentary', 'regions-ec', '2020'
    )

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
            + ElectionResultsXlsxBuild.PARTY_IDS
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
            random_float(0.1, 0.5) for _ in ElectionResultsXlsxBuild.PARTY_IDS
        ]
        total_weight = sum(party_weight)

        for i, _ in enumerate(ElectionResultsXlsxBuild.PARTY_IDS):
            p_party = 0.95 * party_weight[i] / total_weight
            row.append(int(valid * p_party))

    @staticmethod
    def add_eds(ws):
        eds = Ent.list_from_type(EntType.ED)
        election_2020_idx = (
            ElectionResultsXlsxBuild.GIG_TABLE_ELECTION_2020.remote_data_idx
        )
        for ed in eds:
            postal_pd_id = ed.id + 'P'
            data = election_2020_idx[postal_pd_id]
            electors_2020 = int(round(float(data['electors']), 0))

            row = [
                postal_pd_id,
                ed.name,
                'Postal - ' + ed.name,
            ]
            ElectionResultsXlsxBuild.add_statistics(row, electors_2020)

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
                        ElectionResultsXlsxBuild.GIG_TABLE_ELECTION_2020
                    ).electors,
                    0,
                )
            )
            row = [
                pd.id,
                ed.name,
                pd.name,
            ]
            ElectionResultsXlsxBuild.add_statistics(row, electors_2020)

            ws.append(row)

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

    @classmethod
    def build(cls, xlsx_path):
        log.debug(f'Building {xlsx_path}...')
        wb = Workbook()
        ws = wb.active
        ws.title = 'results'

        ElectionResultsXlsxBuild.add_header(ws)
        ElectionResultsXlsxBuild.add_eds(ws)
        ElectionResultsXlsxBuild.add_pds(ws)

        ElectionResultsXlsxBuild.format_columns(ws)

        XLSXUtils.fix_column_widths(ws)
        XLSXUtils.format_cells(ws)
        XLSXUtils.freeze(ws)

        wb.save(xlsx_path)
        log.info(f'Wrote {xlsx_path}')

        return cls(xlsx_path)

    @classmethod
    def load(cls, xlsx_path):
        if os.path.exists(xlsx_path):
            log.warning(f'{xlsx_path} exists')
            return cls(xlsx_path)

        return cls.build(xlsx_path)
