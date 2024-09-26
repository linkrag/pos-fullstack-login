from sqlalchemy import Boolean, Column, Integer, DateTime, String, ForeignKey
from datetime import datetime

from model.Base import Base


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    deleted = Column(Boolean, default=False)
    nome = Column(String(200), nullable=False)
    username = Column(String(200), nullable=False)
    pwd = Column(String(200), nullable=False)
    cep = Column(String(200), nullable=False)
    logradouro = Column(String(200), nullable=False)
    complemento = Column(String(200), nullable=False)
    bairro = Column(String(200), nullable=False)
    localidade = Column(String(200), nullable=False)
    uf = Column(String(200), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    empresa_id = Column(Integer, ForeignKey("empresa.id"), nullable=False)