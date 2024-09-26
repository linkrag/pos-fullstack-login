from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, jsonify, request
import jwt
import hashlib
from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError

from model import Session, Empresa, Usuario
from logger import logger
from schemas.erro import *
from schemas.empresa import *
from schemas.usuario import *    
from flask_cors import CORS


info = Info(title="API Empresa de Produção", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
empresa_tag = Tag(name="Empresa ", description="Adição, visualização e remoção de uma empresa ")
usuario_tag = Tag(name="Usuario", description="Adição e remoção de usuarios à empresa ")
auth_tag = Tag(name="Authentication", description="Endpoints for user authentication")

SECRET_KEY = 'secret'


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.get('/empresa/<int:empresa_id>', tags=[empresa_tag],
           responses={"200": EmpresaListViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_ordens(path: EmpresaBuscaSchema):
    """Faz uma busca pelo ID informado no path ou pelo default 0
    
    Retorna todas as ordens  cadastradas, se o ID enviado for 0 (default), ou a empresa  do ID enviado.
    """
    try:
        session = Session()
        #verifica o ID enviado
        if path.empresa_id != 0:
            ordens = session.query(Empresa).filter(Empresa.id == path.empresa_id)
        else:
            ordens = session.query(Empresa).filter(Empresa.deleted == False)
        result = apresenta_ordens(ordens)
        session.close()
        return jsonify(result), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao consultar a empresa  {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao consultar a empresa  {e.args}")
        return {"mesage": e.args}, 400
    
    
@app.post('/empresa', tags=[empresa_tag],
           responses={"200": EmpresaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_order(body: EmpresaSchema):
    """Cria uma nova empresa  com os usuarios enviados
    
    Retorna uma representação da empresa  com os usuarios associados.
    """
    logger.debug("Criando nova empresa ")
    empresa = Empresa()
    try:
        for usuario in body.usuarios:
            novo_usuario = Usuario(nome=usuario.nome, quantidade=usuario.quantidade)
            usuario_existente = False

            # Verificar se o usuario já está na empresa
            for usuario_empresa in empresa.usuarios:
                if usuario_empresa.nome == novo_usuario.nome:
                    # Se o usuario já estiver na empresa, apenas somar a quantidade
                    usuario_empresa.quantidade += novo_usuario.quantidade
                    usuario_existente = True
                    break
            
            # Se o usuario não estiver na empresa, adicione-o
            if not usuario_existente:
                empresa.usuarios.append(novo_usuario)
        session = Session()
        session.add(empresa)
        session.commit()
        return apresenta_empresa(empresa), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao criar empresa  {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao criar empresa  {e.args}")
        return {"mesage": e.args}, 400


@app.delete('/empresa/<int:empresa_id>', tags=[empresa_tag],
            responses={"200": EmpresaDelSchema, "404": ErrorSchema})
def delete_empresa(path: EmpresaBuscaSchema):
    """Deleta uma empresa  a partir de um ID informado no path

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        logger.debug(f"Deletando a empresa  #{path.empresa_id}")
        session = Session()
        empresa = session.query(Empresa).filter(Empresa.id == path.empresa_id).first()
        empresa.deleted = True
        session.commit()
        return {"mesage": "Empresa removida", "id": path.empresa_id}
        
    except IntegrityError as e:
        logger.warning(f"Erro ao excluir a empresa  {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao excluir a empresa  {e.args}")
        return {"mesage": e.args}, 400
    
    
@app.get('/usuario/<int:usuario_id>', tags=[usuario_tag],
            responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def get_usuario(path: UsuarioPathSchema):
    """Deleta um usuário a partir de um ID informado no path

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        session = Session()
        #verifica o ID enviado
        if path.usuario_id != 0:
            usuario = session.query(Usuario).filter(Usuario.id == path.usuario_id).first()
        result = apresenta_usuario(usuario)
        session.close()
        return jsonify(result), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao consultar o usuário  {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao consultar o usuário  {e.args}")
        return {"mesage": e.args}, 400


@app.put('/usuario', tags=[usuario_tag],
         responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def create_usuario(body: UsuarioSchema):
    """Cria um novo usuário com os dados enviados.
    
    A senha é armazenada como um hash SHA256.
    """
    logger.debug("Criando um novo usuário")
    novo_usuario = Usuario()
    try:
        session = Session()

        novo_usuario = Usuario(nome=body.nome, 
                               username=body.username,
                               pwd=body.pwd,  # Store the hashed password
                               cep=body.cep,
                               logradouro=body.logradouro,
                               complemento=body.complemento,
                               bairro=body.bairro,
                               localidade=body.localidade,
                               uf=body.uf,
                               empresa_id=body.empresa_id)

        # Verificar se o usuario já existe
        usuario_existente = session.query(Usuario).filter(Usuario.username == body.username).first()

        if usuario_existente:
            return {"message": "Usuário já existe."}, 409

        # Adiciona o novo usuário
        session.add(novo_usuario)
        session.commit()
        return apresenta_usuario(novo_usuario), 200

    except IntegrityError as e:
        logger.warning(f"Erro ao criar um novo usuário {e.args}")
        return {"message": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao criar um novo usuário {e.args}")
        return {"message": e.args}, 400
    
    
@app.delete('/usuario/<int:usuario_id>', tags=[usuario_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})
def delete_usuario(path: UsuarioPathSchema):
    """Deleta um usuário a partir de um ID informado no path

    Retorna uma mensagem de confirmação da remoção.
    """
    try:
        logger.debug(f"Deletando usuário #{path.usuario_id}")
        session = Session()
        usuario = session.query(Usuario).filter(Usuario.id == path.usuario_id).first()
        usuario.deleted = True
        session.commit()
        return {"mesage": "Usuário removido", "id": path.usuario_id}
        
    except IntegrityError as e:
        logger.warning(f"Erro ao excluir o usuário  {e.args}")
        return {"mesage": e.args}, 409

    except Exception as e:
        logger.warning(f"Erro ao excluir o usuário  {e.args}")
        return {"mesage": e.args}, 400


@app.post('/login', tags=[auth_tag])
def login():
    """
    User login to generate JWT token.
    A senha enviada é comparada com o hash SHA256 armazenado.
    """
    auth_data = request.json
    username = auth_data.get("username")
    password = auth_data.get("password")

    # Find user in the database
    session = Session()
    user = session.query(Usuario).filter(Usuario.username == username).first()

    if user:
        # Compare the hashed password with the stored password
        if user.pwd == password:
            # Generate JWT token with expiration of 1 hour
            token = jwt.encode({
                'id': user.id,
                'username': user.username,
                'exp': datetime.utcnow() + timedelta(hours=1)  # Correct use of timedelta
            }, SECRET_KEY, algorithm="HS256")

            # Ensure the token is returned as a string (decode if necessary)
            return jsonify({'token': token if isinstance(token, str) else token.decode('utf-8')}), 200

    return jsonify({'message': 'Invalid credentials'}), 401
    

if __name__ == '__main__':  
   app.run(host='0.0.0.0', port=5002)