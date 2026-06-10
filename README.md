# MIM

MIM é um diário inteligente local e uma prótese cognitiva pessoal. Ele registra experiências, decisões, aprendizados, memórias futuras e acontecimentos relevantes dos sistemas da vida.

A proposta do MIM é ajudar a observar, interpretar, decidir, agir e memorizar com mais continuidade, mantendo os dados localmente em JSON.

Versão atual: **v0.4**

## Como Executar

Na raiz do projeto:

```bash
python3 main.py
```

## Como Rodar os Testes

```bash
python3 -m unittest discover -s tests
```

## Estrutura do Projeto

```text
mim/
├── main.py
├── data/
│   └── registros.json
├── inbox/
│   ├── inbox.txt
│   └── modelos.txt
├── reports/
│   └── relatorio_diario.txt
├── tests/
│   └── test_main.py
├── docs/
│   ├── MANUAL_MIM.md
│   ├── ARQUITETURA.md
│   ├── VISAO.md
│   ├── ROADMAP.md
│   ├── CHANGELOG.md
│   └── DESCOBERTAS.md
└── README.md
```

## Documentação

- [Manual de uso](docs/MANUAL_MIM.md)
- [Arquitetura técnica](docs/ARQUITETURA.md)
- [Visão conceitual](docs/VISAO.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)
- [Descobertas](docs/DESCOBERTAS.md)

## Privacidade

Este projeto é privado e contém dados pessoais. Não publique este repositório, os arquivos de `data/`, os relatórios ou qualquer conteúdo da inbox em ambientes públicos.
