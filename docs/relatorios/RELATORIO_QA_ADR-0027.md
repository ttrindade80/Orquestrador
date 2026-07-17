# Relatório de QA da ADR-0027

## 1. Identificação

```yaml
etapa_executada: QA_ADR
adr: ADR-0027
arquivo_auditado: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
data: "2026-07-17"
papel: auditor_documental_independente
handoff_relacionado: H-0036
```

## 2. Escopo da auditoria

Esta auditoria verificou exclusivamente a ADR-0027 contra as decisões explícitas
do usuário, a ADR-0026 aplicada, os contratos ativos, o bloqueio documental do
H-0036 e as fronteiras entre ponto de entrada, loader, modelo e renderizador.

Nenhuma correção foi feita na ADR. Nenhum handoff, contrato, JSON, teste,
demonstração ou código foi alterado. Este relatório é o único arquivo criado
nesta etapa.

## 3. Autoridades e evidências examinadas

Foram lidos e examinados:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_ADR-0026.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
```

Também foram inspecionados, somente para confirmação técnica:

```text
demo/demo.py
demo/teste_demo.py
demo/teste_diagnostico.py
config/telas/demo/
tela/loader.py
tela/modelo.py
tela/renderizador.py
```

## 4. Estado Git

Comandos executados antes da criação deste relatório:

```bash
git status --short
git diff --check
git ls-files --others --exclude-standard
git branch --show-current
git rev-parse --short HEAD
```

Estado verificado:

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
git_diff_check: sem_erros
modificados_acumulados:
  - docs/NOMENCLATURA.md
  - docs/adr/INDICE_ADR.md
  - docs/contratos/contrato_console.md
  - docs/contratos/contrato_json_console.md
  - docs/contratos/contrato_tela_json.md
nao_rastreados_acumulados:
  - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  - docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
  - docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
arquivos_inesperados_antes_deste_relatorio: []
arquivo_criado_nesta_etapa:
  - docs/relatorios/RELATORIO_QA_ADR-0027.md
```

O workspace contém os artefatos acumulados da ADR-0026, do H-0036 e da
ADR-0027. Eles não foram classificados como inesperados.

## 5. Decisões explícitas do usuário

Resultado da verificação D1-D12:

| Decisão | Registro na ADR-0027 | Resultado |
|---|---|---|
| D1 — Separação dos documentos | D1, D2, D4, D8 | fiel |
| D2 — Responsabilidade do `demo.py` | D2, D3, D8, §6, §8 | fiel |
| D3 — Demonstração integrada | D3, §8 | fiel |
| D4 — JSONs permanentes | D4, §7 | fiel |
| D5 — Revisão dos JSONs do H-0035 | D5, §7.3 | fiel |
| D6 — Localização das fixtures | D6, §7.4, §14 | fiel com restrição suficiente |
| D7 — Associação no catálogo | D7, §6, §14 | fiel |
| D8 — Entradas separadas no fluxo | D8, §6 | fiel |
| D9 — Fixture provisória e produtor futuro | D9, §9 | fiel |
| D10 — Protocolo do Pipeline deferido | D10, §9.3, §14 | fiel |
| D11 — Estrutura multinível | D11 | fiel quanto ao envelope e à não inferência |
| D12 — Alcance do H-0036 | D12 | parcialmente insuficiente por depender do schema de `dados[]` |

## 6. Fidelidade da ADR-0027

A ADR-0027 registra corretamente a separação entre JSON estrutural e JSON
externo de conteúdo; transfere a associação para o ponto de entrada real
`demo/demo.py`; impede campo de vínculo no `tela.json`; mantém o protocolo do
Pipeline deferido; exige JSONs permanentes; e preserva ADR-0025, H-0035 e
ADR-0026.

