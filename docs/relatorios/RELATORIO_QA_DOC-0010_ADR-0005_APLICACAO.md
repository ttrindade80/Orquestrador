---
name: REL-DOC-DOC-0010-ADR-0005-APLICACAO
description: Auditoria documental da aplicação da ADR-0005 — lancador não é corpo navegável por [✥]
metadata:
  type: relatorio_qa
  status: APROVADO_COM_AJUSTES
  data: 2026-07-06
rastreabilidade:
  auditoria: "DOC-0010 / ADR-0005 aplicação"
  adr_relacionadas:
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
  contratos_alvo:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
  configs_alvo:
    - config/barra_de_menus.json
---

# REL-DOC — QA DOC-0010 / Aplicação ADR-0005

## Revisão executada

Foi verificada a aplicação da ADR-0005 nos contratos e configs ativos indicados para DOC-0010.
A auditoria conferiu validade do JSON, diffs do escopo esperado, ausência de migração indevida para `console`/`dashboard` e ocorrências remanescentes de `[✥]`, `Navegar`, `navegar` e `corpo navegável`.
Também foi verificado que os arquivos preservados listados para a aplicação não apresentam diff/status nesta etapa.

## Status final

APROVADO_COM_AJUSTES

## Arquivos verificados

- docs/NOMENCLATURA.md
- docs/contratos/contrato_composicao_corpo.md
- docs/contratos/contrato_barra_de_menus.md
- config/barra_de_menus.json
- docs/build_docs/to_do.md
- docs/contratos/contrato_lancador.md
- docs/contratos/contrato_cabecalho.md
- docs/contratos/contrato_estilo.md
- config/lancador.json
- config/layout_menu.json
- config/layout_dado.json
- config/cabecalho.json
- config/estilo.json
- docs/adr/ADR-0001-menu-suporta-matriz.md
- docs/adr/ADR-0002-menu-sobra-direita.md
- docs/adr/ADR-0003-vaos-elasticos-menu.md
- docs/adr/ADR-0004-estilo-cor-inativo-cor-alerta.md

## Evidências

### E-001 — JSON válido

`python -m json.tool config/barra_de_menus.json >/dev/null && echo "barra_de_menus.json OK"` retornou:

```text
barra_de_menus.json OK
```

### E-002 — Condição de [✥] restrita a dado

- `docs/NOMENCLATURA.md:280-283` registra que `[✥]` e as setas da `barra_de_menus` controlam somente cursor de corpo tipo `dado`.
- `docs/NOMENCLATURA.md:382` declara `[✥]` como condicional a tela com ao menos um corpo tipo `dado` navegável.
- `docs/contratos/contrato_barra_de_menus.md:144` declara `[✥]` como existente quando a tela possui ao menos um corpo tipo `dado` navegável.
- `docs/contratos/contrato_barra_de_menus.md:153-161` reforça a existência estrutural de `[✥]` vinculada a corpo tipo `dado` navegável.
- `config/barra_de_menus.json:87-90` restringe existência, estado dinâmico e comportamento de `navegar` a corpo tipo `dado` navegável.

### E-003 — lancador removido da navegabilidade por [✥]

- `docs/NOMENCLATURA.md:280-283` afirma que corpo tipo `lancador` possui navegação própria por itens via `tela_destino`, mas não é corpo navegável por `[✥]`.
- `docs/contratos/contrato_composicao_corpo.md:125-127` afirma que `lancador` não é corpo navegável por `[✥]` nem pelas setas da `barra_de_menus`.
- `docs/contratos/contrato_composicao_corpo.md:345-346` registra no checklist que corpo tipo `lancador` não deve ser tratado como corpo navegável por `[✥]`.

### E-004 — Info não navegável por [✥]

- `docs/NOMENCLATURA.md:280-283` registra que `Info` também não é corpo navegável por `[✥]`.
- Não foram encontradas ocorrências ativas afirmando que `Info` seja corpo navegável por `[✥]`.

### E-005 — Sem migração indevida console/dashboard

O grep por `console|dashboard` nos arquivos alvo não retornou ocorrências.
Não há evidência de aplicação indevida da futura renomeação `dado` -> `console` ou `Info` -> `dashboard`.

### E-006 — Escopo preservado

`git status --short` mostrou alterações nos alvos da aplicação e nos arquivos pré-existentes do DOC-0010:

```text
 M config/barra_de_menus.json
 M docs/INDICE.md
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/build_docs/to_do.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
?? docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
```

O diff/status dos arquivos que deveriam permanecer preservados não retornou alterações.
O diff dos arquivos alvo mostra a remoção de `tipo dado ou menu`/`tipo dado ou lancador` e a restrição de `[✥]` a corpo tipo `dado`, com a ressalva do achado ACHADO-001.

## Ocorrências remanescentes classificadas

