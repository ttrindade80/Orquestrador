# Relatório de QA da aplicação da ADR-0026

## 1. Identificação

| Campo | Valor |
|---|---|
| **Identificador do Relatório** | RELATORIO_QA_APLICACAO_ADR-0026 |
| **Data de Execução** | 2026-07-17 |
| **ADR auditada** | ADR-0026 — Fornecimento externo de dados ao console por JSON multinível |
| **Etapa auditada** | APLICAR_ADR (aplicação documental da ADR-0026) |
| **Relatório de aplicação** | `docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md` |
| **QA de referência da ADR** | `docs/relatorios/RELATORIO_QA_ADR-0026.md` (status: `ADR_APPROVED`) |
| **Autor da auditoria** | Auditor Documental Independente |

---

## 2. Escopo da auditoria

Esta auditoria verifica a propagação fiel das 13 decisões da ADR-0026 aos
documentos normativos ativos, a preservação das decisões deferidas, a ausência
de resultados calculados no documento externo, a coerência com ADR-0025 e
H-0035, a integridade dos contratos declarados como preservados, a fidedignidade
do relatório de aplicação e a rastreabilidade do estado Git.

O escopo não inclui implementação de código, criação de handoff nem correção
de achados identificados.

---

## 3. Autoridades e evidências examinadas

| Documento | Papel |
|---|---|
| `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` | Autoridade normativa primária |
| `docs/relatorios/RELATORIO_QA_ADR-0026.md` | QA de referência da ADR |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md` | Objeto da auditoria |
| `docs/adr/INDICE_ADR.md` | Documento alterado — índice |
| `docs/NOMENCLATURA.md` | Documento alterado — terminologia |
| `docs/contratos/contrato_tela_json.md` | Documento alterado — contrato |
| `docs/contratos/contrato_console.md` | Documento alterado — contrato |
| `docs/contratos/contrato_json_console.md` | Documento alterado — contrato |
| `docs/contratos/contrato_composicao_corpo.md` | Declarado preservado — inspecionado |
| `docs/contratos/contrato_json_dashboard.md` | Declarado preservado — inspecionado |
| `docs/contratos/contrato_json_lancador.md` | Declarado preservado — inspecionado |
| `docs/contratos/contrato_lancador.md` | Declarado preservado — inspecionado |
| `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md` | Compatibilidade |

Todos os arquivos foram lidos integralmente. Os diffs de cada documento
alterado foram examinados linha a linha.

---

## 4. Estado Git e escopo real

### 4.1 Estado verificado

```bash
git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_ADR-0026.md
```

`git diff --stat`:
```
docs/NOMENCLATURA.md                    | 83 +
docs/adr/INDICE_ADR.md                  |  1 +
docs/contratos/contrato_console.md      | 77 +
docs/contratos/contrato_json_console.md | 95 +
docs/contratos/contrato_tela_json.md    | 66 +
5 files changed, 322 insertions(+)
```

`git diff --check`: sem problemas de whitespace.

### 4.2 Arquivos não rastreados

```text
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_ADR-0026.md
```

O conjunto era esperado conforme estado anterior declarado. Nenhum arquivo
inesperado encontrado. Este relatório (`RELATORIO_QA_APLICACAO_ADR-0026.md`)
será o quarto arquivo não rastreado após sua criação.

### 4.3 Contratos declarados preservados — confirmação Git

Os arquivos abaixo não constam no diff (`git diff --name-only` não os lista),
confirmando que não foram modificados:

```text
docs/contratos/contrato_composicao_corpo.md   — sem alteração ✓
docs/contratos/contrato_json_dashboard.md     — sem alteração ✓
docs/contratos/contrato_json_lancador.md      — sem alteração ✓
docs/contratos/contrato_lancador.md           — sem alteração ✓
```

---

## 5. Fidelidade do relatório de aplicação

### 5.1 Arquivos declarados alterados vs. Git

| Arquivo | Declarado | Git |
|---|---|---|
| `docs/NOMENCLATURA.md` | alterado | ` M` ✓ |
| `docs/adr/INDICE_ADR.md` | alterado | ` M` ✓ |
| `docs/contratos/contrato_console.md` | alterado | ` M` ✓ |
| `docs/contratos/contrato_json_console.md` | alterado | ` M` ✓ |
| `docs/contratos/contrato_tela_json.md` | alterado | ` M` ✓ |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md` | criado | `??` ✓ |

