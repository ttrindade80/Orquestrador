---
description: Levantamento pos-validacao manual do H-0040 sem correcao de codigo, fixtures ou documentacao normativa
---

# Relatorio de Levantamento Pos-Validacao Manual H-0040

## 1. Identificacao

```yaml
etapa: LEVANTAMENTO_POS_VALIDACAO_MANUAL_H0040
handoff: H-0040
adr: ADR-0031
data: 2026-07-26
relatorio: docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
```

## 2. Objeto

Investigar os problemas reportados na validacao manual do H-0040, sem aplicar
correcoes, e classificar cada ponto como defeito de implementacao, defeito de
demonstracao/fixture, defeito do roteiro, lacuna documental que exige ADR ou
evidencia insuficiente.

## 3. Estado de entrada

```yaml
handoff: H-0040
adr: ADR-0031
qa_tecnico: I1_IMPLEMENTATION_APPROVED
validacao_manual:
  resultado_global: NAO_APROVADA
  VM-01: APROVADO
  VM-02: INCONCLUSIVO
  VM-03: APROVADO
  VM-04: APROVADO
  VM-05: APROVADO
  VM-06: APROVADO
  VM-07: FALHOU
  VM-08: APROVADO
  VM-09: APROVADO
  VM-10: APROVADO_COM_COBERTURA_FRACA
  VM-11: APROVADO_COM_COBERTURA_FRACA
```

## 4. Autoridades

Lidas e usadas como autoridades:

- `docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md`
- `docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md`
- `docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md`
- `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/nomenclatura/32_CONSOLE.md`
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`

Inspecionados seletivamente:

- `demo/demo.py`
- `demo/demo_navegacao.py`
- `tela/navegacao.py`
- `tela/renderizador.py`
- `config/telas/demo/h0040_nav_dois_consoles.json`
- `config/telas/demo/h0040_nav_tres_consoles_em_grupo.json`
- `config/telas/demo/h0040_nav_console_unico_linear.json`
- `config/telas/demo/h0040_nav_console_grade_2x3.json`
- `config/telas/demo/h0040_nav_degenere_uma_linha.json`
- `config/telas/demo/h0040_nav_degenere_uma_coluna.json`
- cenarios H-0037 de modo: `h0037_console_nao_verboso.json`,
  `h0037_console_verboso_dois_niveis.json`,
  `h0037_console_alternavel_tres_niveis.json`.

## 5. Estado Git

Inventario inicial executado somente com comandos permitidos:

```yaml
git_diff_cached_name_only: []
git_diff_name_only:
  - demo/demo.py
  - docs/adr/INDICE_ADR.md
  - docs/backlog.md
  - docs/contratos/contrato_barra_de_menus.md
  - docs/contratos/contrato_chip.md
  - docs/contratos/contrato_composicao_corpo.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
  - docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
  - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
  - docs/nomenclatura/32_CONSOLE.md
  - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
  - tela/renderizador.py
arquivos_nao_rastreados_relevantes_h0040:
  - config/telas/demo/h0040_nav_console_grade_2x3.json
  - config/telas/demo/h0040_nav_console_unico_linear.json
  - config/telas/demo/h0040_nav_degenere_uma_coluna.json
  - config/telas/demo/h0040_nav_degenere_uma_linha.json
  - config/telas/demo/h0040_nav_dois_consoles.json
  - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
  - demo/demo_navegacao.py
  - demo/teste_demo_navegacao.py
  - docs/adr/ADR-0031-navegacao-simples-e-selecao-unica-em-console-de-nivel-unico.md
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
  - docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0040.md
  - docs/relatorios/RELATORIO_PATCH_H-0040_IMPLEMENTACAO.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_H-0040_IMPLEMENTACAO.md
  - tela/navegacao.py
  - tela/teste_navegacao.py
observacao: worktree acumulado preservado; nenhum arquivo preexistente foi alterado por este levantamento.
```

## 6. Analise de VM-02

Com dois consoles, a demonstracao aberta por `h0040_nav_dois_consoles.json`
inicia com foco no primeiro console. A lista de foco material observada foi:

```yaml
lista_foco: [console_esq, console_dir]
estado_inicial:
  foco_console: 0
