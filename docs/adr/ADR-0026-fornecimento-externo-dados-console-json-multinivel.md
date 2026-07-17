---
name: ADR-0026-fornecimento-externo-dados-console-json-multinivel
description: Formaliza a separacao entre configuracao estrutural da tela e fornecimento externo de dados de runtime ao console por JSON declarativo multinivel
metadata:
  type: adr
  status: aceita e aplicada
  data: "2026-07-17"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_console.md
    - docs/contratos/contrato_json_console.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/NOMENCLATURA.md
    - docs/adr/INDICE_ADR.md
  handoffs_bloqueados: []
---

# ADR-0026 — Fornecimento externo de dados ao console por JSON multinível

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0026 |
| Título | Fornecimento externo de dados ao console por JSON multinível |
| Status | aceita e aplicada |
| Data | 2026-07-17 |
| Origem | Decisão explícita do usuário |

---

## 2. Status

`aceita e aplicada`

---

## 3. Contexto

O ciclo H-0035 foi concluído como:

```yaml
handoff: H-0035
titulo: distribuicao matricial configuravel de nivel unico do conteudo dos elementos
adr: ADR-0025
status: CONCLUIDO
commit: fb9e5be
branch: master
workspace: LIMPO
stage: VAZIO
ciclo_ativo: NENHUM
```

O H-0035 permanece fechado. Esta ADR não reabre, reinterpreta nem altera esse
ciclo.

A ADR-0025 formalizou a distribuição matricial configurável de nível único do
conteúdo dos elementos. Ela preservou o papel do renderizador no cálculo de
geometria, dimensões, margens, espaços, alinhamentos, fallback e recuperação
após redimensionamento, e deixou composição multinível fora do seu escopo.

A decisão atual separa três camadas:

- **estrutura de tela**: configuração declarativa da interface;
- **conteúdo recebido**: dados de runtime fornecidos externamente ao console;
- **resultado calculado**: representação física produzida pelo renderizador em
  runtime.

O console deve ser preparado para receber dados produzidos externamente. No
orquestrador final, um script produzirá ou devolverá esses dados ao fluxo de
apresentação. O protocolo concreto de comunicação com esse script ainda não foi
decidido.

Esta ADR usa como autoridade externa da decisão o anexo indicado pelo usuário:

```text
ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md
```

Esse anexo é entrada externa desta etapa. Ele não é tratado como arquivo já
pertencente ao repositório, não é copiado para o repositório e suas regras não
são declaradas como já aplicadas aos contratos.

---

## 4. Autoridades ativas lidas

| Documento | Relação com a decisão |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registra a sequência de ADRs aceitas e o status da ADR-0025 como aceita e aplicada. |
| `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md` | Autoridade imediatamente anterior sobre distribuição matricial de nível único, preservação de cálculos geométricos pelo renderizador e exclusão de multinível. |
| `docs/adr/ADR-0008-modelo-configuracao-por-tela.md` | Define o modelo declarativo por tela e a proibição de hardcoding de dados de instância. |
| `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md` | Define composição hierárquica do corpo, distribuição de área por container e separação entre área alocada e conteúdo. |
| `docs/adr/ADR-0017-redimensionamento-reativo-tui.md` | Define recalculo integral após redimensionamento e preserva decisões declarativas durante o redesenho. |
| `docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md` | Diferencia matriz estrutural de `grupo` da distribuição interna de conteúdo. |
| `docs/adr/ADR-0021-separacao-demo-produto-politica-caminhos.md` | Preserva `tela/` como motor compartilhado e separa demonstração do produto real. |
| `docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md` | Registra o orquestrador final, sua tela inicial futura e a presença estrutural inicial de `console` e `dashboard`. |
| `docs/adr/ADR-0024-proibicao-preenchimento-vazio-corpo.md` | Preserva a proibição de espaço externo vazio e a obrigação de ocupação visual por elementos. |
| `docs/NOMENCLATURA.md` | Referência terminológica ativa para JSON de tela, motor compartilhado, runtime, renderizador e distribuição matricial. |
| `docs/contratos/contrato_tela_json.md` | Contrato ativo do JSON estrutural da tela, pipeline conceitual de renderização e seção de distribuição matricial de nível único. |
| `docs/contratos/contrato_console.md` | Contrato ativo do `console` como container genérico e das responsabilidades do renderizador, itens, paginação e runtime. |
| `docs/contratos/contrato_json_console.md` | Envelope ativo do elemento `console` no JSON de tela e ponto a reconciliar com o futuro fornecimento externo de conteúdo. |
| `docs/contratos/contrato_composicao_corpo.md` | Contrato ativo de composição do corpo, loader, renderizador, distribuição de área e fronteira com distribuição interna de elementos. |
| `docs/contratos/contrato_json_dashboard.md` | Contrato ativo correlato da distribuição matricial aplicada a elemento funcional. |
| `docs/contratos/contrato_json_lancador.md` | Contrato ativo correlato da distribuição matricial aplicada a elemento funcional. |
| `docs/contratos/contrato_lancador.md` | Contrato ativo com precedência e fallback relacionados à distribuição matricial em `lancador`. |

