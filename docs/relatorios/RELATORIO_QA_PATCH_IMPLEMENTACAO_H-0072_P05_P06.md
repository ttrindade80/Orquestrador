# RELATÓRIO — QA_POS_PATCH H-0072 P05+P06

```yaml
etapa: QA_POS_PATCH
objeto: H-0072
patches_auditados:
  - P05
  - P06
achados_origem:
  - VM-H0073-001
  - VM-H0073-002
predecessor_imediato:
  docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P06.md
cadeia_raiz:
  docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
status: I1_IMPLEMENTATION_APPROVED
```

## Resultado

Os dois achados estão tecnicamente resolvidos e **PRONTO_PARA_REVALIDACAO** em
TTY. Não há achado material de implementação, handoff ou documentação.

## VM-H0073-001 — H-0055 / tabulação dinâmica

P06 não alterou a fórmula genérica: `_escolher_maior_que_cabe` e
`_cabe_tabulacao` permanecem os mesmos. A única alteração de configuração de
P06 é `barra_de_menus.distribuicao.linhas.maximo: 3 → 5` em
`config/telas/demo/h0055_dois_niveis_por_foco.json`; o teste recebeu somente a
evidência correspondente. A medição no fluxo real demonstra que 5 é o menor
teto suficiente: máximo 3 deixa piso aproximado W=40 e não alcança
intermediário/5; máximo 4 chega a aproximadamente W=35 e não alcança 5;
máximo 5 chega a aproximadamente W=24 e alcança máximo/intermediário/mínimo.
Máximos 6/7 não trazem benefício relevante adicional.

No mesmo estado lógico, sem reconstrução da tela, o quadro real percorre
80 → 36 → 32 e produz tabulação 10 → 9 → 5, sem `erro_layout` antecipado.
Em W=90 e W=80 a barra permanece em uma linha; o teto 5 não força cinco
linhas. Permanecem A), o sufixo estrutural `)`, pai/filho lógico, foco,
cursor, seleção, identidade e apresentação texto. O conteúdo externo H-0055
segue byte-a-byte preservado. A correção usa a política genérica, sem política
especial de tabulação para texto.

## VM-H0073-002 — H-0063 / ANSI

Nos pontos causais de `_aplicar_indicador_linhas` não há mais corte bruto:
ambos usam `_cortar_sem_ansi`. `_tokens_ansi` não emite CSI incompleto;
truncamento com SGR ativo fecha foreground/background, e
`_quebrar_texto` usa `_quebrar_sem_ansi`, que fecha cada linha e reabre o
estilo somente quando a região continua. O chip “Destaque Fundo” mantém seu
fundo 44 e reset 49; padding, coluna seguinte, linha seguinte, regiões
superior/inferior e restante do quadro ficam neutros.

O caso regressivo equivalente a W=50 prova o quadro real H-0063 via
`renderizar_estado`/resize: o fatiamento anterior podia devolver `\x1b[49`
e deixar 44 ativo; a saída atual mantém o CSI íntegro, neutraliza o estado e
o quadro subsequente não herda o fundo. Não é apenas teste de helper.

Tabulação dinâmica, designador ausente, preset, título, cor/amostra,
alinhamento global, identidade lógica, navegação e seleção permanecem; a
evidência real marca `H0063_ESPACAMENTO_COLUNAS_3_8: PRESERVADO`.

## Escopo e preservações

P05 atribui nominalmente a configuração H-0055, os três renderizadores
(`matriz_participantes.py`, `texto_ansi.py`, `conteudo_externo.py`), os dois
testes demo reconciliados, `tela/teste_estilo_h0073_h0063.py` e seu relatório.
P06 atribui somente a configuração H-0055 (campo `linhas.maximo`), a evidência
necessária em `demo/teste_demo_h0073_h0055_reconciliado.py` e seu relatório.
H-0055 conteúdo, H-0063, H-0062, preset, ADR, contratos, handoffs,
nomenclatura e teste H-0070 não receberam delta atribuído a P05/P06.

## Testes e classificação

Focais: **168 passed**. H-0070: **1 failed**, `index("→") == 2` contra
esperado `>= 4`; é `FALHA_HISTORICA_NAO_CAUSAL`, fora do escopo causal P05/P06.
Suíte canônica: **1460 passed, 1 failed**, somente H-0070.

Achados materiais: nenhum. Ambos ficam **PRONTO_PARA_REVALIDACAO** manual TTY.
\n