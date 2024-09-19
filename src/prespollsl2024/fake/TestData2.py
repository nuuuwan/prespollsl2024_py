import os
import random

from gig import Ent
from utils import JSONFile, Log, Time, TimeFormat

from prespollsl2024.ec import EDResult2, ForParty2, Summary2
from prespollsl2024.fake.RemoteDataUtils import RemoteDataUtils
from prespollsl2024.fake.TEST_PARTY_TO_P_VOTES2 import TEST_PARTY_TO_P_VOTES2
from utils_future import StringX

log = Log('TestData2')


TEST_PARTY_IDX = JSONFile(os.path.join('data', 'ec', 'party_idx.json')).read()


class TestData2:
    @staticmethod
    def build_summary(d):
        total = StringX(d['valid']).int

        return Summary2(
            total=total,
        )

    @staticmethod
    def get_party_and_q_votes():
        K_RANDOM = 1
        party_to_q_votes = {
            party: p_votes * (1 + K_RANDOM * random.random())
            for party, p_votes in TEST_PARTY_TO_P_VOTES2.items()
        }

        party_and_q_votes = sorted(
            party_to_q_votes.items(), key=lambda x: x[1], reverse=True
        )

        return party_and_q_votes

    @staticmethod
    def build_by_party(valid):
        
        
        party_and_q_votes = TestData2.get_party_and_q_votes()
        sum_q_votes = sum([x[1] for x in party_and_q_votes])

        by_party = []
        for party_code, q_votes in party_and_q_votes:
            preferences = int(round(valid * q_votes / sum_q_votes, 0))

            party_data = TEST_PARTY_IDX[party_code]

            for_party = ForParty2(
                party_code=party_code,
                preferences=preferences,
                party_name=party_data['party_name'],
                candidate=party_data['candidate'],
            )
            by_party.append(for_party)

        return by_party

    @staticmethod
    def build() -> list[EDResult2]:
        data_list = []
        TIME_FORMAT = TimeFormat('%Y-%m-%d %H:%M:%S:000')
        sequence_number = 0
        remote_data_list = RemoteDataUtils.HACK_get_remote_data_list()

        

        n_results = random.randint(1, 22)
        for d in remote_data_list:
            entity_id = d['entity_id']
            if not (entity_id.startswith('EC-') and len(entity_id) == 5):
                continue

            sequence_number += 1
            if sequence_number > n_results:
                break
            
            ed_id = entity_id
            ed_code = ed_id[3:]
            ed = Ent.from_id(ed_id)
            ed_name = ed.name

            summary = TestData2.build_summary(d)
            data = EDResult2(
                timestamp=TIME_FORMAT.stringify(
                    Time(Time.now().ut - sequence_number * 120)
                ),
                level=EDResult2.get_level(),
                ed_code=ed_code,
                ed_name=ed_name,
                by_party=TestData2.build_by_party(
                    summary.total, 
                ),
                summary=summary,
                type=EDResult2.get_type(),
                sequence_number=f'{sequence_number:04}',
                reference=f'{sequence_number:09}',
            )
            data_list.append(data)

        data_list.sort(key=lambda x: x.timestamp)

        return data_list
