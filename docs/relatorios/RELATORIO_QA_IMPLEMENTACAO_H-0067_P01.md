# RELATORIO_QA_IMPLEMENTACAO_H-0067_P01

```yaml
rastreabilidade:
  etapa: QA_IMPLEMENTACAO
  objeto: H-0067
  revisao: P01
  origem:
    docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0067_P01.md

resultado:
  status: I1_IMPLEMENTATION_APPROVED
  testes:
    popup: "83 passed (tela/teste_popup.py + demo/teste_demo_popup.py)"
    h0067: "22 passed (tela/teste_estilo_h0067.py + demo/teste_demo_estilo_h0067.py)"
    regressao_h0063_h0064_h0065_h0066_h0067: "113 passed"
    suite_completa: "1296 passed, 0 failed"
  achados: []
  bloqueios:
    - "H-0068 permanece BLOQUEADA GERENCIALMENTE ate H-0067 passar pela validacao manual"
    - "validacao_manual_necessaria permanece obrigatoria (gate separado; nao usa I5)"

pontos_especiais:
  largura_visual: >
    Caminho de overlay relevante usa max(_largura_sem_ansi(linha)) em
    sobrepor_no_corpo e na medida preliminar de renderizar_tela. Nao resta
    max(len(linha)) para geometria de corpo. SGR nao conta como coluna.
    max(len(coluna)) residuais em formacao de marcacao e max(len(texto)) na
    intrinsica textual do popup nao medem largura de terminal do overlay.
  padding: >
    Padding do corpo no overlay usa _ljust_sem_ansi(linha_atual, largura_corpo)
    condicionado a _largura_sem_ansi < largura_corpo. Nao ha linha.ljust
    bruto no splice.
  dividir_visual: >
    Corte por coluna visual; CSI completo nunca e fatiado; texto visivel
    prefixo/sufixo correto nos probes (antes de SGR, dentro de regiao
    colorida, apos reset, corte 0 e fim visual). Segmento auto-contido
    descartado no meio nao deixa ESC/fg/bg no sufixo. Sem overflow visual
    no quadro final Estilo.
  sgr: >
    Rastreio separado fg/bg confirmado: reset_total (0) limpa ambos;
    reset_fg (39) e reset_bg (49) sao independentes; reopen so quando o
    canal permanece aberto no corte. Subconjunto suficiente para SGR
    simples usados no projeto (texto_ansi: 32/33/34/90 + 39; estilo
    amostra_chip: fg + bg derivado 40-47/100-107 + 49). \x1b[1;34m cai em
    "outro" e nao e usado nas amostras. Fluxo real Estilo: 0 linhas com
    ESC no quadro final com popup (amostras cobertas sem residuo).
  console_subjacente: >
    L=100: linhas fora do retangulo vertical identicas byte a byte ao
    quadro sem popup; nas linhas atravessadas, prefixo/sufixo visiveis
    fora de [x, x_final) equivalentes; nenhuma linha com
    _largura_sem_ansi > L.
  margem_direita: >
    L=100: largura_popup=94, x=3, x_final=97, margens 3/3. L=120: 13/13.
    L<=80: popup ocupa L, margens 0/0, sem overflow.
  controles_w_e_m: >
    Em 120/100/80/70/62: overflow=0; e/m preservam geometria previa
    (ex. L=100 popup=77 x=11; L=80 x=1); centralizacao e modalidade
    intactas. Correcao generica sem hardcode de Estilo.
  resize: >
    Ciclo Estilo 120->80->62->100->120: max_visual<=L, mesma instancia,
    sem residuo ANSI, centralizacao coerente. Ciclo equivalente com e:
    idem.
  funcional_h0067: >
    Enter/Aplicar abre popup; Enter->CONFIRMADO (retém solicitacao);
    Esc->ABORTADO (descarta, nao sai da tela); modalidade bloqueia
    subjacente; snapshot imutavel; sem persistencia/publicacao.
    _quebrar_texto intacto: aceitavel — envelope Estilo sem ANSI.
  validacao_manual_necessaria:
    - popup Estilo largura normal
    - popup Estilo largura estreita
    - borda Console subjacente
    - resize estreito/largo
    - comparacao visual com w/e/m

arquivos_escopo_p01:
  alterados:
    - tela/renderizacao/popup.py
    - tela/renderizacao/tela.py
    - tela/teste_popup.py
    - demo/teste_demo_estilo_h0067.py
  criados_pelo_patch:
    - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0067_P01.md
  este_qa:
    - docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0067_P01.md

git:
  stage: vazio
  acao: somente leitura; nenhum stage/commit/push
```

## Veredito

Auditoria independente do P01 confirma correcao da causa raiz do diagnostico
visual: medicao/splice do overlay agora e ANSI-aware via `_largura_sem_ansi`,
`_ljust_sem_ansi` e `_dividir_visual`. Probes em memoria no fluxo real
(F4 → divergencia → Enter) eliminam overflow em todas as larguras pedidas e
restauram L=100 com margens 3/3. Controles w/e/m e semantica H-0067 nao
regrediram. Suítes batem o esperado (83 / 22 / 113 / 1296). Status tecnico
aprovado; validacao manual listada permanece obrigatoria antes de reabrir o
gate manual de H-0067. H-0068 nao foi lido nem alterado.
