# Relatório de Aplicação Documental — ADR-0028 Revisão D23 (Política de Modo por Tela)

**Data:** 2026-07-18
**ADR:** ADR-0028 — Apresentações de conteúdo multinível no console e alternância verbosa
**Revisão aplicada:** D23 — Política de modo de apresentação da tela
**Tipo:** APLICAR_ADR — segunda aplicação documental (primeira: D1–D22, 2026-07-17)
**Aprovação prévia:** ADR_APPROVED_WITH_NOTES (RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md)

---

## 1. Objetivo

Propagar documentalmente a decisão D23 da ADR-0028 (revisão de política de modo
por tela) para todos os contratos afetados, definindo os campos canônicos concretos
e tornando os contratos coerentes com a revisão aprovada.

Esta aplicação complementa e corrige a aplicação anterior (D1–D22), que propagou
as decisões D1 a D22 sem incluir D23 (decisão acrescentada posteriormente).

---

## 2. Escopo normativo aplicado

### 2.1 Decisão D23 — três políticas de modo

Cada tela de `console` multinível nova ou revisada deve declarar uma das três
políticas:

- **`somente_verboso`** — sempre em modo verboso; sem `V`; chip não obrigatório.
- **`somente_nao_verboso`** — sempre em modo não verboso; sem `V`; chip não obrigatório; truncamento `...` válido.
- **`alternavel`** — suporta ambos os modos; chip `[V] Verboso` obrigatório; tecla `V` alterna; `modo_inicial` obrigatório.

### 2.2 Revisões de D11 e D12 decorrentes de D23

- **D11** (tecla V): restrita a telas alternáveis. Não se aplica a telas de modo único.
- **D12** (modo inicial): telas de modo único iniciam no único modo disponível; telas alternáveis devem declarar o modo inicial.

### 2.3 Campos canônicos definidos por esta aplicação

Esta aplicação resolve o adiamento do §43 item 3 da ADR-0028 (schema concreto
estava adiado; conceito já decidido em D23/§25). Os campos canônicos são:

| Campo | Localização | Tipo | Restrição |
|---|---|---|---|
| `formato.excesso.politica_modo` | JSON estrutural — elemento `console` | string | `"somente_verboso"`, `"somente_nao_verboso"`, `"alternavel"` |
| `formato.excesso.modo_inicial` | JSON estrutural — elemento `console` | string | `"verboso"`, `"nao_verboso"` — somente quando `politica_modo: "alternavel"` |

### 2.4 Cenários futuros mínimos (§36.2)

Quatro cenários documentados:
1. Tela somente não verbosa — truncamento; sem chip; sem V.
2. Tela somente verbosa — dois níveis em várias linhas; sem chip; sem V.
3. Tela alternável de três níveis — iniciando em não verboso; chip obrigatório; alternância por V.
4. Tabela alternável — iniciando em verboso; chip obrigatório; alternância disponível.

### 2.5 Regra de alinhamento de dois níveis em modo verboso (§36.3)

Coluna do segundo nível calculada a partir do identificador mais largo do primeiro
nível no conteúdo lógico completo. Coluna estável entre páginas. Linhas de
continuação alinhadas à mesma coluna. Escopo: `conteúdo completo` (§27) restrito
ao cenário.

### 2.6 Compatibilidade com telas legadas

Telas pré-D23 (ex.: H-0036) permanecem válidas sem declaração de `politica_modo`.
Não são reinterpretadas. Migração adiada.

---

## 3. Arquivo: `docs/contratos/contrato_json_console.md`

### 3.1 Modificações aplicadas

**§13.11 — Cenários de demonstração obrigatórios (D8)**

- **Problema**: última frase afirmava "Os mesmos dados devem ser observáveis nos
  modos verboso e não verboso na mesma tela" — incompatível com telas de modo
  único (D23).
- **Correção**: substituída pela distinção: para telas alternáveis, observação em
  ambos os modos; telas de modo único não precisam permitir alternância.

**§13.12 — Remissões**

- Atualizada referência a `contrato_tela_json.md` §33: de "JSON estrutural e modo
  de visualização" para "JSON estrutural e política de modo".

**§13.13 — Política de modo de apresentação da tela (D23) — NOVA SEÇÃO**

