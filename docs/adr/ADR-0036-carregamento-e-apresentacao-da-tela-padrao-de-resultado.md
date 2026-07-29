---
name: ADR-0036-carregamento-e-apresentacao-da-tela-padrao-de-resultado
description: "Formaliza a especificação do Handoff 3 da ADR-0034: identidade e composição da tela padrão resultado_execucao, ciclo de carregamento do JSON estrutural e do documento runtime, regra de escolha entre documento de resultado e envelope de erro, schema visual do envelope, cenários obrigatórios em 80x24 e manifesto nominal previsto"
metadata:
  type: adr
  status: aceita
  id: ADR-0036
  data: 2026-07-29
  substitui: null
rastreabilidade:
  decisao_usuario: "D-H3-01 a D-H3-19 — identidade e perfil da tela resultado_execucao; console único console_resultado sem navegação, seleção nem paginação; cabeçalho fixo; composição do corpo por um único console em arranjo vertical; associação do conteúdo externa em runtime, sem novo campo de caminho nem novo tipo de binding; apresentação declarada pelo documento runtime entre tabela/hierarquia/conjuntos_campos, política somente_verboso, ausência de chip [V]; estado estrutural inicial vazio; barra de menus com único chip Esc/Voltar; ciclo de carregamento único na entrada do cenário, sem releitura em redesenho/SIGWINCH; regra de escolha entre apresentar o documento original (código 0 e documento válido) e gerar envelope de erro (código não zero, resultado ausente, malformado ou semanticamente inválido); status único falha no envelope, com codigo_saida 130 em interrupção; diagnósticos canônicos determinísticos; estrutura integral do envelope em seis campos de ordem fixa (status, diagnostico, codigo_saida, stdout, stderr, resultado_json); apresentação visual do envelope em conjuntos_campos sem estilo especial nem cor de alerta; canais textuais vazios exibidos como indisponível; campo resultado_json com preservação literal byte a byte ou null; seis cenários obrigatórios em 80x24 (sucesso, parcial, falha_semantica, falha_operacional, resultado_invalido, interrupcao); evidências obrigatórias por cenário via demo/demo.py; manifesto nominal previsto para o futuro handoff, sem autorizar implementação nesta etapa; supersessão parcial e pontual da divisão de handoffs de D-SEL-21 quanto à abertura da tela e ao retorno, atribuídas ao Handoff 4"
  rfc_origem: null
  issues_relacionadas:
    - ITEM-0006
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
  handoffs_bloqueados: []
---

# ADR-0036 — Carregamento e apresentação da tela padrão de resultado (especialização do Handoff 3 da ADR-0034)

## 1. Status

`aceita`

## 2. Contexto

A ADR-0034 fechou, para o `ITEM-0006`, o modelo de seleção múltipla e o fluxo
focal de processamento, decomposto em quatro handoffs sequenciais (D-SEL-21).
O Handoff 1 foi entregue por `H-0041` (estado da seleção, comandos e
apresentação, sem operação externa). O Handoff 2 — protocolo focal do
binding e execução — foi especializado pela ADR-0035 (executor sintético,
cópia de trabalho reversível, documento de resultado de execução em JSON
multinível, controles sintéticos e interrupção protegida) e implementado por
`H-0042`, com QA pós-patch aprovado (`I1_IMPLEMENTATION_APPROVED`).

O Handoff 3 — tela padrão e integração da interface — permanece aberto. A
ADR-0034 já fechou, em nível geral, a existência do perfil `resultado_execucao`
(D-SEL-16), a validação antecipada do destino (D-SEL-17) e o envelope de erro
multinível (D-SEL-15; `contrato_json_console.md` §14.6). Esse fechamento geral
não decide, porém, o que é indispensável para especificar o Handoff 3 de forma
focal: a identidade exata da tela e do console únicos; a composição concreta
do cabeçalho, do corpo e da barra de menus; a regra precisa de associação do
conteúdo externo em runtime; o ciclo de carregamento e construção do modelo em
memória e seu comportamento sob redesenho/`SIGWINCH`; a regra determinística de
escolha entre apresentar o documento de resultado original ou gerar o envelope
de erro; o schema visual e a semântica concreta do envelope (status único,
diagnósticos canônicos, tratamento dos canais textuais e do campo
`resultado_json`); os seis cenários obrigatórios de demonstração em `80x24`; as
evidências exigidas por cenário; e o manifesto nominal de arquivos previsto
para a implementação futura.

