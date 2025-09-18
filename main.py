from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import sqlite3
from models import iniciar_bd 

# TIPAGEM DOS DADOS DO LOGIN
class Dados(BaseModel):
    nome_usuario: str
    email_usuario: str
    senha_usuario: str

app = FastAPI()
iniciar_bd() 

def conectar_bd():
    conn = sqlite3.connect('auth-api.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def main():
    return "web-mobile-auth-api totalmente no ar!!"

# LOGIN
@app.post("/login/")
async def login(dados: Dados):
    conn = conectar_bd()
    user = conn.execute('SELECT * FROM usuario WHERE email_usuario = ? AND senha_usuario = ?', (dados.email_usuario, dados.senha_usuario)).fetchone()
    if user:
        return {'message': 'Login realizado com sucesso!'}
    else:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos!')

# CADASTRO
@app.post("/cadastro/")
async def cadastro(dados: Dados):
    conn = conectar_bd()
    try:
        usuario_existente = conn.execute('SELECT * FROM usuario WHERE email_usuario = ?', (dados.email_usuario,)).fetchone()
        if usuario_existente:
            raise HTTPException(status_code=409, detail='Email já cadastrado!')

        conn.execute('INSERT INTO usuario (nome_usuario, email_usuario, senha_usuario) VALUES (?, ?, ?)', (dados.nome_usuario, dados.email_usuario, dados.senha_usuario))
        conn.commit()
        return {'message': 'Usuário cadastrado com sucesso!'}
    except Exception as e:
        print(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail='Internal Server Error')

# SELECT DE TODOS OS USUARIOS
@app.get("/select/")
async def selectDadosUser():
    conn = conectar_bd()
    dados = conn.execute('SELECT * FROM usuario').fetchall()
    return [dict(item) for item in dados]

# SELECT DE TODAS AS NOTICIAS
@app.get("/select-noticias/")
async def selectDadosUser():
    conn = conectar_bd()
    dados = conn.execute('SELECT * FROM noticias').fetchall()
    return [dict(item) for item in dados]
