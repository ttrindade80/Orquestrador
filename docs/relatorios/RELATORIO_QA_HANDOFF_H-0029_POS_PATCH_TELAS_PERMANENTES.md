# QA do handoff H-0029 apos patch de telas permanentes

## 1. Identificacao

```yaml
ciclo: H-0029
tipo: QA_HANDOFF
objeto_auditado: scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
patch_auditado: PATCH_HANDOFF_TELAS_PERMANENTES_2026-07-12
estado_recebido: HANDOFF_PATCHED
auditor: Codex
```

Esta auditoria avaliou exclusivamente o handoff corrigido apos a autorizacao
documental de sete telas JSON permanentes para reproducao, testes de integracao
e validacao visual.

Nao foram corrigidos handoff, codigo, testes ou JSONs. Nao foi executada
implementacao, validacao visual, stage ou commit. A unica escrita desta etapa e
este relatorio.

## 2. Arquivos e autoridades consultadas

Leitura integral obrigatoria realizada:

- `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`;
- `scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md`.

Autoridades ativas consultadas nos pontos necessarios:

- `scripts/docs/contratos/contrato_composicao_corpo.md`: composicao do corpo,
  grupos, ausencia de distribuicao, distribuicao explicita, modos `igual`,
  `fracao` e `percentual`, filhos diretos e preservacao de `barra_de_menus`;
- `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`:
  grupo estrutural, distribuicao por container e preenchimento de area alocada;
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`:
  ausencia de distribuicao nao equivale a `igual`;
- `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`:
  cardinalidade e grupos hierarquicos;
- `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`:
  preservacao de `estrutura: livre`, matriz fora do escopo e independencia entre
  distribuicoes;
- `scripts/tela/demo.py` e `scripts/tela/loader.py`, somente para verificar a
  interface real de carregamento por identificador.

## 3. Estado Git

Conferencia executada na raiz Git real:

```text
git rev-parse --show-toplevel
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

```text
git status --short
 M scripts/tela/renderizador.py
 M scripts/tela/teste_renderizador.py
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

```text
git diff --check
sem saida; codigo 0
```

`git diff --name-only` listou apenas:

```text
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

Nao foram observados arquivos `scripts/config/telas/h0029_*.json` no estado
inicial desta auditoria. Portanto, o patch documental do handoff nao produziu
arquivos de tela adicionais nesta etapa.

## 4. Coerencia interna do handoff corrigido

O patch incorporou uma secao nominal `11A. Telas permanentes autorizadas`, incluiu
os sete JSONs em `Arquivos autorizados`, adicionou testes nominais na secao 12.2,
detalhou uso pelo `demo.py` na secao 16A, acrescentou formulario de validacao
manual na secao 16B e incluiu as telas na lista acumulada do ciclo.

Nao foi encontrada proibicao generica `h0029_*` concorrente que torne impossivel
criar as sete telas. A secao de arquivos proibidos contem excecao explicita para
os sete `config/telas/h0029_*.json`.

Ha, porem, uma contradicao material remanescente: a secao 10 ainda permite alterar
`config/telas/grupo_minimo.json` em uma excecao restrita, enquanto a nova secao
11A exige construir as telas a partir de `destino_minimo.json` e `grupo_minimo.json`
sem alterar os arquivos usados como referencia. Essa excecao tambem conflita com
o objetivo pos-patch de limitar a futura implementacao aos sete JSONs, testes,
relatorio e renderer somente se uma falha reproduzida exigir nova correcao.

## 5. Escopo nominal das sete telas

As sete telas autorizadas nominalmente sao:

- `h0029_dashboard_igual.json`;
- `h0029_dashboard_fracao.json`;
- `h0029_dashboard_percentual.json`;
- `h0029_grupo_pai_distribuido.json`;
- `h0029_grupo_igual.json`;
- `h0029_grupo_fracao.json`;
- `h0029_grupo_percentual.json`.

O handoff mantem fora do H-0029: telas 2x2, 3x2 e 2x4, catalogo geral de telas,
integracao ao lancador, alteracao de `orquestrador.json`, console unico fora das
fixtures nominais, dashboard unico fora das fixtures nominais, navegacao,
selecao, execucao de acoes, carregamento de conteudo de JSON de testes, ADRs,
contratos, nomenclatura, indices, commit e alteracao de historico Git.

A limitacao nominal nao esta perfeita porque `grupo_minimo.json` permanece
alteravel por excecao. Isso nao autoriza uma oitava tela `h0029_*`, mas autoriza
alteracao declarativa fora dos sete JSONs permanentes.

## 6. Especificacao declarativa dos JSONs