Este documento fecha essas lacunas como especialização do Handoff 3, sem
reabrir o núcleo da seleção múltipla (D-SEL-01 a D-SEL-10), sem substituir a
ADR-0034 ou a ADR-0035 — ressalvada a supersessão parcial e pontual,
declarada em D-H3-19, da divisão de responsabilidades entre Handoff 3 e
Handoff 4 fixada por D-SEL-21 —, sem redefinir o protocolo do Handoff 2
fechado por `H-0042`, sem ativar o chip `Executar` na interface, sem definir
o binding real entre Orquestrador e Pipeline e sem criar o handoff de
implementação correspondente — essa autorização permanece para um `H-0043`
futuro, criado em etapa distinta.

---

## 3. Decisão explícita do usuário

### D-H3-01 — Identidade da tela

```yaml
id: resultado_execucao
arquivo_previsto: config/telas/demo/resultado_execucao.json
natureza: tela_estatica_reutilizavel
perfil: resultado_execucao
```

A identidade não contém o número do handoff e pode ser reutilizada por
diferentes telas e scripts.

### D-H3-02 — Console único

```yaml
id: console_resultado
titulo: Resultado
tipo: console
navegavel: false
politica_selecao: nenhuma
```

Nenhum `dashboard`, `lancador`, `grupo` ou segundo console participa da
composição.

### D-H3-03 — Cabeçalho

```yaml
titulo: Resultado da execução
descricao: Resultado estruturado da operação realizada.
```

### D-H3-04 — Composição do corpo

```yaml
corpo:
  arranjo: vertical
  distribuicao: ausente
  elementos:
    - console_resultado
```

O único console ocupa integralmente a área do corpo por cardinalidade
unitária. O arranjo explícito impede dependência do `tiling` global ainda não
definido.

### D-H3-05 — Associação do conteúdo

```yaml
origem_dados: null
associacao_do_documento: externa_em_runtime
novo_campo_de_caminho: nao
novo_tipo_de_binding: nao
```

O `tela.json` permanece estrutural. O documento externo validado é entregue
separadamente pelo ponto de entrada e não é incorporado ao JSON estrutural.

### D-H3-06 — Apresentação e modo

```yaml
apresentacao_fixa_na_tela: ausente
politica_modo: somente_verboso
apresentacao_declarada_pelo_documento_runtime: true
apresentacoes_aceitas:
  - tabela
  - hierarquia
  - conjuntos_campos
chip_V: ausente
```

### D-H3-07 — Estado estrutural inicial

```yaml
origem_dados: null
itens: []
politica_navegacao:
  navegavel: false
politica_selecao: nenhuma
politica_paginacao: sem
```

O conteúdo estático começa vazio. O conteúdo real existe somente no modelo
composto de runtime.

### D-H3-08 — Barra de menus

```yaml
barra_de_menus:
  distribuicao: horizontal
  chips:
    - id: esc
      tecla: Esc
      texto: Voltar
      acao: voltar
```

A declaração deve ser estruturalmente válida. A execução efetiva do retorno,
a origem suspensa e sua restauração pertencem ao Handoff 4. Nenhum outro chip
é permitido.

### D-H3-09 — Ciclo de carregamento

```yaml
inicio_do_cenario:
  carregar_tela_json: uma_vez
  validar_schema_e_perfil: antes_da_construcao
  carregar_documento_runtime: uma_vez
  validar_documento: antes_da_construcao
  construir_modelo_composto_em_memoria: true

redesenho_ou_SIGWINCH:
  reler_arquivos: false
  reutilizar_modelo_em_memoria: true
  recalcular_representacao_fisica: true
```

O redesenho não deve tornar a sessão dependente de alterações posteriores nos
arquivos de origem.

### D-H3-10 — Documento de resultado versus envelope de erro

Apresentar o documento original somente quando as duas condições forem
satisfeitas:

```yaml
codigo_saida: 0
documento_resultado: valido
```

