import os

from utils import JSONFile, Log

from prespollsl2024 import PDResult1

log = Log("parse_ec_data")


def main():
    ec_data_list = PDResult1.list_from_test()

    # JSON
    test_path = os.path.join('data', 'ec', 'test-2024.json')
    PDResult1.store_list_to_json_compact(ec_data_list, test_path)

    # TSV
    test_path = os.path.join('data', 'ec', 'test-2024.tsv')
    PDResult1.build_tsv(ec_data_list, test_path)
    log.info(f'Wrote {test_path}')

    # Party Data
    party_idx = {}
    for for_party in ec_data_list[0].by_party:
        party_idx[for_party.party_code] = dict(
            party_code=for_party.party_code,
            party_name=for_party.party_name,
            candidate=for_party.candidate,
        )
    party_idx_path = os.path.join('data', 'ec', 'party_idx.json')
    JSONFile(party_idx_path).write(party_idx)
    log.info(f'Wrote {party_idx_path}')

    party_id_list = sorted(list(party_idx.keys()))
    party_id_list_path = os.path.join('data', 'ec', 'party_id_list.json')
    JSONFile(party_id_list_path).write(party_id_list)
    log.info(f'Wrote {party_id_list_path}')


if __name__ == "__main__":
    main()
