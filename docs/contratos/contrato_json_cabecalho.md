---
name: contrato-json-cabecalho
description: Especifica a forma mínima da seção cabecalho dentro do JSON de tela — campos obrigatórios titulo e descricao, separação entre textos concretos e parâmetros de apresentação
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_cabecalho.md
      - docs/contratos/contrato_tela_json.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo da seção `cabecalho` (`contrato_json_cabecalho.md`)

## 1. Objetivo

Especificar a forma mínima da seção `cabecalho` dentro do JSON de tela
concreto: os dois campos textuais obrigatórios, a separação entre textos
concretos (que pertencem ao JSON da tela) e parâmetros universais de
apresentação (que pertencem a `config/cabecalho.json`), e as restrições
que decorrem de `contrato_cabecalho.md`.

---

## 2. Natureza e escopo

`cabecalho` é a região fixa superior de toda tela. Ela sempre existe —
não é opcional, não é condicional, não pode ser omitida.

Este contrato especifica apenas a **representação mínima de `cabecalho` no
JSON de tela**. As regras semânticas completas da região (parâmetros de
apresentação, posição do título, alinhamento, capitalização, truncamento)
pertencem a `contrato_cabecalho.md`, que continua sendo a autoridade sobre
o comportamento do `cabecalho`.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seção 7) estabelece que:

- a seção `cabecalho` é obrigatória;
- os campos mínimos são `titulo` e `descricao`;
- os textos concretos pertencem à tela declarada no JSON;
- parâmetros universais de apresentação pertencem a `contrato_cabecalho.md`
  e/ou a configuração de tela quando a ADR-0008 for aplicada.

Este contrato operacionaliza esses princípios para o formato JSON concreto
do arquivo de tela.

---

## 4. JSON mínimo

A forma mínima da seção `cabecalho` dentro do JSON de tela é:

```json
"cabecalho": {
  "titulo": "Título da Tela",
  "descricao": "Descrição concisa do propósito desta tela."
}
```

Não há campos adicionais no `cabecalho` do JSON de tela. Parâmetros de
apresentação (posição, alinhamento, capitalização) vivem em
`config/cabecalho.json`, lidos pelo renderer em tempo de execução.

---

## 5. Campos obrigatórios

| Campo | Tipo | Regra |
|---|---|---|
| `titulo` | string | Texto curto de identificação da tela. Declarado pela classe/tela, nunca pelo renderer nem por configuração global. Sem limite de caracteres definido neste contrato — apresentação regida por `config/cabecalho.json`. |
| `descricao` | string | Texto de contextualização. Máximo de 200 caracteres efetivos antes do truncamento (conforme `max_caracteres` em `config/cabecalho.json`). Declarado pela classe/tela. |

Apenas `titulo` e `descricao` existem como campos textuais do `cabecalho`
no JSON de tela. Nenhum outro campo textual pode ser adicionado sem nova
decisão documental e atualização de `contrato_cabecalho.md`.

---

## 6. Regras de validação

**V-1. Presença obrigatória.**
`cabecalho` deve existir no JSON de tela. JSON de tela sem `cabecalho` é
inválido.

**V-2. `titulo` presente e não vazio.**
`titulo` deve ser string não vazia. Ausência ou string vazia é erro de
validação.

**V-3. `descricao` presente.**
`descricao` deve existir como campo. String vazia é aceitável quando a tela
não exige descrição, mas o campo não pode ser omitido.

**V-4. Sem campos adicionais.**
Nenhum campo além de `titulo` e `descricao` pode ser declarado em `cabecalho`
no JSON de tela. Campo adicional é erro de validação ou ignorado conforme
política do renderer.

**V-5. Textos pertencem ao JSON da tela.**
Os valores concretos de `titulo` e `descricao` são declarados no JSON de
cada tela. Não pertencem a `config/cabecalho.json` nem a nenhum artefato
global.

**V-6. Parâmetros de apresentação não pertencem ao JSON de tela.**
Posição do título, alinhamento, capitalização, `max_caracteres` e
`recuo_lateral` são parâmetros de apresentação, não campos do JSON de tela.
Eles pertencem a `config/cabecalho.json`, lidos em tempo de execução.

---

## 7. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- parâmetros de apresentação do `cabecalho` — cobertos por
  `contrato_cabecalho.md` e `config/cabecalho.json`;
- regras de renderização, alinhamento, capitalização, posição do título,
  truncamento — pertencem a `contrato_cabecalho.md`;
- introdução de terceiro campo textual — exige atualização de
  `contrato_cabecalho.md`.

---

## 8. Critérios de aceite documental

- [ ] O JSON mínimo contém exatamente `titulo` e `descricao` como campos.
- [ ] Nenhum campo de apresentação (alinhamento, capitalização,
      `recuo_lateral`, `max_caracteres`) consta no JSON mínimo.
- [ ] A separação entre textos concretos (JSON de tela) e parâmetros de
      apresentação (`config/cabecalho.json`) está formalizada neste contrato.
- [ ] O JSON mínimo de exemplo não contradiz `contrato_cabecalho.md` nem
      `contrato_tela_json.md`.
- [ ] Nenhuma seção deste contrato cria terceiro campo textual para `cabecalho`.
