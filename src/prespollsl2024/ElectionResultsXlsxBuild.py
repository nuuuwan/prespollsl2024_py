import random

from gig import Ent, EntType, GIGTable
from openpyxl import Workbook
from utils import Log, Time, TimeFormat

from utils_future import XLSXUtils

log = Log('ExcelResultsXlsx')


def random_float(min_value, max_value):
    return random.random() * (max_value - min_value) + min_value


class ElectionResultsXlsxBuild:
    PARTY_TO_WEIGHT = {
        'SJB': 0.45,
        'NPP': 0.3,
        'UNP': 0.2,
        'SLPP': 0.05,
    }
    PARTY_IDS = list(PARTY_TO_WEIGHT.keys())
    VOTES_NOISE = 0.6

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

        party_to_weight_random = {
            party: weight
            + random.random() * ElectionResultsXlsxBuild.VOTES_NOISE
            for party, weight in ElectionResultsXlsxBuild.PARTY_TO_WEIGHT.items()
        }
        total_weight = sum(party_to_weight_random.values())

        for party_weight_random in party_to_weight_random.values():
            p_party = 0.95 * party_weight_random / total_weight
            row.append(int(valid * p_party))

    @staticmethod
    def add_statistics_zero(row):
        row.append("")

        result_time = 0
        row.append(result_time)
        row.append("")

        electors = 0
        polled = 00
        rejected = 0
        valid = 0
        row.extend([electors, polled, rejected, valid])
        row.append("")

        for _ in ElectionResultsXlsxBuild.PARTY_IDS:
            row.append(0)

    @staticmethod
    def add_eds(ws, p_result_released):
        eds = Ent.list_from_type(EntType.ED)

        election_2020_idx = (
            ElectionResultsXlsxBuild.GIG_TABLE_ELECTION_2020.remote_data_idx
        )
        for ed in eds:
            postal_pd_id = ed.id + 'P'
            data = election_2020_idx[postal_pd_id]

            row = [
                postal_pd_id,
                ed.name,
                'Postal - ' + ed.name,
            ]

            if random.random() < p_result_released:
                electors_2020 = int(round(float(data['electors']), 0))
                ElectionResultsXlsxBuild.add_statistics(row, electors_2020)
            else:
                ElectionResultsXlsxBuild.add_statistics_zero(row)
            ws.append(row)

    @staticmethod
    def add_pds(ws, p_result_released):
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
            if random.random() < p_result_released:
                electors_2020 = int(round(float(electors_2020), 0))
                ElectionResultsXlsxBuild.add_statistics(row, electors_2020)
            else:
                ElectionResultsXlsxBuild.add_statistics_zero(row)
            ws.append(row)

    @staticmethod
    def format_columns(ws):
        number_format = '#,##0'
        for col in ws.iter_cols(min_col=4):
            for cell in col:
                cell.number_format = number_format

    @classmethod
    def build(cls, xlsx_path, p_result_released):
        log.debug(f'Building {xlsx_path}...')
        wb = Workbook()
        ws = wb.active
        ws.title = 'results'

        ElectionResultsXlsxBuild.add_header(ws)

        ElectionResultsXlsxBuild.add_eds(ws, p_result_released)
        ElectionResultsXlsxBuild.add_pds(ws, p_result_released)

        ElectionResultsXlsxBuild.format_columns(ws)

        XLSXUtils.fix_column_widths(ws)
        XLSXUtils.format_cells(ws)
        XLSXUtils.freeze(ws)

        wb.save(xlsx_path)
        log.info(f'Wrote {xlsx_path}')

        return cls(xlsx_path)
