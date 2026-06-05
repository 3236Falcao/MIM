# Arquitetura do MIM v0.4

O MIM é um aplicativo Python local, sem dependências externas obrigatórias. Ele salva dados em JSON, gera relatórios em texto e usa testes automatizados com `unittest`.

## Estrutura Atual

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
└── docs/
```

## Componentes

### Persistência

Arquivo principal:

```text
data/registros.json
```

Todos os registros são salvos em uma lista JSON. O formato permite manter registros antigos e adicionar novos campos conforme a evolução do projeto.

### Relatórios

Arquivo principal:

```text
reports/relatorio_diario.txt
```

O relatório diário filtra registros pela data e renderiza:

- registros de manhã e noite
- experiências manuais
- registros rápidos
- registros estruturados
- registros de aula com campos pedagógicos

### Inbox Universal

Arquivo de entrada:

```text
inbox/inbox.txt
```

A inbox aceita dois modos:

- registro avulso rápido
- registro estruturado completo

Se a mensagem contém campos no formato `[CAMPO]:`, o MIM processa como estruturada. Caso contrário, processa como registro rápido.

### Registros Rápidos

O registro rápido mapeia uma palavra-chave para `sistema` e `tipo_registro`.

Exemplo:

```text
IDEIA: O MIM deve organizar sistemas, não tarefas.
```

Gera:

- origem: `inbox_rapida`
- sistema: `PROJETOS`
- tipo_registro: `IDEIA`
- título automático
- descrição
- processado: `true`

### Registros Estruturados

O registro estruturado usa campos nomeados.

Campos gerais obrigatórios:

- SISTEMA
- TIPO
- TÍTULO
- MEMÓRIA FUTURA
- DESCRIÇÃO ou O QUE ACONTECEU

Para `AULA`, também são obrigatórios:

- DISCIPLINA
- TURMA
- TEMA
- EVIDÊNCIAS
- INTERVENÇÃO FUTURA

## Modelo Cognitivo

O MIM é orientado pelo ciclo:

1. Observar
2. Interpretar
3. Decidir
4. Agir
5. Memorizar

Na v0.4, o sistema implementa principalmente Observar e Memorizar. Interpretar, Decidir e Agir serão fortalecidos pelo futuro Módulo ECO.

## Módulo ECO

O Módulo ECO é a camada futura de interpretação ecológica. Ele deverá relacionar registros aos sistemas da vida e apoiar leituras inspiradas na teoria bioecológica de Bronfenbrenner.

Entrada provável:

- registros por sistema
- impacto
- aprendizado
- memória futura
- campos pedagógicos de aula

Saída provável:

- padrões
- alertas
- sínteses
- hipóteses
- sugestões de ação

## Testes

Os testes ficam em:

```text
tests/test_main.py
```

Eles validam:

- registros antigos
- sistemas válidos e inválidos
- tipos válidos e inválidos
- registros de aula
- consulta por sistema
- registros rápidos
- registros estruturados
- limpeza da inbox
- relatórios
