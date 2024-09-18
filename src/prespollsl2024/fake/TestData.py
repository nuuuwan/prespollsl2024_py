from gig import Ent, GIGTable
from utils import Time, TimeFormat

from prespollsl2024.ec import ECData, ECDataForParty, ECDataSummary
from prespollsl2024.fake.TEST_PARTY_IDX import TEST_PARTY_IDX


def parse_int(x):
    return int(round(float(x), 0))


class TestData:
    @staticmethod
    def build_summary(d):
        valid = parse_int(d['valid'])
        rejected = parse_int(d['rejected'])
        polled = parse_int(d['polled'])
        electors = parse_int(d['electors'])

        return ECDataSummary(
            valid=valid,
            rejected=rejected,
            polled=polled,
            electors=electors,
            percent_valid=valid / electors,
            percent_rejected=rejected / electors,
            percent_polled=polled / electors,
        )

    @staticmethod
    def build_by_party(valid):
        value_sum = sum(TEST_PARTY_IDX.values())
        by_party = []
        for party_code, value in TEST_PARTY_IDX.items():
            votes = int(round(valid * value / value_sum, 0))

            for_party = ECDataForParty(
                party_code=party_code,
                votes=votes,
                percentage=votes / valid,
                party_name='TODO',
                candidate='TODO',
            )
            by_party.append(for_party)

        return by_party

    @staticmethod
    def build() -> list[ECData]:
        gig_table_2019 = GIGTable(
            'government-elections-presidential', 'regions-ec', '2019'
        )

        ec_data_list = []
        # '2024-09-06 12:02:22:814'
        TIME_FORMAT = TimeFormat('%Y-%m-%d %H:%M:%S:000')
        sequence_number = 0
        for d in gig_table_2019.remote_data_list:
            entity_id = d['entity_id']
            if not (entity_id.startswith('EC-') and len(entity_id) == 6):
                continue

            sequence_number += 1
            pd_id = entity_id
            pd_code = pd_id[3:]

            if pd_id.endswith('P'):
                ed_id = pd_id[:-1]
                ed = Ent.from_id(ed_id)
                ed_name = ed.name
                pd_name = f'Postal {ed_name}'

            else:
                pd = Ent.from_id(pd_id)
                pd_name = pd.name
                ed_id = pd.ed_id
                ed = Ent.from_id(ed_id)
                ed_name = ed.name
                ed_code = ed_id[3:]

            summary = TestData.build_summary(d)
            ec_data = ECData(
                timestamp=TIME_FORMAT.stringify(Time.now()),
                level='POLLING-DIVISION',
                ed_code=ed_code,
                ed_name=ed_name,
                pd_code=pd_code,
                pd_name=pd_name,
                by_party=TestData.build_by_party(summary.valid),
                summary=summary,
                type='PRESIDENTIAL-FIRST',
                sequence_number=f'{sequence_number:04}',
                reference=f'{sequence_number:09}',
            )
            ec_data_list.append(ec_data)

        return ec_data_list
