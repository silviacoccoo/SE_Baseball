from dataclasses import dataclass
@dataclass
class Team:
    year: int
    id: int
    team_code: str
    name: str

    def __str__(self):
        return self.team_code

    def __repr__(self):
        return self.team_code

    def __hash__(self):
        return hash(self.id)