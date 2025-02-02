from enum import Enum


class Party(Enum):
    SPD = "SPD"
    CDU = "CDU"
    AFD = "AFD"
    FDP = "FDP"
    DL = "DL"
    DGR = "DGR"
    BSW = "BSW"

    @staticmethod
    def get_from(question):
        for party in Party:
            if party.value.lower() in question.lower():
                return party
        raise PartyNotFoundError(question)


class PartyNotFoundError(Exception):
    def __init__(self, question):
        supported_parties = ", ".join([party.name for party in Party])
        self.question = question
        super().__init__(f"The provided question '{question}' does not reference any supported political party. "
                         f"Please include one of the following: {supported_parties}")


def extract_party_from(question):
    for party in Party:
        if party.value.lower() in question.lower():
            return party
    raise PartyNotFoundError(question)
