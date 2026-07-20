---
status_literal: IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: patch_required
historia: H-0037
tipo: QA_POS_PATCH_IMPLEMENTACAO
patch_auditado: terceiro_patch_pos_QA
data: 2026-07-19
---

# RELATORIO QA POS PATCH 3 H-0037 IMPLEMENTACAO

## 1. Identificacao

Auditoria tecnica independente do terceiro patch focal da implementacao H-0037.

Resultado: `IMPLEMENTATION_PATCH_REQUIRED`.

## 2. Objetivo

Verificar se o terceiro patch resolveu integralmente:

- `H0037-IMPL-QAPP2-001`: bypass do D23 por campo de envelope ou estrutura hibrida.
- `H0037-IMPL-QAPP2-002`: coluna reconhecida por valores semanticamente vazios e separacao incompleta V-01/V-14.

## 3. Autoridades

Foram lidos os artefatos obrigatorios indicados no prompt, incluindo os tres QAs anteriores de implementacao, o relatorio `IMP-0037`, o handoff H-0037, o QA pos-patch do handoff, a ADR-0028 e os contratos ativos.

Autoridades principais usadas na decisao:

- `docs/adr/ADR-0028-apresentacoes-conteudo-externo-alternancia-verbosa-console.md`: D23 exige politica em telas novas/revisadas, sem default implicito; `somente_verboso` abre em modo verboso.
- `docs/contratos/contrato_json_console.md`: envelope minimo do console possui tipos e regras obrigatorias; V-01 e V-14 sao invalidacoes obrigatorias.
- `docs/contratos/contrato_tela_json.md`, `docs/contratos/contrato_console.md`, `docs/contratos/contrato_composicao_corpo.md`, `docs/contratos/contrato_barra_de_menus.md`.

## 4. Estado Git

```yaml
branch: master
head: f6982d08640af1762b8e0e8814b6e90c9421538e
head_log: "f6982d0 docs: corrige whitespace do fechamento H-0036"
stage: vazio
commit_novo: inexistente
push: inexistente
git_diff_check: sem_erros
```

Arquivos modificados rastreados:

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

Arquivos nao rastreados relevantes incluem os JSONs H-0037, `demo/teste_demo_console_modos.py`, ADR/handoff/relatorios H-0037/ADR-0028 e artefatos transitorios `tela/__pycache__/` e `demo/__pycache__/teste_demo_console_modos.cpython-314.pyc`.

Para itens inesperados:

```yaml
arquivo: "demo/__pycache__/teste_demo_console_modos.cpython-314.pyc"
origem: NAO_CONFIRMADA
produzido_pelo_terceiro_patch: NAO_CONFIRMADO
arquivo: "tela/__pycache__/"
origem: NAO_CONFIRMADA
produzido_pelo_terceiro_patch: NAO_CONFIRMADO
```

## 5. Escopo do Terceiro Patch

O executor declarou alteracao apenas em:

```text
tela/loader.py
tela/teste_loader.py
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md
```

Confirmacao por diff:

```yaml
tela/loader.py:
  numstat: "462 insertions, 2 deletions"
tela/teste_loader.py:
  numstat: "639 insertions, 42 deletions"
docs/relatorios/IMP-0037-apresentacao-multinivel-console-alternancia-verbosa.md:
  estado_git: untracked
```

Nao ha evidencia suficiente para atribuir os demais arquivos modificados ao terceiro patch.

## 6. Integridade

```yaml
python_ast_parse:
  tela/loader.py: OK
  tela/teste_loader.py: OK
  demo/teste_demo_console_modos.py: OK
json_loads:
  config/telas/demo/demo.json: OK
  config/telas/demo/h0037_console_nao_verboso.json: OK
  config/telas/demo/h0037_console_verboso_dois_niveis.json: OK
  config/telas/demo/h0037_console_alternavel_tres_niveis.json: OK
  config/telas/demo/h0037_console_tabela_alternavel.json: OK
  config/telas/demo/h0037_dois_niveis_conteudo.json: OK
  config/telas/demo/h0037_tres_niveis_conteudo.json: OK
  config/telas/demo/h0037_tabela_conteudo.json: OK
conflitos:
  busca_inicio_linha: nenhum marcador real encontrado
temporarios:
  - tela/__pycache__
  - tela/__pycache__/loader.cpython-314.pyc
  - tela/__pycache__/teste_loader.cpython-314.pyc
  - demo/__pycache__/teste_demo_console_modos.cpython-314.pyc
```

