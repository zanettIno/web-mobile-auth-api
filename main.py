from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
from models import iniciar_bd 

# TIPAGEM DOS DADOS DO USUÁRIO
class DadosUser(BaseModel):
    nome_usuario: str
    email_usuario: str
    senha_usuario: str

# TIPAGEM DOS DADOS DAS NOTÍCIAS
class DadosNoti(BaseModel):
    id_noticias: int
    titulo_noticias: str
    conteudo_noticias: str

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
iniciar_bd() 

def conectar_bd():
    conn = sqlite3.connect('auth-api.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
async def main():
    return "web-mobile-auth-api totalmente no ar!!"

# LOGIN DO USUÁRIO
@app.post("/login-usuario/")
async def loginUser(dados: DadosUser):
    conn = conectar_bd()
    user = conn.execute('SELECT * FROM usuario WHERE email_usuario = ? AND senha_usuario = ?', (dados.email_usuario, dados.senha_usuario)).fetchone()
    if user:
        return {'message': 'Login realizado com sucesso!'}
    else:
        raise HTTPException(status_code=401, detail='Email ou senha incorretos!')

# CADASTRO DO USUÁRIO
@app.post("/cadastro-usuario/")
async def cadastroUser(dados: DadosUser):
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

# CADASTRO DAS NOTÍCIAS
@app.post("/cadastro-noticias/")
async def cadastroNoti(dados: DadosNoti):
    conn = conectar_bd()
    cursor = conn.cursor()
    conn.execute('INSERT INTO noticias (titulo_noticias, conteudo_noticias) VALUES (?, ?)', (dados.titulo_noticias, dados.conteudo_noticias))
    cursor.execute('SELECT last_insert_rowid()')
    novo_id = cursor.fetchone()[0]
    conn.commit()
    return {'message': 'Notícia postada com sucesso!',
            "id_noticias": novo_id,
            "titulo_noticias": dados.titulo_noticias,
            "conteudo_noticias": dados.conteudo_noticias}

# EDIÇÃO DAS NOTÍCIAS
@app.post("/update-noticias/")
async def edicaoNoti(dados: DadosNoti):
    conn = conectar_bd()
    conn.execute('UPDATE noticias SET titulo_noticias = ?, conteudo_noticias = ? WHERE id_noticias = ?', (dados.titulo_noticias, dados.conteudo_noticias, dados.id_noticias))
    conn.commit()
    return {'message': 'Notícia atualizada com sucesso!'}

# SELECT DE TODAS AS NOTICIAS
@app.get("/select-noticias/")
async def selectDadosNoti():
    conn = conectar_bd()
    dados = conn.execute('SELECT * FROM noticias').fetchall()
    return [dict(item) for item in dados]
