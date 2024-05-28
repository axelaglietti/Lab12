from dataclasses import dataclass


@dataclass
class Retailer:
    Retailer_code: int
    Retailer_name: str
    Type: str
    Country: str
    volumeVendita: int

    def __hash__(self):
        return hash(self.Retailer_code)

    def __eq__(self, other):
        return self.Retailer_code == other.Retailer_code
