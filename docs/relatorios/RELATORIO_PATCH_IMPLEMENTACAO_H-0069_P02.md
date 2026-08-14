# Relatório de patch de implementação — H-0069 P02

```yaml
rastreabilidade:
  etapa: PATCH_IMPLEMENTACAO
  objeto: H-0069
  patch: P02
  cadeia:
    raiz: docs/relatorios/IMP-0069-demonstracao-integrada-override-local-estilo.md
    predecessor_imediato: docs/relatorios/RELATORIO_VALIDACAO_MANUAL_H-0069.md
  achado_tratado: MV-A1-CRASH-CONFIRMADO

resultado:
  status: IMPLEMENTATION_PATCHED
  hipotese: CONFIRMADA
  crash_reproduzido_antes_da_correcao: true
  causa_confirmada: >
    Apos CONFIRMADO, tela_atual permanece H-0063 e o loop reobtem o modelo
    via _modelo_corrente. O modelo local ainda era o da demonstracao, entao
    a API recarregava o shell H-0063 sem _preparar_modelo_estilo. O console
    dois_niveis_por_foco chegava com conteudo_externo=None; _estado_estilo_
    observavel chamava em_nivel_filhos e crashava.
  crash_pos_correcao: ausente
  modelo_pos_confirmado: h0063_estilo_estrutura_navegacao_dois_niveis
  tela_pos_confirmado: h0063_estilo_estrutura_navegacao_dois_niveis
  validacao_manual_H0069: REVALIDACAO_OBRIGATORIA_APOS_QA_P02
  validacao_manual_final_ITEM0010: OBRIGATORIA
```

## Diagnostico factual (antes da escrita)

Percurso reproduzido non-TTY, equivalente ao TTY: trocar borda → Aplicar →
popup → CONFIRMADO → avaliacao pos-comando de `demo.py:main`.

1. `estilo_antes` usa o modelo do loop, ja resolvido por `_modelo_corrente`
   enquanto a sessao H-0069 esta aberta: `h0069_estilo_demonstracao_integrada`.
2. `processar_comando` recebe esse mesmo modelo H-0069.
3. Depois de CONFIRMADO: `tela_atual` permanece H-0063; sessao/origem/local
   removidas (A1); o modelo semanticamente corrente e o da tela Estilo.
4. A chamada posterior `_estado_estilo_observavel(estado, modelo)` ocorre
   depois de `modelo = _modelo_corrente(estado, modelo)`.
5. `_modelo_corrente` detecta o modelo H-0069 obsoleto e recarrega H-0063.
   O estado ja e o da tela Estilo; o objeto recarregado e o shell correto
   em ID, mas nao e o modelo preparado da tela Estilo.
6. `console_do_modelo` devolve `console_h0063_estilo`
   (`politica_navegacao.tipo = dois_niveis_por_foco`).
7. `conteudo_externo` e `None` porque H-0063 nao esta em
   `_CATALOGO_CONTEUDO_EXTERNO`; o conteudo de dois niveis e associado em
   runtime por `_preparar_modelo_estilo`. O loop so chama essa preparacao
   quando `tela_atual` muda, o que CONFIRMADO/ABORTADO nao fazem.

A hipotese transportada confirma-se neste sentido: a avaliacao pos-comando
misturava estado pos-CONFIRMADO da tela Estilo com um shell H-0063
incompativel com a premissa de navegacao em dois niveis. Nao era o modelo
H-0069 que entrava em `_indices_dois_niveis` (o console da demonstracao
nao e `dois_niveis_por_foco`).

## Correcao

Arquivos alterados: `demo/demo.py`, `demo/teste_demo_estilo_h0069.py`.
Arquivo criado: este relatorio. `teste_demo_estilo_h0068.py` nao precisou
de atualizacao.

Em `_modelo_corrente`, o ramo que recarrega H-0063 apos o overlay passar
a devolver `_preparar_modelo_estilo(shell, estado)`. A reobtencao ja
existia no loop; faltava a associacao de conteudo da API vigente. Sem
hardcode de IDs no `main`, sem tolerar `conteudo_externo=None`, sem
try/except, sem reter chave privada da tentativa.

## Teste do caminho manual

`test_confirmado_pos_comando_do_main_retorna_a_estilo_sem_crash` espelha o
recorte de `main`: observa estilo, processa Enter, reobtem modelo, observa
de novo. Prova ausencia de `AttributeError`, modelo pos-comando com
`conteudo_externo` associado, tela Estilo, candidato/baseline/global
coerentes com H-0068, Aplicar inativo, sessao H-0069 limpa.

`test_abortado_pos_comando_do_main_nao_quebra_nem_deixa_modelo_incompativel`
cobre o mesmo recorte pos-ABORTADO.

## A1 / A2 do P01

A1 permanece: ABORTADO e CONFIRMADO continuam sem
`_sessao_demonstracao_estilo`, `_modelo_origem_demonstracao_estilo` e
`estilo_demonstracao_local`.

A2 permanece: demonstracao e popup seguem materializados localmente com C;
nao houve retorno a G1. A invariavel geometrica do popup nao foi alterada
neste patch (caminho com sessao ainda aberta, ramo novo nao executado).

## Testes

- Novos/alterados H-0069: passaram.
- `tela/teste_estilo_h0069.py` + `demo/teste_demo_estilo_h0069.py`:
  17 passed / 0 failed.
- H-0068: 14 passed / 0 failed.
- Popup: 79 passed / 4 failed (chips/ANSI externos; nao tratados).
- Regressao H-0063–H-0069: 130 passed / 14 failed. As 13 falhas externas
  do preset Ponto (Ajuda/Voltar/Selecionar/Aplicar/Paginas ausentes no
  quadro) continuam. A 14ª e
  `test_borda_console_subjacente_preservada_fora_do_popup`, reproduzida
  em isolamento com sessao H-0069 ainda aberta — fora do ramo corrigido;
  nao atribuivel ao P02; chips/overlay permanecem fora de escopo.
- Suíte completa: 1246 passed / 82 failed / 19 errors.
  Baseline imediata ao P02: 1250 / 76 / 17. O delta (falhas/erros a mais)
  concentra-se em chips, barra, paginacao, popup e loaders ja afetados
  pelo preset Ponto no worktree. Nenhum teste H-0069 falhou. Nenhuma
  falha nova atribuivel a este patch.

`config/estilo.json` nao foi escrito. Stage vazio.
`git diff --check` limpo nos arquivos do P02.

Gates manuais pendentes: revalidacao TTY de H-0069 apos QA P02; validacao
manual final do ITEM-0010.
