from dataclasses import dataclass


@dataclass
class ECDataForParty:
    party_code: str
    votes: int
    percentage: str
    party_name: str
    candidate: str

    def from_dict(d):
        return ECDataForParty(
            party_code=d["party_code"],
            votes=int(d["votes"]),
            percentage=float(d["percentage"]),
            party_name=d["party_name"],
            candidate=d["candidate"],
        )