### 5.2 Linhas adicionadas — verificação

| Documento | Declarado | Git diff --stat |
|---|---|---|
| `docs/NOMENCLATURA.md` | 83 | 83 ✓ |
| `docs/adr/INDICE_ADR.md` | 1 | 1 ✓ |
| `docs/contratos/contrato_tela_json.md` | 66 | 66 ✓ |
| `docs/contratos/contrato_console.md` | 77 | 77 ✓ |
| `docs/contratos/contrato_json_console.md` | 95 | 95 ✓ |
| **Total** | **322** | **322 ✓** |

### 5.3 Contagem de `documentos_alterados: 5`

O relatório declara `documentos_alterados: 5`. O Git confirma exatamente
5 arquivos normativos modificados. O relatório de aplicação
(`RELATORIO_APLICACAO_ADR-0026.md`) foi criado como novo artefato — não
é uma modificação de documento pré-existente. O campo
`documentos_alterados: 5` é factualmente correto para documentos normativos
modificados; a criação do relatório é contabilizada separadamente. A diferença
entre "5 modificados" e "6 arquivos afetados" é de forma de contagem, não
inexatidão factual.

### 5.4 `proxima_categoria: aguarda_instrucao_do_usuario`

O relatório declara `proxima_categoria: aguarda_instrucao_do_usuario`. A
categoria processual correta após `APLICAR_ADR` — antes de auditoria
independente — é `QA_APLICACAO_ADR`. O valor declarado não corresponde à
sequência processual canônica. O impacto foi nulo, pois o ciclo `QA_APLICACAO_ADR`
foi executado pela instrução direta do usuário. Esta divergência é registrada
como observação (ver seção 16).

### 5.5 Commit

O relatório declara `commit: nao_realizado`. Git confirma: nenhum commit
novo desde `fb9e5be`. ✓

### 5.6 Autoaprovação

O relatório não atribui a si mesmo o status de QA independente. ✓

---

## 6. Propagação da decisão aprovada

Verificadas as 13 decisões da seção 6 da ADR-0026:

| # | Decisão | Propagada em | Verificado |
|---|---|---|---|
| D1 | Conteúdo de runtime tem origem externa | NOMENCLATURA §17.1; console §19.1; json_console §11.1 | ✓ |
| D2 | JSON estrutural não é repositório de runtime | tela_json §31.1; NOMENCLATURA §17.1 | ✓ |
| D3 | Console recebe dados por JSON externo | json_console §11.1; console §19.1 | ✓ |
| D4 | Documento externo segue envelope declarativo | json_console §11.2; NOMENCLATURA §17.1 | ✓ |
| D5 | Formato inicial: `tipo: "multinivel"` | json_console §11.3; NOMENCLATURA §17.1 | ✓ |
| D6 | Bloco `formato` descreve intenção de apresentação | json_console §11.2; NOMENCLATURA §17.1 | ✓ |
| D7 | Bloco `dados` contém estrutura semântica | json_console §11.2; NOMENCLATURA §17.1 | ✓ |
| D8 | Níveis declarados explicitamente | json_console §11.3; NOMENCLATURA §17.1 | ✓ |
| D9 | Dados chegam previamente estruturados | json_console §11.3; console §19.2 | ✓ |
| D10 | Consumidor não reconstrói nem infere hierarquia | console §19.3; json_console §11.3; NOMENCLATURA §17.4 | ✓ |
| D11 | Renderizador calcula geometria, quebras, paginação, posições | console §19.4; json_console §11.4; NOMENCLATURA §17.3 | ✓ |
| D12 | Script produzirá os dados no sistema final | console §19.5; INDICE_ADR (linha ADR-0026) | ✓ |
| D13 | Protocolo de invocação do script permanece para decisão futura | console §19.7; json_console §11.8 | ✓ |

