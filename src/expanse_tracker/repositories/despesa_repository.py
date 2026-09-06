import json
from decimal import Decimal
from datetime import date
from pathlib import Path
from models.despesa import Despesa

class DespesaRepository:
    def __init__(self, caminho="src/expanse_tracker/data/despesas.json"):
        self.caminho = Path(caminho)

    def _serializar(self, despesa): # Método interno da classe
        dados_despesa = {
            "id": despesa.id,
            "descricao": despesa.descricao,
            "valor": str(despesa.valor),
            "data": despesa.data.strftime("%Y-%m-%d"),
            "categoria": despesa.categoria
        }
        return dados_despesa

    def _desserializar(self, dados_json): # Método interno da classe
        despesa = Despesa(
            id=dados_json["id"],
            descricao=dados_json["descricao"],
            valor=Decimal(dados_json["valor"]),
            data=date.fromisoformat(dados_json["data"]),
            categoria=dados_json["categoria"]
        )
        return despesa

    def carregar_despesas(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo_json:
                despesas_json = json.load(arquivo_json)
                despesas = [self._desserializar(despesa) for despesa in despesas_json]
                return despesas
        except FileNotFoundError:
            return []

    def salvar_despesas(self, despesas):
        despesas_json = [self._serializar(despesa) for despesa in despesas]
        with open(self.caminho, "w", encoding="utf-8") as arquivo_json:
            json.dump(despesas_json, arquivo_json, indent=4, ensure_ascii=False)