Gerar envelope de erro quando ocorrer qualquer uma destas condições:

```yaml
- codigo_saida_nao_zero
- resultado_ausente
- resultado_malformado
- resultado_semanticamente_invalido
```

Um documento válido cujo processo terminou com código não zero não é
apresentado diretamente. Seu texto bruto deve ser preservado no campo
`resultado_json` do envelope.

Os estados semânticos `sucesso`, `parcial` e `falha` pertencentes a um
documento válido com código zero continuam sendo apresentados como documento
de resultado.

### D-H3-11 — Status do envelope

```yaml
status: falha
```

O valor é único para todos os envelopes. A causa específica é registrada em
`diagnostico` e `codigo_saida`.

Para interrupção:

```yaml
status: falha
codigo_saida: 130
```

### D-H3-12 — Diagnósticos canônicos

O diagnóstico é produzido pelo Orquestrador, de forma canônica e
determinística:

```yaml
codigo_nao_zero: A execução terminou com código de saída não zero.
resultado_ausente: A execução não produziu o documento de resultado.
resultado_malformado: O documento de resultado não contém JSON válido.
resultado_semanticamente_invalido: O documento de resultado não atende ao schema esperado.
interrupcao: A execução foi interrompida.
```

`stdout` e `stderr` permanecem em campos próprios. Não devem ser copiados,
concatenados ou usados como substitutos do diagnóstico.

### D-H3-13 — Apresentação visual do erro

```yaml
apresentacao: conjuntos_campos
estilo_especial: nao
cor_alerta: nao_utilizada
```

A falha é identificada pelos campos `status`, `diagnostico` e `codigo_saida`.

É proibido hardcodar cor, alterar a moldura ou criar comportamento visual
especial para o envelope neste ciclo.

### D-H3-14 — Canais textuais vazios

```yaml
stdout_ausente_ou_vazio: indisponível
stderr_ausente_ou_vazio: indisponível
campos_sempre_visiveis: true
```

### D-H3-15 — Campo `resultado_json`

```yaml
sem_conteudo_disponivel: null

com_conteudo:
  tipo: string
  valor: texto_bruto_exato
```

A regra aplica-se tanto a conteúdo JSON válido quanto inválido.

Devem ser preservados:

```yaml
- espacos
- quebras_de_linha
- ordem_das_chaves
- indentacao
```

É proibido:

```yaml
- corrigir
- normalizar
- reserializar
- inferir_conteudo
```

É permitido somente o escape necessário para transportar o texto como string
JSON. O valor `null` é exibido visualmente como `indisponível`.

### D-H3-15a — Estrutura integral do envelope de erro

Tornando explícita a estrutura já decidida em D-H3-11 a D-H3-15, sem criar
schema concorrente:

```yaml
envelope_de_erro:
  tipo: multinivel
  apresentacao: conjuntos_campos
  campos_em_ordem_fixa:
    - status
    - diagnostico
    - codigo_saida
    - stdout
    - stderr
    - resultado_json
```

```yaml
os_seis_campos: obrigatorios
ordem: normativa_nao_alteravel_pelo_renderer
omissao_de_campo: proibida
status: falha
stdout_ausente_ou_vazio: indisponível
stderr_ausente_ou_vazio: indisponível
resultado_json_null: indisponível
resultado_json_com_conteudo: string_com_texto_bruto_exato
apresentacao: sempre_conjuntos_campos
cor_ou_moldura_ou_estilo_especial: nao
```

Os seis campos listados são obrigatórios e devem estar sempre presentes; a
ordem acima é normativa e não pode ser alterada pelo renderer; nenhum campo
pode ser omitido.

### D-H3-16 — Cenários obrigatórios em 80×24

Devem existir seis cenários distintos:

```yaml
- sucesso:
    codigo_saida: 0
    documento_valido: true
    status_semantico: sucesso

- parcial:
    codigo_saida: 0
    documento_valido: true
    status_semantico: parcial

- falha_semantica:
    codigo_saida: 0
    documento_valido: true
    status_semantico: falha
    apresentacao: documento_original

- falha_operacional:
    codigo_saida: nao_zero
    apresentacao: envelope_de_erro

- resultado_invalido:
    apresentacao: envelope_de_erro

- interrupcao:
    codigo_saida: 130
    apresentacao: envelope_de_erro
```

