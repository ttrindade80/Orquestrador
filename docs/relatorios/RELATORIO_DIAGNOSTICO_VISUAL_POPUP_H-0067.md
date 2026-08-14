# RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067

```yaml
rastreabilidade:
  etapa: DIAGNOSTICO_POS_VALIDACAO_MANUAL
  objeto: H-0067
  data: 2026-08-12
  branch: master
  head: 77bd8bf3772985325bc51a850f7c6d76d61ad573
  metodo: codigo_atual + probes_em_memoria
  nao_usado_como_prova_de_correcao:
    - docs/relatorios/IMP-0067-confirmacao-aplicacao-estilo.md
    - qualquer QA automatico que tenha declarado geometria/resize corretos

evidencia_manual:
  navegacao_estilo: correta (confirmada pelo enunciado; fora do escopo de defeito)
  borda_console: >
    ao abrir o popup de confirmacao de Estilo, a borda do Console
    subjacente aparece desenhada incorretamente abaixo/no entorno do popup
  margem_direita: >
    ao reduzir a largura horizontal, o popup de Estilo encosta na borda
    direita e nao mantem o afastamento observado nos popups canonicos
  controles_w_e_m: >
    popups acionados por w / e / m nao apresentam esses dois defeitos
    nas mesmas condicoes (controles positivos)

resultado:
  status: DIAGNOSTICO_CONCLUIDO
  bloqueios:
    - H-0068 permanece BLOQUEADA GERENCIALMENTE ate resolucao manual de H-0067
  stage: vazio
  artefato_unico_criado:
    - docs/relatorios/RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067.md
```

## 1. Respostas factuais (objetivo)

### 1.1 O popup de Estilo passa pelo mesmo pipeline de renderização dos popups w/e/m?

**Sim, no motor de composição.** Todos terminam em:

`renderizar_estado` → `renderizar_tela(..., popup=...)` → `sobrepor_no_corpo` → `_layout_popup` / `renderizar_popup` → `_caixa`.

Não há segundo renderer de popup para Estilo.

### 1.2 Se sim, qual dado/configuração/envelope faz o comportamento divergir?

A divergência **não** está na declaração do popup de Estilo em si (tipo, espaçamentos, chips Esc/Enter). Está no **corpo subjacente** sobre o qual o overlay mede geometria:

- A tela de Estilo (H-0063/H-0064) materializa amostras de chip com SGR ANSI
  (`amostra_chip` em `tela/renderizacao/estilo.py`) nas linhas dos presets
  “Destaque Texto” / “Destaque Fundo”.
- Essas linhas têm `len(linha) = L + 10` e `_largura_sem_ansi(linha) = L`.
- `sobrepor_no_corpo` e o trecho de overlay em `tela.py` usam
  `max(len(linha) ...)` como `largura_corpo`.

Os controles w/e/m abrem sobre a tela `demo`, cujo corpo **não** contém ANSI;
ali `len == largura visual == L`, e o motor se comporta corretamente.

### 1.3 Se não, onde os caminhos se separam?

Os caminhos **separam-se antes** do motor comum:

| Etapa | Estilo | w / e / m |
|---|---|---|
| Tecla/evento | `Enter`/`\r` na tela H-0063 com `aplicar_disponivel` | `w` / `e` / `m` via `acionamentos` da tela `demo` |
| Dispatch | `processar_comando` ramo H-0066/H-0067 | `_abrir_popup_demonstrativo` |
| Envelope | `ControladorTelaEstilo.conteudo_popup_confirmacao` | fixtures H-0057/H-0058 |
| Tela subjacente | `h0063_estilo_...` (Console com amostras ANSI) | `demo` (sem ANSI no corpo) |
| Motor comum | idêntico a partir de `abrir_popup` + `popup=` em `renderizar_tela` | idem |

### 1.4 Por que a borda do Console subjacente fica incorreta?

Porque o overlay calcula e aplica o retângulo do popup contra uma
`largura_corpo` **inflada** (+10 por causa do ANSI). As linhas cobertas pelo
popup saem com largura visual `L+10` (ou `popup_w` alinhado a essa base),
empurrando/apagando a coluna da borda direita `│` no retângulo do popup.
Linhas imediatamente abaixo do retângulo, não cobertas, permanecem com
largura `L` e borda íntegra — o defeito concentra-se no entorno das linhas
atravessadas pelo popup.

