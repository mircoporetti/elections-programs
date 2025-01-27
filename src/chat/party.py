from enum import Enum


class Party(Enum):
    SPD = "SPD"
    CDU = "CDU"
    AFD = "AFD"
    FDP = "FDP"
    DL = "DL"
    DGR = "DGR"


class PartyNotFoundError(Exception):
    def __init__(self, question):
        supported_parties = ", ".join([party.name for party in Party])
        self.question = question
        super().__init__(f"The provided question '{question}' does not reference any supported political party. "
                         f"Please include one of the following: {supported_parties}")

