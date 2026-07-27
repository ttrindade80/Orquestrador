---
name: relatorios-readme
description: Roteamento de relatorios e evidencias de agentes para o pacote canonico de templates (ADR-0032)
metadata:
  type: referencia
  scope: scripts
---

# Relatorios — Regras

## Definicao

Relatorio e evidencia. Ele descreve o que foi feito, o que foi verificado e o
que ficou bloqueado. Relatorio nao altera contrato, nao aprova ADR e nao cria
escopo novo.

## Template canonico obrigatorio

O indice canonico de templates documentais e de relatorios/evidencias e:

```text
docs/templates/00_INDICE_TEMPLATES_DOCUMENTAIS_E_RELATORIOS.md
```

O gerente resolve, antes de gerar o prompt do agente, o nome, o caminho e o
template canonico unico aplicavel a cada relatorio ou evidencia. O agente
nao escolhe nem adapta template por proximidade.

Ausencia de template canonico aplicavel, ou conflito material entre o
template resolvido e a regra vigente, bloqueia a execucao antes da producao
do relatorio ou evidencia.

## Regras gerais

- todos os relatorios e evidencias produzidos por agentes ficam em
  `docs/relatorios/`;
- o relatorio externo do gerente permanece fora desta politica e continua
  regido pelo sistema externo do gerente;
- relatorios e artefatos historicos nao sao reescritos para adequacao a
  templates novos;
- nova execucao gera novo relatorio; relatorio anterior nao e sobrescrito,
  salvo correcao factual da propria execucao por comando de terminal manual.