Não foi encontrada contradição material entre essas autoridades que impeça o
registro desta decisão. Campos já existentes, como `origem_dados`, deverão ser
reconciliados futuramente; esta ADR não decide se esse ou outro nome será o
vínculo final entre tela e fonte externa.

---

## 5. Problema

Falta uma fronteira normativa clara entre:

- configuração estrutural da tela;
- documento externo de conteúdo;
- produtor futuro dos dados;
- consumidor, modelo e loader;
- renderizador;
- resultados geométricos calculados em runtime.

Sem essa fronteira, dados de conteúdo de runtime podem ser confundidos com o
JSON estrutural da tela, e o consumidor pode acabar assumindo responsabilidades
não decididas, como reconstruir hierarquia a partir de dados de domínio não
normalizados ou inferir estrutura semântica que deveria chegar pronta.

---

## 6. Decisão

Ficam registradas as seguintes decisões:

1. O conteúdo de runtime do console terá origem externa.
2. O JSON estrutural da tela não será o repositório desses dados de runtime.
3. O console receberá os dados por meio de um JSON externo.
4. O documento externo seguirá um envelope declarativo compatível com o anexo
   externo informado pelo usuário.
5. O formato inicial de interesse é `tipo: "multinivel"`.
6. O bloco `formato` descreve a intenção de apresentação.
7. O bloco `dados` contém a estrutura semântica.
8. Os níveis são declarados explicitamente.
9. Os dados chegam previamente estruturados para a apresentação multinível.
10. O consumidor desses dados não reconstrói, descobre ou infere a hierarquia a
    partir de dados de domínio não normalizados.
11. O renderizador continua calculando geometria, dimensões efetivas, quebras,
    truncamentos, alinhamentos calculados, paginação, posições finais e
    recuperação após redimensionamento.
12. No sistema final, um script será responsável por produzir ou devolver o
    documento de dados ao fluxo de apresentação.
13. O contrato concreto de invocação desse script permanece para decisão
    futura.

Esta decisão trata da origem e da fronteira dos dados. Ela não altera as
responsabilidades implementadas no H-0035 para cálculo de geometria,
dimensões, distribuição, quebras, alinhamentos e posições finais.

---

## 7. Fronteiras de responsabilidade

### Produtor futuro

Responsável por produzir dados semanticamente adequados ao formato multinível.
O produtor não é definido nesta ADR além da decisão de que, no orquestrador
final, um script produzirá ou devolverá os dados.

### Documento JSON externo

Responsável por transportar:

```text
tipo de conteúdo
formatação desejada
políticas declarativas
dados semânticos
declaração dos níveis
```

### Configuração estrutural da tela

Responsável pela composição e configuração estrutural da interface, sem
incorporar o conteúdo de runtime que será fornecido externamente.

