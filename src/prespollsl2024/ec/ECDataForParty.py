from dataclasses import dataclass


@dataclass
class ECDataForParty:
    party_code: str
    votes: int
    percentage: str
    party_name: str
    candidate: str

    def to_dict(self):
        return {
            "party_code": self.party_code,
            "votes": self.votes,
            "percentage": self.percentage,
            "party_name": self.party_name,
            "candidate": self.candidate,
        }

    @staticmethod
    def to_dict_compact(by_party):
        return {
            x.party_code: x.votes
            for x in sorted(by_party, key=lambda x: x.party_code)
        }

    def from_dict(d):
        return ECDataForParty(
            party_code=d["party_code"],
            votes=int(d["votes"]),
            percentage=float(d["percentage"]),
            party_name=d["party_name"],
            candidate=d["candidate"],
        )
