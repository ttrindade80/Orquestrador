# Relatório de aplicação da ADR-0027

## 1. Identificação

```yaml
etapa_executada: APLICAR_ADR
adr: ADR-0027
arquivo_adr: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
data: "2026-07-17"
papel: autor_documental
handoff_relacionado: H-0036
qa_autorizador: docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
status_qa_autorizador: ADR_APPROVED
achados_obrigatorios_pendentes: 0
```

## 2. Autoridades utilizadas

Foram lidos integralmente antes de qualquer alteração:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0027.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md

docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md

docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md

docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
```

Lidos adicionalmente para preservar compatibilidade:

```text
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Autoridade local primária utilizada:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
```

O anexo externo `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md` não estava
disponível como arquivo local. A aplicação baseou-se no schema semântico
incorporado à própria ADR-0027 (D11, D13), conforme autorizado pelo QA
pós-patch, que declarou a ressalva como não bloqueante.

## 3. Estado Git inicial

```bash
cd "$(git rev-parse --show-toplevel)"
git status --short
git diff --name-only
git diff --check
git ls-files --others --exclude-standard
```

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
git_diff_check: sem_erros
modificados_rastreados:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
nao_rastreados_acumulados:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
arquivos_inesperados: []
```

O workspace contém artefatos acumulados da ADR-0026, ADR-0027 e H-0036.
Nenhum foi classificado como inesperado. Nenhum impediu distinguir o escopo
desta etapa.

## 4. Escopo autorizado

Arquivos autorizados para alteração:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md  [alterado]
docs/adr/INDICE_ADR.md                                                          [alterado]
docs/NOMENCLATURA.md                                                             [alterado]
docs/contratos/contrato_tela_json.md                                             [alterado]
docs/contratos/contrato_console.md                                               [alterado]
docs/contratos/contrato_json_console.md                                          [alterado]
```

Arquivo criado:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md                                 [criado]
```

Nenhum outro arquivo foi criado ou alterado.

## 5. Atualização do status da ADR-0027

**Arquivo:** `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`

Alterações realizadas:

| Local | Antes | Depois |
|---|---|---|
| Frontmatter `metadata.status` | `aceita` | `aceita e aplicada` |
| Tabela §1 campo Status | `aceita` | `aceita e aplicada` |
| Seção §2 (literal de status) | `` `aceita` `` | `` `aceita e aplicada` `` |

Preservados integralmente: decisões D1–D13, schema semântico (D11.1–D11.6),
validações (D13), exemplos, consequências, decisões deferidas, §7, §8, §9,
§13, §14, §15, §16, §17, §18.

Nenhuma referência histórica foi alterada.

## 6. Aplicação no índice de ADRs

**Arquivo:** `docs/adr/INDICE_ADR.md`

Adicionada a seguinte linha à tabela de decisões, após a ADR-0026:

```text
| ADR-0027 | Carregamento conjunto da tela e do conteúdo externo pelo ponto de
entrada — formaliza a responsabilidade do ponto de entrada real `demo/demo.py`
pelo carregamento separado do JSON estrutural e do JSON externo de conteúdo;
associação externa por cenário sem campo de vínculo no JSON estrutural; schema
semântico multinível obrigatório (`tipo: "multinivel"`, três apresentações, três
tipos de nível, forma dos nós, designadores, 20 validações mínimas); JSONs
permanentes para testes e demonstração; revisão dos JSONs afetados do H-0035
pelo H-0036; protocolo do Pipeline deferido | aceita e aplicada | 2026-07-17 |
```

Confirmações:

- número: ADR-0027 ✓
- título: correto ✓
- data: 2026-07-17 ✓
- status: `aceita e aplicada` ✓
- ordenação: após ADR-0026, antes do Exemplo de linha ✓
- entradas históricas: inalteradas ✓
- H-0036 não declarado como corrigido nem implementado ✓

## 7. Aplicação na nomenclatura

**Arquivo:** `docs/NOMENCLATURA.md`

Adicionada **seção 18** ao final do documento:

```text
## 18. Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada (ADR-0027)
```

Subseções criadas:

| Subseção | Conteúdo |
|---|---|
| 18.1 — Termos fundamentais do carregamento conjunto | `ponto de entrada da demonstração`, `associação externa por cenário`, `campo de vínculo`, `loader ou camada equivalente`, `fixture permanente de conteúdo`, `produtor futuro ligado ao Pipeline` |
| 18.2 — Schema semântico multinível | `schema semântico multinível`, `nível declarado`, `nó multinível`, `tipo de nível`, `nível container`, `nível conteudo`, `nível nome_valor`, `designador`, `apresentação declarada`; enumeração dos tipos de nível e apresentações |
| 18.3 — Princípio normativo central | Fluxo ponto de entrada → loader → modelo → renderizador |
| 18.4 — Fronteiras de responsabilidade | Tabela por componente |
| 18.5 — Distinções obrigatórias | 6 pares de distinção |
| 18.6 — Decisões deferidas | Tabela de 8 itens deferidos |

Nenhum alias normativo concorrente foi criado. Nenhum termo histórico foi
redefinido sem necessidade. As seções 1–17 permanecem intactas.

## 8. Aplicação no contrato de JSON estrutural da tela

**Arquivo:** `docs/contratos/contrato_tela_json.md`

Alterações realizadas:

1. Adicionada `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
   à lista `adrs_aplicadas` do frontmatter.

2. Adicionada **seção 32** ao final do documento:

```text
## 32. Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada (ADR-0027)
```

Subseções criadas:

| Subseção | Conteúdo |
|---|---|
| 32.1 — Fronteira do JSON estrutural | JSON permanece exclusivo e estrutural; não contém conteúdo de runtime; não possui campo de vínculo; não duplica conteúdo externo; associação ocorre externamente |
| 32.2 — Responsabilidade do ponto de entrada | 5 responsabilidades do `demo/demo.py` |
| 32.3 — Representação interna composta | Permitida depois da validação, com preservação da distinção de origens |
| 32.4 — Telas sem conteúdo externo | Comportamento histórico preservado; sem migração automática |
| 32.5 — Revisão dos JSONs do H-0035 | Delegada ao `PATCH_HANDOFF` do H-0036 |
| 32.6 — Remissões | Para seções 20 e 12 dos contratos e seção 18 da nomenclatura |

Seções históricas (1–31) permanecem inalteradas.

## 9. Aplicação no contrato do console

**Arquivo:** `docs/contratos/contrato_console.md`

Alterações realizadas:

1. Adicionada `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
   à lista `adrs_aplicadas` do frontmatter.

2. Adicionada **seção 20** ao final do documento:

```text
## 20. Fluxo de responsabilidade pelo carregamento e entrega do conteúdo externo (ADR-0027)
```

Subseções criadas:

| Subseção | Conteúdo |
|---|---|
| 20.1 — Ponto de entrada | Responsabilidades de `demo/demo.py`; obrigatoriedade para prova integrada; demos auxiliares permitidos |
| 20.2 — Loader ou camada equivalente | Leitura, validação, conversão; sem geometria; sem inferência |
| 20.3 — Modelo | Transporte semântico; preservação de ordem e hierarquia; composição interna permitida sem apagar origens |
| 20.4 — Renderizador | Resultados físicos; proibição de abrir JSONs, escolher arquivos ou reconstruir hierarquia |
| 20.5 — Demonstração real | Obrigatoriedade do `demo/demo.py`; JSONs permanentes; prova de identidade; código zero não basta |
| 20.6 — Fonte futura | Fixture no H-0036; Pipeline no produto final; protocolo deferido |
| 20.7 — Remissões | Para seções 32 e 12 dos contratos e seção 18 da nomenclatura |

Seções históricas (1–19) permanecem inalteradas.

## 10. Aplicação no contrato do JSON externo do console

**Arquivo:** `docs/contratos/contrato_json_console.md`

Alterações realizadas:

1. Adicionada `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
   à lista `adrs_aplicadas` do frontmatter.

2. **§11.2 atualizado**: o parágrafo final que declarava o exemplo como
   "conceitual" e remetia ao "futuro contrato do documento externo, o schema
   completo, as validações" foi substituído por texto que remete ao schema
   completo já formalizado na seção 12.

3. **§11.8 atualizado**: removido "schema completo e validações do documento
   externo" da lista de decisões deferidas; adicionado parágrafo explicando
   que esse ponto foi decidido pela ADR-0027 e está na seção 12.

4. Adicionada **seção 12** ao final do documento:

```text
## 12. Schema semântico multinível do documento externo de conteúdo (ADR-0027)
```

Subseções criadas:

| Subseção | Conteúdo |
|---|---|
| 12.1 — Envelope raiz obrigatório | Regras de `tipo`, `formato`, `dados`, `formato.apresentacao`, `formato.niveis`; proibição de inferência |
| 12.2 — Apresentações previstas | `tabela`, `hierarquia`, `conjuntos_campos`; blocos específicos por apresentação; compatibilidade dos blocos |
| 12.3 — Forma dos níveis | Campos `id`, `tipo`, `conteudo`, `designador`; tipos permitidos; `conteudo` por tipo; tipos de designador |
| 12.4 — Forma comum dos nós | Campos `id`, `nivel`; regras comuns; forma dos nós por tipo (`container`, `conteudo`, `nome_valor`) |
| 12.5 — Validações semânticas mínimas | 20 validações numeradas |
| 12.6 — Resultados físicos proibidos | Lista de 12 resultados proibidos no documento externo |
| 12.7 — Exemplo normativo de três níveis | Exemplo `conjunto → subconjunto → elemento nome_valor`; apresentação `conjuntos_campos` |
| 12.8 — Relação com as fixtures do H-0036 | Fixtures seguirão este contrato; caminhos definidos no handoff corrigido; sem diretório global definitivo |
| 12.9 — Relação com o Pipeline | Produtor futuro obedecerá este schema; troca de fonte não altera fronteira semântica; protocolo deferido |
| 12.10 — Remissões | Para seções 20 e 32 dos contratos e seção 18 da nomenclatura |

Seções históricas (1–11) permanecem inalteradas, com as atualizações pontuais
em §11.2 e §11.8 descritas acima.

## 11. Schema semântico multinível propagado

O schema formalizado na ADR-0027 D11 foi propagado integralmente para
`contrato_json_console.md` seção 12:

```yaml
envelope:
  - tipo: obrigatório, valor "multinivel"
  - formato: obrigatório, objeto
  - dados: obrigatório, array
  - formato.apresentacao: obrigatório
  - formato.niveis: obrigatório, array
apresentacoes:
  - tabela
  - hierarquia
  - conjuntos_campos
tipos_de_nivel:
  - container
  - conteudo
  - nome_valor
forma_dos_niveis:
  - id: string não vazia e única
  - tipo: do conjunto permitido
  - conteudo: campo semântico ou objeto nome/valor
  - designador: política declarativa
forma_dos_nos:
  - id: obrigatório
  - nivel: obrigatório, referencia nivel declarado
  - filhos: obrigatório em container
tipos_de_designador:
  - nenhum, simbolo, decimal, alfabetico_minusculo, alfabetico_maiusculo
  - romano_minusculo, romano_maiusculo, decimal_composto, personalizado
