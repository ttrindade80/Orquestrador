# Relatório de QA da aplicação da ADR-0027

## 1. Identificação

```yaml
etapa_executada: QA_APLICACAO_ADR
adr: ADR-0027
arquivo_adr: docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
data: "2026-07-17"
papel: auditor_documental_independente
handoff_relacionado: H-0036
relatorio_auditado: docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
```

## 2. Escopo da auditoria

Esta auditoria verificou a aplicação documental da ADR-0027 contra a ADR
aprovada, o QA pós-patch da ADR, os contratos e a nomenclatura atualizados, o
relatório de aplicação, os três bloqueios documentais do H-0036 e o estado real
do repositório.

Nenhum documento normativo foi corrigido. Nenhuma ADR, contrato, handoff, JSON,
demo, teste ou código foi alterado. Este relatório é o único arquivo criado por
esta etapa.

## 3. Autoridades e evidências examinadas

Foram examinados:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/relatorios/RELATORIO_QA_ADR-0027.md
docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md
docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
docs/relatorios/IMP-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md
```

Também foram usadas evidências de `git status --short`, `git diff --name-only`,
`git diff --check`, `git ls-files --others --exclude-standard`, diffs focais dos
contratos alterados e buscas textuais por resíduos documentais.

## 4. Estado Git

Estado antes da criação deste relatório:

```yaml
branch: master
head: fb9e5be
stage: vazio
commit_novo: nao_realizado
git_diff_check: sem_erros
modificados_rastreados:
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
  - docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0026.md
  - docs/relatorios/RELATORIO_QA_H-0036_HANDOFF.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0027.md
  - docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0026.md
