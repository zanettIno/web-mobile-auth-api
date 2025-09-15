import sqlite3

def iniciar_bd():
    conn = sqlite3.connect('auth-api.db')
    c = conn.cursor()

    # CRIACAO DE TABELA DE USUARIO  
    c.execute('''
        CREATE TABLE IF NOT EXISTS usuario (
            id_usuario      INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario    TEXT NOT NULL,
            email_usuario   TEXT NOT NULL UNIQUE,
            senha_usuario   TEXT NOT NULL)
        ''')

    c.execute('''
        DELETE FROM usuario
    ''')

    conn.commit()
    conn.close()