exemplo_normativo: três níveis (conjunto → subconjunto → elemento nome_valor)
```

## 12. Validações semânticas propagadas

As 20 validações semânticas mínimas da ADR-0027 D13 foram propagadas para
`contrato_json_console.md` §12.5:

1. raiz é objeto
2. presença e tipo correto de `tipo`
3. valor de `tipo` igual a `"multinivel"`
4. presença e tipo objeto de `formato`
5. presença e tipo array de `dados`
6. presença de `formato.apresentacao`
7. `formato.apresentacao` pertence ao conjunto permitido
8. presença e tipo array de `formato.niveis`
9. cada item de `formato.niveis` possui `id`, `tipo`, `conteudo` e `designador`
10. IDs de nível não vazios e não duplicados
11. tipos de nível pertencem ao conjunto permitido
12. cada nó possui `id` e `nivel`
13. `nivel` referencia declaração existente
14. nó `container` possui campo semântico e `filhos` como array
15. nó `conteudo` possui campo semântico declarado
16. nó `nome_valor` possui campos de nome e valor declarados
17. filhos validados recursivamente
18. ordem dos arrays preservada
19. blocos específicos compatíveis com a apresentação
20. ausência de resultados físicos calculados

## 13. Responsabilidade do demo.py propagada

A responsabilidade do `demo/demo.py` foi formalizada nos seguintes documentos:

| Documento | Seção | Conteúdo |
|---|---|---|
| `contrato_console.md` | §20.1 | Ponto de entrada obrigatório para demonstração integrada; 6 responsabilidades |
| `contrato_console.md` | §20.5 | Demonstração real: JSONs permanentes, prova de identidade, código zero não basta |
| `contrato_tela_json.md` | §32.2 | 5 responsabilidades do `demo/demo.py` como ponto de entrada |
| `docs/NOMENCLATURA.md` | §18.1 | Definição de `ponto de entrada da demonstração` |
| `docs/NOMENCLATURA.md` | §18.4 | Tabela de fronteiras de responsabilidade |

## 14. JSONs permanentes e revisão futura do H-0035

Formalizado nos contratos:

- `contrato_console.md` §20.5: demonstração deve usar JSONs permanentes
- `contrato_tela_json.md` §32.5: revisão dos JSONs do H-0035 afetados delegada
  ao `PATCH_HANDOFF` do H-0036, sem reabrir o ciclo fechado
- `contrato_json_console.md` §12.8: fixtures permanentes seguirão o schema;
  caminhos definidos nominalmente no handoff corrigido; sem diretório global
  definitivo de runtime

A lista nominal dos JSONs do H-0035 afetados não foi criada nesta etapa —
permanece para o `PATCH_HANDOFF`, como a ADR-0027 determina.

## 15. Fronteira futura com o Pipeline

Formalizado nos contratos:

- `contrato_console.md` §20.6: fonte futura via Pipeline; protocolo deferido
- `contrato_json_console.md` §12.9: produtor futuro obedecerá este schema;
  troca não altera fronteira semântica; protocolo e demais itens deferidos

Permanecem deferidos: protocolo, transporte, argumentos, códigos de saída,
timeout, autenticação, atualização, cache, versionamento, persistência.

## 16. Decisões preservadas como deferidas

| Decisão deferida | Autoridade |
|---|---|
| Nome de variável, classe, função, assinatura do mecanismo de associação | ADR-0027 §14; NOMENCLATURA §18.6 |
| Lista nominal dos JSONs do H-0035 afetados | ADR-0027 §14; contrato_tela_json §32.5 |
| Localização e nomes exatos das fixtures | ADR-0027 §14; contrato_json_console §12.8 |
| APIs e classes definitivas do consumidor/loader | ADR-0026 §14; ADR-0027 §14 |
| Forma de vínculo entre `tela.json` e documento externo no produto final | ADR-0026 §14; ADR-0027 §14 |
| Protocolo do script produtor futuro (todos os itens) | ADR-0027 §14; contrato_json_console §12.9 |
| Diretório global definitivo de dados de runtime do produto | ADR-0027 §14 |
| Suporte ao `tipo: "matriz"` no mecanismo | ADR-0026 §14; ADR-0027 §14 |
| Comportamento diante de fonte ausente ou inválida | ADR-0027 §14 |

## 17. Compatibilidade e preservações

Verificadas e confirmadas:

| Autoridade | Preservação |
|---|---|
| ADR-0025 e H-0035 | Distribuição matricial configurável de nível único permanece inalterada |
| ADR-0026 | Separação entre JSON estrutural e documento externo de conteúdo preservada e estendida; nenhuma decisão reescrita |
| Telas não afetadas | Comportamento histórico preservado; sem migração automática |
| Responsabilidade geométrica do renderizador | Geometria, quebras, truncamentos, alinhamentos, paginação e posições permanecem sob o renderizador |
| Comportamento sem conteúdo externo | Console sem conteúdo externo mantém comportamento histórico |
| Separação entre demo e produto | `demo/demo.py` como ponto de entrada da demonstração; `orquestrador.py` como ponto de entrada futuro do produto real |
| H-0035 não reaberto | O H-0035 permanece fechado; JSONs afetados serão revisados no H-0036 |
| H-0036 não alterado | O H-0036 permanece como artefato criado e reprovado, aguardando `PATCH_HANDOFF` |

## 18. Busca de resíduos

Documentos alteráveis foram inspecionados para as seguintes categorias:

| Formulação | Ocorrências encontradas | Classificação | Ação |
|---|---|---|---|
| `schema completo deferido` | `contrato_json_console.md §11.8` | ativa e contraditória com ADR-0027 | corrigida: removida da lista de deferidos; seção 12 foi adicionada |
| `validação de dados[] futura` | `contrato_json_console.md §11.8` | ativa e contraditória com ADR-0027 | corrigida: removida da lista de deferidos |
| `envelope mínimo apenas` | `contrato_json_console.md §11.2` | ativa e insuficiente | corrigida: adicionada referência ao schema completo na seção 12 |
| `demo dedicado` | não encontrada nos documentos alteráveis | não aplicável | nenhuma |
| `demo.py preservado` | não encontrada como resíduo ativo | não aplicável | nenhuma |
| `config/conteudo` | não encontrada nos documentos alteráveis | não aplicável | nenhuma |
| `campo de vínculo` | referências existentes são corretas (termo proibido definido) | ativa e coerente | nenhuma |
| `origem_dados` como vínculo | `contrato_json_console.md §11.6`: campo não é mecanismo final | ativa e coerente com ADR-0026; deferido preservado | nenhuma |
| `hierarquia inferida` | referências existentes proíbem inferência corretamente | ativa e coerente | nenhuma |
| `níveis inferidos` | referências existentes proíbem inferência corretamente | ativa e coerente | nenhuma |
| `renderizador abre arquivo` | não encontrada nos documentos alteráveis | não aplicável | nenhuma |
| `modelo escolhe arquivo` | não encontrada nos documentos alteráveis | não aplicável | nenhuma |
| `dados codificados em Python` | não encontrada nos documentos alteráveis | não aplicável | nenhuma |
| `tipo matriz` | `contrato_json_console.md §11.8`: suporte deferido (ADR-0026 §14) | ativa e coerente | preservada como deferida |

Resíduos ativos corrigidos: 3 (§11.2 e §11.8 do `contrato_json_console.md`).
Nenhuma referência histórica correta foi removida.

## 19. Arquivos alterados e criados

**Arquivos alterados (6):**

| Arquivo | Alterações |
|---|---|
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | Status atualizado em frontmatter, tabela §1 e seção §2 |
| `docs/adr/INDICE_ADR.md` | Linha da ADR-0027 adicionada na tabela |
| `docs/NOMENCLATURA.md` | Seção 18 adicionada (6 subseções, 15 termos novos) |
| `docs/contratos/contrato_tela_json.md` | ADR-0027 em `adrs_aplicadas`; seção 32 adicionada (6 subseções) |
| `docs/contratos/contrato_console.md` | ADR-0027 em `adrs_aplicadas`; seção 20 adicionada (7 subseções) |
| `docs/contratos/contrato_json_console.md` | ADR-0027 em `adrs_aplicadas`; §11.2 atualizado; §11.8 atualizado; seção 12 adicionada (10 subseções) |

**Arquivo criado (1):**

| Arquivo | Conteúdo |
|---|---|
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md` | Este relatório |