```

O diff rastreado dos cinco documentos alterados mostra 957 inserções e 1
remoção. Os arquivos não rastreados correspondem ao ciclo documental acumulado
da ADR-0026, ADR-0027 e H-0036; não foram classificados como inesperados.

## 5. Fidelidade do relatório de aplicação

O relatório de aplicação é fiel ao estado observado:

- lista os seis documentos alterados autorizados;
- lista o relatório de aplicação como arquivo criado;
- informa corretamente o status `APLICACAO_CONCLUIDA`;
- registra a atualização do status da ADR-0027;
- registra a entrada no índice;
- descreve a seção 18 da nomenclatura;
- descreve as seções 32, 20 e 12 nos contratos;
- registra as três apresentações, os três tipos de nível, designadores e as 20 validações;
- registra a responsabilidade do `demo/demo.py`;
- preserva decisões deferidas;
- confirma ausência de alteração do H-0036, código, JSONs e `demo.py`;
- confirma stage vazio, ausência de commit e `git diff --check` sem erros.

Não foi encontrada divergência material entre o relatório de aplicação e o
estado real do repositório.

## 6. Estado da ADR-0027 e índice

A ADR-0027 está vigente como `aceita e aplicada` em:

```yaml
frontmatter: metadata.status
tabela_identificacao: Status
secao_2_status: literal `aceita e aplicada`
indice_adr: linha ADR-0027
```

O índice contém ADR-0027 após ADR-0026, com título, data, caminho lógico e
status coerentes. O índice não declara H-0036 aprovado ou implementado. As
referências históricas ao bloqueio anterior do H-0036 foram preservadas
corretamente.

## 7. Aplicação na nomenclatura

`docs/NOMENCLATURA.md` recebeu a seção 18, que define de forma inequívoca:

- JSON estrutural da tela e JSON externo de conteúdo;
- associação externa por cenário e campo de vínculo proibido;
- ponto de entrada da demonstração;
- loader ou camada equivalente;
- fixture permanente de conteúdo;
- produtor futuro ligado ao Pipeline;
- schema semântico multinível;
- nível declarado, nó multinível e tipos `container`, `conteudo`, `nome_valor`;
- designador como política declarativa, não numeração concreta calculada.

Não foram encontrados aliases normativos concorrentes. A fixture permanente não
foi confundida com diretório global definitivo de runtime. O produtor futuro não
foi confundido com o consumidor atual.

## 8. Aplicação no contrato do JSON estrutural

`docs/contratos/contrato_tela_json.md` preserva o JSON de tela como estrutural.
A seção 32 confirma que:

- conteúdo de runtime fica em documento separado;
- não há campo obrigatório de vínculo no `tela.json`;
- a associação ocorre externamente ao JSON estrutural;
- conteúdo externo não pode ser duplicado nem reinserido como configuração;
- representação interna composta pode existir sem apagar a separação de origens;
- telas sem conteúdo externo preservam comportamento histórico;
- JSONs do H-0035 materialmente afetados serão revisados pelo H-0036.

O contrato não inventa nome de campo, caminho, argumento, variável de ambiente,
protocolo, fallback ou política de erro.

## 9. Aplicação no contrato do console

`docs/contratos/contrato_console.md` formaliza o fluxo:

```text
ponto de entrada
→ carregamento e validação
→ modelo semântico
→ renderizador
```

O ponto de entrada identifica cenário, carrega JSON estrutural, carrega JSON
externo quando aplicável, associa externamente e entrega entradas separadas.
No cenário de demonstração integrada, essa responsabilidade pertence a
`demo/demo.py`.

O loader lê, valida e converte sem calcular geometria nem inferir hierarquia. O
modelo preserva conteúdo semântico, ordem, níveis e relação pai-filho, sem abrir
arquivos, escolher fonte ou calcular representação física. O renderizador recebe
representação semântica, calcula resultados físicos e designadores concretos,
sem abrir JSONs nem inferir hierarquia de domínio.

## 10. Aplicação no contrato do JSON externo

`docs/contratos/contrato_json_console.md` é o contrato principal da aplicação.
A seção 11 foi reconciliada com a ADR-0027: o envelope mínimo passou a ser ponto
de partida, e schema completo/validações deixaram de constar como decisões
deferidas. A seção 12 propagou o schema semântico multinível completo.

Não há redução silenciosa do H-0036 a uma única apresentação. Não há campo de
vínculo imposto ao JSON estrutural. `origem_dados` permanece tratado como campo
histórico do envelope do console, sem ser declarado mecanismo final de vínculo.

## 11. Envelope e apresentações multinível

O contrato define o envelope raiz:

```json
{
  "tipo": "multinivel",
  "formato": {
    "apresentacao": "hierarquia",
    "niveis": []
  },
  "dados": []
}
```

Regras confirmadas: raiz objeto; `tipo` obrigatório e igual a `"multinivel"`;
`formato` obrigatório e objeto; `dados` obrigatório e array;
`formato.apresentacao` obrigatório; `formato.niveis` obrigatório e array;
níveis declarados explicitamente; hierarquia não inferida.

As apresentações propagadas são:

```text
tabela
hierarquia
conjuntos_campos
```

O bloco `tabela` é compatível apenas com `tabela`; o bloco `campos`, apenas com
`conjuntos_campos`; e nenhum deles pertence a `hierarquia`. O exemplo com
`"hierarquia"` não torna essa apresentação única ou obrigatória.

## 12. Níveis, nós e designadores

Cada nível exige `id`, `tipo`, `conteudo` e `designador`. `id` deve ser string
não vazia e única; `tipo` pertence a `container`, `conteudo` ou `nome_valor`;
`conteudo` indica os campos exibíveis; `designador` declara uma política.

Para `container` e `conteudo`, `conteudo` é o nome do campo textual. Para
`nome_valor`, `conteudo` declara campos de nome e valor. O contrato permite que
os nomes dos campos sejam declarados pelo próprio nível, sem fixar os literais
dos exemplos como únicos.

Designadores propagados:

```text
nenhum
simbolo
decimal
alfabetico_minusculo
alfabetico_maiusculo
romano_minusculo
romano_maiusculo
decimal_composto
personalizado
```

Campos condicionais previstos: `prefixo`, `sufixo`, `valor`, `separador`. O
JSON declara política; o renderizador calcula a sequência concreta.

## 13. Validações semânticas

As 20 validações semânticas foram propagadas nominalmente:

1. raiz é objeto;
2. presença e tipo correto de `tipo`;
3. valor de `tipo` igual a `"multinivel"`;
4. presença e tipo objeto de `formato`;
5. presença e tipo array de `dados`;
6. presença de `formato.apresentacao`;
7. apresentação válida;
8. presença e tipo array de `formato.niveis`;
9. cada nível com `id`, `tipo`, `conteudo` e `designador`;
10. IDs de nível não vazios e únicos;
11. tipos de nível válidos;
12. cada nó com `id` e `nivel`;
13. referência a nível declarado;
14. forma válida de `container`;
15. forma válida de `conteudo`;
16. forma válida de `nome_valor`;
17. filhos validados recursivamente;
18. ordem dos arrays preservada;
19. blocos compatíveis com a apresentação;
20. ausência de resultados físicos calculados.

Não se trata apenas de declaração quantitativa: cada regra aparece como item
material no contrato.

## 14. Separação entre conteúdo e geometria

O documento externo não pode armazenar largura efetiva, altura efetiva,
quantidade física calculada de linhas ou colunas, posição final, coordenada
física, página calculada, quebra física pronta, truncamento aplicado,
distribuição concreta do espaço restante, células vazias calculadas, geometria
final ou numeração concreta de designadores.

Essa lista é coerente com ADR-0025 e ADR-0026: semântica e intenção ficam no
documento externo; representação física fica no renderizador.

## 15. JSONs permanentes e revisão do H-0035

A aplicação formaliza fixtures permanentes para H-0036, separação entre JSON
estrutural e conteúdo, aderência ao contrato e definição nominal futura no
`PATCH_HANDOFF`. Ela não cria diretório global definitivo de runtime nem permite
conteúdo codificado em Python.

O H-0036 deverá inspecionar os JSONs `h0035_*.json`, listar apenas os
materialmente afetados, separar estrutura e conteúdo quando necessário e
preservar identidade e finalidade original sem reabrir o fechamento do H-0035.

## 16. Responsabilidade do demo.py

A responsabilidade do `demo/demo.py` foi propagada para ADR, nomenclatura,
contrato de tela e contrato do console. A demonstração integrada deve ocorrer
por esse ponto de entrada. Demo auxiliar pode existir, mas não é prova única.
JSONs permanentes são obrigatórios, a identidade da tela e do conteúdo deve ser
comprovada, e código de saída zero não basta.

## 17. Fronteira futura com o Pipeline

A aplicação decidiu somente que o produtor futuro buscará dados no Pipeline,
entregará documento compatível com o mesmo schema e substituirá a fixture sem
alterar a fronteira semântica.

Permanecem deferidos: nome do script, localização, execução, argumentos,
transporte, `stdout`, arquivo temporário, códigos de saída, mensagens de erro,
timeout, autenticação, atualização, cache, persistência e versionamento.

## 18. Resíduos e contradições

Busca focal nos documentos alterados:

| Formulação | Classificação |
|---|---|
| `schema completo deferido` | não encontrada como regra ativa vigente |
| `schema futuro` | não encontrada como regra ativa vigente |
| `validação de dados[] futura` | não encontrada como regra ativa vigente |
| `envelope mínimo` | ativa e coerente; tratado como ponto de partida, não schema completo |
| `demo dedicado` | histórica ou ativa coerente; não pode ser prova única |
| `config/conteudo` | histórica na ADR, descrevendo bloqueio do H-0036 |
| `campo de vínculo` | ativa e coerente; campo proibido no JSON estrutural |
| `origem_dados` | ativa e coerente; não é mecanismo final de vínculo |
| `hierarquia inferida` / `níveis inferidos` | ativa e coerente; inferência proibida |
| `renderizador abre` / `modelo escolhe` | não encontrada como regra ativa permissiva |
| `dados codificados em Python` | não encontrada como regra ativa permissiva |
| `tipo matriz` / `tipo: "matriz"` | ativa e coerente; suporte permanece deferido |

Os resíduos declarados `RES-01` e `RES-02` existiam no contrato do JSON do
console e foram corrigidos sem apagar decisões realmente deferidas.

## 19. Resolução dos bloqueios do H-0036

```yaml
QAH-0036-001:
  achado: mecanismo de entrega do documento externo sem autoridade ativa
  autoridade_ativa_que_agora_o_resolve:
    - ADR-0027 D2, D3, D7, D8
    - contrato_console.md secao 20
    - contrato_tela_json.md secao 32
    - NOMENCLATURA.md secao 18
  regra_propagada: demo/demo.py carrega, associa externamente e entrega entradas separadas
  correcao_exigida_no_PATCH_HANDOFF: substituir demo dedicado como prova unica e incluir demo/demo.py no fluxo
  resolvido_documentalmente: true
  lacuna_remanescente: nenhuma impeditiva

