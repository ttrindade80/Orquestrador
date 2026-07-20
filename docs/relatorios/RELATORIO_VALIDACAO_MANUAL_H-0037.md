---
status_literal: MANUAL_VALIDATION_FAILED
status_normalizado: VALIDACAO_MANUAL_REPROVADA_PATCH_NECESSARIO
historia: H-0037
tipo: VALIDACAO_MANUAL_TTY
data: "2026-07-20"
implementacao_aprovada_manualmente: false
proxima_categoria: PATCH_IMPLEMENTACAO
---

# RELATORIO DE VALIDACAO MANUAL H-0037

## 1. Identificacao

| Campo | Valor |
|---|---|
| Handoff | H-0037 |
| Titulo | Apresentacao multinivel no console com politica de modo por tela (D23) |
| Tipo de relatorio | VALIDACAO_MANUAL_TTY |
| Data da validacao | 2026-07-20 |
| Executado por | Usuario (TTY real) |
| Registrado por | Registrador documental |
| Branch | master |
| HEAD | f6982d08640af1762b8e0e8814b6e90c9421538e |
| Arquivo | `docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0037.md` |

---

## 2. Objetivo

Registrar documentalmente o resultado da validacao manual executada pelo usuario
em terminal real (TTY real) para o H-0037, conforme obrigatoriedade estabelecida
em ADR-0028 §38 e roteiro do `H-0037-apresentacao-multinivel-console-alternancia-verbosa.md`
secao 24.

---

## 3. Ambiente

```yaml
ambiente:
  terminal_real: APROVADO
  raiz_correta: APROVADO
```

A validacao foi executada em terminal real (TTY), na raiz correta do projeto.

---

## 4. Autoridades

Documentos lidos como base normativa deste registro:

```text
docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
docs/relatorios/RELATORIO_QA_POS_PATCH_6_H-0037_IMPLEMENTACAO.md
docs/contratos/contrato_console.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_json_console.md
```

Evidencia principal: resultado humano fornecido diretamente pelo usuario.

---

## 5. Metodo

O usuario executou o roteiro de validacao manual descrito no handoff H-0037
secao 24, utilizando os quatro comandos de entrada diretos por cenario:

```bash
python demo/demo.py h0037_console_nao_verboso
python demo/demo.py h0037_console_verboso_dois_niveis
python demo/demo.py h0037_console_alternavel_tres_niveis
python demo/demo.py h0037_console_tabela_alternavel
```

O resultado foi fornecido pelo usuario e registrado abaixo sem transformacoes,
aplicando somente as normalizacoes canonicas:

```yaml
SIM: APROVADO
CORRETO: APROVADO
FUNCIONAMENTO_CORRETO: APROVADO
NAO_EXISTE_FORA_DO_ESCOPO: NAO_APLICAVEL
```

Itens reprovados pelo usuario sao registrados como reprovados. Nao ha
transformacao de reprovado em observacao.

---

## 6. Cenario 1 — somente nao verboso

**Tela:** `h0037_console_nao_verboso`
**Politica:** `somente_nao_verboso`
**Modo inicial:** fixo (nao alternavel)

```yaml
cenario_1_nao_verboso:
  tela_correta: APROVADO
  modo_inicial: APROVADO
  truncamento: APROVADO
  marcador_de_reticencias: REPROVADO
  chip_V_ausente: APROVADO
  tecla_V_maiuscula_inerte: APROVADO
  redimensionamento: APROVADO
```

**Resumo do cenario 1:**
- 6 itens aprovados, 1 item reprovado.
- Reprovacao: `marcador_de_reticencias` — conteudo truncado sem exibicao do marcador `...`.

---

## 7. Cenario 2 — somente verboso em dois niveis

**Tela:** `h0037_console_verboso_dois_niveis`
**Politica:** `somente_verboso`
**Modo inicial:** fixo (nao alternavel)