**Arquivos não alterados (preservados):**

```text
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md  ✓
docs/relatorios/RELATORIO_QA_ADR-0026.md                                  ✓
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md                           ✓
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md                        ✓
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md              ✓
docs/relatorios/RELATORIO_QA_ADR-0027.md                                  ✓
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md                        ✓
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md  ✓
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md                            ✓
docs/adr/ADR-0025-*.md                                                     ✓
docs/handoff/H-0035-*.md                                                   ✓
docs/relatorios/IMP-0035-*.md                                              ✓
demo/                                                                       ✓
config/                                                                     ✓
tela/                                                                       ✓
```

## 20. Verificações finais

```bash
cd "$(git rev-parse --show-toplevel)"
git diff --check                         # sem erros
git status --short                       # stage vazio; sem commit
git diff --name-only                     # 5 arquivos rastreados modificados
git ls-files --others --exclude-standard # arquivos não rastreados do ciclo
```

Confirmações nominais:

| # | Verificação | Resultado |
|---|---|---|
| 1 | ADR-0027 com status `aceita e aplicada` | ✓ confirmado em frontmatter, §1 e §2 |
| 2 | Índice coerente com a ADR | ✓ entrada adicionada com número, título, data e status corretos |
| 3 | Nomenclatura sem aliases concorrentes | ✓ seção 18 adicionada; termos distintos dos da seção 17 |
| 4 | JSON estrutural permanece sem conteúdo de runtime | ✓ §32.1 do `contrato_tela_json.md` |
| 5 | Nenhum campo de vínculo criado no `tela.json` | ✓ §32.1 proíbe explicitamente |
| 6 | `demo.py` definido como responsável pelo carregamento dos dois documentos | ✓ §32.2 e §20.1 |
| 7 | Loader, modelo e renderizador com fronteiras coerentes | ✓ §20.2, §20.3, §20.4 |
| 8 | Renderizador não abre arquivo | ✓ §20.4 |
| 9 | Modelo não escolhe fonte | ✓ §20.3 |
| 10 | Schema raiz propagado | ✓ §12.1 do `contrato_json_console.md` |
| 11 | Três apresentações propagadas | ✓ §12.2 |
| 12 | Três tipos de nível propagados | ✓ §12.3 |
| 13 | Forma dos níveis propagada | ✓ §12.3 |
| 14 | Forma dos nós propagada | ✓ §12.4 |
| 15 | Designadores propagados | ✓ §12.3 e `NOMENCLATURA §18.2` |
| 16 | 20 validações semânticas propagadas | ✓ §12.5 (numeradas 1–20) |
| 17 | Resultados físicos permanecem fora do documento | ✓ §12.6 |
| 18 | Fixtures formalizadas sem diretório global definitivo | ✓ §12.8 |
| 19 | Revisão dos JSONs do H-0035 preservada para o H-0036 | ✓ §32.5 e §12.8 |
| 20 | Protocolo do Pipeline permanece deferido | ✓ §12.9, §20.6 e §18.6 |
| 21 | H-0036 não alterado | ✓ arquivo não tocado |
| 22 | Nenhum JSON criado ou alterado | ✓ confirmado |
| 23 | `demo.py` não alterado | ✓ confirmado |
| 24 | Nenhum código ou teste alterado | ✓ confirmado |
| 25 | Somente arquivos autorizados modificados ou criados | ✓ confirmado |
| 26 | Relatórios de QA anteriores intactos | ✓ confirmado |
| 27 | Stage vazio | ✓ confirmado |
| 28 | Nenhum commit | ✓ confirmado |
| 29 | `git diff --check` sem erros | ✓ confirmado |

