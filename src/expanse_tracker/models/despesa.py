from dataclasses import dataclass
from decimal import Decimal
from datetime import date

@dataclass
class Despesa:
    id: int
    descricao: str
    valor: Decimal
    data: date
    categoria: str