Não é “falha de restaurar após fechar”: já ocorre na **primeira**
renderização com popup aberto. Não é redraw parcial seletivo: o quadro é
recomposto por inteiro; a geometria do overlay é que está errada.

### 1.5 Por que o popup de Estilo encosta na borda direita quando a largura diminui?

Mesma causa. Com `largura_corpo = L+10`:

- em `L=100`: popup intrínseco 94 → `x=8`, `x_final=102` → ultrapassa `L` em 2;
- em `L≤90`: o popup passa a ocupar toda a largura **inflada**, gerando
  overflow visual de +10 colunas além do terminal.

Com medição visual correta (`largura_corpo = L`):

- em `L=100`: `x=3`, `x_final=97`, margens 3/3 (afastamento simétrico);
- em `L=120`: margens 13/13.

Os controles e/m, na mesma largura, mantêm margem porque o corpo não infla
(ex.: e em `L=80` → margens 1/2; popup 77).

### 1.6 Correção mínima (proposta — não implementada)

Fazer o overlay usar a **mesma semântica de largura visual** já canônica no
renderer (`_largura_sem_ansi` / `_ljust_sem_ansi` / corte por colunas
visíveis), em vez de `len()`, para medir o corpo e para fatiar/recombinar
linhas. Sem motor paralelo e sem exceção “se popup de estilo”.

---

## 2. Comparação de pipeline (lado a lado)

### 2.1 Popup Estilo (`popup_confirmacao_aplicacao_estilo`)

```text
F4 → tela H-0063
→ Espaco/setas (divergir candidato; Aplicar ativo)
→ Enter/\r
→ demo.processar_comando (ramo tela H-0063)
→ ControladorTelaEstilo.solicitar_aplicacao()
→ ControladorTelaEstilo.conteudo_popup_confirmacao(solicitacao)
→ popup.abrir_popup(modelo_h0063, ID_POPUP_CONFIRMACAO_APLICACAO_ESTILO, envelope)
→ estado["popup"] = instancia
→ renderizar_estado → renderizar_tela(..., popup=instancia)
→ tela.py: materializa bloco_corpo; mede largura_corpo=max(len)
→ popup.sobrepor_no_corpo → _layout_popup / renderizar_popup / splice centralizado
→ resize/redraw: mesmo caminho a cada SIGWINCH / nova (L,H)
```

Funções relevantes: `demo.processar_comando`, `ControladorTelaEstilo.solicitar_aplicacao`,
`conteudo_popup_confirmacao`, `abrir_popup`, `renderizar_estado`,
`renderizar_tela`, `sobrepor_no_corpo`, `_layout_popup`, `renderizar_popup`,
`consumir_tecla_popup` (modal).

### 2.2 Popup w (`popup_texto_dinamico`)

```text
tecla "w" na tela demo
→ _popup_acionado_por (acionamentos[])
→ _abrir_popup_demonstrativo
→ conteudo_popup_h0057()
→ abrir_popup(modelo_demo, "popup_texto_dinamico", ...)
→ renderizar_estado → renderizar_tela → sobrepor_no_corpo (mesmo motor)
```

### 2.3 Popup e (`popup_lista_exclusiva`)

```text
tecla "e"
→ _abrir_popup_demonstrativo
→ conteudo_popup_h0058_exclusiva()
→ abrir_popup(..., "popup_lista_exclusiva", tipo marcacao)
→ mesmo motor de overlay
```

### 2.4 Popup m (`popup_lista_multipla`)

```text
tecla "m"
→ _abrir_popup_demonstrativo
→ conteudo_popup_h0058_multipla()
→ abrir_popup(..., "popup_lista_multipla", tipo marcacao)
→ mesmo motor de overlay
```

### 2.5 Mesmo motor?

```yaml
mesmo_motor:
  entrada_render: renderizar_tela + sobrepor_no_corpo
  layout: _layout_popup / geometria_popup / renderizar_popup
  caixa: _caixa / _borda_de_estilo
  resposta: SIM
divergencias:
  - evento_de_abertura (Enter Aplicar vs acionamentos w/e/m)
  - tela_subjacente (H-0063 com ANSI nas amostras vs demo sem ANSI)
  - envelope (texto curto de confirmacao vs texto longo H-0057 / listas H-0058)
  - tipo (Estilo=texto+Enter; w=texto so Esc; e/m=marcacao+Enter)
  - NAO ha geometria dedicada de Estilo; a divergencia visual vem do corpo ANSI
```

