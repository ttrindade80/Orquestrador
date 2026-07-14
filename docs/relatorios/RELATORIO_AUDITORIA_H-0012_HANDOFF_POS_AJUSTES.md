---
name: RELATORIO_AUDITORIA_H-0012_HANDOFF_POS_AJUSTES
description: Auditoria/QA do handoff H-0012 apos ajustes documentais
metadata:
  type: relatorio_auditoria_handoff
  status: QA_APPROVED_WITH_NOTES
  handoff_auditado: docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
  data: 2026-07-08
---

# Relatório de Auditoria — H-0012 pós-ajustes

## Status

`QA_APPROVED_WITH_NOTES`

O handoff H-0012 revisado pode seguir para implementação pelo OpenCode/GLM.
O bloqueio anterior sobre a exigência de "apenas linhas [PASSOU]" foi
resolvido. Restam apenas ressalvas documentais não bloqueantes, principalmente
a divergência já conhecida entre o formato operacional atual de `dashboard`
com `campos[]` e o envelope incremental de `contrato_json_dashboard.md`.

## Contexto

Esta auditoria revisa a versão pós-ajustes do H-0012, cujo objetivo é iniciar
suporte de código a `grupo` como container estrutural mínimo em tela isolada.
A auditoria anterior havia bloqueado o handoff porque os comandos obrigatórios
exigiam que os testes imprimissem apenas linhas `[PASSOU]`, o que contradizia
os harnesses reais.

O escopo auditado permanece documental. Nenhum código foi implementado,
nenhum handoff foi alterado e nenhum commit foi realizado.

## Arquivos lidos

- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md`
- `docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md`

## Verificações executadas

```bash
git status --short
```

Resultado:

```text
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
```

```bash
git log --oneline -5
```

Resultado:

```text
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
```

```bash
git diff --stat
git diff --name-only
```

Resultado: ambos sem saída, pois os arquivos auditados estão não rastreados.

```bash
grep -n "PASSOU\|FALHOU\|traceback\|grupo\|container estrutural\|diagnostico.py\|demo.py" docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
```

Resultado: confirmou a presença da nova regra de testes por código de saída 0,
sem `[FALHOU]` e sem traceback; confirmou também as declarações sobre `grupo`
como container estrutural e as proibições de `diagnostico.py`, `demo.py`,
`teste_diagnostico.py` e `teste_demo.py`.

## Resultado da auditoria anterior

A auditoria anterior classificou o H-0012 como `ARCHITECTURE_REVIEW_REQUIRED`
por um achado bloqueante: a exigência literal de que os testes imprimissem
apenas linhas `[PASSOU]`.

O levantamento pós-auditoria demonstrou que os testes existentes imprimem
cabeçalhos, seções, resumos e linhas diagnósticas mesmo quando passam com
código de saída 0 e sem `[FALHOU]`. A recomendação era substituir a regra por:
código de saída 0, ausência de `[FALHOU]` e ausência de traceback, permitindo
a saída diagnóstica existente.

## Verificação dos ajustes

### 1. Regra de saída dos testes

Resolvido.

O H-0012 revisado exige que os testes encerrem com código de saída 0, não
imprimam linhas `[FALHOU]` e não produzam traceback. O texto permite
explicitamente cabeçalhos, seções, resumos e linhas diagnósticas já existentes.

Não há mais exigência de "apenas linhas [PASSOU]". O bloqueio anterior foi
removido.

### 2. Grupo como container estrutural

Adequado.

O handoff declara que `grupo` é container estrutural de composição, não é
elemento funcional do corpo e não altera a taxonomia funcional. Os tipos
funcionais permanecem `console`, `dashboard` e `lancador`.

Também está explícito que `grupo` pode aparecer em `corpo.elementos[]` como
nó estrutural mínimo no H-0012, não gera caixa visual própria e não possui
foco, chip, ação, navegação ou registry.

### 3. Escopo mínimo e tela isolada

Adequado.

O escopo positivo está limitado a `config/telas/grupo_minimo.json`, um grupo
estrutural e exatamente um elemento funcional interno, recomendado e
exemplificado como `dashboard` literal/passivo.

O escopo negativo proíbe migração do Orquestrador, `lado_a_lado`, grupos com
2 ou mais elementos, aninhamento, distribuição percentual/fração, foco,
seleção, navegação por `[✥]`, registry e alteração de contratos/ADRs.

### 4. Dashboard campos[] versus contrato incremental

Aceitável com ressalva não bloqueante.

O H-0012 usa `dashboard.campos[]` como formato operacional já validado pelo
H-0010A e suportado pelos JSONs reais e pelo renderer atual. O próprio handoff
registra que a harmonização entre `contrato_json_dashboard.md`, que descreve
`conteudo`/`regras_exibicao`, e o formato operacional com `campos[]` fica fora
do escopo do H-0012.

Essa decisão evita expandir o ciclo para alteração de contrato ou migração de
formato. A ressalva é apenas documental: a divergência deverá ser harmonizada
em ciclo próprio.

### 5. diagnostico.py/demo.py/testes proibidos

Adequado.

O handoff proíbe explicitamente:

- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`

