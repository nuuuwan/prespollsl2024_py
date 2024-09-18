import os
from dataclasses import dataclass

from utils import JSONFile, Log, TSVFile

from prespollsl2024.ec.ECDataForParty import ECDataForParty
from prespollsl2024.ec.ECDataSummary import ECDataSummary

log = Log("ECJSONData")


@dataclass
class ECData:
    timestamp: str
    level: str
    ed_code: str
    ed_name: str
    pd_code: str
    pd_name: str
    by_party: list[ECDataForParty]
    summary: ECDataSummary
    type: str
    sequence_number: str
    reference: str

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "ed_code": self.ed_code,
            "ed_name": self.ed_name,
            "pd_code": self.pd_code,
            "pd_name": self.pd_name,
            "by_party": [x.to_dict() for x in self.by_party],
            "summary": self.summary.to_dict(),
            "type": self.type,
            "sequence_number": self.sequence_number,
            "reference": self.reference,
        }

    # Properties

    @property
    def pd_id(self) -> str:
        return f'EC-{self.pd_code}'

    # Loaders

    DIR_DATA_TEST = os.path.join('data', 'ec', 'test')
    DIR_DATA_PROD = os.path.join('data', 'ec', 'prod')

    @staticmethod
    def from_dict(d):
        return ECData(
            timestamp=d["timestamp"],
            level=d["level"],
            ed_code=d["ed_code"],
            ed_name=d["ed_name"],
            pd_code=d["pd_code"],
            pd_name=d["pd_name"],
            by_party=[ECDataForParty.from_dict(x) for x in d["by_party"]],
            summary=ECDataSummary.from_dict(d["summary"]),
            type=d["type"],
            sequence_number=d["sequence_number"],
            reference=d["reference"],
        )

    @staticmethod
    def from_file(json_file_path: str) -> 'ECData':
        d = JSONFile(json_file_path).read()
        ec_data = ECData.from_dict(d)
        log.debug(f'Loaded from {json_file_path}')
        return ec_data

    @staticmethod
    def list_for_dir(dir_path: str) -> list['ECData']:
        ec_data_list = []
        for file_name in os.listdir(dir_path):
            if not file_name.endswith(".json"):
                continue
            ec_data = ECData.from_file(os.path.join(dir_path, file_name))
            ec_data_list.append(ec_data)
        log.info(f'Loaded {len(ec_data_list)} ECData from {dir_path}')
        return ec_data_list

    @staticmethod
    def list_from_test() -> list['ECData']:
        return ECData.list_for_dir(ECData.DIR_DATA_TEST)

    @staticmethod
    def list_from_prod() -> list['ECData']:
        return ECData.list_for_dir(ECData.DIR_DATA_PROD)

    @staticmethod
    def build_tsv(ec_data_list: list['ECData'], tsv_file_path: str):
        data_list = []
        for ec_data in ec_data_list:
            if ec_data.level != 'POLLING-DIVISION':
                continue
            data = dict(
                entity_id=ec_data.pd_id,
                valid=ec_data.summary.valid,
                rejected=ec_data.summary.rejected,
                polled=ec_data.summary.polled,
                electors=ec_data.summary.electors,
            )

            for ec_data_for_party in ec_data.by_party:
                data[ec_data_for_party.party_code] = ec_data_for_party.votes

            data_list.append(data)
        TSVFile(tsv_file_path).write(data_list)
        log.info(f'Wrote {len(data_list)} records to {tsv_file_path}')

    @staticmethod
    def store_list_to_dir(ec_data_list: list['ECData'], dir_path: str):
        for ec_data in ec_data_list:
            json_file_path = os.path.join(dir_path, f'{ec_data.pd_code}.json')
            JSONFile(json_file_path).write(ec_data.to_dict())
            log.debug(f'Stored to {json_file_path}')
        log.info(f'Stored {len(ec_data_list)} ECData to {dir_path}')