Todas as 13 decisões foram propagadas integralmente.

---

## 7. Fronteiras entre estrutura, conteúdo e renderização

### 7.1 Princípio normativo central

O princípio `"O JSON externo declara a intenção de apresentação e o conteúdo
semântico. O renderizador calcula a representação física na área disponível."`
foi propagado literalmente em quatro pontos:

| Local | Seção | Verificado |
|---|---|---|
| `docs/NOMENCLATURA.md` | §17.2 | ✓ |
| `docs/contratos/contrato_tela_json.md` | §31.5 | ✓ |
| `docs/contratos/contrato_console.md` | §19.6 | ✓ |
| `docs/contratos/contrato_json_console.md` | §11.5 | ✓ |

### 7.2 Resultados calculados proibidos no documento externo

A NOMENCLATURA §17.2 enumera explicitamente os resultados proibidos:

- largura ou altura efetiva ✓
- linha ou coluna física calculada ✓
- posição ou coordenada física final ✓
- página calculada ✓
- quebra física pronta ✓
- truncamento já aplicado ✓
- geometria física final ✓
- distribuição concreta de espaço já calculada ✓

O `contrato_json_console.md` §11.4 lista os mesmos itens (exceto o último,
que é coberto pelo princípio geral). Nenhum resultado calculado foi atribuído
ao documento externo nos contratos alterados.

### 7.3 Fronteira do renderizador

O `contrato_console.md` §19.4 lista explicitamente as responsabilidades
exclusivas do renderizador: geometria, dimensões efetivas, quebras físicas,
truncamentos, alinhamentos calculados, paginação, posições finais e recuperação
após redimensionamento (SIGWINCH). ✓

### 7.4 Fronteira do consumidor

O `contrato_console.md` §19.3 proíbe ao consumidor: reconstruir hierarquia
a partir de dados de domínio não normalizados; descobrir ou inferir estrutura
semântica; assumir responsabilidades geométricas ou de cálculo físico. ✓

---

## 8. Conteúdo multinível e níveis declarados

- O `contrato_json_console.md` §11.3 formaliza que o foco inicial é
  `tipo: "multinivel"` e que os níveis são declarados explicitamente no
  bloco `dados`. ✓
- O consumidor não reconstrói, descobre nem infere a hierarquia. ✓
- A NOMENCLATURA §17.1 define `conteúdo multinível` como hierarquia de dados
  com níveis declarados explicitamente no documento externo. ✓
- A distinção `conteúdo multinível` × `distribuição matricial de nível único`
  (ADR-0025) está formalmente estabelecida na NOMENCLATURA §17.4. ✓

---

## 9. Decisões deferidas

Nenhuma das seguintes decisões foi antecipada ou inventada pela aplicação:

| Item deferido | Localização da não-decisão | Verificado |
|---|---|---|
| Nome e forma do vínculo tela → fonte | tela_json §31.3; json_console §11.6 | ✓ |
| Protocolo de invocação do script | console §19.5; json_console §11.8 | ✓ |
| Assinatura, argumentos, códigos de saída | console §19.7; json_console §11.8 | ✓ |
| Execução síncrona ou assíncrona | console §19.7 | ✓ |
| Caminho e ciclo de vida do documento externo | NOMENCLATURA §17.5 | ✓ |
| APIs, classes e módulos do consumidor/loader | console §19.3; json_console §11.8 | ✓ |
| Suporte a `tipo: "matriz"` na primeira implementação | json_console §11.8; NOMENCLATURA §17.5 | ✓ |
| Comportamento com fonte ausente ou inválida | console §19.7; json_console §11.8 | ✓ |
| Navegação, seleção, expansão, recolhimento | console §19.7 | ✓ |
| Paginação interativa de conteúdo multinível | console §19.7 | ✓ |
| Versionamento, cache, persistência, segurança | NOMENCLATURA §17.5 | ✓ |
| Número ou escopo de futuro handoff | Não mencionado ✓ | ✓ |

A indicação desses assuntos como pendências nos contratos é correta e não
constitui invenção de decisão.