Cada cenário deve caber integralmente em terminal `80×24`, sem paginação,
truncamento, omissão ou fallback temporário.

### D-H3-17 — Evidências

Para cada cenário, exigir:

```yaml
- fixture_de_entrada
- quadro_textual_esperado_80x24
- comparacao_automatizada_do_quadro
- demonstracao_TTY_reproduzivel
```

Invariantes:

```yaml
linhas_do_quadro: 24
colunas_maximas_por_linha: 80
todos_os_campos_esperados_visiveis: true
paginacao: ausente
truncamento: ausente
chips_visiveis:
  - Esc_Voltar
```

A prova integrada deve passar por `demo/demo.py`. Demonstrador auxiliar não
substitui o ponto de entrada obrigatório.

### D-H3-18 — Manifesto nominal previsto para o handoff

Arquivos novos previstos:

```text
tela/resultado_execucao.py
tela/teste_resultado_execucao.py
config/telas/demo/resultado_execucao.json

demo/fixtures/h0043_resultado_sucesso.json
demo/fixtures/h0043_resultado_parcial.json
demo/fixtures/h0043_resultado_falha_semantica.json
demo/fixtures/h0043_envelope_falha_operacional.json
demo/fixtures/h0043_envelope_resultado_invalido.json
demo/fixtures/h0043_envelope_interrupcao.json

demo/fixtures/h0043_quadro_sucesso_80x24.txt
demo/fixtures/h0043_quadro_parcial_80x24.txt
demo/fixtures/h0043_quadro_falha_semantica_80x24.txt
demo/fixtures/h0043_quadro_falha_operacional_80x24.txt
demo/fixtures/h0043_quadro_resultado_invalido_80x24.txt
demo/fixtures/h0043_quadro_interrupcao_80x24.txt
```

Arquivos existentes cuja alteração poderá ser autorizada pelo handoff:

```text
tela/loader.py
tela/teste_loader.py
tela/renderizador.py
tela/teste_renderizador.py
demo/demo.py
demo/teste_demo.py
```

Arquivos e capacidades preservados:

```text
tela/execucao_focal.py
demo/executor_sintetico.py
demo/demo_execucao_focal.py
demo/fixtures/h0042_*.json
config/estilo.json
tela/selecao.py
```

A lista nominal final de arquivos e a alteração efetiva dos arquivos
existentes listados acima pertencem ao futuro handoff. Esta ADR não autoriza
implementação nesta etapa.

### D-H3-19 — Supersessão parcial da divisão de handoffs (ADR-0034 D-SEL-21; `contrato_json_console.md` §14.11)

```yaml
supersessao_parcial:
  autoridades_anteriores_afetadas:
    - ADR-0034_D-SEL-21
    - contrato_json_console_secao_14.11

  aspecto_substituido:
    - divisao_de_responsabilidades_entre_Handoff_3_e_Handoff_4

  nova_divisao:
    Handoff_3:
      - carregar_tela_estatica_de_resultado
      - validar_schema_perfil_e_documento_runtime
      - construir_modelo_composto_em_memoria
      - escolher_documento_de_resultado_ou_envelope_de_erro
      - materializar_e_apresentar_o_conteudo
      - produzir_fixtures_quadros_e_evidencias_80x24

    Handoff_4:
      - ativar_chip_Executar
      - abrir_a_tela_de_resultado
      - suspender_a_tela_de_origem
      - executar_o_retorno
      - restaurar_a_tela_de_origem
```

Esta supersessão é **somente** sobre a divisão de responsabilidades entre o
Handoff 3 e o Handoff 4 originalmente fixada por D-SEL-21 — que atribuía ao
Handoff 3 também a abertura da tela e o retorno por `Esc` — e reproduzida em
`contrato_json_console.md` §14.11. Todas as demais decisões da ADR-0034,
incluindo D-SEL-01 a D-SEL-20 e D-SEL-22 a D-SEL-24, bem como a própria
decomposição em quatro handoffs sequenciais, permanecem integralmente
vigentes.

