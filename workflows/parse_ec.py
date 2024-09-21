import os

from utils import Log

from prespollsl2024 import PDResult1

log = Log("parse_ec")


def main():
    # PDResult1
    data_list = PDResult1.list_from_prod()
    test_path = os.path.join('data', 'ec', 'prod1-2024.json')
    PDResult1.store_list_to_json_compact(data_list, test_path)


if __name__ == "__main__":
    main()