O campo `origem_dados` existente no envelope do console não foi declarado como
mecanismo final de vínculo: `contrato_json_console.md` §11.6 explicitamente
registra que esse campo "não é declarado por esta ADR como mecanismo final de
vínculo" e que a forma do vínculo permanece para decisão futura. ✓

---

## 10. Relação com o formato matricial

- `tipo: "matriz"` não foi tornado escopo obrigatório da primeira
  implementação. ✓
- A NOMENCLATURA §17.5 lista "Suporte ao `tipo: 'matriz'` no mesmo
  mecanismo" como item não decidido. ✓
- Os contratos alterados não mencionam `tipo: "matriz"` como obrigatório. ✓
- Nenhuma formulação implica suporte mandatório ao tipo matricial. ✓

---

## 11. Compatibilidade com ADR-0025 e H-0035

- A ADR-0025 (distribuição matricial configurável de nível único) permanece
  vigente e não foi alterada. ✓
- O H-0035 permanece fechado, commit `fb9e5be` intocado. ✓
- A distinção `conteúdo multinível` × `distribuição matricial de nível único`
  é formalizada na NOMENCLATURA §17.4 sem contradição. ✓
- A seção 10 de `contrato_json_console.md` (ADR-0025) foi preservada
  integralmente; a nova seção 11 (ADR-0026) foi acrescentada após ela. ✓
- `contrato_composicao_corpo.md` seção 11 (fronteira com distribuição interna
  de participantes, ADR-0025) foi preservada sem alteração. ✓
- Nenhuma migração automática, alteração retroativa de telas ou redistribuição
  implícita foi declarada. ✓
- Não houve reabertura de H-0035 nem redefinição da distribuição matricial
  já implementada. ✓

---

## 12. Verificação por documento alterado

### 12.1 `docs/adr/INDICE_ADR.md`

A linha adicionada:

```
| ADR-0026 | Fornecimento externo de dados ao console por JSON multinível — ... | aceita e aplicada | 2026-07-17 |
```

- Posição: após a linha da ADR-0025. ✓
- Formato: idêntico ao padrão das linhas anteriores. ✓
- Título: resume fielmente as decisões da ADR-0026. ✓
- Data: 2026-07-17, concordante com o arquivo da ADR. ✓
- Status: `aceita e aplicada`.

**Divergência identificada**: o arquivo `ADR-0026-...md` contém
`status: aceita` no seu frontmatter, enquanto o índice declara
`aceita e aplicada`. Precedente (ADR-0025) mostra que o arquivo da ADR deve
ser atualizado para `aceita e aplicada` durante `APLICAR_ADR`. Esta
atualização não foi feita — o arquivo da ADR não foi modificado. Ver
achado QAAPADR-0026-002.

Entradas históricas não foram alteradas. ✓
O índice não afirma implementação de código. ✓

### 12.2 `docs/NOMENCLATURA.md`

Seção 17 adicionada após seção 16 (última linha do documento anterior). ✓

**Termos canonizados — contagem declarada e real:**

A aplicação declara 13 termos em §17.1. Contagem real da tabela §17.1:
`JSON estrutural da tela`, `JSON externo de conteúdo`, `conteúdo de runtime
do console`, `conteúdo multinível`, `envelope declarativo`, `bloco tipo`,
`bloco formato`, `bloco dados`, `níveis declarados`, `produtor de dados`
(futuro), `consumidor`, `representação semântica`, `representação física
calculada`. Total: 13. ✓

- Cada termo possui definição inequívoca. ✓
- `JSON estrutural da tela` e `JSON externo de conteúdo` são explicitamente
  distinguidos. ✓
- `conteúdo semântico` e `representação física calculada` são distinguidos. ✓
- Produtor, consumidor e renderizador possuem fronteiras claras na tabela
  §17.3. ✓
- Nenhum alias normativo concorrente foi criado. ✓
- Nenhuma redefinição indevida de termos anteriores (seções 1–16
  preservadas). ✓
- §17.5 registra corretamente os itens não decididos como "não são termos
  ativos". ✓