### Consumidor, modelo e loader

Esta ADR define apenas a fronteira conceitual: consumidor, modelo e loader
deverão tratar a separação entre JSON estrutural de tela e documento externo de
conteúdo quando a aplicação documental e a implementação forem autorizadas.

Esta ADR não inventa APIs, classes, campos, assinaturas, caminhos ou protocolo.

### Renderizador

Responsável pelos resultados calculados, incluindo:

```text
geometria
dimensões efetivas
quebras físicas
truncamentos
alinhamentos calculados
paginação
posições finais
recuperação após redimensionamento
```

---

## 8. Estrutura conceitual mínima

O envelope conceitual mínimo do documento externo é:

```json
{
  "tipo": "multinivel",
  "formato": {},
  "dados": []
}
```

Esse exemplo é conceitual. Ele não substitui o futuro contrato, schema,
validações, vocabulário completo ou mecanismo de integração.

Princípio normativo:

```text
O JSON declara intenção e conteúdo semântico.
O renderizador calcula a representação física.
```

---

## 9. Relação com o formato matricial

O anexo externo também descreve `tipo: "matriz"`.

Esta ADR não apaga nem contradiz essa parte do anexo. Porém, a inclusão do
formato matricial no mesmo mecanismo de fornecimento não está decidida para a
primeira implementação. Não se deve inferir suporte, escopo de implementação
ou obrigação inicial apenas pela existência desse formato no anexo.

---

## 10. Compatibilidade

O H-0035 e a ADR-0025 permanecem válidos.

A distribuição matricial já implementada e aplicada aos contratos ativos não é
redefinida por esta decisão. A ADR-0026 trata da origem e da fronteira dos
dados de conteúdo de runtime recebidos pelo console.

Não existe migração automática decidida. Não existe alteração retroativa
comprovada nas telas atuais. O comportamento histórico deve ser preservado até
aplicação documental e implementação aprovadas.

---

## 11. Consequências

Consequências positivas:

- separação entre estrutura de tela e conteúdo de runtime;
- possibilidade de produtores externos;
- dados reutilizáveis e testáveis;
- fronteira clara entre semântica declarada e representação física calculada;
- preparação documental para conteúdo multinível no console.

Custos e riscos:

- necessidade futura de contrato do documento externo recebido;
- necessidade de validação do documento recebido;
- necessidade futura de contrato de integração com o script;
- necessidade futura de tratamento explícito de erros;
- risco de divergência entre produtor e consumidor sem versionamento ou schema.

Esta ADR não transforma esses riscos em soluções escolhidas.

---

## 12. Documentos afetados identificados

Documentos a atualizar ou avaliar em etapa futura, sem alteração nesta etapa:

| Documento | Motivo |
|---|---|
| `docs/adr/INDICE_ADR.md` | Registrar a ADR-0026 após QA e aplicação documental autorizada. |
| `docs/NOMENCLATURA.md` | Formalizar a terminologia de documento externo de conteúdo, conteúdo multinível e fronteira com JSON estrutural. |
| `docs/contratos/contrato_tela_json.md` | Reconciliar o JSON estrutural da tela com a fonte externa de conteúdo, sem escolher ainda o vínculo. |
| `docs/contratos/contrato_console.md` | Registrar a fronteira do `console` como consumidor de conteúdo externo multinível. |
| `docs/contratos/contrato_json_console.md` | Reconciliar o envelope atual do `console`, inclusive `origem_dados`, com o futuro contrato externo sem decidir nome de campo nesta ADR. |
| `docs/contratos/contrato_composicao_corpo.md` | Preservar a distinção entre composição estrutural, distribuição interna e conteúdo externo recebido. |
| `docs/contratos/contrato_json_dashboard.md` | Avaliar impacto somente se referências ou exemplos compartilharem vocabulário de distribuição/conteúdo. |
| `docs/contratos/contrato_json_lancador.md` | Avaliar impacto somente se referências ou exemplos compartilharem vocabulário de distribuição/conteúdo. |
| `docs/contratos/contrato_lancador.md` | Avaliar impacto apenas para preservar distinções com políticas já aplicadas da ADR-0025. |
| `config/telas/demo/` | Exemplos demonstrativos poderão precisar ser reconciliados quando a aplicação e implementação forem autorizadas. |
| `demo/` | Documentação e demonstrações poderão precisar refletir o fluxo externo quando autorizado. |

