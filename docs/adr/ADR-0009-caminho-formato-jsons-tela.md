---
name: ADR-0009-caminho-formato-jsons-tela
description: Caminho, nomenclatura e organização dos JSONs de tela — pasta config/telas/, snake_case, um arquivo por tela, sem índice central obrigatório nesta etapa
metadata:
  type: adr
  status: aceita
  data: 2026-07-07
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados:
    - docs/contratos/contrato_tela_json.md
  handoffs_bloqueados: []
---

# ADR-0009 — caminho, nomenclatura e formato dos JSONs de tela

## Status

`aceita`

## Data

2026-07-07

## Nota de atualização — ADR-0021 (2026-07-14)

A ADR-0021 substitui parcialmente a política de raiz única desta ADR.

Ponto preservado:

- o produto real continua usando JSONs de tela em `config/telas/<id>.json`;
- o `id` interno da tela continua coincidindo com o nome base do arquivo;
- `config/estilo.json` permanece fora de `config/telas/`.

Ponto substituído:

- a formulação "todo JSON de tela em `config/telas/<id>.json`" deixa de ser
  única para todo o repositório. A demonstração passa a ter raiz declarativa
  própria: `config/telas/demo/<id>.json`.

A futura identidade demonstrativa será `config/telas/demo/demo.json` com
`"id": "demo"`. Não há alias entre `demo` e `orquestrador`. A futura
`config/telas/orquestrador.json` fica reservada ao produto real.

Esta nota não reescreve a decisão histórica original; explicita a superação
parcial introduzida pela ADR-0021.

## Nota de atualização — ADR-0022 (2026-07-14)

A ADR-0022 define a reserva feita pela ADR-0021:

- `orquestrador.py` será o ponto de entrada principal futuro do produto real,
  diretamente na raiz;
- `orquestrador.py` deverá usar explicitamente a raiz `config/telas/`;
- `config/telas/orquestrador.json` será a tela inicial real;
- o campo `"id"` dessa tela será `"orquestrador"`;
- a identidade `orquestrador` pertence exclusivamente ao produto real e
  continua sem alias ou fallback com `demo`.

Esta nota não cria o arquivo físico e não altera a raiz demonstrativa
`config/telas/demo/`.

## Contexto

A ADR-0008 estabeleceu que cada tela terá seu próprio JSON de configuração
concreta. O contrato `contrato_tela_json.md` definiu o schema conceitual.
Ambos deixaram explicitamente fora de escopo a decisão de caminho, nomenclatura
e organização dos arquivos JSON em disco.

O relatório de consolidação `RELATORIO_CONSOLIDACAO_FASE_0_ADR-0008_TELA_BASE.md`
identificou DOC-B010 como pré-requisito para o draft real da tela raiz do
Orquestrador: sem definir onde e como os JSONs de tela ficam, não é possível
criar, referenciar nem carregar o arquivo de forma consistente.

Esta ADR preenche essa lacuna. Não cria JSON real de tela nem altera contratos.

## Decisão

As seguintes declarações constituem a decisão formal desta ADR:

**1. Cada tela concreta terá um JSON próprio.**
Não haverá arquivo único global que agrupe todas as telas. Cada tela vive em
um arquivo separado.

**2. Os JSONs de tela ficam em `config/telas/`.**
O caminho canônico de todo JSON de tela é:

```text
config/telas/<id_da_tela>.json
```

Esse diretório fica dentro de `config/`, irmão de `docs/`, seguindo a política
já estabelecida na seção 0 do `NOMENCLATURA.md`.

**3. O nome do arquivo segue o identificador estável da tela.**
Regras de nomenclatura obrigatórias:

- identificador estável, minúsculo, sem acentos, sem espaços;
- preferencialmente em `snake_case`;
- o `id` interno da tela deve coincidir com o nome base do arquivo, salvo
  exceção futura documentada em ADR própria;
- nunca abreviar de forma que misture dois termos já distinguidos no glossário.

