---
name: RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON
description: QA documental e estrutural do primeiro draft real do JSON da tela raiz do Orquestrador
metadata:
  type: relatorio_qa
  doc_origem: DOC-B011
  status: APROVADO_COM_AJUSTES
  criado_em: 2026-07-07
---

# Relatório QA - DOC-B011 - Tela raiz do Orquestrador JSON

## Status final

`APROVADO_COM_AJUSTES`

O arquivo `config/telas/orquestrador.json` é JSON válido, respeita o caminho e
a identidade definidos pela ADR-0009, usa a estrutura macro exigida por
`contrato_tela_json.md` e mantém as pendências principais explícitas como
pendências. O draft não deve ser tratado como configuração executável final
enquanto os ajustes recomendados abaixo não forem resolvidos ou confirmados.

## Escopo verificado

- `config/telas/orquestrador.json`
- `docs/build_docs/to_do.md`
- ADR-0008 e ADR-0009
- contratos: `contrato_tela_json.md`, `contrato_composicao_corpo.md`,
  `contrato_console.md`, `contrato_lancador.md`,
  `contrato_barra_de_menus.md`, `contrato_chip.md`,
  `contrato_cabecalho.md`, `contrato_estilo.md`
- `docs/NOMENCLATURA.md`, seção 9

## Comandos executados

```bash
git status --short
python3 -m json.tool config/telas/orquestrador.json >/dev/null
git diff --check -- config/telas/orquestrador.json docs/build_docs/to_do.md
git diff -- config/telas/orquestrador.json docs/build_docs/to_do.md
```

Resultados:

- `python3 -m json.tool`: aprovado, sem saída.
- `git diff --check`: aprovado, sem saída.
- `git diff -- config/telas/orquestrador.json docs/build_docs/to_do.md`:
  mostrou apenas o diff rastreado de `docs/build_docs/to_do.md`; como
  `config/telas/orquestrador.json` está não rastreado, o conteúdo foi
  verificado por leitura direta.
- `git status --short`: a worktree já contém alterações acumuladas em ADRs,
  contratos, índices, relatórios e `config/telas/`. Esta QA não alterou esses
  artefatos.

## Evidências objetivas

### Caminho, identidade e schema

- O arquivo existe em `config/telas/orquestrador.json`.
- O JSON declara `"schema": "tela.v1"` e `"id": "orquestrador"`
  (`config/telas/orquestrador.json`, linhas 2-3).
- ADR-0009 define `config/telas/<id_da_tela>.json` como caminho canônico,
  exige coincidência entre `id` interno e nome base do arquivo e define
  `orquestrador` como identificador da tela raiz
  (`ADR-0009`, linhas 49-76).
- `contrato_tela_json.md` define `"schema": "tela.v1"` como versão obrigatória
  (`contrato_tela_json.md`, linhas 82-91).

### Estrutura macro

- `contrato_tela_json.md` exige `schema`, `id`, `cabecalho`, `corpo` e
  `barra_de_menus` (`contrato_tela_json.md`, linhas 56-78).
- O draft contém esses campos e ainda `metadados`, `filtros`, `bindings` e
  `referencias_de_acoes` (`config/telas/orquestrador.json`, linhas 1-246).

### Metadados e pendências

- O draft está marcado como `draft`, com origem `DOC-B011` e ADRs base
  `ADR-0008` e `ADR-0009` (`config/telas/orquestrador.json`, linhas 4-16).
- As pendências internas citam DOC-0018, DOC-B008, DOC-B009, DOC-B004, itens
  de `lancador`, origens de dados e destino do `chip_estilo`
  (`config/telas/orquestrador.json`, linhas 8-15).
- `to_do.md` mantém DOC-B008 e DOC-B009 como `bloqueado_decisao`
  (`to_do.md`, linhas 358-365), DOC-0018 como `pronto_para_execucao`
  (`to_do.md`, linhas 237-243) e DOC-B011 como concluído
  (`to_do.md`, linhas 374-380).

### Corpo

- `contrato_composicao_corpo.md` fecha a taxonomia do corpo em `console`,
  `lancador` e `dashboard` (`contrato_composicao_corpo.md`, linhas 64-81).
