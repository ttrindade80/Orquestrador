---
name: contrato-json-barra-de-menus
description: Especifica a forma mínima da seção barra_de_menus dentro do JSON de tela — chips como entidades declarativas, campos obrigatórios de chip, separação de lancador
metadata:
  type: contrato
  scope: orquestrador
  versao: "0.1"
  status: ativo
  rastreabilidade:
    origem_especificacao:
      - docs/contratos/contrato_barra_de_menus.md
      - docs/contratos/contrato_chip.md
      - docs/contratos/contrato_tela_json.md
    adrs_aplicadas:
      - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
      - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
      - docs/adr/ADR-0022-ponto-entrada-tela-inicial-orquestrador.md
    reaproveitado_de_legado: false
---

# Contrato — JSON mínimo da seção `barra_de_menus` (`contrato_json_barra_de_menus.md`)

## 1. Objetivo

Especificar a forma mínima da seção `barra_de_menus` dentro do JSON de tela
concreto: a estrutura mínima de `chips[]`, os campos obrigatórios de cada
chip declarativo, as distinções fundamentais entre `barra_de_menus` e
`lancador`, e as restrições que decorrem de `contrato_barra_de_menus.md` e
`contrato_chip.md`.

---

## 2. Natureza e escopo

`barra_de_menus` é a região fixa inferior de toda tela. É declarada no JSON
de tela como instância com lista concreta de chips. Ela não é o corpo, não
é `lancador`, não é `cabecalho`.

Este contrato especifica apenas a **representação mínima de `barra_de_menus`
no JSON de tela**. As regras semânticas completas da região (ordem canônica
de chips, semântica de chips canônicos, estados dinâmicos, distribuição)
pertencem a `contrato_barra_de_menus.md` e `contrato_chip.md`, que
continuam sendo as autoridades sobre o comportamento da barra.

---

## 3. Relação com `contrato_tela_json.md`

`contrato_tela_json.md` (seções 18 e 19) estabelece que:

- a seção `barra_de_menus` é obrigatória;
- campo mínimo é `chips[]`;
- chips são entidades declarativas — não hardcoded pelo renderer;
- cada chip deve poder declarar `id`, `tipo`, `tecla`, `texto`, `acao`,
  `regra_existencia`, `regra_ativo` e `forma_exibicao`.

Este contrato operacionaliza esses princípios para o formato JSON concreto
do arquivo de tela.

---

## 4. JSON mínimo

A forma mínima da seção `barra_de_menus` dentro do JSON de tela é:

```json
"barra_de_menus": {
  "chips": [
    {
      "id": "sair",
      "tipo": "acao",
      "tecla": "Esc",
      "texto": "Sair",
      "acao": "sair",
      "regra_existencia": "sempre",
      "regra_ativo": "sempre",
      "forma_exibicao": "padrao"
    }
  ]
}
```

O exemplo acima usa o chip `sair` como referência mínima — não impõe que
toda tela tenha exatamente este chip. A lista concreta de chips pertence à
declaração da tela.

---

## 5. Campos obrigatórios

### 5.1 Campos de `barra_de_menus`

| Campo | Tipo | Regra |
|---|---|---|
| `chips` | array | Lista de chips declarados da instância. Pode ser lista não vazia. O renderer não inventa chips ausentes. |

### 5.2 Campos mínimos de cada chip em `barra_de_menus.chips[]`

| Campo | Tipo | Regra |
|---|---|---|
| `id` | string | Identificador único do chip no escopo da instância da `barra_de_menus`. Chip sem `id` é inválido. |
| `tipo` | string | Tipo conceitual do chip: `acao`, `filtro`, `alternancia`, `navegacao`, `informativo` ou `especifico`. Tipo desconhecido é erro de validação. |
| `tecla` | string | Identificador acionável pelo usuário. Não pode duplicar dentro da mesma instância da `barra_de_menus`. |
| `texto` | string | Rótulo exibido ao lado da tecla. Não pode ser hardcoded pelo renderer. |
| `acao` | objeto ou string declarativa | Referência declarativa à ação registrada. Comando arbitrário é proibido. |
| `regra_existencia` | string | Quando o chip existe nesta instância: `"sempre"` ou condição estrutural declarativa. |
| `regra_ativo` | string | Quando o chip está ativo/inativo: condição dinâmica recalculada a cada render. |
| `forma_exibicao` | string | Como o chip aparece: `"padrao"` ou valor declarativo reconhecido. |

