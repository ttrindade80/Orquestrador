---
name: REL-DOC-DOC-0014-ADR-0007-APLICACAO
description: Auditoria documental da aplicação da ADR-0007 — tela de processamento como composição de tipos existentes
metadata:
  type: relatorio_qa
  status: APROVADO
  data: 2026-07-06
rastreabilidade:
  auditoria: "DOC-0014 / ADR-0007 aplicação"
  adr_relacionadas:
    - docs/adr/ADR-0007-tela-processamento-composicao.md
    - docs/adr/ADR-0006-renomeacao-console-dashboard.md
    - docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
  contratos_alvo:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
  documentos_alvo:
    - docs/NOMENCLATURA.md
    - docs/build_docs/to_do.md
---

# REL-DOC — QA DOC-0014 / Aplicação ADR-0007

## Revisão executada

Foi verificada a aplicação documental da ADR-0007 nos quatro arquivos esperados para DOC-0014. A auditoria conferiu se a tela de processamento foi registrada como composição de tipos existentes, sem abrir a taxonomia do corpo, sem deslocar chips específicos para o corpo e sem especificar itens fora de escopo.

Também foram executados os comandos obrigatórios de inspeção de status, diff, ocorrências textuais, alterações em JSON/config e diff de código.

## Status final

APROVADO

Não foram encontrados achados bloqueantes nem ajustes obrigatórios na aplicação da ADR-0007.

## Arquivos verificados

