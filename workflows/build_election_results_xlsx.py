import os
import shutil
from utils import Log

from prespollsl2024 import ElectionResultsXlsx

log = Log('build_election_results_xlsx')

if __name__ == '__main__':
    xlsx_path = os.path.join('data', f'prespollsl2024.xlsx')
    n_results_released = 130
    erx = ElectionResultsXlsx.build(xlsx_path, n_results_released)

    erx.validate()

    erx.write_json()
    js_path = erx.write_js()
    dest_js_path = os.path.join(
        os.environ['DIR_JS_REACT'],
        'prespollsl2024',
        'src',
        'nonview',
        'constants',
        'PRESPOLLSL2024.js',
    )
    shutil.copy(js_path, dest_js_path)
    log.info(f'Copied {js_path} to {dest_js_path}')
