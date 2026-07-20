---
name: RELATORIO_QA_H-0037_IMPLEMENTACAO
description: Auditoria independente da implementacao do H-0037
handoff: H-0037
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: REPROVADO_PATCH_NECESSARIO
proxima_categoria: PATCH_IMPLEMENTACAO
---

# Relatorio de QA da implementacao do H-0037

## 1. Identificacao

| Campo | Valor |
|---|---|
| Projeto | Orquestrador |
| Etapa executada | QA_IMPLEMENTACAO |
| Handoff | `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| QA do handoff | `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0037_HANDOFF.md` (`H1_HANDOFF_APPROVED`) |
| Relatorio de implementacao | `docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md` |
| Resultado | `IMPLEMENTATION_PATCH_REQUIRED` |

## 2. Objetivo

Auditar a implementacao do H-0037 contra o handoff aprovado, ADR-0028 D23,
contratos reaplicados, comportamento das quatro telas, testes, relatorio IMP e
estado Git. Nenhum codigo, teste, JSON, contrato ou handoff foi corrigido por
este QA.

## 3. Autoridades

Leitura obrigatoria considerada: H-0037, QA pos-patch do handoff, IMP-0037,
ADR-0028, contratos `contrato_json_console.md`, `contrato_console.md`,
`contrato_tela_json.md`, `contrato_barra_de_menus.md`,
`contrato_composicao_corpo.md`, `docs/NOMENCLATURA.md` e documentos H-0036 de
regressao.

Autoridades centrais aplicadas:

- `contrato_json_console.md` §13.13: D23 usa
  `formato.excesso.politica_modo` e `formato.excesso.modo_inicial` no JSON
  estrutural.
- `contrato_json_console.md` §13.13.3: ausencia de `politica_modo` em tela
  nova ou revisada e invalida; nao existe default implicito.
- ADR-0028 §33 e `contrato_json_console.md` §13.9: V-01 a V-15 possuem
  significados normativos especificos.
- `contrato_console.md` §21.11 e `contrato_barra_de_menus.md` §22.8: chip
  `[V] Verboso` e tecla `V` sao exclusivos de telas `alternavel`.

## 4. Estado Git

Comandos executados na raiz real do repositorio:

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
log_1: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
git_diff_check: sem_erros
```

Observacao de base de caminhos: o checkout atual ja e a base operacional que
contem `tela/`, `demo/`, `config/` e `docs/`. O comando literal `find scripts`
falhou com `No such file or directory`; a busca equivalente foi executada em
`.` e esta divergencia foi registrada.

## 5. Inventario

Arquivos rastreados modificados no diff real:

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

Arquivos H-0037 nao rastreados esperados: quatro JSONs estruturais, tres JSONs
de conteudo, `demo/teste_demo_console_modos.py` e `docs/relatorios/IMP-0037-*`.

Arquivos fora da lista nominal de implementacao: `docs/NOMENCLATURA.md`,
`docs/adr/INDICE_ADR.md`, contratos modificados e varios relatorios/ADR/handoff
nao rastreados acumulados. Nao atribuo automaticamente estes arquivos ao
executor da implementacao; eles parecem pertencer ao ciclo documental D23, mas
continuam fora do escopo tecnico nominal do H-0037.

Transitorios encontrados e nao removidos:

```text
tela/__pycache__/*
demo/__pycache__/*
```

## 6. Escopo

Arquivos autorizados alterados ou criados foram encontrados. Estado por grupo:

| Arquivo | Estado | Necessidade | Resultado |
|---|---|---|---|
| `tela/loader.py` | ALTERADO | D23 e V-01 a V-15 | Nao conforme, ver achados |
| `tela/modelo.py` | ALTERADO | transporte de politica/modo | Parcialmente conforme |
| `tela/renderizador.py` | ALTERADO | verboso/nao verboso, alinhamento e tabela | Parcialmente conforme |
| `demo/demo.py` | ALTERADO | catalogo, tecla V, modo efetivo | Nao conforme no modo inicial do cenario 4 |
| testes autorizados | ALTERADOS/CRIADOS | cobertura de regressao e H-0037 | Suite passa, mas ha testes semanticamente incorretos |
| JSONs H-0037 | CRIADOS | quatro telas e tres conteudos | Estrutura basica conforme |
| `docs/relatorios/IMP-0037-*` | CRIADO | relatorio de implementacao | Incompleto/incorreto em pontos materiais |