Tab_a_partir_do_foco_0:
  foco_console: 1
  console: console_dir
Shift_Tab_a_partir_do_foco_0:
  foco_console: 1
  console: console_dir
```

Isso confirma materialmente a observacao do usuario: numa lista circular de
dois consoles, avancar a partir do primeiro e recuar a partir do primeiro
produzem a mesma mudanca visual imediata. O comportamento e coerente com D5,
mas o roteiro VM-02 nao consegue distinguir sentido direto e inverso nesse
cenario.

O cenario `h0040_nav_tres_consoles_em_grupo.json` produziu:

```yaml
lista_foco_depth_first: [console_a1, console_a2, console_externo]
Tab:
  sequencia: [console_a2, console_externo, console_a1, console_a2]
  circularidade: true
  entrada_item_0: true
Shift_Tab:
  sequencia: [console_externo, console_a2, console_a1, console_externo]
  circularidade: true
  entrada_item_0: true
ordem_depth_first: true
```

Classificacao de VM-02: `DEFEITO_DO_ROTEIRO_DE_VALIDACAO`.

## 7. Analise da politica de modo de VM-07

No JSON nominal de VM-07:

```yaml
arquivo: config/telas/demo/h0040_nav_console_unico_linear.json
politica_exibicao:
  modo_inicial: normal
  verboso: false
politica_modo: ausente
modo_inicial_D23: ausente
alternancia_por_V: ausente
conteudo_externo_multinivel: false
modelo:
  politica_modo: null
  modo_inicial: null
```

A tela e classificada como `legada_sem_politica` para D23. Ela usa envelope
pre-ADR-0028 com `itens` diretos, nao console com `conteudo_externo`
multinivel. A regra vigente em ADR-0028, `contrato_console.md` e
`contrato_barra_de_menus.md` e que `V` so e acao aplicavel em telas
multinivel com `politica_modo: "alternavel"`.

```yaml
VM07_tecla_V:
  classificacao: DEFEITO_DO_ROTEIRO_DE_VALIDACAO
  expectativa_compativel_com_politica_real: false
  nova_ADR_necessaria: false
  correcao_minima: retirar a expectativa de alternancia por V de VM-07; se for preciso validar alternancia, usar cenario H-0037 alternavel.
```

Achado adjacente, sem correcao aplicada: `processar_comando()` nao preserva
`modo_verboso_forcado` ao processar comandos. Assim, uma sessao iniciada por
`--verboso` pode perder o modo efetivo apos comando posterior com redesenho.
Isso e candidato a patch de implementacao existente, nao a nova ADR.

## 8. Analise do item multilinha

Texto real do item longo:

```yaml
id: i3
texto: "Gamma Delta Epsilon Zeta Eta Theta Iota Kappa Lambda Mu"
comprimento: 55
numero_de_itens: 4
distribuicao_matricial:
  politica: preferencia_colunas
  colunas_minimo: 1
  colunas_maximo: 1
  ordem: por_linha
```

Em modo normal, o caminho matricial nao quebra o item; o texto e truncado pela
celula. Em modo verboso efetivo, o renderer quebra o texto em linhas fisicas.
A abertura `--verboso` torna o modo efetivo verboso por override de runtime,
mas isso nao equivale a tela alternavel por `V`.

Faixa observada com altura 24:

```yaml
largura_10_a_32:
  resultado: quadro_minimo_terminal_pequeno
largura_33_a_34:
  resultado: aceita_e_produz_continuacao
  observacao: sobreposicao visual no fim do item longo com o item Omega
largura_35_a_90:
  resultado: aceita_e_produz_continuacao_sem_sobreposicao_observada
exemplo_largura_80:
  linhas_item_longo:
    - "Gamma Delta Epsilon Zeta Eta Theta"
    - "Iota Kappa Lambda Mu"
