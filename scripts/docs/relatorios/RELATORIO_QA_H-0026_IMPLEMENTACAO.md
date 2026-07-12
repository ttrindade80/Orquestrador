# RELATORIO_QA_H-0026_IMPLEMENTACAO

## 1. Identificacao da etapa

Etapa executada: `QA_IMPLEMENTACAO`.

Papel: auditor formal da implementacao do H-0026, sem correcao de codigo, sem
alteracao de testes, sem alteracao do handoff, sem alteracao do relatorio de
implementacao, sem stage, sem commit e sem push.

Arquivo autorizado para escrita nesta etapa:

```text
docs/relatorios/RELATORIO_QA_H-0026_IMPLEMENTACAO.md
```

Antes da criacao foi confirmado:

```text
test ! -e docs/relatorios/RELATORIO_QA_H-0026_IMPLEMENTACAO.md
resultado: exit 0
```

## 2. Artefato auditado

Handoff auditado:

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
```

Implementacao auditada:

```text
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
tela/renderizador.py
tela/teste_renderizador.py
```

Status informado pelo executor: `IMPLEMENTATION_COMPLETED`.

## 3. Branch e commit-base

```text
branch: master
commit-base: 1cc0dff feat: implementa distribuicao vertical explicita do corpo
```

## 4. Estado Git inicial

Comandos obrigatorios executados no inicio deste QA:

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git status --short` | 2 alteracoes rastreadas, 6 entradas nao rastreadas |
| `git diff --stat` | `renderizador.py` e `teste_renderizador.py`, 556 insercoes, 16 remocoes |
| `git diff --name-only` | `scripts/tela/renderizador.py`, `scripts/tela/teste_renderizador.py` |
| `git diff --cached --stat` | sem saida |
| `git diff --cached --name-only` | sem saida |
| `git diff --check` | sem saida, exit 0 |

Alteracoes rastreadas fora do stage:

```text
M tela/renderizador.py
M tela/teste_renderizador.py
```

Alteracoes no stage: nenhuma.

Arquivos nao rastreados:

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0026_HANDOFF.md
tela/__pycache__/
```

Caches e temporarios: `tela/__pycache__/`.

Arquivos adicionais nao esperados: nenhum.

Divergencias da referencia: nenhuma material; o estado real coincide com o estado
esperado para este QA.

## 5. Arquivos rastreados alterados

Somente:

```text
tela/renderizador.py
tela/teste_renderizador.py
```

`git diff --numstat`:

```text
75	13	scripts/tela/renderizador.py
481	3	scripts/tela/teste_renderizador.py
```

## 6. Arquivos nao rastreados

O relatorio `IMP-0027` e o unico artefato novo criado pela implementacao. Os
demais nao rastreados correspondem ao handoff, levantamento, QAs do handoff e
cache esperados.

## 7. Autoridades consultadas

Foram consultadas as secoes aplicaveis de:

```text
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

Referencias historicas de preservacao vertical:

```text
docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

Regras confirmadas: arranjo horizontal reparte largura quando ha distribuicao
explicita, `percentual` e `fracao` sao genericos, valores se associam por ordem
declarada, maiores restos preservam soma exata e empatam pelo menor indice,
bordas horizontais ficam em contato e a ausencia de `distribuicao` nao equivale
a modo `igual`.

## 8. Handoff e QAs consultados

Lidos:

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0026_HANDOFF.md
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
```

O QA pos-patch do handoff concluiu `H1_HANDOFF_READY_FOR_IMPLEMENTATION`.

## 9. Metodologia

Foram inspecionados estado Git, diff real, relatorio de implementacao, handoff,
QAs do handoff, levantamento, autoridades normativas, codigo resultante, testes
alterados e arquivos de preservacao (`loader`, `modelo`, suites de regressao).
Os testes foram executados independentemente na ordem exigida, com
`PYTHONDONTWRITEBYTECODE=1`. Nenhum arquivo foi alterado alem deste relatorio.

## 10. Resumo do diff

Em `tela/renderizador.py`:

- adicionado helper local `_distribuir_larguras` em `tela/renderizador.py:257`;
- `_montar_corpo_horizontal` passou a aceitar `larguras=None` em
  `tela/renderizador.py:791`;
- o caminho uniforme sem distribuicao permanece em `tela/renderizador.py:823-831`;
- a concatenacao horizontal sem separador permanece em `tela/renderizador.py:892-902`;
- o ramo horizontal consulta `modelo.corpo.distribuicao` e calcula larguras em
  `tela/renderizador.py:1015-1054`.

Em `tela/teste_renderizador.py`:

