# RELATORIO_QA_H-0027_HANDOFF

## 1. Identificação

- Artefato auditado: `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`
- Categoria processual executada: `QA_HANDOFF`
- ADR base: `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md` (status `aceita`)
- Auditor: agente formal de QA do handoff H-0027
- Data: 2026-07-12
- Branch: `master`
- Commit base: `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria`
- Handoff precedente (informado): `docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md`
- Relatório precedente (informado): `docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md`
- Relatório de implementação esperado: `docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`

Limites estritos desta etapa:

- somente auditar o handoff H-0027;
- somente produzir este relatório;
- não corrigir o handoff;
- não implementar código;
- não alterar testes, ADRs, contratos, nomenclatura ou índice;
- não criar outro handoff;
- não preparar commit;
- não executar etapa posterior.

---

## 2. Estado Git inicial

Comandos executados a partir de `scripts/` (raiz efetiva dos caminhos declarados na
documentação; toplevel Git em `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`).

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 27 +++++++++------
 .../adr/ADR-0007-tela-processamento-composicao.md  | 15 ++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 40 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    |  7 +++-
 scripts/docs/contratos/contrato_tela_json.md       | 15 +++++---
 6 files changed, 72 insertions(+), 33 deletions(-)

git diff --check
(sem saída)

git diff --cached --stat
(sem saída)

