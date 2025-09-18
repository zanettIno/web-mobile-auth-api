import sqlite3

dados_noticias = [
    ('O sucesso de Bohemian Rhapsody no cinema', 'O filme Bohemian Rhapsody, que conta a história de Freddie Mercury e da banda Queen, se tornou uma das cinebiografias musicais de maior sucesso de todos os tempos. Lançado em 2018, o longa-metragem não só conquistou o público, mas também a crítica, garantindo quatro estatuetas do Oscar, incluindo a de Melhor Ator para Rami Malek, que interpretou Freddie. O sucesso do filme gerou um interesse renovado pela música do Queen e pela história da banda.'),
    ('Depeche Mode: Lançamento de Memento Mori e turnê mundial', 'A banda britânica lançou o aclamado álbum Memento Mori, o primeiro sem o tecladista Andy Fletcher, que faleceu em 2022. Com o novo trabalho, o grupo embarcou em uma turnê mundial que tem lotado arenas e levado os clássicos da banda a fãs do mundo todo, celebrando sua longeva carreira.'),
    ('Vida Reluz: Lançamento de novo single e projeto comemorativo', 'O grupo católico está celebrando mais de 30 anos de estrada e, para comemorar, lançou um novo single, "Gratidão". Além disso, a banda anunciou um projeto especial para revisitar grandes sucessos da carreira, com regravações e parcerias com outros artistas da música católica.'),
]

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

    # CRIACAO DE TABELA DE NOTICIAS
    c.execute('''
        CREATE TABLE IF NOT EXISTS noticias (
            id_noticias      INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo_noticias    TEXT NOT NULL,
            conteudo_noticias   TEXT NOT NULL
        ''')

    c.execute('''
        DELETE FROM noticias
        ''')

    c.executemany('''
        INSERT INTO noticias (titulo_noticias, conteudo_noticias)
        VALUES (?, ?)
        ''', dados_noticias)

    conn.commit()
    conn.close()