Para cada tela, o handoff define caminho nominal, `id`, estrutura do corpo,
modo e valores de distribuicao, resultado geometrico esperado e preservacao de
cabecalho e `barra_de_menus`. Define tambem que as telas devem ser construidas
a partir de `destino_minimo.json` nos cenarios de dashboard direto e de
`grupo_minimo.json` nos cenarios com grupo.

O executor nao precisa escolher nome de arquivo, identificador, modo de
distribuicao, vetor de valores, quantidade de filhos diretos, tipo dos filhos ou
resultado geometrico esperado. O texto visivel nao e literalizado campo a campo,
mas o handoff exige `cabecalho.titulo` e `cabecalho.descricao` capazes de
identificar claramente cada cenario; isso e implementavel sem decisao
arquitetural nova.

A proibicao de alterar os JSONs de referencia existe na secao 11A, mas fica
enfraquecida pela excecao remanescente de `grupo_minimo.json` na secao 10.

## 7. Cenarios de cardinalidade unitaria

### Dashboard direto

O handoff exige equivalencia geometrica entre:

- `h0029_dashboard_igual`;
- `h0029_dashboard_fracao`;
- `h0029_dashboard_percentual`.

Cada tela contem um unico `dashboard` direto no corpo, com distribuicao explicita
no corpo, e deve ocupar toda a area distribuivel entre cabecalho e
`barra_de_menus`.

### Grupo sem distribuicao interna

Para `h0029_grupo_pai_distribuido`, o handoff distingue corretamente:

- corpo com `fracao [1]`;
- unico filho direto do corpo e um grupo;
- grupo sem distribuicao propria;
- dashboard interno permanece em altura natural;
- sobra pertence a area estrutural do grupo;
- altura total e posicao da barra permanecem corretas;
- nao se exige que a borda inferior do dashboard encoste na `barra_de_menus`.

Esse caso nao e confundido com os cenarios de distribuicao nos dois niveis.

### Distribuicao nos dois niveis

O handoff exige equivalencia geometrica entre:

- `h0029_grupo_igual`;
- `h0029_grupo_fracao`;
- `h0029_grupo_percentual`.

Nesses casos, o corpo distribui para o grupo, o grupo distribui para o dashboard,
e a borda inferior do dashboard deve ficar imediatamente antes da
`barra_de_menus`.

## 8. Testes automatizados e geometria

A secao 12.2 exige testes nominais para cada um dos sete arquivos reais
`h0029_*`, carregados pelo loader. A cobertura exigida inclui validade sintatica,
loader, modelo, estrutura declarada, distribuicao em cada nivel, renderizacao
com largura e altura fixas, altura total, largura uniforme, posicao da barra,
posicao da borda inferior nos cenarios distribuidos, altura natural no caso sem
distribuicao interna, ausencia de sobreposicao, ausencia de lacuna indevida,
equivalencia geometrica entre modos e mais de uma altura de terminal.

O handoff explicita que nao basta verificar somente a quantidade total de linhas.
Tambem exige regressao da suite canonica.

## 9. Execucao pelo demo.py

O handoff exige inspecao integral da interface real de `tela/demo.py`, verificacao
de suporte ou ausencia de argumentos CLI para tela inicial, e registro de comando
exato para abrir cada uma das sete telas pelo pipeline real, sem modificar
`demo.py`, sem integrar as telas ao lancador e sem editar JSONs manualmente.

A consulta ao codigo confirma que `demo.py` carrega modelos por identificador via
`_carregar_modelo_por_id(id_tela)`, que chama `carregar_tela(None, id_tela)` e
`construir_modelo`. O `main()` usa o estado inicial e nao apresenta interface CLI
direta para selecionar tela inicial. O handoff lida com isso ao exigir que o
executor documente explicitamente o que a interface suporta e o que nao suporta.

## 10. Validacao manual

A secao 16B exige validacao humana em TTY real para as sete telas, com formulario
separado contendo:

```yaml
tela:
carregou:
altura_total_correta:
barra_de_menus_na_posicao_correta:
borda_inferior_do_dashboard:
lacuna_indevida:
sobreposicao:
resultado:
```

O handoff preserva:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

ate que o usuario execute os cenarios. O executor e o auditor nao podem declarar
aprovacao visual.

## 11. Arquivos permitidos e proibidos

A futura implementacao fica quase limitada ao escopo esperado: sete JSONs
autorizados, testes pertinentes, relatorio de implementacao e `renderizador.py`
somente no caso delimitado de falha reproduzida ou correcao necessaria dentro do
mesmo escopo.

Permanecem preservados por regra geral:

- `destino_minimo.json`;
- `stub_b.json`;
- `orquestrador.json`;
- contratos;
- ADRs;
- nomenclatura;
- funcionalidades futuras do console.

O ponto nao conforme e `grupo_minimo.json`: o handoff o declara como referencia
para os JSONs de grupo e proibe alterar os arquivos usados como referencia, mas
ainda preserva uma excecao que permite altera-lo se considerado indispensavel
para teste de integracao. Essa autorizacao residual deve ser removida ou
reescrita para leitura apenas no escopo pos-patch.

## 12. Implementabilidade

Um executor em contexto limpo consegue implementar as sete telas e seus testes sem
inventar estrutura, nomes, modos, valores, cenarios ou semantica nova. Tambem
consegue registrar comandos de validacao sem integrar as telas ao lancador e sem
presumir aprovacao visual.

Contudo, o handoff ainda permite uma decisao de escopo indesejada: alterar ou nao
`grupo_minimo.json` sob a excecao da secao 10. Essa permissao e incompatavel com
o objetivo pos-patch de preservar os JSONs de referencia e autorizar somente os
sete novos JSONs permanentes. Portanto, o handoff corrigido ainda requer patch
documental antes de ser aprovado como H1.

## 13. Achados

```yaml
id: ACH-H0029-PP-001
severidade: alto
local: scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md, secoes 10, 11 e 11A
regra_ou_autoridade: escopo nominal pos-patch; preservacao de JSONs de referencia; contrato de ausencia de distribuicao
problema: A secao 10 ainda autoriza alterar config/telas/grupo_minimo.json em excecao restrita, enquanto a secao 11A manda usar grupo_minimo.json como referencia sem alterar os arquivos de referencia.
impacto: O handoff nao autoriza de forma inequivoca somente os sete JSONs permanentes. Um executor em contexto limpo ainda pode entender que ha permissao para modificar um JSON real de referencia fora do novo escopo nominal.
correcao_necessaria: Remover a excecao de alteracao de grupo_minimo.json ou reescreve-la como leitura obrigatoria/preservacao explicita, mantendo alteraveis apenas os sete h0029_*.json, testes pertinentes, relatorio e renderer somente diante de falha reproduzida delimitada.
```

```yaml
id: OBS-H0029-PP-001
severidade: observacao
local: estado Git e scripts/config/telas/
regra_ou_autoridade: patch declarado; conferencia inicial do QA
problema: Nenhum dos sete arquivos h0029_*.json existe ainda.
impacto: Coerente com o patch declarado, que era documental. Confirma que nao houve criacao de arquivos adicionais nesta etapa.
correcao_necessaria: Nenhuma nesta etapa.
```

```yaml
id: OBS-H0029-PP-002
severidade: observacao
local: scripts/tela/demo.py e handoff secao 16A
regra_ou_autoridade: interface real de carregamento por identificador
problema: demo.py nao expoe argumento CLI direto para escolher a tela inicial; o carregamento por id existe internamente por _carregar_modelo_por_id e pelo loader.
impacto: Nao bloqueia o handoff, pois a secao 16A exige que o executor inspecione essa interface e documente explicitamente o mecanismo real e a ausencia de CLI, sem integrar as telas ao lancador.
correcao_necessaria: Nenhuma obrigatoria para o handoff; o executor deve registrar comandos factuais no relatorio de implementacao.
```

## 14. Classificacao final

```text
H2_HANDOFF_PATCH_REQUIRED
```

Justificativa: o patch resolve a lacuna principal de reproducibilidade ao
autorizar nominalmente as sete telas permanentes, testes nominais, comandos de
uso pelo pipeline real e validacao manual humana. Entretanto, a excecao
remanescente para alterar `grupo_minimo.json` contradiz a preservacao dos JSONs
de referencia e impede concluir que somente os sete JSONs permanentes estao
autorizados.

## 15. Proxima categoria permitida

```text
PATCH_HANDOFF
```

Resumo de saida:

```text
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: HANDOFF_PATCH_REQUIRED
relatorio: scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
handoff_auditado: scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
achados_bloqueantes: 0
achados_altos: 1
achados_medios: 0
achados_baixos: 0
observacoes: 2
sete_telas_autorizadas: nao_integralmente_por_excecao_remanescente_em_grupo_minimo_json
testes_nominais_suficientes: sim
demo_py_especificado: sim
validacao_manual_especificada: sim
estado_git: diff_check_sem_saida; renderizador_e_teste_renderizador_modificados_preexistentes; handoff_e_relatorios_nao_rastreados; sete_jsons_h0029_ainda_ausentes
proxima_categoria: PATCH_HANDOFF
arquivos_alterados: scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
```