### 12.3 `docs/contratos/contrato_tela_json.md`

Seção 31 adicionada após o final da seção 30.

- Frontmatter `adrs_aplicadas` atualizado com ADR-0026. ✓
- §31.1: JSON estrutural não é repositório de runtime. ✓
- §31.2: origem externa do conteúdo com envelope conceitual mínimo. ✓
- §31.3: vínculo entre tela e fonte — explicitamente não decidido; `origem_dados`
  não declarado como mecanismo final. ✓
- §31.4: responsabilidades preservadas do `tela.json`. ✓
- §31.5: princípio normativo literal. ✓
- §31.6: remissões cruzadas corretas (json_console §11, console §19,
  NOMENCLATURA §17). ✓
- Nenhum campo de ligação inventado. ✓
- Nenhum caminho de runtime escolhido. ✓
- Nenhum exemplo fecha decisão deferida. ✓

**Achado QAAPADR-0026-001** (ver seção 15): a linha
`A especificação normativa completa está na ADR-0025.` (linha 1313 do arquivo
— última linha) aparece imediatamente após o último bullet de §31.6, sem
linha em branco separadora, referenciando ADR-0025 em seção relativa à
ADR-0026. Ver achado completo na seção 15.

### 12.4 `docs/contratos/contrato_console.md`

Seção 19 adicionada após seção 18.

- Frontmatter `adrs_aplicadas` atualizado com ADR-0026. ✓
- §19.1: conteúdo de runtime tem origem externa. ✓
- §19.2: conteúdo chega previamente estruturado com níveis declarados. ✓
- §19.3: fronteira do consumidor — proibições corretas. ✓
- §19.4: fronteira do renderizador — responsabilidades exclusivas listadas
  integralmente. ✓
- §19.5: integração com o script produtor com protocolo não decidido. ✓
- §19.6: princípio normativo literal. ✓
- §19.7: decisões deferidas — lista explícita e completa. ✓
- §19.8: remissões cruzadas corretas. ✓
- Nenhum protocolo de comunicação com script inventado. ✓
- Nenhum comportamento diante de erro ou ausência de fonte inventado. ✓

### 12.5 `docs/contratos/contrato_json_console.md`

Seção 11 adicionada após seção 10.5.

- Frontmatter `adrs_aplicadas` atualizado com ADR-0026. ✓
- §11.1: distinção JSON estrutural × documento externo. ✓
- §11.2: envelope declarativo mínimo com tabela de responsabilidades por
  bloco (`tipo`, `formato`, `dados`). ✓
- §11.3: foco inicial `tipo: "multinivel"` e níveis declarados. ✓
- §11.4: lista de resultados calculados proibidos no documento externo. ✓
- §11.5: princípio normativo literal. ✓
- §11.6: campo `origem_dados` não declarado como vínculo final. ✓
- §11.7: compatibilidade — ausência do documento externo não invalida envelope
  estrutural; JSONs existentes preservados. ✓
- §11.8: decisões deferidas — lista explícita. ✓
- §11.9: remissões cruzadas corretas. ✓
- `tipo: "matriz"` não foi transformado em escopo obrigatório. ✓
- Schema, versão, transporte e vínculo não foram inventados. ✓
- Seção anterior 10 (ADR-0025) preservada integralmente. ✓

---

## 13. Verificação dos documentos preservados

### 13.1 `docs/contratos/contrato_composicao_corpo.md`

Lido integralmente (1856 linhas). Não há formulação que:

- obrigue conteúdo de runtime dentro do JSON estrutural do console: a seção 2
  ("o estado de runtime não pertence ao JSON da tela") é CONSISTENTE com
  ADR-0026. ✓
- atribua ao renderizador inferência de hierarquia semântica do conteúdo do
  console. ✓
- contradiga a origem externa aprovada. ✓
- redefina o tipo multinível. ✓
- torne o `lancador` ou o `dashboard` consumidores do novo mecanismo. ✓

A linha 476 ("conteúdo e campos vêm da instância declarada no `tela.json`")
refere-se ao `dashboard` e à sua configuração estrutural declarativa — sem
conflito com ADR-0026 que trata do conteúdo de runtime do console. ✓

