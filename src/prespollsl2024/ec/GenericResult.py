import os
import shutil

from utils import JSONFile, Log

log = Log("GenericResult")


class GenericResult:
    @classmethod
    def from_file(cls, json_file_path: str) -> 'GenericResult':
        d = JSONFile(json_file_path).read()
        if d.get('level') not in cls.get_level_list():
            return None
        if d.get('type') != cls.get_type():
            return None

        data = cls.from_dict(d)
        log.debug(f'Loaded from {json_file_path}')
        return data

    @staticmethod
    def dedupe(data_list: list['GenericResult']) -> list['GenericResult']:
        deduped_data_list = []
        code_set = set()
        for data in data_list:
            code = data.code
            if code in code_set:
                log.warning(f'Duplicate: {code}')
                continue
            deduped_data_list.append(data)
            code_set.add(code)
        return deduped_data_list

    @classmethod
    def list_for_dir(cls, dir_path: str) -> list['GenericResult']:
        data_list = []
        for file_name in os.listdir(dir_path):
            if not file_name.endswith(".json"):
                log.warning(f'Ignoring {file_name}')
                continue
            data = cls.from_file(os.path.join(dir_path, file_name))
            if not data:
                log.warning(f'No result for {file_name}')
                continue

            data_list.append(data)

        data_list = GenericResult.dedupe(data_list)
        
        data_list.sort(key=lambda x: x.timestamp)
        log.info(f'Loaded {len(data_list)} results from {dir_path}')
        return data_list

    @classmethod
    def list_from_test(cls) -> list['GenericResult']:
        return cls.list_for_dir(cls.get_dir_test())

    @classmethod
    def list_from_prod(cls) -> list['GenericResult']:
        return cls.list_for_dir(cls.get_dir_prod())

    @classmethod
    def store_list_to_dir(
        cls, data_list: list['GenericResult'], dir_path: str
    ):
        shutil.rmtree(dir_path, ignore_errors=True)
        os.makedirs(dir_path, exist_ok=True)

        for data in data_list:
            json_file_path = os.path.join(dir_path, f'{data.code}.json')
            JSONFile(json_file_path).write(data.to_dict())
        log.info(f'Stored {len(data_list)} GenericResult to {dir_path}')

    @classmethod
    def store_list_to_json_compact(
        cls, data_list: list['GenericResult'], json_file_path: str
    ):
        JSONFile(json_file_path).write(
            [data.to_dict_compact() for data in data_list]
        )
        size_k = os.path.getsize(json_file_path) / 1000
        log.info(
            f'Wrote {len(data_list)} records to {json_file_path} ({size_k:.1f}KB)'
        )