- importado `_distribuir_larguras`;
- atualizado `test_arranjo_horizontal_nao_regride_com_distribuicao` em
  `tela/teste_renderizador.py:3765-3824`;
- criada `TestDistribuicaoHorizontalH0026` em `tela/teste_renderizador.py:3853`,
  com 16 metodos de teste reais.

## 11. Analise do escopo positivo

Conforme. A implementacao limita a capacidade ao corpo raiz horizontal com
`corpo.distribuicao` declarada. O calculo reparte `total_w` entre filhos diretos
por pesos derivados de `percentual` ou `fracao`, antes da renderizacao, preserva
a ordem declarada e passa uma largura por filho para `_montar_corpo_horizontal`.

## 12. Analise do escopo negativo

Conforme. Nao houve alteracao relacionada a `grupo.arranjo = "horizontal"`, nem
remocao da barreira do loader (`tela/loader.py:227-251`), nem composicao em tres
niveis, nem outros arranjos, nem politica de conteudo maior que a cota, nem ADR,
contrato, JSON, barra de menus, dashboard, console, lancador ou API publica nova.

`tela/loader.py`, `tela/modelo.py`, `tela/teste_loader.py`,
`tela/teste_modelo.py` e `tela/teste_demo.py` nao possuem diff.

## 13. Analise do helper de larguras

Conforme. `_distribuir_larguras` e local a `renderizador.py`, independente de
`_distribuir_alturas`, nao altera API publica e replica o algoritmo de maiores
restos:

- retorna `[]` para lista vazia;
- rejeita defensivamente soma de pesos nao positiva;
- calcula `ideais = largura_disponivel * p / soma`;
- usa `int(x)` como floor para valores nao negativos;
- calcula `faltam = largura_disponivel - sum(cotas)`;
- ordena restos por `(-resto, indice)`;
- distribui exatamente `faltam` colunas;
- produz uma largura por filho e soma final igual a `largura_disponivel`.

A defesa para entradas impossiveis nao cria semantica concorrente com o loader;
ela segue o padrao ja existente do helper vertical.

## 14. Analise percentual

Conforme. Para `percentual`, `_pesos_distribuicao` devolve os valores declarados
e `_distribuir_larguras` usa a soma 100 validada pelo loader, resultando em:

```text
cota ideal = total_w * percentual / 100
```

Casos verificados nos testes:

- `[50, 50]`, `total_w=42` -> `[21, 21]`;
- `[60, 40]`, `total_w=42` -> `[25, 17]`;
- soma final exata;
- associacao posicional por titulo/ordem dos filhos.

## 15. Analise fracionaria

Conforme. Para `fracao`, o denominador e a soma dos pesos:

```text
cota ideal = total_w * peso / soma_dos_pesos
```

Casos verificados:

- `[1, 1]` -> `[21, 21]`;
- `[2, 1]` -> `[28, 14]`;
- `[4, 2]` equivale a `[2, 1]`;
- tres filhos com `[1, 1, 1]`;
- larguras nao divisiveis com soma final exata.

## 16. Analise de maiores restos

Conforme. O algoritmo faz floor deterministico, calcula restantes e distribui
por restos decrescentes com desempate pelo menor indice. Nao foram identificadas
perda de colunas, coluna externa ou largura negativa nas entradas validadas pelo
loader.

## 17. Analise de T06 e T07

Conforme.

T06:

```text
modo: fracao
valores: [1, 1, 1]
total_w: 100
resultado: [34, 33, 33]
```

T07:

```text
modo: fracao
valores: [1, 1, 1]
total_w: 101
partes inteiras iniciais: [33, 33, 33]
colunas restantes: 2
restos: empatados
posicoes favorecidas: 0 e 1
resultado: [34, 34, 33]
soma final: 101
```

## 18. Analise da integracao horizontal

Conforme. O ramo horizontal em `tela/renderizador.py:1018-1054`:

- consulta `distribuicao_corpo = modelo.corpo.distribuicao`;
- calcula `_l_corpo_disponivel` antes da montagem quando ha altura explicita;
- calcula `pesos_corpo` via `_pesos_distribuicao`;
- calcula `larguras_corpo` via `_distribuir_larguras(total_w, pesos_corpo)`;
- passa `larguras=larguras_corpo` para `_montar_corpo_horizontal`;
- preserva o caminho separado sem distribuicao com `larguras_corpo = None`.

## 19. Analise da ausencia

