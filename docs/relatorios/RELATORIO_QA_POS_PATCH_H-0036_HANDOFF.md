# Relatório de QA pós-patch do H-0036

## 1. Identificação

```yaml
etapa_executada: QA_HANDOFF
tipo_qa: POS_PATCH
handoff: H-0036
arquivo_auditado: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
qa_inicial: H3_BLOCKED_DOCUMENTATION
estado_auditado: CORRIGIDO_AGUARDANDO_QA
implementacao: NAO_INICIADA
auditoria: independente_de_handoff
```

## 2. Escopo da auditoria

Auditoria documental e técnica do H-0036 corrigido contra ADR-0026, ADR-0027 aceita e aplicada, contratos ativos, QA inicial do H-0036, aplicação documental da ADR-0027, estado real do repositório e exequibilidade da futura implementação.

Esta etapa não corrigiu handoff, não implementou código, não criou JSONs, não alterou `demo/demo.py`, não preparou stage e não realizou commit.

## 3. Autoridades e evidências examinadas

Foram examinados integralmente ou por leitura técnica dirigida os documentos obrigatórios listados no prompt, com autoridade normativa final atribuída a:

- `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`
- `docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_json_console.md`
- `docs/NOMENCLATURA.md`

Também foram examinados o QA inicial do H-0036, relatórios de QA/aplicação da ADR-0027, relatórios da ADR-0026, ADR-0025, H-0035, IMP-0035, arquivos técnicos citados nominalmente, suíte canônica atual e JSONs `h0035_*.json`.

## 4. Estado Git

Comandos executados antes da criação deste relatório:

```yaml
branch: master
head: fb9e5be
stage: vazio
git_diff_check: sem_erros
commit_novo: nao_realizado
```

`git status --short` antes deste relatório:

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_console.md
 M docs/contratos/contrato_json_console.md
 M docs/contratos/contrato_tela_json.md
?? docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
?? docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
?? docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
```

`git ls-files --others --exclude-standard` listou somente os artefatos documentais acumulados da ADR-0026, ADR-0027 e H-0036 antes deste relatório. `git diff -- docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` retornou vazio porque o handoff está não rastreado.

## 5. Estado e rastreabilidade do H-0036

Confirmado no handoff:

```yaml
handoff: H-0036
estado: CORRIGIDO_AGUARDANDO_QA
qa_handoff_inicial: H3_BLOCKED_DOCUMENTATION
qa_pos_patch: NAO_REALIZADO
implementacao: NAO_INICIADA
commit: NAO_REALIZADO
numero_preservado: true
novo_handoff_criado_ou_reservado: false
documento_autoaprova: false
adr_0027_como_autoridade_corretiva: true
```

Observação: o frontmatter usa `metadata.status: CORRIGIDO_AGUARDANDO_QA` e `metadata.id: H-0036`; o bloco literal completo com `estado`, `qa_pos_patch`, `implementacao` e `commit` aparece na seção 31.

## 6. Verificação de QAH-0036-001

O problema original foi a ausência de mecanismo normativo suficiente para entregar o JSON externo ao console.

Resultado: corrigido documentalmente. O handoff exige alteração de `demo/demo.py`, associação externa por cenário, carregamento separado dos documentos, ausência de campo de vínculo no JSON estrutural, preservação das origens, entrega separada ao fluxo, preservação de cenários sem conteúdo externo, ausência de leitura pelo modelo/renderizador e ausência de protocolo final com o Pipeline.

Autoridades confirmadas: ADR-0027 D2, D3, D7, D8; `contrato_console.md` §20; `contrato_tela_json.md` §32.

## 7. Verificação de QAH-0036-002

O problema original foi a criação de `config/conteudo/` como convenção global sem autoridade normativa.

Resultado: corrigido quanto ao problema central. O handoff remove `config/conteudo/` das listas normativas, fixa fixtures permanentes em `config/telas/demo/`, exige sufixo `_conteudo.json`, distingue JSON estrutural de JSON externo e declara que a localização não é diretório global definitivo de runtime.

Há, porém, achado de completude no inventário dos JSONs H-0035, registrado em QAHPP-0036-001.

## 8. Verificação de QAH-0036-003

O problema original foi deixar schema de `dados[]`, níveis, nós e validações para decisão da implementação.

Resultado: corrigido documentalmente. O handoff torna obrigatórios envelope, três apresentações, três tipos de nível, declaração de nível, campos comuns de nó, hierarquia por `filhos`, designadores previstos, proibição de resultados físicos e as 20 validações semânticas.

A exceção operacional não pode decidir schema, forma de nós, níveis, apresentações, validações, localização geral das fixtures, responsabilidade do `demo.py` ou protocolo do Pipeline.

## 9. Schema, apresentações, níveis e nós

Confirmados no handoff:

```yaml
envelope: "{tipo, formato, dados}"
tipo: multinivel
apresentacoes:
  - tabela
  - hierarquia
  - conjuntos_campos