```

```yaml
VM07_item_multilinha:
  menor_largura_valida_testada: 33
  menor_largura_sem_sobreposicao_observada: 35
  largura_que_produz_continuacao: 35..90 com altura 24
  continuacao_observada: true
  causa: faixa_existe; falso_negativo_manual_induzido_por_roteiro_sem_dimensao_segura_e_por_expectativa_de_V
  classificacao: DEFEITO_DO_ROTEIRO_DE_VALIDACAO
```

O item multilinha e observavel em dimensoes validas. A lista de causas para
faixa inexistente (`DADOS_INSUFICIENTES`, `DISTRIBUICAO_INADEQUADA`,
`LIMITE_MINIMO_INCOMPATIVEL`, `MODO_VERBOSO_NAO_APLICAVEL`,
`DEFEITO_DE_RENDERIZACAO`) nao se aplica como causa principal, porque a faixa
existe. A sobreposicao em 33-34 e risco de implementacao a investigar em patch,
mas nao explica a inexistencia de faixa.

## 9. Limites validos do terminal

```yaml
limite_global_demo:
  largura_minima_fisica: 10
  altura_minima_fisica: 6
quadro_minimo_por_renderizacao_VM07_verboso:
  altura_24:
    primeira_largura_normal: 33
    primeira_largura_multilinha_sem_sobreposicao: 35
  altura_16:
    primeira_largura_normal: 61
  altura_30:
    primeira_largura_normal: 27
  altura_40:
    primeira_largura_normal: 17
```

O ponto em que aparece a mensagem `terminal pequeno demais` pode vir do limite
fisico global ou de `RenderizadorErro`/fallback de impossibilidade geometrica
durante a distribuicao. Para VM-07, em altura 24 a transicao material observada
foi largura 32 com quadro minimo e largura 33 com tela normal.

## 10. Modo verboso e dados

O modo verboso vigente em ADR-0028 opera sobre dados com campos semanticos
adicionais em `conteudo_externo` multinivel. Ele nao e definido apenas como
"quebrar qualquer texto longo" de qualquer fixture. As autoridades dizem:

- modo nao verboso: uma linha fisica por conteudo aplicavel, com truncamento;
- modo verboso: varias linhas fisicas calculadas, com continuacao alinhada;
- `V`: exclusivo de telas alternaveis;
- politica de modo: pertence ao console com conteudo multinivel externo;
- composicao do corpo nao infere politica de modo por largura, altura ou
  distribuicao.

Comparacao:

```yaml
H0037:
  dados: conteudo_externo_multinivel
  politicas_reais:
    - somente_nao_verboso
    - somente_verboso
    - alternavel
  tecla_V: aplicavel_somente_em_alternavel
H0040_VM07:
  dados: itens_diretos_pre_ADR_0028
  conteudo_externo: false
  politica_modo: null
  uso_de_verboso: override_demonstrativo_por_--verboso
  classificacao_dados: DADO_LONGO_APENAS_PARA_WRAP
```

## 11. Analise de VM-10 e VM-11

O cenario linear de quatro itens permanece 4 linhas x 1 coluna nas larguras
35, 60, 80 e 120. Ele confirma preservacao basica do item logico em
redimensionamento, mas nao comprova materialmente:

- mudanca de quantidade de colunas;
- mudanca de quantidade de linhas;
- mudanca de vizinhos por redistribuicao;
- matriz incompleta;
- linhas de separacao entre itens;
- item multilinha no comando sem `--verboso`.

```yaml
VM10_VM11:
  comportamento_basico_confirmado: true
  cobertura_material_suficiente: false
  melhor_cenario_existente: h0040_nav_console_grade_2x3.json
  complemento_existente:
    - h0040_nav_degenere_uma_linha.json
    - h0040_nav_degenere_uma_coluna.json
    - h0040_nav_tres_consoles_em_grupo.json
  arquivo_novo_necessario: somente_se_o_roteiro_exigir_redistribuicao_dinamica_observavel_por_redimensionamento
  nova_ADR_necessaria: false
