PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS signo (
    id_signo INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_signo VARCHAR(20) NOT NULL UNIQUE,
    simbolo VARCHAR(4) NOT NULL,
    dia_inicio INTEGER NOT NULL,
    mes_inicio INTEGER NOT NULL,
    dia_fim INTEGER NOT NULL,
    mes_fim INTEGER NOT NULL,
    elemento VARCHAR(10) NOT NULL,
    planeta_regente VARCHAR(20) NOT NULL,
    cor VARCHAR(10) NOT NULL,
    resumo TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(30) NOT NULL,
    data_nascimento DATE NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    data_cadastro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_signo INTEGER NOT NULL,
    FOREIGN KEY (id_signo) REFERENCES signo(id_signo)
);

CREATE TABLE IF NOT EXISTS caracteristica (
    id_caracteristica INTEGER PRIMARY KEY AUTOINCREMENT,
    id_signo INTEGER NOT NULL,
    descricao TEXT NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_signo) REFERENCES signo(id_signo) ON DELETE CASCADE
);
