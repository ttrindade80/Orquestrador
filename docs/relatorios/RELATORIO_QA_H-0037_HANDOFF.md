---
name: RELATORIO_QA_H-0037_HANDOFF
description: Auditoria documental independente do handoff H-0037 — verificação de fidelidade normativa, completude, determinismo, implementabilidade, testabilidade, coerência com autoridades e com o estado real do repositório
metadata:
  type: relatorio_qa_handoff
  handoff_auditado: H-0037
  data: "2026-07-17"
  auditor: independente (contexto limpo)
  status_literal: H1_HANDOFF_APPROVED
---

# Relatório de QA do Handoff — H-0037

---

## 1. Identificação

| Campo | Valor |
|---|---|
| Relatório | `docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md` |
| Handoff auditado | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| Status recebido do handoff | `AGUARDANDO_QA` |
| Data da auditoria | 2026-07-17 |
| Etapa | `QA_HANDOFF` |
| Ciclo precedente | H-0036 / ADR-0028 aplicada / status pós-patch `ADR_APPLICATION_APPROVED_WITH_NOTES` |

---

## 2. Objetivo

Auditar o H-0037 como auditor documental independente para determinar se é:
fiel às autoridades normativas; completo; determinístico; implementável; testável;
demonstrável; limitado a uma capacidade coesa; compatível com o H-0036; livre de
decisões arquiteturais inventadas; e suficiente para permitir implementação sem lista
paralela de arquivos.

---

## 3. Autoridades lidas

| Documento | Status de leitura |
|---|---|
| `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` | Lido integralmente |
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | Lido integralmente |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md` | Lido integralmente |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` | Lido (seções relevantes) |
| `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md` | Lido integralmente |
| `docs/contratos/contrato_json_console.md` | Lido integralmente |
| `docs/contratos/contrato_console.md` | Lido integralmente (até §21) |
| `docs/contratos/contrato_barra_de_menus.md` | Lido integralmente |
| `docs/contratos/contrato_tela_json.md` | Lido (seções relevantes) |
| `docs/contratos/contrato_composicao_corpo.md` | Confirmado como ativo |
| `docs/NOMENCLATURA.md` | Confirmado como existente e modificado |
| `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` | Confirmado como existente |
| `docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md` | Consultado para baseline |
| `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0036.md` | Confirmado como existente |
| `demo/demo.py` | Inspecionado (catálogo, processar_comando, _tela_inicial_de_argv) |
| `config/telas/demo/` | Inspecionado (fixtures H-0036 confirmadas; H-0037 ausentes — esperado) |

---

## 4. Estado Git

### 4.1 Inspecção executada

```bash
git status --short
# Branch: master / HEAD: f6982d0
```

### 4.2 Resultado

```yaml
branch: master
head: f6982d0
git_diff_check: LIMPO
stage: VAZIO
arquivos_modificados_rastreados:
  - docs/NOMENCLATURA.md          # acumulado da aplicação ADR-0028
  - docs/adr/INDICE_ADR.md        # acumulado da aplicação ADR-0028
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
arquivos_nao_rastreados:
  - docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
  - docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
  - demo/__pycache__/   # diretório de cache Python — não é arquivo de conteúdo
  - tela/__pycache__/   # diretório de cache Python — não é arquivo de conteúdo
arquivos_inesperados_de_conteudo: NENHUM
```

### 4.3 Análise

Os 7 arquivos modificados (contratos, nomenclatura, índice) são produto do ciclo
acumulado da ADR-0028. Os arquivos não rastreados são os esperados para este ciclo.
O H-0037 é não rastreado — confirmado como novo arquivo criado na etapa `CRIAR_HANDOFF`.
Os `__pycache__` são diretórios de cache Python de execuções anteriores de testes e
não constituem alteração de conteúdo de ciclo.

**Escopo da etapa `CRIAR_HANDOFF` verificado:** apenas o arquivo
`docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` foi
adicionado nessa etapa. Nenhum outro arquivo de conteúdo apresenta origem inesperada.

---

## 5. Escopo auditado

O H-0037 declara 32 seções. Esta auditoria cobre todas as verificações críticas
mandatórias (1–23) mais verificação de coerência e exequibilidade.

---

## 6. Verificação crítica 1 — Suficiência real do schema

### 6.1 Valores concretos autorizados para `excesso.modo`

O `contrato_json_console.md` §12.7 apresenta exemplo normativo com:

```json
"excesso": {
  "modo": "verboso"
}
```

O único valor estabelecido pelos contratos ativos para `excesso.modo` é `"verboso"`.
Não existe valor `"nao_verboso"` definido em nenhuma autoridade (ADR-0028 §25;
`contrato_console.md` §21.7; `contrato_json_console.md` §12.7).

### 6.2 Representação declarativa do modo não verboso

O modo não verboso **não possui representação no schema JSON**. É o estado oposto
do verboso, atingido em runtime pela ativação da tecla `V`. Esta é a posição
correta conforme ADR-0028 §43 item 3 (decisão adiada) e §25.

### 6.3 Declaração de modo inicial não verboso

Uma fixture **não pode** declarar modo inicial não verboso por valor JSON —
`"nao_verboso"` não existe como valor autorizado. A única forma de ter comportamento
não verboso como estado inicial seria um valor padrão definido quando `excesso.modo`
está ausente, mas isso é decisão adiada (ADR-0028 §43 item 3).

### 6.4 Declaração de modo inicial verboso

Uma fixture declara modo inicial verboso com `"excesso": {"modo": "verboso"}`.
Todas as quatro fixtures H-0037 usarão este campo.

### 6.5 Alternância da tecla V

A tecla `V` alterna entre dois estados — verboso e não verboso — mas somente
`"verboso"` possui representação declarativa. O modo não verboso é alcançável
apenas pela ativação de `V` a partir do modo verboso.

**Implicação:** todos os quatro cenários H-0037 abrem em modo verboso. Não há
fixture que abra diretamente em modo não verboso. Isso é uma limitação
consequente da decisão adiada (ADR-0028 §43 item 3), não um defeito do handoff.

### 6.6 Reprodutibilidade do estado inicial sem default implícito

O estado inicial **é reproduzível**: todas as fixtures declaram
`excesso.modo: "verboso"` explicitamente. A ausência de `excesso.modo` tem
comportamento indefinido — o handoff (§8.2, §14.1, §30.3) proíbe a ausência
do campo em qualquer fixture H-0037. Esta restrição é correta.