```yaml
cenario_2_verboso_dois_niveis:
  tela_correta: APROVADO
  modo_inicial: APROVADO
  mesmos_dados_do_cenario_1: APROVADO
  multiplas_linhas: APROVADO
  alinhamento_do_segundo_nivel: APROVADO
  chip_V_ausente: APROVADO
  tecla_V_maiuscula_inerte: APROVADO
  redimensionamento: APROVADO
```

**Resumo do cenario 2:**
- 8 itens aprovados, 0 itens reprovados.
- Conteudo compartilhado com o cenario 1 confirmado. Politica diferente produz
  resultado visual diferente com os mesmos dados — prova que a politica pertence
  a tela, nao ao documento externo.

---

## 8. Cenario 3 — alternavel em tres niveis

**Tela:** `h0037_console_alternavel_tres_niveis`
**Politica:** `alternavel`
**Modo inicial:** `nao_verboso`

```yaml
cenario_3_alternavel_tres_niveis:
  tela_correta: APROVADO
  modo_inicial_nao_verboso: APROVADO
  chip_V_presente: APROVADO
  chip_Esc_primeiro: REPROVADO
  alternancia_com_V_maiusculo: APROVADO
  alternancia_com_v_minusculo: REPROVADO
  reversibilidade: APROVADO_COM_V_MAIUSCULO
  tres_niveis_preservados: APROVADO
  redimensionamento_nos_dois_modos: APROVADO
```

**Resumo do cenario 3:**
- 7 itens aprovados (incluindo `reversibilidade: APROVADO_COM_V_MAIUSCULO`),
  2 itens reprovados.
- Reprovacao: `chip_Esc_primeiro` — chip Esc nao ocupa a primeira posicao na
  barra de menus.
- Reprovacao: `alternancia_com_v_minusculo` — a tecla `v` minuscula nao
  produz alternancia.

---

## 9. Cenario 4 — tabela alternavel

**Tela:** `h0037_console_tabela_alternavel`
**Politica:** `alternavel`
**Modo inicial:** `verboso`

```yaml
cenario_4_tabela_alternavel:
  tela_correta: APROVADO
  modo_inicial_verboso: APROVADO
  chip_V_presente: APROVADO
  chip_Esc_primeiro: REPROVADO
  cabecalho_preservado: APROVADO
  celulas_multilinha: APROVADO
  compactacao_com_V_maiusculo: APROVADO
  compactacao_com_v_minusculo: REPROVADO
  truncamento: APROVADO
  marcador_de_reticencias: REPROVADO
  retorno_ao_verboso_com_V_maiusculo: APROVADO
  retorno_ao_verboso_com_v_minusculo: REPROVADO
  redimensionamento_nos_dois_modos: APROVADO
```

**Resumo do cenario 4:**
- 9 itens aprovados, 4 itens reprovados.
- Reprovacao: `chip_Esc_primeiro` — chip Esc nao ocupa a primeira posicao.
- Reprovacao: `compactacao_com_v_minusculo` — tecla `v` minuscula nao compacta.
- Reprovacao: `marcador_de_reticencias` — conteudo truncado sem exibicao do
  marcador `...`.
- Reprovacao: `retorno_ao_verboso_com_v_minusculo` — tecla `v` minuscula nao
  restaura o modo verboso.

---

## 10. Comportamento do Terminal

```yaml
terminal:
  teclas_sem_eco: APROVADO
  cursor_oculto: APROVADO
  redesenho: APROVADO
  cintilacao: APROVADO
  retorno_ao_terminal_apos_sair: APROVADO
```

Todos os 5 itens de comportamento do terminal aprovados sem ressalvas.

---

## 11. Paginacao

```yaml
paginacao:
  resultado: NAO_APLICAVEL
  motivo: funcionalidade_nao_prevista_para_esta_rodada
  falha_da_implementacao: false
```

A paginacao foi incluida incorretamente no roteiro manual. A ausencia de
paginacao nao constitui reprovacao e nao gera achado de implementacao.
Nao ha falha da implementacao neste item.

---

## 12. Itens Aprovados

