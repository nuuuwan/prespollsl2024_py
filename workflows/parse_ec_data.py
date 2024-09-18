import os
from utils import JSONFile, Log
from prespollsl2024 import ECData

log = Log("parse_ec_data")


def main():
    ec_data_list = ECData.list_from_test()
    test_path = os.path.join('data', 'ec', 'test-2024.tsv')
    ECData.build_tsv(ec_data_list, test_path)
    log.info(f'Wrote {test_path}')

    party_idx = {}
    for for_party in ec_data_list[0].by_party:
        party_idx[for_party.party_code] = dict(
            party_code=for_party.party_code,
            party_name=for_party.party_name,
            candidate=for_party.candidate,
        )
    party_idx_path = os.path.join('data', 'ec', 'party_idx.json')
    JSONFile.write(party_idx, party_idx_path)
    log.info(f'Wrote {party_idx_path}')

    party_id_list = sorted(list(party_idx.keys()))
    party_id_list_path = os.path.join('data', 'ec', 'party_id_list.json')
    JSONFile.write(party_id_list, party_id_list_path)


if __name__ == "__main__":
    main()
