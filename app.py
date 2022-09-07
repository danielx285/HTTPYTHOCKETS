from itertools import count
from typing import Optional
from flask import Flask, request, jsonify
from flask_pydantic_spec import (
    FlaskPydanticSpec, Response, Request
)
from pydantic import BaseModel, Field
from tinydb import TinyDB, Query

server = Flask(__name__)
spec = FlaskPydanticSpec('flask', title='Cadastrário de Livros')
spec.register(server)
database = TinyDB('database.json')
id_count = count()

class QueryLivro(BaseModel):
    id: Optional[int]
    titulo: Optional[str]
    preco: Optional[int]

class Livro(BaseModel):
    id: Optional[int] = Field(default_factory=lambda: next(id_count))
    titulo: str
    preco: int

class Livros(BaseModel):
    livros:  list
    quantidade: int


@server.get('/livros')
@spec.validate(
    query=QueryLivro,
    resp=Response(HTTP_200=Livros))
def buscar_livros():
    """Retorna os livro que derem match com os parametros inseridos"""
    query = request.context.query.dict(exclude_none=True)
    todos_os_livros = database.search(
        Query().fragment(query)
    )
    return jsonify(
        Livros(
            livros=todos_os_livros,
            quantidade=len(todos_os_livros)
        ).dict()
    )


@server.get('/livro/<int:id>')
@spec.validate(resp=Response(HTTP_200=Livro))
def buscar_livro(id):
    """Retorna o livro associado ao respectivo id passado na rota"""
    try:
        pessoa = database.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Livro não encontrado'}, 404
    return jsonify(pessoa)


@server.post('/livros')
@spec.validate(
    body=Request(Livro), resp=Response(HTTP_201=Livro)
)
def inserir_livro():
    """Insere um livro no Banco de Dados"""
    body = request.context.body.dict()
    database.insert(body)
    return body


@server.put('/livros/<int:id>')
@spec.validate(
    body=Request(Livro), resp=Response(HTTP_201=Livro)
)
def altera_livro(id):
    """Altera os dados do livro a partir do ID"""
    Livro = Query()
    body = request.context.body.dict()
    database.update(body, Livro.id == id)
    return jsonify(body)


@server.delete('/livros/<int:id>')
@spec.validate(resp=Response('HTTP_204'))
def deleta_livro(id):
    """Deleta livros a partir do ID"""
    database.remove(Query().id == id)
    return jsonify({})


@server.delete('/livros')
@spec.validate(resp=Response('HTTP_204'))
def deleta_livros():
    """Deleta todos os livros do Banco"""
    database.drop_tables()
    return jsonify({})

server.run()