Os seguintes itens foram aprovados explicitamente na validacao:

- Identidade das quatro telas (todas as quatro telas reconhecidas corretamente);
- Modos iniciais de todos os cenarios (`nao_verboso` no cenario 3,
  `verboso` no cenario 4, fixos nos cenarios 1 e 2);
- Conteudo compartilhado entre os cenarios 1 e 2 (`mesmos_dados_do_cenario_1`);
- Multiplas linhas no modo verboso do cenario 2;
- Alinhamento do segundo nivel no cenario 2;
- Presenca correta do chip `[V] Verboso` nos cenarios 3 e 4;
- Ausencia correta do chip `[V] Verboso` nos cenarios 1 e 2;
- Alternancia reversivel com `V` maiusculo nos cenarios 3 e 4;
- Preservacao dos tres niveis no cenario 3 apos alternancia;
- Cabecalho da tabela preservado no cenario 4;
- Celulas multilinha no cenario 4 modo verboso;
- Truncamento presente nos cenarios 1 e 4 (conteudo cortado confirmado);
- Redimensionamento em todos os cenarios;
- Redesenho apos redimensionamento;
- Ausencia de eco de teclas;
- Cursor oculto;
- Ausencia de cintilacao problematica;
- Retorno correto ao terminal apos sair;
- Tecla `V` maiuscula inerte nos cenarios de politica fixa (1 e 2).

---

## 13. Itens Reprovados

Os seguintes itens foram reprovados pelo usuario na validacao em TTY real:

| Cenario | Item | Observado |
|---|---|---|
| Cenario 1 | `marcador_de_reticencias` | Conteudo truncado sem exibicao do marcador `...` |
| Cenario 3 | `chip_Esc_primeiro` | Chip Esc nao ocupa a primeira posicao na barra de menus |
| Cenario 3 | `alternancia_com_v_minusculo` | Tecla `v` minuscula nao produz alternancia |
| Cenario 4 | `chip_Esc_primeiro` | Chip Esc nao ocupa a primeira posicao na barra de menus |
| Cenario 4 | `compactacao_com_v_minusculo` | Tecla `v` minuscula nao compacta |
| Cenario 4 | `marcador_de_reticencias` | Conteudo truncado sem exibicao do marcador `...` |
| Cenario 4 | `retorno_ao_verboso_com_v_minusculo` | Tecla `v` minuscula nao restaura modo verboso |

Total: 7 itens reprovados em 4 cenarios distintos.

---

## 14. Achados Funcionais

### H0037-MANUAL-001 — Marcador de truncamento ausente

```yaml
id: H0037-MANUAL-001
titulo: Marcador de truncamento ausente
severidade: medio
tipo: DEFEITO_FUNCIONAL_VISUAL
cenarios:
  - h0037_console_nao_verboso
  - h0037_console_tabela_alternavel
observado: conteudo_truncado_sem_marcador
esperado: conteudo_truncado_com_marcador_...
reproduzido_em_TTY_real: true
autoridade:
  - contrato_json_console.md secao 13.5
  - H-0037 secao 13.1 comportamento_obrigatorio
```

O renderizador trunca o conteudo excedente no modo nao verboso mas nao exibe o
marcador `...` ao final da linha truncada. O truncamento em si foi confirmado
(`truncamento: APROVADO`); a ausencia e exclusiva do marcador visual.

---

### H0037-MANUAL-002 — Ordem dos chips

```yaml
id: H0037-MANUAL-002
titulo: Chip Esc nao ocupa a primeira posicao na barra de menus
severidade: medio
tipo: DEFEITO_FUNCIONAL_VISUAL
cenarios:
  - h0037_console_alternavel_tres_niveis
  - h0037_console_tabela_alternavel
observado: chip_Esc_nao_ocupa_a_primeira_posicao
esperado: chip_Esc_sempre_primeiro
autoridade:
  - decisao_explicita_do_usuario_na_validacao_manual
reproduzido_em_TTY_real: true
```

