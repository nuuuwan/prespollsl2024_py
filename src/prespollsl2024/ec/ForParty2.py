from dataclasses import dataclass


@dataclass
class ForParty2:
    party_code: str
    preferences: int
    party_name: str
    candidate: str

    def to_dict(self):
        return {
            "party_code": self.party_code,
            "preferences": self.votes,
            "party_name": self.party_name,
            "candidate": self.candidate,
        }

    @staticmethod
    def to_dict_compact(by_party):
        return {
            x.party_code: x.preferences
            for x in sorted(by_party, key=lambda x: x.party_code)
        }

    def from_dict(d):
        return ForParty2(
            party_code=d["party_code"],
            preferences=int(d["preferences"]),
            party_name=d["party_name"],
            candidate=d["candidate"],
        )
