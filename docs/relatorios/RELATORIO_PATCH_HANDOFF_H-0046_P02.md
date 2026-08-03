---
name: RELATORIO_PATCH_HANDOFF_H-0046_P02
description: "Patch P02 do H-0046 — corrige os quatro achados pendentes do QA pós-patch P01 (QA-H0046-02, 04, 05, 06)"
metadata:
  type: relatorio_patch_handoff
  id: H-0046
  patch: "P02"
---

# Patch P02 do H-0046

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0046
  artefato_principal: docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
  cadeia_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0046.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_POS_PATCH_HANDOFF_H-0046_P01.md
  achados_tratados:
    - QA-H0046-02
    - QA-H0046-04
    - QA-H0046-05
    - QA-H0046-06

execucao:
  status: HANDOFF_PATCHED
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0046_P02.md
  arquivos_alterados:
    - docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md
```

## Correções aplicadas

**QA-H0046-02 (dependências e arquitetura acíclica).** Releitura focal de
`tela/renderizador.py` confirmou as três dependências reais apontadas pelo
QA: `_linha_conteudo` consome `_cortar_sem_ansi`/`_ljust_sem_ansi` (hoje
L251-252); `_participantes_distribuicao_matricial` consome
`_participantes_de_conteudo_externo` (hoje L2566); `_linhas_distribuicao_matricial`
importa `tela.navegacao` localmente (hoje L3307). Criado o módulo comum
`tela/renderizacao/texto_ansi.py` (primitivas ANSI de baixo nível, sem
dependência de `geometria_caixa.py` nem `barra_menus.py`), evitando que um
dependesse do outro. Atualizados: §2.4, §2.6, §3.1 a §3.5, §4.1, §5.1 e
todos os comandos executáveis da §7 que enumeram módulos, símbolos ou
arestas do grafo.

**Reexportações omitidas.** `_quebrar_texto` e `_texto_valor_campo`
(proprietário `conteudo_externo.py`) e `_avaliar_regra_ativo` e
`_texto_chip_barra` (proprietário `barra_menus.py`) — todos com consumidor
real confirmado em `tela/teste_renderizador.py` e `demo/teste_demo_paginacao.py`
via `from tela import renderizador as _rend`/`_rend_qa002` — foram incluídos
em §2.4, §3.5, §5.1 e §7 (comando 7). Repetida a busca focal de consumidores
por atributo (`_rend_qa002.*`, `_rend.*`, `_mod.*`, `_mod_rend.*`,
`_rend_mod.*`); nenhum outro símbolo consumido ficou omitido.

**QA-H0046-04 (detector de ciclos).** O comando 2 da §7 foi reescrito: além
de imports relativos, agora rejeita explicitamente `from tela.renderizacao
import <modulo>` e `import tela.renderizacao` (sem submódulo), por ocultarem
a aresta real do grafo. Inclui verificações sintéticas embutidas que
comprovam a rejeição das duas formas proibidas e a aceitação/normalização de
`import tela.renderizacao.<modulo>` e `from tela.renderizacao.<modulo>
import <simbolo>`, executadas antes da análise real do pacote.

**QA-H0046-05 (fachada sem funções).** Comandos 6 e 6b foram substituídos
por um único comando 6 normativo: exige zero `FunctionDef`,
`AsyncFunctionDef`, `Lambda` e `ClassDef` em qualquer profundidade (cobre
função aninhada e classe interna), e restringe o corpo do módulo a
docstring, imports, atribuições de alias simples (`Name`/cadeia de
`Attribute`, sem chamada/operador) e `__all__` como lista literal. Nenhuma
alternativa de wrapper "opcional" permanece. §3.4 foi reescrita: um wrapper
só pode existir se a implementação parar pela exceção operacional focal
(§11) e solicitar patch documental antes de criá-lo.

**QA-H0046-06 (mapa completo e propriedade efetiva).** Comando 7 da §7
reescrito em três dimensões: (a) existência física de `__init__.py` e de
todos os módulos, incluindo `texto_ansi.py`, com verificação de que
`__init__.py` é importável, sem lógica e sem reexportar a API da fachada;
(b) `esperados` reestruturado com `definidos`/`aliases_autorizados` por
módulo, e verificação por AST de que cada símbolo é materializado
(`FunctionDef`/`AsyncFunctionDef`/`ClassDef`/atribuição de nível superior) no
proprietário — não apenas `hasattr`; (c) verificação de origem AST da
reexportação na própria fachada, resolvendo tanto `ImportFrom` direto quanto
alias de atribuição.

## Verificações executadas nesta correção

- `rg` confirmando as três dependências pendentes e os quatro consumidores
  adicionais (linhas exatas citadas acima).
- Todos os 5 blocos `python3 - <<'PY'` do handoff validados sintaticamente
  (`ast.parse` sem erro).
- Lógica do novo detector de ciclos (comando 2) executada isoladamente: as
  quatro verificações sintéticas passam.
- Lógica de materialização AST e resolução de origem (comando 7) executada
  isoladamente contra o monólito atual, confirmando ausência de erros de
  execução (o pacote `tela/renderizacao/` ainda não existe — execução
  completa permanece reservada à implementação, como já registrado pelo QAs
  anteriores).
- `test -f` no relatório criado; `git diff --check` sem marcadores de
  conflito.

## Resultado

```yaml
resultado:
  delta_material:
    - "Novo módulo tela/renderizacao/texto_ansi.py inserido na arquitetura-alvo"
    - "Dependências geometria_caixa->texto_ansi, barra_menus->texto_ansi, matriz_participantes->conteudo_externo (_participantes_de_conteudo_externo) e paginacao_interna->tela.navegacao registradas nominalmente"
    - "4 símbolos adicionais (_quebrar_texto, _texto_valor_campo, _avaliar_regra_ativo, _texto_chip_barra) incluídos na lista de reexportação, prova de compatibilidade e mapa de propriedade"
    - "Detector de ciclos (comando 2) normaliza/rejeita 'from tela.renderizacao import modulo' e 'import tela.renderizacao', com verificações sintéticas embutidas"
    - "Comando 6b eliminado; comando 6 único exige zero funções/lambdas/classes em qualquer profundidade, sem alternativa de wrapper"
    - "Comando 7 reestruturado em três dimensões (existência física incl. __init__.py, materialização AST no proprietário, origem AST da reexportação na fachada)"
  verificacoes_executadas:
    - "rg das dependências e consumidores pendentes"
    - "ast.parse dos 5 blocos heredoc do handoff"
    - "execução isolada da lógica sintética do detector de ciclos"
    - "execução isolada da lógica de materialização/resolução de origem do comando 7"
  bloqueios: []
```