| Arquivo:linha | Trecho | Classificação | Justificativa |
|---|---|---|---|
| docs/NOMENCLATURA.md:224 | navegacao via `[✥]` (setas do teclado) | OK — regra correta ativa | Está dentro da seção de mecanismos de seleção do corpo tipo `dado`. |
| docs/NOMENCLATURA.md:239 | Navegação por `[✥]` | OK — regra correta ativa | Título da seção de regra de navegação. |
| docs/NOMENCLATURA.md:241 | `[✥]` é a dica visual de "use as setas do teclado" | OK — regra correta ativa | Define o chip sem ampliar escopo para `lancador`. |
| docs/NOMENCLATURA.md:280 | Escopo de `[✥]` (ADR-0005) | OK — regra correta ativa | Inicia regra explícita da ADR-0005. |
| docs/NOMENCLATURA.md:283 | `lancador` ... não é corpo navegável por `[✥]`; `Info` também não é corpo navegável por `[✥]` | OK — menção negativa | Nega navegabilidade por `[✥]` para `lancador` e `Info`. |
| docs/NOMENCLATURA.md:372 | ordem fixa inclui `[✥]` | OK — regra correta ativa | Apenas posiciona o chip na ordem canônica. |
| docs/NOMENCLATURA.md:382 | tela possui ao menos um corpo tipo `dado` navegável | OK — regra correta ativa | Condição ativa restringida a `dado`. |
| docs/NOMENCLATURA.md:405 | `[⇆]` Alternar vs `[✥]` Navegar | OK — regra correta ativa | Distingue níveis de navegação. |
| docs/NOMENCLATURA.md:407 | `[✥]` move o cursor dentro do corpo em foco | OK — regra correta ativa | Deve ser lida com a regra de escopo da seção e da tabela, restrita a `dado`. |
| docs/contratos/contrato_composicao_corpo.md:126 | `lancador` não é corpo navegável por `[✥]` | OK — menção negativa | Está alinhado à ADR-0005. |
| docs/contratos/contrato_composicao_corpo.md:345 | `lancador` não é tratado como corpo navegável por `[✥]` | OK — menção negativa | Checklist confirma a exclusão do `lancador`. |
| docs/contratos/contrato_barra_de_menus.md:84 | lista de chips inclui `[✥]` | OK — regra correta ativa | Apenas enumera chip canônico. |
| docs/contratos/contrato_barra_de_menus.md:103 | ordem fixa inclui `[✥]` | OK — regra correta ativa | Apenas posiciona o chip na ordem canônica. |
| docs/contratos/contrato_barra_de_menus.md:143 | `[⇆]` ... não confundir com `[✥]` | OK — regra correta ativa | Distingue foco entre corpos de cursor interno. |
| docs/contratos/contrato_barra_de_menus.md:144 | tela possui ao menos um corpo tipo `dado` navegável | OK — regra correta ativa | Condição ativa correta para `[✥]`. |
| docs/contratos/contrato_barra_de_menus.md:153 | `[✥]` — existência estrutural vs estado dinâmico | OK — regra correta ativa | Subseção normativa da barra. |
| docs/contratos/contrato_barra_de_menus.md:154-161 | tela possui corpo tipo `dado` navegável; sem corpo tipo `dado`, `[✥]` não existe | OK — regra correta ativa | Reforça restrição a `dado`. |
| docs/contratos/contrato_barra_de_menus.md:168-170 | `[⇆]` muda foco; `[✥]` move cursor dentro do corpo | OK — regra correta ativa | Distinção conceitual; deve ser lida com a seção normativa anterior. |
| docs/contratos/contrato_barra_de_menus.md:327-330 | `[✥]` só existe estruturalmente quando a tela possui ao menos um corpo navegável | PENDENTE — texto ativo ainda ambíguo | Checklist não repete `tipo dado`; pode ser lido genericamente, embora não cite `lancador`/`menu`. |
| config/barra_de_menus.json:19 | `"navegar"` | OK — regra correta ativa | Chave canônica do chip. |
| config/barra_de_menus.json:81 | distinto de 'navegar' | OK — regra correta ativa | Distingue alternância entre corpos de navegação interna. |
| config/barra_de_menus.json:83 | `"navegar"` | OK — regra correta ativa | Objeto de configuração do chip. |
| config/barra_de_menus.json:84 | `"simbolo": "[✥]"` | OK — regra correta ativa | Símbolo canônico. |
| config/barra_de_menus.json:85 | `"rotulo": "Navegar"` | OK — regra correta ativa | Rótulo canônico. |
| config/barra_de_menus.json:87 | corpo tipo dado navegavel | OK — regra correta ativa | Existência estrutural restrita a `dado`. |
| config/barra_de_menus.json:89 | corpo tipo dado navegavel; nao e navegavel por [✥] | OK — regra correta ativa | Estado dinâmico restrito a `dado`. |

Greps sem ocorrências:

- `tipo dado ou menu`, `tipo dado ou lancador` e equivalentes: sem ocorrências.
- `console|dashboard`: sem ocorrências.

## Achados

- ACHADO-001
- Severidade: baixa
- Arquivo/linha: `docs/contratos/contrato_barra_de_menus.md:327-330`
- Descrição: o checklist final ainda usa a expressão genérica "ao menos um corpo navegável" para `[✥]`, sem repetir "tipo `dado`". O corpo principal do contrato está correto, mas esse item ativo permanece ambíguo.
- Ação recomendada: em correção documental posterior, alinhar o item do checklist para "ao menos um corpo tipo `dado` navegável".
- Status: aberto

## Conclusão

A aplicação da ADR-0005 está aprovada com ajuste documental local.
Não há achado bloqueante: `lancador` e `Info` não permanecem como corpos navegáveis por `[✥]`, a condição ativa de `[✥]` foi restringida a corpo tipo `dado`, não há ocorrência de `dado ou menu`/`dado ou lancador`, e não houve migração indevida para `console`/`dashboard`.
O único ajuste recomendado é remover a ambiguidade remanescente no checklist de `contrato_barra_de_menus.md`.