A seção 11 (fronteira com distribuição interna de participantes, ADR-0025)
preservada sem alteração. ✓

Preservação correta. ✓

### 13.2 `docs/contratos/contrato_json_dashboard.md`

Específico ao `dashboard`. Nenhuma referência à origem de dados de runtime do
console. A seção 9 (ADR-0025) permanece intacta. Nenhuma contradição com
ADR-0026. Preservação correta. ✓

### 13.3 `docs/contratos/contrato_json_lancador.md`

Específico ao `lancador`. Nenhum vocabulário de origem de conteúdo que conflite
com ADR-0026. A seção 9 (ADR-0025) permanece intacta. Preservação correta. ✓

### 13.4 `docs/contratos/contrato_lancador.md`

Define comportamento do `lancador`. Nenhuma referência a script produtor,
documento externo de conteúdo de console nem fronteiras de consumidor que
precisassem ser reconciliadas. Preservação correta. ✓

---

## 14. Busca de resíduos e contradições

Buscadas formulações relacionadas aos termos da seção de busca de resíduos
nos documentos normativos alterados e preservados:

| Termo pesquisado | Ocorrências | Classificação |
|---|---|---|
| `dados codificados no JSON da tela` | Seção 2 de contrato_composicao_corpo: "o estado de runtime não pertence ao JSON da tela" | Ativa e coerente (proibição) |
| `conteúdo embutido` / `conteúdo hardcoded` | NOMENCLATURA §17.1 ("Não confundir com") | Ativa e coerente (distinção) |
| `hierarquia inferida` / `inferir hierarquia` | NOMENCLATURA §17.1, §17.4; json_console §11.3; console §19.3 | Ativas e coerentes (proibições) |
| `reconstruir hierarquia` | NOMENCLATURA §17.1 (coluna "Não confundir com"); console §19.3 | Ativas e coerentes (proibições) |
| `origem dos dados` / `fonte de dados` | console §19.1 ("tem origem externa") | Ativa e coerente |
| `conteúdo multinível` | Múltiplas ocorrências nos contratos alterados e NOMENCLATURA §17.1 | Ativas e coerentes |
| `geometria no JSON` / `posição calculada` / `página calculada` | NOMENCLATURA §17.2; json_console §11.4 (como proibição) | Ativas e coerentes |
| `script produtor` | console §19.5 (como futuro, protocolo não decidido) | Ativa e coerente |

Nenhum resíduo conflitante encontrado. As ocorrências são formulações
normativas corretas (proibições e distinções), não resíduos de formulações
anteriores.

---

## 15. Achados

### QAAPADR-0026-001

```yaml
id: QAAPADR-0026-001
severidade: baixa
arquivo: docs/contratos/contrato_tela_json.md
secao_ou_trecho: linha 1313 (última linha do arquivo) — cauda de §31.6
decisao_ou_regra_afetada: Clareza de remissão; referência à ADR correta em
  seção específica de ADR-0026
evidencia: |
  A linha "A especificação normativa completa está na ADR-0025." (linha 1313)
  aparece imediatamente após o último bullet de §31.6 — sem linha em branco
  separadora. Essa linha era o encerramento do bloco de remissões da seção
  anterior (ADR-0025), posicionada originalmente como última linha do arquivo
  antes da inserção de §31. A edição inseriu §31 entre as duas linhas de
  encerramento da seção 30 da ADR-0025, deixando esta última como linha
  final do arquivo após o conteúdo de §31. Resultado: a linha agora aparece
  como continuação de §31.6 (ADR-0026) e referencia ADR-0025.
impacto: |
  Um leitor seguindo §31 vê "A especificação normativa completa está na
  ADR-0025" ao final da seção sobre ADR-0026. A referência ao número errado
  de ADR pode confundir ou induzir o leitor a buscar a especificação
  normativa na ADR errada.
correcao_necessaria: |
  Reposicionar ou remover a linha órfã. Uma das opções:
  (a) Remover a linha da posição atual e garantir que a linha equivalente
      para ADR-0026 seja adicionada ao final de §31.6 com blank line
      separador: "A especificação normativa completa está na ADR-0026.";
  (b) Remover a linha completamente, já que §31.6 já provê as remissões
      necessárias.
  Em qualquer caso, deve haver linha em branco entre o último bullet de
  §31.6 e qualquer texto que o siga.
```

