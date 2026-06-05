# MIM

MIM é um diário inteligente local e uma prótese cognitiva pessoal. Ele registra experiências, decisões, aprendizados, memórias futuras e acontecimentos relevantes dos sistemas da vida.

A proposta do MIM é ajudar a observar, interpretar, decidir, agir e memorizar com mais continuidade, mantendo os dados localmente em JSON.

Versão atual: **v0.4**

## Como Rodar

Execute na raiz do projeto:

```bash
python3 main.py
```

O menu principal permite registrar manhã, registrar noite, ver registros, gerar relatório diário, registrar experiências, consultar sistemas e processar a inbox.

## Como Rodar os Testes

Execute:

```bash
python3 -m unittest discover -s tests
```

## Inbox Universal

A inbox fica em:

```text
inbox/inbox.txt
```

Ela aceita dois modos de entrada:

- registro rápido
- registro estruturado

Depois de escrever na inbox, rode o programa e escolha a opção `7. Processar inbox`.

## Registro Rápido

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

Nesse caso, a primeira palavra vira a palavra-chave e o restante vira a descrição.

## Registro Estruturado

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

Para registros do tipo `AULA`, também use:

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

Modelos prontos estão em:

```text
inbox/modelos.txt
```

## Processar a Inbox

1. Escreva um registro em `inbox/inbox.txt`.
2. Execute:

```bash
python3 main.py
```

3. Escolha a opção:

```text
7. Processar inbox
```

Se o registro for válido, ele será salvo em `data/registros.json` e a inbox será limpa.

## Privacidade

Este projeto é privado e contém dados pessoais. Não publique este repositório, os arquivos de `data/`, os relatórios ou qualquer conteúdo da inbox em ambientes públicos.
