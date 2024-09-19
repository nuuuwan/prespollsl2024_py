import random
import time

from gig import GIGTable
from utils import Log

log = Log('RemoteDataUtils')


class RemoteDataUtils:
    @staticmethod
    def HACK_get_remote_data_list():
        MAX_RETRIES = 3
        T_SLEEP_BASE = 2
        for i in range(MAX_RETRIES):
            try:
                gig_table = GIGTable(
                    'government-elections-presidential', 'regions-ec', '2019'
                )
                remote_data_list = gig_table.remote_data_list
                if remote_data_list:
                    random.shuffle(remote_data_list)
                    return remote_data_list
            except Exception as e:
                log.error(f'[HACK_get_remote_data_list] {e}')
                t_sleep = T_SLEEP_BASE**i
                log.error(
                    f'[HACK_get_remote_data_list] Sleeping for {t_sleep}s'
                )
                time.sleep(t_sleep)
        raise Exception('[HACK_get_remote_data_list] Failed')
