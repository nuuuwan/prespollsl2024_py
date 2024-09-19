import os
from dataclasses import dataclass

from utils import Log

from prespollsl2024.ec.ForParty2 import ForParty2
from prespollsl2024.ec.GenericResult import GenericResult
from prespollsl2024.ec.Summary2 import Summary2

log = Log("EDResult2")


@dataclass
class EDResult2(GenericResult):
    timestamp: str
    level: str
    ed_code: str
    ed_name: str

    by_party: list[ForParty2]
    summary: Summary2

    type: str
    sequence_number: str
    reference: str

    @property
    def ed_id(self) -> str:
        return f'EC-{self.ed_code}'

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "level": self.level,
            "ed_code": self.ed_code,
            "ed_name": self.ed_name,
            "by_party": [x.to_dict() for x in self.by_party],
            "summary": self.summary.to_dict(),
            "type": self.type,
            "sequence_number": self.sequence_number,
            "reference": self.reference,
        }

    def to_dict_compact(self):
        return {
            "result_time": self.timestamp,
            "ed_id": self.ed_id,
            "party_to_votes": ForParty2.to_dict_compact(self.by_party),
            "summary": self.summary.to_dict_compact(),
        }

    # Loaders

    @classmethod
    def get_level(cls) -> str:
        return 'ELECTORAL-DISTRICT'

    @classmethod
    def get_type(cls) -> str:
        return 'PRESIDENTIAL-SECOND'

    @classmethod
    def get_dir_test(cls) -> str:
        return os.path.join('data', 'ec', 'test2')

    @classmethod
    def get_dir_prod(cls) -> str:
        return os.path.join('data', 'ec', 'prod2')

    @staticmethod
    def from_dict(d):
        return EDResult2(
            timestamp=d["timestamp"],
            level=d["level"],
            ed_code=d["ed_code"],
            ed_name=d["ed_name"],
            by_party=[ForParty2.from_dict(x) for x in d["by_party"]],
            summary=Summary2.from_dict(d["summary"]),
            type=d["type"],
            sequence_number=d["sequence_number"],
            reference=d["reference"],
        )
