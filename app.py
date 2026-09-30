from __future__ import annotations

import re
import sqlite3
from datetime import date, datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "signos.db"

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

SIGNOS = [
    {
        "nome": "Áries", "simbolo": "♈", "dia_inicio": 21, "mes_inicio": 3, "dia_fim": 19, "mes_fim": 4,
        "elemento": "Fogo", "planeta_regente": "Marte", "cor": "#ff6b6b",
        "resumo": "Energia, iniciativa e coragem para abrir caminhos.",
        "caracteristicas": [
            ("Força", "Corajoso e direto, costuma agir com muita iniciativa."),
            ("Força", "Competitivo, entusiasmado e cheio de energia."),
            ("Atenção", "Pode agir por impulso quando está sob pressão."),
        ],
    },
    {
        "nome": "Touro", "simbolo": "♉", "dia_inicio": 20, "mes_inicio": 4, "dia_fim": 20, "mes_fim": 5,
        "elemento": "Terra", "planeta_regente": "Vênus", "cor": "#66d9a0",
        "resumo": "Estabilidade, persistência e apreço pelo que traz conforto.",
        "caracteristicas": [
            ("Força", "Paciente, leal e consistente nas decisões."),
            ("Força", "Valoriza segurança, beleza e experiências sensoriais."),
            ("Atenção", "Pode resistir bastante a mudanças repentinas."),
        ],
    },
    {
        "nome": "Gêmeos", "simbolo": "♊", "dia_inicio": 21, "mes_inicio": 5, "dia_fim": 20, "mes_fim": 6,
        "elemento": "Ar", "planeta_regente": "Mercúrio", "cor": "#ffd166",
        "resumo": "Curiosidade, comunicação e rapidez para conectar ideias.",
        "caracteristicas": [
            ("Força", "Comunicativo, versátil e interessado por novidades."),
            ("Força", "Aprende rápido e gosta de trocar ideias."),
            ("Atenção", "Pode dispersar quando há estímulos demais ao mesmo tempo."),
        ],
    },
    {
        "nome": "Câncer", "simbolo": "♋", "dia_inicio": 21, "mes_inicio": 6, "dia_fim": 22, "mes_fim": 7,
        "elemento": "Água", "planeta_regente": "Lua", "cor": "#8ec5ff",
        "resumo": "Sensibilidade, proteção e conexão forte com afetos e memórias.",
        "caracteristicas": [
            ("Força", "Acolhedor, intuitivo e ligado às pessoas importantes."),
            ("Força", "Tem forte percepção emocional e senso de cuidado."),
            ("Atenção", "Pode se fechar quando se sente inseguro."),
        ],
    },
    {
        "nome": "Leão", "simbolo": "♌", "dia_inicio": 23, "mes_inicio": 7, "dia_fim": 22, "mes_fim": 8,
        "elemento": "Fogo", "planeta_regente": "Sol", "cor": "#ff9f43",
        "resumo": "Criatividade, presença e vontade de expressar o próprio brilho.",
        "caracteristicas": [
            ("Força", "Carismático, criativo e generoso com quem admira."),
            ("Força", "Gosta de liderar, criar e ser reconhecido pelo esforço."),
            ("Atenção", "Pode levar críticas para o lado pessoal."),
        ],
    },
    {
        "nome": "Virgem", "simbolo": "♍", "dia_inicio": 23, "mes_inicio": 8, "dia_fim": 22, "mes_fim": 9,
        "elemento": "Terra", "planeta_regente": "Mercúrio", "cor": "#9ad29a",
        "resumo": "Organização, análise e atenção aos detalhes que fazem diferença.",
        "caracteristicas": [
            ("Força", "Observador, responsável e atento aos detalhes."),
            ("Força", "Gosta de melhorar processos e tornar as coisas úteis."),
            ("Atenção", "Pode ser exigente demais consigo mesmo."),
        ],
    },
    {
        "nome": "Libra", "simbolo": "♎", "dia_inicio": 23, "mes_inicio": 9, "dia_fim": 22, "mes_fim": 10,
        "elemento": "Ar", "planeta_regente": "Vênus", "cor": "#d6a4ff",
        "resumo": "Equilíbrio, diplomacia e busca por harmonia nas relações.",
        "caracteristicas": [
            ("Força", "Diplomático, sociável e sensível à estética."),
            ("Força", "Busca justiça e tenta enxergar mais de um lado."),
            ("Atenção", "Pode demorar para decidir quando há muitas opções."),
        ],
    },
    {
        "nome": "Escorpião", "simbolo": "♏", "dia_inicio": 23, "mes_inicio": 10, "dia_fim": 21, "mes_fim": 11,
        "elemento": "Água", "planeta_regente": "Plutão", "cor": "#b25b6a",
        "resumo": "Intensidade, profundidade e capacidade de transformação.",
        "caracteristicas": [
            ("Força", "Intenso, estratégico e muito perceptivo."),
            ("Força", "Valoriza confiança, profundidade e vínculos verdadeiros."),
            ("Atenção", "Pode guardar ressentimentos por mais tempo."),
        ],
    },
    {
        "nome": "Sagitário", "simbolo": "♐", "dia_inicio": 22, "mes_inicio": 11, "dia_fim": 21, "mes_fim": 12,
        "elemento": "Fogo", "planeta_regente": "Júpiter", "cor": "#8b7cf6",
        "resumo": "Expansão, liberdade e entusiasmo por experiências novas.",
        "caracteristicas": [
            ("Força", "Otimista, aventureiro e aberto a novas ideias."),
            ("Força", "Gosta de aprender, viajar e ampliar horizontes."),
            ("Atenção", "Pode prometer mais do que consegue cumprir."),
        ],
    },
    {
        "nome": "Capricórnio", "simbolo": "♑", "dia_inicio": 22, "mes_inicio": 12, "dia_fim": 19, "mes_fim": 1,
        "elemento": "Terra", "planeta_regente": "Saturno", "cor": "#9c8f84",
        "resumo": "Disciplina, ambição e paciência para construir resultados sólidos.",
        "caracteristicas": [
            ("Força", "Disciplinado, estratégico e comprometido com objetivos."),
            ("Força", "Tem paciência para construir resultados de longo prazo."),
            ("Atenção", "Pode cobrar de si mesmo mais do que o necessário."),
        ],
    },
    {
        "nome": "Aquário", "simbolo": "♒", "dia_inicio": 20, "mes_inicio": 1, "dia_fim": 18, "mes_fim": 2,
        "elemento": "Ar", "planeta_regente": "Urano", "cor": "#61d4e8",
        "resumo": "Originalidade, independência e interesse por ideias de futuro.",
        "caracteristicas": [
            ("Força", "Original, independente e aberto a ideias diferentes."),
            ("Força", "Gosta de inovação, grupos e projetos com propósito."),
            ("Atenção", "Pode parecer distante quando precisa de espaço."),
        ],
    },
    {
        "nome": "Peixes", "simbolo": "♓", "dia_inicio": 19, "mes_inicio": 2, "dia_fim": 20, "mes_fim": 3,
        "elemento": "Água", "planeta_regente": "Netuno", "cor": "#6fa3ef",
        "resumo": "Imaginação, empatia e percepção sutil do ambiente e das pessoas.",
        "caracteristicas": [
            ("Força", "Sensível, imaginativo e empático."),
            ("Força", "Tem forte intuição e criatividade artística."),
            ("Atenção", "Pode evitar conflitos e adiar decisões difíceis."),
        ],
    },
]


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    with get_db() as conn:
        conn.executescript(
            """
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
            """
        )

        total = conn.execute("SELECT COUNT(*) AS qtd FROM signo").fetchone()["qtd"]
        if total == 0:
            for s in SIGNOS:
                cur = conn.execute(
                    """
                    INSERT INTO signo
                    (nome_signo, simbolo, dia_inicio, mes_inicio, dia_fim, mes_fim, elemento, planeta_regente, cor, resumo)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        s["nome"], s["simbolo"], s["dia_inicio"], s["mes_inicio"], s["dia_fim"], s["mes_fim"],
                        s["elemento"], s["planeta_regente"], s["cor"], s["resumo"],
                    ),
                )
                id_signo = cur.lastrowid
                conn.executemany(
                    "INSERT INTO caracteristica (id_signo, tipo, descricao) VALUES (?, ?, ?)",
                    [(id_signo, tipo, descricao) for tipo, descricao in s["caracteristicas"]],
                )


def data_no_intervalo(dia: int, mes: int, inicio_dia: int, inicio_mes: int, fim_dia: int, fim_mes: int) -> bool:
    atual = mes * 100 + dia
    inicio = inicio_mes * 100 + inicio_dia
    fim = fim_mes * 100 + fim_dia
    if inicio <= fim:
        return inicio <= atual <= fim
    return atual >= inicio or atual <= fim


def descobrir_signo(data_nascimento: date) -> sqlite3.Row | None:
    with get_db() as conn:
        signos = conn.execute("SELECT * FROM signo ORDER BY id_signo").fetchall()
        for signo in signos:
            if data_no_intervalo(
                data_nascimento.day,
                data_nascimento.month,
                signo["dia_inicio"],
                signo["mes_inicio"],
                signo["dia_fim"],
                signo["mes_fim"],
            ):
                return signo
    return None


def signo_completo(id_signo: int) -> dict | None:
    with get_db() as conn:
        signo = conn.execute("SELECT * FROM signo WHERE id_signo = ?", (id_signo,)).fetchone()
        if not signo:
            return None
        caracteristicas = conn.execute(
            "SELECT tipo, descricao FROM caracteristica WHERE id_signo = ? ORDER BY id_caracteristica",
            (id_signo,),
        ).fetchall()
    payload = dict(signo)
    payload["caracteristicas"] = [dict(c) for c in caracteristicas]
    return payload


def validar_email(email: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email))


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/signos")
def api_signos():
    with get_db() as conn:
        signos = conn.execute("SELECT * FROM signo ORDER BY id_signo").fetchall()
    return jsonify([dict(s) for s in signos])


@app.get("/api/signos/<int:id_signo>")
def api_signo(id_signo: int):
    signo = signo_completo(id_signo)
    if not signo:
        return jsonify({"erro": "Signo não encontrado."}), 404
    return jsonify(signo)


@app.post("/api/descobrir")
def api_descobrir():
    dados = request.get_json(silent=True) or request.form
    nome = str(dados.get("nome", "")).strip()
    email = str(dados.get("email", "")).strip().lower()
    data_texto = str(dados.get("data_nascimento", "")).strip()

    if len(nome) < 2 or len(nome) > 30:
        return jsonify({"erro": "Informe um nome entre 2 e 30 caracteres."}), 400
    if not validar_email(email):
        return jsonify({"erro": "Informe um e-mail válido."}), 400

    try:
        nascimento = datetime.strptime(data_texto, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"erro": "Data de nascimento inválida."}), 400

    hoje = date.today()
    if nascimento > hoje:
        return jsonify({"erro": "A data de nascimento não pode estar no futuro."}), 400
    if nascimento.year < 1900:
        return jsonify({"erro": "Use uma data de nascimento a partir de 1900."}), 400

    signo = descobrir_signo(nascimento)
    if not signo:
        return jsonify({"erro": "Não foi possível identificar o signo."}), 500

    with get_db() as conn:
        existente = conn.execute("SELECT id_usuario FROM usuario WHERE email = ?", (email,)).fetchone()
        if existente:
            conn.execute(
                """
                UPDATE usuario
                SET nome = ?, data_nascimento = ?, id_signo = ?, data_cadastro = CURRENT_TIMESTAMP
                WHERE email = ?
                """,
                (nome, nascimento.isoformat(), signo["id_signo"], email),
            )
        else:
            conn.execute(
                "INSERT INTO usuario (nome, data_nascimento, email, id_signo) VALUES (?, ?, ?, ?)",
                (nome, nascimento.isoformat(), email, signo["id_signo"]),
            )

    resultado = signo_completo(signo["id_signo"])
    resultado["usuario"] = {"nome": nome, "data_nascimento": nascimento.isoformat()}
    return jsonify(resultado)


@app.get("/api/estatisticas")
def api_estatisticas():
    with get_db() as conn:
        total_usuarios = conn.execute("SELECT COUNT(*) AS qtd FROM usuario").fetchone()["qtd"]
        distribuicao = conn.execute(
            """
            SELECT s.nome_signo, s.simbolo, COUNT(u.id_usuario) AS total
            FROM signo s
            LEFT JOIN usuario u ON u.id_signo = s.id_signo
            GROUP BY s.id_signo
            ORDER BY total DESC, s.id_signo
            """
        ).fetchall()
    return jsonify({"total_usuarios": total_usuarios, "distribuicao": [dict(r) for r in distribuicao]})


init_db()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