tipos_de_nivel:
  - container
  - conteudo
  - nome_valor
campos_de_nivel:
  - id
  - tipo
  - conteudo
  - designador
campos_comuns_de_no:
  - id
  - nivel
hierarquia: filhos
designadores: [nenhum, simbolo, decimal, alfabetico_minusculo, alfabetico_maiusculo, romano_minusculo, romano_maiusculo, decimal_composto, personalizado]
resultados_fisicos_no_json_externo: proibidos
```

## 10. Vinte validações semânticas

As 20 validações aparecem nominalmente na seção 14 do handoff e são cobertas por casos previstos na seção 19.1 para o loader. A cobertura inclui raiz objeto, tipo presente e correto, `multinivel`, `formato`, `dados`, apresentação, níveis, campos de nível, unicidade de IDs, tipos válidos, nós, referência a nível declarado, formas `container`/`conteudo`/`nome_valor`, recursão, ordem, compatibilidade por apresentação e ausência de resultados físicos.

## 11. Inventário dos JSONs do H-0035

Estado técnico confirmado:

```yaml
jsons_H0035_total_confirmado: 26
jsons_H0035_afetados_confirmados: 2
jsons_H0035_preservados_confirmados: 24
```

Inspeção estruturada dos `h0035_*.json` confirmou que apenas:

- `config/telas/demo/h0035_console_com.json` possui console com 12 itens e `distribuicao_matricial`;
- `config/telas/demo/h0035_console_sem.json` possui console com 2 itens e sem `distribuicao_matricial`.

Os outros 24 arquivos não possuem elemento `console` com conteúdo de runtime materialmente afetado. Alguns preservados possuem `itens`, mas em `lancador` ou catálogo, não em `console`.

Defeito: o handoff não registra, para cada um dos 26 arquivos, todos os campos exigidos pelo prompt (`json_externo_correspondente` e `justificativa` ausentes na tabela por arquivo). Ver QAHPP-0036-001.

## 12. JSONs estruturais afetados

Confirmado diretamente:

```yaml
config/telas/demo/h0035_console_com.json:
  contem_console: true
  itens: 12
  textos: "P01 linha ... P12 linha"
  contem_distribuicao_matricial: true
  acao_handoff: ALTERAR_E_SEPARAR
  json_externo_previsto: config/telas/demo/h0035_console_com_conteudo.json

config/telas/demo/h0035_console_sem.json:
  contem_console: true
  itens: 2
  textos: ["Linha alfa", "Linha bravo"]
  contem_distribuicao_matricial: false
  acao_handoff: ALTERAR_E_SEPARAR
  json_externo_previsto: config/telas/demo/h0035_console_sem_conteudo.json