## 7. Sete Campos de Envelope

Campos identificados em `_CAMPOS_ENVELOPE_PRE_ADR_0028`:

```yaml
campos_de_envelope:
  - itens
  - origem_dados
  - politica_composicao
  - politica_navegacao
  - politica_selecao
  - politica_paginacao
  - politica_exibicao
```

## 8. Classificacao em Tres Estados

Implementacao observada:

```yaml
zero_campos_de_envelope: em_escopo_D23_salvo_legado_nominal
sete_campos_de_envelope: fora_de_escopo_D23_salvo_hibrido_com_politica_modo_ou_modo_inicial
um_a_seis_campos_de_envelope: TelaEstruturaInvalida
```

Problema: sete campos sao aceitos por presenca de chaves, sem validar tipos, valores obrigatorios e subestruturas do envelope minimo. Isso viola a exigencia contratual de envelope valido.

## 9. Matriz Adversarial D23

```yaml
D23-QA3-01_consumidor_valido_com_politica: ACEITO
D23-QA3-02_consumidor_sem_politica: REJEITADO
D23-QA3-03_consumidor_sem_formato_excesso: REJEITADO
D23-QA3-04_consumidor_ID_arbitrario_sem_politica: REJEITADO
D23-QA3-05_campos_isolados:
  itens: REJEITADO
  origem_dados: REJEITADO
  politica_composicao: REJEITADO
  politica_navegacao: REJEITADO
  politica_selecao: REJEITADO
  politica_paginacao: REJEITADO
  politica_exibicao: REJEITADO
D23-QA3-06_combinacoes_2_a_6: REJEITADAS
D23-QA3-07_sete_campos_invalidos:
  all_null: ACEITO
  wrong_types: ACEITO
  semantic_invalid: ACEITO
D23-QA3-08_envelope_historico_valido: ACEITO
D23-QA3-09_envelope_historico_incompleto: REJEITADO
D23-QA3-10_estrutura_hibrida_com_D23: REJEITADO
D23-QA3-11_cinco_legados_nominais: ACEITOS
D23-QA3-12_copia_renomeada_de_legado: REJEITADA
D23-QA3-13_prefixos_semelhantes: REJEITADOS
D23-QA3-14_campo_legado_excesso_modo: REJEITADO
```

## 10. Envelopes Incompletos

O caso de 1 a 6 campos agora rejeita. Entretanto, a regressao em `config/telas/demo/demo.json` mostra que a classificacao "todos ou nenhum" esta grosseira demais para a base existente: o console real `console_principal` possui 6 dos 7 campos historicos e `regra_geracao_itens`, e passou a quebrar `carregar_tela(demo)`.

## 11. Estruturas Hibridas

Envelope completo com `formato.excesso.politica_modo` foi rejeitado. A deteccao atual depende dos campos D23 em `formato.excesso`; nao ha validacao estrutural completa do envelope antes da isencao.

## 12. Cinco Legados

```yaml
h0035_console_com: ACEITO
h0035_console_sem: ACEITO
h0036_console_hierarquia: ACEITO
h0036_console_tabela: ACEITO
h0036_console_conjuntos: ACEITO
copia_renomeada: REJEITADA
prefixos_semelhantes: REJEITADOS
```

## 13. `_coluna_reconhecivel`

`_coluna_reconhecivel` rejeita corretamente `None`, string vazia e whitespace para `titulo`, `nivel`, `campo` e strings simples. Porem o criterio tambem reconhece objetos por `titulo` nao vazio mesmo sem origem; isso so e valido se V-14 rejeitar depois.

## 14. Matriz V-01

```yaml
ausente: V-01
nulo: V-01
lista_vazia: V-01
[null]: V-01
[1]: V-01
[true]: V-01
[{}]: V-01
[""]: V-01
["   "]: V-01
[{"titulo": null}]: V-01
[{"titulo": ""}]: V-01
[{"titulo": "   "}]: V-01
[{"nivel": null}]: V-01
[{"nivel": ""}]: V-01
[{"nivel": "   "}]: V-01
[{"campo": null}]: V-01
[{"campo": ""}]: V-01
[{"campo": "   "}]: V-01
lista_apenas_invalidos: V-01
coluna_string_valida: ACEITO
texto_com_espacos_externos: ACEITO
```

