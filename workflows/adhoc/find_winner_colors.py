from gig import GIGTable


def parse_votes(x):
    return int(round(float(x), 0))


def main():
    election_type = 'presidential'
    p_winner_list = []
    for year in [1982, 1988, 1994, 1999, 2005, 2010, 2015, 2019]:
        gig_table = GIGTable(
            f'government-elections-{election_type}',
            'regions-ec',
            f'{year}',
        )

        for d in gig_table.remote_data_list:
            entity_id = d['entity_id']
            valid = parse_votes(d['valid'])
            if len(entity_id) != 6:
                continue
            party_to_votes = {}
            for k, v in d.items():
                if k in [
                    'entity_id',
                    'valid',
                    'rejected',
                    'electors',
                    'polled',
                ]:
                    continue
                party_to_votes[k] = parse_votes(v)
            party_to_votes = dict(
                sorted(
                    party_to_votes.items(),
                    key=lambda item: item[1],
                    reverse=True,
                )
            )
            list(party_to_votes.keys())[0]
            p_winner = list(party_to_votes.values())[0] / valid

            p_winner_list.extend([p_winner])

    p_winner_list.sort()
    n = len(p_winner_list)
    p_min = p_winner_list[n // 6]
    p_mid = p_winner_list[n // 2]
    p_max = p_winner_list[n * 5 // 6]

    print(f'p_min: {p_min:.1%}')
    print(f'p_mid: {p_mid:.1%}')
    print(f'p_max: {p_max:.1%}')


if __name__ == "__main__":
    main()
