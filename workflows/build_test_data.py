import os

from utils import Log

from prespollsl2024 import EDResult2, PDResult1, TestData1, TestData2

log = Log("build_test_data")


def main():
    for TestData, Result, id in [
        (TestData1, PDResult1, 'test1'),
        (TestData2, EDResult2, 'test2'),
    ]:
        data_list = TestData.build()
        dir_fake_test = os.path.join('data', 'fake', id)
        Result.store_list_to_dir(data_list, dir_fake_test)
        log.info(f'Wrote {dir_fake_test}')

        fake_json_path = os.path.join('data', 'fake', f'{id}-2024.json')
        Result.store_list_to_json_compact(data_list, fake_json_path)
        log.info(f'Wrote {fake_json_path}')


if __name__ == "__main__":
    main()
