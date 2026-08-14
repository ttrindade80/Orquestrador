# RELATORIO_PATCH_IMPLEMENTACAO_H-0067_P01

```yaml
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0067
  patch: P01
  origem:
    - docs/relatorios/RELATORIO_DIAGNOSTICO_VISUAL_POPUP_H-0067.md

resultado:
  status: PATCH_APLICADO
  causa_raiz_tratada: >
    sobrepor_no_corpo (tela/renderizacao/popup.py) e a medida preliminar de
    largura_corpo em renderizar_tela (tela/renderizacao/tela.py) mediam o
    corpo fisico com max(len(linha)), contando bytes de sequencias SGR como
    colunas. Linhas de amostra ANSI H-0064 ("Destaque Texto"/"Destaque
    Fundo") inflavam essa medida (+10), deslocando a centralizacao do
    popup, produzindo padding via ljust() bruto e splice por indice cru de
    str -- causa unica dos dois sintomas manuais (borda do Console
    incorreta e popup encostando/ultrapassando a borda direita).
  arquivos_alterados:
    - tela/renderizacao/popup.py
    - tela/renderizacao/tela.py
    - tela/teste_popup.py
    - demo/teste_demo_estilo_h0067.py
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0067_P01.md
  alteracoes:
    largura_corpo: >
      max(len(linha)) substituido por max(_largura_sem_ansi(linha)) nos
      dois pontos de medida (sobrepor_no_corpo e renderizar_tela). Nenhuma
      outra formula de geometria (x, x_final, altura) foi alterada.
    padding: >
      linha_atual.ljust(largura_corpo) substituido por
      _ljust_sem_ansi(linha_atual, largura_corpo), preservando SGR e
      contando apenas colunas visiveis.
    splice_visual: >
      Substituido o corte por indice cru (linha[:x] + popup + linha[x+w:])
      por composicao em colunas visuais via novo helper privado
      _dividir_visual(texto, corte), reutilizando _largura_sem_ansi ja
      canonico. Nao ha motor paralelo: o helper e chamado duas vezes
      (split em x, depois em largura_popup) dentro do mesmo
      sobrepor_no_corpo generico que atende Estilo e w/e/m.
    ansi: >
      _dividir_visual nunca corta uma sequencia ESC/CSI no meio (preserva
      o codigo inteiro em qualquer lado do corte). Estado de cor ainda
      aberto no ponto de corte e reaberto no sufixo, com rastreio separado
      de foreground/background reconhecendo os resets efetivamente usados
      neste codigo (\x1b[39m, \x1b[49m, \x1b[0m) -- nao apenas reset total.
      Um segmento auto-contido (abre e fecha antes do corte, caso real de
      amostra_chip) nao deixa nenhum residuo SGR no sufixo.
  testes:
    popup: "83 passed (tela/teste_popup.py + demo/teste_demo_popup.py)"
    h0067: "22 passed (tela/teste_estilo_h0067.py + demo/teste_demo_estilo_h0067.py)"
    regressao_h0063_h0064_h0065_h0066_h0067: "113 passed"
    suite_completa: "1296 passed, 0 failed"
  probes:
    - "L=120: largura_popup=94 x=13 x_final=107 margem_esq=13 margem_dir=13 max_visual=120"
    - "L=100: largura_popup=94 x=3  x_final=97  margem_esq=3  margem_dir=3  max_visual=100"
    - "L=80:  largura_popup=80 x=0  x_final=80  margem_esq=0  margem_dir=0  max_visual=80"
    - "L=70:  largura_popup=70 x=0  x_final=70  margem_esq=0  margem_dir=0  max_visual=70"
    - "L=62:  largura_popup=62 x=0  x_final=62  margem_esq=0  margem_dir=0  max_visual=62"
    - "controles w/e/m nas mesmas larguras: overflow=0 em todas (sem regressao)"
  validacao_manual_necessaria:
    - popup Estilo em largura normal
    - popup Estilo em largura estreita
    - borda Console subjacente
    - resize estreito/largo
    - comparacao visual com w/e/m
  bloqueios:
    - "H-0068 permanece BLOQUEADA GERENCIALMENTE ate H-0067 passar novamente pela validacao manual"

preservacoes:
  - sem_motor_paralelo
  - sem_hardcode_estilo
  - amostras_ANSI_H0064
  - CONFIRMADO_ABORTADO
  - modalidade
  - snapshot
  - sem_persistencia
  - sem_publicacao
```

## Resumo da correcao