Esta ADR não afirma que `contrato_json_console.md` §14.11 já foi atualizado
para refletir a nova divisão. A futura etapa `APLICAR_ADR` deverá propagar
esta alteração a `contrato_json_console.md` e a qualquer outra remissão
documental materialmente afetada por essa nova fronteira.

Sob a nova divisão, o Handoff 3 continua sem qualquer abertura funcional da
tela de resultado e sem execução do retorno — essas capacidades permanecem
exclusivamente do Handoff 4, que continua responsável pelo ciclo completo de
navegação entre a tela de origem e a tela de resultado (suspensão, retorno e
restauração).

Não há contradição residual entre a especialização declarada nas demais
seções desta ADR e a preservação geral da ADR-0034: esta ADR é autoridade
documental posterior e substitui expressamente, de forma pontual, apenas o
aspecto aqui identificado, sem reabrir ou alterar qualquer outra decisão de
D-SEL-21 ou das demais decisões da ADR-0034.

---

## 4. Decisão

Fica adotada, como especialização do Handoff 3 do `ITEM-0006` (ADR-0034
D-SEL-15 a D-SEL-17, D-SEL-21), a especificação de carregamento e apresentação
da tela padrão de resultado `resultado_execucao`, organizada em seis camadas:

**Identidade e composição estrutural (D-H3-01 a D-H3-08).** A tela
`resultado_execucao` é um `tela.json` estático e reutilizável, identificado
pelo `perfil: resultado_execucao` já compatível com `tela.v1` (ADR-0034
D-SEL-16), composta por cabeçalho fixo, um único console passivo
(`console_resultado`, sem navegação, sem seleção, sem paginação) que ocupa
integralmente o corpo em arranjo vertical explícito, e barra de menus com o
único chip `Esc`/`Voltar`. A associação do documento de conteúdo ocorre
externamente, em runtime, sem novo campo de caminho e sem novo tipo de
binding no JSON estrutural; o estado estrutural inicial do console é vazio,
e a apresentação concreta (`tabela`, `hierarquia` ou `conjuntos_campos`) é
declarada pelo documento runtime, sob política `somente_verboso` e sem chip
`[V]`.

**Ciclo de carregamento e construção do modelo (D-H3-09).** O `tela.json` e o
documento runtime são cada um carregado e validado exatamente uma vez, antes
da construção do modelo composto em memória. Redesenho e `SIGWINCH` nunca
relêem os arquivos de origem — reutilizam o modelo já construído e recalculam
apenas a representação física.

**Regra de escolha entre documento de resultado e envelope, e schema do
envelope (D-H3-10 a D-H3-15).** O documento de resultado original só é
apresentado diretamente quando o processo terminou com código de saída `0` e
o documento é válido; qualquer código não zero, resultado ausente, malformado
ou semanticamente inválido produz envelope de erro multinível com `status:
falha` único (e `codigo_saida: 130` para interrupção), diagnóstico canônico
determinístico produzido pelo Orquestrador, apresentação `conjuntos_campos`
sem estilo especial nem cor de alerta, canais textuais vazios exibidos como
`indisponível`, e campo `resultado_json` preservado literalmente (byte a
byte, sem correção, normalização ou reserialização) ou `null` quando
indisponível. A estrutura integral do envelope compreende seis campos em
ordem fixa e normativa — `status`, `diagnostico`, `codigo_saida`, `stdout`,
`stderr`, `resultado_json` —, todos obrigatórios e nenhum omissível
(D-H3-15a).

**Cenários e evidências obrigatórias (D-H3-16 e D-H3-17).** Seis cenários
distintos — `sucesso`, `parcial`, `falha_semantica` (documento original) e
`falha_operacional`, `resultado_invalido`, `interrupcao` (envelope de erro) —
devem caber integralmente em terminal `80×24`, sem paginação, truncamento,
omissão ou fallback, cada um com fixture de entrada, quadro textual esperado,
comparação automatizada e demonstração TTY reproduzível, com a prova
integrada obrigatoriamente passando por `demo/demo.py`.

**Manifesto nominal previsto (D-H3-18).** A especificação registra a lista
nominal de arquivos novos, arquivos existentes cuja alteração poderá ser
autorizada, e arquivos e capacidades preservados para o futuro handoff de
implementação — sem autorizar essa implementação nesta etapa.

