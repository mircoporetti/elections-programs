from enum import Enum


class Party(Enum):
    SPD = "SPD"
    CDU = "CDU"
    AFD = "AFD"
    FDP = "FDP"
    DL = "DL"
    DG = "DG"
    BSW = "BSW"

    @staticmethod
    def get_from_history(history):
        for message in reversed(history):
            if message["role"] != "AI":
                party = Party.get_from_message(message["content"])
                if party:
                    return party
        raise PartyNotFoundError("No party found in chat history")


    @staticmethod
    def get_from_message(message):
        for party in Party:
            if party.value.lower() in message.lower():
                return party
        return None



class PartyNotFoundError(Exception):
    def __init__(self, question):
        supported_parties = ", ".join([party.name for party in Party])
        self.question = question
        super().__init__(f"It was not possible to infer any supported political party from chat history. "
                         f"Please include one of the following: {supported_parties}")


def extract_party_from(question):
    for party in Party:
        if party.value.lower() in question.lower():
            return party
    raise PartyNotFoundError(question)