## 7. Integridade

```yaml
python_ast:
  tela/loader.py: VALIDO
  tela/modelo.py: VALIDO
  tela/renderizador.py: VALIDO
  tela/teste_loader.py: VALIDO
  tela/teste_modelo.py: VALIDO
  tela/teste_renderizador.py: VALIDO
  demo/demo.py: VALIDO
  demo/teste_demo.py: VALIDO
  demo/teste_diagnostico.py: VALIDO
  demo/teste_demo_console.py: VALIDO
  demo/teste_explorar_barra_de_menus.py: VALIDO
  demo/teste_demo_console_modos.py: VALIDO
json:
  demo.json: VALIDO
  h0037_console_nao_verboso.json: VALIDO
  h0037_console_verboso_dois_niveis.json: VALIDO
  h0037_console_alternavel_tres_niveis.json: VALIDO
  h0037_console_tabela_alternavel.json: VALIDO
  h0037_dois_niveis_conteudo.json: VALIDO
  h0037_tres_niveis_conteudo.json: VALIDO
  h0037_tabela_conteudo.json: VALIDO
conflitos_merge: AUSENTES
```

## 8. Schema D23

Conforme:

- os quatro JSONs H-0037 declaram `politica_modo` no JSON estrutural;
- `modo_inicial` aparece apenas nas duas telas `alternavel`;
- valores validos aceitos e valores desconhecidos rejeitados;
- `modo_inicial` em politica fixa rejeitado;
- `alternavel` sem `modo_inicial` rejeitado;
- conteudos externos nao possuem chaves `politica_modo` nem `modo_inicial`.

Nao conforme:

- `_validar_d23_console` aceita `politica_modo` ausente sempre que
  `modo_inicial` tambem esta ausente (`tela/loader.py:1410-1411`). Falta
  mecanismo para diferenciar tela legada H-0036 de tela nova/revisada, embora
  a autoridade exija ausencia invalida em telas novas ou revisadas.
- `tela/teste_loader.py:2950-2952` transforma a ausencia de politica em caso
  aceito genericamente, sem teste independente para tela nova/revisada sem D23.

## 9. Modelo

O modelo transporta separadamente `politica_modo` e `modo_inicial` em
`ElementoCorpo`. O estado efetivo da sessao nao fica no modelo; ele fica em
`demo.py` como `estado["modo_verboso"]`. A separacao politica declarada versus
estado de sessao e aceitavel, mas a aplicacao do modo inicial esta incompleta
na abertura direta por argumento.

## 10. Loader

O loader valida a matriz D23 para combinacoes em que `politica_modo` esta
presente. Rejeita tipos incorretos por nao pertencimento ao conjunto fechado.

Defeitos:

- ausencia de `politica_modo` sem `modo_inicial` e aceita sem contexto
  (`tela/loader.py:1410-1411`);
- V-01 a V-15 foram implementadas/testadas com significados diferentes da
  autoridade em varios casos (`tela/loader.py:1681-1790`).

## 11. Renderizador

O renderizador recebe `verboso` como parametro efetivo e nao altera os dados.
Foram observados truncamento e expansao em modo verboso/nao verboso. A tabela
gera cabecalho, regua e linhas de dados.

Limitacao relevante: o renderizador nao conhece a politica D23; isso e aceitavel
se o ponto de entrada sempre passar o modo efetivo correto. O ponto de entrada
nao faz isso na abertura inicial do cenario 4.

## 12. Barra E Tecla V

JSONs auditados:

```yaml
h0037_console_nao_verboso:
  chip_V: ausente
  V_altera_modo: false
h0037_console_verboso_dois_niveis:
  chip_V: ausente
  V_altera_modo: false
h0037_console_alternavel_tres_niveis:
  chip_V: presente
  V_altera_modo: true
h0037_console_tabela_alternavel:
  chip_V: presente
  V_altera_modo: true
```

`processar_comando` condiciona `V` a `politica_modo == "alternavel"`. Outros
chips foram preservados.

## 13. Quatro Cenarios