### 6.7 Comportamento na ausência de `excesso.modo`

O comportamento é indefinido conforme `contrato_console.md` §21.7 e ADR-0028 §43
item 3. O handoff preserva essa indefinição e proíbe fixtures sem o campo.

### 6.8 Decisão adiada preenchida pelo handoff?

**NÃO.** O handoff §10 lista a "definição do valor para modo não verboso" e
o "comportamento padrão quando `excesso.modo` está ausente" como decisões adiadas,
com autoridade correta (ADR-0028 §43 item 3). §30.3 proíbe a implementação de
definir esses valores.

### 6.9 Semântica de runtime não presente nas autoridades?

**NÃO.** A semântica de runtime (flip de estado pela tecla V) está formalizada
em ADR-0028 D11, §23, §24; `contrato_console.md` §21.5, §21.6; e
`contrato_barra_de_menus.md` §22.2.

**Classificação:** CONFORME. A afirmação do autor é correta e demonstrável
nas autoridades. A restrição de que todas as fixtures declararem `excesso.modo`
é uma consequência necessária da decisão adiada, não uma invenção do handoff.

---

## 7. Verificação crítica 2 — Modo inicial

O handoff (§5 item 3; §14; §20.3; §21.3; §25.2):

- **Não** escolhe default para ausência do campo ✓ (§10, §30.3)
- **Não** trata ausência como modo não verboso ✓ (§10, decisão adiada)
- **Não** exige que todas as fixtures comecem verbosas por obrigação normativa —
  exige para garantir comportamento determinístico dado que a ausência é indefinida
  (§8.2) ✓
- **Especifica** método reproduzível:
  - Modo inicial: verboso (via `excesso.modo: "verboso"`) ✓
  - Após V: não verboso ✓
  - Após segundo V: verboso (restaurado) ✓

**Sequência demonstrável por cenário:** §21.3 e §24 detalham todos os passos.

**Classificação:** CONFORME. O modo inicial é determinístico. A impossibilidade de
ter fixture que inicie em não verboso é limitação do schema atual (decisão adiada),
não defeito do handoff.

---

## 8. Verificação crítica 3 — Escopo exclusivo do console

O handoff §5, §7, §26 e §30 restringem o escopo a:

> conteúdo multinível externo exibido em componentes do tipo `console`

Verificado:

- Dashboard: explicitamente excluído (§26, §30.2, §17.3) ✓
- Lançador: explicitamente excluído (§17.3, §30.2) ✓
- Conteúdo matricial: explicitamente excluído (§26, §30.3) ✓
- Distribuição matricial: explicitamente excluída (§17.3, §30.3) ✓
- Integração concreta com Pipeline: explicitamente excluída (§26, §30.3) ✓
- Referências históricas ao H-0036 (§4, §30.1): são preservação, não inclusão no escopo ✓

**Classificação:** CONFORME.

---

## 9. Verificação crítica 4 — Quatro cenários

### 9.1 IDs declarados

| ID | Declarado em | Confirmado |
|---|---|---|
| `h0037_console_tabela` | §13.1 | SIM |
| `h0037_console_hierarquia` | §13.2 | SIM |
| `h0037_console_conjuntos2` | §13.3 | SIM |
| `h0037_console_conjuntos3` | §13.4 | SIM |

### 9.2 Campos por cenário

Para cada um dos quatro cenários, o handoff declara nominalmente:

| Campo | Tabela | Hierarquia | Conjuntos2 | Conjuntos3 |
|---|---|---|---|---|
| ID da tela | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Arquivo estrutural | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Arquivo externo de conteúdo | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Associação no catálogo | §20.1 ✓ | §20.1 ✓ | §20.1 ✓ | §20.1 ✓ |
| Apresentação | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Estrutura de níveis | §13.1 (mínimos) ✓ | §13.2 (mínimos) ✓ | §13.3 (2 níveis) ✓ | §13.4 (3 níveis) ✓ |
| Identidade semântica | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Modo inicial | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Texto diferenciando truncamento/continuação | §19.3 (global) △ | §19.3 (global) △ | §19.3 (global) △ | §19.3 (global) △ |
| Comando exato de abertura | §13.1 ✓ | §13.2 ✓ | §13.3 ✓ | §13.4 ✓ |
| Teste automatizado | §22.5 (global) ✓ | §22.5 (global) ✓ | §22.5 (global) ✓ | §22.5 (global) ✓ |
| Roteiro de validação manual | §24 (global) ✓ | §24 Passo 5 ✓ | §24 Passo 6 ✓ | §24 Passo 7 ✓ |

△ O requisito de dados suficientes para observar truncamento/continuação está em §19.3
de forma global, não por cenário. Esta é uma omissão de granularidade nas seções
individuais de cenário, mas o requisito normativo existe. **Impacto baixo:** o
executor pode derivar o critério de §19.3.

### 9.3 Nomes sem colisão

Os oito arquivos (4 estruturais + 4 externos) têm nomes distintos e sem colisão com
fixtures existentes H-0036 (`h0036_*`). ✓

**Classificação:** CONFORME com observação de granularidade em §19.3 (ver Achado QA-LOW-01).

---

## 10. Verificação crítica 5 — Separação JSON estrutural e conteúdo

O handoff confirma:

```yaml
carregamento: separado (§20.1, §6)
entrega_ao_fluxo: conjunta (§6, §20.1)
documentos: distintos (§12, §19.1, §19.2)
conteudo_no_JSON_estrutural: proibido (§19.1, §30.3)
```

- Dados não inseridos na tela estrutural: §19.1 proíbe explicitamente ✓
- Documentos não fundidos: §6 regras invioláveis ✓
- Produtor Pipeline não codificado na tela: §26, §30.3 ✓
- Renderizador não abre arquivos: §11 (fronteiras) ✓

**Classificação:** CONFORME.

---

## 11. Verificação crítica 6 — Tecla V

### 11.1 Definição

O handoff §16 define `V` como alternadora entre verboso e não verboso, derivando de:
ADR-0028 D11; `contrato_console.md` §21.5; `contrato_barra_de_menus.md` §22.2.

Chip declarado: `[V] Verboso` — texto `"Verboso"`, tecla `"V"` (§17.2).

