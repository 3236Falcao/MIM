# Manual do MIM v0.4

O MIM é uma prótese cognitiva local: um diário inteligente para registrar experiências, organizar sistemas da vida e preservar memórias úteis para decisões futuras.

Nesta versão, o MIM funciona como uma inbox universal. Ele aceita registros rápidos e registros estruturados, salva tudo em JSON e gera relatórios diários em texto.

## Sistemas da Vida

O MIM organiza experiências por sistemas:

- TRABALHO
- FAMILIA
- ESPIRITUALIDADE
- ESCRITA
- ESTUDOS
- PROJETOS
- SAUDE

Essa organização se inspira na teoria bioecológica de Bronfenbrenner: a vida não acontece em tarefas isoladas, mas em sistemas relacionados. Cada registro pode revelar tensões, oportunidades, padrões e necessidades dentro de um sistema.

## Registros Rápidos

Use registros rápidos quando a prioridade for capturar algo sem interromper o fluxo do dia.

Formato:

```text
PALAVRA-CHAVE: frase
```

Exemplos:

```text
IDEIA: O MIM deve organizar sistemas, não tarefas.
FAMILIA: Samuel já está melhor.
AULA: A turma respondeu melhor ao trabalho em duplas.
TRABALHO Preciso revisar o planejamento semanal.
```

Se não houver dois-pontos, o MIM usa a primeira palavra como palavra-chave e o restante como descrição.

## Registros Estruturados

Use registros estruturados quando a experiência exigir mais contexto.

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

Para aulas, use também os campos pedagógicos:

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

## Inbox Universal

A inbox fica em:

```text
inbox/inbox.txt
```

Escreva um registro rápido ou um modelo estruturado nesse arquivo. Depois rode o programa e escolha a opção de processar inbox.

Quando o processamento dá certo, o registro é salvo em `data/registros.json` e a inbox é limpa.

## Ciclo Cognitivo

O MIM organiza a memória prática pelo ciclo:

1. Observar
2. Interpretar
3. Decidir
4. Agir
5. Memorizar

O objetivo não é apenas guardar acontecimentos, mas transformar experiências em memória operacional para escolhas futuras.

## Módulo ECO

O Módulo ECO é a direção conceitual do MIM para interpretar registros dentro dos sistemas da vida. ECO significa observar a experiência no contexto ecológico da pessoa: casa, trabalho, saúde, espiritualidade, escrita, estudos e projetos.

Na v0.4, o ECO ainda é uma camada conceitual. A base técnica já existe nos campos `sistema`, `tipo_registro`, `impacto`, `aprendizado` e `memoria_futura`.
