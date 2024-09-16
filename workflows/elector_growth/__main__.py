from gig import Ent, EntType, GIGTable


def parse_n(x):
    return int(round(float(x), 0))


def main():
    gig_election_first = GIGTable(
        f'government-elections-presidential',
        'regions-ec',
        f'1982',
    )
    gig_election_last = GIGTable(
        f'government-elections-presidential',
        'regions-ec',
        f'2019',
    )
    pd_idx = Ent.idx_from_type(EntType.PD)

    d_list = []
    for pd_id, pd in pd_idx.items():
        electors_first = pd.gig(gig_election_first).electors
        electors_last = pd.gig(gig_election_last).electors
        p_growth = (electors_last - electors_first) / electors_first
        d = {
            'pd_id': pd_id,
            'pd_name': pd.name,
            'electors_first': electors_first,
            'electors_last': electors_last,
            'p_growth': p_growth,
        }
        d_list.append(d)
    d_list.sort(key=lambda x: x['p_growth'], reverse=True)

    for i, d in enumerate(d_list, start=1):
        p_growth = d['p_growth']
        print(f'{i}) {d["pd_name"]}')


if __name__ == "__main__":
    main()
