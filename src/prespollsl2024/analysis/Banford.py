from gig import EntType, GIGTable


def parse_num(s):
    return int(round(float(s)))


class Banford:
    @staticmethod
    def analyze(year):
        gt = GIGTable(
            'government-elections-presidential', 'regions-ec', f'{year}'
        )
        num_list = []
        for d in gt.remote_data_list:
            entity_id = d['entity_id']
            if EntType.from_id(entity_id) != EntType.PD:
                continue
            for k, v in d.items():
                if k in ['entity_id']:
                    continue
                num_list.append(parse_num(v))

        Banford.test(num_list)

    @staticmethod
    def test(num_list):
        idx = {}
        for num in num_list:
            lead = int(str(num)[0])
            if lead == 0:
                continue
            if lead not in idx:
                idx[lead] = 0
            idx[lead] += 1

        n_total = sum(idx.values())
        print(f'{n_total=:,}')
        for lead, n in sorted(idx.items(), key=lambda x: x[1], reverse=True):
            p = n / n_total
            print(lead, f'{p:.1%}')


if __name__ == '__main__':
    for year in [1982, 1988, 1994, 1999, 2005, 2010, 2015, 2019]:
        print(f'{year=}')
        Banford.analyze(year)