### 11.2 Comportamento especificado

| Comportamento | Autoridade | Handoff |
|---|---|---|
| Alterna entre verboso/não verboso | ADR-0028 D11 | §16.1 ✓ |
| Mesmos dados, mesma tela, mesmo externo | ADR-0028 §23 | §16.1 ✓ |
| Não troca apresentação | ADR-0028 D11 | §16.1 ✓ |
| Não persiste | `contrato_console.md` §21.6 | §16.1, §25.2 ✓ |
| Não reescreve arquivos | `contrato_console.md` §21.6 | §16.1 ✓ |
| Reversível (segunda ativação) | ADR-0028 D11 | §16.1 ✓ |
| Não vaza entre consoles | `contrato_console.md` §21.6 | §16.2 ✓ |
| Não persiste preferência global | `contrato_barra_de_menus.md` §22.3 | §16.2 ✓ |
| Recalcula após redimensionamento | `contrato_console.md` §21.8 | §16.4 ✓ |

### 11.3 Conflito com teclas existentes

Verificado em `demo/demo.py`: teclas existentes são `"b"` (borda), `"s"` e `"\x1b"`
(saída). A tecla `V` não está em uso. **Sem conflito.** ✓

### 11.4 Consoles sem conteúdo multinível

§16.3 especifica que a tecla V não tem efeito em consoles sem conteúdo multinível
externo. §24 Passo 8 requer validação manual de que cenários H-0036 (sem
`excesso.modo`) não são afetados. ✓

**Código de saída zero não é prova suficiente:** §22 §22.2 nota esta exigência
explicitamente, derivando de ADR-0028 §37. ✓

**Classificação:** CONFORME.

---

## 12. Verificação crítica 7 — Barra de menus

O handoff §17:

- Identifica que o chip é declarado no `tela.json` (§17.1; `contrato_barra_de_menus.md` §22.1) ✓
- Referencia `contrato_barra_de_menus.md` como autoridade ✓
- Chip existência condicional (somente telas H-0037): §17.3, §26 ✓
- Não exige alteração dinâmica do rótulo — chip é declarado estaticamente no JSON ✓
- APLIC-QA-003 preservada: §17.4 reconhece a coexistência das seções 14 e 22 como
  observação não corretiva; o handoff proíbe explicitamente adicionar referências
  cruzadas ou alterar contratos para resolver ✓

**Arquivo técnico responsável pelo chip:** a `barra_de_menus` é declarada no JSON
estrutural da tela. O arquivo `tela/renderizador.py` é o executor, mas o chip
existe por declaração no JSON — não por inferência do renderer.

**Testes existentes da barra:** `demo/teste_explorar_barra_de_menus.py` e
`demo/teste_demo_console.py` são arquivos existentes. O handoff não explicita
que esses testes devem confirmar a presença do chip `[V] Verboso`, mas §22
e §25.3 exigem que `teste_demo_console_verboso.py` cubra esta prova. ✓

**Classificação:** CONFORME.

---

## 13. Verificação crítica 8 — Estrutura e tipos de níveis

### 13.1 Nomes concretos usados

O handoff usa os nomes concretos vigentes do schema (estabelecidos pela ADR-0027
e propagados para `contrato_json_console.md` §12.3 e §13.3):

| Conceito normativo | Nome no schema | Usado no handoff |
|---|---|---|
| contêiner | `container` | §13.3, §13.4 ✓ |
| folha | `conteudo` | §13.1 ("conteúdo folha") ✓ |
| campo nome-valor | `nome_valor` | §13.3, §13.4 ✓ |

### 13.2 Correspondência e regra suficiente

`contrato_json_console.md` §13.3 documenta a correspondência entre conceito
normativo e nome do schema. O handoff usa os nomes do schema (não os do contrato
externo), o que é correto para implementação.

A correspondência entre `folha` / `campo` / `conteudo` / `nome_valor` está
documentada em `contrato_json_console.md` §13.3 e ADR-0028 §34. **Há regra
suficiente; sem bloqueio documental.**

### 13.3 Cobertura implementável

O handoff cobre raiz única, níveis, relações pai-filho, contêiner, folha, campo
nome-valor, origem declarada, ordem e dados compatíveis. Os designadores são
cobertos por referência ao schema (§12.3 do contrato, §8.1 do handoff). ✓

**Classificação:** CONFORME.

---

## 14. Verificação crítica 9 — Apresentação tabular

O handoff §13.1 e §19.1 requerem fixtures de tabela com:

- `formato.tabela.cabecalho` declarado (V-01 proíbe tabela sem cabeçalho) ✓
- Ao menos um nível `"conteudo"` por coluna ✓
- `excesso.modo: "verboso"` ✓

A ADR-0028 §17 define as regras completas de tabela. O `contrato_json_console.md`
§13.4 propaga essas regras. O handoff §15 lista V-01 (tabela sem cabeçalho) e
V-14 (coluna sem origem) como validações obrigatórias. ✓

Os critérios de verificação específicos (cabeçalho repetido, paginação, altura
pela maior célula, uma linha no modo não verboso, múltiplas no verboso) derivam
da ADR-0028 §17 e são verificáveis pelo executor a partir das autoridades. ✓

**Classificação:** CONFORME (critérios detalhados nas autoridades, não necessário
replicar integralmente no handoff).

---

## 15. Verificação crítica 10 — Hierarquia indentada

O handoff §13.2 e §19 requerem ao menos dois níveis: `container` raiz e `conteudo`
folha. A ADR-0028 §18 e `contrato_json_console.md` §13.4 definem as regras de
hierarquia (recuo por nível, ausência de tab implícito, alinhamento de continuação,
truncamento no não verboso, repetição de ancestrais).

O handoff não reintroduz regras de tab implícito (ausência documentada na ADR-0028
§18.2) e remete às autoridades para os detalhes. ✓

**Classificação:** CONFORME.

---

## 16. Verificação crítica 11 — Conjuntos e campos

### 16.1 Dois cenários distintos

O handoff §13.3 (conjuntos2) e §13.4 (conjuntos3) são tratados como cenários
estruturalmente distintos, conforme ADR-0028 D17 e `contrato_json_console.md` §13.4:

- Cenário 3: dois níveis (`container` + `nome_valor`) ✓
- Cenário 4: três níveis (`container` + `container` + `nome_valor`) ✓
- Mesma apresentação `conjuntos_campos` — mas estruturas distintas ✓
- Cada um: fixture própria, tela própria, identidade própria, teste próprio, comando próprio ✓

### 16.2 Separação formal

§13.5 afirma explicitamente: "o uso da mesma apresentação não os torna equivalentes".
Cada cenário exige "fixture própria, associação própria, tela própria e testes
independentes". ✓

**Classificação:** CONFORME.

---

## 17. Verificação crítica 12 — Validações

### 17.1 Lista V-01 a V-15

O handoff §15.1 lista todas as 15 validações (V-01 a V-15) com condição e status
INVÁLIDO, derivadas de `contrato_json_console.md` §13.9. ✓

### 17.2 Cobertura de testes de rejeição

O handoff §22.3 especifica cobertura mínima de testes:

- "um caso válido por validação aplicável ao cenário" (todos os V-01–V-15)
- Caso de rejeição explícito: V-01 (tabela sem cabeçalho) ✓
- Caso de rejeição explícito: V-03 (múltiplas raízes) ✓
- Caso de rejeição explícito: V-13 (dados incompatíveis) ✓

**Lacuna identificada (ver Achado QA-LOW-02):** Para V-02, V-04–V-12, V-14, V-15,
o handoff exige apenas "um caso válido" — não exige explicitamente um caso de
rejeição. Esses casos de rejeição pertencem naturalmente a `tela/teste_loader.py`,
que já cobre validações da ADR-0027, mas o handoff não declara isso explicitamente.

### 17.3 Independência dos esperados

§22.4: valores esperados derivados dos contratos ativos, não da saída do loader. ✓

### 17.4 Contêiner obrigatório não reintroduzido

V-05 é "Contêiner sem nível filho declarado — INVÁLIDO" (sem o qualificador
"obrigatório" removido pelo QA-002 da ADR). ✓

**Classificação:** CONFORME com Achado QA-LOW-02.

---

## 18. Verificação crítica 13 — Paginação e impossibilidade

O handoff referencia ADR-0028 §17.12 (paginação de tabela), §18.8 (hierarquia),
§20.5 (conjuntos) e §32 (impossibilidade) via as 15 validações V-15 (condição
excepcional sem política). §§ das autoridades estão propagadas nos contratos.

**Paginação não resolve impossibilidade horizontal:** declarado em ADR-0028 §30.4
e `contrato_json_console.md` §13.7. O handoff §6 (fluxo) confirma que o renderizador
calcula geometria; §11 confirma que impossibilidade é do renderizador. ✓

**Política de impossibilidade:** O handoff não inventa nova política — remete às
ADRs vigentes (ADR-0017, ADR-0023) conforme ADR-0028 §32. ✓

**Classificação:** CONFORME.

---

## 19. Verificação crítica 14 — Arquivos da futura implementação

### 19.1 Criar (§18.1)

```text
config/telas/demo/h0037_console_tabela.json       ← nominal ✓
config/telas/demo/h0037_tabela_conteudo.json       ← nominal ✓
config/telas/demo/h0037_console_hierarquia.json    ← nominal ✓
config/telas/demo/h0037_hierarquia_conteudo.json   ← nominal ✓
config/telas/demo/h0037_console_conjuntos2.json    ← nominal ✓
config/telas/demo/h0037_conjuntos2_conteudo.json   ← nominal ✓
config/telas/demo/h0037_console_conjuntos3.json    ← nominal ✓
config/telas/demo/h0037_conjuntos3_conteudo.json   ← nominal ✓
demo/teste_demo_console_verboso.py                 ← nominal ✓
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md ← nominal ✓
```

### 19.2 Alterar (§18.2)

```text
demo/demo.py                   ← catálogo + tecla V ✓
config/telas/demo/demo.json    ← entradas H-0037 no launcher ✓
```

### 19.3 Autorização condicional (§18.3)

```text
demo/teste_demo.py             ← autorizado condicionalmente ✓
demo/teste_demo_console.py     ← autorizado condicionalmente ✓
tela/teste_loader.py           ← autorizado condicionalmente ✓
tela/teste_renderizador.py     ← autorizado condicionalmente ✓
```

### 19.4 Arquivos da suíte canônica não listados em §18

| Arquivo | Na suíte §23.1 | Em §18 | Avaliação |
|---|---|---|---|
| `tela/loader.py` | implícito (suíte) | não listado explicitamente | É o arquivo que implementa as 15 validações; alteração provável; **ver Achado QA-LOW-03** |
| `tela/modelo.py` | implícito | não listado | Pode não precisar de alteração se `excesso.modo` já é transportado |
| `tela/renderizador.py` | implícito | não listado | Implementará lógica de modo verboso/não verboso; alteração provável; **ver Achado QA-LOW-03** |
| `tela/teste_modelo.py` | na suíte | não em §18.3 | Provavelmente não precisa alteração se modelo já transporta `excesso` |
| `demo/teste_diagnostico.py` | na suíte §23.1 | não em §18 | Não será alterado — correto não estar ✓ |
| `demo/teste_explorar_barra_de_menus.py` | na suíte §23.1 | não em §18 | Não será alterado — correto não estar ✓ |
| `demo/teste_demo_distribuicao.py` | na suíte §23.1 | não em §18 | Não será alterado — correto não estar ✓ |
| `tela/teste_distribuicao_matricial.py` | na suíte §23.1 | não em §18 | Não será alterado — correto não estar ✓ |

**Achado QA-LOW-03:** Os arquivos `tela/loader.py` e `tela/renderizador.py` precisam
ser alterados para implementar as 15 validações V-01–V-15 e a lógica de renderização
dos dois modos, respectivamente. O handoff §18.3 autoriza seus testes condicionalmente,
mas não lista os arquivos de implementação (`loader.py`, `renderizador.py`) explicitamente.
A exceção operacional (§27) cobre alterações necessárias não listadas. Nenhum
arquivo necessário está simultaneamente proibido. **Impacto baixo** — o executor
usará §27 para registrar essas alterações, o que é o mecanismo correto.

### 19.5 Arquivos para relatórios futuros

| Arquivo | Status no handoff |
|---|---|
| `docs/relatorios/IMP-0037-...md` | Autorizado (§29) ✓ |
| `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md` | Não mencionado — **Achado QA-LOW-04** |
| `docs/relatorios/RELATORIO_QA_H-0037_IMPLEMENTACAO.md` | Não mencionado — **Achado QA-LOW-04** |

