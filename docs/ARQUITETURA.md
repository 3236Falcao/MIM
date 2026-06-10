# Arquitetura do MIM v0.4

Este documento descreve a estrutura técnica atual do MIM.

## Pastas e Arquivos

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

## Arquivo Principal

`main.py` concentra a implementação atual:

- constantes de sistemas e tipos
- carga e gravação de JSON
- criação de registros de diário
- criação de experiências
- processamento da inbox
- formatação de registros
- geração de relatório diário
- menu interativo

## Fluxo de Dados

### Registro pelo Menu

1. O usuário executa `python3 main.py`.
2. O menu coleta dados pelo terminal.
3. O registro é validado.
4. O registro é adicionado à lista carregada de `data/registros.json`.
5. A lista completa é gravada novamente em JSON.

### Registro pela Inbox

1. O usuário escreve em `inbox/inbox.txt`.
2. A opção `7. Processar inbox` lê o conteúdo do arquivo.
3. Se houver campos no formato `[CAMPO]:`, o conteúdo é tratado como registro estruturado.
4. Se não houver campos estruturados, cada linha é tratada como registro rápido.
5. Registros válidos são adicionados a `data/registros.json`.
6. A inbox é limpa somente quando há registros salvos e nenhum erro.

### Relatório Diário

1. A opção `4. Gerar relatório diário` carrega `data/registros.json`.
2. Os registros são filtrados pela data atual.
3. O texto é gerado com registros de diário e experiências.
4. O resultado é salvo em `reports/relatorio_diario.txt`.

## Dados

Todos os dados persistidos ficam em uma lista JSON em:

```text
data/registros.json
```

## Campos de Registro de Diário

Campos possíveis:

- periodo
- texto
- data
- hora
- tipo_de_dia
- estado
- prioridades
- foco_unico
- decisao_importante
- aprendizado_principal
- lembrar_30_dias
- conselho_para_amanha

## Campos de Experiência

Campos principais:

- categoria: `experiencia`
- sistema
- tipo_registro
- titulo
- descricao
- impacto
- aprendizado
- memoria_futura
- data
- hora

Campos opcionais usados principalmente pela inbox:

- origem
- processado

Valores atuais de `origem`:

- `inbox_rapida`
- `inbox_estruturada`

Quando uma experiência não tem `origem`, a formatação exibe `registro_manual`.

## Campos de Aula

Experiências do tipo `AULA` podem conter o objeto `aula` com:

- disciplina
- turma
- tema
- objetivo
- o_que_aconteceu
- evidencias
- descobertas
- hipotese_pedagogica
- intervencao_futura

Na v0.4, `turma` e `o_que_aconteceu` são preenchidos pelo registro estruturado da inbox, mas não pelo fluxo manual interativo.

## Validações Atuais

Sistemas aceitos:

- TRABALHO
- FAMILIA
- ESPIRITUALIDADE
- ESCRITA
- ESTUDOS
- PROJETOS
- SAUDE

Tipos de registro aceitos:

- EVENTO
- REFLEXAO
- PLANEJAMENTO
- AULA
- IDEIA

Tipos de dia aceitos:

- docente
- doméstico
- criativo
- planejamento
- recuperação
- híbrido

## Limitações Atuais

- `main.py` concentra responsabilidades que futuramente podem ser separadas em módulos.
- A inbox processa múltiplos registros rápidos, mas apenas um registro estruturado por vez.
- Não existe arquivo persistente de erros da inbox.
- Não existe prévia antes de salvar registros da inbox.
- Não existe relatório por sistema.
- Não existe relatório semanal.
- Não existe backup automático de `data/registros.json`.
- O Módulo ECO ainda é planejado; não há análise automática de padrões, tensões ou hipóteses.
