# Manual do MIM v0.4

Este documento explica como usar o MIM no dia a dia.

## Como Executar

Na raiz do projeto:

```bash
python3 main.py
```

Menu atual:

```text
1. Registrar manhã
2. Registrar noite
3. Ver registros
4. Gerar relatório diário
5. Registrar experiência
6. Consultar sistema
7. Processar inbox
8. Sair
9. Síntese ECO do dia
```

## Sistemas da Vida

Ao registrar experiências, escolha um dos sistemas aceitos:

- TRABALHO
- FAMILIA
- ESPIRITUALIDADE
- ESCRITA
- ESTUDOS
- PROJETOS
- SAUDE

## Tipos de Registro

As experiências aceitam estes tipos:

- EVENTO
- REFLEXAO
- PLANEJAMENTO
- AULA
- IDEIA

## Registros de Manhã e Noite

Use `1. Registrar manhã` para registrar:

- texto livre do período
- tipo de dia
- estado físico, mental e emocional
- até três prioridades
- foco único
- memória para 30 dias

Use `2. Registrar noite` para registrar:

- texto livre do período
- decisão importante
- aprendizado principal
- conselho para amanhã

## Registrar Experiência Manualmente

Use `5. Registrar experiência` para salvar uma experiência com:

- sistema
- tipo de registro
- título
- descrição
- impacto
- aprendizado
- memória futura

Se o tipo for `AULA`, o menu interativo também pede:

- disciplina
- tema
- objetivo
- evidências
- descobertas
- hipótese pedagógica
- intervenção futura

Observação: na v0.4, o registro manual interativo de aula não pede `turma` nem `o que aconteceu`. Esses campos existem no registro estruturado pela inbox.

## Consultar Sistema

Use `6. Consultar sistema` para listar registros de experiência filtrados por sistema da vida.

## Gerar Relatório Diário

Use `4. Gerar relatório diário`.

O relatório é salvo em:

```text
reports/relatorio_diario.txt
```

Ele inclui registros de diário e experiências da data atual.

## Síntese ECO do Dia

Use `9. Síntese ECO do dia`.

A síntese lê os registros da data atual e mostra:

- quantidade de experiências registradas
- sistemas envolvidos
- aprendizados encontrados
- memórias futuras registradas

Se não houver registros no dia, o MIM informa isso no terminal.

## Inbox Universal

A inbox fica em:

```text
inbox/inbox.txt
```

Ela aceita:

- registros rápidos
- um registro estruturado

Depois de preencher a inbox, execute o MIM e escolha:

```text
7. Processar inbox
```

Se não houver erros, os registros são salvos em `data/registros.json` e a inbox é limpa.

## Registro Rápido

Use registro rápido para capturar uma ideia ou acontecimento sem preencher um formulário.

Formato:

```text
PALAVRA-CHAVE: frase
```

Exemplos:

```text
IDEIA: O MIM deve organizar sistemas, não tarefas.
FAMILIA: Samuel já está melhor.
AULA: A turma respondeu melhor ao trabalho em duplas.
TRABALHO: Preciso revisar o planejamento semanal.
ESCRITA: Ideia para capítulo do livro.
SAUDE: Preciso descansar mais.
FE: Reflexão sobre disciplina espiritual.
```

Também funciona sem dois-pontos:

```text
TRABALHO Preciso revisar o planejamento semanal.
```

Nesse caso, a primeira palavra é tratada como palavra-chave e o restante como descrição.

## Palavras-Chave Rápidas

- IDEIA -> PROJETOS / IDEIA
- AULA -> TRABALHO / AULA
- TRABALHO -> TRABALHO / EVENTO
- FAMILIA ou FAMÍLIA -> FAMILIA / EVENTO
- ESCRITA -> ESCRITA / IDEIA
- SAUDE ou SAÚDE -> SAUDE / EVENTO
- FE ou FÉ -> ESPIRITUALIDADE / REFLEXAO
- ESTUDOS -> ESTUDOS / REFLEXAO
- MIM -> PROJETOS / IDEIA

## Registro Estruturado

Use registro estruturado quando o contexto precisa ser preservado com mais precisão.

Formato geral:

```text
[SISTEMA]:
[TIPO]:
[TÍTULO]:
[DATA]:
[DESCRIÇÃO]:
[IMPACTO]:
[APRENDIZADO]:
[MEMÓRIA FUTURA]:
```

Campos obrigatórios gerais:

- SISTEMA
- TIPO
- TÍTULO
- MEMÓRIA FUTURA
- DESCRIÇÃO ou O QUE ACONTECEU

`DATA` é opcional. Quando usada, deve seguir o formato `AAAA-MM-DD`.

## Registro Estruturado de Aula

Para `AULA`, use também:

```text
[DISCIPLINA]:
[TURMA]:
[TEMA]:
[OBJETIVO]:
[O QUE ACONTECEU]:
[EVIDÊNCIAS]:
[DESCOBERTAS]:
[HIPÓTESE PEDAGÓGICA]:
[INTERVENÇÃO FUTURA]:
```

Campos obrigatórios adicionais para `AULA`:

- DISCIPLINA
- TURMA
- TEMA
- EVIDÊNCIAS
- INTERVENÇÃO FUTURA

## Modelos Prontos

Os modelos ficam em:

```text
inbox/modelos.txt
```

Use esse arquivo como referência para preencher a inbox.

## Limitações de Uso na v0.4

- A inbox aceita vários registros rápidos, um por linha.
- A inbox aceita apenas um registro estruturado por processamento.
- Se houver erro no processamento, a inbox não é limpa.
- Prévia antes de salvar, processamento parcial estruturado e arquivo de erros ainda são recursos planejados.