QAH-0036-002:
  achado: config/conteudo como primeira convencao global sem autoridade
  autoridade_ativa_que_agora_o_resolve:
    - ADR-0027 D6, D12, secao 7.4, secao 14
    - contrato_json_console.md secao 12.8
    - NOMENCLATURA.md secao 18.5
  regra_propagada: fixture permanente segue organizacao existente; caminhos nominais ficam no PATCH_HANDOFF; sem diretorio global definitivo
  correcao_exigida_no_PATCH_HANDOFF: definir caminhos nominais aderentes ao repositorio sem declarar convencao global de runtime
  resolvido_documentalmente: true
  lacuna_remanescente: nenhuma impeditiva

QAH-0036-003:
  achado: schema interno de dados[] e validacoes deixados para implementacao/excecao
  autoridade_ativa_que_agora_o_resolve:
    - ADR-0027 D11, D13
    - contrato_json_console.md secao 12
    - NOMENCLATURA.md secao 18.2
  regra_propagada: envelope, apresentacoes, niveis, nos, designadores, exemplo normativo, resultados proibidos e 20 validacoes
  correcao_exigida_no_PATCH_HANDOFF: substituir schema por excecao operacional pelo schema semantico propagado
  resolvido_documentalmente: true
  lacuna_remanescente: nenhuma impeditiva
