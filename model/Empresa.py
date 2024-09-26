from sqlalchemy import Boolean, Column, Integer, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime

from model.Base import Base
from model.Usuario import Usuario

class Empresa(Base):
    __tablename__ = 'empresa'
    
    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    nome = Column(String(200), nullable=False)
    cep = Column(String(200), nullable=False)
    logradouro = Column(String(200), nullable=False)
    complemento = Column(String(200), nullable=False)
    bairro = Column(String(200), nullable=False)
    localidade = Column(String(200), nullable=False)
    uf = Column(String(200), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    usuario = relationship("Usuario")


    def adiciona_usuario(self, usuario:Usuario):
        """ Adiciona um usuario à empresa
        """
        self.usuario.append(usuario)