**Classificação:** CONFORME com achados LOW-03 e LOW-04.

---

## 20. Verificação crítica 15 — Arquivos preservados

O handoff §30.1 lista nominalmente:

- ADRs (0028, 0026, 0027) ✓
- Contratos (5 contratos) ✓
- Relatórios históricos (5 relatórios da ADR-0028) ✓
- Fixtures H-0036 (6 fixtures) ✓
- Fixtures H-0035 (4 fixtures) ✓
- Arquivos de distribuição matricial ✓
- Contratos de dashboard, lancador, json_dashboard ✓
- NOMENCLATURA.md, INDICE_ADR.md ✓
- H-0036 handoff e IMP-0036 ✓

§30.2 preserva comportamentos (placeholder, cenários H-0036, distribuição matricial).

**As proibições não tornam a implementação inexequível:** §27 (exceção operacional)
cobre casos não previstos. ✓

**Classificação:** CONFORME.

---

## 21. Verificação crítica 16 — Exceção operacional

§27 define regra focal com todos os elementos obrigatórios:

- Parar antes da alteração ✓
- Informar arquivo ✓
- Informar motivo ✓
- Informar escopo ✓
- Informar mudança esperada ✓
- Pedir autorização explícita ✓
- Não criar nova semântica ou arquitetura ✓

§27 também lista itens que a exceção NÃO autoriza (schema, validações, apresentações,
etc.), delimitando corretamente o escopo. ✓

**Classificação:** CONFORME.

---

## 22. Verificação crítica 17 — Baseline e suíte canônica

### 22.1 Correspondência ao estado H-0036

O `IMP-0036-...md` §27/§28 confirma: `total_verificacoes: 2423`;
`baseline_final: 9 scripts, 0 falhas`. O handoff §23.1 declara
`9 scripts / 2423 verificações / 0 falhas`. **CORRESPONDE.** ✓

### 22.2 Identificada como histórica

§23.1 nomeia a baseline como "Baseline verificado (H-0036)". §23.5 exige que o
executor registre "baseline encontrado antes das alterações (deve ser 9/2423/0)",
implicando medição antes da implementação. ✓

### 22.3 Scripts canônicos existentes

Todos os 9 scripts listados em §23.1 foram confirmados como existentes no repositório:

```yaml
tela/teste_loader.py:                EXISTE ✓
tela/teste_modelo.py:                EXISTE ✓
tela/teste_renderizador.py:          EXISTE ✓
tela/teste_distribuicao_matricial.py: EXISTE ✓
demo/teste_demo.py:                  EXISTE ✓
demo/teste_diagnostico.py:           EXISTE ✓
demo/teste_demo_distribuicao.py:     EXISTE ✓
demo/teste_explorar_barra_de_menus.py: EXISTE ✓
demo/teste_demo_console.py:          EXISTE ✓
```

### 22.4 Novo script — décimo da suíte

`demo/teste_demo_console_verboso.py` não existe (esperado — futuro). Será o
décimo script. ✓

### 22.5 Comando canônico

`PYTHONDONTWRITEBYTECODE=1 python <script>` — executado diretamente, não via pytest.
Confirmado por `RELATORIO_ORIGEM_ERROS_PYTEST_LEGADO.md` (existência confirmada). ✓

### 22.6 Contagem final não prometida antes da implementação

§23.2: "A contagem de verificações deve aumentar" — sem prometer quantidade exata. ✓

**Classificação:** CONFORME.

---

## 23. Verificação crítica 18 — Novo teste

`demo/teste_demo_console_verboso.py`:

| Critério | Status |
|---|---|
| Necessidade | CONFIRMADA — integração da tecla V não coberta por nenhum teste existente ✓ |
| Responsabilidade | Testes semânticos de integração (9 provas por cenário) ✓ |
| Sem duplicação inadequada | `teste_demo_console.py` não cobre V; `teste_loader.py` cobre validações V-01–V-15 em nível de loader — papéis distintos ✓ |
| Inclusão nominal em §18.1 | ✓ |
| Inclusão na suíte (§23.2) | ✓ |
| Cobertura dos 4 cenários | §22.5 ✓ |
| Prova de primeira ativação de V | §22.2 prova 5 ✓ |
| Prova de segunda ativação de V | §22.2 prova 6 ✓ |
| Prova de identidade | §22.2 provas 1–3 ✓ |
| Prova de isolamento | §22.2 prova 8 ✓ |
| Prova de redimensionamento | §22.2 prova 9 ✓ |

**Classificação:** CONFORME.

---

## 24. Verificação crítica 19 — Ponto de entrada e comandos

### 24.1 Ponto de entrada real

`demo/demo.py` — confirmado existente. Função `_tela_inicial_de_argv` aceita
ID de tela como argumento posicional. Confirmado por inspeção (linhas 548–562). ✓

### 24.2 Forma de selecionar tela

```bash
python demo/demo.py <id_tela>
```

Mecanismo real: `_tela_inicial_de_argv(sys.argv)` → retorna o primeiro argumento
não iniciado por `-`. Confirmado. ✓

### 24.3 Forma de associar conteúdo

`_CATALOGO_CONTEUDO_EXTERNO` em `demo/demo.py` (linhas 135–141), populado com
entradas H-0036 e H-0035. Confirmado funcionando via `id_conteudo_externo_de()`.
As quatro entradas H-0037 devem ser adicionadas conforme §20.1. ✓

### 24.4 Comandos exatos

```bash
python demo/demo.py h0037_console_tabela       # §13.1 ✓
python demo/demo.py h0037_console_hierarquia   # §13.2 ✓
python demo/demo.py h0037_console_conjuntos2   # §13.3 ✓
python demo/demo.py h0037_console_conjuntos3   # §13.4 ✓
```

Cada comando abre inequivocamente o cenário pretendido (após implementação das
fixtures e das entradas no catálogo). ✓

### 24.5 Suficiência dos testes

§22.2 requer 9 provas por cenário, verificando tela, conteúdo, apresentação,
modo inicial, alternância V, retorno, preservação, isolamento e resize. Código
zero não é prova suficiente (§22.2). ✓

**Classificação:** CONFORME.

---

## 25. Verificação crítica 20 — Validação manual