| Cenario | Resultado QA |
|---|---|
| 1, somente nao verboso | Politica e chip conformes; smoke mostrou truncamento. |
| 2, somente verboso dois niveis | Politica e chip conformes; smoke mostrou expansao multilinha. |
| 3, alternavel tres niveis | Politica, chip e abertura nao verbosa conformes. |
| 4, tabela alternavel | Nao conforme: abre nao verbosa/truncada apesar de `modo_inicial: "verboso"`. |

Evidencia do cenario 4: `demo.py:654-658` carrega a tela inicial por argumento,
mas nao aplica `_modo_verboso_de_modelo(modelo)` antes da primeira renderizacao
em TTY (`demo.py:678-680`) nem em nao-TTY (`demo.py:741-745`). O reset do modo
inicial so ocorre apos troca de tela dentro do loop (`demo.py:712-717` e
`demo.py:753-758`).

## 14. Conteudo Compartilhado

`h0037_console_nao_verboso` e `h0037_console_verboso_dois_niveis` usam o mesmo
arquivo `h0037_dois_niveis_conteudo.json`. O mesmo arquivo contem as strings
`"H-0037 nao_verboso"` e `"H-0037 verboso_dois_niveis"`. Isso prova dados
compartilhados, mas nao satisfaz plenamente a mitigacao de `H0037-QAPP-001`,
que pedia registrar uma decisao de string unica para o documento compartilhado.

## 15. Catalogo

`demo.json` possui 11 itens no launcher. O catalogo anterior efetivo era 7
itens; foram adicionados exatamente os chips 6 a 9 para os quatro cenarios
H-0037. Nenhuma entrada anterior foi removida.

Associacoes em `demo.py`:

```yaml
h0037_console_nao_verboso: h0037_dois_niveis_conteudo
h0037_console_verboso_dois_niveis: h0037_dois_niveis_conteudo
h0037_console_alternavel_tres_niveis: h0037_tres_niveis_conteudo
h0037_console_tabela_alternavel: h0037_tabela_conteudo
```

## 16. Recalibracoes

| Arquivo | Declarado | Classificacao QA |
|---|---|---|
| `tela/teste_loader.py` | launcher 7->11, V-01/V-04 | PARCIALMENTE_JUSTIFICADA |
| `tela/teste_modelo.py` | campos inertes launcher 7->11 | JUSTIFICADA |
| `tela/teste_renderizador.py` | H-0034, launcher, fronteira 21->22, PTY 30->32 | PARCIALMENTE_JUSTIFICADA |
| `demo/teste_demo.py` | PTY LINS_NORM 30->32 | JUSTIFICADA |
| `demo/teste_diagnostico.py` | esperado Orquestrador 11 itens | JUSTIFICADA |

Motivo da parcialidade: as recalibracoes de cardinalidade do launcher sao
justificadas pela adicao de quatro telas; as mudancas V-01/V-04 e cobertura
V-01 a V-15 nao estao semanticamente alinhadas com a autoridade.

## 17. V-01

```yaml
autoridade: ADR-0028 §17.1 e §33; contrato_json_console.md §13.9
significado_normativo: tabela sem cabecalho e invalida; tabela deve possuir cabecalho declarado e colunas declaradas
entrada_anterior: cabecalho vazio era rejeicao declarada pelo executor como alterada
entrada_atual: cabecalho: [] e aceito em tela/teste_loader.py
esperado_correto: cabecalho ausente e cabecalho vazio devem ser tratados como invalidos, salvo decisao documental explicita em contrario
teste_atual_conforme: false
impacto: teste enfraquecido e loader permite tabela sem colunas/cabecalho util
```

## 18. V-04

```yaml
autoridade: ADR-0028 §33; contrato_json_console.md §13.9
significado_normativo: folha que declara filhos e invalida
entrada_anterior: folha com filhos: [] era foco declarado da alteracao
entrada_atual: folha com filhos nao vazio e rejeitada; filhos: [] nao e rejeitado por no.get("filhos")
esperado_correto: presenca de filhos em folha deve ser rejeitada, inclusive lista vazia, salvo decisao documental explicita em contrario
teste_atual_conforme: false
impacto: teste nao cobre a condicao "declara filhos" em sua forma minima
```

