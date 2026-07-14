---
name: indice-orquestrador
description: Indice da documentacao padrao para desenvolvimento do Orquestrador
metadata:
  type: indice
  scope: orquestrador
  atualizado_em: 2026-07-07
---

# Indice — Documentacao do Orquestrador

## Proposito

Esta pasta guarda regras documentais, templates, contratos ativos, ADRs,
handoffs e relatorios de evidencia para conduzir desenvolvimento por
especificacao. Ela nao deve conter codigo nem dado JSON de producao lido pelo
renderer.

## Regra de limpeza

Antes de mover este padrao para outro projeto, verificar:

- nenhum arquivo de cache ou bytecode esta presente;
- nenhum documento afirma decisao concreta que ainda nao foi aprovada;
- exemplos usam nomes genericos como `modulo_exemplo`;
- JSON de producao fica em `config/`, nunca dentro de `docs/`.

## Ordem de leitura

1. `docs/INDICE.md`
2. `docs/contratos/contrato_processo_desenvolvimento.md`
3. `docs/NOMENCLATURA.md` — fonte de verdade dos nomes; todo contrato de
   modulo é escrito a partir dela, nunca do codigo antigo (ver seção 0 do
   proprio glossário para a política schema × dados)
4. `docs/adr/INDICE_ADR.md`
5. `docs/contratos/` — demais contratos de modulo ja `ativo` (hoje:
   `contrato_estilo.md`, `contrato_composicao_corpo.md`,
   `contrato_barra_de_menus.md`, `contrato_cabecalho.md`,
   `contrato_lancador.md`, `contrato_tela_json.md`, `contrato_chip.md`,
   `contrato_console.md`; contratos incrementais de JSON:
   `contrato_json_tela_minima.md`, `contrato_json_cabecalho.md`,
   `contrato_json_barra_de_menus.md`, `contrato_json_lancador.md`,
   `contrato_json_dashboard.md`, `contrato_json_console.md`)
6. `docs/handoff/README.md`
7. `docs/relatorios/README.md`
8. Templates em `docs/templates/`, conforme a tarefa.

## Estrutura esperada

```text
config/
  estilo.json
  lancador.json
  layout_console.json
  layout_dado.json  # obsoleto/transicional; nao canonico
  barra_de_menus.json
  cabecalho.json
  layout_menu.json  # obsoleto/transicional; nao canonico
docs/
  INDICE.md
  NOMENCLATURA.md
  backlog.md
  issues.md
  contratos/
    contrato_processo_desenvolvimento.md
    contrato_estilo.md
    contrato_composicao_corpo.md
    contrato_barra_de_menus.md
    contrato_cabecalho.md
    contrato_lancador.md
    contrato_tela_json.md
    contrato_chip.md
    contrato_console.md
  adr/
    INDICE_ADR.md
    ADR-0001-menu-suporta-matriz.md
    ADR-0002-menu-sobra-direita.md
    ADR-0003-vaos-elasticos-menu.md
    ADR-0004-estilo-cor-inativo-cor-alerta.md
    ADR-0005-lancador-nao-e-corpo-navegavel.md
    ADR-0006-renomeacao-console-dashboard.md
    ADR-0007-tela-processamento-composicao.md
    ADR-0008-modelo-configuracao-por-tela.md
  handoff/
    README.md
  relatorios/
    README.md
  templates/
    TEMPLATE_ADR.md
    TEMPLATE_BUG.md
    TEMPLATE_HANDOFF_IMPLEMENTACAO.md
    TEMPLATE_HANDOFF_QA.md
    TEMPLATE_RELATORIO_IMPL.md
    TEMPLATE_RELATORIO_QA.md
    TEMPLATE_RFC.md
tela/
  loader.py
  modelo.py
  renderizador.py
  demo.py
  diagnostico.py
```

**`config/` não é documentação** — é dado de produção lido pelo renderer em
tempo de execução (ver `docs/NOMENCLATURA.md` seção 0). Fica na raiz do
Orquestrador, irmã de `docs/`, nunca dentro de `docs/`.

## Artefatos

| Artefato | Funcao | Regra |
|---|---|---|
| Glossário (`NOMENCLATURA.md`) | Fonte única de nomes e schema | Todo contrato deriva dele; ele não guarda valor concreto de produção (ver seção 0) |
| Config (`config/*.json`) | Valores concretos que o renderer lê | Modelo em migração pela ADR-0008: `config/estilo.json` permanece biblioteca global de estilo; telas passam a ter JSON próprio de configuração concreta conforme `contrato_tela_json.md`. JSONs por domínio existentes permanecem transicionais até revisão específica. |
| Contrato | Define comportamento esperado | Deve ser aprovado antes da implementacao |
| ADR | Registra decisao arquitetural | Nao substitui contrato; contratos afetados devem ser atualizados |
| RFC | Propoe mudanca | Nao autoriza implementacao |
| Handoff | Ordem fechada de trabalho | Deve citar contrato e criterios de aceite |
| Relatorio | Evidencia do que foi feito | Nao cria regra nova |
| Bug | Registra falha observada | Deve classificar se e local ou arquitetural |

## Exemplo de referência neutra

```text
Contrato alvo: docs/contratos/contrato_modulo_exemplo.md
Modulo alvo: tela/modulo_exemplo/
Config alvo: config/modulo_exemplo.json
Handoff: H-0001-criar-interface-minima.md
Relatorio: IMP-0001-criar-interface-minima.md
QA: REL-QA-0001-criar-interface-minima.md
```