**Supersessão pontual da divisão de handoffs (D-H3-19).** Fica registrada a
supersessão parcial da divisão de responsabilidades entre o Handoff 3 e o
Handoff 4 originalmente fixada pela ADR-0034 (D-SEL-21) e reproduzida em
`contrato_json_console.md` §14.11: a abertura da tela de resultado e o
retorno passam a pertencer exclusivamente ao Handoff 4, junto com a
suspensão da tela de origem e a restauração; o Handoff 3 permanece limitado
ao carregamento, à validação, à construção do modelo, à regra de escolha
entre documento e envelope, à materialização/apresentação do conteúdo e às
fixtures/evidências. Todas as demais decisões da ADR-0034 permanecem
vigentes; a propagação dessa alteração aos contratos afetados cabe à futura
etapa `APLICAR_ADR`.

Esta decisão não altera D-SEL-01 a D-SEL-10 (núcleo da seleção múltipla), não
redefine o protocolo do Handoff 2 fechado pela ADR-0035 e implementado por
`H-0042`, não ativa o chip `Executar` nem a abertura real da tela de
resultado na interface, e não institui binding definitivo entre Orquestrador
e Pipeline.

---

## 5. Consequências

### Positivas

- Fecha as lacunas indispensáveis para especificar o Handoff 3 de forma
  focal, sem reabrir o núcleo de seleção múltipla nem o protocolo já fechado
  do Handoff 2.
- Estabelece uma regra determinística e testável de escolha entre documento
  de resultado e envelope de erro, eliminando ambiguidade sobre quando cada
  um é apresentado.
- Fixa um schema visual único e estável para o envelope de erro
  (`conjuntos_campos`, campos fixos, sem estilo especial), reduzindo a
  necessidade de decisões visuais ad hoc na implementação futura.
- Fecha a exigência de preservação literal do campo `resultado_json`,
  evitando qualquer heurística de correção silenciosa de conteúdo inválido
  produzido por processo externo.
- Define seis cenários obrigatórios com evidência automatizada e
  reproduzível via `demo/demo.py`, reduzindo o risco de regressão silenciosa
  na futura implementação.
- Registra um manifesto nominal previsto, orientando o escopo do futuro
  `H-0043` sem antecipar autorização de implementação.

### Custos e restrições

- Exige que a futura implementação distinga, para cada cenário, entre
  reutilizar o documento de resultado do Handoff 2 (`H-0042`) e produzir
  envelopes de erro novos para os cenários de falha operacional, resultado
  inválido e interrupção.
- Restringe todos os seis cenários de demonstração à dimensão lógica
  `80×24`, exigindo disciplina na criação das fixtures e dos quadros
  textuais esperados.
- Exige que o ciclo de carregamento nunca releia os arquivos de origem em
  redesenho/`SIGWINCH`, o que impõe que o modelo composto em memória seja
  suficiente para qualquer recálculo de representação física.
- Adia para o manifesto nominal do futuro handoff a decisão final sobre
  quais arquivos existentes (`tela/loader.py`, `tela/renderizador.py`,
  `demo/demo.py`, entre outros) precisarão de alteração efetiva.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `docs/contratos/contrato_tela_json.md` | Especializar a seção 34 (`perfil: resultado_execucao`) com a composição concreta de D-H3-01 a D-H3-08 e o ciclo de carregamento de D-H3-09, preservando integralmente a validação antecipada (D-SEL-17) já registrada. |