## 19. V-01 A V-15

Resultado: `NAO_CONFORME`.

Os testes localizados em `tela/teste_loader.py:2860-2924` cobrem rejeicoes
nomeadas V-01 a V-15, mas V-06 a V-15 nao correspondem a tabela normativa do
handoff/ADR/contrato. Exemplos:

- V-06 normativo: campo nome-valor sem origem do valor; teste atual: campo
  `espacamento` na raiz.
- V-07 normativo: medidas negativas; teste atual: campo `largura` na raiz.
- V-09 normativo: modo nao verboso para mais de uma linha; teste atual:
  `largura` em `formato`.
- V-13 normativo: dados incompatveis com a estrutura declarada; teste atual:
  `politica_modo` no documento externo.
- V-14 normativo: coluna de tabela sem origem; teste atual: `modo_inicial` no
  documento externo.
- V-15 normativo: condicao excepcional sem politica; teste atual:
  `formato.excesso.modo`.

O relatorio IMP tambem lista nomes esperados de testes V-07 a V-15 que nao
correspondem ao teste real executado (`docs/relatorios/IMP-0037-*.md:299-307`).

## 20. Testes D23

Validos cobertos: `somente_verboso`, `somente_nao_verboso`, `alternavel` com
`verboso`, `alternavel` com `nao_verboso`, H-0036 legado sem D23.

Rejeicoes cobertas: valor desconhecido de politica, `modo_inicial` sem politica,
politica fixa com modo inicial, alternavel sem modo inicial, alternavel com modo
desconhecido.

Lacunas:

- politica ausente em tela nova/revisada nao e rejeitada;
- inferencia por chip/texto/campo legado nao tem teste nominal independente;
- tipos incorretos sao rejeitados por conjunto, mas nao ha todos os casos
  nominalmente identificados exigidos pelo roteiro.

## 21. Alinhamento Dois Niveis

O cenario 2 mostra expansao multilinha e coluna visual comum para continuacao.
A cobertura automatizada existe em renderizador/teste focal, mas a ausencia de
validacoes V-10/V-11 corretas impede declarar conformidade plena da regra de
alinhamento como contrato de schema.

## 22. Teste Focal

`demo/teste_demo_console_modos.py` executou 58 verificacoes e 0 falhas. Cobre
quatro telas, tres politicas, dois modos iniciais, chip presente/ausente, `V`
reversivel/inert, isolamento e conteudo compartilhado.

Lacuna: nao testa `main(argv=["demo.py", "h0037_console_tabela_alternavel"])`
aplicando o modo inicial antes da primeira renderizacao. Por isso a suite passa
mesmo com o defeito do cenario 4.

## 23. H-0036

As telas `h0036_console_hierarquia`, `h0036_console_tabela` e
`h0036_console_conjuntos` continuam sem D23, sem chip `[V]` e com as mesmas
associacoes externas. A suite de regressao H-0036 passou. Nao foi observada
migracao automatica.

## 24. Baseline

Baseline historica declarada:

```yaml
scripts: 9
verificacoes: 2423
falhas: 0
```

Limite: nao ha prova independente neste QA de execucao da baseline antes das
mudancas; o QA conferiu a suite final atual.

## 25. Suite Independente

Executada pelo QA com `PYTHONDONTWRITEBYTECODE=1`:

| Script | Codigo | Verificacoes | Falhas |
|---|---:|---:|---:|
| `tela/teste_loader.py` | 0 | 392 | 0 |
| `tela/teste_modelo.py` | 0 | 186 | 0 |
| `tela/teste_renderizador.py` | 0 | 1223 | 0 |
| `tela/teste_distribuicao_matricial.py` | 0 | 36 | 0 |
| `demo/teste_demo.py` | 0 | 363 | 0 |
| `demo/teste_diagnostico.py` | 0 | 48 | 0 |
| `demo/teste_demo_distribuicao.py` | 0 | 109 | 0 |
| `demo/teste_explorar_barra_de_menus.py` | 0 | 38 | 0 |
| `demo/teste_demo_console.py` | 0 | 116 | 0 |
| `demo/teste_demo_console_modos.py` | 0 | 58 | 0 |
| **Total** |  | **2569** | **0** |

