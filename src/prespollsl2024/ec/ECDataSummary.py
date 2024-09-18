from dataclasses import dataclass


@dataclass
class ECDataSummary:
    valid: int
    rejected: int
    polled: int
    electors: int
    percent_valid: float
    percent_rejected: float
    percent_polled: float

    def to_dict(self):
        return {
            "valid": self.valid,
            "rejected": self.rejected,
            "polled": self.polled,
            "electors": self.electors,
            "percent_valid": self.percent_valid,
            "percent_rejected": self.percent_rejected,
            "percent_polled": self.percent_polled,
        }
    
    def to_dict_compact(self):
        return {
            "valid": self.valid,
            "rejected": self.rejected,
            "polled": self.polled,
            "electors": self.electors,
        }

    def from_dict(d):
        return ECDataSummary(
            valid=int(d["valid"]),
            rejected=int(d["rejected"]),
            polled=int(d["polled"]),
            electors=int(d["electors"]),
            percent_valid=float(d["percent_valid"]),
            percent_rejected=float(d["percent_rejected"]),
            percent_polled=float(d["percent_polled"]),
        )
