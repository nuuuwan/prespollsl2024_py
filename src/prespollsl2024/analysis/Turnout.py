from gig import EntType, GIGTable


def parse_num(s):
    return int(round(float(s)))


class Turnout:
    @staticmethod
    def analyze(year):
        gt = GIGTable(
            'government-elections-presidential', 'regions-ec', f'{year}'
        )
        for d in gt.remote_data_list:
            entity_id = d['entity_id']
            if EntType.from_id(entity_id) != EntType.ED:
                continue
            polled = parse_num(d['polled'])
            electors = parse_num(d['electors'])
            p_turnout = polled / electors
            print(p_turnout)


if __name__ == '__main__':
    for year in [2015, 2019]:
        print(f'{year=}')
        Turnout.analyze(year)
