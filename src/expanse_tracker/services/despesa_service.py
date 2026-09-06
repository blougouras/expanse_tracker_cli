from models.despesa import Despesa
from repositories.despesa_repository import DespesaRepository
from exceptions.exceptions import DespesaNaoEncontradaError
from decimal import Decimal
from datetime import date

class DespesaService:
    def __init__(self, repositorio=None):
        self.repositorio = DespesaRepository() if repositorio is None else repositorio

    def _validar_dados(self, descricao, valor, data, categoria):
        if not descricao or not isinstance(descricao, str) or not descricao.strip():
            raise ValueError("Campo de descrição obrigatório")
        if not isinstance(valor, Decimal):
            raise TypeError("Campo de valor deve ser do tipo Decimal!")
        if valor <= 0:
            raise ValueError("Campo de valor deve ser maior que zero!")
        if not isinstance(data, date):
            raise TypeError("Data do tipo inválida!")
        if not categoria or not isinstance(categoria, str) or not categoria.strip():
            raise ValueError("Campo categoria obrigatório")

        return descricao.strip(), valor, data, categoria.strip()

    def adicionar(self, descricao, valor, data, categoria):
        descricao_validada, valor_validado, data_validada, categoria_validada = self._validar_dados(
            descricao, valor, data, categoria
        )
        despesas_existentes = self.repositorio.carregar_despesas()
        next_id = 1 if not despesas_existentes else max(despesa.id for despesa in despesas_existentes) + 1

        despesa = Despesa(
            id=next_id,
            descricao=descricao_validada,
            valor=valor_validado,
            data=data_validada,
            categoria=categoria_validada
        )

        despesas_existentes.append(despesa)
        self.repositorio.salvar_despesas(despesas=despesas_existentes)

    def atualizar(self, id, descricao=None, valor=None, data=None, categoria=None):
        despesas_existentes = self.repositorio.carregar_despesas()
        despesa_atual = None
        for despesa in despesas_existentes:
            if despesa.id == id:
                despesa_atual = despesa
                break

        if despesa_atual is None:
            raise DespesaNaoEncontradaError("ID de Despesa não Encontrado")

        descricao_a_usar = descricao if descricao is not None else despesa_atual.descricao
        valor_a_usar = valor if valor is not None else despesa_atual.valor
        data_a_usar = data if data is not None else despesa_atual.data
        categoria_a_usar = categoria if categoria is not None else despesa_atual.categoria

        descricao_validada, valor_validado, data_validada, categoria_validada = self._validar_dados(
            descricao=descricao_a_usar, valor=valor_a_usar, data=data_a_usar, categoria=categoria_a_usar
        )

        despesa_atual.descricao=descricao_validada
        despesa_atual.valor=valor_validado
        despesa_atual.data=data_validada
        despesa_atual.categoria=categoria_validada

        self.repositorio.salvar_despesas(despesas=despesas_existentes)
        
    def deletar(self, id):
        despesas_existentes = self.repositorio.carregar_despesas()
        despesa_atual = None
        for despesa in despesas_existentes:
            if despesa.id == id:
                despesa_atual = despesa
                break        

        if despesa_atual is None:
            raise DespesaNaoEncontradaError("ID de Despesa não Encontrado")

        despesas_existentes.remove(despesa_atual)
        self.repositorio.salvar_despesas(despesas=despesas_existentes)

    def listar(self):
        despesas_existentes = self.repositorio.carregar_despesas()
        return despesas_existentes

    def resumo_total(self):
        despesas_existentes = self.repositorio.carregar_despesas()
        return sum([despesa.valor for despesa in despesas_existentes], start=Decimal(0))

    def resumo_mensal(self, month):
        ano_atual = date.today().year
        despesas_existentes = self.repositorio.carregar_despesas()

        return sum([despesa.valor for despesa in despesas_existentes if despesa.data.month == month and despesa.data.year == ano_atual], start=Decimal(0))