- O draft usa somente `console_principal`, `dashboard_info` e
  `lancador_principal` com tipos válidos (`config/telas/orquestrador.json`,
  linhas 24-103).
- Não há `menu`, `dado`, `info` como tipo de corpo, nem `barra_de_menus` dentro
  de `corpo.elementos[]`.
- `arranjo: sobreposto` está previsto no contrato de composição
  (`contrato_composicao_corpo.md`, linhas 131-139) e aparece no draft
  (`config/telas/orquestrador.json`, linha 23).

### Console principal

- O contrato exige `id`, `tipo = console`, título ou identificador visual,
  origem/binding ou regra de geração, políticas de composição, navegação,
  seleção, paginação e exibição (`contrato_console.md`, linhas 70-100).
- O draft declara esses campos para `console_principal`
  (`config/telas/orquestrador.json`, linhas 25-55).
- O draft não guarda página atual, item em foco, seleção atual, filtro ativo
  ou modo verboso atual. `modo_inicial: normal` é default declarativo, permitido
  por `contrato_tela_json.md` (`contrato_tela_json.md`, linhas 115-136).
- Filtro antes de paginação é regra contratual (`contrato_console.md`,
  linhas 284-302 e 306-329) e o filtro é declarado fora de estado de runtime
  (`config/telas/orquestrador.json`, linhas 232-238).

### Dashboard Info

- `NOMENCLATURA.md` define `dashboard` como passivo, não navegável por `[✥]`,
  sem `config/dashboard.json` universal e com instância declarada por tela
  (`NOMENCLATURA.md`, linhas 802-820).
- O draft usa `tipo: dashboard`, `posicao_dashboard: vertical`, `origem_dados`
  pendente e campos declarados na instância (`config/telas/orquestrador.json`,
  linhas 57-92).
- Os 8 campos do resumo, `Total` e os 8 marcadores correspondem à seção 9 de
  `NOMENCLATURA.md` (`NOMENCLATURA.md`, linhas 837-855) e ao draft
  (`config/telas/orquestrador.json`, linhas 66-91).

### Lancador principal

- O contrato exige `id`, `tipo = lancador`, `titulo`, `itens[]` e
  `layout/regras_exibicao` (`contrato_lancador.md`, linhas 59-121).
- O draft declara `lancador_principal` com esses campos
  (`config/telas/orquestrador.json`, linhas 94-103).
- `itens: []` está explicitamente marcado como pendência no próprio JSON e no
  `to_do.md`, sem inventar `tela_destino` (`config/telas/orquestrador.json`,
  linhas 12 e 102; `to_do.md`, linhas 374-380).
- Não há texto de item acima de 15 caracteres porque não há itens.

### Barra de menus e chips

- `contrato_barra_de_menus.md` define a barra como instância declarada no
  `tela.json`, com lista concreta de chips e sem hardcoding
  (`contrato_barra_de_menus.md`, linhas 96-128).
- `contrato_chip.md` exige campos mínimos de chip: `id`, `tipo`, `tecla`,
  `texto`, `acao` ou referência, `regra_existencia`, `regra_ativo` e
  `forma_exibicao` (`contrato_chip.md`, linhas 90-116).
- Todos os 11 chips do draft possuem os campos mínimos
  (`config/telas/orquestrador.json`, linhas 108-229).
- A ordem dos chips segue a ordem canônica
  `[Esc] -> [<][>] -> [-][+] -> [#] -> [⇆] -> [✥] -> [␣] -> [⏎] -> específicos -> [V] -> [?]`
  definida no contrato (`contrato_barra_de_menus.md`, linhas 172-184).
- Não há teclas duplicadas na lista declarada.
- `[✥]` aponta para `navegar_console`, com existência
  `tela_com_console_navegavel`, e não para `lancador` nem `dashboard`
  (`config/telas/orquestrador.json`, linhas 162-170).
- `[␣]`, `[<][>]`, `[-][+]`, `[#]`, `[⇆]` e `[V]` são justificados pelas
  capacidades declaradas no `console_principal` e pela existência de múltiplos
  elementos de corpo (`config/telas/orquestrador.json`, linhas 45-55 e
  122-218).
