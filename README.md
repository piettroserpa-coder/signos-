# AstroSign — Descobrir Signos

Projeto full stack inspirado no diagrama da lousa: **usuário**, **signo** e **característica**, com relacionamento por chave estrangeira.

## Tecnologias
- Python + Flask
- SQLite
- HTML5
- CSS3
- JavaScript

## Estrutura
```text
astro-signos/
├── app.py
├── requirements.txt
├── signos.db              # criado automaticamente na primeira execução
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── app.js
```

## Rodar no Windows / VS Code
1. Abra a pasta no VS Code.
2. Abra o Terminal.
3. Crie o ambiente virtual:
   ```powershell
   py -m venv .venv
   ```
4. Ative:
   ```powershell
   .venv\Scripts\Activate.ps1
   ```
5. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```
6. Execute:
   ```powershell
   py app.py
   ```
7. Abra `http://127.0.0.1:5000` no navegador.

## Banco de dados
O arquivo `signos.db` é criado automaticamente. O sistema também cadastra os 12 signos e suas características na primeira execução.

### Tabelas
- `usuario`: id, nome, data de nascimento, e-mail, data de cadastro e `id_signo`.
- `signo`: nome, datas de início/fim, elemento, planeta regente, símbolo, cor e resumo.
- `caracteristica`: tipo e descrição ligados ao signo por `id_signo`.

## APIs
- `GET /api/signos`
- `GET /api/signos/<id>`
- `POST /api/descobrir`
- `GET /api/estatisticas`