O diagnostico ja havia isolado a causa raiz em dois pontos de medicao por
`len()` sobre o corpo materializado. Este patch trocou exclusivamente essas
duas medidas por `_largura_sem_ansi` (ja existente em
`tela/renderizacao/texto_ansi.py`, reutilizada, nao duplicada), trocou o
padding `ljust()` bruto por `_ljust_sem_ansi`, e substituiu o splice por
indice cru de string por um novo helper privado `_dividir_visual`, local a
`popup.py`, chamado duas vezes em `sobrepor_no_corpo` para produzir
prefixo/sufixo por coluna visual. Nao foi criado nenhum caminho especial
para o popup de Estilo: a mudanca e inteiramente na infraestrutura generica
consumida tambem por `w`/`e`/`m`.

`tela/renderizacao/estilo.py` (origem das amostras ANSI) nao foi tocado.
`_quebrar_texto` nao foi alterado -- o conteudo do popup de Estilo nao
contem ANSI, e nenhum teste desta etapa exigiu essa mudanca (H-0067
§11 respeitado).

Durante a implementacao do splice visual foi descoberto e corrigido um
segundo defeito, mais sutil, dentro do proprio helper novo: a primeira
versao de `_dividir_visual` so reconhecia `\x1b[0m` como reset, mas este
codigo-fonte usa resets especificos de canal (`\x1b[39m` para
foreground, `\x1b[49m` para background, definidos em
`tela/renderizacao/texto_ansi.py`/`estilo.py`). Sem o reconhecimento por
categoria, um segmento SGR auto-contido e totalmente coberto pelo
retangulo do popup (o caso real das amostras "Destaque Texto"/"Destaque
Fundo") deixava um par abre+reset "morto" (sem efeito visual, mas
presente como bytes) vazando para o sufixo. Corrigido rastreando
foreground e background separadamente antes de compor o sufixo; a prova
esta em `test_overlay_corta_segmento_ansi_no_meio_sem_corromper_sequencia`
e confirmada empiricamente: renderizando a tela de Estilo real (F4 ->
divergencia -> Enter) em L=100/120/260, nenhuma linha do quadro final
contem `\x1b` residual fora do necessario.

## Prova sobre o fluxo real H-0067

Os probes numericos e os novos testes em
`demo/teste_demo_estilo_h0067.py` usam o fluxo real (F4, divergir
candidato, Enter, popup aberto) sobre a fixture H-0063/H-0064 real —
nao um corpo sintetico. O caso concreto do diagnostico foi reproduzido
byte a byte: em L=100 a intrinseca permanece 94 e as margens sao
exatamente 3/3 (nunca `x=8`/`x_final=102`); em L=120, margens 13/13; em
L<=90 o popup ocupa a largura disponivel sem ultrapassa-la (margens
0/0). `test_borda_console_subjacente_preservada_fora_do_popup` renderiza
a tela com e sem popup a partir do MESMO estado de navegacao e prova que
(a) as linhas fora do retangulo vertical do popup sao identicas
byte-a-byte, incluindo a borda `│`; (b) nas linhas atravessadas
verticalmente, o texto visivel fora da faixa horizontal `[x, x_final)`
tambem permanece identico. `test_resize_popup_estilo_geometria_sem_
residuo_em_cada_frame` cobre o ciclo 120->80->62->100->120 com a mesma
instancia de popup, sem overflow em nenhum frame.

Os controles `w`/`e`/`m` foram reexecutados nas mesmas larguras
(120/100/80/70/62): overflow=0 em todos, sem alteracao de codigo ou
configuracao proprios deles -- a correcao e inteiramente na
infraestrutura compartilhada.

## Limite e proximos passos

Este patch e estritamente geometrico/compositivo: nenhuma regra de
CONFIRMADO/ABORTADO, modalidade, snapshot, persistencia ou publicacao foi
tocada (testes de fronteira, snapshot e non-TTY do H-0067 seguem
passando). `pytest` completo passa (1296/1296), mas — como o proprio
diagnostico se originou de uma falha que os testes automaticos anteriores
nao capturaram — este patch **nao** deve ser considerado fechado apenas
por isso. A validacao manual listada acima e obrigatoria antes de
qualquer nova tentativa de validacao de H-0067. H-0068 continua
BLOQUEADA GERENCIALMENTE. Nenhum arquivo de handoff, ADR, contrato,
nomenclatura ou backlog foi alterado; stage permanece vazio; nenhum
commit ou push foi realizado.