Adicionada seção com:
- §13.13.1: localização e tipos dos campos (`formato.excesso` no JSON estrutural);
- §13.13.2: valores admitidos (`politica_modo` e `modo_inicial`);
- §13.13.3: matriz de validade (9 combinações, válidas e inválidas);
- §13.13.4: exemplos válidos das quatro combinações funcionais;
- §13.13.5: exemplos inválidos (alternável sem `modo_inicial`; fixa com `modo_inicial`; tela nova sem declaração);
- §13.13.6: proibições (default implícito; `modo_inicial` em política fixa; política no documento externo);
- §13.13.7: campo `excesso.modo` (legado — supersedido para telas novas; não conflita pois está no documento externo);
- §13.13.8: compatibilidade com telas legadas;
- §13.13.9: separação entre JSON estrutural e documento externo (tabela de responsabilidades);
- §13.13.10: quatro cenários futuros mínimos (§36.2);
- §13.13.11: regra de alinhamento no cenário verboso de dois níveis (§36.3).

### 3.2 O que não foi alterado

- Seções §13.1 a §13.10: preservadas integralmente.
- §12.7 (exemplo normativo com `excesso.modo`): preservado como referência histórica.
- Nenhum arquivo de configuração JSON foi alterado.

---

## 4. Arquivo: `docs/contratos/contrato_console.md`

### 4.1 Modificações aplicadas

**§21.4 — Relação com `modo normal`**

- **Problema**: texto afirmava que o registro não constitui "decisão sobre o valor
  padrão do modo inicial, que permanece adiado" — mas D23 encerra esse adiamento.
- **Correção**: a última frase foi substituída por nota de que `modo normal` não é
  sinônimo automático de `somente_nao_verboso`.

**§21.5 — Alternância pela tecla V**

- **Problema**: afirmava que chip e tecla V estão presentes em "demonstrações de
  dados multinível do console" sem restrição por política — incompatível com D23.
- **Correção**: reestruturada com distinção explícita entre telas alternáveis (chip
  obrigatório, V disponível) e telas de modo único (sem chip obrigatório, V não
  aplicável). Restante do comportamento de alternância preservado.

**§21.7 — Modo inicial**

- **Problema**: afirmava que o modo inicial vem do campo `excesso` no documento
  JSON externo de conteúdo, e que a definição do padrão estava adiada conforme
  §43 item 3 — ambos contraditórios com D23.
- **Correção**: substituída pela regra D23: modo inicial determinado pela política
  no JSON estrutural (`formato.excesso.politica_modo`); três casos (somente
  verbosa, somente não verbosa, alternável); campo `excesso.modo` do documento
  externo registrado como supersedido para telas novas.

**§21.10 — Remissões**

- Atualizadas referências de `contrato_json_console.md` e `contrato_tela_json.md`
  para incluir política de modo.

**§21.11 — Políticas de modo por tela (D23) — NOVA SEÇÃO**

Adicionada seção com:
- §21.11.1: tela somente verbosa — comportamento, ausência de V e chip;
- §21.11.2: tela somente não verbosa — comportamento, ausência de V e chip;
- §21.11.3: tela alternável — comportamento, chip obrigatório, `modo_inicial` obrigatório;
- §21.11.4: escopo de obrigatoriedade (telas novas vs. legadas);
- §21.11.5: remissão aos cenários futuros mínimos.

### 4.2 O que não foi alterado

- §21.1 (escopo exclusivo): preservado.
- §21.2 (modo não verboso): preservado.
- §21.3 (modo verboso): preservado.
- §21.6 (estado visual da sessão): preservado.
- §21.8 (redimensionamento): preservado.
- §21.9 (paginação e impossibilidade): preservado.

---

## 5. Arquivo: `docs/contratos/contrato_barra_de_menus.md`

### 5.1 Modificações aplicadas

**§22.1 — Existência condicional**

- **Problema**: condição do chip era "configurada para permitir alternância
  verbosa" — vocabulário pré-D23, sem referência à política declarada.
- **Correção**: condição refere-se à política `"alternavel"` declarada em
  `formato.excesso.politica_modo`; telas de modo único explicitamente excluídas;
  inferência pelo renderer proibida.

**§22.3 — Estado de sessão**

- **Problema**: afirmava que ao recarregar, o modo inicial é determinado "pela
  configuração declarativa do documento de conteúdo" — contraditório com D23.
- **Correção**: modo inicial determinado pela política no JSON estrutural
  (`formato.excesso.politica_modo` e `modo_inicial`).

**§22.7 — Remissões**

- Atualizadas com referências a `contrato_tela_json.md` §33 e inclusão de
  "políticas de modo" nas referências existentes.

**§22.8 — Três políticas de modo e o chip `[V] Verboso` (D23) — NOVA SEÇÃO**

