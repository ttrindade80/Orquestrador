# Relatório de patch — H-0074 P01

```yaml
cadeia:
  raiz: H-0074
  predecessor_imediato: RELATORIO_QA_HANDOFF_H-0074.md
status: HANDOFF_PATCHED
patch: P01
item: ITEM-0026
adr: ADR-0048
handoff: H-0074
achados_tratados:
  - QA-H0074-001
  - QA-H0074-002
  - QA-H0074-003
  - QA-H0074-004
```

## Fronteira de validação (QA-H0074-001)

Levantamento focal: `validar_conteudo_externo` não conhece
`politica_navegacao`; `formato_dois_niveis_por_foco.py` valida só
apresentação estrutural; helpers de `teste_navegacao.py` montam árvores
in-memory; `estilo.aplicar_ao_modelo` atribui conteúdo depois da
construção (H-0063).

A menor fronteira em que pais/filhos, `filho_default` em `campos` e a
política do console já coexistem é o final de
`tela/modelo.py::construir_modelo`, após `_propagar_conteudo_externo`.
A função permanece em `tela/navegacao.py` (discriminadores já existentes).
A chamada deixa de ser exclusiva da demo: ocorre em `construir_modelo`,
com import local para evitar ciclo `navegacao.py` → `ModeloTela`. Sem
módulo nem pipeline novos. Sem bloqueio.

## Caminhos cobertos

Atravessam a validação: `_carregar_modelo_por_id` (H-0055 e H-0072) e
qualquer outro chamador de `construir_modelo` com conteúdo associado a
console `dois_niveis_por_foco`. Testes 6–9 e 13 exigem `construir_modelo`
direto, não wrapper da demo. Fora: helpers in-memory (sujeitos à guarda
de reconciliação); H-0063 (`conteudo_externo is None` na construção;
autoridade em `preset_default`).

## Fallback (QA-H0074-002)

Deixou de ser opcional. `_reconciliar_ids_dois_niveis` não substitui
`filho_default` ausente/inválido por `filhos[0]`. `entrar_nivel_filhos`
elimina `next(..., filhos[0][0])`: usa escolha já reconciliada ou
devolve o estado inalterado. Teste explícito: estado sem escolha válida
não posiciona no primeiro filho.

## H-0072 (QA-H0074-003)

Os três consoles declaram `dois_niveis_por_foco`; o catálogo associa
documento externo com dois pais e filhos diretos, sem `filho_default`.
Mesmo caminho de carga de H-0055. Sujeita ao schema. Fixture de conteúdo
incluída: `h0072_pai_01` → `h0072_filho_01_02`; `h0072_pai_02` →
`h0072_filho_02_03`. Estrutural H-0072 preservado.

## Lista futura de arquivos

Editar: `tela/modelo.py` (chamada), `tela/navegacao.py` (validador +
guarda), `tela/selecao.py` (reconciliação), conteúdos H-0055 e H-0072,
`tela/teste_navegacao.py`, `tela/teste_loader.py`.

Não editar: `demo/demo.py` (já passa por `construir_modelo`),
`conteudo_externo.py`, `formato_dois_niveis_por_foco.py`, renderers,
Estilo/H-0063, estruturais H-0055/H-0072/H-0063, persistência/H-0075.

## Testes acrescentados

Além dos já previstos: identidade duplicada via `construir_modelo` com
`filho_default` presente (rejeição sem baseline); estado sem escolha
válida; travessia da fronteira comum; H-0072 reconciliada. Lista mínima
do handoff: 14 itens.

## Demonstração com digest

Arquivo:
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`.
`sha256sum` antes; demo; observação dos defaults; Espaço só em runtime;
`sha256sum` depois; igualdade. Sem restaurar/reescrever a fixture.
H-0072 coberta por teste automatizado.

## Bloqueios

nenhum.

Artefato corrigido:
`docs/handoff/H-0074-filho-default-carregamento-baseline-runtime.md`.
