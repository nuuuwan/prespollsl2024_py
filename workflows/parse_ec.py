import os

from utils import JSONFile, Log

from prespollsl2024 import PDResult1, EDResult2

log = Log("parse_data")


def main():
    

    # PDResult1
    data_list = PDResult1.list_from_test()
    test_path = os.path.join('data', 'ec', 'test1-2024.json')
    PDResult1.store_list_to_json_compact(data_list, test_path)

    # Party Data
    party_idx = {}
    for for_party in data_list[0].by_party:
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

    # EDResult2
    data_list = EDResult2.list_from_test()
    test_path = os.path.join('data', 'ec', 'test2-2024.json')
    EDResult2.store_list_to_json_compact(data_list, test_path)


if __name__ == "__main__":
    main()
