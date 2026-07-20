---
name: RELATORIO_APLICACAO_ADR-0028
description: Relatório factual da aplicação documental da ADR-0028 aos documentos normativos ativos do projeto
metadata:
  type: relatorio_aplicacao
  adr: ADR-0028
  data: "2026-07-17"
  status: APLICACAO_CONCLUIDA
---

# Relatório de Aplicação — ADR-0028

## 1. Objetivo

Aplicar as decisões aprovadas da ADR-0028 aos documentos normativos ativos do
projeto Orquestrador. A aplicação é exclusivamente documental: nenhum código,
configuração, fixture, handoff ou QA foi produzido nesta etapa.

O escopo normativo da ADR-0028 é exclusivamente conteúdo multinível exibido em
componentes do tipo `console`.

---

## 2. Autoridades

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | ADR aplicada; fonte primária das decisões D1–D22 |
| `docs/relatorios/RELATORIO_QA_ADR-0028.md` | QA inicial — status `ADR_REJECTED`; quatro achados corretivos (QA-001 a QA-004) |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | QA pós-patch — status `ADR_APPROVED_WITH_NOTES`; QA-001 a QA-004 corrigidos; QA-005 e QA-006 como observações não corretivas; autoriza `APPLY_ADR` |
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | Autoridade ativa sobre separação JSON estrutural/externo; envelope `{tipo, formato, dados}` |
| `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md` | Autoridade ativa sobre carregamento separado, entrega conjunta, schema semântico multinível e 20 validações mínimas |

---

## 3. Estado Git inicial

| Campo | Valor |
|---|---|
| Branch | master |
| HEAD | f6982d0 |
| Mensagem do commit | docs: corrige whitespace do fechamento H-0036 |
| Workspace | LIMPO |
| Stage | VAZIO |
| Arquivos não rastreados presentes | `docs/adr/ADR-0028-...md`, `docs/relatorios/RELATORIO_QA_ADR-0028.md`, `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` |

Os três arquivos não rastreados são os documentos produzidos nas etapas
anteriores (ADR, QA e QA pós-patch). Nenhum arquivo de código ou configuração
estava modificado.

---

## 4. Arquivos alterados