Conforme. Quando `corpo.distribuicao is None`, o caminho segue
`tela/renderizador.py:823-831`, com particionamento uniforme operacional
preexistente. O patch nao transforma ausencia em distribuicao explicita e este
QA nao interpreta esse comportamento como redefinicao normativa da ausencia.

## 20. Analise da preservacao vertical

Conforme. `_distribuir_alturas` permanece funcionalmente intacto em
`tela/renderizador.py:219-254`; o ramo vertical permanece separado em
`tela/renderizador.py:1057` em diante; os testes H-0025 continuam presentes e
foram executados dentro de `teste_renderizador.py`. A nova logica horizontal nao
interfere na altura.

## 21. Analise visual e estrutural

Conforme. Os testes e o codigo comprovam:

- contato entre bordas horizontais (`╮╭`, `╯╰`, `││`);
- ausencia de coluna externa entre filhos;
- largura total preservada;
- margens e molduras preservadas;
- preenchimento interno quando conteudo e menor que a cota;
- ordem dos filhos preservada;
- nenhuma politica nova de recorte ou overflow horizontal.

## 22. Auditoria dos testes adicionados

`TestDistribuicaoHorizontalH0026` possui 16 metodos reais:

```text
test_algoritmo_distribuir_larguras_soma_exata
test_algoritmo_distribuir_larguras_exemplos_normativos
test_percentual_simetrico_50_50
test_percentual_assimetrico_60_40
test_fracao_simetrico_1_1
test_fracao_assimetrico_2_1
test_fracao_equivalencia_por_escala
test_t06_maiores_restos_largura_100
test_t07_empate_restos_resolvido_por_ordem_declarada
test_t08_soma_larguras_igual_distribuivel
test_t09_bordas_em_contato
test_t10_largura_total_preservada
test_t11_preenchimento_interno_conteudo_menor_que_cota
test_ausencia_distribuicao_preserva_uniforme
test_distribuicao_vertical_h0025_nao_regride
test_rejeicoes_loader_preservadas
```

Os asserts sao exatos para larguras e somas, os casos sao independentes, as
fixtures sao coerentes com o handoff e nao foram identificados testes duplicados
sem valor. A contagem do renderizador subiu para 434 verificacoes, sem reducao.

## 23. Auditoria do teste historico atualizado

Conforme. `test_arranjo_horizontal_nao_regride_com_distribuicao` deixou de
documentar que a distribuicao horizontal e ignorada e passou a verificar
larguras reais para `fracao [1, 1]` em `total_w=42`, mantendo renderizacao sem
erro, bordas coladas e largura total.

## 24. Tabela de rastreabilidade dos testes

| Teste | Requisito do handoff | Resultado esperado | Cobertura real | Situacao |
| ----- | -------------------- | ------------------ | -------------- | -------- |
| T01 | Percentual `[50,50]` | `[21,21]`, soma 42, `╮╭` | `test_percentual_simetrico_50_50` | Conforme |
| T02 | Percentual assimetrico | `[25,17]`, soma 42 | `test_percentual_assimetrico_60_40` | Conforme |
| T03 | Fracao `[1,1]` | `[21,21]`, soma 42 | `test_fracao_simetrico_1_1` | Conforme |
| T04 | Fracao `[2,1]` | `[28,14]`, soma 42 | `test_fracao_assimetrico_2_1` | Conforme |
| T05 | Equivalencia por escala | `[2,1] == [4,2]` e `[28,14]` | `test_fracao_equivalencia_por_escala` | Conforme |
| T06 | Maiores restos em 100 | `[34,33,33]` | helper e render em `test_t06_maiores_restos_largura_100` | Conforme |
| T07 | Empate em 101 | `[34,34,33]` | helper e render em `test_t07_empate_restos_resolvido_por_ordem_declarada` | Conforme |
| T08 | Soma exata | `sum(larguras) == total_w` | 6 fixtures em `test_t08_soma_larguras_igual_distribuivel` | Conforme |
| T09 | Bordas em contato | `╮╭`, `╯╰`, `││` | `test_t09_bordas_em_contato` | Conforme |
| T10 | Largura total | todas as linhas com 42 chars | `test_t10_largura_total_preservada` | Conforme |
| T11 | Preenchimento interno | cota preenchida ate a borda | `test_t11_preenchimento_interno_conteudo_menor_que_cota` | Conforme |
| T-NR01 | Ausencia sem regressao | uniforme preservado | `test_ausencia_distribuicao_preserva_uniforme` | Conforme |
| T-NR02 | Vertical H-0025 | exemplos verticais preservados | `test_distribuicao_vertical_h0025_nao_regride` e suite H-0025 | Conforme |
| T-NR03 | Rejeicoes loader | percentual invalido e peso zero rejeitados | `test_rejeicoes_loader_preservadas` e `teste_loader.py` | Conforme |
| Historico | Teste antigo atualizado | larguras reais com `fracao [1,1]` | `test_arranjo_horizontal_nao_regride_com_distribuicao` | Conforme |

