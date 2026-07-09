---
name: contrato-json-dashboard
description: Especifica o envelope mínimo de um elemento tipo dashboard em corpo.elementos[] do JSON de tela — passivo, opcional, sem conteúdo universal, modelo para contratos futuros de conteúdo
metadata:
  type: contrato
  scope: scripts
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_tela_json.md
      - docs/contratos/contrato_composicao_corpo.md
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo de elemento `dashboard` (`contrato_json_dashboard.md`)

## 1. Objetivo

Especificar apenas o **envelope mínimo** de um elemento do tipo `dashboard`
declarado em `corpo.elementos[]` no JSON de tela concreto: os campos mínimos
do envelope, a natureza passiva e opcional do elemento, a ausência de conteúdo
universal fixo, e o modelo normativo que todo contrato futuro de conteúdo de
`dashboard` deve seguir.

Este contrato fecha o envelope mínimo. Não fecha conteúdo interno. Cada tipo
real de conteúdo de `dashboard` terá contrato próprio.

---

## 2. Natureza e escopo

`dashboard` é um tipo de elemento do corpo passivo e opcional. Uma ocorrência
concreta de `dashboard` é uma instância declarada em `corpo.elementos[]` no
JSON de tela.

Propriedades fundamentais:

- `dashboard` é **passivo** — não aceita cursor navegável, não responde a
  setas do teclado, não expõe ação de Enter;
- `dashboard` é **opcional** — sua presença exige declaração explícita em
  `corpo.elementos[]`; ausência não gera estrutura nem espaço reservado;
- `dashboard` **não tem conteúdo universal fixo** — não existe conteúdo
  padrão válido para qualquer tela;
- conteúdo concreto pertence ao JSON da tela, declarado pela instância;
- **não existe `config/dashboard.json`** — conteúdo de `dashboard` não é
  configuração global por componente (ADR-0008, decisão 7).

Este contrato especifica apenas o **envelope mínimo** do elemento. As regras
de composição e posicionamento no corpo pertencem a
`contrato_composicao_corpo.md`.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seção 11) estabelece que:

- `dashboard` é instância passiva configurável por tela;
- não é navegável por `[✥]`;
- não é obrigatório;
- possui moldura própria;
- não possui conteúdo universal fixo.

Este contrato operacionaliza esses princípios para o formato JSON concreto e
estabelece o modelo para contratos futuros de conteúdo de `dashboard`.

---

## 4. JSON mínimo

O envelope mínimo de um elemento `dashboard` em `corpo.elementos[]` é:

```json
{
  "id": "dashboard_principal",
  "tipo": "dashboard",
  "titulo": "Resumo",
  "conteudo": {
    "tipo": "placeholder",
    "binding": null
  },
  "regras_exibicao": {
    "posicao_dashboard": "vertical"
  }
}
```

Observações sobre o envelope mínimo:

- `conteudo.tipo: "placeholder"` indica ausência de conteúdo real — é o
  valor mínimo válido antes de um contrato de conteúdo ser aplicado;
- `conteudo.binding: null` indica que não há vínculo de dados declarado;
- `regras_exibicao.posicao_dashboard`: **campo transicional — superado pela
  ADR-0010 (2026-07-08)**. A posição do `dashboard` no corpo é controlada
  pela estrutura declarativa geral do `corpo`, como acontece com `console` e
  `lancador`. O campo `posicao_dashboard` não é eixo independente de
  `arranjo` nem de `tiling`. JSONs existentes com este campo podem ser
  honrados por compatibilidade em ciclo futuro de migração. A migração/
  descarte do campo ocorrerá em handoff numerado posterior.

---

## 5. Campos obrigatórios

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador estável e único do elemento no escopo de `corpo.elementos[]`. Elemento sem `id` é inválido. |
| `tipo` | string | Deve ser o valor literal `"dashboard"`. |
| `titulo` | string | Rótulo identificador da instância — exibido na borda ou como cabeçalho do elemento. Declarado pela instância. |
| `conteudo` | objeto | Envelope de conteúdo. Deve declarar ao menos `tipo` e `binding`. Conteúdo concreto pertence ao JSON da tela; cada tipo real de conteúdo tem contrato próprio. |
| `conteudo.tipo` | string | Tipo de conteúdo: `"placeholder"` (sem conteúdo real) ou identificador de tipo real definido por contrato próprio. |
| `conteudo.binding` | objeto ou null | Vínculo declarativo com a origem de dados. `null` quando não há dados vinculados. |
| `regras_exibicao` | objeto | Regras de posicionamento e exibição da instância no corpo. A posição visual do `dashboard` é controlada pela estrutura declarativa geral do `corpo` (ADR-0010). |
| `regras_exibicao.posicao_dashboard` | string (transicional) | **Campo descontinuado como eixo independente (ADR-0010)**. `"vertical"` ou `"horizontal"`. JSONs existentes com este campo podem ser honrados por compatibilidade em handoff futuro de migração. Não é eixo separado de `arranjo` nem de `tiling`. |