Adicionada tabela de presença/ausência do chip por política; definição de que o
chip representa disponibilidade de alternância (não modo corrente nem política em
si); proibição de exibir chip por inferência.

### 5.2 O que não foi alterado

- §22.2 (semântica da alternância): preservada.
- §22.4 (isolamento): preservado.
- §22.5 (inaplicabilidade fora do escopo): preservada.
- §22.6 (posição canônica): preservada.

---

## 6. Arquivo: `docs/contratos/contrato_tela_json.md`

### 6.1 Modificações aplicadas

**§33.2 — separação entre política de modo e estado de visualização**

- **Problema**: afirmava que o `tela.json` não armazena nem declara modo de
  visualização, e que o modo é determinado pelo documento externo — ambos
  contraditórios com D23.
- **Correção**: reestruturada para distinguir política (declarada no JSON
  estrutural) de estado de visualização (não persistido). Título atualizado.

**§33.5 — Remissões**

- Atualizadas com referências a `contrato_barra_de_menus.md` §22 e "política de
  modo".

**§33.6 — Declaração de política de modo no JSON estrutural (D23) — NOVA SEÇÃO**

Adicionada seção com:
- §33.6.1: localização dos campos (`formato.excesso` do elemento `console`);
- §33.6.2: obrigação declarativa para telas novas ou revisadas;
- §33.6.3: compatibilidade com telas legadas;
- §33.6.4: coerência com a barra de menus (chip ↔ política);
- §33.6.5: política não está no documento externo.

### 6.2 O que não foi alterado

- §33.1 (JSON estrutural não contém dados de conteúdo): preservado.
- §33.3 (associação feita pelo ponto de entrada): preservado.
- §33.4 (responsabilidades preservadas): preservado.

---

## 7. Arquivo: `docs/contratos/contrato_composicao_corpo.md`

### 7.1 Modificações aplicadas

**§12.7 — Remissões**

- Atualizadas com referência a `contrato_tela_json.md` §33 e "políticas de modo".

**§12.8 — Delegação de política de modo ao console (D23) — NOVA SEÇÃO**

Adicionada seção estabelecendo que:
- A política de modo pertence ao elemento `console`, não à composição do corpo.
- O corpo preserva a área útil independentemente da política.
- O corpo não infere política a partir de parâmetros geométricos.
- Telas de modo único recebem a mesma área que telas alternáveis.

### 7.2 O que não foi alterado

- §12.1 a §12.6: preservados integralmente.

---

## 8. Arquivo: `docs/NOMENCLATURA.md`

### 8.1 Modificações aplicadas

**§19.6 — Decisões deferidas (ADR-0028)**

- Removida linha sobre "valores padrão (incluindo modo padrão quando o campo de
  excesso estiver ausente)" — D23 encerrou esse adiamento para telas novas.
- Adicionado item sobre estratégia de migração de telas legadas (permanece adiado).

**§19.7 — Política de modo de apresentação por tela (D23) — NOVA SEÇÃO**

Adicionada seção com:
- §19.7.1: termos canônicos — `política de modo`, `somente verbosa`, `somente não
  verbosa`, `alternável`, `modo inicial (D23)`, `tela legada`;
- §19.7.2: campos canônicos no JSON estrutural (tabela `formato.excesso`);
- §19.7.3: distinções obrigatórias D23 — política × estado; inicial × corrente;
  somente não verbosa × alternável em modo não verboso; legada × nova;
  `excesso.modo` legado × `politica_modo` D23;
- §19.7.4: nota sobre `modo normal` × `somente não verboso` (política ≠ estado);
- §19.7.5: itens de D23 ainda deferidos.

### 8.2 O que não foi alterado

- §19.1 a §19.5: preservados.

---

## 9. Arquivo: `docs/adr/INDICE_ADR.md`

### 9.1 Modificações aplicadas

Entrada da ADR-0028 atualizada para incluir:
- D23 e as três políticas de modo.
- Campos canônicos `formato.excesso.politica_modo` e `formato.excesso.modo_inicial`.
- Chip e tecla V restritos a telas alternáveis.
- Telas legadas preservadas.
- Cenários futuros §36.2 e regra de alinhamento §36.3.
- Registro de segunda aplicação documental (2026-07-18).

---

## 10. Arquivo: `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`

### 10.1 Modificações aplicadas

Entrada de histórico (§47) adicionada para 2026-07-18 registrando esta segunda
aplicação documental, os campos canônicos definidos e todos os documentos
atualizados.

---

## 11. Arquivos não alterados