---

## 3. Diagnóstico

### 3.1 Defeito: borda do Console subjacente

```yaml
defeito_borda_console:
  causa_raiz: >
    sobrepor_no_corpo (e o preambulo em renderizar_tela) medem a largura
    fisica do corpo com len(linha). Linhas do Console de Estilo contem
    sequencias SGR das amostras de chip (H-0064), inflando len em +10
    sem alterar a largura visual. O splice centralizado produz linhas do
    retangulo do popup com largura visual > L; a coluna da borda direita
    do Console e deslocada/perdida nessas linhas.
  arquivo:
    - tela/renderizacao/popup.py
    - tela/renderizacao/tela.py
    - tela/renderizacao/estilo.py  # origem do ANSI no corpo (nao o bug do overlay)
  funcao:
    - sobrepor_no_corpo  # max(len(linha)); splice por indice de str
    - renderizar_tela    # largura_corpo = max(len(linha)...) antes do overlay
    - amostra_chip / compor_titulo_com_amostra  # injeta ANSI no titulo do item
  comportamento: >
    Em L=100, linhas cobertas pelo popup saem com len=vis=110; varias
    terminam em espacos (borda │ ausente na coluna L) ou com │ alem de L.
    Linhas abaixo do retangulo permanecem len=vis=L. Controles w/e/m:
    overflow=0, borda direita preservada.
  porque_afeta_estilo: corpo da tela de Estilo tem linhas com ANSI
  porque_nao_afeta_w_e_m: corpo da tela demo nao tem ANSI; len==vis==L
  classificacao: DEFEITO_PREEXISTENTE_EXPOSTO_POR_H0067
  classificacao_secundaria: DEFEITO_INFRAESTRUTURA_POPUP
  justificativa_classificacao: >
    H-0067 reutilizou o motor generico corretamente do ponto de vista de
    contrato. O bug de medicao por len() ja existia no overlay; so passou
    a ser observavel quando um popup abriu sobre um corpo com ANSI
    (amostras H-0064). Nao e regressao da declaracao
    popup_confirmacao_aplicacao_estilo em si.
```

Hipóteses **refutadas** por probe:

| Hipótese | Veredito |
|---|---|
| Popup sobrescreve e não restaura após fechar | Refutada — defeito na 1ª pintura com popup aberto |
| Redraw só de parte da tela | Refutada — quadro completo; geometria errada |
| Coordenadas contra viewport diferente do terminal (além da inflação) | Parcial — a “viewport” usada é o corpo, mas a largura do corpo está errada |
| Ordem de camadas diferente para Estilo | Refutada — mesmo `popup=` em `renderizar_tela` |
| Borda já incorreta antes do popup | Refutada — sem popup, `max_vis=L` (quadro íntegro); só `max_len` infla |
| `linhas.maximo: 3` causa o defeito horizontal | Refutada — só altera altura da barra / `l_corpo_disponivel` |
| Conteúdo do texto/chips do popup força sozinho a borda quebrada | Refutada — intrínseco 94 é válido; a quebra exige a inflação |

### 3.2 Defeito: margem direita / encoste

```yaml
defeito_margem_direita:
  causa_raiz: >
    Mesma inflacao de largura_corpo. Centralizacao
    x=(largura_corpo_inflada - largura_popup)//2 desloca o popup e/ou
    permite x_final > L. Em larguras medias (ex. 100), o popup ja
    ultrapassa a borda direita do terminal; em larguras menores, ocupa
    toda a base inflada (overflow +10).
  arquivo:
    - tela/renderizacao/popup.py  # sobrepor_no_corpo
    - tela/renderizacao/tela.py     # medida preliminar de largura_corpo
  funcao:
    - sobrepor_no_corpo
    - _layout_popup  # recebe largura_corpo ja inflada; min(intrinseca, corpo)
  classificacao: DEFEITO_PREEXISTENTE_EXPOSTO_POR_H0067
  classificacao_secundaria: DEFEITO_INFRAESTRUTURA_POPUP
  fator_agravante_conteudo: >
    O texto de confirmacao tem len=87 e define largura intrinsica 94
    (maior que e/m=77). Isso faz as margens corretas sumirem mais cedo
    (em L≈94), mas NAO explica overflow alem de L nem a assimetria
    observada frente a e/m em L=80..120 — isso e exclusivo da inflacao.
  porque_nao_afeta_w_e_m: sem inflacao; e/m mantem margem ate L≈77
```