§24 fornece roteiro de validação humana em TTY real com 9 passos:

| Passo | Conteúdo | Status |
|---|---|---|
| 1 | Identidade e modo verboso inicial de `h0037_console_tabela` | ✓ |
| 2 | Alternar para não verboso com V | ✓ |
| 3 | Retornar ao verboso com segundo V | ✓ |
| 4 | Verificar não persistência ao trocar de cenário | ✓ |
| 5 | Repetir para hierarquia | ✓ |
| 6 | Repetir para conjuntos dois níveis | ✓ |
| 7 | Repetir para conjuntos três níveis | ✓ |
| 8 | Confirmar H-0036 não afetado | ✓ |
| 9 | Redimensionamento | ✓ |

**Método reproduzível:** comandos exatos declarados por passo. ✓
**Resultado informado pelo usuário:** §24.4. ✓
**Redimensionamento:** Passo 9. ✓
**Quadro mínimo / fallback:** referenciado via ADR-0017/0023 pelas autoridades. ✓

**Uso correto de status literais:**
- `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO` — apropriado para uso futuro na IMP
- `MANUAL_VALIDATION_FAILED` — só usável após reprodução de comportamento incorreto
- O handoff não usa esses status diretamente; são para o relatório de implementação

**Classificação:** CONFORME.

---

## 26. Verificação crítica 21 — Relatórios futuros

### 26.1 IMP-0037

§29 autoriza explicitamente a criação de
`docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md`. ✓

### 26.2 Validação manual pelo usuário

§24.4: "O resultado da validação manual é informado pelo usuário no relatório de
implementação." O executor não pode declarar aprovação da própria implementação
(§29, último parágrafo). ✓

### 26.3 Relatório de validação manual separado

O H-0036 produziu `RELATORIO_VALIDACAO_MANUAL_H-0036.md` como arquivo separado.
O H-0037 não menciona `RELATORIO_VALIDACAO_MANUAL_H-0037.md` — o resultado vai
para o IMP-0037. Esta é uma diferença de convenção, não uma falha normativa, mas
pode criar inconsistência com o precedente. **Achado QA-LOW-04.**

### 26.4 Relatório de QA da implementação

O handoff não menciona `RELATORIO_QA_H-0037_IMPLEMENTACAO.md`. Por precedente
(H-0036), este relatório seria criado pelo auditor (não pelo executor). O handoff
deveria tornar isso explícito. **Achado QA-LOW-04.**

**Classificação:** CONFORME com achado LOW-04.

---

## 27. Verificação crítica 22 — Escopo negativo

§26 lista explicitamente os itens fora do escopo. Verificados:

| Item | Excluído |
|---|---|
| Conteúdo matricial | §26 ✓ |
| Integração concreta com Pipeline | §26, §30.3 ✓ |
| Persistência global | §16.2, §26 ✓ |
| Edição de JSON | §26, §30.3 ✓ |
| Navegação interativa | §26 ✓ |
| Expansão e recolhimento | §26 ✓ |
| Novo default | §26, §30.3 ✓ |
| Nova versão de schema | §10 ✓ |
| Novo marcador padrão | §10 ✓ |
| Nova profundidade máxima | §10 ✓ |
| Nova política global de fallback | §10 ✓ |
| Commit | §26, §30.3 ✓ |
| Push | §26 ✓ |

**Classificação:** CONFORME.

---

## 28. Verificação crítica 23 — Relatório de implementação

§29 exige conteúdo factual em 24 itens. Auditados:

- Autoridades, estado Git inicial, arquivos, schema concreto ✓
- Implementação por camada, quatro cenários, alternância ✓
- Testes focais, suíte canônica, smoke tests ✓
- Identidade semântica, pseudo-TTY, pendência manual ✓
- Exceções, bloqueios, limitações, diff ✓
- Autoaprovação proibida: "O relatório não pode declarar aprovação da própria
  implementação." ✓

**Classificação:** CONFORME.

---

## 29. Verificação de coerência e exequibilidade

| # | Verificação | Resultado |
|---|---|---|
| 1 | Autor do handoff alterou somente o handoff | CONFIRMADO — git status mostra apenas H-0037 como novo arquivo de handoff |
| 2 | Arquivo existe | CONFIRMADO — `docs/handoff/H-0037-...md` presente |
| 3 | Usa autoridade suficiente | CONFIRMADO — ADR-0028, contratos, relatórios QA listados em §3 |
| 4 | Schema determinístico | CONFIRMADO — `excesso.modo: "verboso"` obrigatório; 35 validações definidas |
| 5 | Nenhuma decisão adiada preenchida | CONFIRMADO — §10 lista todas as decisões adiadas; §30.3 proíbe implementação |
| 6 | Todos os arquivos necessários autorizados | CONFIRMADO com ressalva de achados LOW-03 e LOW-04 (exceção operacional cobre) |
| 7 | Nenhum arquivo necessário está proibido | CONFIRMADO |
| 8 | Quatro demonstrações com nomes | CONFIRMADO — §13.1–13.4 e §12 |
| 9 | Existem comandos exatos | CONFIRMADO — §13.1–13.4 e §21.1 |
| 10 | Identidade semântica definida | CONFIRMADO — strings H-0037 específicas por cenário |
| 11 | V pode ser testado | CONFIRMADO — §22.2 provas 5 e 6 |
| 12 | Suíte pode ser executada | CONFIRMADO — 10 scripts, comandos canônicos |
| 13 | Validação manual reproduzível | CONFIRMADO — §24 com 9 passos |
| 14 | Relatório IMP pode ser criado | CONFIRMADO — §29 autoriza |
| 15 | Exceção operacional presente | CONFIRMADO — §27 |
| 16 | Sem implementação antecipada | CONFIRMADO |
| 17 | Sem autorização de commit | CONFIRMADO — §26, §30.3 |

---

## 30. Achados

### QA-LOW-01 — Critério de truncamento/continuação ausente por cenário

| Campo | Valor |
|---|---|
| ID | QA-LOW-01 |
| Arquivo/seção | H-0037, §13.1–13.4 (seções individuais de cenário) |
| Evidência | Seções 13.1–13.4 não incluem critério explícito de truncamento/continuação |
| Autoridade | ADR-0028 §36 ("permite observar os mesmos dados nos modos verboso e não verboso"); analogia com requisito de dados suficientes |
| Severidade | baixo |
| Impacto | O executor pode derivar o critério de §19.3 ("ao menos uma linha truncada em não verboso; ao menos uma linha expandida em verboso"). Não há bloqueio de implementação |
| Correção exigida | Não obrigatória para aprovação; recomenda-se incluir referência a §19.3 em cada seção de cenário em futura revisão |
| Exige decisão do usuário | não |