## 21. Classificação factual

```yaml
etapa_executada: APLICAR_ADR
adr: ADR-0027
status_literal: APLICACAO_CONCLUIDA
status_normalizado: >
  Aplicação documental da ADR-0027 concluída. Todos os contratos, o índice e a
  nomenclatura foram atualizados. O relatório de aplicação foi criado. Nenhum
  código, JSON ou handoff foi alterado. Stage vazio. Nenhum commit realizado.
relatorio: docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
documentos_alterados:
  - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  - docs/adr/INDICE_ADR.md
  - docs/NOMENCLATURA.md
  - docs/contratos/contrato_tela_json.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
documentos_criados:
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
schema_semantico_propagado: true
apresentacoes_propagadas:
  - tabela
  - hierarquia
  - conjuntos_campos
tipos_de_nivel_propagados:
  - container
  - conteudo
  - nome_valor
validacoes_semanticas_propagadas: 20
responsabilidade_demo_py_propagada: true
separacao_dos_documentos_propagada: true
jsons_permanentes_formalizados: true
revisao_H0035_preservada_para_handoff: true
fronteira_pipeline_preservada: true
decisoes_deferidas:
  - mecanismo de associação (nome de variável, classe, função, assinatura)
  - lista nominal dos JSONs do H-0035 afetados
  - localização e nomes exatos das fixtures
  - APIs e classes do consumidor/loader
  - protocolo completo do script produtor futuro
  - diretório global definitivo de runtime do produto
  - suporte ao tipo matriz no mecanismo
  - comportamento diante de fonte ausente ou inválida
residuos_conflitantes:
  - id: RES-01
    arquivo: docs/contratos/contrato_json_console.md
    secao: "§11.8"
    formulacao: schema completo e validações do documento externo como deferidos
    classificacao: ativa e contraditória com ADR-0027
    acao: corrigida
  - id: RES-02
    arquivo: docs/contratos/contrato_json_console.md
    secao: "§11.2"
    formulacao: envelope mínimo como único referente, sem schema completo
    classificacao: ativa e insuficiente
    acao: corrigida por adição de referência à seção 12
arquivos_inesperados: []
verificacoes:
  adr_status_atualizado: true
  indice_coerente: true
  nomenclatura_sem_aliases_concorrentes: true
  json_estrutural_sem_conteudo_runtime: true
  campo_vinculo_proibido: true
  demo_py_formalizado: true
  loader_modelo_renderizador_com_fronteiras: true
  renderizador_nao_abre_arquivo: true
  modelo_nao_escolhe_fonte: true
  schema_raiz_propagado: true
  tres_apresentacoes_propagadas: true
  tres_tipos_de_nivel_propagados: true
  forma_niveis_propagada: true
  forma_nos_propagada: true
  designadores_propagados: true
  vinte_validacoes_propagadas: true
  resultados_fisicos_fora_do_documento: true
  fixtures_formalizadas_sem_diretorio_global: true
  revisao_h0035_para_h0036: true
  protocolo_pipeline_deferido: true
  h0036_nao_alterado: true
  nenhum_json_criado_ou_alterado: true
  demo_py_nao_alterado: true
  nenhum_codigo_ou_teste_alterado: true
  somente_arquivos_autorizados: true
  relatorios_qa_intactos: true
  stage_vazio: true
  nenhum_commit: true
  git_diff_check_sem_erros: true
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
bloqueios: []
proxima_categoria: QA_APLICACAO_ADR
```