- `chip_estilo` está declarado como específico, tipo `aciona_tela`, com
  destino pendente explicitamente marcado (`config/telas/orquestrador.json`,
  linhas 195-209).

### Bindings, ações e estado de runtime

- `bindings` e `referencias_de_acoes` existem apenas como notas de pendência
  para DOC-B008/DOC-B009 (`config/telas/orquestrador.json`, linhas 240-245).
- Não há comando shell, chamada Python livre, classe hardcoded ou ação
  procedural arbitrária no JSON.
- As ações de chips são objetos declarativos com `tipo`; o registry formal
  ainda está pendente em DOC-B009, como declarado.
- O JSON não guarda página atual, item em foco, seleção atual, filtro ativo,
  modo verboso atual nem coluna atual ajustada em runtime.

## Problemas encontrados

### P1 - Registry de ações e tipos ainda pendente

O draft declara ações conceituais (`paginar`, `ajustar_colunas`,
`alternar_filtro`, `alternar_foco_corpo`, `navegar_console`,
`toggle_selecao`, `acao_por_item_em_foco`, `abrir_tela`, `toggle_estado`,
`abrir_ajuda`) antes de existir o registry formal de tipos e ações. Isso está
corretamente marcado como pendência em `metadados`, `bindings` e
`referencias_de_acoes`, então não reprova o draft, mas impede tratá-lo como
configuração validável final.

Evidência: `config/telas/orquestrador.json`, linhas 10, 240-245;
`to_do.md`, linhas 362-365.

### P2 - Colunas ajustáveis sem mínimo/máximo declarados

O draft habilita `colunas_ajustavel: "com"` e declara o chip `[-][+]`, mas
`contrato_console.md` afirma que, quando `colunas_ajustavel: com`, a instância
deve declarar número mínimo e número máximo. Esses campos não aparecem em
`console_principal`.

Evidência: `config/telas/orquestrador.json`, linhas 53 e 132-140;
`contrato_console.md`, linhas 333-348.

### P3 - Filtro de grupo com campo pendente

O filtro `filtro_grupo` referencia `campo: "pendente"`. O contrato exige que
filtros atuem sobre campos existentes nos dados vinculados. Como DOC-B009 ainda
está aberto e a pendência está explícita, isso é aceitável para draft, mas
deve ser resolvido antes de validação executável.

Evidência: `config/telas/orquestrador.json`, linhas 232-238;
`contrato_console.md`, linhas 284-302.

### P4 - `lancador_principal` sem itens

`itens: []` evita inventar telas destino, mas o contrato do `lancador` define
itens como lista de navegação para telas destino. Para draft documental, a
pendência está clara; para configuração final, será preciso declarar itens ou
decidir formalmente que a tela raiz pode ter `lancador` vazio.

Evidência: `config/telas/orquestrador.json`, linhas 94-103;
`to_do.md`, linhas 374-380.

## Ajustes recomendados

1. Formalizar em DOC-B009 o registry de ações usado pelos chips e pelas ações
   por item antes de considerar o JSON executável.
2. Completar a política de colunas do `console_principal` com mínimo/máximo,
   ou registrar uma exceção/adiamento explícito se esse detalhe pertencer ao
   futuro registry.
3. Substituir `filtro_grupo.campo: "pendente"` por campo real vinculado aos
   dados, quando DOC-B008/DOC-B009 forem fechados.
4. Definir os itens e `tela_destino` do `lancador_principal`, ou registrar em
   contrato/ADR que `itens: []` é permitido em draft ou em tela raiz sem
   destinos conhecidos.
5. Confirmar o destino de `chip_estilo` quando o ID da tela de estilo for
   documentado.

## Escopo de alterações desta QA

Esta QA criou somente:

- `docs/relatorios/RELATORIO_QA_DOC-B011_TELA_RAIZ_ORQUESTRADOR_JSON.md`

Esta QA não alterou:

- `config/telas/orquestrador.json`
- `docs/build_docs/to_do.md`
- contratos
- ADRs
- índices
- outros JSONs
- código

Observação: `git status --short` já apresentava alterações e arquivos não
rastreados fora deste relatório, associados ao ciclo documental anterior. Eles
foram lidos para verificação, mas não foram modificados por esta QA.