git diff --cached --name-only
(sem saída)
```

### 2.1 Confirmação do estado informado pelo autor

Estado comprovado informado pelo autor do handoff (H-0027 seção 2.1):

- stage vazio — **CONFIRMADO** (`git diff --cached --stat` sem saída);
- seis arquivos documentais rastreados modificados pela aplicação da ADR-0019 — **CONFIRMADO** (os mesmos seis `M` em `git status --short`, mesma contagem de diff stat);
- ADR-0019, relatórios do ciclo, handoff H-0027 e `tela/__pycache__/` não rastreados — **CONFIRMADO** (as sete entradas `??` em `git status --short`); observa-se que o handoff H-0027 está entre os não rastreados, como esperado para arquivo recém-criado;
- nenhum arquivo rastreado foi alterado durante a criação do handoff — **CONFIRMADO** (os seis arquivos `M` são exatamente os alterados pela aplicação documental da ADR-0019, conforme registrado em `RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` seção 2 e `RELATORIO_APLICACAO_ADR-0019.md` seção 11; nenhuma alteração em `tela/*.py`);
- único arquivo criado nessa etapa: `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md` — **CONFIRMADO** como presente e não rastreado.

A descrição do estado Git no handoff (H-0027:66-114) é fiel ao estado real. O
handoff reconhece corretamente as alterações documentais como não constituindo
divergência e identifica qualquer alteração rastreada inesperada em `tela/*.py`
como divergência relevante (H-0027:114).

O handoff descreve o stage como vazio, a branch como `HEAD (master)` e o commit
como `40015b6` (H-0027:72) — tudo confirmado. Não há afirmações não comprovadas
sobre o estado Git.

---

## 3. Artefatos consultados

Leitura integral (autoridades normativas e evidência):

- `docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/NOMENCLATURA.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md`
- `docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`

Leitura das seções diretamente relevantes (ADRs de contexto):

- `docs/adr/ADR-0007-tela-processamento-composicao.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- `docs/adr/INDICE_ADR.md`

Leitura para confirmar estado atual (implementação e testes):

- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`

Implementação e testes atuais foram usados somente para confirmar a fidelidade
do diagnóstico do handoff (seção 6) e a necessidade real dos arquivos
permitidos — nunca para redefinir as autoridades normativas.

Buscas adicionais (`rg`) executadas para confirmar:

- ausência de definição contratual de `elemento_por_id`/`elementos_por_tipo`;
- ausência de validação de cardinalidade global de `dashboard` no loader;
- ausência de aplicação de `grupo.arranjo`/`grupo.distribuicao` no renderizador;
- presença dos quatro testes históricos em `tela/teste_loader.py`;
- presença das constantes `ARRANJOS_CORPO_VALIDOS`,
  `MODOS_DISTRIBUICAO_CORPO_VALIDOS`, `TIPOS_CORPO_VALIDOS` no loader.

---

## 4. Matriz obrigatória

| Área | Cobertura no handoff | Evidência por linha | Resultado |
| --- | --- | --- | --- |
| D1–D7 | Todas as sete decisões cobertas e fiéis | H-0027:154-161 (tabela D1–D7); ADR-0019:104-233 | SUFICIENTE |
| Loader | Validação recursiva, níveis 1–3, nível 4 inválido, múltiplos filhos, grupos irmãos, arranjos, `distribuicao` por grupo, modos, associação a filhos diretos, ausência de limite global de dashboards, diagnóstico determinístico com caminho | H-0027:366-423 (seção 13); H-0027:575-603 (seção 17) | SUFICIENTE |
| Modelo | Construção recursiva, preservação de filhos e ordem, ausência de achatamento, tipos funcionais existentes, limite 3 níveis, `_campos_inertes` com `arranjo`/`distribuicao` | H-0027:427-465 (seção 14) | SUFICIENTE |
| Renderizador | Composição recursiva por container, verticais/horizontais, combinações, distribuição independente e por filhos diretos, ausência preservada, modos, maiores restos e ordem, propagação de largura/altura, múltiplos grupos/funcionais/dashboards, grupo sem moldura | H-0027:469-559 (seção 15) | SUFICIENTE |
| Testes | Zero/um/dois/três níveis, nível 4, irmãos, múltiplos funcionais, mistura, verticais/horizontais, combinações, ausência, `igual`/`percentual`/`fracao`, vetores inválidos, filhos diretos, múltiplos dashboards, regressões, diagnósticos determinísticos; substituir não remover | H-0027:656-726 (seção 20) | SUFICIENTE |
| Arquivos permitidos | Os sete `tela/*.py` + IMP-0028 + `config/telas/` para novas fixtures; proibição efetiva dos 4 JSONs ativos; registro obrigatório de cada fixture nova | H-0027:256-274 (seção 8); H-0027:278-292 (seção 9) | SUFICIENTE |
| Arquivos proibidos | ADRs, contratos, nomenclatura, índice, handoffs, relatórios históricos, JSONs ativos, arquivos fora da capacidade, commit e push | H-0027:278-292 (seção 9); H-0027:320-339 (escopo negativo); H-0027:798-804 (proibição de commit) | SUFICIENTE |
| Preservações | Planas, um nível, distribuições vertical/horizontal do corpo raiz, ausência, ordem, maiores restos, `console`/`lancador`/`dashboard`, passividade do dashboard, navegação, JSONs existentes, diagnósticos não relacionados, suítes anteriores | H-0027:343-362 (seção 12) | SUFICIENTE |
| Critérios de aceite | Níveis 1–3 aceitos, 4 rejeitado, árvore preservada, renderização recursiva, multiplicidade, arranjos combinados, distribuição em grupos, múltiplos dashboards, preservações, estado Git, arquivos alterados, IMP-0028 | H-0027:637-652 (seção 19) | SUFICIENTE |
| Relatório IMP-0028 | Exigido em caminho canônico; conteúdo obrigatório cobre arquivos, camadas, profundidade, multiplicidade, dashboards, testes, comandos, preservações, limitações, Git, bloqueios | H-0027:748-776 (seção 22) | SUFICIENTE |
| Bloqueios | Estado Git divergente, regra ausente, contradição não explicada, arquivo necessário proibido, capacidade exigindo documento adicional, arquitetura não definida, suítes não zero; executor não preenche lacunas | H-0027:780-794 (seção 23) | SUFICIENTE |

---

## 5. Verificação das decisões D1–D7

A tabela abaixo cruza cada decisão da ADR-0019 com o tratamento dado pelo
handoff H-0027. Todas as sete decisões estão aprovadas (ADR-0019 status
`aceita`; `RELATORIO_QA_POS_PATCH_ADR-0019.md` status `ADR_APPROVED`;
`RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md` status
`ADR_APPLICATION_APPROVED_WITH_NOTES`).

| ID | Enunciado ADR-0019 | Tratamento no handoff | Evidência | Resultado |
| --- | --- | --- | --- | --- |
| D1 | Profundidade contada exclusivamente por níveis de nós `grupo` | Loader conta profundidade por grupos; corpo raiz não conta; listas `elementos[]` não contam; funcionais não contam | H-0027:155, 300, 366-397 (seção 13.1) | FIEL |
| D2 | Máximo de três níveis de grupos | Aceitação de grupos nos níveis 1, 2 e 3; construção recursiva | H-0027:156, 301, 673-678 | FIEL |
| D3 | Grupo do nível 3 pode conter múltiplos funcionais sem criar nível 4 | Cenário "Funcionais no nível 3" válido; três níveis com múltiplos funcionais no nível 3; funcionais não criam nível 4 | H-0027:157, 615, 678 | FIEL |
| D4 | Grupo filho de grupo do nível 3 é nível 4 e deve ser rejeitado | Rejeição estrutural de grupo no nível 4 com `TelaGrupoInvalido` e mensagem determinística com caminho | H-0027:158, 302, 382-386, 406-416, 577-584, 679 | FIEL |
| D5 | Múltiplos grupos irmãos permitidos | Múltiplos grupos irmãos no mesmo container; cenários válidos | H-0027:159, 304, 617-618, 680-681 | FIEL |
| D6 | Múltiplos elementos funcionais por grupo permitidos | Múltiplos filhos por grupo em todos os níveis válidos; cenário "Múltiplos filhos no grupo" | H-0027:160, 303, 616 | FIEL |
| D7 | Ausência de limite global de um dashboard por tela, inclusive em telas de processamento | Ausência de limite global de dashboards; seção 16 dedicada; múltiplos dashboards na mesma tela e em grupos distintos; alínea proibindo regra global | H-0027:161, 314, 419-423, 563-571, 631-632, 691 | FIEL |

### 5.1 Não reintrodução da contagem antiga

Verificação específica solicitada: o handoff **não reintroduz a contagem antiga
por listas `elementos[]`**. Em todos os pontos onde trata de profundidade, o
handoff usa a noção de "níveis de grupos" (D1) e estabelece que apenas nós
estruturais `grupo` contam (H-0027:155, 300, 366-397). Elementos funcionais são
tratados explicitamente como não constituintes de nível de grupo (H-0027:157,
615). Busca por "contagem antiga", "`elementos[]` conta como nível" ou
formulações equivalentes no handoff: nenhuma ocorrência. A descrição do
diagnóstico atual (H-0027:185-230) cita as linhas do código atual que contém as
restrições históricas do H-0012, mas sempre para indicar que **devem ser
substituídas** pela nova semântica, nunca para preservá-las.

---

## 6. Verificações por área

### 6.1 Identificação e estado (verificação 1)

- ID `H-0027` — correto (H-0027:53, 47).
- Título "Composição hierárquica do corpo com três níveis de grupos" e assunto coerentes com a descrição do frontmatter (H-0027:3, 47).
- Commit-base identificado corretamente como `40015b6 feat: implementa distribuicao horizontal percentual e fracionaria` (H-0027:72) — confirmado por `git log`.
- Reconhecimento das alterações documentais (seis arquivos `M`) e dos não rastreados (ADR-0019, relatórios, `tela/__pycache__/`) — fiel ao estado real (H-0027:66-97).
- Relatório previsto `IMP-0028` em caminho canônico (H-0027:58, 748-776).
- Ausência de afirmações não comprovadas sobre o estado Git: confirmada (todas as afirmações de H-0027 seção 2.1 coincidem com a saída real dos comandos).

### 6.2 Autoridades (verificação 2)

- ADR-0019 e contratos aplicados (`contrato_composicao_corpo`, `contrato_tela_json`, `contrato_json_tela_minima`) são identificados como autoridades principais (H-0027:118-143).
- Relatórios (`RELATORIO_QA_POS_PATCH_ADR-0019`, `RELATORIO_APLICACAO_ADR-0019`, `RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO`, `RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS`) são tratados como evidência técnica, não como arquitetura (H-0027:139-143; o levantamento é explicitamente "evidência técnica, não autoridade normativa").
- Implementação e testes não prevalecem sobre contratos: o handoff cita linhas de código apenas como diagnóstico do estado divergente atual que deve ser corrigido (H-0027:185-230), nunca como autoridade.
- ADR-0018 não é corrigida nem reinterpretada: a alínea "Correção da divergência de status da ADR-0018 (pendência documental separada)" está explicitamente no escopo negativo (H-0027:334); o handoff preserva a ADR-0018 como autoridade para a semântica de ausência de distribuição (H-0027:167-170, 548-553).
- Não há autoridade obrigatória omitida: ADR-0019, ADR-0015, ADR-0018, ADR-0010, ADR-0007 e os três contratos estão todos listados (H-0027:9-18, 118-143). A NOMENCLATURA e o INDICE_ADR constam como somente leitura (H-0027:38-39, 243-247).

### 6.3 Coesão da capacidade (verificação 3)

O handoff trata a capacidade como unidade coesa (H-0027:174-182): loader,
modelo, renderizador, testes, profundidade, multiplicidade, arranjo por
container, distribuição por container e múltiplos dashboards são cobertos de
forma articulada. As especificações por camada (seções 13, 14, 15) são
coerentes entre si:

- o loader aceita a árvore que o modelo preserva e que o renderizador percorre;
- `_campos_inertes` preserva `arranjo`/`distribuicao` do grupo para o
  renderizador (H-0027:441-443);
- o renderizador lê esses campos via `grupo._campos_inertes.get(...)`
  (H-0027:479-486);
- a rejeição do nível 4 no loader (H-0027:382-386) é coerente com a construção
  recursiva limitada a três níveis no modelo (H-0027:427-446) e com a ausência
  de renderização além do nível 3 no renderizador (implícito na composição
  recursiva por container).

Não foi identificada camada aceitando estrutura que outra não represente nem
renderize. A coesão é suficiente.

### 6.4 Loader (verificação 4)

O handoff exige (seção 13):

- validação recursiva (H-0027:368-388);
- profundidade contada por grupos (H-0027:382-388);
- níveis 1, 2 e 3 válidos (H-0027:385);
- nível 4 inválido (H-0027:383-384);
- múltiplos filhos em grupo (H-0027:380-381);
- múltiplos grupos irmãos (cobertura indireta via H-0027:304, 617-618);
- grupos verticais e horizontais (H-0027:375-376, 305);
- `distribuicao` própria por grupo (H-0027:389-391);
- validação dos modos `igual`, `percentual` e `fracao` (H-0027:389-391 via
  `_validar_distribuicao_corpo`);
- associação da distribuição somente aos filhos diretos
  (H-0027:542-546, `n_elementos = len(elementos)`);
- ausência de limite global de dashboards (H-0027:419-423);
- diagnóstico determinístico com contexto estrutural suficiente
  (H-0027:406-416, 577-603).

Constantes reutilizáveis confirmadas existentes no loader atual:
`ARRANJOS_CORPO_VALIDOS = {None, "vertical", "horizontal", "sobreposto",
"lado_a_lado"}` (`loader.py:37`), `MODOS_DISTRIBUICAO_CORPO_VALIDOS = {"igual",
"percentual", "fracao"}` (`loader.py:42`), `TIPOS_CORPO_VALIDOS = {"console",
"lancador", "dashboard"}` (`loader.py:25`). A função `_validar_distribuicao_corpo`
existe (`loader.py:148`).

Política de diagnóstico para nível 4 (H-0027:406-416, 577-584): o handoff
estabelece requisitos determinísticos (mesma entrada → mesma mensagem; incluir
`id` do grupo ofensor; incluir caminho completo; indicar máximo de 3 níveis),
mas **não fixa o texto exato** — explicitamente "O texto exato é decisão de
implementação, respeitando os requisitos acima" (H-0027:415). Isso está em
conformidade com ADR-0019 D4, que diz "A forma exata do erro é decisão de
implementação futura" (`ADR-0019:170-171`). Logo, o handoff **não inventa
política de diagnóstico sem autoridade** — apenas define requisitos observáveis
para uma decisão de implementação que a ADR defere explicitamente. Não há
bloqueio documental neste ponto.

### 6.5 Modelo (verificação 5)

O handoff define (seção 14):

- construção recursiva da árvore (H-0027:431-446);
- preservação de todos os filhos (H-0027:435-438);
- preservação da ordem (implícita na preservação integral da árvore; ordem é
  necessária para desempate de maiores restos, preservada em H-0027:308);
- ausência de achatamento (H-0027:308 "sub-árvore recursiva");
- suporte aos tipos funcionais existentes (H-0027:435-436);
- limite de três níveis de grupos (garantido pelo loader; modelo preserva o que
  o loader aceita — H-0027:431).

`_campos_inertes` preserva `arranjo`, `distribuicao` e demais campos do dict
do grupo (H-0027:441-443); confirmado que `_campos_inertes` existe como campo
da dataclass `ElementoCorpo` (`modelo.py:53`).

Métodos públicos `elemento_por_id` e `elementos_por_tipo`: o handoff opta por
mantê-los planos (H-0027:448-458). Ver análise detalhada no achado ACH-001
(seção 7.1).

### 6.6 Renderizador (verificação 6)

O handoff exige (seção 15), com critérios observáveis (não apenas expressões
genéricas):

- composição recursiva por container com pseudo-código `_renderizar_container`
  (H-0027:475-487);
- grupos verticais e horizontais (H-0027:512-533);
- combinações vertical/horizontal entre níveis (H-0027:536-539);
- distribuição independente em cada container (H-0027:515-533);
- distribuição somente entre filhos diretos (H-0027:542-546);
- ausência de distribuição preservada (H-0027:548-553);
- modos `igual`, `percentual` e `fracao` (H-0027:515-529);
- maiores restos e desempate por ordem declarada (preservados das ADR-0015
  decisões 7-8, citados em H-0027:164-166);
- propagação correta de largura e altura (H-0027:482-486, 498-500, 521-522);
- múltiplos grupos irmãos (H-0027:304, 719-720);
- múltiplos funcionais (H-0027:303, 706);
- múltiplos dashboards (H-0027:555-559, 721-722);
- grupo sem moldura, título ou conteúdo funcional próprio (H-0027:313,
  487-489).

A descrição do estado divergente atual (H-0027:208-216) foi confirmada pela
inspeção do `renderizador.py`: o ramo vertical itera `elemento.elementos` apenas
1 nível (`renderizador.py:1107-1117` e `1083-1094`), o modo horizontal gera slot
vazio para grupo (`renderizador.py:808-809, 846-856`), e não há aplicação de
`grupo.arranjo`/`grupo.distribuicao` nem composição recursiva por container.
A função `_montar_corpo_horizontal` existe (`renderizador.py:791`). Tudo fiel.

### 6.7 Arquivos permitidos (verificação 7)

Auditoria da lista informada (H-0027:8 e H-0027:256-274):

- `tela/loader.py` — necessário: contém `_validar_grupo` a ser substituída por
  validação recursiva.
- `tela/modelo.py` — necessário: contém `_construir_elementos_internos_grupo`
  não recursiva a ser substituída.
- `tela/renderizador.py` — necessário: não possui composição recursiva por
  container.
- `tela/teste_loader.py` — necessário: contém os quatro testes históricos a
  substituir e receberá nova cobertura.
- `tela/teste_modelo.py` — necessário: receberá cobertura de árvore recursiva
  e `_campos_inertes`.
- `tela/teste_renderizador.py` — necessário: receberá cobertura de composição
  recursiva, arranjos combinados e distribuição em grupos.
- `tela/teste_demo.py` — **observação**: sua cobertura atual não é diretamente
  afetada pela hierarquia de grupos (opera sobre os quatro JSONs ativos, todos
  planos ou de um nível; confirmado por inspeção — `teste_demo.py` não contém
  referências a "hierarquia", "aninhad", "profundidade" ou "recursi"). Sua
  inclusão na lista é justificável como suíte de regressão da demo TUI
  (H-0027:644 critério 4 exige código de saída 0; H-0027:362 exige preservação
  das suítes anteriores), mas o handoff **não justifica explicitamente** por
  que precisaria ser alterado. Ver observação OBS-002 (seção 7.3).
- `docs/relatorios/IMP-0028-...md` — corretamente permitido como relatório de
  implementação esperado.
- `config/telas/` — limitado a novas fixtures, com nomes descritivos, sem
  alterar os quatro JSONs existentes, e cada fixture nova deve ser listada no
  relatório de implementação (H-0027:271-274).

Os quatro critérios da verificação 7 do roteiro são atendidos:

- proibição explícita dos JSONs ativos: sim (H-0027:288-291, seção 9; e
  H-0027:272-273, seção 8);
- limitação de nova fixture a arquivo novo, individualmente registrável: sim
  (H-0027:271-273);
- exigência de informar cada fixture criada: sim (H-0027:273-274 "Cada fixture
  criada deve ser listada no relatório de implementação"; H-0027:763 item 3
  "arquivos alterados"; H-0027:766 item 9 "testes adicionados");
- impedimento de alteração de JSON real por conveniência de teste: sim
  (H-0027:272-273 "sem alterar os quatro JSONs existentes"; H-0027:335 escopo
  negativo).

A permissão de `config/telas/` é suficientemente limitada e auditável. Não há
contradição entre essa permissão e a lista de JSONs proibidos (seção 9), porque
a permissão é restrita a arquivos novos e a proibição é explícita sobre os
quatro existentes.

### 6.8 Arquivos proibidos (verificação 8)

A proibição é efetiva (H-0027:278-292):

- ADRs: `docs/adr/` (qualquer arquivo) — sim;
- contratos: `docs/contratos/` (qualquer arquivo) — sim;
- nomenclatura: `docs/NOMENCLATURA.md` — sim;
- índice: coberto por `docs/adr/` (INDICE_ADR está em `docs/adr/`) — sim;
- handoffs: `docs/handoff/` (qualquer arquivo, incluindo este) — sim;
- relatórios históricos: `docs/relatorios/` exceto IMP-0028 — sim;
- configurações reais: os quatro JSONs ativos — sim;
- arquivos fora da capacidade: implícito pela lista exaustiva de permitidos;
- commit e push: H-0027:339, 798-804.

Observa-se que o escopo negativo (H-0027:320-339) reforça "Alteração das
configurações `config/telas/*.json` existentes" (H-0027:335), coerente com a
proibição específica da seção 9. Não há contradição entre a permissão ampla de
`config/telas/` (somente para arquivos novos) e a lista de JSONs proibidos
(arquivos existentes): o handoff distingue explicitamente "criar arquivos ...
sem alterar os quatro JSONs existentes" (H-0027:271-273).

### 6.9 Escopo positivo e negativo (verificação 9)

Escopo positivo (H-0027:296-316) cobre toda a capacidade aprovada (D1–D7,
validação recursiva, construção recursiva, composição recursiva, distribuição
em grupos, múltiplos dashboards, testes, IMP-0028).

Escopo negativo (H-0027:320-339) exclui:

- nível de grupo 4: "Quarta camada de grupos ou profundidade ilimitada" (H-0027:324);
- profundidade ilimitada: idem;
- novos tipos: "Novos tipos funcionais além de `console`, `lancador`, `dashboard`" (H-0027:325);
- novos campos JSON: "Novos campos JSON além dos já definidos nos contratos" (H-0027:326);
- novos modos de distribuição: "Novos modos de distribuição além de `igual`, `percentual`, `fracao`" (H-0027:327);
- mudança de arredondamento: "Alteração do algoritmo de maiores restos ou de desempate por ordem" (H-0027:328);
- nova política de overflow: "Nova política de overflow ou de conteúdo maior que a cota" (H-0027:329);
- mudança de navegabilidade: "Mudança de navegabilidade de qualquer tipo" (H-0027:331);
- alteração de `[✥]`: "Alteração de `[✥]`, `[⏎]`, `[␣]` ou outros chips" (H-0027:332);
- bindings: "Alteração de bindings" (H-0027:333);
- ADR-0018: "Correção da divergência de status da ADR-0018 (pendência documental separada)" (H-0027:334);
- correções documentais: "Aplicação documental adicional em ADRs, contratos ou nomenclatura" (H-0027:336);
- commit: "Commit ou push" (H-0027:339).

Todos os itens exigidos pelo roteiro estão presentes.

### 6.10 Preservações (verificação 10)

A seção 12 (H-0027:343-362) estabelece critérios explícitos para preservar:

- composições planas (`orquestrador`, `destino_minimo`, `stub_b`) — H-0027:348;
- composição com um nível de grupo (`grupo_minimo`) — H-0027:349;
- distribuições vertical e horizontal do corpo raiz (`igual`, `percentual`,
  `fracao`) — H-0027:351;
- ausência de distribuição — H-0027:352;
- ordem declarada — H-0027:353;
- maiores restos — H-0027:354;
- `console`, `lancador`, `dashboard` — H-0027:355;
- passividade de dashboard — H-0027:357;
- navegação (`[✥]` restrito a `console`) — H-0027:358;
- JSONs existentes — H-0027:348-349 e indiretamente H-0027:335;
- ocupação vertical (ADR-0013, ADR-0017) — H-0027:359;
- redimensionamento reativo — H-0027:360;
- diagnósticos não relacionados — H-0027:361;
- suítes anteriores — H-0027:362.

Todos os itens exigidos pelo roteiro estão presentes.

### 6.11 Critérios de aceite (verificação 11)

A seção 19 (H-0027:637-652) permite verificação objetiva:

- aceitação de níveis 1–3: via cobertura da seção 18 + suítes em código 0;
- rejeição do nível 4: critério explícito em H-0027:8 (item 4 dos testes
  substituídos) e H-0027:679;
- árvore preservada: H-0027:696-698;
- renderização recursiva: H-0027:707-713;
- multiplicidade estrutural e funcional: H-0027:706, 719-720;
- arranjos combinados: H-0027:711-713;
- distribuição em grupos: H-0027:714-717;
- múltiplos dashboards: H-0027:721-722;
- preservações: H-0027:647-648 (suítes não regridem) + seção 12;
- estado Git: H-0027:645, 652;
- arquivos alterados: H-0027:763 (item do IMP-0028);
- relatório de implementação: H-0027:651.

Os critérios são observáveis e não circulares. Nenhum se limita a repetir
"implementar conforme ADR". Os comandos são concretos (`python tela/teste_*.py`
com código 0; `git diff --check`; `git diff --cached --stat`). Há exigência
explícita de não fixar contagens absolutas (H-0027:743).

### 6.12 Testes (verificação 12)

A seção 20 (H-0027:656-726) cobre todos os itens exigidos pelo roteiro:

- zero, um, dois e três níveis de grupos: H-0027:673-678;
- nível 4 inválido: H-0027:679;
- múltiplos grupos irmãos: H-0027:680-681;
- múltiplos funcionais: H-0027:675;
- mistura de grupo e funcional: H-0027:682;
- grupos verticais e horizontais: H-0027:683-684;
- combinações de arranjo: H-0027:711-713;
- ausência de distribuição: H-0027:714;
- `igual`, `percentual` e `fracao` em grupos: H-0027:715-717;
- vetores inválidos: H-0027:689-690;
- associação aos filhos diretos: H-0027:718;
- múltiplos dashboards: H-0027:721-722;
- regressão das distribuições do corpo raiz: H-0027:724;
- regressão de JSONs existentes: H-0027:726;
- diagnósticos determinísticos: H-0027:692.

Testes históricos incompatíveis serão **substituídos ou reescritos**, não
removidos (H-0027:658-669 — seção 20.1 intitulada "Testes a substituir (não
remover)"; critério de aceite H-0027:649-650 reforça "substituídos por testes
coerentes com as regras vigentes (não simplesmente removidos)").

Comandos mínimos esperados (H-0027:734-740):

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
git diff --check
```

Presentes e na ordem esperada. O handoff não exige contagens históricas fixas
(H-0027:743 "Não fixar contagens absolutas de testes").

### 6.13 Relatório de implementação (verificação 13)

O handoff exige a criação de
`docs/relatorios/IMP-0028-composicao-hierarquica-tres-niveis-grupos.md`
(H-0027:748-753). O conteúdo obrigatório (H-0027:756-776) inclui:

- arquivos alterados (item 3);
- implementação por camada (item 4);
- profundidade (item 5);
- multiplicidade (item 7);
- dashboards (item 8);
- testes novos e alterados (itens 9, 10);
- comandos e resultados (itens 11, 12);
- preservações (item 13);
- limitações (item 14);
- Git (item 15);
- bloqueios (item 16).

Todos os itens exigidos pelo roteiro estão cobertos.

### 6.14 Condições de bloqueio (verificação 14)

A seção 23 (H-0027:780-794) exige parada quando:

- faltar regra: "Uma regra necessária não estiver definida nas autoridades" →
  `ARCHITECTURE_REVIEW_REQUIRED` (H-0027:785-786);
- houver contradição documental: "Houver contradição entre ADR-0019 e um
  contrato que não esteja explicada" → `ARCHITECTURE_REVIEW_REQUIRED`
  (H-0027:787-788);
- for necessária decisão pública sobre API: coberta por
  `ARCHITECTURE_REVIEW_REQUIRED` nos três gatilhos;
- arquivo necessário estiver proibido: "A implementação não couber nos
  arquivos permitidos da seção 8" → `BLOCKED_SCOPE` (H-0027:790-792);
- a capacidade exigir documento adicional: implícito em
  `ARCHITECTURE_REVIEW_REQUIRED` (regra ausente ou contradição);
- for necessária arquitetura não definida: `ARCHITECTURE_REVIEW_REQUIRED`.

Há também `BLOCKED_REPOSITORY_STATE` para divergência de estado Git
(H-0027:784). O handoff não instrui o executor a preencher lacunas: a seção 23
usa consistentemente "parar" e remeter a `ARCHITECTURE_REVIEW_REQUIRED` ou
`BLOCKED_SCOPE`, e a seção 25 (H-0027:808-818) reafirma os limites de
encerramento.

### 6.15 Ausência de implementação antecipada (verificação 15)

Confirmado que o handoff:

- não altera código (somente arquivos `tela/*.py` rastreados estão sem diff,
  conforme `git status` inicial);
- não cria fixture (nenhum arquivo novo em `config/telas/`); os quatro JSONs
  ativos permanecem inalterados;
- não cria IMP-0028 (não consta em `git status`);
- não executa implementação;
- não aprova a si próprio (status `proposto` — H-0027:54);
- não prepara commit (H-0027:798-804 proíbe commit; `git diff --cached --stat`
  vazio confirma stage vazio).

O único arquivo criado é o próprio handoff
(`docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md`), não
rastreado, conforme informado pelo autor e confirmado por `git status`.

---

## 7. Achados

### 7.1 ACH-001 — Justificativa factual inexata sobre `elemento_por_id`/`elementos_por_tipo`

```text
ID: ACH-001
severidade: média
categoria: DEFEITO_DO_HANDOFF_COM_REGRA_A_ESCLARECER
descrição: A seção 14.2 do handoff justifica a manutenção de elemento_por_id e
  elementos_por_tipo como planos (busca somente em self.corpo.elementos diretos)
  afirmando: "sua documentação diz explicitamente que operam sobre
  self.corpo.elementos" (H-0027:454-455). Essa afirmação é inexata. As docstrings
  atuais dos métodos (tela/modelo.py:90-106) não explicitam o escopo da busca:
  elemento_por_id diz apenas "Retorna o primeiro ElementoCorpo com o id
  informado, ou None" e elementos_por_tipo diz apenas "Retorna lista de
  ElementoCorpo cujo `tipo` coincide". Nenhuma das duas docstrings afirma operar
  sobre self.corpo.elementos diretos (muito menos exclui descendentes de
  grupos). A implementação atual percorre self.corpo.elementos, mas a
  documentação (docstring) é omissa quanto ao escopo.
autoridade ou requisito afetado: roteiro de QA seção 5 ("Se o handoff escolher
  unilateralmente entre busca apenas no nível raiz e busca recursiva sem
  autoridade ou evidência suficiente, classifique adequadamente como decisão
  arquitetural ausente"); ausência de definição contratual — confirma-se por rg
  que nenhum arquivo de docs/contratos/ menciona elemento_por_id ou
  elementos_por_tipo; H-0002-modelo-interno-tela.md:167-170 apenas autorizou os
  métodos como "métodos auxiliares somente leitura", sem definir semântica de
  busca (raiz vs recursiva).
arquivo e linha: docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md:448-458
impacto: A decisão de manter os métodos planos é tecnicamente razoável (o
  renderizador não os usa — confirmado por inspeção de renderizador.py; os
  testes atuais CA-18/CA-19 do H-0012 só verificam grupo de nível 1, que está
  em corpo.elementos diretos) e está registrada como "limitação documentada, não
  bug" (H-0027:701, 771). Porém, como após este ciclo haverá elementos
  funcionais dentro de grupos em níveis 1-3, esses elementos não serão
  encontráveis por elemento_por_id nem por elementos_por_tipo. A justificativa
  atual do handoff apóia-se em uma premissa factual falsa ("documentação diz
  explicitamente"), o que enfraquece a bases da decisão. Um futuro executor ou
  revisor poderia entender (incorretamente) que existe autoridade contratual
  para a limitação, quando na verdade a decisão é arquitetural tácita do
  handoff.
correção necessária: corrigir a justificativa da seção 14.2 para não afirmar que
  a documentação atual "diz explicitamente" o escopo. Alternativas coerentes:
  (a) registrar explicitamente que a manutenção do escopo plano é decisão
  arquitetural deste ciclo (com base na evidência de uso — renderizador não os
  utiliza e contratos não os definem), deixando a semântica recursiva como
  pendência explícita para ciclo futuro; ou (b) exigir que o executor atualize
  as docstrings de elemento_por_id e elementos_por_tipo no modelo para declarar
  explicitamente o escopo plano (somente corpo.elementos diretos), tornando
  verdadeira a afirmação. A opção (b) é compatível com o escopo permitido
  (tela/modelo.py está na lista da seção 8) e com H-0002 (métodos auxiliares
  somente leitura).
nova decisão do usuário necessária: não. A decisão entre manter plano ou tornar
  recursivo é arquitetural e pode ser resolvida no patch do handoff com base em
  evidência existente (contratos omissos + uso consolidado pelo renderizador).
```

Classificação: **defeito do handoff com regra a esclarecer** — a decisão é
corrigível no próprio handoff com base em autoridades já existentes (H-0002 e
ausência de definição contratual), sem exigir nova decisão do usuário nem nova
ADR.

### 7.2 OBS-001 — Divergência de status da ADR-0018 (pendência documental conhecida)

```text
ID: OBS-001
severidade: observação
categoria: PENDENCIA_DOCUMENTAL_CONHECIDA
descrição: O frontmatter e o corpo de ADR-0018 declaram status: proposta
  (docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md:6 e
  :26), enquanto docs/adr/INDICE_ADR.md:48 lista a ADR-0018 como aceita. Essa
  divergência é pendência documental conhecida (registrada em ADR-0019:471-477,
  RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md:74-75 e em
  RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md:156-164 como OBS-001). O handoff
  H-0027 trata a divergência corretamente: inclui "Correção da divergência de
  status da ADR-0018 (pendência documental separada)" no escopo negativo
  (H-0027:334) e preserva a ADR-0018 como autoridade para a semântica de
  ausência de distribuição (H-0027:167-170, 548-553), sem tentar corrigi-la nem
  reinterpretá-la.
autoridade ou requisito afetado: nenhum — o handoff está alinhado com a
  orientação normativa (a divergência é separada e não bloqueia este ciclo).
arquivo e linha: docs/adr/ADR-0018-...:6, :26; docs/adr/INDICE_ADR.md:48;
  docs/handoff/H-0027-...:334
impacto: nenhum impacto no ciclo H-0027.
correção necessária: nenhuma nesta etapa.
nova decisão do usuário necessária: não.
```

### 7.3 OBS-002 — `tela/teste_demo.py` na lista de permitidos sem justificativa explícita

```text
ID: OBS-002
severidade: observação
categoria: PERMISSAO_DE_ARQUIVO_NAO_JUSTIFICADA
descrição: A seção 8 do handoff inclui tela/teste_demo.py na lista de arquivos
  permitidos para alteração (H-0027:267), mas não justifica explicitamente por
  que esse arquivo precisaria ser alterado. Pela inspeção do arquivo atual, sua
  cobertura não é diretamente afetada pela hierarquia de grupos: ele opera sobre
  os quatro JSONs ativos (orquestrador, destino_minimo, grupo_minimo, stub_b),
  todos planos ou de um nível; não contém referências a "hierarquia",
  "aninhad", "profundidade" ou "recursi"; e a demo carrega modelos via
  _carregar_modelo_por_id e os renderiza via renderizar_estado, caminhos que
  hoje não exercitam (nem poderiam exercitar) hierarquias mais profundas. A
  inclusão é justificável como suíte de regressão da demo TUI (H-0027:644
  critério 4 exige código de saída 0; H-0027:362 exige preservação das suítes
  anteriores), mas o handoff não torna essa justificativa explícita, deixando
  aberta a interpretação de que o executor precise alterar teste_demo.py para
  cumprir o ciclo.
autoridade ou requisito afetado: roteiro de QA seção 7 ("se
  tela/teste_demo.py possui cobertura afetada que justifique permissão").
arquivo e linha: docs/handoff/H-0027-...:267
impacto: baixo. O executor provavelmente manterá teste_demo.py sem alterações
  (ou apenas semânticas), dado que os JSONs ativos não mudam. O risco é pequeno:
  a permissão é aberta sem necessidade demonstrada, mas não autoriza alteração
  indevida — o escopo negativo (H-0027:325-339) e os critérios de aceite
  (H-0027:644) limitam o que pode ser feito.
correção necessária: desejável, mas não bloqueante — esclarecer na seção 8 que
  teste_demo.py está listado para garantir verificação de regressão da demo TUI
  (suíte que deve permanecer em código 0), não porque se espera alteração
  substantiva da cobertura.
nova decisão do usuário necessária: não.
```

### 7.4 OBS-003 — Políticas de diagnóstico declaradas como decisão de implementação (conforme)

```text
ID: OBS-003
severidade: observação
categoria: CONFORMIDADE_COM_AUTORIDADE
descrição: O roteiro de QA seção 4 pede para "classificar como bloqueio
  documental qualquer política necessária de diagnóstico que o handoff tenha
  inventado sem autoridade". O handoff H-0027 estabelece, para o diagnóstico de
  grupo no nível 4 (seções 13.4 e 17.1), requisitos observáveis: mensagem
  determinística, incluir id do grupo ofensor, incluir caminho completo,
  indicar máximo de 3 níveis. Esses requisitos são coerentes com ADR-0019 D4,
  que defere explicitamente "A forma exata do erro é decisão de implementação
  futura" (ADR-0019:170-171), e com contrato_composicao_corpo.md R-22, que
  exige "erro determinístico com mensagem descritiva". O handoff não fixa o
  texto exato da mensagem ("O texto exato é decisão de implementação",
  H-0027:415). Portanto, o handoff não inventa política sem autoridade — apenas
  torna observáveis os requisitos que a ADR e o contrato já estabelecem.
autoridade ou requisito afetado: nenhum (conformidade).
arquivo e linha: docs/handoff/H-0027-...:406-416, 577-584
impacto: nenhum.
correção necessária: nenhuma.
nova decisão do usuário necessária: não.
```

---

## 8. Coerência interna

### 8.1 Contradições entre seções

Não foram identificadas contradições internas relevantes. Pontos de tensão
verificados:

- **Permissão `config/telas/` × proibição dos 4 JSONs**: não há contradição. A
  seção 8 restringe a permissão a arquivos novos ("sem alterar os quatro JSONs
  existentes", H-0027:272-273); a seção 9 proíbe explicitamente os quatro
  existentes (H-0027:288-291); o escopo negativo reforça (H-0027:335).
- **Manter `elemento_por_id`/`elementos_por_tipo` planos × construção recursiva
  do modelo**: não é contradição lógica — o modelo preserva a árvore
  integralmente em `ElementoCorpo.elementos` (H-0027:308, 460-465); apenas os
  dois métodos auxiliares de busca permanecem planos, como limitação
  documentada (H-0027:701, 771). A única imprecisão é a justificativa factual
  (ACH-001).
- **`grupo.arranjo` incluindo `sobreposto` e `lado_a_lado` (aliases
  transicionais)**: coerente com ADR-0011 e com a constante
  `ARRANJOS_CORPO_VALIDOS` atual do loader (`loader.py:37`). Não há reintrodução
  de terminologia nova.
- **Seção 6.4 (testes a substituir) × seção 20.1**: coerentes. Ambas descrevem
  os mesmos quatro testes e exigem substituição, não remoção.

### 8.2 Coerência com autoridades

- **ADR-0019 (D1–D7)**: todas as decisões cobertas fielmente (seção 5 desta
  auditoria).
- **ADR-0015**: preservada nos pontos vigentes (arranjo por container,
  distribuição por container, maiores restos, ordem declarada, preenchimento de
  área alocada). O handoff não a reescreve nem cancela (H-0027:164-166).
- **ADR-0018**: preservada; a divergência de status é tratada como pendência
  separada (H-0027:334).
- **ADR-0010**: taxonomia funcional preservada; `dashboard` passivo e não
  navegável por `[✥]` (H-0027:355-358).
- **ADR-0007**: não contradita; o handoff cita ADR-0007 como contexto (H-0027
  metadados `escopo_somente_leitura`, linha 34).
- **Contratos**: o handoff não reescreve nem contraria os três contratos; cita
  seções específicas como autoridades (H-0027:118-128).
- **NOMENCLATURA**: não alterada (escopo negativo H-0027:285).

---

## 9. Fidelidade do diagnóstico do estado atual

A seção 6 do handoff (H-0027:185-230) descreve o estado divergente atual do
loader, modelo, renderizador e testes. A inspeção direta confirmou todos os
pontos:

- `loader.py:243-251` rejeita `grupo.arranjo` horizontal/lado_a_lado — confirmado;
- `loader.py:269-273` rejeita `len(sub) > 1` — confirmado;
- `loader.py:302-306` rejeita `tipo_item == "grupo"` — confirmado;
- ausência de validação recursiva de profundidade — confirmado;
- ausência de validação de `grupo.distribuicao` — confirmado;
- `modelo.py:127-133` `_construir_elementos_internos_grupo` não recursivo —
  confirmado;
- `modelo.py:127` docstring "Não há recursão: grupo dentro de grupo é rejeitado
  pelo loader" — confirmado;
- `modelo.py:90-106` `elemento_por_id`/`elementos_por_tipo` planos — confirmado;
- `renderizador.py:1107-1117` e `1083-1094` iteram apenas 1 nível — confirmado;
- `renderizador.py:808-809, 846-856` grupo vira slot vazio em modo horizontal —
  confirmado;
- ausência de aplicação de `grupo.arranjo`/`grupo.distribuicao` no renderizador
  — confirmado;
- ausência de composição recursiva por container — confirmado;
- os quatro testes históricos em `teste_loader.py:645-682` — confirmados.

A descrição do estado atual é fiel. Não há uso de implementação ou teste
divergente para redefinir autoridades.

---

## 10. Ausência de implementação antecipada

Conforme verificação 15 (seção 6.15), o handoff:

- não altera código (`git status` não mostra diff em `tela/*.py`);
- não cria fixture (`config/telas/` permanece com exatamente os quatro JSONs
  existentes);
- não cria IMP-0028 (ausente em `git status`);
- não aprova a si próprio (status `proposto`);
- não prepara commit (stage vazio, H-0027:798-804 proíbe commit).

O único artefato criado é o próprio handoff (não rastreado).

---

## 11. Classificação final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: o handoff H-0027 é majoritariamente completo, coerente,
verificável e implementável sem decisões adicionais do usuário. A matriz
obrigatória é integralmente SUFICIENTE. As decisões D1–D7 estão fiéis. A
coesão entre camadas está assegurada. Os arquivos permitidos, proibidos,
preservações, critérios de aceite, testes, relatório IMP-0028 e bloqueios estão
cobertos. O estado Git descrito é fiel.

Há, todavia, um **achado de severidade média (ACH-001)** que configura defeito
do handoff corrigível com base em autoridades já existentes: a justificativa
factual da seção 14.2 sobre `elemento_por_id`/`elementos_por_tipo` apóia-se em
premissa inexata ("sua documentação diz explicitamente que operam sobre
`self.corpo.elementos`"), quando as docstrings atuais não explicitam o escopo e
nenhum contrato define a semântica de busca. A decisão em si (manter planos) é
razoável e está registrada como limitação documentada, mas a justificativa
precisa ser corrigida no próprio handoff (seção 14.2) ou complementada com a
exigência de atualização das docstrings pelo executor (compatível com o escopo
permitido de `tela/modelo.py`).

Não foram identificados achados bloqueantes. Não há contradição normativa
interna nem entre o handoff e as autoridades. Não há regra faltante que exija
nova ADR ou nova decisão do usuário: a correção de ACH-001 resolve-se dentro do
próprio handoff, usando H-0002 e a ausência de definição contratual como base.

As observações OBS-001 (divergência de status da ADR-0018, pendência conhecida
tratada corretamente), OBS-002 (permissão de `teste_demo.py` sem justificativa
explícita) e OBS-003 (política de diagnóstico conforme ADR-0019 D4) não exigem
correção antes da implementação.

---

## 12. Próxima categoria processual (sem executá-la)

Aplicado o patch ao handoff H-0027 para corrigir o ACH-001, a próxima categoria
processual permitida é a reauditoria do handoff (`QA_HANDOFF`) para confirmar a
resolução do achado. Após aprovação, o ciclo prossegue para implementação
(`IMPLE` / executor) conforme as seções 13–22 do handoff, com produção do
relatório `IMP-0028`.

Esta categoria não foi executada nesta auditoria.

---

## 13. Estado Git final

```text
git log -1 --oneline
40015b6 feat: implementa distribuicao horizontal percentual e fracionaria

git status --short
 M docs/NOMENCLATURA.md
 M docs/adr/ADR-0007-tela-processamento-composicao.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md
?? docs/handoff/H-0027-composicao-hierarquica-tres-niveis-grupos.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0019.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_HIERARQUICA_TRES_NIVEIS.md
?? docs/relatorios/RELATORIO_QA_ADR-0019.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0019_REEXECUCAO.md
?? docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0019.md
?? tela/__pycache__/

git diff --stat
 scripts/docs/NOMENCLATURA.md                       | 27 +++++++++------
 .../adr/ADR-0007-tela-processamento-composicao.md  | 15 ++++++--
 scripts/docs/adr/INDICE_ADR.md                     |  1 +
 .../docs/contratos/contrato_composicao_corpo.md    | 40 ++++++++++++++--------
 .../docs/contratos/contrato_json_tela_minima.md    |  7 +++-
 scripts/docs/contratos/contrato_tela_json.md       | 15 +++++---
 6 files changed, 72 insertions(+), 33 deletions(-)

git diff --check
(sem saída)

git diff --cached --stat
(sem saída)

git diff --cached --name-only
(sem saída)
```

O único novo arquivo criado nesta auditoria é
`docs/relatorios/RELATORIO_QA_H-0027_HANDOFF.md` (este relatório). Nenhum
arquivo rastreado foi alterado. O handoff H-0027, a ADR-0019, os relatórios do
ciclo e `tela/__pycache__/` permanecem não rastreados, sem alteração, remoção,
movimentação ou stage. Stage permanece vazio ao final.