- docs/NOMENCLATURA.md
- docs/contratos/contrato_composicao_corpo.md
- docs/contratos/contrato_barra_de_menus.md
- docs/build_docs/to_do.md
- docs/adr/ADR-0007-tela-processamento-composicao.md
- docs/adr/ADR-0006-renomeacao-console-dashboard.md
- docs/adr/ADR-0005-lancador-nao-e-corpo-navegavel.md
- docs/adr/INDICE_ADR.md
- docs/INDICE.md
- docs/contratos/contrato_lancador.md
- docs/contratos/contrato_cabecalho.md
- docs/contratos/contrato_estilo.md
- config/*.json
- arquivos de código rastreados por extensões py/sh/js/ts/tsx/jsx/rs/go/java/c/cpp/h/hpp

## Evidências

### E-001 — Processamento não virou tipo de corpo

`docs/NOMENCLATURA.md:188-190` declara que tela de processamento não é tipo de corpo e que não existe quarto tipo de corpo para processamento.

`docs/contratos/contrato_composicao_corpo.md:70-71` registra a mesma regra: não existe quarto tipo além de `console`, `lancador` e `dashboard`.

### E-002 — Taxonomia fechada preservada

`docs/NOMENCLATURA.md:189-190` preserva a taxonomia fechada do corpo como `console`, `lancador`, `dashboard`.

`docs/contratos/contrato_composicao_corpo.md:70-71` confirma a mesma taxonomia contratual.

### E-003 — Composição de tela de processamento registrada

`docs/NOMENCLATURA.md:192-198` descreve a tela de processamento como composição com corpos tipo `console`, zero ou um `dashboard` e chips específicos declarados pela classe na `barra_de_menus`.

`docs/contratos/contrato_composicao_corpo.md:73-80` repete a composição: `console` para partes interativas/navegáveis, `dashboard` para saída passiva formatada e chips específicos fora do corpo.

### E-004 — Chips específicos permanecem na `barra_de_menus`

`docs/NOMENCLATURA.md:198-201` afirma que chips específicos pertencem à `barra_de_menus`, nunca ao corpo.

`docs/contratos/contrato_barra_de_menus.md:224-228` registra que ações próprias da classe, em tela de processamento, são chips específicos da `barra_de_menus`.

### E-005 — `barra_de_menus` permanece espelho

`docs/NOMENCLATURA.md:200-202` declara que a classe de tela decide e que a `barra_de_menus` é espelho, não fonte de decisão.

`docs/contratos/contrato_barra_de_menus.md:57-63` estabelece a regra geral de espelho e `docs/contratos/contrato_barra_de_menus.md:224-228` aplica essa regra ao caso de processamento.

### E-006 — `lancador` não representa processamento

`docs/NOMENCLATURA.md:204-205` afirma que `lancador` não representa processamento e continua sendo navegação para outras telas via `tela_destino`.

`docs/contratos/contrato_composicao_corpo.md:75-77` registra que `lancador` não representa processamento.

### E-007 — `[✥]` continua restrito a `console`

`docs/NOMENCLATURA.md:205-206` declara que nenhuma regra de `[✥]` muda e que `[✥]` continua restrito a corpo tipo `console`.

`docs/contratos/contrato_barra_de_menus.md:153-161` detalha que `[✥]` existe estruturalmente apenas quando há corpo tipo `console` navegável.

### E-008 — Fora de escopo preservado

`docs/NOMENCLATURA.md:215-217` deixa fora de escopo pop-up de ferramenta, seleção prévia de ferramenta, execução em segundo plano, estrutura do chip `aciona_processo`, renderer de progresso, implementação e alteração de dados reais.

`docs/contratos/contrato_composicao_corpo.md:84-86` declara que a seção não cria contrato detalhado de processamento nem define `aciona_processo`.

`docs/contratos/contrato_barra_de_menus.md:230-232` mantém `aciona_processo` fora de escopo e pendente.

### E-009 — Escopo de arquivos preservado

`git diff --name-only` retornou alterações acumuladas em JSONs, índices, ADRs e contratos, além dos arquivos-alvo. Isso é compatível com a observação do pedido de que o worktree já contém alterações acumuladas de DOC-0010, DOC-0011, DOC-0013 e DOC-0014.

Para DOC-0014, `docs/build_docs/to_do.md:195-205` lista como arquivos envolvidos apenas `docs/NOMENCLATURA.md`, `docs/contratos/contrato_composicao_corpo.md`, `docs/contratos/contrato_barra_de_menus.md` e `docs/build_docs/to_do.md`. O mesmo arquivo atribui as alterações em `config/barra_de_menus.json`, `config/layout_console.json` e `config/layout_dado.json` a DOC-0012 (`docs/build_docs/to_do.md:166-180`).

O comando de diff de código não retornou arquivos, indicando ausência de alteração em código rastreado pelas extensões verificadas.

## Ocorrências remanescentes classificadas

| Arquivo:linha | Trecho | Classificação | Justificativa |
|---|---|---|---|
| docs/NOMENCLATURA.md:190 | não existe quarto tipo de corpo para processamento | OK — menção negativa | A frase nega explicitamente a criação de quarto tipo. |
| docs/contratos/contrato_composicao_corpo.md:70-71 | Não existe quarto tipo além de `console`, `lancador` e `dashboard` | OK — menção negativa | Preserva a taxonomia fechada. |
| docs/NOMENCLATURA.md:192-198 | tela de processamento é descrita como composição de tipos existentes | OK — regra correta ativa | Registra composição por `console`, `dashboard` e chips específicos. |
| docs/NOMENCLATURA.md:200-202 | Chips específicos pertencem à `barra_de_menus`, nunca ao corpo | OK — regra correta ativa | Mantém chips fora do corpo e a barra como espelho. |
| docs/contratos/contrato_composicao_corpo.md:79-80 | Chips específicos ficam fora do corpo, na `barra_de_menus` | OK — regra correta ativa | Alinha contrato de composição à ADR-0007. |
| docs/contratos/contrato_barra_de_menus.md:224-228 | ações próprias da classe são chips específicos da `barra_de_menus` | OK — regra correta ativa | Confirma que a classe declara e a barra espelha. |
| docs/NOMENCLATURA.md:204-206 | `lancador` não representa processamento; `[✥]` restrito a `console` | OK — regra correta ativa | Evita uso de `lancador` como processamento e preserva `[✥]`. |
| docs/contratos/contrato_composicao_corpo.md:75-83 | `console`, `dashboard`, `lancador` e `[✥]` | OK — regra correta ativa | Define a composição e restringe `[✥]` a `console`. |
| docs/NOMENCLATURA.md:215-217 | pop-up, seleção prévia, segundo plano, `aciona_processo`, renderer de progresso | OK — fora de escopo | A enumeração aparece apenas como exclusão explícita da decisão. |
| docs/contratos/contrato_composicao_corpo.md:86 | não define `aciona_processo` | OK — fora de escopo | Mantém `aciona_processo` sem contrato na ADR-0007. |
| docs/contratos/contrato_barra_de_menus.md:230-232 | `aciona_processo` permanece fora de escopo e pendente | OK — fora de escopo | Não especifica execução; apenas preserva pendência. |
| docs/NOMENCLATURA.md:486 | um quarto tipo foi identificado | OK — referência existente/histórica | Refere-se aos tipos de chips específicos, não aos tipos de corpo. |
| docs/NOMENCLATURA.md:807-813 | `popup_execucao` em pendências | OK — fora de escopo | Pendência explícita; não é corpo/dashboard/barra_de_menus. |
| docs/build_docs/to_do.md:16 | ADRs, `config/*.json` | OK — referência existente/histórica | Descreve o escopo geral do backlog documental. |
| docs/build_docs/to_do.md:171-180 | JSONs em DOC-0012 | OK — referência existente/histórica | Atribui alterações de JSON à aplicação da ADR-0006, não à ADR-0007. |
| docs/build_docs/to_do.md:195-205 | DOC-0014 arquivos envolvidos e descrição | OK — regra correta ativa | Lista apenas os quatro arquivos esperados para aplicação da ADR-0007. |

## Achados

Nenhum achado bloqueante. Nenhum ajuste obrigatório.