```

Classificacao de VM-10/VM-11: `DEFEITO_DE_DEMONSTRACAO_OU_FIXTURE` para a
cobertura fraca do cenario usado no roteiro; `DEFEITO_DO_ROTEIRO_DE_VALIDACAO`
se o roteiro continuar declarando cobertura material que o cenario linear nao
tem.

## 12. Analise do principio arquitetural

| Principio | Autoridade existente | Ja decidido | Implementacao atual compativel | Exige ADR |
|---|---|---:|---:|---:|
| A navegacao consome as distribuicoes existentes | ADR-0031 D7/D10/D12; relatorio de implementacao §15.1 | sim | sim | nao |
| A geometria de navegacao corresponde a geometria renderizada | ADR-0031 D10; NC-003/NC-006; QA pos-patch §§12-15 | sim | sim, com risco pontual em `--verboso`/comandos | nao |
| Nao existe grade paralela | `tela/navegacao.py` docstring; relatorio de implementacao §15.1 | sim | sim | nao |
| O indicador apenas reserva espaco dentro da distribuicao | ADR-0031 D12; relatorio de patch §§7-10 | sim | sim | nao |
| As regras de teclado nao redefinem o layout | ADR-0031 D5-D10; contrato_console §22 | sim | sim | nao |

O principio arquitetural levantado pelo usuario ja esta documentado. Nao ha
lacuna documental que exija ADR nova.

## 13. Matriz de necessidade de ADR

| Problema | Decisao ausente? | Pode ser resolvido por patch/roteiro/fixture? | Nova ADR |
|---|---:|---:|---:|
| VM-02 usa dois consoles para provar sentido de Shift+Tab | nao | sim, roteiro/cenario | nao |
| VM-07 espera `V` em tela legada sem politica alternavel | nao | sim, roteiro | nao |
| VM-07 item multilinha nao observado manualmente | nao | sim, roteiro/dimensoes/fixture; possivel patch de robustez | nao |
| VM-10/VM-11 pouca redistribuicao observavel | nao | sim, roteiro/fixture/teste | nao |
| Principio arquitetura distribuicao+navegacao | nao | ja decidido | nao |

Nenhuma das materias que exigiriam nova ADR foi encontrada: novo limite minimo
de terminal, nova politica de overflow, `V` em telas nao alternaveis, nova
semantica de modo verboso, navegacao fora do nivel unico, nova familia de
distribuicao, alteracao de paginacao ou alteracao estrutural de contratos.

## 14. Correcoes minimas candidatas

Nao aplicadas neste levantamento:

- VM-02: trocar o roteiro manual para `h0040_nav_tres_consoles_em_grupo.json`
  ao validar sentido direto/inverso e circularidade.
- VM-07: separar "abrir em `--verboso` e observar item multilinha" de "testar
  alternancia por `V`"; validar `V` somente em H-0037 alternavel.
- VM-07: registrar largura/altura segura, por exemplo largura 80 altura 24,
  ou faixa minima largura >= 35 em altura 24.
- VM-07 patch candidato: preservar `modo_verboso_forcado` em
  `demo/demo.py::processar_comando`.
- VM-07 patch candidato: investigar sobreposicao em larguras 33-34.
- VM-10/VM-11: usar `h0040_nav_console_grade_2x3.json` e degenerados para
  matriz incompleta/eixos; criar ou revisar fixture apenas se a validacao
  manual exigir mudanca dinamica de linhas/colunas por redimensionamento.

## 15. Arquivos possivelmente envolvidos

```yaml
roteiro_validacao:
  - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
fixtures_ou_demos:
  - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
  - config/telas/demo/h0040_nav_console_unico_linear.json
  - config/telas/demo/h0040_nav_console_grade_2x3.json
  - config/telas/demo/h0040_nav_degenere_uma_linha.json
  - config/telas/demo/h0040_nav_degenere_uma_coluna.json
implementacao_caso_patch_seja_aberto:
  - demo/demo.py
  - tela/renderizador.py
testes_caso_patch_seja_aberto:
  - demo/teste_demo_navegacao.py
  - tela/teste_navegacao.py