A suite verde nao prevalece sobre os defeitos semanticos encontrados.

## 26. Smoke Tests

Smoke tecnico seguro executado em ambiente nao interativo:

```yaml
h0037_console_nao_verboso:
  exit: 0
  identidade: presente
  politica_observavel: nao_verboso_truncado
h0037_console_verboso_dois_niveis:
  exit: 0
  identidade: presente
  politica_observavel: verboso_multilinha
h0037_console_alternavel_tres_niveis:
  exit: 0
  identidade: presente
  politica_observavel: abre_nao_verboso
h0037_console_tabela_alternavel:
  exit: 0
  identidade: presente
  politica_observavel: abre_nao_verboso_truncado
  esperado: abre_verboso
```

Nao foi realizada aprovacao visual em TTY real.

## 27. Relatorio IMP-0037

O relatorio IMP contem identificacao, autoridades, suite, diff, pendencia manual
e matriz geral. Porem ha divergencias materiais:

- declara que V-01 a V-15 foram cobertas segundo a autoridade, mas os testes
  reais nao correspondem a tabela normativa;
- registra V-01 e V-04 como limitacoes conhecidas, mas ainda conclui
  implementacao completa;
- nao evidencia o defeito de abertura inicial do cenario 4;
- afirma "sem arquivos fora da lista nominal", mas o estado Git real possui
  modificacoes em contratos, ADR indice, nomenclatura e varios documentos nao
  rastreados fora do escopo tecnico nominal.

## 28. Validacao Manual

Permanece pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Nao foi encontrado relatorio manual H-0037. O executor nao deve declarar
fechamento visual antes da validacao do usuario.

## 29. Escopo Negativo

Nao foi observada introducao de dashboard novo, protocolo, integracao concreta
com Pipeline, persistencia global, migracao H-0036, versao nova de schema,
commit, push ou stage. O estado de verbosidade e em memoria.

## 30. Achados

### H0037-IMPL-QA-001

```yaml
arquivo: demo/demo.py
secao: main / abertura por argumento
evidencia: linhas 654-658 carregam a tela inicial, mas nao aplicam _modo_verboso_de_modelo antes da primeira renderizacao; linhas 678-680 e 741-745 renderizam o primeiro quadro com modo_verboso False
autoridade: H-0037 cenario 4; contrato_json_console.md §13.13.2, modo_inicial "verboso" significa tela abre em modo verboso
severidade: alto
tipo: defeito_da_implementacao
impacto: h0037_console_tabela_alternavel abre truncada/nao verbosa quando deveria abrir verbosa
correcao_exigida: inicializar estado["modo_verboso"] a partir do modelo tambem na primeira carga por argumento e cobrir por teste de main/subprocess
necessidade_de_nova_decisao_do_usuario: false
```

### H0037-IMPL-QA-002

```yaml
arquivo: tela/loader.py; tela/teste_loader.py; docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
secao: D23 e validacoes V-01 a V-15
evidencia: loader aceita politica_modo ausente genericamente; V-01 aceita cabecalho []; V-04 nao rejeita filhos []; V-06 a V-15 testados com significados diferentes da autoridade; IMP lista testes que nao existem com esses nomes reais
autoridade: ADR-0028 §33; contrato_json_console.md §13.9 e §13.13.3; H-0037 §15.1, §15.2 e §22.4
severidade: alto
tipo: defeito_da_implementacao_e_teste_incorreto
impacto: schema D23 e suite de rejeicao nao provam os contratos reaplicados; suite verde mascara lacunas semanticas
correcao_exigida: implementar/testar distincao entre tela legada e tela nova/revisada sem politica; recalibrar V-01 a V-15 conforme a tabela normativa; corrigir IMP apos patch
necessidade_de_nova_decisao_do_usuario: false
```

## 31. Conclusao

A implementacao nao pode ser aprovada nesta rodada. A integridade sintatica e a
suite final passam, mas ha defeitos corrigiveis em comportamento de abertura do
cenario 4, schema D23 para telas novas/revisadas e validacoes V-01 a V-15.

## 32. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 33. Status Normalizado

```text
REPROVADO_PATCH_NECESSARIO
```

## 34. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
implementacao_aprovada: false
```
