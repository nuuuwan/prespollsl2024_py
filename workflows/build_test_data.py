import os
import sys

from utils import Log

from prespollsl2024 import ElectionResultsXlsx

log = Log('build_test_data')

if __name__ == '__main__':
    xlsx_path = os.path.join('data', f'prespollsl2024.xlsx')
    p_result_released = float(sys.argv[1])
    log.debug(f'{p_result_released=}')
    erx = ElectionResultsXlsx.build(xlsx_path, p_result_released)

    erx.validate()
    erx.write_json()
