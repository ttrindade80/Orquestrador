---
name: RELATORIO_QA_H-0036_IMPLEMENTACAO
description: Auditoria independente da implementacao do H-0036 (fornecimento externo de dados ao console por JSON multinivel) — verificacao de escopo, codigo, JSONs, testes, smoke tecnico e fidelidade do relatorio de implementacao
metadata:
  type: relatorio_qa_implementacao
  id: QAI-0036
  handoff: H-0036
  data: "2026-07-17"
  etapa: QA_IMPLEMENTACAO
  status_literal: I5_MANUAL_VALIDATION_REQUIRED
---

# Relatório de QA da implementação do H-0036

> Auditoria independente da etapa `IMPLEMENTAR`. Não corrige a implementação,
> não altera o relatório de implementação, o handoff, ADRs, contratos, código,
> testes, JSONs ou demonstrações. Não aprova a validação visual em nome do
> usuário. Não prepara stage, não faz commit, não inicia fechamento nem ciclo.

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | RELATORIO_QA_H-0036_IMPLEMENTACAO |
| Handoff auditado | H-0036 (QA final do handoff `H1_HANDOFF_APPROVED`) |
| Relatório de implementação auditado | `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md` |
| Etapa | QA_IMPLEMENTACAO |
| Data | 2026-07-17 |
| Branch | master |
| HEAD | fb9e5be |
| Papel | Auditor independente da implementação |
| Classificação final | `I5_MANUAL_VALIDATION_REQUIRED` |

## 2. Escopo da auditoria

Auditoria integral da implementação do H-0036: estado Git, inventário autorizado,
diffs reais versus handoff, arquivos criados, validade e separação dos JSONs,
loader e as 20 validações semânticas, modelo, renderizador, três apresentações,
tipos de nível, designadores, catálogo do `demo.py`, preservação do H-0035,
suíte canônica (9 scripts), smoke tests técnicos, cenário sem conteúdo,
ausência de vazamento, escopo negativo, hardcoding/caches e fidelidade do
IMP-0036. A validação visual em TTY é exclusiva do usuário e não foi realizada
por este QA.

## 3. Autoridades examinadas

Lidas integralmente:

- `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` (1813 linhas);
- `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md`;
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0036_HANDOFF.md` (status `H1_HANDOFF_APPROVED`, próxima categoria `IMPLEMENTAR`);
- `docs/adr/ADR-0026-*`, `docs/adr/ADR-0027-*`;
- `docs/contratos/contrato_tela_json.md`, `contrato_console.md`, `contrato_json_console.md`;
- `docs/NOMENCLATURA.md`.

Ordem de autoridade aplicada: contratos ativos > ADR-0027 > ADR-0026 > H-0036
aprovado > relatórios como evidência histórica.

Observação sobre o arquivo do handoff: o bloco `§31` do próprio arquivo H-0036
ainda registra `qa_pos_segundo_patch: NAO_REALIZADO` e `proxima_categoria:
QA_HANDOFF`. Esse conteúdo é anterior ao executor (não foi atualizado após o
terceiro QA do handoff) e não é responsabilidade da implementação. O relatório
IMP-0036 cita corretamente `H1_HANDOFF_APPROVED`, confirmado pelo terceiro QA do
handoff. Não gera achado contra a implementação.

## 4. Estado Git inicial

```
branch: master
head: fb9e5be
git log -1: fb9e5be feat: implementa distribuicao matricial de nivel unico
stage (git diff --cached): vazio
commit novo: nao realizado
git diff --check: sem erros (saida vazia)
```

Confere com o estado declarado: `branch_esperada: master`, `head_esperado:
fb9e5be`, `stage_esperado: vazio`, `commit_novo_esperado: nao_realizado`.

### 4.1 Diferenciação da origem dos arquivos do workspace

| Categoria | Arquivos | Atribuição |
|---|---|---|
| Documentos anteriores ao executor (fase ADR) — MODIFICADOS | `docs/NOMENCLATURA.md`, `docs/adr/INDICE_ADR.md`, `docs/contratos/contrato_console.md`, `contrato_json_console.md`, `contrato_tela_json.md` | Aplicação da ADR-0026/0027 (pré-implementação) |
| Documentos anteriores ao executor — NÃO RASTREADOS | ADR-0026, ADR-0027, H-0036, `RELATORIO_*ADR-002{6,7}*`, `RELATORIO_QA_*H-0036*` (3 QAs do handoff) | Ciclos documentais ADR/handoff |
| Arquivos técnicos alterados pela implementação | 12 (ver §6) | Executor |
| Arquivos técnicos novos | 8 JSON + `demo/teste_demo_console.py` | Executor |
| Relatório da implementação | `docs/relatorios/IMP-0036-*.md` | Executor |
| Relatório criado por este QA | `docs/relatorios/RELATORIO_QA_H-0036_IMPLEMENTACAO.md` | Este QA |

As modificações em NOMENCLATURA, INDICE_ADR e contratos referem-se às seções que
o próprio handoff cita como já existentes (`contrato_json_console §12`,
`contrato_console §19/§20`, `contrato_tela_json §31/§32`), ou seja, foram
introduzidas antes da criação do handoff — logo, antes da implementação. O
IMP-0036 §3 declara explicitamente que esses documentos NÃO foram atribuídos à
implementação, não foram alterados nem restaurados. Como não há commits, a
autoria não é provável por Git isoladamente, mas o conteúdo é coerente com a
fase de aplicação de ADR e a lista nominal do executor os exclui.

```yaml
origem_dos_docs_modificados: fase_de_aplicacao_ADR (anterior ao executor)
produzido_pelo_executor: NAO (nao constam da lista nominal; conteudo pre-handoff)
```

Nenhum arquivo tecnicamente inesperado foi encontrado.

## 5. Inventário autorizado

Extraído do H-0036 §15.1:

```yaml
autorizados_para_ALTERAR: 13
autorizados_para_CRIAR: 10
total_autorizado: 23
caminhos_unicos: 23
duplicatas: 0
```

Confirmado contra o handoff. O 13º autorizado a ALTERAR é
`config/telas/demo/demo.json`, cuja autorização é **condicional** ("se o
mecanismo de catálogo do `demo.py` exigir entradas no JSON estrutural").

## 6. Arquivos alterados

Observados 12 alterados (todos autorizados a ALTERAR):

| Arquivo | Autorização | Estado observado | Aderente | Observação |
|---|---|---|---|---|
| `tela/loader.py` | ALTERAR | ALTERADO (+390) | sim | Carregamento + 20 validações do documento externo |
| `tela/modelo.py` | ALTERAR | ALTERADO (+172/-2) | sim | Representação semântica de origem separada |
| `tela/renderizador.py` | ALTERAR | ALTERADO (+322/-4) | sim | Três apresentações + designadores; placeholder preservado |
| `tela/teste_loader.py` | ALTERAR | ALTERADO (+208) | sim | 20 validações materiais |
| `tela/teste_modelo.py` | ALTERAR | ALTERADO (+115/-1) | sim | Entradas separadas, origens, ordem |
| `tela/teste_renderizador.py` | ALTERAR | ALTERADO (+126) | sim | Três apresentações, designadores, placeholder |
| `demo/demo.py` | ALTERAR | ALTERADO (+72/-4) | sim | Catálogo + carregamento duplo + argv |
| `demo/teste_demo.py` | ALTERAR | ALTERADO (+40) | sim | Regressão do catálogo |
| `demo/teste_diagnostico.py` | ALTERAR | ALTERADO (+59) | sim | Pipeline integrado H-0036 |
| `demo/teste_demo_distribuicao.py` | ALTERAR | ALTERADO (+89/-3) | sim | Carregamento separado nos cenários H-0035 |
| `config/telas/demo/h0035_console_com.json` | ALTERAR | ALTERADO (-14) | sim | `itens` removido; `distribuicao_matricial` preservada |
| `config/telas/demo/h0035_console_sem.json` | ALTERAR | ALTERADO (-10) | sim | `itens` removido; estrutura preservada |

`git diff --check`: sem erros. `git diff --numstat` bate com a tabela.

## 7. Arquivos criados

Observados 10 criados (todos autorizados a CRIAR):

| Arquivo | Autorização | Estado | JSON válido | Aderente |
|---|---|---|---|---|
| `config/telas/demo/h0036_console_hierarquia.json` | CRIAR | CRIADO | sim | sim (estrutural tela.v1) |
| `config/telas/demo/h0036_console_tabela.json` | CRIAR | CRIADO | sim | sim (estrutural tela.v1) |
| `config/telas/demo/h0036_console_conjuntos.json` | CRIAR | CRIADO | sim | sim (estrutural tela.v1) |
| `config/telas/demo/h0036_hierarquia_conteudo.json` | CRIAR | CRIADO | sim | sim (conteúdo externo) |
| `config/telas/demo/h0036_tabela_conteudo.json` | CRIAR | CRIADO | sim | sim (conteúdo externo) |
| `config/telas/demo/h0036_conjuntos_conteudo.json` | CRIAR | CRIADO | sim | sim (conteúdo externo) |
| `config/telas/demo/h0035_console_com_conteudo.json` | CRIAR | CRIADO | sim | sim (conteúdo externo) |
| `config/telas/demo/h0035_console_sem_conteudo.json` | CRIAR | CRIADO | sim | sim (conteúdo externo) |
| `demo/teste_demo_console.py` | CRIAR | CRIADO | n/a | sim (responsabilidade própria) |
| `docs/relatorios/IMP-0036-*.md` | CRIAR | CRIADO | n/a | sim (relatório) |

Nenhum arquivo obrigatório omitido; nenhum caminho substituído; nenhum nome
divergente; nenhum cache/temporário.

## 8. Arquivo autorizado não alterado

`config/telas/demo/demo.json` — **não alterado**, conforme declarado.

Auditoria da decisão (H-0036 §15.1, §17.2, §28.2):

1. A alteração era realmente **condicional** ("se o mecanismo de catálogo do
   `demo.py` exigir entradas no JSON estrutural") — confirmado no §15.1.
2. Condição que a exigiria: o mecanismo de catálogo precisar de entradas de
   launcher no JSON estrutural.
3. A solução adotada — catálogo interno `_CATALOGO_CONTEUDO_EXTERNO` no
   `demo.py` e seleção da tela inicial por argumento — **não** exige entradas no
   JSON estrutural. Condição não acionada. §17.2 permite explicitamente
   "argumento de linha de comando" como detalhe de implementação.
4. Os cenários H-0036 são acessíveis de modo permanente e reproduzível por
   `python demo/demo.py <id_tela>` (precedente já existente em
   `demo/demo_distribuicao.py <id_tela>`).
5. A validação manual de 12 passos permanece exequível (ver §32, com uma
   observação de método sobre os passos 11–12).
6. O retorno a um cenário sem conteúdo é feito por reinício sem argumento
   (`python demo/demo.py` → tela raiz `demo`, placeholder) — ver §32/QAI-0036-001.
7. A ausência de alteração preserva integralmente os testes históricos do
   launcher (`demo/teste_demo.py`, `demo/teste_explorar_barra_de_menus.py`
   verdes) e a identidade/finalidade do `demo.json` (§28.2).

Conclusão: a omissão é legítima e justificada; **não** constitui defeito. Nenhum
critério do handoff é impedido por ela.

## 9. Fidelidade do relatório de implementação

Comparação IMP-0036 × estado real:

| Item declarado | Declarado | Observado | Fiel |
|---|---|---|---|
| Autorizados (alterar/criar) | 13 / 10 | 13 / 10 | sim |
| Arquivos alterados | 12 | 12 | sim |
| Arquivos criados | 10 (9 + relatório) | 10 | sim |
| Autorizado não alterado | `demo.json` | `demo.json` | sim |
| 20 validações | 20 | 20 | sim |
| Fixtures externas | 5 | 5 | sim |
| JSONs estruturais novos | 3 | 3 | sim |
| Suíte | 2423 (9 scripts) | 2423 (9 scripts) | sim |
| Exceções operacionais | nenhuma | nenhuma | sim |
| Baseline | 8 scripts / 2235 | 2235 | sim |
| `git diff --check` | sem erros | sem erros | sim |
| Caches | nenhum | nenhum | sim |

As contagens por script do §28 do IMP conferem uma a uma (ver §26 deste
relatório). Não há divergência material. Relatório **fiel**.

## 10. Separação entre JSON estrutural e conteúdo

Verificação material dos seis JSONs (3 estruturais + 3 conteúdo do H-0036):

- Estruturais (`h0036_console_hierarquia|tabela|conjuntos.json`): apenas
  `schema: "tela.v1"`, `id`, `cabecalho`, `corpo` (um elemento console sem
  `itens`) e `barra_de_menus`. **Nenhum** campo de vínculo ao documento externo;
  **nenhum** conteúdo de runtime.
- Conteúdo (`h0036_*_conteudo.json`): apenas envelope `{tipo, formato, dados}`;
  **nenhuma** composição estrutural da tela; **nenhum** `schema: "tela.v1"`.
- Associação ocorre no ponto de entrada (`_CATALOGO_CONTEUDO_EXTERNO` no
  `demo.py`), nunca no JSON.
- Sem duplicação de dados entre estrutural e externo.
- Renderizador não lê arquivo (ver §14).

Mesma verificação aplicada aos dois cenários adaptados do H-0035: os `itens`
foram removidos do estrutural e migrados para os `_conteudo.json` (§19). Os dois
tipos não foram fundidos.

## 11. Loader e validação

`tela/loader.py` (adições, a partir da linha 1268):

- `carregar_conteudo_externo(caminho_base, id_conteudo, raiz_telas=None) -> dict`:
  abre, decodifica (`json.loads`), valida e devolve a representação semântica.
- `validar_conteudo_externo(documento, origem=...) -> dict`: executa as 20
  validações; exposto para testes em memória.
- Auxiliares: `_validar_no_conteudo` (recursivo), `_validar_designador_conteudo`,
  `_rejeitar_resultados_fisicos_conteudo` (recursivo).
- Constantes normativas: `APRESENTACOES_CONTEUDO_VALIDAS`,
  `TIPOS_NIVEL_CONTEUDO_VALIDOS`, `TIPOS_DESIGNADOR_VALIDOS`,
  `CAMPOS_RESULTADO_FISICO_PROIBIDOS`.
- Classes de erro **reutilizadas** (nenhuma nova): `TelaEstruturaInvalida`,
  `TelaCampoObrigatorioAusente`, `TelaJsonInvalido`, `TelaArquivoNaoEncontrado`.

Fronteira confirmada: o loader **não** calcula geometria, **não** renderiza,
**não** escolhe cenário, **não** abre o JSON estrutural como fonte de conteúdo,
**não** infere hierarquia (usa `filhos`) e **não** depende de caminho global
fixo (raiz parametrizada). Assinaturas coincidem com o IMP-0036 §9.

## 12. Vinte validações semânticas

Cada regra tem código nominal em `validar_conteudo_externo` (comentário numerado)
e teste material em `tela/teste_loader.py::teste_conteudo_externo_h0036`. O
helper `_rejeita` exige a **classe** correta de erro de domínio (exceção errada
ou ausência de exceção → falha), não apenas ausência de exceção; o esperado é
independente da saída do loader.

| # | Regra | Código | Teste material | Resultado |
|---|---|---|---|---|
| 1 | raiz objeto | `isinstance(documento, dict)` | rejeição não-objeto → `TelaEstruturaInvalida` | OK |
| 2 | `tipo` presente e string | checagem presença/tipo | ausente → `TelaCampoObrigatorioAusente`; não-string → `TelaEstruturaInvalida` | OK |
| 3 | `tipo == "multinivel"` | comparação | `!=` → `TelaEstruturaInvalida` | OK |
| 4 | `formato` presente e objeto | checagem | ausente/não-objeto rejeitados | OK |
| 5 | `dados` presente e array | checagem | ausente/não-array rejeitados | OK |
| 6 | `formato.apresentacao` presente | checagem | ausente → `TelaCampoObrigatorioAusente` | OK |
| 7 | apresentação válida | conjunto | inválida → `TelaEstruturaInvalida` | OK |
| 8 | `formato.niveis` presente e array | checagem | ausente/não-array rejeitados | OK |
| 9 | nível com id/tipo/conteudo/designador | laço de campos | falta campo → `TelaCampoObrigatorioAusente` | OK |
| 10 | IDs de nível não vazios e únicos | set `niveis_por_id` | vazio/duplicado → `TelaEstruturaInvalida` | OK |
| 11 | tipo de nível válido | conjunto | inválido → `TelaEstruturaInvalida` | OK |
| 12 | nó com id e nivel | `_validar_no_conteudo` | ausente → `TelaCampoObrigatorioAusente` | OK |
| 13 | `nivel` referencia nível declarado | `in niveis_por_id` | não declarado → `TelaEstruturaInvalida` | OK |
| 14 | `container`: campo + `filhos` array | ramo container | sem filhos/campo rejeitado | OK |
| 15 | `conteudo`: campo semântico | ramo conteudo | ausente → `TelaCampoObrigatorioAusente` | OK |
| 16 | `nome_valor`: nome e valor | ramo nome_valor | ausente → `TelaCampoObrigatorioAusente` | OK |
| 17 | filhos recursivos | recursão `_validar_no_conteudo` | filho inválido rejeitado recursivamente | OK |
| 18 | ordem preservada | não reordena | verificação material da ordem | OK |
| 19 | blocos compatíveis com apresentação | `_BLOCO_ESPECIFICO_POR_APRESENTACAO` | `tabela`/`campos` em `hierarquia` → `TelaEstruturaInvalida` | OK |
| 20 | sem resultados físicos | `_rejeitar_resultados_fisicos_conteudo` (recursivo) | raiz e aninhado → `TelaEstruturaInvalida` | OK |

Extras: `designador.tipo` inválido → `TelaEstruturaInvalida`; JSON inválido →
`TelaJsonInvalido`; ausente → `TelaArquivoNaoEncontrado`. As 5 fixtures
permanentes carregam com sucesso.

## 13. Modelo semântico

`tela/modelo.py` (adições):

- `NivelConteudo(id, tipo, conteudo, designador, _campos_inertes)`;
- `NoConteudo(id, nivel, campos, filhos)` — `filhos` preserva hierarquia e ordem;
- `ConteudoExterno(tipo, apresentacao, niveis, nos, formato, _raw)` com
  `nivel_por_id`;
- `construir_conteudo_externo`, `_construir_no_conteudo` (recursivo),
  `_propagar_conteudo_externo` (aos consoles, recursivo em grupos);
- `construir_modelo(tela_raw, conteudo_externo=None)`;
- campos `ModeloTela.conteudo_externo` e `ElementoCorpo.conteudo_externo`.

Confirmado: estrutura e conteúdo chegam **separados**; a origem permanece
distinguível (conteúdo tipado, nunca reinserido em `_raw` nem em
`_campos_inertes`); ordem e `filhos` preservados; três tipos de nível
transportados; o modelo **não** abre arquivo, **não** escolhe fonte, **não**
infere hierarquia e **não** calcula geometria. Coberto por
`tela/teste_modelo.py::teste_conteudo_externo_h0036_modelo` (186 verificações).

## 14. Renderizador

`tela/renderizador.py` (adições): `_linhas_console(elemento, content_w)` despacha
para `_linhas_conteudo_externo`, que roteia às três apresentações. Placeholder
histórico `"(console)"` preservado quando `conteudo_externo is None`.

Confirmado por inspeção de fonte: o renderizador **não** importa `json`, `os`,
`pathlib` nem `tela.loader`; **não** chama `open`/`read_text`/`json.load`; **não**
escolhe cenário; **não** contém conteúdo H-0036 hardcoded; **não** contém lista
fixa P01–P12; **não** reconstrói hierarquia por ID/nome (usa `filhos`).
Integração com a distribuição matricial preservada via
`_participantes_de_conteudo_externo` (achata em ordem de documento; a grade só
muda a célula, nunca a ordem).

## 15. Apresentações multinível

- `hierarquia` (`_linhas_apresentacao_hierarquia`): lista recuada por
  profundidade, designador por nível, recursiva por `filhos`.
- `tabela` (`_linhas_apresentacao_tabela`): cabeçalho + régua + colunas com
  larguras calculadas pelo renderizador; `ancestrais: "repetir"` repete os
  textos ancestrais como colunas iniciais.
- `conjuntos_campos` (`_linhas_apresentacao_conjuntos`): conjuntos (container +
  designador + título) com pares nome–valor justificados por conjunto e
  separador de `formato.campos`.

Cobertas por `teste_renderizador.py` (1223) e `teste_demo_console.py` (72),
sem placeholder com conteúdo e com placeholder sem conteúdo. Truncamento aplicado
como cálculo (largura respeitada), não vindo do JSON.

## 16. Tipos de nível e designadores

Tipos de nível: `container`, `conteudo`, `nome_valor` — implementados em
`_texto_no_conteudo` e nos ramos das apresentações.

Designadores (`_texto_designador`): `nenhum`, `simbolo`, `decimal`,
`alfabetico_minusculo`, `alfabetico_maiusculo`, `romano_minusculo`,
`romano_maiusculo`, `decimal_composto`, `personalizado`. Prefixo/sufixo/valor/
separador aplicados condicionalmente. Verificação de limites de conversão:

```
romano: 1=I 4=IV 9=IX 14=XIV 40=XL 90=XC 2024=MMXXIV
alfabetico (bijetivo): 1=a 26=z 27=aa 28=ab 52=az 53=ba ; maiusculo 27=AA
```

Conversões corretas nos limites (subtrativo romano; carry bijetivo alfabético).
O JSON declara a política; o renderizador calcula o marcador concreto (o
documento não armazena numeração pronta).

## 17. Associação por cenário no demo.py

`demo/demo.py`: `_CATALOGO_CONTEUDO_EXTERNO`, `id_conteudo_externo_de`,
`_carregar_modelo_por_id`, `_tela_inicial_de_argv`, `main(argv=None)`.

As cinco associações batem exatamente:

```yaml
h0036_console_hierarquia: h0036_hierarquia_conteudo
h0036_console_tabela:      h0036_tabela_conteudo
h0036_console_conjuntos:   h0036_conjuntos_conteudo
h0035_console_com:         h0035_console_com_conteudo
h0035_console_sem:         h0035_console_sem_conteudo
```

Confirmado: o ponto de entrada abre os dois arquivos separadamente; ausência de
conteúdo é explícita (chave ausente → `None`); conteúdo não vaza entre cenários
(cada chamada reconstrói o modelo do zero); a seleção por argumento não define
protocolo do produto final; **nenhum** campo de vínculo no JSON estrutural;
**nenhum** caminho global de runtime; **nenhum** conteúdo hardcoded.

## 18. JSONs e fixtures H-0036

Todos válidos (`python -m json.tool`). Fixtures principais:

- `h0036_hierarquia_conteudo.json`: 3 níveis (container, container, conteudo);
  designadores `decimal`, `decimal_composto`, `alfabetico_minusculo`; recursão
  por `filhos`; identidade exclusiva `"Fluxo H-0036 hierarquia"` e
  `"Documento H-0036 carregado pelo demo.py"` (contém a string `"H-0036"`).
- `h0036_tabela_conteudo.json`: bloco `tabela` (cabeçalho, `ancestrais:
  "repetir"`); tipos container + nome_valor; identidade `"tabela H-0036"`.
- `h0036_conjuntos_conteudo.json`: bloco `campos` (separador, justificação);
  container + nome_valor; identidade `"Parametros"`/`"Origens"` e valor
  `"H-0036"`.

Cobertura conjunta: 3 apresentações; 3 níveis; múltiplos nós em ≥2 níveis;
`container`/`conteudo`/`nome_valor`; `filhos`; ordem; designadores declarativos;
texto direto; par nome–valor; blocos específicos isolados por apresentação;
ausência de geometria. Identidade exclusiva por cenário distingue hierarquia,
tabela, conjuntos, `h0035_console_com` e `h0035_console_sem` (não apenas o
literal genérico `"H-0036"`).

## 19. Adaptação dos JSONs H-0035

`git diff` dos dois estruturais:

- `h0035_console_com.json`: removido apenas o array `itens` (12 itens `P01..P12
  linha`); preservados `titulo`, `overflow_normal` e `distribuicao_matricial`
  íntegros.
- `h0035_console_sem.json`: removido apenas o array `itens` (2 itens);
  preservados `titulo`, `overflow_normal`.

Fixtures externas correspondentes:

- `h0035_console_com_conteudo.json`: `tipo: "multinivel"`, apresentação
  `hierarquia`, nível único `conteudo` (`texto`), designador `nenhum`; 12 nós
  `P01 linha`..`P12 linha` com IDs `l01..l12` na ordem original.
- `h0035_console_sem_conteudo.json`: mesma forma; 2 nós `Linha alfa`, `Linha
  bravo` (IDs `l1`, `l2`), ordem preservada.

Sem duplicação: os textos estão **somente** nos documentos externos (ausentes do
estrutural — provado em `teste_demo_distribuicao.py::teste_separacao_h0036_console`).
A identidade histórica do H-0035 foi preservada, não substituída por conteúdo
genérico do H-0036.

## 20. Preservação dos 24 JSONs H-0035

`git diff --name-only -- config/telas/demo/` mostra somente os dois estruturais
alterados (`h0035_console_com.json`, `h0035_console_sem.json`). Os outros 24
`h0035_*.json` não aparecem em `git status` — preservados byte-a-byte.

```yaml
jsons_h0035_total: 26
jsons_h0035_adaptados: 2
jsons_h0035_preservados: 24
```

## 21. Testes do loader

`PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py` → 348/348, 0 falhas,
exit 0 (baseline 303, +45). Cobre as 20 validações (aceitação e rejeição por
classe), designador inválido, ordem material, JSON inválido, documento ausente e
carga das 5 fixtures permanentes. Esperados independentes (classe de erro exigida,
não derivada da saída).

## 22. Testes do modelo

`python tela/teste_modelo.py` → 186/186, 0 falhas, exit 0 (baseline 169, +17).
Cobre separação das entradas, origem distinta (não reinserção em `_raw`), ordem
de `dados` e `filhos`, níveis acessíveis, pais/filhos, três tipos de nível,
ausência de leitura de arquivo e ausência de geometria.

## 23. Testes do renderizador

`python tela/teste_renderizador.py` → 1223/1223, 0 falhas, exit 0 (baseline
1191, +32). Cobre três apresentações, designadores concretos (unitários),
hierarquia recursiva, nome–valor, tabela, placeholder presente/ausente,
truncamento como cálculo, redimensionamento, regressão H-0035 (grade DM com
externo) e inspeção de fonte (renderizador não abre arquivos).

## 24. Testes do demo e catálogo

- `python demo/teste_demo_console.py` (NOVO) → 72/72, 0 falhas, exit 0. Cobre:
  catálogo exato; ausência explícita; carregamento separado por cenário; tela
  estrutural e fixture corretas; identidade no externo e não no estrutural; três
  apresentações; troca de cenário sem vazamento (mesmo fluxo); smoke por cenário
  com esperado independente; ponto de entrada real por subprocess (com e sem
  argumento). Responsabilidade **própria** (fronteira = ponto de entrada +
  catálogo + subprocess); **não** é duplicação dos demais scripts.
- `python demo/teste_demo.py` → 363/363, 0 falhas (baseline 358, +5).
- `python demo/teste_diagnostico.py` → 48/48, 0 falhas (baseline 41, +7);
  pipeline integrado dos 5 cenários e cenário sem conteúdo.

## 25. Regressão da distribuição matricial

- `python tela/teste_distribuicao_matricial.py` → 36/36, 0 falhas, exit 0
  (inalterado).
- `python demo/teste_demo_distribuicao.py` → 109/109, 0 falhas (baseline 99,
  +10); `teste_separacao_h0036_console` prova: `itens` ausente do estrutural,
  associação no catálogo, contagem do externo (12/2), não-duplicação,
  `distribuicao_matricial` de `h0035_console_com` preservada, `h0035_console_sem`
  sem DM. Participantes externos P01–P12 usados na grade, ordem preservada.
  Nenhuma flexibilização indevida de teste histórico.
- `python demo/teste_explorar_barra_de_menus.py` → 38/38, 0 falhas, exit 0
  (canônico e verde, sem alteração).

## 26. Suíte canônica

Execução independente dos 9 scripts (`PYTHONDONTWRITEBYTECODE=1`, código de saída
verificado por script):

```yaml
- comando: python tela/teste_loader.py              ; aprovadas: 348  ; total: 348  ; falhas: 0 ; exit: 0
- comando: python tela/teste_modelo.py              ; aprovadas: 186  ; total: 186  ; falhas: 0 ; exit: 0
- comando: python tela/teste_renderizador.py        ; aprovadas: 1223 ; total: 1223 ; falhas: 0 ; exit: 0
- comando: python tela/teste_distribuicao_matricial.py; aprovadas: 36 ; total: 36   ; falhas: 0 ; exit: 0
- comando: python demo/teste_demo.py                ; aprovadas: 363  ; total: 363  ; falhas: 0 ; exit: 0
- comando: python demo/teste_diagnostico.py         ; aprovadas: 48   ; total: 48   ; falhas: 0 ; exit: 0
- comando: python demo/teste_demo_distribuicao.py   ; aprovadas: 109  ; total: 109  ; falhas: 0 ; exit: 0
- comando: python demo/teste_explorar_barra_de_menus.py; aprovadas: 38; total: 38   ; falhas: 0 ; exit: 0
- comando: python demo/teste_demo_console.py        ; aprovadas: 72   ; total: 72   ; falhas: 0 ; exit: 0
```

```yaml
total_observado: 2423
total_declarado_pelo_executor: 2423
coincide: true
baseline_anterior: 2235 (8 scripts)
crescimento: +188 (nenhuma verificação histórica removida; scripts anteriores permanecem verdes)
```

## 27. Smoke tests semânticos

Provados em `teste_demo_console.py` (matriz `_SMOKE` com esperado independente;
não usam apenas código de saída zero, ausência de exceção, nome de arquivo nem
snapshot da própria saída) e confirmados por subprocess real:

| cenário | estrutural | externo | identidade | incorreto ausente | placeholder | resultado |
|---|---|---|---|---|---|---|
| h0036_console_hierarquia | h0036_console_hierarquia | h0036_hierarquia_conteudo | `H-0036` / `Fluxo H-0036 hierarquia` | `Parametros` | AUSENTE | OK |
| h0036_console_tabela | h0036_console_tabela | h0036_tabela_conteudo | `tabela H-0036` / `Entradas` | `Fluxo H-0036 hierarquia` | AUSENTE | OK |
| h0036_console_conjuntos | h0036_console_conjuntos | h0036_conjuntos_conteudo | `Parametros` + `H-0036` | `Entradas` | AUSENTE | OK |
| h0035_console_com | h0035_console_com | h0035_console_com_conteudo | `P01 linha`..`P12 linha` | `Linha alfa` | AUSENTE | OK |
| h0035_console_sem | h0035_console_sem | h0035_console_sem_conteudo | `Linha alfa`/`Linha bravo` | `P01 linha` | AUSENTE | OK |
| sem conteúdo (demo / h0030_console_unico) | — | NENHUM | — | `H-0036` | PRESENTE | OK |

## 28. Cenário sem conteúdo e ausência de vazamento

Confirmado tecnicamente:

- Cenário sem conteúdo não abre fixture externa (chave ausente no catálogo →
  `None`; loader externo nem é chamado).
- Placeholder `"(console)"` presente; comportamento histórico preservado.
- Após abrir um cenário com conteúdo, abrir um sem conteúdo produz placeholder e
  `conteudo_externo is None`, sem a marca `"H-0036"` — provado em
  `teste_demo_console.py::teste_ausencia_de_mistura` usando o **mesmo fluxo** de
  reconstrução do modelo (linhas 179–185), que é exatamente o mecanismo acionado
  na troca de tela em sessão real (`_carregar_modelo_por_id` a cada mudança de
  `tela_atual`).
- Subprocess sem argumento: tela raiz `ORQUESTRADOR`, placeholder presente,
  `"H-0036"` ausente.

Ausência de vazamento confirmada tecnicamente. A observação visual permanece do
usuário.

## 29. Escopo negativo

Confirmada ausência de: script produtor do Pipeline; protocolo final; stdout como
protocolo; arquivo temporário de integração; autenticação; timeout; cache;
atualização automática; persistência; versionamento; suporte externo a `tipo:
"matriz"`; navegação/expansão/recolhimento/paginação interativa; alteração de
ADR/contrato/handoff; stage; commit.

Nota: as ocorrências de `"matriz"` no código pertencem à estrutura de grupo/
dashboard pré-existente (`ESTRUTURAS_GRUPO_VALIDAS`, layout matricial do
H-0030/H-0035), **não** ao tipo de conteúdo externo. Os documentos externos usam
exclusivamente `tipo: "multinivel"`. A distribuição matricial interna preservada
no cenário H-0035 não é suporte externo a `tipo: "matriz"`.

## 30. Hardcoding, caches e resíduos

- Busca por `H-0036`, `P01`, `P12`, `Linha alfa/bravo`, `Fluxo H-0036`,
  `Parametros` em código de produção (`loader.py`, `modelo.py`,
  `renderizador.py`, `demo.py`): **somente** em comentários/docstrings que
  referenciam o ciclo/ADR. **Nenhum** dado de fixture hardcoded em código de
  produção.
- `_CATALOGO_CONTEUDO_EXTERNO` contém IDs nominais de cenário (catálogo
  legítimo), não conteúdo.
- `TODO`/`FIXME`/`XXX`/`TEMP`/`HACK`: nenhum nos arquivos alterados.
- `find` por `__pycache__`/`*.pyc`: nenhum (execuções com
  `PYTHONDONTWRITEBYTECODE=1`).

Classificação: ocorrências de identidade em testes/fixtures são legítimas;
ocorrências em produção são comentários. Nenhum resíduo removido por este QA
(apenas registrado).

## 31. Demonstração técnica

`python demo/demo.py <cenario>` (fora de TTY, entrada `s`) confirmado por
subprocess em `teste_demo_console.py::teste_ponto_de_entrada_real` para os 5
cenários com conteúdo (exit 0, identidade material presente, placeholder ausente,
conteúdo de outro cenário ausente) e sem argumento (tela raiz, placeholder
presente, sem `"H-0036"`). Comandos reais observados:

```bash
python demo/demo.py h0036_console_hierarquia
python demo/demo.py h0036_console_tabela
python demo/demo.py h0036_console_conjuntos
python demo/demo.py h0035_console_com
python demo/demo.py h0035_console_sem
python demo/demo.py            # tela raiz (cenário sem conteúdo)
```

Esta execução técnica **não** substitui a observação visual do usuário em TTY.

## 32. Validação manual

Obrigatória e exclusiva do usuário (H-0036 §21). Este QA verificou o que é
verificável tecnicamente: existência das fixtures, comandos, rotas, identidade,
repetibilidade, testes automatizados, smoke técnico e preparo do roteiro. **Não**
aprova legibilidade, aspecto visual, maximização, restauração, redimensionamento
livre, quadro mínimo, recuperação visual nem ausência visual de resíduos.

Reprodutibilidade dos 12 passos:

| Passos | Rota | Reprodutível |
|---|---|---|
| 1–3 (abrir hierarquia, conferir identidade, conferir separação) | `python demo/demo.py h0036_console_hierarquia` + inspeção do estrutural | sim |
| 4–10 (maximizar/restaurar/reduzir/redimensionar/quadro mínimo/recuperar) | manipulação do terminal na mesma sessão | observação visual do usuário |
| 11 (retornar a cenário sem conteúdo) | reinício `python demo/demo.py` (tela raiz) — ver QAI-0036-001 | sim (por reinício) |
| 12 (ausência de vazamento) | tela raiz sem `"H-0036"` + `teste_demo_console` (in-session) | sim (técnico) / observação visual do usuário |

Estado: `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO`. A rota é reproduzível; o
não-vazamento in-session está tecnicamente provado (§28); resta a observação
visual, que é do usuário.

## 33. Achados

### QAI-0036-001

```yaml
id: QAI-0036-001
severidade: observacao
classificacao_da_causa: METODO_DE_VALIDACAO_INSUFICIENTE
arquivo: demo/demo.py ; config/telas/demo/demo.json (nao alterado) ; docs/handoff/H-0036 §21.3
linha_ou_secao: navegacao (demo.py §atualizar_por_tecla) ; roteiro manual passos 11-12
autoridade_afetada: H-0036 §21.3 (roteiro), §17.2 (argumento permitido), §28.2 (demo.json condicional)
evidencia: >
  Os cenarios H-0036 (hierarquia/tabela/conjuntos) e os H-0035 com conteudo sao
  acessiveis apenas por argumento (python demo/demo.py <id>), pois o launcher do
  demo.json (nao alterado, condicao nao acionada) so navega para cenarios sem
  conteudo (h0030_*, destino/grupo_minimo). Abertos por argumento, esses
  cenarios tem pilha_telas vazia e suas telas nao possuem elemento lancador;
  Esc com pilha vazia encerra a sessao. Logo, o retorno a um cenario sem
  conteudo (passo 11) e feito por REINICIO do processo, nao por navegacao
  in-session a partir da fixture principal H-0036.