---

## 6. Regras de validação

**V-1. `dashboard` é elemento do corpo e é opcional.**
`dashboard` só aparece como elemento de `corpo.elementos[]`. A ausência de
elemento com `tipo = "dashboard"` é estado normal — `dashboard` nunca existe
por default.

**V-2. `id` presente e único.**
Elemento `dashboard` sem `id` é inválido. `id` duplicado no escopo de
`corpo.elementos[]` é erro de validação.

**V-3. `dashboard` não é navegável por `[✥]`.**
`dashboard` é passivo. Não expõe cursor navegável. O chip `[✥]` não pode ter
`dashboard` como condição de existência ou de ativação (ADR-0005).

**V-4. Conteúdo pertence ao JSON da tela.**
Conteúdo concreto de `dashboard` é declarado pela instância no JSON de cada
tela. Não existe conteúdo universal padrão aplicável a qualquer tela.

**V-5. Não existe `config/dashboard.json`.**
Nenhum arquivo global `config/dashboard.json` deve ser criado. Conteúdo de
`dashboard` não é configuração global por componente (ADR-0008, decisão 7).

**V-6. Tipo de conteúdo desconhecido é erro de validação.**
`conteudo.tipo` com valor não registrado é erro de validação. `"placeholder"`
é valor de reserva enquanto não há contrato de conteúdo aplicado.

**V-7. Posição do `dashboard` é controlada pela composição geral do corpo (ADR-0010).**
A posição visual do `dashboard` no corpo é definida pela estrutura declarativa
do `corpo`, como acontece com `console` e `lancador`. O campo
`regras_exibicao.posicao_dashboard` está descontinuado como eixo de
posicionamento independente de `arranjo` e `tiling` (ADR-0010, 2026-07-08).
JSONs existentes com esse campo podem ser honrados por compatibilidade em
handoff futuro de migração; a migração/descarte ocorrerá em handoff
numerado posterior. A sequência anterior de planejamento foi
cancelada/removida e não orienta novos ciclos.

---

## 7. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- conteúdo interno de qualquer instância de `dashboard` — cada tipo real de
  conteúdo terá contrato próprio (`contrato_conteudo_dashboard_<tipo>.md`);
- regras de renderização visual do `dashboard` (moldura, alinhamento de
  rótulos) — pertencem a `contrato_composicao_corpo.md` seção 5.3;
- draft da instância de `dashboard` da tela raiz do Orquestrador (8 campos
  + Total + 8 marcadores) — é instância específica, não regra universal;
- posicionamento horizontal do bloco dentro do espaço disponível — pendência
  DOC-B004.

---

## Contratos futuros de conteúdo de `dashboard`

Todo contrato `contrato_conteudo_dashboard_<tipo>.md` deve conter:

1. Objetivo do tipo de conteúdo
2. Elemento hospedeiro permitido: `dashboard`
3. Campos próprios do conteúdo
4. Binding no `tela.json`
5. JSON mínimo associado
6. Regras de validação
7. Fora de escopo

Esses contratos são os responsáveis por fechar o que este envelope não fecha.
Nenhum conteúdo real de `dashboard` pode ser declarado no JSON de tela sem
que exista contrato próprio do tipo de conteúdo correspondente.

---

## 8. Critérios de aceite documental

- [ ] O JSON mínimo contém `id`, `tipo`, `titulo`, `conteudo` e
      `regras_exibicao`.
- [ ] `conteudo` declara `tipo` e `binding`, sem fechar conteúdo universal.
- [ ] `dashboard` está posicionado em `corpo.elementos[]`.
- [ ] `dashboard` não é navegável por `[✥]` está declarado.
- [ ] `dashboard` é opcional está declarado.
- [ ] Ausência de `config/dashboard.json` está declarada e fundamentada.
- [ ] A seção "Contratos futuros de conteúdo de `dashboard`" contém o modelo
      com as 7 seções obrigatórias.
- [ ] O JSON mínimo não contradiz `contrato_tela_json.md` nem
      `contrato_composicao_corpo.md`.
