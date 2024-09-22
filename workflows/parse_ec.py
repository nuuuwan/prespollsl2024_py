import os

from utils import Log

from prespollsl2024.ec import EDResult2

log = Log("parse_ec")


def main():
    # EDResult2
    data_list = EDResult2.list_from_prod()
    test_path = os.path.join('data', 'ec', 'prod2-2024.json')
    EDResult2.store_list_to_json_compact(data_list, test_path)


if __name__ == "__main__":
    main()
