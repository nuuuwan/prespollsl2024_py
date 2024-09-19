from dataclasses import dataclass


@dataclass
class Summary2: # for 2nd Preference Counts
    total: int


    def to_dict(self):
        return {
            "total": self.total,
        }

    def to_dict_compact(self):
        return {
            "total": self.total,

        }

    def from_dict(d):
        return Summary2(
            valid=int(d["total"]),
        )
