from pydantic import BaseModel
from datetime import datetime

from model.Usuario import Usuario


class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido deve ser representado
    """
    nome: str = "Fulano da Silva"
    username: str = "fulano"
    pwd: str = "23RR4-235VGB-4R34TT23G"
    cep: str = "01001-000"
    logradouro: str = "Praça da Sé"
    complemento: str = "lado ímpar"
    bairro: str = "Sé"
    localidade: str = "São Paulo"
    uf: str = "SP"
    empresa_id: int = 1


class UsuarioViewSchema(BaseModel):
    """ Define como um usuario deve ser apresentado
    """
    id: int = 1
    deleted: int = 1
    nome: str = "Fulano da Silva"
    username: str = "fulano"
    cep: str = "01001-000"
    logradouro: str = "Praça da Sé"
    complemento: str = "lado ímpar"
    bairro: str = "Sé"
    localidade: str = "São Paulo"
    uf: str = "SP"
    empresa_id: int = 1
    data_criacao: datetime = "dd/MM/yyyy"
    
    
class UsuarioPathSchema(BaseModel):
    """ Define como um usuário deverá ser buscado.
    """
    usuario_id: int = 0


class UsuarioQueryBuscaSchema(BaseModel):
    """ Define como um usuário deverá ser buscado.
    """
    usuario_id: int = 0
    empresa_id: int = 0
    nome: str = "Fulano da Silva"


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    id: int = 1
    nome: str
    mesage: str


class AuthViewSchema(BaseModel):
    """ Define como a autenticação é realizada.
    """
    token: str = "JTW TOKEN"


class AuthSchema(BaseModel):
    """ Define como a autenticação é realizada.
    """
    username: str = "fulano"
    pwd: str = "SHA256 HASH"
    
    
def apresenta_usuario(usuario: Usuario):
    """ Retorna uma representação de um usuário seguindo o schema definido em
        UsuarioViewSchema.
    """
    mascara = "%d/%m/%Y %H:%M:%S"

    return {
        "id": usuario.id,
        "deleted": usuario.deleted,
        "nome": usuario.nome,
        "username": usuario.username,
        "cep": usuario.cep,
        "logradouro": usuario.logradouro,
        "complemento": usuario.complemento,
        "bairro": usuario.bairro,
        "localidade": usuario.localidade,
        "uf": usuario.uf,
        "empresa_id": usuario.empresa_id,
        "data_criacao": usuario.create_time.strftime(mascara),
    }
    
    
def apresenta_token(token):
    """ Retorna uma representação de um token seguindo o schema definido em
        AuthSchema.
    """
    mascara = "%d/%m/%Y %H:%M:%S"

    return {
        "token": token
    }