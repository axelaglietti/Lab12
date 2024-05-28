from dataclasses import dataclass
from model.retailer import Retailer


@dataclass
class Connessione:
    v0: Retailer
    v1: Retailer
    peso: int

    def __hash__(self):
        return hash((self.v0, self.v1))

    def __eq__(self, other):
        return self.v0, self.v1 == other.v0, other.v1
