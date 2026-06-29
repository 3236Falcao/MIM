# MIM — Mentor Inteligente Modular

MIM é um sistema local de memória reflexiva e uma prótese cognitiva pessoal. Ele registra experiências, decisões, aprendizados, memórias futuras e acontecimentos relevantes dos sistemas da vida.

Sua função é transformar observações em conhecimento acumulado: organizar experiências, identificar padrões e apoiar processos de aprendizagem, pesquisa e tomada de decisão.

> MIM é uma memória organizada que aprende com a experiência.

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
- [Linha do tempo do MIM](docs/LINHA_DO_TEMPO_MIM.md)
- [EcoSíntese: base metodológica](docs/ecosintese/ECOSINTESE_PEDAGOGIA_DOS_ECOSSISTEMAS.md)
- [Guia de Estudos EcoSíntese 2.0](docs/ecosintese/GUIA_DE_ESTUDOS_ECOSINTESE_2_0.md)
- [Programa de Pesquisa e Desenvolvimento da EcoSíntese](docs/ecosintese/PROGRAMA_DE_PESQUISA_E_DESENVOLVIMENTO.md)
- [Procedimento de Planejamento Pedagógico da EcoSíntese](docs/ecosintese/PROCEDIMENTO_PLANEJAMENTO_PEDAGOGICO.md)

## Privacidade

Este projeto é privado e contém dados pessoais. Não publique este repositório, os arquivos de `data/`, os relatórios ou qualquer conteúdo da inbox em ambientes públicos.
