from tinydb import TinyDB, Query
from tinydb.storages import MemoryStorage

banco_de_dados = TinyDB(storage=MemoryStorage)

def buscar_livros():
    """Retorna todos os livro"""
    return banco_de_dados.all()

def buscar_livro(id):
    """Retorna o livro associado ao respectivo id passado na rota"""
    try:
        pessoa = banco_de_dados.search(Query().id == id)[0]
    except IndexError:
        return {'message': 'Livro não encontrado'}, 404
    return pessoa

def inserir_livro(livro):
    """Insere um livro no Banco de Dados"""
    banco_de_dados.insert(livro)
    return livro


def altera_livro(id, livro):
    """Altera os dados do livro a partir do ID"""
    banco_de_dados.update(livro, Query().id == id)
    return livro

def deleta_livro(id):
    """Deleta livros a partir do ID"""
    banco_de_dados.remove(Query().id == id)
    return {}

def deleta_livros():
    """Deleta todos os livros do Banco"""
    banco_de_dados.drop_tables()
    return {}