A lacuna material está no schema semântico de `dados[]`: a ADR exige
representação multinível material, criação/revisão de fixtures e apresentação
real no console, mas mantém "schema completo e validações de `dados[]`" como
decisão não tomada. As autoridades ativas confirmam apenas envelope,
existência de níveis declarados e proibição de inferência; não definem a forma
mínima de nó, nível, filhos, rótulo, valor ou identidade renderizável.

## 7. Resolução dos achados bloqueantes do H-0036

```yaml
- achado_h0036: QAH-0036-001
  decisao_da_ADR0027_que_o_resolve: D2, D3, D7, D8, §6, §8, §13
  resolucao_suficiente: true
  lacuna_remanescente: >
    A ADR define que demo.py carrega e associa os documentos, sem campo no
    tela.json e sem renderizador abrindo arquivos. Detalhes internos podem
    ficar para implementação.

- achado_h0036: QAH-0036-002
  decisao_da_ADR0027_que_o_resolve: D6, §7.4, §12, §13, §14
  resolucao_suficiente: true
  lacuna_remanescente: >
    A ADR proíbe transformar config/conteudo/ em convenção global definitiva e
    exige que o PATCH_HANDOFF defina nomes/caminhos nominais aderentes à
    organização existente. Isso é suficiente para impedir a escolha arbitrária,
    embora o caminho exato permaneça para o handoff corrigido.

- achado_h0036: QAH-0036-003
  decisao_da_ADR0027_que_o_resolve: D11, D12, §13, §14
  resolucao_suficiente: false
  lacuna_remanescente: >
    A ADR remove a autorização de schema por exceção operacional, mas não
    fornece schema semântico mínimo para dados[]. Como H-0036 deve criar
    fixture, validar conteúdo, transportar representação semântica e apresentar
    no console, o futuro PATCH_HANDOFF ainda não pode executar essa parte sem
    arquitetura nova.
```

## 8. Responsabilidade do ponto de entrada

A ADR-0027 confirma que `demo/demo.py` deve identificar a tela, carregar o JSON
estrutural, carregar o JSON externo quando aplicável, associar os dois
documentos por cenário e entregá-los separadamente ao fluxo.

A inspeção técnica confirma que o `demo/demo.py` atual ainda carrega apenas a
tela estrutural por `_carregar_modelo_por_id`, usando `carregar_tela` e
`construir_modelo`. O estado atual não contradiz a ADR, pois a implementação do
H-0036 ainda não começou.

A ADR não atribui ao `demo.py` cálculos de representação física. Esses seguem
sob responsabilidade do renderizador.

## 9. Separação entre os documentos

A ADR preserva a separação no disco e no fluxo. Ela proíbe reinserir conteúdo
externo no objeto bruto da configuração estrutural e permite apenas uma
representação interna composta quando as origens e responsabilidades continuem
separadas.

O `tela.json` permanece estrutural. O documento externo carrega conteúdo de
runtime. O renderizador produz a representação física.

## 10. Associação externa por cenário

A associação é colocada no catálogo ou mecanismo interno do `demo.py`. A ADR
não cria campo de vínculo no JSON estrutural; não escolhe nome de variável,
classe, função, assinatura, estrutura interna ou argumento de linha de comando;
e não transforma a associação da demonstração em protocolo final do produto.

Esse ponto resolve a falta documental sobre o mecanismo de associação para o
H-0036 sem antecipar API concreta.

## 11. JSONs permanentes e revisão do H-0035

A ADR exige arquivos permanentes para testes, demonstração, validação manual,
prova da separação estrutural e prova da identidade semântica. Também proíbe
dados codificados em teste, demo, renderizador, JSON estrutural ou edição
temporária.

Quanto ao H-0035, a ADR exige inspeção real dos `h0035_*.json`, limita
alterações aos arquivos materialmente afetados, preserva cenários originais,
não presume que todos os JSONs contenham conteúdo de console e não reabre o
estado fechado do H-0035.