### QAAPADR-0026-002

```yaml
id: QAAPADR-0026-002
severidade: baixa
arquivo: docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: frontmatter — campo `status`
decisao_ou_regra_afetada: Consistência de rastreabilidade de status entre o
  arquivo da ADR e o INDICE_ADR.md
evidencia: |
  O arquivo da ADR-0026 contém `status: aceita` no frontmatter. O
  INDICE_ADR.md registra a ADR-0026 com status `aceita e aplicada`. A ADR-0025
  (precedente imediato) tem `status: aceita e aplicada` em seu próprio arquivo,
  confirmando que a atualização do status do arquivo da ADR é parte da etapa
  APLICAR_ADR. A aplicação não modificou o arquivo da ADR-0026 (declarado
  em §8.5 do relatório como "preservado sem alteração"), deixando a
  inconsistência entre arquivo e índice.
impacto: |
  Inconsistência de rastreabilidade: o arquivo da ADR e o índice declaram
  estados diferentes para o mesmo artefato. Ferramentas ou auditores que
  lerem apenas o arquivo da ADR não saberão que ela foi aplicada.
correcao_necessaria: |
  Atualizar o frontmatter do arquivo ADR-0026: alterar `status: aceita` para
  `status: aceita e aplicada`, seguindo o precedente da ADR-0025.
```

---

## 16. Observações

### OBS-001: `proxima_categoria: aguarda_instrucao_do_usuario`

O relatório de aplicação declara `proxima_categoria: aguarda_instrucao_do_usuario`.
A categoria processual canônica após `APLICAR_ADR` — antes de auditoria
independente — é `QA_APLICACAO_ADR`. O ciclo correto foi executado por
instrução direta do usuário, portanto o impacto prático foi nulo. Recomenda-se
que futuros relatórios de aplicação usem a categoria processual correta.

### OBS-002: Contagem de `documentos_alterados` vs. artefatos criados

O relatório declara `documentos_alterados: 5`. O Git confirma 5 documentos
normativos modificados e 1 relatório de aplicação criado (total de 6 artefatos
afetados). O valor `5` é factualmente correto para documentos normativos
modificados; a criação do relatório é um artefato complementar, não uma
modificação de documento pré-existente. A diferença é apenas de forma de
contagem. Não há inexatidão factual.

### OBS-003: `contrato_composicao_corpo.md` — ausência de entrada em `adrs_aplicadas`

A ADR-0026 lista `contrato_composicao_corpo.md` em sua rastreabilidade como
`contratos_afetados`. A aplicação avaliou este contrato e concluiu corretamente
que nenhuma alteração normativa era necessária. O frontmatter do arquivo não
foi atualizado para incluir ADR-0026 em `adrs_aplicadas`. Isso é consistente
com a convenção observada no projeto (o campo `adrs_aplicadas` é atualizado
quando uma seção normativa é efetivamente adicionada). Registra-se como
observação para rastreabilidade.

---

## 17. Classificação final

```yaml
status_literal: ADR_APPLICATION_REJECTED
status_normalizado: Aplicação requer patch em dois pontos — defeitos baixos
  corrigíveis sem nova decisão arquitetural; propagação normativa completa e
  correta
relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 2
observacoes: 3
documentos_alterados_confirmados: 5
documentos_inspecionados_sem_alteracao_confirmados: 4
arquivos_inesperados: 0
residuos_conflitantes: 0
decisoes_deferidas_inventadas: 0
git:
  branch: master
  commit_head: fb9e5be
  workspace: sujo (5 arquivos modificados, 3 não rastreados)
  stage: vazio
  commit_novo: nao_realizado
proxima_categoria: PATCH_APLICACAO_ADR
```