## 25. Testes executados e resultados

Com cache antes:

```text
__init__.cpython-314.pyc
loader.cpython-314.pyc
modelo.cpython-314.pyc
renderizador.cpython-314.pyc
```

Resultados independentes:

| Comando | Saida resumida | Verificacoes | Resultado | Exit |
|---|---|---:|---|---:|
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py` | `Total de verificacoes: 105; Passaram: 105; Falharam: 0` | 105 | passou | 0 |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py` | `Total de verificacoes: 58; Passaram: 58; Falharam: 0` | 58 | passou | 0 |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py` | `Total de verificacoes: 434; Passaram: 434; Falharam: 0` | 434 | passou | 0 |
| `PYTHONDONTWRITEBYTECODE=1 python tela/teste_demo.py` | `Total de verificacoes: 303; Passaram: 303; Falharam: 0` | 303 | passou | 0 |

Divergencia frente ao `IMP-0027`: nenhuma.

Cache depois:

```text
__init__.cpython-314.pyc
loader.cpython-314.pyc
modelo.cpython-314.pyc
renderizador.cpython-314.pyc
```

`PYTHONDONTWRITEBYTECODE=1` evitou novos arquivos `.pyc` observaveis nessa lista.

## 26. Comparacao com o IMP-0027

Conforme. O `IMP-0027` registra handoff executado, QA pos-patch do handoff,
arquivos alterados, abordagem tecnica, percentual, fracao, maiores restos,
desempate, integracao horizontal, preservacao da ausencia, preservacao vertical,
testes adicionados, teste historico atualizado, comandos, contagens, estado Git,
nao rastreados, itens fora de escopo, ausencia de commit e ausencia de QA proprio.

Nao foi localizada declaracao material sem suporte no diff ou nos testes reais.

## 27. Estado Git final

Antes da criacao deste relatorio, o estado final da implementacao auditada era:

```text
branch: master
commit: 1cc0dff feat: implementa distribuicao vertical explicita do corpo
stage: vazio
diff rastreado: tela/renderizador.py, tela/teste_renderizador.py
```

Depois da criacao deste relatorio, espera-se uma entrada nao rastreada adicional
para `docs/relatorios/RELATORIO_QA_H-0026_IMPLEMENTACAO.md`. O stage permanece
vazio.

## 28. Validacao manual

```text
validacao_manual: nao necessaria para esta capacidade
```

Justificativa: os criterios do H-0026 sao deterministicos e cobertos por
renderizacao textual e testes automatizados. A pendencia historica de validacao
humana TTY real exibida por `teste_demo.py` pertence a comportamento TUI de outro
ciclo e nao e requisito material desta capacidade de distribuicao horizontal.

## 29. Achados numerados

### H0026-IMPL-QA-O01

- Severidade: observacao.
- Arquivo e linha: `tela/teste_demo.py` saida da suite, bloco "Validacao humana TTY real: PENDENTE".
- Requisito do handoff ou autoridade: H-0026 secao de validacao manual; validar TTY real somente se for objetivamente necessario para esta capacidade.
- Evidencia: `teste_demo.py` passou 303/303 e imprimiu pendencia TTY historica; os testes H-0026 passaram em `teste_renderizador.py`.
- Descricao objetiva: existe pendencia textual de validacao humana TTY real em suite de demo, mas ela nao incide sobre a distribuicao horizontal percentual/fracionaria do corpo.
- Impacto: sem impacto bloqueante para H-0026.
- Categoria da causa: observacao sem correcao necessaria.
- Proxima categoria aplicavel: `VERIFICAR_FECHAMENTO`.

Nao ha achados bloqueantes, altos, medios ou baixos.

## 30. Conclusao

A implementacao corresponde integralmente ao H-0026. O escopo positivo foi
implementado no renderizador, o escopo negativo foi preservado, loader/modelo e
documentos normativos nao foram alterados, os testes independentes passaram, o
relatorio `IMP-0027` corresponde ao diff real e nao ha validacao manual
obrigatoria para esta capacidade.

## 31. Status final unico

```text
I1_IMPLEMENTATION_APPROVED
```

## 32. Lista do unico arquivo criado ou alterado por esta etapa

```text
docs/relatorios/RELATORIO_QA_H-0026_IMPLEMENTACAO.md
```