---

### QA-LOW-02 — Cobertura de rejeição V-02 a V-15 não especificada no teste verboso

| Campo | Valor |
|---|---|
| ID | QA-LOW-02 |
| Arquivo/seção | H-0037, §22.3 |
| Evidência | §22.3 exige "um caso válido por validação aplicável" para V-01–V-15, mas exige caso de rejeição explícito somente para V-01, V-03 e V-13. Para V-02, V-04–V-12, V-14, V-15 a cobertura de rejeição não é explicitamente exigida em `teste_demo_console_verboso.py` |
| Autoridade | ADR-0028 D21 ("loader deve rejeitar configurações inválidas conforme §33"); V-01–V-15 definidos no contrato |
| Severidade | baixo |
| Impacto | Os casos de rejeição para V-02, V-04–V-12, V-14, V-15 provavelmente estarão em `tela/teste_loader.py`, mas o handoff não declara isso. O executor pode interpretar "caso válido" como apenas testando que VÁLIDOS são aceitos, sem testar que INVÁLIDOS são rejeitados |
| Correção exigida | O executor deve garantir que todos os 15 casos de rejeição estejam cobertos, seja em `teste_demo_console_verboso.py` ou em `tela/teste_loader.py` (autorizado em §18.3). O relatório de implementação deverá documentar onde cada caso de rejeição foi testado |
| Exige decisão do usuário | não |

---

### QA-LOW-03 — `tela/loader.py` e `tela/renderizador.py` não listados em §18

| Campo | Valor |
|---|---|
| ID | QA-LOW-03 |
| Arquivo/seção | H-0037, §18 |
| Evidência | Os arquivos de implementação `tela/loader.py` (15 validações V-01–V-15) e `tela/renderizador.py` (renderização dos dois modos) precisarão ser alterados para implementar o H-0037, mas não aparecem em §18.1 (criar) nem em §18.2 (alterar) nem em §18.3 (condicionais). Apenas seus testes (`tela/teste_loader.py` e `tela/teste_renderizador.py`) estão em §18.3 |
| Autoridade | §27 (exceção operacional) cobre arquivos necessários não listados |
| Severidade | baixo |
| Impacto | O executor precisará usar §27 para registrar e solicitar autorização para `loader.py` e `renderizador.py`. Isso é um passo extra de burocracia, mas não bloqueia a implementação |
| Correção exigida | O executor deve usar §27 ao alterar `tela/loader.py` e `tela/renderizador.py`. O relatório de implementação deve registrar estas alterações via exceção operacional |
| Exige decisão do usuário | não (§27 já autoriza o processo) |

---

### QA-LOW-04 — Relatórios futuros de validação manual e QA da implementação não endereçados

| Campo | Valor |
|---|---|
| ID | QA-LOW-04 |
| Arquivo/seção | H-0037, §29 e §24 |
| Evidência | O handoff menciona apenas `IMP-0037-...md`. Não menciona `RELATORIO_VALIDACAO_MANUAL_H-0037.md` nem `RELATORIO_QA_H-0037_IMPLEMENTACAO.md`. Por precedente do H-0036, ambos existem como arquivos separados. O §24.4 coloca o resultado da validação no IMP-0037, diferindo da prática anterior |
| Autoridade | Precedente H-0036: `RELATORIO_VALIDACAO_MANUAL_H-0036.md` e `RELATORIO_QA_H-0036_IMPLEMENTACAO.md` são arquivos distintos |
| Severidade | baixo |
| Impacto | Ambiguidade sobre se o auditor de QA da implementação deve criar `RELATORIO_QA_H-0037_IMPLEMENTACAO.md` e se a validação manual deve ser registrada em arquivo separado. Não bloqueia a implementação |
| Correção exigida | Nenhuma correção de handoff obrigatória para aprovação. O auditor de implementação deverá criar `RELATORIO_QA_H-0037_IMPLEMENTACAO.md` conforme precedente, e a validação manual poderá gerar `RELATORIO_VALIDACAO_MANUAL_H-0037.md` separado |
| Exige decisão do usuário | não (convenção da prática estabelecida resolve) |

---

### QA-OBS-01 — Impossibilidade de cenário com modo inicial não verboso

| Campo | Valor |
|---|---|
| ID | QA-OBS-01 |
| Arquivo/seção | H-0037, §8.2, §14.2, §14.3 |
| Natureza | Observação não corretiva |
| Descrição | Todas as fixtures H-0037 iniciam em modo verboso. Não existe forma de ter fixture com modo inicial não verboso enquanto ADR-0028 §43 item 3 (valor padrão do modo inicial) permanecer adiado. O modo não verboso somente é observável após pressionar V |
| Autoridade | ADR-0028 §43 item 3 (decisão adiada) |
| Impacto | Limitação conhecida e corretamente declarada. A demonstração dos dois modos é realizada pela alternância V, não por dois fixtures distintos |
| Ação | Nenhuma — corretamente preservado como decisão adiada |

---

### QA-OBS-02 — Comportamento de V em H-0036 (sem `excesso.modo`) não formalmente especificado

| Campo | Valor |
|---|---|
| ID | QA-OBS-02 |
| Arquivo/seção | H-0037, §16.3, §24 Passo 8 |
| Natureza | Observação não corretiva |
| Descrição | O handoff diz que V "não produz efeito inesperado" em cenários H-0036 (sem `excesso.modo`). O comportamento quando `excesso.modo` está ausente é formalmente indefinido (ADR-0028 §43 item 3), mas a implementação segura seria ignorar V nesses cenários. §24 Passo 8 exige validação manual disso |
| Autoridade | `contrato_console.md` §21.7; ADR-0028 §43 item 3 |
| Impacto | A validação manual do Passo 8 captura este comportamento. A implementação deverá decidir como tratar V quando `excesso.modo` está ausente — provavelmente ignorando silenciosamente, conforme §16.3 |
| Ação | Nenhuma — §16.3 e §24 Passo 8 tratam adequadamente |