Nos cenarios 3 e 4, o chip Esc nao e exibido na primeira posicao da barra de
menus. A expectativa do usuario, expressa explicitamente na validacao manual, e
que o chip Esc ocupe sempre a primeira posicao.

---

### H0037-MANUAL-003 — Tecla minuscula nao reconhecida

```yaml
id: H0037-MANUAL-003
titulo: Tecla v minuscula nao reconhecida como alternancia
severidade: medio
tipo: DEFEITO_FUNCIONAL_DE_INTERACAO
cenarios:
  - h0037_console_alternavel_tres_niveis
  - h0037_console_tabela_alternavel
observado: somente_V_maiusculo_alterna
esperado:
  - V_maiusculo_alterna
  - v_minusculo_alterna
autoridade:
  - decisao_explicita_do_usuario_na_validacao_manual
reproduzido_em_TTY_real: true
```

Nos cenarios 3 e 4, somente a tecla `V` maiuscula produz alternancia de modo.
A tecla `v` minuscula nao e reconhecida. A expectativa do usuario, expressa
explicitamente na validacao manual, e que ambas as variantes (maiuscula e
minuscula) produzam alternancia.

---

## 15. Impacto

Os tres achados afetam:

- **H0037-MANUAL-001**: experiencia visual nos modos nao verbosos dos cenarios 1
  e 4. O usuario nao consegue identificar visualmente onde o conteudo foi
  truncado.
- **H0037-MANUAL-002**: organizacao da barra de menus nos cenarios alternáveis
  (3 e 4). A convencao esperada pelo usuario e que o chip de saida ocupe
  sempre a primeira posicao.
- **H0037-MANUAL-003**: interacao nos cenarios alternáveis (3 e 4). O usuario
  que pressiona `v` minuscula nao obtem resposta, comprometendo a usabilidade
  da alternancia.

Nenhum achado compromete a estrutura de dados, a política de modo declarada
no JSON estrutural, o carregamento do documento externo ou o comportamento
dos cenarios de politica fixa.

---

## 16. Conclusao

A validacao manual executada pelo usuario em terminal real identificou 7 itens
reprovados distribuidos em 3 achados funcionais distintos. A implementacao nao
esta aprovada manualmente. Um patch e necessario antes da aprovacao.

Os aspectos fundamentais da implementacao foram aprovados: identidade de telas,
modos iniciais, conteudo compartilhado, verbosidade multinivel, alternancia com
`V` maiusculo, preservacao de estrutura e dados, comportamento do terminal.

A implementacao necessita de correcao focal nos tres achados antes de nova
rodada de validacao manual.

---

## 17. Status Literal

```yaml
status_literal: MANUAL_VALIDATION_FAILED
```

---

## 18. Status Normalizado

```yaml
status_normalizado: VALIDACAO_MANUAL_REPROVADA_PATCH_NECESSARIO
```

---

## 19. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
implementacao_aprovada_manualmente: false
achados_bloqueantes: 3
achados:
  - H0037-MANUAL-001
  - H0037-MANUAL-002
  - H0037-MANUAL-003
```

---

## 20. Estado Git Observado

```yaml
git:
  branch: master
  head: f6982d08640af1762b8e0e8814b6e90c9421538e
  head_log: "f6982d0 docs: corrige whitespace do fechamento H-0036"
  stage: vazio
  diff_check: sem_erros
  commit_novo: nao_realizado
  push: nao_executado
```

Arquivos modificados rastreados (workspace sujo acumulado, nao commitado):

```text
config/telas/demo/demo.json
demo/demo.py
demo/teste_demo.py
demo/teste_demo_console.py
demo/teste_diagnostico.py
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/contratos/contrato_tela_json.md
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

Arquivos nao rastreados relevantes: fixtures H-0037, ADR-0028, handoff H-0037,
relatorios H-0037/ADR-0028, `demo/teste_demo_console_modos.py` e este relatorio
de validacao manual.

(Fim do relatorio)