**Conclusão:** os dois sintomas manuais são **efeitos da mesma causa raiz**
(medição/splice por `len` sobre corpo com ANSI). Não são duas falhas
independentes de implementação.

```text
CAUSA_RAIZ:
  arquivo: tela/renderizacao/popup.py (+ tela/renderizacao/tela.py)
  funcao: sobrepor_no_corpo (e medida de largura_corpo em renderizar_tela)
  comportamento: largura_corpo = max(len(linha)) ignora que len inclui SGR
  porque_afeta_estilo: Console de Estilo embute ANSI nas amostras de chip
  porque_nao_afeta_w_e_m: corpo demo sem ANSI; len == largura visual
```

---

## 4. Probes

```yaml
probes:
  dimensoes_testadas: [120, 100, 90, 80, 70, 62, 60, 58, 55, 50]
  altura_fix: 28
  metodo: >
    processar_comando + renderizar_estado em memoria; derivacao de x/x_final
    pelo topo da caixa; comparacao quadro sem popup vs com popup;
    ciclos resize L_maior→L_menor→L_maior
  resultados:
    - id: estilo_L120
      terminal: 120
      largura_popup: 94
      x: 18
      x_final: 112
      margem_esquerda: 18
      margem_direita_contra_L: 8
      linhas_com_largura_gt_L: 7
      nota: corpo_max_len observado 130 (=L+10)
    - id: estilo_L100
      terminal: 100
      largura_popup: 94
      x: 8
      x_final: 102
      margem_direita_contra_L: -2
      linhas_com_largura_gt_L: 7
      borda_direita_linhas_popup: ausente_ou_alem_de_L
    - id: estilo_L80
      terminal: 80
      largura_popup: 90  # min(94, L+10)
      x: 0
      x_final: 90
      overflow_past_L: 10
    - id: estilo_L70
      terminal: 70
      largura_popup: 80
      overflow_past_L: 10
    - id: estilo_L62
      terminal: 62
      largura_popup: 72
      overflow_past_L: 10
    - id: w_todas_L_testadas
      overflow_past_L: 0
      nota: popup textual longo; ocupa L inteira quando L < intrinsica; sem overflow
    - id: e_L100
      largura_popup: 77
      x: 11
      x_final: 88
      margens: [11, 12]
      overflow_past_L: 0
    - id: e_L80
      largura_popup: 77
      x: 1
      x_final: 78
      margens: [1, 2]
      overflow_past_L: 0
    - id: m_igual_e_na_geometria_horizontal: true
    - id: corpo_estilo_sem_popup_L100
      linhas_ansi: [14, 15]
      len: 110
      vis: 100
      delta_sgr: 10
      amostra: "Destaque Texto/Fundo" com ESC[34m / ESC[44m + reset
    - id: corpo_demo_sem_popup
      linhas_ansi: 0
      len_eq_vis_eq_L: true
    - id: diffs_fora_retangulo_string_index
      estilo: 0_dentro_do_retangulo_inflado
      nota: >
        O overlay nao pinta fora do retangulo que ele mesmo calculou;
        o retangulo e que esta dimensionado/posicionado contra base errada,
        fazendo as linhas do retangulo excederem o terminal.
    - id: resize_estilo_120_100_120
      overflow_em_todos_os_frames: true
      residuo_apos_crescer: nao_aplicavel_ainda_overflow_na_largura_maior
    - id: resize_e_mesmo_ciclo
      overflow_em_todos_os_frames: false
    - id: geometria_hipotetica_largura_corpo_eq_L
      L120: {popup: 94, margens: [13, 13]}
      L100: {popup: 94, margens: [3, 3]}
      L90: {popup: 90, margens: [0, 0]}
      nota: elimina overflow; restaura afastamento simetrico enquanto L > 94
```

### 4.1 Unicode / largura visual

- Bordas box-drawing e chips usam tipicamente largura de célula 1; o
  problema medido **não** é East-Asian Width.
- O caminho de overlay **não** usa `_largura_sem_ansi` para
  `largura_corpo` nem para o splice — usa `len()` / fatiamento de `str`.