| Arquivo | Tipo de alteração |
|---|---|
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Status atualizado para `aceita e aplicada`; §2 atualizado; §47 com entrada de aplicação |
| `docs/adr/INDICE_ADR.md` | Nova linha de ADR-0028 na tabela de decisões |
| `docs/NOMENCLATURA.md` | Nova seção 19 (ADR-0028) |
| `docs/contratos/contrato_json_console.md` | Nova seção 13 (ADR-0028) |
| `docs/contratos/contrato_console.md` | Nova seção 21 (ADR-0028) |
| `docs/contratos/contrato_tela_json.md` | Nova seção 33 (ADR-0028) |
| `docs/contratos/contrato_composicao_corpo.md` | Nova seção 12 (ADR-0028) |
| `docs/contratos/contrato_barra_de_menus.md` | Nova seção 22 (ADR-0028) |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` | Criado (este arquivo) |

Nenhum arquivo de código, configuração, fixture ou teste foi alterado.

---

## 5. Decisões propagadas

A tabela abaixo mapeia cada decisão da ADR-0028 às seções normativas em que
foi propagada.

| Decisão ADR-0028 | Resumo | Propagada em |
|---|---|---|
| D1 — Conteúdo externo ao JSON estrutural | Dados multinível permanecem separados do JSON estrutural | `contrato_tela_json.md` §33.1; `contrato_console.md` §21.1 |
| D2 — Documento JSON como fronteira de consumo | Console recebe documento JSON com mesma estrutura independente da origem | `contrato_json_console.md` §13.1; `contrato_console.md` §21.1 |
| D3 — Carregamento separado e entrega conjunta | Ponto de entrada carrega separado, entrega conjunto, sem fusão | `contrato_json_console.md` §13.10; `contrato_tela_json.md` §33.3 |
| D4 — Estrutura independente da apresentação | Mesmos dados servem a tabela, hierarquia ou conjuntos | `contrato_json_console.md` §13.4 |
| D5 — Designadores independentes da estrutura | Troca de designador não altera dados ou níveis | `docs/NOMENCLATURA.md` §19.2 (`designador`) |
| D6 — Estrutura hierárquica declarada | Raiz única, identificadores, relações, tipos declarados | `contrato_json_console.md` §13.2 |
| D7 — Tipos conceituais de níveis | Contêiner, folha, campo; correspondência com schema do projeto | `contrato_json_console.md` §13.3; `docs/NOMENCLATURA.md` §19.2 |
| D8 — Cenários de apresentação multinível | Quatro cenários obrigatórios de demonstração | `contrato_json_console.md` §13.11 |
| D9 — Modo não verboso | Uma linha física por conteúdo; truncamento do excedente | `contrato_json_console.md` §13.5; `contrato_console.md` §21.2; `docs/NOMENCLATURA.md` §19.2 |
| D10 — Modo verboso | Múltiplas linhas físicas; quebras pelo renderizador | `contrato_json_console.md` §13.6; `contrato_console.md` §21.3; `docs/NOMENCLATURA.md` §19.2 |
| D11 — Alternância pela tecla V | V alterna modos; reversível; sem persistência; sem troca de dados | `contrato_console.md` §21.5; `contrato_barra_de_menus.md` §22.2 |
| D12 — Modo inicial | Vem do campo de excesso do documento externo; ausência = comportamento indefinido | `contrato_console.md` §21.7; `docs/NOMENCLATURA.md` §19.2 (`modo inicial`) |
| D13 — Conteúdo declarativo do JSON | JSON declara semântica e políticas; não contém resultados físicos | `contrato_json_console.md` §13.5–13.6; `contrato_tela_json.md` §33.2 |
| D14 — Responsabilidade do renderizador | Renderizador calcula tudo físico; não abre arquivos | `contrato_json_console.md` §13.10; `contrato_composicao_corpo.md` §12.1–12.5 |
| D15 — Tabela multinível | Regras da tabela conforme §17 da ADR | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 |
| D16 — Hierarquia indentada | Regras da hierarquia conforme §18 da ADR | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 |
| D17 — Conjuntos e campos | Regras dos cenários de 2 e 3 níveis conforme §§19–20 da ADR | `contrato_json_console.md` §13.4; `docs/NOMENCLATURA.md` §19.2 |
| D18 — Quebra de palavras | Política declarada para palavras maiores que largura disponível | `contrato_json_console.md` §13.6 (política final declarada) |
| D19 — Paginação e contexto | Preservação de contexto por modo de apresentação | `contrato_json_console.md` §13.7; `contrato_composicao_corpo.md` §12.3; `docs/NOMENCLATURA.md` §19.2 (`contexto visual repetido`) |
| D20 — Impossibilidade geométrica | Política aplicada via ADR-0017/ADR-0023; paginação não resolve horizontal | `contrato_json_console.md` §13.8; `contrato_composicao_corpo.md` §12.4; `contrato_console.md` §21.9; `docs/NOMENCLATURA.md` §19.2 |
| D21 — Validações | V-01 a V-15 obrigatórias; complementam 20 da ADR-0027 | `contrato_json_console.md` §13.9 |
| D22 — Demonstração e validação | Fixtures permanentes e provas semânticas para futura implementação | `contrato_json_console.md` §13.11 |

---

## 6. Aplicação por documento

### 6.1 ADR-0028

- `metadata.status` atualizado para `aceita e aplicada`
- §1 tabela de identificação: campo Status atualizado
- §2 Status: texto atualizado; pointer para este relatório adicionado
- §47 Histórico de alterações: nova linha de aplicação documental

### 6.2 INDICE_ADR.md

Nova linha adicionada à tabela de decisões registradas:

```
ADR-0028 | [descrição resumida] | aceita e aplicada | 2026-07-17
```

### 6.3 NOMENCLATURA.md — seção 19

Nova seção com:
- §19.1 Escopo (exclusivo ao `console` com conteúdo multinível)
- §19.2 Termos principais (17 termos: `conteúdo multinível do console`, `documento JSON externo de conteúdo`, `modo não verboso`, `modo verboso`, `alternância por V`, `estado visual da sessão`, `modo inicial`, `linha lógica`, `linha física`, `contexto visual repetido`, `contêiner`, `folha`, `campo nome-valor`, `designador`, `escopo de alinhamento`, `[V] Verboso`, `impossibilidade geométrica (multinível)`)
- §19.3 Diferenças terminológicas registradas (não resolvidas): `folha`/`conteudo`, `campo`/`nome_valor`, `hierarquia_indentada`/`hierarquia`
- §19.4 `modo normal` × `modo não verboso`: equivalência conceitual registrada sem resolução
- §19.5 Distinções obrigatórias
- §19.6 Decisões deferidas (8 itens)

### 6.4 contrato_json_console.md — seção 13

Nova seção com:
- §13.1 Escopo (exclusivo ao `console` com conteúdo multinível)
- §13.2 Modelo hierárquico
- §13.3 Tipos conceituais de nível (tabela com correspondência ao schema)
- §13.4 Modos de apresentação (tabela, hierarquia, conjuntos_campos)
- §13.5 Modo não verboso
- §13.6 Modo verboso
- §13.7 Paginação e contexto (por apresentação)
- §13.8 Impossibilidade geométrica
- §13.9 Validações V-01 a V-15 (tabela completa)
- §13.10 Responsabilidades das camadas (tabela)
- §13.11 Cenários de demonstração obrigatórios (D8)
- §13.12 Remissões

### 6.5 contrato_console.md — seção 21

Nova seção com:
- §21.1 Escopo exclusivo
- §21.2 Modo não verboso
- §21.3 Modo verboso
- §21.4 Relação com `modo normal` (equivalência conceitual registrada sem resolução)
- §21.5 Alternância pela tecla V
- §21.6 Estado visual da sessão (lista de proibições)
- §21.7 Modo inicial (campo `excesso`; ausência = comportamento indefinido)
- §21.8 Redimensionamento
- §21.9 Paginação e impossibilidade geométrica
- §21.10 Remissões

### 6.6 contrato_tela_json.md — seção 33

Nova seção com:
- §33.1 O JSON estrutural não contém dados de conteúdo
- §33.2 O JSON estrutural não armazena modo de visualização
- §33.3 Associação feita pelo ponto de entrada
- §33.4 Responsabilidades preservadas
- §33.5 Remissões

### 6.7 contrato_composicao_corpo.md — seção 12

Nova seção com:
- §12.1 Área útil entregue ao console
- §12.2 Linha lógica e linha física (tabela de definições)
- §12.3 Paginação vertical
- §12.4 Impossibilidade geométrica horizontal
- §12.5 Recuperação após redimensionamento
- §12.6 Separação de responsabilidades (tabela)
- §12.7 Remissões

### 6.8 contrato_barra_de_menus.md — seção 22

Nova seção com:
- §22.1 Existência condicional
- §22.2 Semântica da alternância
- §22.3 Estado de sessão
- §22.4 Isolamento
- §22.5 Inaplicabilidade fora do escopo
- §22.6 Posição canônica
- §22.7 Remissões

---

## 7. Termos incluídos na NOMENCLATURA.md

Seção 19 criada com os seguintes termos novos (§19.2):

1. `conteúdo multinível do console`
2. `documento JSON externo de conteúdo`
3. `modo não verboso`
4. `modo verboso`
5. `alternância por V`
6. `estado visual da sessão`
7. `modo inicial`
8. `linha lógica`
9. `linha física`
10. `contexto visual repetido`
11. `contêiner` (tipo conceitual)
12. `folha` (tipo conceitual)
13. `campo nome-valor` (tipo conceitual)
14. `designador`
15. `escopo de alinhamento`
16. `[V] Verboso`
17. `impossibilidade geométrica (multinível)`

---

## 8. Compatibilidade com ADR-0026

A ADR-0026 permanece autoridade ativa sobre:
- separação entre JSON estrutural da tela e documento externo de conteúdo;
- envelope conceitual `{tipo, formato, dados}`;
- princípio de que o JSON declara intenção e o renderizador calcula a representação física.

Nenhuma decisão da ADR-0026 foi reescrita, contraditada ou substituída nesta
aplicação. As seções propagadas (contrato_tela_json.md §33, contrato_json_console.md
§13) referem-se explicitamente à ADR-0026 como autoridade anterior e preservam
suas fronteiras.

---

## 9. Compatibilidade com ADR-0027

A ADR-0027 permanece autoridade ativa sobre:
- responsabilidade do ponto de entrada pelo carregamento separado e entrega conjunta;
- schema semântico multinível: envelope raiz, três apresentações, três tipos de nível, forma dos nós, designadores, 20 validações mínimas;
- uso de fixtures permanentes.

As 20 validações da ADR-0027 (§D13) não foram alteradas. As validações V-01 a
V-15 desta aplicação são declaradas explicitamente como **complemento** das 20
da ADR-0027, não como substituição.

A correspondência entre tipos conceituais (contêiner, folha, campo) e os nomes
do schema estabelecidos pela ADR-0027 (`container`, `conteudo`, `nome_valor`)
foi registrada na NOMENCLATURA.md §19.3 sem renomear nenhum campo.

---

## 10. Tratamento de `modo normal` e `modo não verboso`

O `contrato_console.md` (§6) usa o termo **`modo normal`** para o modo de
exibição sem quebra de linha, declarado como default da instância.

A ADR-0028 usa o termo **`modo não verboso`** para o mesmo comportamento
conceitual nas apresentações de conteúdo multinível.

Esta aplicação:

1. **não renomeou** nenhum dos termos;
2. **não declarou** nenhum deles como substituto do outro;
3. **registrou** a equivalência conceitual em:
   - `docs/NOMENCLATURA.md` §19.4;
   - `docs/contratos/contrato_console.md` §21.4.
4. **adiou** a reconciliação terminológica definitiva, conforme ADR-0028 §43.

O registro desta equivalência não constitui decisão sobre o valor padrão do
modo inicial.

---

## 11. Tratamento do modo inicial

O modo inicial é determinado pelo campo do bloco `excesso` no documento JSON
externo de conteúdo (estabelecido pelo schema da ADR-0027).

Esta aplicação:

1. **não escolheu** um valor padrão para o caso de campo ausente;
2. **registrou** que, quando o campo estiver ausente, o comportamento não está
   definido pela ADR-0028;
3. **propagou** esse registro em:
   - `docs/contratos/contrato_console.md` §21.7;
   - `docs/NOMENCLATURA.md` §19.2 (termo `modo inicial`).

A definição do valor padrão permanece adiada conforme ADR-0028 §43 item 3.

---

## 12. Decisões adiadas

As seguintes decisões não foram tomadas nesta aplicação e permanecem adiadas
conforme ADR-0028 §43:

| # | Item adiado |
|---|---|
| 1 | Nomes definitivos das propriedades do JSON de conteúdo multinível |
| 2 | Versão inicial do schema |
| 3 | Valores padrão (incluindo modo padrão quando o campo de excesso estiver ausente) |
| 4 | Marcador padrão de truncamento |
| 5 | Estilos de designador obrigatórios no schema |
| 6 | Limites máximos de profundidade |
| 7 | Política global de fallback visual para impossibilidade no conteúdo multinível |
| 8 | Estratégia concreta de navegação entre páginas |
| 9 | Formato de mensagens de validação |
| 10 | Protocolo de integração com o Pipeline |
| 11 | Comando, repositório e localização do script do Pipeline |
| 12 | Transporte do JSON produzido pelo Pipeline |
| 13 | Persistência intermediária |
| 14 | Timeout |
| 15 | Tratamento de falha ou indisponibilidade do Pipeline |
| — | Reconciliação terminológica definitiva entre `modo normal` e `modo não verboso` |

---

## 13. Resíduos encontrados

| Achado | Localização | Classificação | Ação |
|---|---|---|---|
| `proposta` em linha 99 da ADR-0028 | §3.3, referência ao contrato externo ("O contrato está em estado de proposta consolidada...") | Não é resíduo de status — descreve o estado do contrato externo; correto | Nenhuma ação necessária |
| Seção 14 do `contrato_barra_de_menus.md` trata de `[V]` modo verboso geral | `contrato_barra_de_menus.md` §14 | Não há conflito — §14 é regra geral; §22 (nova) especifica para conteúdo multinível do console | Nenhuma ação necessária; convivência explicitada em §22.5 |
| Seção 14 do `contrato_console.md` trata de relação com chip e barra | Não há seção 14 de modo verboso no `contrato_console.md` — seção 6 trata de modo normal/verboso | Não há conflito material | Nenhuma ação necessária; §21.4 registra a relação com §6 |

Nenhum resíduo material foi identificado que exija correção antes do QA.

---

## 14. Verificações

| # | Verificação | Resultado |
|---|---|---|
| 1 | `git diff --check` | Sem erros de whitespace |
| 2 | `git status` — apenas arquivos autorizados modificados | Confirmado: 8 arquivos modificados + 1 criado (este relatório) = 9 total |
| 3 | Nenhum arquivo de código, configuração, fixture ou teste alterado | Confirmado |
| 4 | Status da ADR-0028 atualizado para `aceita e aplicada` em frontmatter, §1 e §2 | Confirmado |
| 5 | Pointer para este relatório registrado na ADR-0028 §2 | Confirmado |
| 6 | Histórico §47 da ADR-0028 atualizado com entrada de aplicação | Confirmado |
| 7 | ADR-0028 adicionada ao INDICE_ADR.md | Confirmado |
| 8 | NOMENCLATURA.md — seção 19 criada | Confirmado |
| 9 | contrato_json_console.md — seção 13 criada | Confirmado |
| 10 | contrato_console.md — seção 21 criada | Confirmado |
| 11 | contrato_tela_json.md — seção 33 criada | Confirmado |
| 12 | contrato_composicao_corpo.md — seção 12 criada | Confirmado |
| 13 | contrato_barra_de_menus.md — seção 22 criada | Confirmado |
| 14 | Nenhum valor padrão para modo inicial escolhido | Confirmado — campo ausente = comportamento indefinido |
| 15 | Nenhuma renomeação de propriedade do schema | Confirmado |
| 16 | Nenhuma generalização para dashboard, lancador ou outros componentes | Confirmado — escopo exclusivo ao console com conteúdo multinível registrado em todas as seções |
| 17 | Compatibilidade com ADR-0026 preservada | Confirmado — nenhuma decisão da ADR-0026 reescrita |
| 18 | Compatibilidade com ADR-0027 preservada | Confirmado — 20 validações não alteradas; V-01–V-15 são complemento |
| 19 | Protocolo Pipeline não inventado | Confirmado — itens 10–15 de §43 permanecem adiados |

---

## 15. Bloqueios

Nenhum bloqueio do tipo `BLOCKED_USER_DECISION` foi acionado.

Nenhum bloqueio do tipo `BLOCKED_DOCUMENTATION` foi acionado.

Todas as alterações foram realizadas nos 9 arquivos da lista autorizada:
`ADR-0028`, `INDICE_ADR.md`, `NOMENCLATURA.md`, `contrato_json_console.md`,
`contrato_console.md`, `contrato_tela_json.md`, `contrato_composicao_corpo.md`,
`contrato_barra_de_menus.md` e este relatório.

Nenhuma alteração foi necessária fora dessa lista. A seção 14 do
`contrato_barra_de_menus.md` e a seção 6 do `contrato_console.md` existentes
não precisaram de modificação — apenas as novas seções (22 e 21,
respectivamente) foram adicionadas.

---

## 16. Prontidão documental para QA

Os documentos abaixo foram alterados e estão prontos para inspeção de QA:

| Arquivo | Seção adicionada/alterada |
|---|---|
| `docs/adr/ADR-0028-...md` | Status, §1, §2, §47 |
| `docs/adr/INDICE_ADR.md` | Nova linha ADR-0028 |
| `docs/NOMENCLATURA.md` | Seção 19 |
| `docs/contratos/contrato_json_console.md` | Seção 13 |
| `docs/contratos/contrato_console.md` | Seção 21 |
| `docs/contratos/contrato_tela_json.md` | Seção 33 |
| `docs/contratos/contrato_composicao_corpo.md` | Seção 12 |
| `docs/contratos/contrato_barra_de_menus.md` | Seção 22 |

Este relatório não declara a aplicação aprovada. O QA independente determinará
se a propagação está completa, coerente e livre de contradições com as
autoridades vigentes.

---

## 17. Decisões ainda necessárias antes de criar handoff

Antes que um handoff de implementação possa ser criado para a ADR-0028, é
necessário decidir, no mínimo:

1. **Valor padrão do modo inicial** quando o campo de excesso estiver ausente
   no documento de conteúdo (ADR-0028 §43 item 3) — esta decisão foi
   deliberadamente mantida adiada nesta aplicação.

2. **Nomes definitivos das propriedades** do JSON de conteúdo multinível (ADR-0028
   §43 item 1) — a correspondência entre os termos do contrato externo e os
   nomes do schema atual foi registrada, mas a reconciliação não foi decidida.

3. **Reconciliação terminológica** entre `modo normal` e `modo não verboso` —
   registrada como equivalência conceitual, mas sem escolha do nome canônico.

Os itens 4–15 do §43 da ADR-0028 (protocolo Pipeline, marcador de truncamento,
limites de profundidade etc.) também precisarão ser endereçados quando
pertinentes ao escopo do handoff.

---

## 18. Correção pós-QA (PATCH_APLICACAO_ADR)

Esta seção registra as correções aplicadas após o QA da aplicação
(`RELATORIO_QA_APLICACAO_ADR-0028.md`, status `ADR_APPLICATION_APPROVED_WITH_NOTES`
normalizado para `ADR_APPLICATION_REJECTED` pelo gerente, pois APLIC-QA-001 e
APLIC-QA-002 exigem correções documentais).

### 18.1 Achados corrigidos

| Código | Localização | Defeito | Ação |
|---|---|---|---|
| APLIC-QA-001 | Seção 14, verificação #2 deste relatório | Contagem declarava 7+1=8; correto é 8+1=9 (ADR-0028 é arquivo modificado pela etapa, embora não rastreado como `M` pelo git) | Contagem corrigida para "8 arquivos modificados + 1 criado = 9 total" |
| APLIC-QA-002 | `docs/contratos/contrato_json_console.md` §13.4 | Os dois cenários de `conjuntos_campos` (dois níveis e três níveis) estavam condensados em uma linha única com a formulação "em dois ou três níveis" | §13.4 expandido para separar nominalmente os dois cenários como estruturas distintas com demonstração própria |

### 18.2 Arquivos alterados nesta correção

- `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` (este arquivo): verificação #2
  da seção 14 corrigida; esta seção 18 adicionada.
- `docs/contratos/contrato_json_console.md`: §13.4 expandido com separação
  explícita dos dois cenários de `conjuntos_campos`.

Nenhum outro arquivo foi alterado.

### 18.3 Preservações

- As decisões D1–D22 não foram alteradas.
- Nenhum valor novo de schema foi introduzido.
- Nenhum conteúdo matricial foi introduzido.
- Os nomes concretos aprovados (`conjuntos_campos`, `tabela`, `hierarquia`,
  `container`, `conteudo`, `nome_valor`) permanecem inalterados.
- Nenhum limite global de profundidade foi introduzido.
- A observação APLIC-QA-003 não foi tratada como defeito corretivo e o
  `contrato_barra_de_menus.md` não foi alterado.

### 18.4 Verificações

- `git diff --check`: sem erros de whitespace.
- Busca por contagens conflitantes após correção: não encontrada.
- Busca por cenários de `conjuntos_campos` condensados após correção: não
  encontrada — os dois cenários aparecem separados em §13.4.
- Nenhum arquivo fora da lista autorizada foi alterado.

### 18.5 Bloqueios

Nenhum bloqueio do tipo `BLOCKED_USER_DECISION` foi acionado.

Nenhum bloqueio do tipo `BLOCKED_DOCUMENTATION` foi acionado.

Este relatório não declara a aplicação aprovada.
