# API de usuários e controle de acesso

Este é um projeto de um webservice para uma empresa de petiscos para cães e MVP para o curso de **Desenvolvimento Full Stack** da PUC-RIO.

---

## Objetivo

O objetivo desse projeto é realizar o controle de acesso a aplicação Task Manager e armazenar Usuários e Empresas.

O usuários estão distribuídos de forma que existe uma empresa (tenant) e dentro dessa empresa vários usuários com acesso a mesma informação.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5002
```
Caso não tenha um ambiente virtual, pode ser executado diretamente utilizando o comando abaixo pelo terminal na pasta raiz: 

```
$ python app.py
```

Abra o [http://localhost:5002/#/](http://localhost:5002/#/) no navegador para verificar o status da API em execução.


## Como executar (Docker)

Basta realizar o comando `docker build -t login-app .`
Em seguida: `docker run -p 5002:5002 login-app`