| Arquivo | Motivo |
|---|---|
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md` | Registro histórico da aplicação D1–D22; preservado sem alteração |
| `docs/relatorios/RELATORIO_QA_*.md` | Todos os relatórios de QA preservados sem alteração |
| `docs/handoff/H-0037-*.md` | H-0037 permanece no estado BLOQUEADO_POR_MUDANCA_DOCUMENTAL; não alterado |
| `config/telas/demo/*.json` | Configurações reais; proibido alterar (instrução explícita) |
| `demo/*.py` | Código; proibido alterar |
| `tela/*.py` | Código; proibido alterar |

---

## 12. Inventário de divergências corrigidas

| Código | Contrato | Seção | Divergência | Correção |
|---|---|---|---|---|
| DIV-D23-01 | `contrato_json_console.md` | §13.11 | "Os mesmos dados devem ser observáveis nos modos verboso e não verboso na mesma tela" — inválido para telas de modo único | Restrito a telas alternáveis; telas de modo único excluídas |
| DIV-D23-02 | `contrato_console.md` | §21.5 | Chip e tecla V implicitamente presentes em todas as telas multinível | Restritos a telas com política `"alternavel"` |
| DIV-D23-03 | `contrato_console.md` | §21.7 | Modo inicial vem do documento externo de conteúdo; adiamento de §43 item 3 ainda ativo | Modo inicial determinado pela política no JSON estrutural; adiamento encerrado para telas novas |
| DIV-D23-04 | `contrato_barra_de_menus.md` | §22.1 | Chip condicionado a "configurada para permitir alternância verbosa" — vocabulário pré-D23 | Condição refere-se à política `"alternavel"` por nome canônico |
| DIV-D23-05 | `contrato_barra_de_menus.md` | §22.3 | Modo inicial ao recarregar determinado pelo documento de conteúdo | Determinado pela política no JSON estrutural |
| DIV-D23-06 | `contrato_tela_json.md` | §33.2 | `tela.json` não armazena nem declara modo; modo determinado pelo documento externo — contradiz D23 | Distingue política (no JSON estrutural) de estado de visualização (não persistido) |

---

## 13. Campos canônicos — resolução do §43 item 3

O §43 item 3 da ADR-0028 adiava os "nomes concretos dos campos para declaração
da política de modo de apresentação da tela e do modo inicial em telas alternáveis
(conceito decidido em D23 e §25; mecanismo concreto de schema adiado)".

Esta aplicação documental resolve esse adiamento, definindo como canônicos:

```json
{
  "tipo": "console",
  "formato": {
    "excesso": {
      "politica_modo": "alternavel",
      "modo_inicial": "nao_verboso"
    }
  }
}
```

Os campos pertencem ao **JSON estrutural da tela** (elemento `console`). O
documento externo de conteúdo não contém esses campos.

O campo `excesso.modo` que existia no documento externo de conteúdo (normativo em
`contrato_json_console.md` §12.7) é registrado como supersedido para telas novas
ou revisadas. Telas legadas continuam compatíveis com seu estado original.

---

## 14. Matriz de validade (resumo normativo)

| `politica_modo` | `modo_inicial` | Válido? |
|---|---|---|
| `"somente_verboso"` | ausente | VÁLIDO |
| `"somente_nao_verboso"` | ausente | VÁLIDO |
| `"alternavel"` | `"verboso"` | VÁLIDO |
| `"alternavel"` | `"nao_verboso"` | VÁLIDO |
| `"alternavel"` | ausente | **INVÁLIDO** |
| `"somente_*"` | qualquer valor | **INVÁLIDO** |
| valor desconhecido | qualquer | **INVÁLIDO** |
| ausente (tela nova) | qualquer | **INVÁLIDO** |

---

## 15. Verificações de integridade

| # | Verificação | Resultado |
|---|---|---|
| 1 | D23 propagada para todos os contratos afetados | CONFIRMADO |
| 2 | Campos canônicos definidos e documentados | CONFIRMADO |
| 3 | Matriz de validade presente em `contrato_json_console.md` §13.13.3 | CONFIRMADO |
| 4 | Quatro exemplos válidos presentes | CONFIRMADO |
| 5 | Exemplos inválidos presentes | CONFIRMADO |
| 6 | Chip [V] restrito a telas alternáveis em todos os contratos | CONFIRMADO |
| 7 | Modo inicial por política (não pelo documento externo) em todos os contratos | CONFIRMADO |
| 8 | Compatibilidade de telas legadas preservada | CONFIRMADO |
| 9 | Nenhum arquivo de configuração JSON alterado | CONFIRMADO |
| 10 | Nenhum código alterado | CONFIRMADO |
| 11 | H-0037 não alterado | CONFIRMADO |
| 12 | Relatório da aplicação D1–D22 não alterado | CONFIRMADO |
| 13 | Todos os relatórios de QA preservados | CONFIRMADO |
| 14 | Campo `excesso.modo` legado documentado como supersedido (não removido) | CONFIRMADO |
| 15 | §43 item 3: adiamento resolvido para schema concreto; migração legada permanece adiada | CONFIRMADO |
| 16 | Cenários futuros mínimos §36.2 propagados | CONFIRMADO |
| 17 | Regra de alinhamento §36.3 propagada | CONFIRMADO |
| 18 | Separação JSON estrutural / documento externo mantida | CONFIRMADO |
| 19 | Nenhum default implícito introduzido para telas novas | CONFIRMADO |
| 20 | Delegação de política ao console (corpo não infere política) | CONFIRMADO |

---

## 16. Documentos afetados — lista completa

| Documento | Tipo de alteração |
|---|---|
| `docs/contratos/contrato_json_console.md` | §13.11 corrigido; §13.12 atualizado; §13.13 adicionado |
| `docs/contratos/contrato_console.md` | §21.4 atualizado; §21.5 corrigido; §21.7 corrigido; §21.10 atualizado; §21.11 adicionado |
| `docs/contratos/contrato_barra_de_menus.md` | §22.1 corrigido; §22.3 corrigido; §22.7 atualizado; §22.8 adicionado |
| `docs/contratos/contrato_tela_json.md` | §33.2 corrigido; §33.5 atualizado; §33.6 adicionado |
| `docs/contratos/contrato_composicao_corpo.md` | §12.7 atualizado; §12.8 adicionado |
| `docs/NOMENCLATURA.md` | §19.6 atualizado; §19.7 adicionado |
| `docs/adr/INDICE_ADR.md` | Entrada ADR-0028 atualizada |
| `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md` | §47 — entrada de histórico adicionada |

---

## 17. Status da aplicação

```
ADR_APPLICATION_COMPLETED
```

A revisão D23 da ADR-0028 está integralmente propagada nos contratos documentais.
Os campos canônicos `formato.excesso.politica_modo` e `formato.excesso.modo_inicial`
estão definidos. O H-0037 pode agora ser desbloqueado da condição
`BLOQUEADO_POR_MUDANCA_DOCUMENTAL` quando assim autorizado.

---

## 18. Estado Git — Início da Aplicação Documental

### 18.1 Classificação das informações

As informações desta seção dividem-se em três categorias:

- **Observação direta**: dados coletados durante a etapa de patch (PATCH_APLICACAO_ADR, 2026-07-18).
- **Reconstrução evidenciada**: dados inferíveis com evidência de relatórios preservados e histórico Git.
- **Não recuperável**: dados cujo estado preciso não pode ser verificado sem evidência documental.

### 18.2 Estado observado durante o patch (observação direta)

Coletado na execução do PATCH_APLICACAO_ADR, após a aplicação original e o QA:

```
Branch: master
HEAD: f6982d0 (docs: corrige whitespace do fechamento H-0036)

git status --short:
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_barra_de_menus.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md
?? docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0028.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_H-0037_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0028.md
?? tela/__pycache__/

git diff --cached --name-only: (vazio — nenhum arquivo em stage)
git diff --check: (sem saída — GIT_DIFF_CHECK_OK, exit code 0)
```

### 18.3 Estado no início da aplicação original (reconstrução evidenciada)

A aplicação original não registrou seu estado inicial. As informações abaixo são reconstruídas a partir do relatório de QA preservado, do histórico Git e das propriedades estruturais do diff.

```yaml
branch: master
  fonte: reconstrução — git log (comprovável)

head: f6982d0
  fonte: reconstrução — git log (comprovável)
  nota: >
    f6982d0 é o HEAD atual; a aplicação operou exclusivamente na working tree
    sem criar commit; portanto, HEAD já era f6982d0 ao início da aplicação.

stage:
  valor: NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL
  nota: >
    Provavelmente vazio — a aplicação foi uma operação de working tree; o QA
    não encontrou nada em stage; evidência direta do estado inicial não existe.

arquivos_modificados_acumulados:
  rastreados_no_inicio: NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL
  inferencia: >
    Os 7 arquivos agora com status M presumivelmente não tinham modificações
    acumuladas ao início da aplicação. O git diff mostra 971 insertions(+) e
    0 deletions(-), consistente com adições sobre versões comprometidas;
    porém o estado exato da working tree antes da aplicação não é comprovável.

arquivos_nao_rastreados_acumulados:
  ADR-0028:
    status: presente como não rastreado antes da aplicação
    fonte: >
      RELATORIO_QA_POS_PATCH_ADR-0028_REVISAO_MODOS_POR_TELA.md confirma
      a condição como herdada de sessões anteriores.
  RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md:
    status: não existia antes da aplicação — criado durante esta etapa
  outros_nao_rastreados: NAO_RECONSTRUIVEL_COM_EVIDENCIA_DISPONIVEL

arquivos_inesperados: nenhum identificado
```

---

## 19. Diff Real da Aplicação

### 19.1 Resultado de `git diff --name-status` (coletado durante o patch)

```
M	docs/NOMENCLATURA.md
M	docs/adr/INDICE_ADR.md
M	docs/contratos/contrato_barra_de_menus.md
M	docs/contratos/contrato_composicao_corpo.md
M	docs/contratos/contrato_console.md
M	docs/contratos/contrato_json_console.md
M	docs/contratos/contrato_tela_json.md
```

### 19.2 Resultado de `git diff --stat` (coletado durante o patch)

```
docs/NOMENCLATURA.md                        | 139 ++++++++++
docs/adr/INDICE_ADR.md                      |   1 +
docs/contratos/contrato_barra_de_menus.md   |  90 +++++++
docs/contratos/contrato_composicao_corpo.md |  92 +++++++
docs/contratos/contrato_console.md          | 165 ++++++++++++
docs/contratos/contrato_json_console.md     | 386 ++++++++++++++++++++++++++++
docs/contratos/contrato_tela_json.md        |  98 +++++++
7 files changed, 971 insertions(+)
```

### 19.3 Resultado de `git diff --check` (coletado durante o patch)

```
(sem saída)
Exit code: 0
Resultado: GIT_DIFF_CHECK_OK — nenhum problema de whitespace nos 7 arquivos rastreados
```

### 19.4 Resultado de `git diff --cached --name-only` (coletado durante o patch)

```
(vazio — nenhum arquivo em stage)
```

### 19.5 ADR-0028 (arquivo não rastreado)

O arquivo `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
aparece como `??` (não rastreado). A modificação (adição do §47) não é verificável
por `git diff`. Verificada por leitura direta durante o patch: §47 presente com
entrada de 2026-07-18, campos canônicos declarados, consistente com o declarado
pela aplicação.

### 19.6 Este relatório (arquivo não rastreado)

O arquivo `docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md`
aparece como `??` (não rastreado). Foi criado durante a aplicação; seu conteúdo
não é verificável por `git diff` mas é diretamente legível.

### 19.7 Natureza das alterações (7 arquivos rastreados)

| Arquivo | Inserções | Tipo | Seções afetadas |
|---|---|---|---|
| `contrato_json_console.md` | 386 | Modificação | §13.11 corrigido; §13.12 atualizado; §13.13 nova |
| `contrato_console.md` | 165 | Modificação | §21.4–§21.5–§21.7–§21.10 corrigidos; §21.11 nova |
| `contrato_tela_json.md` | 98 | Modificação | §33.2–§33.5 corrigidos; §33.6 nova |
| `contrato_barra_de_menus.md` | 90 | Modificação | §22.1–§22.3–§22.7 corrigidos; §22.8 nova |
| `contrato_composicao_corpo.md` | 92 | Modificação | §12.7 atualizado; §12.8 nova |
| `docs/NOMENCLATURA.md` | 139 | Modificação | §19.6 atualizado; §19.7 nova |
| `docs/adr/INDICE_ADR.md` | 1 | Modificação | Linha ADR-0028 atualizada |

Todas as alterações são inserções puras (0 deletions). Nenhum arquivo técnico
(`.py`, `config/`) foi modificado.

---

## 20. Busca de Resíduos de Linguagem Pré-D23

### 20.1 Termos pesquisados nas adições dos arquivos modificados

| Termo | Ocorrências nas adições | Contexto nas adições | Natureza | Tratamento necessário? |
|---|---|---|---|---|
| `excesso.modo` | Sim | §13.13.7 (campo legado documentado); §12.7 (exemplo normativo pré-D23) | Documentação de campo supersedido | Não — contexto correto |
| `politica_modo` | Sim | Seções novas D23 em todos os contratos | Regra ativa D23 | Não — uso canônico |
| `modo_inicial` | Sim | Seções novas — condicionado a `alternavel` | Regra ativa D23 | Não — uso canônico |
| `normal` / `modo normal` | Sim | §21.4 (nota: `modo normal` ≠ `somente_nao_verboso`); §19.7.4 (desambiguação explícita) | Desambiguação — não regra ativa | Não — contextualizado |
| `verboso` / `não verboso` / `nao_verboso` | Sim | Políticas e valores canônicos D23 | Regra ativa D23 | Não — uso canônico |
| `[V] Verboso` | Sim | §22.1–§22.8 (chip condicionado a `alternavel`) | Regra ativa D23 | Não — uso canônico |
| `toda tela` | Não encontrado nas adições | — | — | Não |
| `tela legada` | Sim | §13.13.8; §33.6.3; §21.11.4; §19.7.1 | Preservação explícita de compatibilidade | Não — correto |
| `default` | Sim | §13.13.6 ("Não existe default implícito..."); §19.7 | Proibição explícita | Não — correto |
| `migração` | Sim | §19.6; §13.13.8 ("até futura decisão de migração") | Adiamento declarado | Não — correto |
| `matriz` / `matricial` | Sim | `matriz`: título de §13.13.3 ("Matriz de validade"); `matricial`: exclusão de escopo (referência à ADR-0025) | Título de seção normativa; exclusão de escopo | Não — correto |
| `mesmos dados` | Sim | §13.11 ("Para telas alternáveis, os mesmos dados devem ser observáveis...") | Condicionado a telas alternáveis | Não — correto após revisão |
| `dois modos` | Sim | Nota sobre `alternável` que suporta dois modos | Definição de política | Não — correto |

### 20.2 Resíduos identificados em seções antigas (não modificadas por esta aplicação)

Os itens abaixo existem em seções anteriores a D23 que estavam fora do escopo
desta aplicação. São registrados para rastreabilidade; não exigem tratamento
nesta etapa (ver observação APLIC-MODOS-QA-004).

| Arquivo | Seção | Termo residual | Impacto | Status |
|---|---|---|---|---|
| `contrato_barra_de_menus.md` | §14 | "`[V]` só existe quando a instância de `console` declara que aceita modo verboso" | Pré-D23; sem referência a `politica_modo: "alternavel"` | Mitigado por §22.5 |
| `contrato_barra_de_menus.md` | §20 | Critério sem escopo D23 | Critério não atualizado | Mitigado por §22.5 |
| `contrato_composicao_corpo.md` | §4.4 | `tipo_exibicao: normal \| verboso` | Opção binária pré-D23 | Mitigado por §12.8 |
| `contrato_tela_json.md` | §14 | "quando a instância permite" sem escopo D23 | Sem escopo D23 | Mitigado por §33.6 |
| `contrato_console.md` | §6 | "modo normal é o default" | Pré-D23; sem escopo multinível | Mitigado por §21.1 |

### 20.3 Confirmações normativas

1. Nenhuma regra ativa exige alternância em toda tela: confirmado (§21.1 e §22.5 restringem ao escopo multinível e à política `alternavel`).
2. Nenhuma regra ativa exige chip em tela fixa: confirmado (§22.1 e §22.8 condicionam chip a `alternavel`).
3. Telas novas não recebem default: confirmado (§13.13.6 proíbe default implícito).
4. Telas legadas não são reinterpretadas: confirmado (§13.13.8).
5. `excesso.modo` antigo não é forma canônica de D23: confirmado (§13.13.7 declara campo supersedido para telas novas).
6. Ocorrências de `matriz` e `matricial` estão em título de seção normativa ou em exclusões de escopo: confirmado.
7. Não há política no documento externo de conteúdo: confirmado (§13.13.6 e §13.13.9).

---

## 21. Inventário Nominal dos Itens Legados H-0036

### 21.1 Composição verificada

Os seis itens H-0036 são **três telas estruturais** e **três documentos externos de
conteúdo** — não seis telas. Verificado por inspeção direta de `config/telas/demo/`
e `demo/demo.py`.

### 21.2 Inventário individual

**Item 1**

```yaml
id_ou_nome: h0036_console_hierarquia
caminho: config/telas/demo/h0036_console_hierarquia.json
tipo:
  - tela_estrutural
associacao: h0036_hierarquia_conteudo.json (declarado em demo.py)
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

**Item 2**

```yaml
id_ou_nome: h0036_console_tabela
caminho: config/telas/demo/h0036_console_tabela.json
tipo:
  - tela_estrutural
associacao: h0036_tabela_conteudo.json (declarado em demo.py)
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

**Item 3**

```yaml
id_ou_nome: h0036_console_conjuntos
caminho: config/telas/demo/h0036_console_conjuntos.json
tipo:
  - tela_estrutural
associacao: h0036_conjuntos_conteudo.json (declarado em demo.py)
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

**Item 4**

```yaml
id_ou_nome: h0036_hierarquia_conteudo
caminho: config/telas/demo/h0036_hierarquia_conteudo.json
tipo:
  - conteudo_externo
associacao: h0036_console_hierarquia.json
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

**Item 5**

```yaml
id_ou_nome: h0036_tabela_conteudo
caminho: config/telas/demo/h0036_tabela_conteudo.json
tipo:
  - conteudo_externo
associacao: h0036_console_tabela.json
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

**Item 6**

```yaml
id_ou_nome: h0036_conjuntos_conteudo
caminho: config/telas/demo/h0036_conjuntos_conteudo.json
tipo:
  - conteudo_externo
associacao: h0036_console_conjuntos.json
politica_D23_declarada: false
tratamento:
  - legado_preservado
reinterpretacao_automatica: proibida
migracao_nesta_etapa: nao
```

### 21.3 Notas sobre o catálogo

- As três telas estruturais são acessadas via argumento de `demo.py`:
  `python demo/demo.py h0036_console_hierarquia` etc.
- Mapeamentos tela→conteúdo declarados em `demo.py`:
  `"h0036_console_hierarquia": "h0036_hierarquia_conteudo"`,
  `"h0036_console_tabela": "h0036_tabela_conteudo"`,
  `"h0036_console_conjuntos": "h0036_conjuntos_conteudo"`.
- Nenhum dos seis arquivos contém `politica_modo` ou `modo_inicial`.
  Ausência é compatibilidade histórica (§13.13.8), não erro.
- Nenhuma política é inferida; nenhum fixture foi alterado nesta aplicação.

---

## 22. Correção Pós-QA (PATCH_APLICACAO_ADR)

### 22.1 Origem

```yaml
qa_de_origem: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
status_de_origem: ADR_APPLICATION_REJECTED
```

### 22.2 Achados tratados

```yaml
achados_tratados:
  APLIC-MODOS-QA-001:
    arquivo: docs/contratos/contrato_json_console.md
    correcao_aplicada: >
      Adicionada linha à matriz §13.13.3:
        "alternavel" | valor desconhecido | INVÁLIDO —
        valor de modo_inicial não pertence ao conjunto admitido.
      Adicionada cláusula ao §13.13.6 definindo explicitamente "valor
      desconhecido" como qualquer valor fora do conjunto ("verboso",
      "nao_verboso").

  APLIC-MODOS-QA-002:
    arquivo: docs/relatorios/RELATORIO_APLICACAO_ADR-0028_REVISAO_MODOS_POR_TELA.md
    correcao_aplicada: >
      Adicionadas seções 18–22: estado Git inicial (com distinção entre
      observação direta, reconstrução evidenciada e não recuperável), diff real
      (git diff --stat, git diff --check, git diff --name-status,
      git diff --cached --name-only), busca de resíduos, inventário nominal
      dos seis itens legados H-0036 (com tipo verificado de cada item), e
      esta seção de correção pós-QA.
```

### 22.3 Observações não tratadas como patch

```yaml
observacoes_nao_tratadas_como_patch:
  APLIC-MODOS-QA-003:
    titulo: "Inconsistência interna §43 vs. §47 da ADR-0028"
    motivo_de_nao_tratar: ADR preservada; §43 não pode ser alterado sem nova decisão
  APLIC-MODOS-QA-004:
    titulo: "Seções pré-D23 não reconciliadas em múltiplos contratos"
    motivo_de_nao_tratar: Outros contratos fora do escopo deste patch; aguarda futura revisão editorial
  APLIC-MODOS-QA-005:
    titulo: "ADR-0028 não rastreada por git"
    motivo_de_nao_tratar: Estado de rastreamento não alterado; ADR preservada
```

### 22.4 Status após patch

Os dois achados corretivos foram tratados. O conteúdo documental permanece
substancialmente correto conforme avaliado pelo QA. Esta seção não declara a
aplicação aprovada.

```yaml
status_pos_patch: AGUARDA_QA_POS_PATCH
proxima_categoria: QA_POS_PATCH_APLICACAO_ADR
```