- Em outros pontos do renderer (`_caixa`, barra) a largura visual canônica
  já existe; o overlay do popup ficou inconsistente com essa primitiva.
- `_quebrar_texto` do popup também usa `len()`; o texto de Estilo não tem
  ANSI, então isso **não** é a causa dos dois defeitos observados (registrado
  só como dívida correlata, não como causa raiz deste diagnóstico).
- O caractere `⏎` na barra de Estilo não entra no `bloco_corpo` sobreposto;
  irrelevante para estes sintomas.

### 4.2 Fixture H-0063

| Alteração recente | Afeta geometria horizontal do popup? |
|---|---|
| `barra_de_menus.distribuicao.linhas.maximo: 3` | Não para os defeitos sob análise — só altura da barra / cota vertical do corpo |
| `popups.popup_confirmacao_aplicacao_estilo` | Define conteúdo/chips; intrínseco 94 é legítimo; não introduz ANSI nem `len()` no overlay |

### 4.3 Conteúdo específico do popup Estilo vs w/e/m

| Campo | Estilo | w | e / m |
|---|---|---|---|
| título | `Aplicar estilo` (14) | `Texto dinamico` | `Lista exclusiva` / `Lista múltipla` |
| texto/instrução | 87 chars (sem ANSI) | ~260 chars | instrução curta + itens |
| chips | Esc+Enter (vis 31) | só Esc | Esc+Enter |
| intrínseca | **94** (texto manda) | 267 | 77 |
| ANSI no envelope | não | não | não |

O conteúdo de Estilo **não** contém ANSI; o ANSI está no **Console sob o popup**.

---

## 5. Correção mínima proposta (sem implementar)

```yaml
correcao_minima_proposta:
  arquivos:
    - tela/renderizacao/popup.py
    - tela/renderizacao/tela.py
  alteracoes:
    - >
      Em sobrepor_no_corpo: largura_corpo = max(_largura_sem_ansi(linha));
      padding com _ljust_sem_ansi; splice por colunas visiveis (helper novo
      ou reuso de caminhada SGR-aware), nao por indice bruto de str.
    - >
      Em renderizar_tela, no bloco popup: a medida preliminar de
      largura_corpo deve usar a mesma largura visual.
    - >
      Nao remover amostras ANSI de Estilo; nao hardcodar excecao por ID de
      popup; nao criar motor paralelo.
    - >
      Opcional correlato (fora do minimo estrito dos sintomas): alinhar
      _quebrar_texto do popup a _largura_sem_ansi para envelopes futuros
      com ANSI — nao necessario para fechar este diagnostico.
  testes:
    - >
      Probe/regressao: render Estilo+popup em L∈{120,100,80,70,62} —
      nenhuma linha com _largura_sem_ansi > L; borda direita │ preservada
      fora do retangulo visual do popup.
    - >
      Margens: com L=100, popup Estilo com intrinsica 94 deve centralizar
      com margens 3/3 (nao x_final>L).
    - >
      Controles w/e/m nas mesmas larguras: sem regressao (overflow 0;
      margens de e/m preservadas).
    - >
      Resize estreito→largo→estreito com popup aberto: sem residuo de
      largura inflada.
    - >
      Comparar quadro sem popup vs com popup: divergencia de caracteres
      apenas no retangulo visual [x, x+wp) × [y, y+hp).
```

### 5.1 Regressões obrigatórias pós-patch

- popup Estilo (abertura via Enter/Aplicar)
- w, e, m
- largura normal (≥120) e estreita (80, 70, 62)
- resize estreito↔largo
- bordas do Console/tela subjacente
- margem direita / simetria de centralização
- infraestrutura H-0056–H-0060 (geometria/wrapping/overlay) e H-0067 (fluxo modal CONFIRMADO/ABORTADO)

### 5.2 Estado H-0068

Documentação H-0068 já existente no repositório **não foi alterada, validada
nem implementada** nesta etapa. Registro gerencial:

`H-0068: BLOQUEADA GERENCIALMENTE até resolução manual de H-0067.`

---

## 6. Git (somente leitura)

```text
branch: master
HEAD:   77bd8bf3772985325bc51a850f7c6d76d61ad573
staged: (vazio)
acao: criado apenas docs/relatorios/RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067.md
```

Nenhum patch de código, teste, handoff, ADR, contrato ou backlog.
Nenhum stage/commit/push.
```