---

### QA-OBS-03 — APLIC-QA-003 preservada

| Campo | Valor |
|---|---|
| ID | QA-OBS-03 |
| Arquivo/seção | H-0037, §17.4, §26 |
| Natureza | Observação preservada |
| Descrição | A coexistência das seções 14 e 22 do `contrato_barra_de_menus.md` sem referência cruzada recíproca (APLIC-QA-003) é preservada no H-0037. §17.4 reconhece isso explicitamente. §26 proíbe o executor de adicionar referências cruzadas ou alterar contratos |
| Impacto | Nenhum sobre a implementabilidade do H-0037 |
| Ação | Nenhuma — comportamento correto |

---

## 31. Resumo de achados

| Categoria | Quantidade |
|---|---|
| Bloqueantes | 0 |
| Altos | 0 |
| Médios | 0 |
| Baixos | 4 (QA-LOW-01, QA-LOW-02, QA-LOW-03, QA-LOW-04) |
| Observações não corretivas | 3 (QA-OBS-01, QA-OBS-02, QA-OBS-03) |

---

## 32. Conclusão

O handoff H-0037 é:

- **Fiel às autoridades:** todas as 22 decisões D-ADR28-D1 a D22 estão mapeadas;
  as 15 validações V-01–V-15 estão presentes; os contratos ativos são as fontes
  normativas para cada comportamento especificado.

- **Completo:** 32 seções cobrindo identificação, estado, autoridades, contexto,
  objetivo, fluxo, base de caminhos, suficiência do schema, decisões fechadas,
  decisões adiadas, fronteiras, fixtures, quatro cenários, modo inicial,
  validações, tecla V, barra de menus, arquivos autorizados, requisitos de
  fixtures, catálogo, demonstração, testes, suíte canônica, validação manual,
  critérios de aceite, escopo negativo, exceção operacional, bloqueios,
  relatório de implementação, preservados/proibidos e coerência.

- **Determinístico:** `excesso.modo: "verboso"` é o único valor estabelecido;
  todas as fixtures o declaram; a sequência V→não-verboso→V→verboso é definida.

- **Implementável:** ponto de entrada real confirmado (`demo/demo.py`);
  catálogo existente (`_CATALOGO_CONTEUDO_EXTERNO`); mecanismo de argumento
  confirmado (`_tela_inicial_de_argv`); nenhuma tecla existente em conflito.

- **Testável:** 9 provas semânticas por cenário; script novo autorizado;
  suíte canônica de 10 scripts; validações V-01–V-15 mapeadas.

- **Demonstrável:** 4 comandos exatos; identidades semânticas; modo inicial
  definido; alternância especificada.

- **Limitado a capacidade coesa:** console com conteúdo multinível externo e
  alternância verbosa. Sem contaminação de dashboard, lançador, matricial ou Pipeline.

- **Compatível com H-0036:** fixtures H-0036 preservadas; catálogo H-0036 mantido;
  Passo 8 do roteiro manual confirma não-interferência.

- **Livre de decisões arquiteturais inventadas:** todas as semânticas remetem
  a autoridades; as 11 decisões adiadas da ADR-0028 §43 são preservadas.

Os 4 achados LOW não bloqueiam a implementação. A exceção operacional (§27) cobre
os arquivos não listados explicitamente em §18. Os precedentes do ciclo H-0036
resolvem as ambiguidades dos relatórios futuros.

---

## 33. Status literal

```text
H1_HANDOFF_APPROVED
```

---

## 34. Status normalizado

```yaml
status_literal: H1_HANDOFF_APPROVED
handoff_auditado: H-0037
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 4
observacoes: 3
schema_concreto_suficiente: SIM
representacao_modo_verboso: "verboso" em formato.excesso.modo (contrato_json_console.md §12.7)
representacao_modo_nao_verboso: ESTADO_DE_RUNTIME_SEM_VALOR_JSON (ADR-0028 §43 item 3 — decisão adiada)
modo_inicial_deterministico: SIM — todas as fixtures declaram excesso.modo verboso
decisao_adiada_preenchida: NAO — §10 e §30.3 preservam todas as decisões adiadas da ADR-0028 §43
escopo_exclusivo_console: SIM
conteudo_matricial_incluido: NAO
cenarios:
  tabela: CONFORME — h0037_console_tabela / h0037_tabela_conteudo
  hierarquia: CONFORME — h0037_console_hierarquia / h0037_hierarquia_conteudo
  conjuntos_dois_niveis: CONFORME — h0037_console_conjuntos2 / h0037_conjuntos2_conteudo
  conjuntos_tres_niveis: CONFORME — h0037_console_conjuntos3 / h0037_conjuntos3_conteudo
alternancia_por_V: DEFINIDA — §16, §20.2, §22.2 provas 5 e 6
conflito_de_tecla: NAO — V não está em uso no demo.py atual
arquivos_futura_implementacao: NOMINAIS E SUFICIENTES (com ressalva QA-LOW-03 para loader.py e renderizador.py via §27)
fixtures_nominais: 8 arquivos nomeados em §12 e §18.1
telas_nominais: h0037_console_tabela, h0037_console_hierarquia, h0037_console_conjuntos2, h0037_console_conjuntos3
ponto_de_entrada: demo/demo.py (confirmado por inspeção — _tela_inicial_de_argv)
comandos_de_demonstracao: 4 comandos exatos em §13.1–13.4 e §21.1
baseline:
  scripts: 9
  verificacoes: 2423
  falhas: 0
  confirmado_em: IMP-0036 §27/§28
suite_canonica:
  antes: 9 scripts (todos confirmados como existentes)
  apos_h0037: 10 scripts (teste_demo_console_verboso.py ainda não existe — esperado)
validacao_manual:
  roteiro: SIM — §24, 9 passos
  tty_real: SIM — §24.1, §24.3
  resultado_pelo_usuario: SIM — §24.4
verificacao_de_coerencia: 17/17 CONFIRMADOS
git:
  branch: master
  head: f6982d0
  diff_check: LIMPO
  stage: VAZIO
  arquivo_handoff_criado_somente_na_etapa_criar_handoff: CONFIRMADO
proxima_categoria: IMPLEMENTAR
```

---

## 35. Próxima categoria

```yaml
proxima_categoria: IMPLEMENTAR
```

(Fim do Relatório)