Observacao: lista mista `[entrada_invalida, coluna_valida]` foi aceita. Nao localizei autoridade explicita que autorize filtragem silenciosa de entradas invalidas; como ha achados bloqueantes independentes, isto fica como observacao de risco.

## 15. Separacao V-01/V-14

Casos V-14 testados com cabecalho valido:

```yaml
titulo_sem_origem:
  ultrapassou_V_01: true
  causa: V-14
largura_sem_origem:
  ultrapassou_V_01: true
  causa: V-14
campo_vazio:
  observado: ACEITO
nivel_vazio:
  observado: ACEITO
campo_null:
  observado: ACEITO
nivel_null:
  observado: ACEITO
```

A separacao esta incompleta: V-14 rejeita apenas ausencia das chaves `nivel` e `campo`, mas aceita origem semanticamente vazia ou nula.

## 16. Testes Novos

Resumo da auditoria dos testes declarados:

```yaml
V-01_P3-01_a_P3-10:
  passa_pelo_carregador_real: validar_conteudo_externo
  conforme_para_V_01: true
V-01_vs_V-14_corrigido:
  resultado_observado: passa quando mensagem contem V-14
  lacuna: nao cobre campo/nivel nulo ou vazio em formato.tabela.colunas
D23-06_envelope_completo:
  passa_pelo_carregador_real: carregar_tela
  conforme_parcial: true
  lacuna: nao valida tipos/valores do envelope
D23-P3-05_a_P3-12:
  passa_pelo_carregador_real: carregar_tela
  conforme_parcial: true
  lacunas:
    - sete_campos_invalidos_nao_testados
    - regressao_demo_json_nao_detectada
verificacoes_diretas_private:
  existem: true
  risco: nao substituem carregar_tela
```

## 17. Preservacao das Correcoes Anteriores

```yaml
modos_iniciais:
  h0037_console_nao_verboso: nao_verboso
  h0037_console_verboso_dois_niveis: nao_verboso
  esperado_para_h0037_console_verboso_dois_niveis: verboso
  h0037_console_alternavel_tres_niveis: nao_verboso
  h0037_console_tabela_alternavel: verboso
tecla_V:
  telas_fixas: inerte
  telas_alternaveis: reversivel
V_04:
  folha_sem_filhos: aceita
  folha_com_filhos_vazio: rejeitada
  folha_com_filho_real: rejeitada
conteudo_compartilhado:
  identidade: H-0037 conteudo_dois_niveis
  varia_por_tela: false
inventario_legado:
  total: 5
  autoridade: confirmada_no_QA_anterior
regressao_H_0036:
  preservada: true
regressao_demo_raiz:
  preservada: false
```

`demo/demo.py` retorna `False` para toda politica que nao seja `alternavel` com `modo_inicial == "verboso"`. Isso contraria D23 para `somente_verboso`.

## 18. Relatorio IMP-0037

A secao 32 registra corretamente a origem QA, os dois achados tratados, os sete campos e a conclusao "implementacao corrigida e aguardando novo QA independente".

Porem o relatorio nao registra:

- que sete chaves invalidas continuam aceitas;
- que a suite focal `tela/teste_loader.py` falha e aborta;
- que `h0037_console_verboso_dois_niveis` abre como `nao_verboso`;
- que V-14 aceita `campo`/`nivel` nulos ou vazios.

Logo, a declaracao de correcao integral nao e sustentada pela auditoria adversarial.

## 19. Testes Focais

```yaml
script: tela/teste_loader.py
codigo_saida: 1
verificacoes_registradas_ate_abort: 57
falhas_registradas_ate_abort: 10
abortou_com: TelaEstruturaInvalida
causa: "elementos console com 2 ou 6 campos de envelope rejeitados"

script: demo/teste_demo_console_modos.py
codigo_saida: 0
verificacoes: 63
falhas: 0
observacao: "teste espera incorretamente modo inicial False para somente_verboso"
```

## 20. Suite Independente

