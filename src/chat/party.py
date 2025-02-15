from enum import Enum

from lingua.lingua import Language

from src.webapp.properties import Properties


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
        if Properties.user_lang == Language.GERMAN:
            message = f"Ups! Ich habe nicht verstanden, auf welche Partei sich Ihre Frage bezieht. " \
                    f"Bitte geben Sie eine der folgenden Parteien an: {supported_parties}"
        else:
            message = f"Oops! I did not understand which party your question is referring to. " \
                      f"Please include one of the following: {supported_parties}"
        super().__init__(message)


def extract_party_from(question):
    for party in Party:
        if party.value.lower() in question.lower():
            return party
    raise PartyNotFoundError(question)
