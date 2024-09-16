import os

from gig import Ent, EntType, GIGTable
from utils import JSONFile


def parse_n(x):
    return int(round(float(x), 0))


def print_d(d):
    group_id = d['group_id']
    ent = d['ent']
    cum_p_pop = d['cum_p_pop']
    p_sinhalese = d['p_sinhalese']
    p_tamil = d['p_tamil']
    p_muslim = d['p_muslim']

    p_buddhist = d['p_buddhist']
    p_non_buddhist = p_sinhalese - p_buddhist

    print(
        f'{cum_p_pop:.1%}\t🟥 {p_non_buddhist:.1%}\t🟨 {p_buddhist:.1%}\t🟧 {p_tamil:.1%}\t🟩 {p_muslim:.1%}\t{ent.name}\t{group_id}'
    )


def main():
    gig_table_rel = GIGTable('population-religion', 'regions', '2012')
    gig_table_eth = GIGTable('population-ethnicity', 'regions', '2012')
    gig_election = GIGTable(
        f'government-elections-presidential',
        'regions-ec',
        f'2019',
    )
    pd_idx = Ent.idx_from_type(EntType.PD)
    ed_idx = Ent.idx_from_type(EntType.ED)

    d_list = []
    for d in gig_election.remote_data_list:
        ent_id = d['entity_id']
        if not (ent_id.startswith('EC-') and len(ent_id) == 6):
            continue

        if ent_id.endswith('P'):
            ent = ed_idx[ent_id[:5]]
        else:
            if ent_id not in pd_idx:
                continue
            ent = pd_idx[ent_id]

        d_rel = ent.gig(gig_table_rel)
        pop = d_rel.total
        p_buddhist = d_rel.buddhist / pop

        d_eth = ent.gig(gig_table_eth)
        p_tamil = (d_eth.sl_tamil + d_eth.ind_tamil) / pop
        p_muslim = (d_eth.sl_moor + d_eth.malay) / pop
        p_sinhalese = d_eth.sinhalese / pop

        p_sin_non_buddhist = p_sinhalese - p_buddhist

        electors = parse_n(d['electors'])
        d = dict(
            ent_id=ent_id,
            ent=ent,
            pop=electors,
            #
            p_buddhist=p_buddhist,
            p_tamil=p_tamil,
            p_muslim=p_muslim,
            p_sinhalese=p_sinhalese,
            p_sin_non_buddhist=p_sin_non_buddhist,
        )

        d_list.append(d)
    d_list.sort(key=lambda d: d['p_buddhist'])

    total_pop = sum(d['pop'] for d in d_list)

    # add cum_p
    exp_d_list = []
    cum_p_pop = 0
    for d in d_list:
        p_pop = d['pop'] / total_pop
        cum_p_pop += p_pop
        exp_d = dict(
            **d,
            p_pop=p_pop,
            cum_p_pop=cum_p_pop,
        )
        exp_d_list.append(exp_d)

    group_to_d_list = {}

    for d in exp_d_list:
        group_id = " No Majority"
        if d['p_tamil'] > 0.5:
            group_id = "Tamil >50%"
        elif d['p_muslim'] > 0.5:
            group_id = "Muslim >50%"
        elif d['p_sin_non_buddhist'] > 0.5:
            group_id = "Sinhala-Non-Buddhist >50%"
        elif d['p_buddhist'] > 0.94:
            group_id = "Sinhala-Buddhist >94%"
        elif d['p_buddhist'] > 0.88:
            group_id = "Sinhala-Buddhist 88-95%"
        elif d['p_buddhist'] > 0.77:
            group_id = "Sinhala-Buddhist 77-88%"
        elif d['p_buddhist'] > 0.50:
            group_id = "Sinhala-Buddhist 50-77%"

        d['group_id'] = group_id

        if group_id not in group_to_d_list:
            group_to_d_list[group_id] = []

        group_to_d_list[group_id].append(d)

        if group_id == "No Majority":
            print_d(d)

    print('-' * 32)
    print(f'{total_pop=}')
    for group_id, group_d_list in group_to_d_list.items():
        group_pop = sum(d['pop'] for d in group_d_list)
        p_group_pop = group_pop / total_pop
        group_pop_m = group_pop / 1_000_000
        print(
            f'{p_group_pop:.1%}', f'{group_pop_m:.1f}M', len(d_list), group_id
        )

    group_to_pd_ids = {}
    for group_id, d_list in group_to_d_list.items():
        pd_ids = [d['ent_id'] for d in d_list]
        group_to_pd_ids[group_id] = pd_ids

    JSONFile(
        os.path.join('workflows', 'electoral_zones', 'electoral_zones.json')
    ).write(group_to_pd_ids)


if __name__ == "__main__":
    main()