```yaml
suite_anterior:
  scripts: 10
  verificacoes: 2601
  falhas: 0
suite_executada_pelo_QA:
  scripts: 10
  verificacoes_registradas_ate_abortos: 640
  falhas_registradas: 22
  abortos_nao_contabilizados_como_verificacao: 3
  codigo_saida_global: falha
por_script:
  tela/teste_loader.py:
    codigo_saida: 1
    verificacoes_registradas_ate_abort: 57
    falhas_registradas_ate_abort: 10
  tela/teste_modelo.py:
    codigo_saida: 1
    verificacoes: 148
    falhas: 3
  tela/teste_renderizador.py:
    codigo_saida: 1
    verificacoes_registradas_ate_abort: 20
    falhas_registradas_ate_abort: 1
  tela/teste_distribuicao_matricial.py:
    codigo_saida: 0
    verificacoes: 36
    falhas: 0
  demo/teste_demo.py:
    codigo_saida: 1
    verificacoes_registradas_ate_abort: 25
    falhas_registradas_ate_abort: 0
  demo/teste_diagnostico.py:
    codigo_saida: 1
    verificacoes: 28
    falhas: 4
  demo/teste_demo_distribuicao.py:
    codigo_saida: 1
    verificacoes: 109
    falhas: 2
  demo/teste_explorar_barra_de_menus.py:
    codigo_saida: 0
    verificacoes: 38
    falhas: 0
  demo/teste_demo_console.py:
    codigo_saida: 1
    verificacoes: 116
    falhas: 2
  demo/teste_demo_console_modos.py:
    codigo_saida: 0
    verificacoes: 63
    falhas: 0
```

## 21. Smoke Tecnico

```yaml
h0037_console_nao_verboso:
  primeiro_modo: nao_verboso
h0037_console_verboso_dois_niveis:
  primeiro_modo: nao_verboso
  esperado: verboso
h0037_console_alternavel_tres_niveis:
  primeiro_modo: nao_verboso
h0037_console_tabela_alternavel:
  primeiro_modo: verboso
```

Nao houve aprovacao visual.

## 22. Validacao Manual

Permanece:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Nao foi executada validacao manual em nome do usuario.

## 23. Achados

```yaml
- id: H0037-IMPL-QAPP3-001
  arquivo: tela/loader.py
  funcao_ou_teste: _console_em_escopo_d23 / carregar_tela
  evidencia: "D23-QA3-07 aceitou all_null, wrong_types e semantic_invalid com os sete campos de envelope; suite tambem falha em demo.json por classificar 6 campos reais como estrutura incompativel."
  autoridade: "contrato_json_console.md secao 5; ADR-0028 D23; contrato_json_console.md secao 13.13"
  severidade: ALTA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Estrutura invalida pode receber isencao D23 apenas por presenca de chaves; ao mesmo tempo, estrutura real existente fica rejeitada e quebra a suite canonica."
  correcao_exigida: "Validar envelope historico por forma contratual completa antes de isentar D23; separar corretamente envelope historico valido, consumidor D23, legado nominal e estruturas invalidas/hibridas sem depender apenas da contagem de chaves."

- id: H0037-IMPL-QAPP3-002
  arquivo: tela/loader.py; demo/demo.py; demo/teste_demo_console_modos.py
  funcao_ou_teste: "_coluna_reconhecivel / validacao V-14 / _modo_verboso_de_modelo"
  evidencia: "V-14 aceita colunas com campo/nivel null ou string vazia; _modo_verboso_de_modelo retorna nao_verboso para politica somente_verboso; o teste focal espera esse valor incorreto."
  autoridade: "contrato_json_console.md V-14; ADR-0028 D23 classes de politica"
  severidade: ALTA
  tipo: DEFEITO_IMPLEMENTACAO
  impacto: "Origem de coluna semanticamente vazia passa como valida; tela somente verbosa abre no modo errado; teste verde mascara semantica incorreta."
  correcao_exigida: "Aplicar validacao semantica tambem em V-14 para nivel/campo; corrigir modo inicial de somente_verboso e atualizar teste para esperar verboso."
```

## 24. Conclusao

O terceiro patch corrigiu a rejeicao de campos isolados e de combinacoes parciais simples, e melhorou V-01 para valores semanticamente vazios. Ainda assim, nao resolveu integralmente os achados QAPP2:

- sete campos de envelope invalidos continuam sendo aceitos;
- a classificacao D23 quebra a suite existente e o `demo.json`;
- V-14 ainda aceita origem nula/vazia;
- o modo inicial `somente_verboso` esta errado e o teste focal codifica o erro.

## 25. Status Literal

```text
IMPLEMENTATION_PATCH_REQUIRED
```

## 26. Status Normalizado

```text
patch_required
```

## 27. Proxima Categoria

```yaml
proxima_categoria: PATCH_IMPLEMENTACAO
```