**4. A tela raiz do Orquestrador usa o identificador canônico `orquestrador`.**
O identificador estável da tela raiz é `orquestrador`. Portanto, quando o
arquivo for criado, o caminho será:

```text
config/telas/orquestrador.json
```

Esse arquivo não existe ainda. Ele será criado quando DOC-B011 for executado.

**5. Não haverá índice central obrigatório de telas nesta etapa.**
A descoberta e listagem de telas pode ser tratada futuramente por convenção de
diretório ou por um registry próprio, mas isso fica fora do escopo desta ADR.
Nenhum arquivo de índice central de telas é criado ou exigido agora.

**6. `config/estilo.json` permanece fora de `config/telas/`.**
O arquivo `config/estilo.json` é a biblioteca global de aparência. Ele não
entra em `config/telas/` e não segue a nomenclatura por identificador de tela.
Sua localização canônica permanece `config/estilo.json`.

**7. JSONs transicionais existentes em `config/` não são apagados nesta etapa.**
Os arquivos abaixo permanecem onde estão, marcados como artefatos a
reavaliar/migrar em tarefas posteriores:

- `config/lancador.json`
- `config/barra_de_menus.json`
- `config/cabecalho.json`
- `config/layout_console.json`
- `config/layout_dado.json`
- `config/layout_menu.json`

Eles não são fontes canônicas de configuração de tela concreta. A migração
ou descarte de cada um será decidido em tarefa específica.

**8. Todo JSON de tela deve seguir o contrato `contrato_tela_json.md`.**
Esta ADR não reescreve nem complementa o contrato de schema. Cada JSON de
tela deve conter, conceitualmente, ao menos:

```text
id
schema
cabecalho
corpo
barra_de_menus
```

E pode conter adicionalmente:

```text
metadados
bindings
acoes_registradas / referencias_de_acoes
```

Os detalhes de campo, tipos, validação e regras de composição pertencem ao
`contrato_tela_json.md`.

## Consequências

- DOC-B011 pode criar o arquivo `config/telas/orquestrador.json` como draft
  da tela raiz do Orquestrador.
- Contratos podem continuar usando o termo genérico `tela.json`; quando
  necessário referenciar o caminho concreto, usar `config/telas/<id>.json`.
- Não se deve criar `config/dashboard.json`.
- `dashboard`, `lancador`, `console`, `barra_de_menus` e `chips` são instâncias
  declaradas dentro do JSON da tela, não arquivos JSON próprios por componente.
- A implementação futura deve carregar tela por `id`, não por nome de classe
  hardcoded — o `id` é a chave de carregamento.
- O diretório `config/telas/` será criado quando o primeiro JSON de tela for
  criado (DOC-B011).

## Fora de escopo

Esta ADR não decide e não autoriza:

- criar o JSON da tela raiz (`config/telas/orquestrador.json`) — isso é DOC-B011;
- criar loader Python de telas;
- validar JSON com schema automático;
- migrar JSONs transicionais;
- apagar arquivos antigos de `config/`;
- implementar registry de ações;
- implementar registry de telas;
- revisar contratos existentes.

## Alternativas consideradas

| Alternativa | Motivo para rejeitar ou adiar |
|---|---|
| Manter todos os JSONs de tela diretamente em `config/` (sem subpasta) | Misturaria JSONs de tela com arquivos transicionais por domínio/componente, dificultando listagem e carregamento; perdia a convenção de diretório como mecanismo de descoberta futura |
| Nomear arquivos por nome de classe Python (ex.: `Orquestrador.json`) | Cria acoplamento entre nomenclatura de arquivo e implementação; viola a regra de identificador estável minúsculo sem acentos e o princípio de mudança declarativa sem alterar código |
| Criar índice central de telas nesta etapa | Introduz dependência de manutenção prematura antes de ter mais de uma tela real; pode ser adicionado futuramente quando houver casos de uso concretos |
| Usar `id` diferente do nome base do arquivo | Criaria divergência desnecessária entre chave de carregamento e localização em disco; a coincidência simplifica diagnóstico e manutenção |