Também determina que, se a implementação exigir alterar qualquer um desses
arquivos ou alterar a saída do Orquestrador, o executor deve parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

### 6. Arquivos permitidos e proibidos

Adequado.

A lista de arquivos permitidos é suficiente e restrita:

- criar `config/telas/grupo_minimo.json`
- criar `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`
- alterar `tela/loader.py`
- alterar `tela/modelo.py`
- alterar `tela/renderizador.py`
- alterar `tela/teste_loader.py`
- alterar `tela/teste_modelo.py`
- alterar `tela/teste_renderizador.py`

A lista de proibidos protege os JSONs existentes do Orquestrador, contratos,
ADRs, nomenclatura, índice, demo, diagnóstico e arquivos fora da lista
permitida.

### 7. Critérios de aceite

Adequados.

Os critérios CA-01 a CA-39 são observáveis e cobrem:

- validade da tela isolada;
- validações positivas e negativas do loader;
- representação de modelo;
- renderização sem caixa visual do grupo;
- preservação de lista plana;
- preservação dos JSONs existentes;
- execução dos testes obrigatórios;
- ausência de alteração em arquivos proibidos;
- ausência de commit;
- ausência de `__pycache__` e `.pyc`.

Os critérios são verificáveis pelo executor sem alterar contratos, ADRs,
Orquestrador ou demo.

## Achados bloqueantes

0.

## Achados não bloqueantes

1. **Divergência documental conhecida em `dashboard`.**

   O H-0012 usa corretamente o formato operacional atual `dashboard.campos[]`,
   mas `contrato_json_dashboard.md` ainda descreve envelope mínimo com
   `conteudo` e `regras_exibicao`. O handoff mitiga o risco ao declarar a
   harmonização fora de escopo e ao proibir alteração de contratos neste ciclo.

2. **Referências históricas H-0011A-D ainda aparecem em contratos/ADR.**

   O H-0012 não reabre H-0011/H-0011A e define sequência futura sem letras.
   Ainda assim, contratos e ADR-0010 preservam referências históricas à
   sequência H-0011A-D. Isso não bloqueia o H-0012 porque o handoff explicita
   a decisão vigente, mas merece limpeza documental futura.

## Pontos positivos

- O bloqueio anterior foi corrigido com redação compatível com os testes reais.
- `grupo` está definido como container estrutural, não como quarto tipo funcional.
- O escopo está bem limitado a tela isolada e grupo mínimo.
- H-0011 permanece cancelado e H-0011A não é recriado.
- `demo.py`, `diagnostico.py` e seus testes estão protegidos.
- O uso de `dashboard.campos[]` está justificado como operacional e não tenta
  resolver divergência contratual dentro do ciclo.
- Os critérios de aceite são numerosos, objetivos e verificáveis.

## Conclusão

O handoff H-0012 revisado pode seguir para implementação pelo OpenCode/GLM.

Status final da auditoria: `QA_APPROVED_WITH_NOTES`.

Não há achados bloqueantes. As notas restantes são documentais e não impedem a
execução do handoff, desde que o executor respeite a lista de arquivos
permitidos/proibidos e pare com `ARCHITECTURE_REVIEW_REQUIRED` se precisar
alterar contrato, ADR, Orquestrador, demo ou diagnóstico.
