import os
import random
import time

from gig import Ent, GIGTable
from utils import JSONFile, Log, Time, TimeFormat

from prespollsl2024.ec import ForParty1, PDResult1, Summary1
from prespollsl2024.fake.RemoteDataUtils import RemoteDataUtils
from prespollsl2024.fake.TEST_PARTY_TO_P_VOTES import TEST_PARTY_TO_P_VOTES
from utils_future import StringX

log = Log('TestData1')


TEST_PARTY_IDX = JSONFile(os.path.join('data', 'ec', 'party_idx.json')).read()


class TestData1:
    @staticmethod
    def build_summary(d):
        valid = StringX(d['valid']).int
        rejected = StringX(d['rejected']).int
        polled = StringX(d['polled']).int
        electors = StringX(d['electors']).int

        return Summary1(
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
        K_RANDOM = 1
        party_to_q_votes = {
            party: p_votes * (1 + K_RANDOM * random.random())
            for party, p_votes in TEST_PARTY_TO_P_VOTES.items()
        }
        sum_q_votes = sum(party_to_q_votes.values())

        by_party = []
        for party_code, q_votes in party_to_q_votes.items():
            votes = int(round(valid * q_votes / sum_q_votes, 0))

            party_data = TEST_PARTY_IDX[party_code]

            for_party = ForParty1(
                party_code=party_code,
                votes=votes,
                percentage=votes / valid,
                party_name=party_data['party_name'],
                candidate=party_data['candidate'],
            )
            by_party.append(for_party)

        return by_party

    @staticmethod
    def HACK_get_remote_data_list():
        MAX_RETRIES = 3
        T_SLEEP_BASE = 2
        for i in range(MAX_RETRIES):
            try:
                gig_table = GIGTable(
                    'government-elections-presidential', 'regions-ec', '2019'
                )
                remote_data_list = gig_table.remote_data_list
                if remote_data_list:
                    random.shuffle(remote_data_list)
                    return remote_data_list
            except Exception as e:
                log.error(f'[HACK_get_remote_data_list] {e}')
                t_sleep = T_SLEEP_BASE**i
                log.error(
                    f'[HACK_get_remote_data_list] Sleeping for {t_sleep}s'
                )
                time.sleep(t_sleep)
        raise Exception('[HACK_get_remote_data_list] Failed')

    @staticmethod
    def build() -> list[PDResult1]:
        ec_data_list = []
        # '2024-09-06 12:02:22:814'
        TIME_FORMAT = TimeFormat('%Y-%m-%d %H:%M:%S:000')
        sequence_number = 0
        remote_data_list = RemoteDataUtils.HACK_get_remote_data_list()

        n_results = random.randint(1, 182)
        for d in remote_data_list:
            entity_id = d['entity_id']
            if not (entity_id.startswith('EC-') and len(entity_id) == 6):
                continue

            sequence_number += 1
            if sequence_number > n_results:
                break
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

            summary = TestData1.build_summary(d)
            ec_data = PDResult1(
                timestamp=TIME_FORMAT.stringify(
                    Time(Time.now().ut - sequence_number * 120)
                ),
                level=PDResult1.get_level(),
                ed_code=ed_code,
                ed_name=ed_name,
                pd_code=pd_code,
                pd_name=pd_name,
                by_party=TestData1.build_by_party(summary.valid),
                summary=summary,
                type=PDResult1.get_type(),
                sequence_number=f'{sequence_number:04}',
                reference=f'{sequence_number:09}',
            )
            ec_data_list.append(ec_data)

        ec_data_list.sort(key=lambda x: x.timestamp)

        return ec_data_list