| `docs/contratos/contrato_composicao_corpo.md` | Especializar a seção 3.1.1 (tela de resultado como composição) com a identidade concreta do console único, do cabeçalho e do arranjo vertical explícito (D-H3-02 a D-H3-04). |
| `docs/contratos/contrato_barra_de_menus.md` | Registrar a instância concreta do único chip `Esc`/`Voltar` da tela de resultado (D-H3-08), sem alterar a ordem canônica já vigente. |
| `docs/contratos/contrato_console.md` | Especializar a seção 23.6 (operação focal) com a fronteira comportamental do Handoff 3 sobre carregamento (D-H3-09) e escolha entre documento e envelope (D-H3-10), preservando D-SEL-01 a D-SEL-10. |
| `docs/contratos/contrato_json_console.md` | Especializar a seção 14 com o schema visual e a semântica concreta do envelope de erro (D-H3-11 a D-H3-15), preservando integralmente o envelope multinível já fechado por D-SEL-15 e especializado por H2-ESP. |
| `docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` | Avaliar necessidade de termos novos para a distinção operacional entre documento de resultado apresentado e envelope de erro gerado, preservando a definição já registrada em §4.5. |
| `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | Avaliar necessidade de termos novos para o ciclo de carregamento único por cenário (D-H3-09), preservando a remissão já registrada em §4.5. |
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0036 após QA favorável. |
| `docs/backlog.md` | Atualizar o estado material do `ITEM-0006` quando o fluxo documental determinar mudança, incluindo a indicação de que o futuro handoff será o `H-0043`. |

---

## 6. Compatibilidade e transição

Esta ADR não executa nenhuma aplicação documental, alteração de contrato,
alteração de nomenclatura, criação de handoff, implementação ou validação
manual — apenas registra a decisão fechada do Handoff 3. Até a aplicação, os
contratos e módulos de nomenclatura listados na seção 5 permanecem no estado
atual.

Esta ADR preserva integralmente:

- `schema: tela.v1` e o caráter aditivo e opcional do campo raiz `perfil`
  (ADR-0034 D-SEL-16; `contrato_tela_json.md` §34.1);
- telas existentes sem `perfil`, que continuam válidas sob os contratos
  vigentes, sem migração automática;
- a separação entre JSON estrutural da tela e documento externo de conteúdo
  (ADR-0026, ADR-0027), inclusive para o documento de resultado de execução
  (`docs/nomenclatura/42_DADOS_EXTERNOS_MULTINIVEL.md` §4.5);
- as apresentações `tabela`, `hierarquia` e `conjuntos_campos` já fechadas
  pela ADR-0027 e pela ADR-0028 (`contrato_json_console.md` §12);
- a sessão TTY, o alternate screen e o redimensionamento reativo vigentes
  (ADR-0016, ADR-0017; `contrato_tela_json.md` §§23-24);
- o protocolo `selecao_execucao.v1` entregue pelo Handoff 1 (`H-0041`) e
  especializado pelo Handoff 2 (ADR-0035);
- os executores e fixtures do `H-0042` (`tela/execucao_focal.py`,
  `demo/executor_sintetico.py`, `demo/demo_execucao_focal.py`,
  `demo/fixtures/h0042_*.json`), sem alteração de comportamento;
- a distinção entre o estado semântico do documento (`sucesso`, `parcial`,
  `falha`) e a classificação do processo (código `0` e JSON válido) já
  fechada por D-SEL-14 e H2-ESP-10/H2-ESP-11;
- a ausência de paginação no perfil `resultado_execucao` (D-SEL-20);
- a ausência do chip `[V]` na tela de resultado (D-SEL-16; D-H3-06);
- a ausência de seleção, cursor e navegação no console de resultado
  (D-H3-02, D-H3-07).

O protocolo provisório de CLI e o schema do documento de sucesso fechados
pela ADR-0035 e implementados por `H-0042` permanecem inalterados; esta ADR
consome esse documento como entrada da regra de escolha (D-H3-10), sem
redefinir seu schema.

## 7. Alternativas consideradas

Não há alternativas de desenho a registrar nesta ADR. As decisões D-H3-01 a
D-H3-19 constituem decisão já fechada fornecida ao autor documental; este
documento não escolhe entre opções nem introduz arquitetura, schema,
comportamento visual ou política além do que foi explicitamente decidido.

## 8. Itens fora de escopo

Permanecem expressamente fora desta ADR e do futuro Handoff 3:

- ativação do chip `Executar`;
- abertura da tela de resultado;
- suspensão da tela de origem;
- retorno e restauração da origem — pertencem expressamente ao Handoff 4;
- binding definitivo com o Pipeline;
- registry ou dispatcher genérico de ações (`ITEM-0004`);
- seleção "Todos" limitada à página atual (item bloqueado por D-SEL-24);
- seleção compartilhada entre consoles (item bloqueado por D-SEL-24);
- escolha de `dry-run` pela interface (item bloqueado por D-SEL-24);
- apresentações adicionais de resultado além de `tabela`, `hierarquia` e
  `conjuntos_campos`;
- paginação da tela de resultado (`ITEM-0003`);
- truncamento ou omissão de conteúdo;
- modo não verboso na tela de resultado (item bloqueado por D-SEL-24);
- modo alternável na tela de resultado (item bloqueado por D-SEL-24);
- colapso de conteúdo multinível (`ITEM-0007`);
- definição global de cor de alerta (`ITEM-0011`).

A atribuição integral da abertura da tela de resultado, da suspensão da
origem, do retorno e da restauração ao Handoff 4 decorre da supersessão
parcial de D-SEL-21 registrada em D-H3-19, e não representa criação de
escopo novo além do já decidido.

Também ficam fora de escopo desta execução: reabertura ou alteração do
`H-0041`; redefinição do protocolo do `H-0042`; alteração do executor
sintético do `H-0042` sem necessidade comprovada posterior; ativação de
`Enter` ou do chip `Executar`; execução de processo real do Pipeline;
criação de tela dinamicamente em runtime; criação de novo tipo funcional de
corpo; criação de novo schema genérico de binding; criação de registry ou
dispatcher genérico; introdução de paginação, truncamento, omissão ou
fallback; hardcoding de cores no renderer; alteração de
`config/estilo.json`; QA, aplicação documental, criação de handoff,
implementação, validação manual e commit.

## 9. Critérios para aplicação

- [ ] `docs/contratos/contrato_tela_json.md`, `docs/contratos/contrato_composicao_corpo.md`,
  `docs/contratos/contrato_barra_de_menus.md`, `docs/contratos/contrato_console.md`
  e `docs/contratos/contrato_json_console.md` foram atualizados conforme a
  tabela de artefatos afetados (seção 5).
- [ ] Somente os módulos proprietários da nomenclatura efetivamente afetados
  (`42`, `43`) foram avaliados e, quando material, atualizados.
- [ ] `docs/adr/INDICE_ADR.md` foi atualizado somente após QA favorável desta
  ADR.
- [ ] `docs/backlog.md` foi atualizado somente quando o fluxo documental
  determinar mudança material do `ITEM-0006`, incluindo a indicação de que o
  futuro handoff é o `H-0043`.
- [ ] O `delta_terminologico` desta aplicação foi registrado no relatório de
  aplicação.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
  documental.
- [ ] Nenhum handoff foi criado na mesma etapa da aplicação documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] A execução de aplicação produziu relatório próprio em
  `docs/relatorios/`.
- [ ] O relatório de aplicação não sobrescreveu relatório de execução
  anterior.
- [ ] A aplicação foi submetida a QA independente.

## 10. Relação com ADR-0034, ADR-0035 e H-0042, e indicação do futuro H-0043

Esta ADR especializa o Handoff 3 já decomposto pela ADR-0034 (D-SEL-21), sem
reabrir D-SEL-01 a D-SEL-10, ressalvada a supersessão parcial e pontual
declarada em D-H3-19 sobre a divisão de responsabilidades entre Handoff 3 e
Handoff 4 — todas as demais decisões de D-SEL-21 e da ADR-0034 permanecem
vigentes e não substituídas. Ela consome, sem redefinir, o protocolo e o
schema do documento de sucesso fechados pela
ADR-0035 (H2-ESP-01 a H2-ESP-18) e implementados por `H-0042` — o documento
de resultado de execução produzido pelo executor sintético é a entrada da
regra de escolha entre documento e envelope (D-H3-10) fechada aqui.

A autorização de implementação das decisões desta ADR permanece sujeita a
handoff próprio, criado em etapa distinta e identificado como `H-0043`. Esta
ADR não cria esse handoff nem autoriza qualquer implementação de código
nesta etapa. O Handoff 4 (integração e validação completa) permanece
responsável pela ativação do chip `Executar`, pela abertura real da tela de
resultado, pela suspensão da origem e pelo retorno e restauração — nenhuma
dessas capacidades é antecipada por esta ADR.

## 11. Bloqueios

nenhum
