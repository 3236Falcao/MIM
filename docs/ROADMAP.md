# Roadmap do MIM

Este documento descreve planos futuros. O histórico do que já foi feito fica em `CHANGELOG.md`.

## v0.5 - Relatórios por Sistema

Objetivo: gerar sínteses por sistema da vida.

Entregas planejadas:

- relatório por sistema
- contagem de registros por sistema
- aprendizados por sistema
- memórias futuras por sistema
- melhor recuperação de contexto por área da vida

## v0.6 - Relatório Semanal

Objetivo: ampliar a visão temporal do MIM.

Entregas planejadas:

- síntese semanal
- decisões recorrentes
- padrões de sobrecarga
- sistemas negligenciados
- aprendizados importantes da semana

## v0.7 - Inbox Avançada

Objetivo: tornar a inbox mais robusta.

Entregas planejadas:

- múltiplos registros estruturados no mesmo arquivo
- arquivo de erros da inbox
- processamento parcial
- prévia antes de salvar
- mensagens de erro mais acionáveis

## v0.8 - Módulo ECO Inicial

Objetivo: criar interpretação ecológica inicial.

Entregas planejadas:

- análise de padrões por sistema
- detecção de tensões
- hipóteses de intervenção
- sínteses orientadas pelo ciclo OIDA-M
- primeiros indicadores de saúde sistêmica

## Melhorias Técnicas Planejadas

- separar responsabilidades de `main.py` em módulos menores
- criar camada de serviço para inbox
- criar camada de serviço para relatórios
- criar backups locais de `data/registros.json`
- considerar exportação em Markdown ou CSV
- manter compatibilidade com registros antigos

## Critérios de Maturidade

O MIM deve amadurecer preservando estes critérios:

- dados pessoais locais e privados
- baixa fricção para capturar registros
- compatibilidade com registros antigos
- relatórios úteis para decisão
- recuperação eficiente de memória futura
- testes cobrindo fluxos críticos
- evolução conceitual sem perder simplicidade operacional

## Fases Futuras

### Fase 1 - Fundação

Status: em andamento.

Foco:

- diário
- experiências
- inbox
- relatórios diários
- documentação

### Fase 2 - Organização

Foco:

- relatórios por sistema
- relatórios semanais
- maior separação interna do código
- inbox mais robusta

### Fase 3 - Interpretação

Foco:

- Módulo ECO
- padrões
- hipóteses
- alertas
- saúde sistêmica

### Fase 4 - Sabedoria Operacional

Foco:

- transformar memória acumulada em orientação prática
- apoiar decisões
- sugerir intervenções
- fortalecer continuidade entre experiência e ação
