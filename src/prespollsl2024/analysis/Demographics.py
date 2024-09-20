import os

from gig import Ent, EntType, GIGTable
from utils import JSONFile, Log

log = Log('Demographics')


class Demographics:
    GT_ELECTION = GIGTable(
        'government-elections-presidential', 'regions-ec', '2019'
    )
    GT_RELIGION = GIGTable('population-religion', 'regions', '2012')
    GT_ETHNICITY = GIGTable('population-ethnicity', 'regions', '2012')

    @staticmethod
    def get_group(ent):
        row_rel = ent.gig(Demographics.GT_RELIGION)
        row_eth = ent.gig(Demographics.GT_ETHNICITY)
        n_total = row_rel.total
        assert row_eth.total == n_total

        # Sinhala-Buddhist
        n_buddhist = row_rel.buddhist
        p_buddhist = n_buddhist / n_total
        p_limits = [0.94, 0.88, 0.77, 0.5]
        previous_p_limit = None
        for p_limit in p_limits:
            if p_buddhist >= p_limit:
                if not previous_p_limit:
                    label = f'>{p_limit:.0%}'
                else:
                    label = f'{int(p_limit*100):d}-{previous_p_limit:.0%}'
                return f'Sinh.-Bud. {label}'
            previous_p_limit = p_limit

        # Sinhala-Non-Buddhist
        n_sinhala = row_eth.sinhalese
        p_sinhala = n_sinhala / n_total
        p_sinhala_non_buddhist = p_sinhala - p_buddhist

        if p_sinhala_non_buddhist > 0.5:
            return 'Sinh.-Non-Bud. >50%'

        # Tamil
        n_tamil = row_eth.sl_tamil + row_eth.ind_tamil
        p_tamil = n_tamil / n_total
        if p_tamil > 0.5:
            return 'Tamil >50%'

        # Muslim
        n_muslim = row_eth.sl_moor + row_eth.malay
        p_muslim = n_muslim / n_total
        if p_muslim > 0.5:
            return 'Muslim >50%'

        return 'No Majority'

    @staticmethod
    def get_pd_id_to_ent():
        idx = {}
        for d in Demographics.GT_ELECTION.remote_data_list:
            entity_id = d['entity_id']
            if EntType.from_id(entity_id) != EntType.PD:
                continue

            if entity_id.endswith('P'):
                ed_id = entity_id[:-1]
                ent = Ent.from_id(ed_id)
            else:
                ent = Ent.from_id(entity_id)

            idx[entity_id] = ent
        return idx

    @staticmethod
    def get_ed_id_to_ent():
        idx = {}
        for d in Demographics.GT_ELECTION.remote_data_list:
            entity_id = d['entity_id']

            if EntType.from_id(entity_id) != EntType.ED:
                continue

            ent = Ent.from_id(entity_id)

            idx[entity_id] = ent
        return idx

    @staticmethod
    def get_group_to_ent_id_list(ent_id_to_ent):
        idx = {}
        for ent_id, ent in ent_id_to_ent.items():
            group = Demographics.get_group(ent)
            if group not in idx:
                idx[group] = []
            idx[group].append(ent_id)
        return idx

    def analyze(group_to_ent_id_list):
        election_idx = Demographics.GT_ELECTION.remote_data_idx
        group_to_electors = {}
        for group, ent_id_list in group_to_ent_id_list.items():
            total_electors = 0
            for ent_id in ent_id_list:
                result = election_idx[ent_id]
                electors = int(round(float(result['electors'])))
                total_electors += electors
            group_to_electors[group] = total_electors

        total_total_electors = sum(group_to_electors.values())
        for group, electors in sorted(
            group_to_electors.items(), key=lambda x: x[1], reverse=True
        ):
            p_electors = electors / total_total_electors
            print(group.ljust(30), f'{p_electors:.1%}'.rjust(10))


if __name__ == '__main__':
    # group_to_pd_id_list = Demographics.get_group_to_ent_id_list(Demographics.get_pd_id_to_ent())
    # Demographics.analyze(group_to_pd_id_list)
    # JSONFile(os.path.join('data-analysis', 'group_to_pd_id_list.json')).write(group_to_pd_id_list)

    group_to_ed_id_list = Demographics.get_group_to_ent_id_list(
        Demographics.get_ed_id_to_ent()
    )
    Demographics.analyze(group_to_ed_id_list)
    JSONFile(os.path.join('data-analysis', 'group_to_ed_id_list.json')).write(
        group_to_ed_id_list
    )