impacto: >
  A prova VISUAL de ausencia de vazamento in-session (conteudo -> sem conteudo na
  mesma sessao rodando) nao e obtida a partir da fixture principal H-0036; o
  usuario a verifica por reinicio (processo novo, trivialmente sem vazamento). O
  nao-vazamento in-session esta provado no teste automatizado
  teste_demo_console.py (mesmo fluxo de reconstrucao do modelo). A rota manual
  permanece REPRODUZIVEL. Nao bloqueia.
correcao_necessaria: >
  Nenhuma correcao obrigatoria nesta etapa. Observacao para ciencia do usuario
  ao executar a validacao manual: o passo 11 usa reinicio sem argumento. Caso se
  deseje navegacao in-session ate os cenarios H-0036, seria necessario decidir
  (em ciclo futuro) incluir entradas no launcher (demo.json) — fora do escopo
  desta implementacao, cuja abordagem por argumento e explicitamente permitida
  pelo handoff §17.2 e cujo demo.json era de alteracao condicional.
```

Nenhum outro achado. Nenhum achado bloqueante, alto, médio ou baixo.

## 34. Observações

- O arquivo do handoff (§31) mantém metadados desatualizados
  (`qa_pos_segundo_patch: NAO_REALIZADO`), anteriores ao executor; o QA final
  real do handoff é `H1_HANDOFF_APPROVED` (terceiro QA). Não afeta a
  implementação nem esta auditoria.
- Modificações em NOMENCLATURA/INDICE_ADR/contratos no workspace pertencem à
  fase de aplicação de ADR (anteriores ao executor); não atribuídas à
  implementação (§4.1).
- A implementação é aderente, coesa e dentro do escopo; as fronteiras
  (loader/modelo/renderizador/demo) estão respeitadas; nenhuma classe de erro
  nova foi inventada; nenhum diretório global de runtime foi criado.

## 35. Classificação final

```yaml
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: Auditoria tecnica aprovada; pendente validacao visual em TTY (exclusiva do usuario)
relatorio: docs/relatorios/RELATORIO_QA_H-0036_IMPLEMENTACAO.md

achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 1   # QAI-0036-001 (METODO_DE_VALIDACAO_INSUFICIENTE, nao bloqueante)

escopo_autorizado_confirmado: true
arquivos_autorizados_alterar: 13
arquivos_autorizados_criar: 10
arquivos_alterados_confirmados: 12
arquivos_criados_confirmados: 10
arquivo_autorizado_nao_alterado_confirmado: config/telas/demo/demo.json
arquivos_inesperados: nenhum

separacao_dos_documentos_confirmada: true
mecanismo_demo_py_confirmado: true   # _CATALOGO_CONTEUDO_EXTERNO, _carregar_modelo_por_id, id_conteudo_externo_de, _tela_inicial_de_argv
associacoes_confirmadas: 5
schema_confirmado: multinivel
apresentacoes_confirmadas: [tabela, hierarquia, conjuntos_campos]
tipos_de_nivel_confirmados: [container, conteudo, nome_valor]
designadores_confirmados: [nenhum, simbolo, decimal, alfabetico_minusculo, alfabetico_maiusculo, romano_minusculo, romano_maiusculo, decimal_composto, personalizado]
validacoes_confirmadas: 20

inventario_H0035_confirmado: true
jsons_H0035_adaptados: 2
jsons_H0035_preservados: 24
identidade_H0035_preservada: true

fixtures_confirmadas: 5
jsons_estruturais_confirmados: 3
smoke_tests_confirmados: true
cenario_sem_conteudo_confirmado: true
ausencia_de_vazamento_confirmada: true   # tecnica (in-session + subprocess)

baseline_confirmado: 2235   # 8 scripts
suite_final_confirmada: 2423 # 9 scripts
total_verificacoes_observado: 2423

relatorio_implementacao_fiel: true
escopo_negativo_preservado: true
caches_ou_temporarios: nenhum
excecoes_operacionais: nenhuma

validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
implementacao_tecnicamente_aprovada: true
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  git_diff_check: sem_erros
proxima_categoria: VALIDACAO_MANUAL
```