```

## 16. Riscos

- Ajustar somente o texto do roteiro sem cobrir o risco de
  `modo_verboso_forcado` pode deixar `--verboso` instavel apos comandos.
- Usar dois consoles para VM-02 continuara inconclusivo por simetria circular.
- Usar o cenario linear para VM-10/VM-11 continuara aprovando com cobertura
  fraca, pois a geometria nao muda.
- Larguras 33-34 em VM-07 produzem continuacao, mas com sobreposicao observada;
  devem ser evitadas como faixa manual segura ate patch especifico.

## 17. Classificacao final

```yaml
classificacao_final: NO_NEW_ADR_PATCH_EXISTING_CYCLE
justificativa:
  nova_decisao_de_produto_ausente: false
  problemas_resolutiveis_por:
    - roteiro_manual
    - cenario_de_demonstracao
    - fixture
    - teste_automatizado
    - patch_de_implementacao_dentro_de_ADR_0031_ADR_0028
```

## 18. Proximo passo recomendado

Abrir um ciclo de patch existente, sem ADR nova, com duas frentes: corrigir o
roteiro/fixtures de validacao manual e, se aceito no escopo do patch, cobrir a
preservacao de `modo_verboso_forcado` e a sobreposicao de larguras estreitas
do item multilinha.

## 19. Estado Git final

Este levantamento criou somente:

```text
docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
```

Nenhum `git add`, `git restore`, `git reset`, `git checkout`, `git clean`,
`git stash` ou `git commit` foi executado. Nenhum `__pycache__` foi removido.

## 20. Encerramento

```yaml
resultado:
  etapa: LEVANTAMENTO_POS_VALIDACAO_MANUAL_H0040
  handoff: H-0040

  VM_02:
    classificacao: DEFEITO_DO_ROTEIRO_DE_VALIDACAO
    cenario_atual_suficiente: false
    cenario_tres_consoles_suficiente: true
    correcao_candidata: usar h0040_nav_tres_consoles_em_grupo.json para sentido direto, inverso, circularidade, entrada no item 0 e ordem depth-first
    nova_ADR_necessaria: false

  VM_07:
    politica_de_modo: legada_sem_politica
    V_aplicavel: false
    item_multilinha_observavel_em_dimensao_valida: true
    causa: roteiro espera V em cenario nao alternavel; faixa multilinha segura existe com --verboso
    classificacao: DEFEITO_DO_ROTEIRO_DE_VALIDACAO
    correcao_candidata: separar validacao de --verboso da validacao de V; usar H-0037 alternavel para V; registrar largura segura
    nova_ADR_necessaria: false

  VM_10_VM_11:
    cobertura_atual: APROVADO_COM_COBERTURA_FRACA
    melhor_cenario_existente: h0040_nav_console_grade_2x3.json
    correcao_candidata: trocar ou complementar roteiro com grade_2x3 e degenerados; criar/revisar fixture apenas para redistribuicao dinamica se exigida
    nova_ADR_necessaria: false

  principio_arquitetural:
    ja_documentado: true
    implementacao_compativel: true
    lacuna_documental: false

  nova_ADR:
    necessaria: false
    decisoes_ausentes: []

  arquivos_possivelmente_envolvidos:
    - docs/handoff/H-0040-implementar-navegacao-simples-e-selecao-unica-console-nivel-unico.md
    - config/telas/demo/h0040_nav_tres_consoles_em_grupo.json
    - config/telas/demo/h0040_nav_console_unico_linear.json
    - config/telas/demo/h0040_nav_console_grade_2x3.json
    - demo/demo.py
    - tela/renderizador.py
    - demo/teste_demo_navegacao.py
    - tela/teste_navegacao.py
  nenhum_arquivo_preexistente_alterado: true
  operacoes_git_de_escrita_executadas: []
  commit_executado: nao

  relatorio_criado: docs/relatorios/RELATORIO_LEVANTAMENTO_POS_VALIDACAO_MANUAL_H-0040.md
  classificacao_final: NO_NEW_ADR_PATCH_EXISTING_CYCLE
```

NO_NEW_ADR_PATCH_EXISTING_CYCLE
