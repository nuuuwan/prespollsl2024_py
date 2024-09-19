import os
from dataclasses import dataclass

from utils import Log

from prespollsl2024.ec.ForParty1 import ForParty1
from prespollsl2024.ec.GenericResult import GenericResult
from prespollsl2024.ec.Summary1 import Summary1

log = Log("PDResult1")


@dataclass
class PDResult1(GenericResult):
    timestamp: str
    level: str
    ed_code: str
    ed_name: str
    pd_code: str
    pd_name: str
    by_party: list[ForParty1]
    summary: Summary1
    type: str
    sequence_number: str
    reference: str



    @property
    def pd_id(self) -> str:
        return f'EC-{self.pd_code}'


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

    def to_dict_compact(self):
        return {
            "result_time": self.timestamp,
            "pd_id": self.pd_id,
            "party_to_votes": ForParty1.to_dict_compact(self.by_party),
            "summary": self.summary.to_dict_compact(),
        }


    # Loaders
    
    @classmethod
    def get_level(cls) -> str:
        return 'POLLING-DIVISION'
    
    @classmethod
    def get_type(cls) -> str:
        return 'PRESIDENTIAL-FIRST'
    
    @classmethod
    def get_dir_test(cls) -> str:
        return os.path.join('data', 'ec', 'test1')

    @classmethod
    def get_dir_prod(cls) -> str:
        return os.path.join('data', 'ec', 'prod1')

    @classmethod
    def from_dict(cls, d):
        return cls(
            timestamp=d["timestamp"],
            level=d["level"],
            ed_code=d["ed_code"],
            ed_name=d["ed_name"],
            pd_code=d["pd_code"],
            pd_name=d["pd_name"],
            by_party=[ForParty1.from_dict(x) for x in d["by_party"]],
            summary=Summary1.from_dict(d["summary"]),
            type=d["type"],
            sequence_number=d["sequence_number"],
            reference=d["reference"],
        )