Possíveis artefatos novos a decidir futuramente:

- contrato do JSON externo de conteúdo multinível;
- schema do JSON externo de conteúdo multinível;
- exemplos ou fixtures do JSON externo;
- documentação de demonstração do fluxo externo.

Nenhum caminho concreto para esses artefatos é definido por esta ADR.

---

## 13. Aplicação futura

A futura aplicação documental desta ADR deverá, no mínimo:

- propagar a separação entre estrutura e conteúdo;
- formalizar o contrato do JSON externo;
- definir validações documentais;
- reconciliar exemplos ativos;
- remover ou marcar formulações normativas concorrentes;
- atualizar índices aplicáveis.

A aplicação documental não deve incluir implementação de código.

---

## 14. Decisões futuras obrigatórias

Permanecem obrigatoriamente para decisão futura:

- forma de vínculo entre tela e fonte de dados;
- se o JSON estrutural armazenará caminho, identificador, referência lógica ou
  outro vínculo;
- protocolo de comunicação com o script;
- se o script devolverá conteúdo em `stdout`, caminho de arquivo, descritor,
  objeto em memória ou outro transporte;
- assinatura de comando;
- argumentos do script;
- códigos de saída;
- protocolo de erros;
- execução síncrona ou assíncrona;
- localização e ciclo de vida do JSON;
- cache;
- atualização automática;
- persistência;
- diretórios de runtime;
- política de segurança;
- política de confiança do conteúdo;
- compatibilidade entre versões do produtor e do consumidor;
- versionamento;
- validação;
- suporte ao formato matricial no mesmo mecanismo;
- comportamento diante de fonte ausente ou inválida;
- navegação, seleção, expansão ou recolhimento de níveis;
- paginação interativa;
- alterações visuais específicas do console;
- arquivos de código que serão modificados;
- número ou escopo de futuro handoff.

---

## 15. Fora de escopo

Estão fora de escopo nesta etapa:

- implementação;
- criação de handoff;
- reserva de número de handoff;
- alteração de código;
- alteração de JSON de tela;
- alteração de contratos;
- criação de fixtures;
- criação de demos;
- testes;
- definição de protocolo do script;
- QA;
- aplicação da ADR;
- commit.

---

## 16. Relação com autoridades anteriores

A ADR-0025 permanece autoridade sobre distribuição matricial configurável de
nível único do conteúdo dos elementos. A ADR-0026 não substitui essa ADR e não
altera a aplicação já refletida nos contratos ativos.

`docs/contratos/contrato_tela_json.md` permanece autoridade sobre o JSON
estrutural da tela até aplicação futura desta ADR.

`docs/contratos/contrato_console.md` e
`docs/contratos/contrato_json_console.md` permanecem autoridades sobre o
`console` e seu envelope atual. A existência de campos atuais de origem ou
binding não decide, por si só, o mecanismo final de vínculo com o documento
externo desta ADR.

`docs/contratos/contrato_composicao_corpo.md` permanece autoridade sobre
composição estrutural do corpo, distribuição de área entre filhos diretos e a
fronteira com distribuição interna de elementos.

`docs/NOMENCLATURA.md` permanece autoridade terminológica ativa até atualização
futura.

Nenhuma ADR anterior é substituída por esta decisão.

---

## 17. Critérios para aplicação

A aplicação documental desta ADR só poderá ocorrer depois de:

- ADR criada;
- QA independente da ADR;
- ausência de bloqueio documental;
- identificação nominal dos documentos afetados.