A inspeção técnica confirma que há conteúdo de console em JSONs como
`config/telas/demo/h0035_console_com.json` e
`config/telas/demo/h0035_console_sem.json`, mas a lista nominal exata pertence
ao futuro `PATCH_HANDOFF`, como a ADR determina.

## 12. Localização das fixtures

A ADR não fixa `config/conteudo/` como convenção global, não cria diretório de
runtime definitivo e exige aderência à organização existente. Ela deixa nomes e
caminhos exatos ao handoff corrigido, com restrições suficientes:

- distinguir JSON estrutural de JSON de conteúdo;
- ser permanente e repetível;
- não depender de diretório global de runtime ainda não decidido;
- não criar convenção silenciosa do produto final.

Não há local inequívoco já normatizado para conteúdo externo. Ainda assim, para
o escopo de QA da ADR, a restrição é suficiente para impedir arbitrariedade no
handoff corrigido. O bloqueio remanescente não é localização, mas schema.

## 13. Estrutura semântica e schema multinível

O envelope mínimo está preservado:

```json
{
  "tipo": "multinivel",
  "formato": {},
  "dados": []
}
```

A ADR-0026 e os contratos ativos afirmam que `dados` contém estrutura
semântica, que níveis são declarados explicitamente e que o consumidor não
infere hierarquia. Porém, `contrato_json_console.md` §11.2 e §11.8 deixam
schema completo e validações do documento externo para decisão futura.

A ADR-0027 §14 mantém "schema completo e validações de `dados[]`" como não
decididos. Isso é incompatível com o alcance material exigido em D12:
validação do documento externo, representação semântica, apresentação no
console, fixtures permanentes e identidade semântica verificável.

Classificação deste ponto: `ARCHITECTURE_REVIEW_REQUIRED`.

## 14. Demonstração real pelo demo.py

A ADR exige que `demo/demo.py` seja obrigatório para a demonstração integrada.
Demo dedicado pode existir apenas como auxiliar. O cenário deve ser permanente,
sem edição temporária do usuário, e código de saída zero não basta: a identidade
da tela e do conteúdo deve ser comprovada.

Essa parte está fiel às decisões do usuário e corrige a premissa bloqueante do
H-0036 atual, que tratava `demo/demo_console_multinivel.py` como ponto de
entrada da demonstração.

## 15. Fronteira futura com o Pipeline

A ADR registra somente direção futura:

- haverá script produtor;
- origem futura no projeto `Pipeline`;
- dados já adequados ao formato multinível;
- manutenção da mesma fronteira semântica.

Ela não define protocolo concreto de nome, localização, execução, argumentos,
transporte, `stdout`, arquivo temporário, códigos de saída, mensagens de erro,
timeout, sincronismo, autenticação, versionamento, atualização ou cache.

## 16. Compatibilidade

A ADR preserva:

- ADR-0025 e H-0035;
- ADR-0026;
- telas não afetadas;
- placeholder `"(console)"` quando não houver conteúdo externo;
- responsabilidade geométrica do renderizador;
- separação entre demo e produto;
- comportamento histórico para cenários sem conteúdo externo.

Não há reabertura retroativa do H-0035 nem invalidação do commit `fb9e5be`.

## 17. Relação com o H-0036

A ADR mantém o H-0036 como criado e não aprovado. Ela não cancela, não
substitui, não renumera e determina retomada por `PATCH_HANDOFF`.

Ela identifica premissas do H-0036 atual que precisarão ser removidas ou
substituídas: `demo.py` fora do fluxo, demo dedicado como única prova,
`config/conteudo/` como convenção global, schema por exceção operacional,
ausência de revisão nominal dos JSONs do H-0035 e inferência de que envelope
mínimo basta para implementação completa.

## 18. Documentos afetados e aplicação futura

A ADR lista nominalmente, no mínimo:

```text
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
```

Não há afirmação de que esses documentos já foram alterados nesta etapa. A
lista é compatível com o impacto comprovado da decisão.

