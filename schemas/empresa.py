from pydantic import BaseModel
from typing import List
from model.Empresa import Empresa
from datetime import datetime

from schemas.usuario import *

class EmpresaSchema(BaseModel):
    """ Define como uma nova empresa inserida deve ser representada
    """
    nome: str = "Empresa 1"
    cep: str = "01001-000"
    logradouro: str = "Praça da Sé"
    complemento: str = "lado ímpar"
    bairro: str = "Sé"
    localidade: str = "São Paulo"
    uf: str = "SP"


class EmpresaBuscaSchema(BaseModel):
    """ Define como uma empresa deverá ser buscada.
    """
    empresa_id: int = 0


class EmpresaViewSchema(BaseModel):
    """ Define como uma empresa deverá ser representada.
    """
    id: int = 1
    nome: str = "Empresa 1"
    cep: str = "01001-000"
    logradouro: str = "Praça da Sé"
    complemento: str = "lado ímpar"
    bairro: str = "Sé"
    localidade: str = "São Paulo"
    uf: str = "SP"
    data_criacao: datetime = "dd/MM/yyyy"
    usuarios: List[UsuarioSchema]


class EmpresaListViewSchema(BaseModel):
    """ Define como uma lista de empresas deverá ser representada.
    """
    empresas: List[EmpresaViewSchema]


class EmpresaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    id: int = 1
    nome: str
    mesage: str


def apresenta_empresa(empresa: Empresa):
    """ Retorna uma representação da empresa seguindo o schema definido em
        EmpresaViewSchema.
    """


    mascara = "%d/%m/%Y %H:%M:%S"

    return {
        "id": empresa.id,
        "data_criacao": empresa.create_time.strftime(mascara),
        "usuarios": [{"nome": p.nome, "cep": p.cep} for p in empresa.usuarios]
    }


def apresenta_ordens(ordens: List[Empresa]):
    """ Retorna uma representação de um conjunto de ordens seguindo o schema definido em
        EmpresaListViewSchema.
    """
    
    
    mascara = "%d/%m/%Y %H:%M:%S"
    
    return {
        "ordens": [{
                "id": o.id,
                    "data_criacao": o.create_time.strftime(mascara),
                    "usuarios": [{"nome": p.nome,"cep": p.cep} for p in o.usuarios]} for o in ordens]
    }