```

## 13. JSONs externos e fixtures

Confirmadas como futuras fixtures permanentes:

- `config/telas/demo/h0036_hierarquia_conteudo.json`
- `config/telas/demo/h0036_tabela_conteudo.json`
- `config/telas/demo/h0036_conjuntos_conteudo.json`
- `config/telas/demo/h0035_console_com_conteudo.json`
- `config/telas/demo/h0035_console_sem_conteudo.json`

O repositório real ainda não possui `h0036_*.json` nem `_conteudo.json`, coerente com `implementacao: NAO_INICIADA`.

## 14. Lista nominal da futura implementação

Contagem real da seção 15.1:

```yaml
arquivos_a_alterar_confirmados: 13
arquivos_a_criar_confirmados: 10
duplicatas: false
diretorios_genericos_ou_curingas: false
```

Arquivos técnicos especialmente exigidos aparecem com classificação correta: `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`, `tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`, `demo/demo.py`, `demo/teste_demo.py`, `demo/teste_diagnostico.py` e `demo/teste_demo_console.py`.

Defeito de coerência: `demo/teste_demo_distribuicao.py` e `config/telas/demo/demo.json` aparecem como `ALTERAR` na seção 15.1 e também dentro de "Preservados sem alteração" na seção 28.1. Ver QAHPP-0036-002.

## 15. Associação externa e demo.py

Confirmado: o handoff exige o ponto de entrada real `python demo/demo.py`, catálogo/mecanismo interno com `cenario`, `json_estrutural` e `json_externo_de_conteudo`, preservação de cenários sem conteúdo externo, ausência de herança de conteúdo anterior e retorno ao catálogo.

O `demo.py` atual ainda carrega apenas a tela estrutural via `carregar_tela`, coerente com ausência de implementação antecipada.

## 16. Testes focais e integrados

Confirmado:

- loader: leitura externa, três apresentações, três tipos de nível, 20 validações, recursão, referências, designadores, blocos específicos e ausência de geometria;
- modelo: entradas separadas, origem, ordem, níveis, pais/filhos, tipos de nó, ausência de leitura e cálculo físico;
- renderizador: três apresentações, designadores concretos, conteúdo direto, nome-valor, hierarquia, placeholder, truncamento, redimensionamento e ausência de leitura;
- integração: pipeline `carregar -> carregar_externo -> construir -> renderizar` para cenários H-0036 e H-0035 afetados.

## 17. Suíte canônica

Confirmados oito scripts atuais e nono futuro:

```yaml
baseline_atual: 8
baseline_atual_executado_nesta_auditoria: true
baseline_atual_resultado: todos_passando
baseline_futuro: 9
novo_script: demo/teste_demo_console.py
```

Resultados observados:

- `tela/teste_loader.py`: 303/303
- `tela/teste_modelo.py`: 169/169
- `tela/teste_renderizador.py`: 1191/1191
- `tela/teste_distribuicao_matricial.py`: 36/36
- `demo/teste_demo.py`: 358/358
- `demo/teste_diagnostico.py`: 41/41
- `demo/teste_demo_distribuicao.py`: 99/99
- `demo/teste_explorar_barra_de_menus.py`: 38/38

## 18. Smoke tests

Confirmado que o handoff exige smoke semântico por cenário com caminho estrutural esperado, caminho externo esperado ou `NENHUM`, identificador semântico esperado, conteúdo incorreto ausente e placeholder presente/ausente. Código zero, ausência de exceção e snapshot derivado da própria saída não bastam.

## 19. Cenários sem conteúdo externo

Confirmado que cenários sem conteúdo externo devem continuar carregando, não abrir fixture inexistente, preservar placeholder ou comportamento histórico, não receber conteúdo de outro cenário e não manter associação residual.

## 20. Regressão do H-0035

Confirmado que a regressão cobre os dois cenários afetados após separação, os 24 preservados por prova material, a distribuição matricial, identidade original, ausência de duplicação e ausência de alteração indevida.

## 21. Demonstração e validação manual

Confirmado que a validação manual:

- usa `python demo/demo.py`;
- possui 12 passos;
- identifica cenário, JSON estrutural e JSON externo;
- cobre maximização, restauração, reduções, redimensionamento livre, quadro mínimo, recuperação e cenário sem conteúdo;
- mantém `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO` até retorno do usuário.

## 22. Relatório de implementação

Confirmado como autorizado:

```text
docs/relatorios/IMP-0036-fornecimento-externo-dados-console-json-multinivel.md
```

O conteúdo obrigatório cobre inventário, alterações estruturais, fixtures, catálogo, API interna efetiva, schema, validações, apresentações, testes, smoke, suíte, demonstração, validação manual, preservação do H-0035, exceções e estado Git. O relatório não pode autoaprovar a implementação.

## 23. Exceção operacional

Confirmado que a exceção operacional exige autorização explícita, arquivo, motivo, escopo e mudança esperada, além de registro no relatório. Ela não autoriza nova arquitetura nem decisão de schema, nós, níveis, apresentações, validações, localização geral de fixtures, responsabilidade do `demo.py` ou protocolo do Pipeline.

## 24. Arquivos preservados e escopo negativo

Escopo negativo confirmado: ADRs, contratos, nomenclatura, produtor Pipeline, protocolo definitivo, stdout, temporários, cache, atualização automática, persistência, versionamento, autenticação, tipo matriz externo, navegação/expansão/recolhimento/paginação interativa, commit e ciclo posterior permanecem fora.

Não permanecem indevidamente fora: schema, validação dos nós, três apresentações, `demo/demo.py`, revisão dos JSONs H-0035, JSONs externos e fixtures permanentes.

Defeito: há conflito textual entre arquivos autorizados e preservados na seção 28.1. Ver QAHPP-0036-002.

## 25. Coerência e exequibilidade

O H-0036 corrigido é implementável sem decisão arquitetural nova quanto aos três achados originais. O fluxo `demo.py -> loader/camada equivalente -> modelo -> renderizador` está fechado; schema, validações e fixtures estão suficientemente normatizados para iniciar implementação.

Entretanto, a exequibilidade documental ainda requer patch por dois problemas internos corrigíveis sem nova ADR: inventário H-0035 incompleto por arquivo e conflito na lista de arquivos preservados/alteráveis.

## 26. Ausência de implementação antecipada

Confirmado:

```yaml
codigo_alterado_pelo_patch_handoff: false
json_criado_ou_alterado: false
demo_py_alterado: false
teste_criado: false
fixture_criada: false
validacao_manual_concluida: false
handoff_aprovado_pelo_proprio_documento: false
stage_preparado: false
commit_realizado: false
```

O estado técnico real ainda mostra `_linhas_console` retornando apenas `"(console)"`, `demo/demo.py` sem import de `json` e sem carregamento externo, e ausência de arquivos `h0036_*`/`*_conteudo.json`.

## 27. Achados

### QAHPP-0036-001

```yaml
id: QAHPP-0036-001
severidade: média
achado_original_relacionado: QAH-0036-002
arquivo: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: "§11 Inventário de inspeção dos JSONs do H-0035"
autoridade_ou_regra_afetada: "Prompt QA_HANDOFF: inventário por arquivo com arquivo, possui_console, possui_conteudo_de_runtime_do_console, classificacao, acao, json_externo_correspondente e justificativa"
evidencia: "A tabela do §11 contém apenas Arquivo, possui_console, possui_conteudo_runtime, materialmente_afetado e ação. Os campos json_externo_correspondente e justificativa não aparecem por arquivo; os externos dos dois afetados aparecem em seções posteriores, mas não há inventário completo dos 26 com todos os campos exigidos."
impacto: "A contagem e a classificação material foram confirmadas tecnicamente, mas o handoff não entrega o inventário nominal completo exigido para QA e futura implementação sem inferência documental."
correcao_necessaria: "Completar o inventário dos 26 JSONs com os campos exigidos por arquivo, incluindo json_externo_correspondente como caminho ou NENHUM e justificativa nominal para alteração ou preservação."
```

### QAHPP-0036-002

```yaml
id: QAHPP-0036-002
severidade: alta
achado_original_relacionado: coerencia_interna
arquivo: docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
secao_ou_trecho: "§15.1 vs §28.1"
autoridade_ou_regra_afetada: "Prompt QA_HANDOFF: nenhum arquivo necessário pode aparecer simultaneamente autorizado e proibido/preservado sem alteração"
evidencia: "§15.1 autoriza ALTERAR `demo/teste_demo_distribuicao.py` e `config/telas/demo/demo.json`; §28.1 lista ambos em 'Preservados sem alteração pela futura implementação', com parênteses indicando que o conteúdo será ou poderá ser atualizado."
impacto: "O executor recebe instruções conflitantes sobre dois arquivos. A intenção parece ser preservar responsabilidade/estrutura histórica enquanto permite atualização, mas a redação vigente contradiz o título da lista de preservados sem alteração."
correcao_necessaria: "Remover esses dois arquivos da lista de preservados sem alteração ou reclassificá-los explicitamente como 'preservar responsabilidade/estrutura histórica, com alteração autorizada conforme §15.1', sem mantê-los sob o título de preservados sem alteração."
```

## 28. Observações

- `QAH-0036-001`, `QAH-0036-002` e `QAH-0036-003` foram resolvidos no núcleo normativo pela ADR-0027 e pelo patch do handoff.
- A fixture de identidade exclusiva é exigida explicitamente para a fixture principal e, em conjunto com os smoke tests por cenário, é suficiente para guiar a implementação; não foi registrado achado separado.
- O frontmatter não replica literalmente todas as chaves da seção 31, mas o estado vigente está registrado no documento.
- A execução da suíte atual foi usada apenas como evidência auxiliar de baseline; ela não aprova a futura implementação do H-0036.

## 29. Classificação final

```yaml
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: Patch documental requerido antes da implementação
relatorio: docs/relatorios/RELATORIO_QA_POS_PATCH_H-0036_HANDOFF.md
achados_bloqueantes: 0
achados_altos: 1
achados_medios: 1
achados_baixos: 0
observacoes: 4

QAH-0036-001_corrigido: true
QAH-0036-002_corrigido: true
QAH-0036-003_corrigido: true

inventario_H0035_confirmado: parcialmente
jsons_H0035_total_confirmado: 26
jsons_H0035_afetados_confirmados: 2
jsons_H0035_preservados_confirmados: 24

arquivos_a_alterar_confirmados: 13
arquivos_a_criar_confirmados: 10
fixtures_por_apresentacao_confirmadas: true
demo_py_confirmado: true
catalogo_confirmado: true
schema_confirmado: true
validacoes_confirmadas: true
suite_canonica_confirmada: true
validacao_manual_confirmada: true
relatorio_implementacao_confirmado: true
PATCH_IMPLEMENTACAO_exequivel: false
arquivos_inesperados: nenhum_fora_do_conjunto_conhecido_antes_deste_relatorio
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
proxima_categoria: PATCH_HANDOFF
```