```

## 20. Exequibilidade do futuro PATCH_HANDOFF

Com a aplicação vigente, o autor do `PATCH_HANDOFF` pode:

- inspecionar nominalmente os JSONs do H-0035;
- listar os JSONs afetados;
- definir caminhos de fixtures segundo a organização existente;
- incluir `demo/demo.py` no escopo;
- retirar demo dedicado como única prova;
- definir entradas separadas;
- exigir o schema multinível;
- exigir as três apresentações;
- exigir os três tipos de nível;
- exigir as 20 validações;
- criar testes e fixtures sem inventar semântica;
- preservar o protocolo do Pipeline como futuro.

Nenhuma dessas ações depende agora de decisão arquitetural nova.

## 21. Compatibilidade

Foram preservados:

- ADR-0025 e distribuição matricial de nível único;
- H-0035 e seus cenários permanentes;
- ADR-0026 e a separação entre estrutura, conteúdo e resultado calculado;
- telas não afetadas e comportamento histórico sem conteúdo externo;
- placeholder quando aplicável;
- separação entre demo e produto;
- responsabilidade geométrica do renderizador;
- ausência de suporte externo obrigatório a `tipo: "matriz"`.

## 22. Ausência de implementação antecipada

A aplicação não altera código, não define assinatura concreta, não define classe
concreta, não fixa variável, não cria estrutura interna de catálogo, não fixa
caminho definitivo de fixture, não altera JSON real, não altera `demo.py`, não
corrige o H-0036, não declara teste executado e não declara implementação
aprovada.

## 23. Escopo real da aplicação

Arquivos alterados pela aplicação:

```text
docs/adr/ADR-0027-carregamento-conjunto-tela-conteudo-externo-ponto-entrada.md
docs/adr/INDICE_ADR.md
docs/NOMENCLATURA.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_console.md
docs/contratos/contrato_json_console.md
```

Arquivo criado pela aplicação:

```text
docs/relatorios/RELATORIO_APLICACAO_ADR-0027.md
```

Arquivo criado por este QA:

```text
docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
```

Não foram observados arquivos inesperados atribuíveis à aplicação. O workspace
contém artefatos acumulados já documentados dos ciclos ADR-0026, ADR-0027 e
H-0036.

## 24. Achados

Nenhum achado foi identificado.

```yaml
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
```

## 25. Observações

```yaml
observacoes:
  - id: OBS-QAAPADR-0027-001
    severidade: observacao
    descricao: >
      O workspace está sujo por artefatos acumulados dos ciclos documentais
      ADR-0026, ADR-0027 e H-0036. Isso não impede a auditoria, mas exige não
      atribuir automaticamente todo arquivo não rastreado a esta aplicação.
    correcao_necessaria: nenhuma
  - id: OBS-QAAPADR-0027-002
    severidade: observacao
    descricao: >
      O checkout real e o próprio H-0036 usam a raiz Git como raiz operacional,
      com caminhos docs/, tela/, demo/ e config/, sem prefixo scripts/. A
      auditoria seguiu os caminhos reais existentes no repositório.
    correcao_necessaria: nenhuma
```

## 26. Classificação final

```yaml
status_literal: ADR_APPLICATION_APPROVED_WITH_NOTES
status_normalizado: Aplicação documental da ADR-0027 aprovada, com observações não corretivas
relatorio: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
schema_semantico_propagado: true
apresentacoes_propagadas:
  - tabela
  - hierarquia
  - conjuntos_campos
tipos_de_nivel_propagados:
  - container
  - conteudo
  - nome_valor
validacoes_semanticas_propagadas: 20
responsabilidade_demo_py_propagada: true
separacao_dos_documentos_propagada: true
jsons_permanentes_formalizados: true
revisao_H0035_formalizada: true
fronteira_pipeline_preservada: true
residuos_conflitantes: []
QAH-0036-001_resolvido: true
QAH-0036-002_resolvido: true
QAH-0036-003_resolvido: true
PATCH_HANDOFF_exequivel: true
arquivos_inesperados: []
git:
  branch: master
  head: fb9e5be
  stage: vazio
  commit_novo: nao_realizado
  diff_check: sem_erros
  arquivo_criado_nesta_etapa: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0027.md
proxima_categoria: PATCH_HANDOFF
```
