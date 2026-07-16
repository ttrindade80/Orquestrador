# Relatorio de QA pos-segundo-patch do handoff H-0034

```yaml
etapa: QA_HANDOFF
subetapa: QA_POS_SEGUNDO_PATCH_HANDOFF
handoff: H-0034
artefato_auditado: docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
primeiro_qa: docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
qa_pos_patch: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
status_literal: H1_HANDOFF_APPROVED
status_normalizado: APROVADO
data: 2026-07-15
auditoria: independente_pos_segundo_patch
```

## 1. Identificacao

Este relatorio audita exclusivamente o segundo patch do handoff:

`docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`

Nenhuma correcao foi aplicada ao handoff. Nenhum codigo, teste, contrato, ADR,
configuracao, nomenclatura, relatorio anterior ou stage Git foi alterado por
esta auditoria. O unico arquivo criado por esta etapa e este relatorio:

`docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`

## 2. Artefato, relatorios e autoridades

Artefato auditado:

- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`

Relatorios anteriores lidos:

- `docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md`

Autoridades consultadas:

- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md`
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md`
- `docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- secoes aplicaveis de `docs/NOMENCLATURA.md`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`

## 3. Estado Git inicial

Comandos executados no inicio, a partir da raiz:

```bash
git status --short
git diff --check
git diff --cached --name-only
```

`git status --short` inicial:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --check`: sem saida.

`git diff --cached --name-only`: sem saida; stage vazio.

O handoff permanece nao rastreado. A inspecao por
`git diff --no-index /dev/null docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
retornou codigo 1, esperado para arquivo novo contra `/dev/null`, e exibiu o
handoff como novo arquivo.

## 4. Proveniencia dos itens nao rastreados

```yaml
demo/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

tela/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/adr/ADR-0023-largura-minima-funcional-lancador.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md:
  origem: CONFIRMADA_EM_RELATORIO_ANTERIOR
  produzido_pelo_executor: CONFIRMADO_EM_RELATORIO_ANTERIOR
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md:
  origem: QA_APLICACAO_ADR-0023
  produzido_pelo_executor: CONFIRMADO_EM_RELATORIO_ANTERIOR
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md:
  origem: QA_POS_PATCH_H-0034_HANDOFF
  produzido_pelo_executor: CONFIRMADO_EM_RELATORIO_ANTERIOR
  produzido_pelo_usuario: NAO_CONFIRMADO

docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md:
  origem: QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF
  produzido_pelo_executor: CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

Os caches nao foram removidos.

## 5. Resultado do achado do segundo QA

```yaml
achado: QA-H0034-POSPATCH-HANDOFF-ALTO-001
estado: CORRIGIDO
evidencia: |
  O handoff agora exige modelo sintetico em memoria com `terminal_w=80`
  constante, `corpo.arranjo="horizontal"` e `corpo.distribuicao.modo="fracao"`.
  As provas globais `largura=20` e `largura=21` foram reclassificadas como
  suplementares, sem isolamento causal. A prova obrigatoria passa a comparar
  `[20,60]` e `[21,59]` dentro do mesmo viewport global.
residuos: |
  `fracao` nao significa largura absoluta; significa peso relativo. Contudo,
  neste caso especifico, o container horizontal recebe largura distribuivel
  80 e os vetores somam 80, entao o algoritmo de maiores restos aloca
  exatamente `[20,60]` e `[21,59]`.
regressoes: |
  Nenhuma regressao identificada.
conclusao: |
  A prova causal isolada ficou tecnicamente verdadeira e executavel dentro dos
  tres arquivos autorizados para a futura implementacao.
```

## 6. Semantica de `fracao` e calculos reais

Pelas autoridades e pela implementacao atual, `modo: fracao` representa
**pesos relativos**, nao larguras absolutas nem percentuais.

Fontes:

- `contrato_composicao_corpo.md` secao 5.7: `fracao.valores[]` declara pesos relativos; a fracao de cada filho e `valor_do_filho / soma_dos_valores`.
- `tela/renderizador.py::_pesos_distribuicao`: para `percentual`/`fracao`, devolve os valores declarados como pesos.
- `tela/renderizador.py::_distribuir_larguras`: reparte a largura pelo metodo dos maiores restos.

Unidades antes da distribuicao no cenario isolado:

```text
terminal_w = 80
largura_da_tela_normal = 80
largura_do_corpo = 80
largura_do_container_horizontal = 80
separadores_entre_filhos = 0
vaos_externos_do_container_horizontal = 0
largura_distribuivel_entre_filhos = 80
```