## 19. Decisões deferidas

Permanecem corretamente deferidos detalhes internos implementáveis:

- nome de variável, classe, função, dicionário, assinatura e argumento de linha
  de comando do mecanismo de associação;
- lista nominal dos JSONs do H-0035 afetados;
- nomes e caminhos exatos das fixtures, sob as restrições da ADR;
- APIs e classes definitivas do consumidor/loader;
- protocolo final do Pipeline.

Permanece indevidamente deferida, para o alcance pretendido do H-0036, a
semântica mínima de `dados[]`.

## 20. Ausência de implementação antecipada

Não há patch do H-0036, alteração de `demo.py`, código, API concreta, classe
concreta, nome de campo, criação de fixture, comando de teste executado ou
afirmação de teste aprovado na ADR-0027.

A ADR também não fornece lista definitiva dos JSONs afetados do H-0035 sem
inspeção, o que está correto.

## 21. Coerência interna

A ADR é coerente nos temas de ponto de entrada, associação externa, fronteira
entre documentos, localização não global, relação com H-0036 e Pipeline.

Contradição material: a ADR declara que não deixa schema semântico obrigatório
para decisão silenciosa na implementação, mas mantém o schema completo de
`dados[]` deferido enquanto exige representação multinível material,
validação, fixtures, identidade semântica e apresentação no console.

## 22. Achados

### QAADR-0027-001

```yaml
id: QAADR-0027-001
severidade: bloqueante
arquivo: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
secao_ou_trecho: D11, D12, §13, §14, §16 item 12
decisao_ou_autoridade_afetada: D11, D12; contrato_json_console.md §§11.2, 11.8; contrato_console.md §19.3; bloqueio QAH-0036-003
evidencia: |
  A ADR exige leitura separada, validação do JSON externo, representação
  semântica, apresentação no console, criação/revisão de JSONs permanentes e
  prova de identidade semântica. Ao mesmo tempo, mantém como não decidido o
  "schema completo e validações de dados[]". As autoridades ativas só definem
  envelope, níveis declarados e proibição de inferência; não definem estrutura
  mínima de nó/nível renderizável.
impacto: |
  O futuro PATCH_HANDOFF ainda precisaria inventar a semântica obrigatória de
  dados[] para criar fixtures, validar níveis, transportar conteúdo no modelo e
  renderizar no console. Isso reabre a lacuna bloqueante QAH-0036-003.
correcao_necessaria: |
  Submeter revisão arquitetural/documental para definir o schema semântico
  mínimo de dados[] necessário ao H-0036, ou reduzir formalmente o alcance do
  H-0036 para não exigir validação, fixture e renderização que dependam desse
  schema. A decisão não deve ser delegada silenciosamente à implementação.
```

## 23. Observações

```yaml
observacoes:
  - id: OBS-QAADR-0027-001
    severidade: observação
    descricao: >
      A ADR-0027 resolve de forma suficiente os bloqueios de ponto de entrada,
      associação sem campo no tela.json e localização não global de fixture.
      Essas partes poderão orientar um PATCH_HANDOFF depois que a lacuna de
      schema for resolvida.
```

## 24. Classificação final

```yaml
status_literal: ARCHITECTURE_REVIEW_REQUIRED
status_normalizado: >
  ADR-0027 exige revisão arquitetural porque ainda não resolve a semântica
  mínima de dados[] indispensável para fixture, validação, representação
  semântica e renderização do H-0036.
relatorio: docs/relatorios/RELATORIO_QA_ADR-0027.md
achados_bloqueantes: 1
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 1
resolucao_h0036:
  QAH-0036-001: resolvido
  QAH-0036-002: resolvido
  QAH-0036-003: nao_resolvido
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
arquivo_criado_nesta_etapa:
  - docs/relatorios/RELATORIO_QA_ADR-0027.md
proxima_categoria: REVISAO_ARQUITETURAL
```
