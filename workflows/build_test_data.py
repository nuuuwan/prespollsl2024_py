import os

from utils import Log

from prespollsl2024 import ECData, TestData

log = Log("build_test_data")


def main():
    ec_data_list = TestData.build()
    dir_fake_test = os.path.join('data', 'fake', 'test')
    ECData.store_list_to_dir(ec_data_list, dir_fake_test)
    log.info(f'Wrote {dir_fake_test}')

    fake_tsv_path = os.path.join('data', 'fake', 'test-2024.tsv')
    ECData.build_tsv(ec_data_list, fake_tsv_path)
    log.info(f'Wrote {fake_tsv_path}')

    fake_json_path = os.path.join('data', 'fake', 'test-2024.json')
    ECData.store_list_to_json_compact(ec_data_list, fake_json_path)
    log.info(f'Wrote {fake_json_path}')


if __name__ == "__main__":
    main()