O cabecalho e a barra usam a largura total 80 em regioes separadas. Eles nao
consomem colunas da largura distribuida entre os filhos do corpo horizontal.
O container horizontal usa particionamento contiguo: as caixas ficam adjacentes,
sem vao externo entre `lancador_teste` e `console_resto`.

### 6.1 Calculo `[20,60]`

```text
largura_distribuivel = 80
pesos = [20,60]
soma_pesos = 80
ideal_lancador = 80 * 20 / 80 = 20
ideal_console = 80 * 60 / 80 = 60
partes_inteiras = [20,60]
faltam = 80 - (20 + 60) = 0
maiores_restos = nao aplicavel
larguras_finais = [20,60]
area_lancador_w_real = 20
content_w_lancador = 20 - 3 = 17
coluna_minima_content_w = 18
lancador_caixa_min_w = 21
resultado_esperado = quadro_minimo_global
```

### 6.2 Calculo `[21,59]`

```text
largura_distribuivel = 80
pesos = [21,59]
soma_pesos = 80
ideal_lancador = 80 * 21 / 80 = 21
ideal_console = 80 * 59 / 80 = 59
partes_inteiras = [21,59]
faltam = 80 - (21 + 59) = 0
maiores_restos = nao aplicavel
larguras_finais = [21,59]
area_lancador_w_real = 21
content_w_lancador = 21 - 3 = 18
coluna_minima_content_w = 18
lancador_caixa_min_w = 21
resultado_esperado = tela_normal
```

Conclusao: o handoff nao redefine `fracao` como largura absoluta. Ele escolhe
pesos cujo somatorio coincide com a largura distribuivel do container, o que
produz cotas inteiras exatas neste caso.

## 7. Dominio da largura 80 e isolamento global

O valor 80 recebe a grandeza `terminal_w`, passado como `largura=80` ao
renderer. No caminho atual:

- `renderizar_tela` define `total_w = 80`;
- o corpo e renderizado por `_renderizar_container(..., total_w=80, ...)`;
- com `arranjo="horizontal"`, `_renderizar_container_horizontal` distribui
  `total_w=80` entre os dois filhos;
- `_caixa_de_elemento` recebe cada cota `w` e monta caixa com comprimento total `w`;
- para o `lancador`, `content_w = area_lancador_w - 3`.

As grandezas ficam distintas:

```yaml
terminal_w: 80
largura_da_tela_normal: 80
largura_do_corpo: 80
largura_do_container_horizontal: 80
area_lancador_w:
  caso_insuficiente: 20
  caso_valido: 21
```

O minimo global preexistente nao e violado pelo viewport de 80: o controle com
`area_lancador_w=21` usa o mesmo terminal, a mesma altura, o mesmo cabecalho, a
mesma barra, os mesmos itens e o mesmo segundo elemento, e espera tela normal.
Assim, a diferenca material fica restrita a cota horizontal do `lancador`.

## 8. Console restante e modelo em memoria

O segundo elemento `console_resto` e valido:

- `console` e tipo funcional fechado ja suportado;
- `ElementoCorpo(id="console_resto", tipo="console", _campos_inertes={"titulo": "Console"})`
  e suficiente para o renderer atual;
- `_linhas_console` retorna placeholder estavel;
- as cotas reais 60 e 59 estao acima do minimo operacional de 10 caracteres
  imposto ao particionamento horizontal;
- nao exige JSON novo nem campo contratual novo;
- nao aciona quadro minimo por causa propria.

O modelo em memoria esta suficientemente especificado para `tela/teste_renderizador.py`:

- ID do modelo: `teste_isolamento_lancador`;
- `schema="tela.v1"`;
- cabecalho minimo com titulo e descricao;
- corpo horizontal;
- distribuicao `fracao`;
- dois elementos diretos, com ids e tipos;
- sete itens do `lancador`, com `id`, `chip` e `texto` suficientes para o teste;
- barra minima com chip `Esc`;
- altura 30;
- valores esperados 20 e 21;
- uso direto das dataclasses `ModeloTela`, `Corpo` e `ElementoCorpo`, compativeis
  com as assinaturas de `tela/modelo.py`.

O teste nao depende de loader nem de criacao de JSON.

## 9. Limite 20/21 e causa semantica

Parametros independentes:

```text
chip_sub_w_max = 3
texto_sub_w_max = 10
vao_chip_texto_min = 1
vao_margem_min = 2
coluna_minima_content_w = 2 + 3 + 1 + 10 + 2 = 18
largura_estrutural_da_caixa = 3
lancador_caixa_min_w = 18 + 3 = 21
```

Em `area_lancador_w=21`, a coluna minima completa cabe exatamente:

```text
content_w = 21 - 3 = 18
18 = coluna_minima_content_w
```

Em `area_lancador_w=20`, fica uma unidade abaixo:

```text
content_w = 20 - 3 = 17
17 < coluna_minima_content_w
```

Impacto:

- T-ISOL-01: prova gatilho interno insuficiente.
- T-ISOL-02: prova controle no limite valido.
- T-ISOL-03: prova determinismo da sequencia 21 -> 20 -> 21.
- Provas 9.5 e 9.6: permanecem corretas desde que a prova global 20/21 fique
  suplementar e a prova isolada seja obrigatoria.
- Criterios de aceite: o criterio 24 fica exequivel.
- Relatorio de implementacao: deve registrar as cotas reais calculadas, nao
  apenas repetir os valores declarados.

## 10. Recuperacao 21 -> 20 -> 21

A formulacao e adequada para o renderer atual, que e uma funcao pura sem estado
persistente entre chamadas. O handoff distingue corretamente:

- equivalencia deterministica de renderizacoes puras (`s_passo1 == s_passo3`);
- recuperacao visual reativa em sessao TTY real, que permanece validacao manual
  futura;
- ausencia de alegacao de que o teste automatizado valida `SIGWINCH`, redraw ou
  sessao TTY real.

## 11. Provas globais suplementares

As ocorrencias de largura global 20 e 21 foram classificadas como:

```yaml
isolamento_gatilho_interno: false
finalidade: prova_suplementar_de_fronteira
```

Nao restou afirmacao material de que a demo vertical em largura total 20 prova
causalmente o novo gatilho interno. As secoes 9.5.1, 9.6.1, 11 e 12 fazem a
separacao entre fronteira global suplementar e prova isolada obrigatoria.

## 12. Testes T-ISOL

```yaml
T-ISOL-01:
  cenario_nominal: modelo em memoria, terminal_w=80, fracao [20,60]
  entrada_independente: pesos declarados e itens literais
  grandezas_esperadas: area_lancador_w=20, content_w=17, lancador_caixa_min_w=21
  causa_esperada: area_lancador_w < lancador_caixa_min_w
  saida_esperada: quadro minimo global, sem chips do lancador
  prova_semantica: controle T-ISOL-02 com mesmo terminal produz tela normal
  dependencia_funcao_futura_para_esperado: false

T-ISOL-02:
  cenario_nominal: mesmo modelo, terminal_w=80, fracao [21,59]
  entrada_independente: pesos declarados e itens literais
  grandezas_esperadas: area_lancador_w=21, content_w=18
  causa_esperada: limite valido da coluna minima
  saida_esperada: tela normal com sete chips
  prova_semantica: todos os demais requisitos iguais a T-ISOL-01
  dependencia_funcao_futura_para_esperado: false

T-ISOL-03:
  cenario_nominal: sequencia 21 -> 20 -> 21
  entrada_independente: mesmos modelos sinteticos
  grandezas_esperadas: [21,20,21]
  causa_esperada: determinismo sem estado persistente
  saida_esperada: s_passo1 == s_passo3
  prova_semantica: nao alega validacao TTY real
  dependencia_funcao_futura_para_esperado: false
```

## 13. Arquivos autorizados e ausencia de arquitetura nova

O cenario pode ser implementado somente em:

- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`

Nao exige configuracao nova, alteracao de `config/telas/demo/demo.json`,
alteracao de `demo/demo.py`, arquivo auxiliar, novo modulo, contrato novo,
ADR nova ou mudanca documental adicional.

Capacidades ja existentes e documentadas:

- `corpo.arranjo = "horizontal"`;
- `corpo.distribuicao.modo = "fracao"`;
- alocacao por pesos e maiores restos;
- tipo funcional `console`;
- tipo funcional `lancador`;
- modelo em memoria por dataclasses existentes.

Nenhum campo ou politica foi inventado. A semantica de `fracao` nao foi
redefinida.

## 14. Preservacao dos achados anteriores

```yaml
QA-H0034-HANDOFF-ALTO-001: CORRIGIDO
QA-H0034-HANDOFF-ALTO-002: CORRIGIDO
QA-H0034-HANDOFF-ALTO-003: CORRIGIDO
QA-H0034-HANDOFF-MEDIO-001: CORRIGIDO
QA-H0034-HANDOFF-MEDIO-002: CORRIGIDO
QA-H0034-HANDOFF-MEDIO-003: CORRIGIDO
QA-H0034-HANDOFF-BAIXO-001: CORRIGIDO
QA-H0034-HANDOFF-OBS-001: CORRIGIDO
```

Confirmacoes:

- suite focal versus canonica permanece distinguida;
- demonstracao deterministica permanece separada de smoke, pseudo-TTY e TTY real;
- quadro minimo global permanece definido;
- cinco grandezas permanecem separadas;
- T-07 continua com colunas independentes;
- T-10/T-11 continuam com esperados completos;
- norma e caminho recomendado de implementacao permanecem separados;
- alinhamento por instancia permanece preservado.

Nenhuma regressao identificada.

## 15. Escopo negativo

Permanecem fora:

- cabecalho;
- reticencias;
- quebra de descricao;
- `destino_minimo`;
- `grupo_minimo`;
- `barra_de_menus`;
- navegacao;
- selecao;
- acoes novas;
- paginacao;
- persistencia;
- H-0030;
- H-0033;
- `orquestrador.py`;
- refatoracao ampla;
- alteracao de contratos ou ADRs;
- commit.

## 16. Relatorio de implementacao esperado

O futuro IMP deve registrar o bloco abaixo com calculos reais:

```yaml
prova_isolada:
  terminal_w: 80
  largura_util_container: 80
  modo_distribuicao: fracao
  pesos:
    insuficiente: [20, 60]
    valido: [21, 59]
  area_lancador_w_calculada:
    insuficiente: 20
    valido: 21
  area_resto_calculada:
    insuficiente: 60
    valido: 59
  lancador_caixa_min_w: 21
  minimo_global_tela_satisfeito: true
  demais_componentes_validos: true
  causa_do_quadro_minimo: area_lancador_w < lancador_caixa_min_w
  evidencias:
    - controle valido com terminal_w=80 e area_lancador_w=21 produz tela normal
    - caso insuficiente com terminal_w=80 e area_lancador_w=20 produz quadro minimo global
```

O relatorio deve explicar que `[20,60]` e `[21,59]` sao pesos relativos que
produzem cotas exatas neste cenario porque a largura distribuivel e 80 e a soma
dos pesos tambem e 80.

## 17. Busca de residuos

Foram avaliadas as ocorrencias no handoff de:

- `[20, 60]`;
- `[21, 59]`;
- `fracao`;
- peso;
- largura absoluta;
- `terminal_w = 80`;
- `area_lancador_w`;
- largura do corpo;
- largura do container;
- separador;
- arredondamento;
- maiores restos;
- `console_resto`;
- modelo em memoria;
- T-ISOL-01;
- T-ISOL-02;
- T-ISOL-03;
- `s_passo1 == s_passo3`;
- largura global 20;
- largura global 21;
- prova causal.

Resultado: nao foram encontrados residuos que invalidem o segundo patch. O unico
ponto que exige cuidado e terminologico: `fracao` continua sendo peso relativo.
O handoff, porem, tambem fornece o calculo `_distribuir_larguras(80, [...])`,
o que torna a area real comprovavel sem depender de semantica absoluta.

## 18. Regressões e novos achados

Regressoes: nenhuma.

Novos achados: nenhum bloqueante, alto, medio ou baixo.

Observacao:

```yaml
id: QA-H0034-POS2-HANDOFF-OBS-001
severidade: observacao
evidencia: |
  O teste isolado usa `fracao` com vetores que somam a largura distribuivel.
  Isso e valido e executavel, mas nao deve ser descrito como largura absoluta.
regra_violada: nenhuma
impacto: |
  Baixo risco de leitura equivocada pelo implementador se o IMP nao registrar
  que os valores sao pesos relativos com resultado exato neste caso.
correcao_necessaria: |
  Nenhuma correcao do handoff exigida. O IMP futuro deve registrar o calculo
  real de cotas.
secao_afetada:
  - 9.5.2
  - 9.5.3
  - 10.3 T-ISOL-01/T-ISOL-02
  - 12 Relatorio de implementacao obrigatorio
```

## 19. Status

```yaml
status_literal: H1_HANDOFF_APPROVED
status_normalizado: APROVADO
achado_segundo_qa:
  QA-H0034-POSPATCH-HANDOFF-ALTO-001: CORRIGIDO
achados_anteriores:
  todos_corrigidos: true
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 1
regressoes: 0
proxima_categoria: IMPLEMENTAR_HANDOFF
```

## 20. Testes e validacao manual

Nao foram executados testes automatizados da implementacao futura. A auditoria
foi documental e tecnica, por leitura das autoridades, inspecao do renderer e
calculos independentes.

Validacao manual em TTY real nao foi executada. Ela permanece futura e exclusiva
da etapa de implementacao/validacao do handoff.

## 21. Estado Git final

Comandos a executar ao final, a partir da raiz:

```bash
git status --short
git diff --check
git diff --cached --name-only
```

Estado esperado apos a criacao deste relatorio:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? tela/__pycache__/
```

`git diff --check` esperado: sem saida.

`git diff --cached --name-only` esperado: sem saida; stage vazio.