---

## 6. Regras de validação

**V-1. `barra_de_menus` presente.**
A seção `barra_de_menus` deve existir no JSON de tela. Ausência é erro de
validação.

**V-2. `chips[]` presente e do tipo array.**
O campo `chips` deve ser um array. Pode ser não vazio, mas não pode ser
omitido nem ser de tipo diferente de array.

**V-3. Todo chip tem `id`.**
Chip sem `id` é inválido.

**V-4. Todo chip acionável tem `tecla`, `texto` e `acao`.**
Ausência de qualquer um desses campos em chip acionável é erro de validação.

**V-5. Teclas não duplicam.**
Teclas duplicadas na mesma instância da `barra_de_menus` são erro de
validação.

**V-6. Ações são declarativas.**
Todo campo `acao` de chip deve referenciar ação registrada/whitelisted. Ação
não registrada é erro de validação. Comando arbitrário (ex.: string de script)
é proibido.

**V-7. Chips são declarados — nunca gerados pelo renderer.**
O renderer não cria, não inventa, não completa chips ausentes. Percorre
`chips[]` conforme declarado.

**V-8. Acesso a estilos na tela real inicial.**
Pela ADR-0022, a futura tela inicial real `orquestrador` deverá declarar
`Esc`, `?` e acesso a estilos em `barra_de_menus.chips[]`. O item de estilos
não pode apontar para tela inexistente, ação temporária, alias de demonstração
ou fallback. Se os contratos ativos exigirem ação ou destino válido para todo
chip visível e não admitirem item declarativo inicialmente não navegável, a
criação física dessa tela deverá aguardar decisão adicional do usuário.

---

## 7. Distinção obrigatória: `barra_de_menus` vs `lancador`

`barra_de_menus` e `lancador` são entidades completamente distintas. Esta
distinção é obrigatória no JSON de tela:

| Conceito | Localização no JSON | Regido por |
|---|---|---|
| `barra_de_menus` | Seção raiz do JSON de tela, fora de `corpo` | `contrato_barra_de_menus.md`, `contrato_chip.md` |
| `lancador` | Elemento de `corpo.elementos[]` | `contrato_lancador.md`, `contrato_json_lancador.md` |

Consequências diretas:

- chips dos **itens** de `lancador` (a letra/tecla de cada item) **não
  pertencem** a `barra_de_menus.chips[]`;
- `barra_de_menus` fica fora de `corpo` — nunca é elemento de
  `corpo.elementos[]`;
- chips da `barra_de_menus` não controlam itens do `lancador`;
- o renderer não confunde as duas estruturas.

---

## 8. Fora de escopo

Os itens abaixo são explicitamente fora do escopo deste contrato:

- ordem canônica de chips na `barra_de_menus` — coberta por
  `contrato_barra_de_menus.md` seção 7;
- semântica de chips canônicos (`[Esc]`, `[⏎]`, `[?]`, etc.) — coberta por
  `contrato_barra_de_menus.md` seções 8–15;
- estados dinâmicos de cor (`cor_inativo`, `cor_alerta`) — cobertos por
  `contrato_estilo.md` e `contrato_chip.md`;
- registry completo de ações de chip — pendência DOC-B009;
- distribuição visual e layout interno da `barra_de_menus`.

---

## 9. Critérios de aceite documental

- [ ] O JSON mínimo de `barra_de_menus` contém `chips[]` com ao menos um
      chip de exemplo com todos os campos mínimos.
- [ ] Os campos mínimos de chip (`id`, `tipo`, `tecla`, `texto`, `acao`,
      `regra_existencia`, `regra_ativo`, `forma_exibicao`) estão listados.
- [ ] A distinção `barra_de_menus` vs `lancador` está formalizada: chips de
      `lancador` não pertencem a `barra_de_menus.chips[]`.
- [ ] Nenhuma seção deste contrato autoriza ação arbitrária (script/comando)
      em chip.
- [ ] O JSON mínimo não contradiz `contrato_barra_de_menus.md` nem
      `contrato_chip.md` nem `contrato_tela_json.md`.
