---
name: H-0012-grupo-estrutural-minimo-tela-isolada
description: Handoff de implementação — grupo estrutural mínimo (1 elemento funcional) em tela isolada; inicia suporte de código a ADR-0010; não migra o Orquestrador
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0012
  data_criacao: 2026-07-08
rastreabilidade:
  contratos_alvo:
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_json_dashboard.md
  adrs_aplicadas:
    - docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
    - docs/adr/ADR-0008-modelo-configuracao-por-tela.md
    - docs/adr/ADR-0009-caminho-formato-jsons-tela.md
  handoffs_anteriores:
    - docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
  handoffs_cancelados:
    - docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
  handoffs_removidos: []
---

# H-0012 — Grupo estrutural mínimo em tela isolada

## Status

`HANDOFF_READY`

---

## Metadados de rastreabilidade

| Campo | Valor |
|---|---|
| ID | H-0012 |
| Data de criação | 2026-07-08 |
| HEAD base | `6c91279` |
| Handoff anterior aprovado | H-0010A |
| H-0011 | CANCELADO — não implementar (ver seção abaixo) |
| H-0011A | REMOVIDO como handoff ativo — granularidade excessiva (ver seção abaixo) |
| ADR base | ADR-0010 |
| Sequência futura | H-0013, H-0014, … (sem letras) |

---

## Ordem de autoridade

Este handoff segue a hierarquia do `contrato_processo_desenvolvimento.md`:

1. Contrato de processo
2. ADRs aceitas
3. Contratos de módulo
4. **Este handoff**
5. Relatório de implementação

Qualquer contradição entre este handoff e um contrato ou ADR deve ser reportada
como `ARCHITECTURE_REVIEW_REQUIRED`. O handoff não pode sobrescrever contrato.

---

## Relação com H-0011 e H-0011A

**H-0011 — `CANCELADO_NAO_IMPLEMENTAR`**

O handoff H-0011 (`docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md`)
foi cancelado antes de qualquer implementação. Ele não deve ser implementado,
reaberto, corrigido nem usado como base. É mantido apenas para rastreabilidade
histórica. O H-0012 NÃO é continuação nem correção do H-0011.

**H-0011A — REMOVIDO por granularidade excessiva**

O handoff H-0011A foi planejado mas removido como handoff ativo antes de ser
escrito como documento completo. A decisão gerencial é que a granularidade
planejada era excessiva. O H-0012 incorpora o objetivo mínimo relevante
(suporte de código a grupo estrutural) em escopo controlado. H-0011A não
deve ser recriado.

**Regras de nomenclatura derivadas desta situação:**

- Não reabrir H-0011.
- Não recriar H-0011A.
- Não usar H-0011 nem H-0011A como base implementável.
- A sequência a partir de H-0012 não deve usar letras (H-0013, H-0014, …).
- Não criar H-0012A, H-0012B nem micro-handoffs derivados.

---

## Contexto

O H-0010A foi concluído e commitado (`36c55d2`). O sistema está com:

- `loader.py`: valida os três tipos funcionais do corpo (`console`, `lancador`,
  `dashboard`); tipo desconhecido levanta `TelaTipoDesconhecido`.
- `modelo.py`: constrói `ElementoCorpo` com `id`, `tipo` e `_campos_inertes`
  para cada elemento de `corpo.elementos[]`; lista plana.
- `renderizador.py`: itera `modelo.corpo.elementos`, despacha por tipo,
  renderiza caixa bordeada por elemento.
- `demo.py`: navegação mínima com pilha de telas.
- `config/telas/orquestrador.json`, `destino_minimo.json`, `stub_b.json`:
  todos com lista plana de `corpo.elementos[]`.

A ADR-0010 (`2026-07-08`) estabelece que `corpo.elementos[]` pode evoluir
de lista plana para estrutura com agrupamentos hierárquicos, e que a lista
plana atual continua válida. O suporte de código para esse modelo não existe
ainda — `tipo = "grupo"` levantaria `TelaTipoDesconhecido` hoje.

O H-0012 inicia esse suporte introduzindo a menor unidade de código
verificável: um `grupo` estrutural com exatamente 1 elemento funcional,
exercitado em uma tela isolada sem tocar no Orquestrador.

---

## Objetivo

Implementar a menor unidade de código necessária para iniciar a ADR-0010:

1. Criar a tela isolada `config/telas/grupo_minimo.json` com exatamente
   1 grupo estrutural contendo exatamente 1 elemento funcional (`dashboard`).
2. Alterar `loader.py` para aceitar e validar o tipo `"grupo"` com exatamente
   1 elemento funcional interno, e rejeitar violações dos invariantes deste ciclo.
3. Alterar `modelo.py` para representar o grupo e seu elemento funcional
   interno de forma acessível ao renderer.
4. Alterar `renderizador.py` para percorrer o grupo e renderizar o elemento
   funcional interno em saída vertical/compatível, sem produzir caixa visual
   própria para o grupo.
5. Atualizar os testes existentes e adicionar testes para o grupo mínimo.
6. Produzir relatório de implementação.

O Orquestrador e seus JSONs não devem ser alterados.

---

## Leitura obrigatória realizada

O preparador deste handoff leu e analisou:

```
docs/INDICE.md
docs/NOMENCLATURA.md
docs/adr/INDICE_ADR.md
docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_json_tela_minima.md
docs/contratos/contrato_json_dashboard.md
docs/contratos/contrato_json_lancador.md
docs/contratos/contrato_json_console.md
docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md
docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md
  (somente para registrar cancelamento — não como base implementável)

tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/diagnostico.py
tela/demo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_diagnostico.py
tela/teste_demo.py

config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

---

## Definição de `grupo estrutural`

**`grupo` é um container estrutural — não é elemento funcional do corpo.**

Um `grupo` agrupa elementos funcionais para fins de composição hierárquica
declarativa. Ele não tem tipo de conteúdo, não tem comportamento próprio,
não é navegável e não produz representação visual própria.

Inequívoco:

- `grupo` é container estrutural de composição.
- `grupo` pode aparecer em `corpo.elementos[]` como nó estrutural no H-0012.
- `grupo` não é elemento funcional do corpo.
- Os tipos funcionais continuam sendo apenas `console`, `dashboard` e `lancador`.
- `grupo` não altera a taxonomia funcional do corpo.
- `grupo` não gera caixa visual própria.
- `grupo` não tem foco, chip, ação, navegação ou registry.

Schema mínimo do elemento grupo em `corpo.elementos[]`:

```json
{
  "id": "grupo_minimo",
  "tipo": "grupo",
  "arranjo": "sobreposto",
  "elementos": [
    {
      "id": "dashboard_grupo_minimo",
      "tipo": "dashboard"
    }
  ]
}
```

As seguintes propriedades são invariantes do tipo `grupo`:

| Propriedade | Valor no H-0012 |
|---|---|
| É elemento funcional? | **Não.** `grupo` não é `console`, `lancador` nem `dashboard`. |
| Produz caixa visual? | **Não.** Sem borda, título, chip ou espaço visual próprio. |
| É navegável por `[✥]`? | **Não.** Nunca. |
| Tem foco? | **Não.** |
| Tem ação? | **Não.** |
| Tem seleção? | **Não.** |
| Aparece na `barra_de_menus`? | **Não.** |
| Papel | Container estrutural de composição hierárquica. |

---

## Definição de `elemento funcional`

Os **elementos funcionais do corpo** são exatamente três. A taxonomia é
fechada (ADR-0006, ADR-0010). Extensões exigem nova ADR.

| Tipo | Função |
|---|---|
| `console` | Container interativo e navegável genérico |
| `lancador` | Elemento de navegação — itens com chip e `tela_destino` |
| `dashboard` | Saída passiva formatada — não navegável por `[✥]` |

No H-0012, o único elemento funcional recomendado dentro do grupo é
`dashboard`, por ser passivo e não exigir navegação nem ação.

---

## Regras técnicas do grupo mínimo (H-0012)

As regras abaixo valem **neste ciclo** e devem ser aplicadas pela
validação do loader. Ciclos futuros (H-0013 em diante) poderão relaxar
algumas delas por ADR ou handoff próprio.

| Regra | Valor |
|---|---|
| Número de elementos funcionais dentro do grupo | Exatamente 1 |
| Tipos permitidos dentro do grupo | `console`, `lancador`, `dashboard` |
| `grupo` dentro de `grupo` | **Proibido neste ciclo** |
| `grupo` como elemento raiz em `corpo.elementos[]` | Permitido |
| Lista plana em `corpo.elementos[]` | Continua válida e imutável |
| Tela com grupo e elementos funcionais juntos em `corpo.elementos[]` | Não testado neste ciclo — escopo é tela isolada com apenas 1 grupo |
| Campo `elementos` ausente no grupo | Erro de validação |
| Campo `elementos` vazio no grupo | Erro de validação |
| Campo `elementos` com mais de 1 item | Erro de validação (H-0012) |
| Tipo funcional desconhecido dentro do grupo | Erro de validação |
| `arranjo: "lado_a_lado"` declarado no grupo | **Proibido neste ciclo** — erro de validação |

Regras obrigatórias do grupo no H-0012:

- exatamente 1 grupo estrutural na tela isolada;
- exatamente 1 elemento funcional dentro do grupo;
- elemento funcional recomendado: `dashboard` literal/passivo;
- grupo dentro de grupo é fora de escopo;
- 2+ elementos no mesmo grupo é fora de escopo;
- `arranjo lado_a_lado` é fora de escopo;
- percentual/fração é fora de escopo;
- migração do Orquestrador é fora de escopo.

---

## Escopo positivo

O H-0012 deve implementar **apenas** o seguinte:

1. **Criar** `config/telas/grupo_minimo.json`:
   - Tela isolada com `schema`, `id`, `cabecalho`, `corpo`, `barra_de_menus`.
   - `corpo.elementos[]` contém exatamente 1 elemento de `tipo = "grupo"`.
   - O grupo contém exatamente 1 elemento funcional de `tipo = "dashboard"`.
   - O dashboard usa `fonte: "literal"` com valor de texto verificável.
   - `barra_de_menus` contém pelo menos `[Esc] Voltar` e `[?] Ajuda`.

2. **Alterar `loader.py`**:
   - Aceitar `tipo = "grupo"` em `corpo.elementos[]`.
   - Para elemento do `tipo = "grupo"`, validar:
     - Campo `"elementos"` presente.
     - `"elementos"` é lista.
     - `"elementos"` não está vazio.
     - `"elementos"` tem exatamente 1 item (H-0012).
     - O item interno tem `id` e `tipo`.
     - `tipo` do item interno é funcional (`console`, `lancador`, `dashboard`).
     - `tipo` do item interno não é `"grupo"` (proibir aninhamento).
   - Preservar o elemento interno como dado inerte (ou estruturado) acessível ao modelo.
   - Manter o comportamento atual para tipos funcionais sem alteração.

3. **Alterar `modelo.py`**:
   - Para elemento do `tipo = "grupo"`, construir representação que preserve
     o elemento funcional interno como `ElementoCorpo` acessível ao renderer.
   - Para elementos funcionais diretos (lista plana), manter o comportamento atual.
   - Não criar registry, não criar subclasses, não criar estado de runtime.

4. **Alterar `renderizador.py`**:
   - Para elemento do `tipo = "grupo"`, percorrer os elementos funcionais
     internos e renderizar cada um usando o despacho por tipo já existente
     (`_linhas_console`, `_linhas_dashboard`, `_linhas_lancador`).
   - O grupo **não** produz caixa visual própria.
   - A saída final é vertical/compatível: cada elemento funcional interno
     aparece como caixa bordeada igual ao comportamento atual de lista plana.
   - Manter o comportamento de lista plana sem alteração.

5. **Alterar `tela/teste_loader.py`**:
   - Ampliar com casos de grupo mínimo válido (carregando `grupo_minimo.json`).
   - Ampliar com casos de erro: grupo sem `elementos`, grupo com `elementos`
     vazio, grupo com mais de 1 elemento, grupo dentro de grupo, tipo
     funcional desconhecido dentro do grupo.
   - Manter todos os casos existentes passando.

6. **Alterar `tela/teste_modelo.py`**:
   - Ampliar com verificação de que o modelo do grupo preserva o elemento
     funcional interno como `ElementoCorpo` acessível.
   - Verificar que a lista plana existente continua representada sem alteração.
   - Manter todos os casos existentes passando.

7. **Alterar `tela/teste_renderizador.py`**:
   - Ampliar com verificação de que o renderer, sobre modelo com grupo,
     produz a saída visual do `dashboard` interno sem caixa visual do grupo.
   - Verificar que o grupo não aparece como caixa extra na saída.
   - Manter todos os casos existentes passando (com `_EXPECTED_*`
     atualizados se necessário).

8. **Criar** `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`:
   - Relatório de implementação descrevendo arquivos alterados,
     testes executados e resultado.

---

## Escopo negativo

O executor **não deve** implementar nada além do escopo positivo acima.
A lista abaixo é exaustiva e obrigatória.

```
NÃO migrar config/telas/orquestrador.json.
NÃO alterar o fluxo principal do Orquestrador.
NÃO alterar tela/demo.py.
NÃO alterar tela/teste_demo.py.
NÃO alterar tela/diagnostico.py.
NÃO alterar tela/teste_diagnostico.py.
NÃO implementar lado_a_lado.
NÃO implementar grupo com 2 ou mais elementos funcionais.
NÃO implementar grupos aninhados (grupo dentro de grupo).
NÃO implementar distribuição por percentual ou fração.
NÃO implementar console real com dados.
NÃO implementar foco entre elementos.
NÃO implementar seleção.
NÃO implementar navegação por [✥] no grupo ou em seus elementos.
NÃO implementar nova ação ou novo chip.
NÃO criar registry de tipos, registry de ações ou registry de telas.
NÃO alterar ADRs.
NÃO alterar contratos, salvo se a auditoria bloquear formalmente com
  ARCHITECTURE_REVIEW_REQUIRED e o escopo de alteração for aprovado
  explicitamente.
NÃO alterar docs/NOMENCLATURA.md.
NÃO reabrir H-0011.
NÃO recriar H-0011A.
NÃO criar H-0012A, H-0012B nem micro-handoff derivado.
NÃO criar micro-handoff separado para JSON quando o suporte já existir.
```

### Observação sobre `tela/demo.py` e `tela/diagnostico.py`

`tela/demo.py`, `tela/teste_demo.py`, `tela/diagnostico.py` e
`tela/teste_diagnostico.py` são **proibidos** neste ciclo.

- H-0012 usa tela isolada e não migra o Orquestrador — o diagnóstico e a
  demo padrão não devem mudar.
- A demo já suporta carregar qualquer `id_tela` via `_carregar_modelo_por_id`
  — nenhuma alteração é necessária para exercitar a tela isolada.

Se a implementação exigir alterar qualquer desses arquivos, o executor deve
parar com `ARCHITECTURE_REVIEW_REQUIRED` e descrever o motivo antes de
qualquer alteração.

---

## Especificação do JSON da tela isolada

### `config/telas/grupo_minimo.json` — CRIAR

```json
{
  "schema": "tela.v1",
  "id": "grupo_minimo",
  "cabecalho": {
    "titulo": "Grupo Minimo",
    "descricao": "Tela de teste — grupo estrutural com dashboard simples"
  },
  "corpo": {
    "arranjo": "sobreposto",
    "elementos": [
      {
        "id": "grupo_principal",
        "tipo": "grupo",
        "arranjo": "sobreposto",
        "elementos": [
          {
            "id": "dashboard_conteudo",
            "tipo": "dashboard",
            "titulo": "Conteudo",
            "campos": [
              {
                "id": "msg_grupo",
                "rotulo": "Grupo",
                "fonte": "literal",
                "valor": "Dashboard dentro de grupo estrutural"
              }
            ]
          }
        ]
      }
    ]
  },
  "barra_de_menus": {
    "distribuicao": "horizontal",
    "chips": [
      {
        "id": "chip_esc",
        "tipo": "acao",
        "tecla": "Esc",
        "texto": "Voltar",
        "acao": {
          "tipo": "acao_contextual_esc"
        },
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "rotulo_dinamico"
      },
      {
        "id": "chip_ajuda",
        "tipo": "acao",
        "tecla": "?",
        "texto": "Ajuda",
        "acao": {"tipo": "abrir_ajuda"},
        "regra_existencia": "sempre",
        "regra_ativo": "sempre",
        "forma_exibicao": "visivel_ativo"
      }
    ]
  }
}
```

Regras obrigatórias do JSON acima:

- `id: "grupo_minimo"` deve coincidir com o nome base do arquivo (ADR-0009).
- `schema: "tela.v1"` — versão reconhecida pelo loader.
- `corpo.elementos[]` contém exatamente 1 elemento de `tipo = "grupo"`.
- O grupo tem `id: "grupo_principal"` e campo `"elementos"` com exatamente 1 item.
- O item interno é `tipo = "dashboard"` com campo `campos[]` e pelo menos
  1 campo com `fonte: "literal"` e `valor` verificável.
- `barra_de_menus.chips` contém pelo menos `[Esc] Voltar` e `[?] Ajuda`.
- Nenhum campo de estado de runtime (cursor, página, seleção, filtro ativo).
- Nenhuma lógica procedural.

O executor pode ajustar detalhes do JSON acima (títulos, textos) desde que:
(a) as regras estruturais acima sejam mantidas; e (b) os critérios de aceite
permaneçam verificáveis com os valores escolhidos.

Observação obrigatória — formato do dashboard:

O H-0012 usa o formato operacional já validado pelo H-0010A: `dashboard.campos[]`.
Esse é o formato que os JSONs reais (`orquestrador.json`, `destino_minimo.json`,
`stub_b.json`) e o renderer atual suportam. A harmonização entre
`contrato_json_dashboard.md` (`conteudo`/`regras_exibicao`) e o formato
operacional atual com `campos[]` fica **fora de escopo do H-0012**. O H-0012
deve usar o formato já suportado pelo renderer/modelo após H-0010A. Não alterar
contratos para resolver essa diferença.

---

## Especificação funcional por módulo

### F-1. `loader.py` — Validação do grupo

O loader deve:

a. Reconhecer `tipo = "grupo"` como tipo estrutural válido em
   `corpo.elementos[]`. Este tipo é separado dos tipos funcionais
   (`TIPOS_CORPO_VALIDOS`). A implementação pode usar um conjunto
   próprio `TIPOS_ESTRUTURAIS_VALIDOS = {"grupo"}` ou expandir a
   lógica de validação de outro modo, desde que os comportamentos
   abaixo sejam garantidos.

b. Para cada elemento de `corpo.elementos[]` com `tipo == "grupo"`:

   - Verificar que o campo `"elementos"` existe no dict do elemento;
     ausência é erro de validação.
   - Verificar que `"elementos"` é uma lista; tipo incorreto é erro.
   - Verificar que a lista não está vazia; lista vazia é erro de validação.
   - Verificar que a lista tem exatamente 1 item (H-0012); mais de 1
     item é erro de validação.
   - Para o item interno, verificar que tem campo `"id"` e campo `"tipo"`.
   - Verificar que o `tipo` do item interno é um dos tipos funcionais
     (`console`, `lancador`, `dashboard`); tipo desconhecido é erro.
   - Verificar que o `tipo` do item interno NÃO é `"grupo"`; grupo
     dentro de grupo é erro de validação (H-0012).
   - Verificar que o campo `"arranjo"` do grupo, se presente, não tem
     valor `"lado_a_lado"`; arranjo horizontal em grupo é erro de
     validação no H-0012.

c. Para elementos de `corpo.elementos[]` com tipo funcional (`console`,
   `lancador`, `dashboard`), manter o comportamento atual sem alteração.

d. Preservar o elemento interno do grupo no dict retornado de forma
   acessível ao construtor do modelo. A estrutura interna recomendada
   é preservar o elemento do grupo com seus sub-elementos inertes no
   dict de saída do loader, seguindo o padrão já existente.

### F-2. `modelo.py` — Representação do grupo

O modelo deve:

a. Para elemento do `tipo = "grupo"`, construir representação que permita
   ao renderer acessar o elemento funcional interno. A solução preferida
   é adicionar campo `elementos: list` em `ElementoCorpo` (com
   `default_factory=list`), preenchido com `ElementoCorpo` do elemento
   interno quando `tipo == "grupo"`, e vazio para tipos funcionais.
   O executor pode adotar solução alternativa desde que:
   - O renderer consiga acessar o elemento funcional interno sem
     manipular dicts crus do JSON.
   - A lista plana de elementos funcionais diretos continue funcionando
     sem alteração.
   - A solução não crie registry, subclasses de tipo, nem estado de runtime.

b. Para elementos do tipo funcional (lista plana), manter o comportamento
   atual de `ElementoCorpo(id, tipo, _campos_inertes)`.

c. Não criar estado de runtime, não criar registry, não criar subclasses.

### F-3. `renderizador.py` — Travessia do grupo

O renderer deve:

a. Para elemento de `corpo.elementos[]` com `tipo == "grupo"`:
   - Percorrer os elementos funcionais internos.
   - Para cada elemento interno, despachar para o mesmo mecanismo de
     renderização já existente:
     - `tipo == "dashboard"` → `_linhas_dashboard(elemento_interno)`
     - `tipo == "console"` → `_linhas_console(elemento_interno)`
     - `tipo == "lancador"` → `_linhas_lancador(elemento_interno)`
   - Produzir a caixa bordeada do elemento funcional interno com o título
     e o conteúdo desse elemento, como se estivesse diretamente em
     `corpo.elementos[]`.
   - NÃO produzir caixa visual própria para o grupo.
   - NÃO emitir linha extra, borda extra, espaçamento extra.

b. A saída visual final com grupo deve ser idêntica à saída que seria
   produzida com a lista plana contendo o mesmo elemento funcional
   diretamente em `corpo.elementos[]`.

c. Para elementos funcionais diretos (lista plana), manter o comportamento
   atual sem alteração.

### F-4. `diagnostico.py` — Proibido neste ciclo

`diagnostico.py` encadeia `carregar_tela → construir_modelo → renderizar_tela`
para a tela raiz (`id_tela = "orquestrador"`). O Orquestrador não é alterado.

`tela/diagnostico.py` é **proibido** neste ciclo. H-0012 usa tela isolada e
não migra o Orquestrador; portanto, o diagnóstico padrão do Orquestrador
não deve mudar.

Se a implementação exigir alterar `tela/diagnostico.py` ou alterar a saída
do Orquestrador, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`
e reportar a causa antes de qualquer alteração.

---

## Arquivos permitidos

Lista explícita e exaustiva. O executor **só pode** criar ou alterar arquivos
desta lista.

### Criar

```
config/telas/grupo_minimo.json
docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
```

### Alterar

```
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
```

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```
config/telas/orquestrador.json
config/telas/destino_minimo.json
config/telas/stub_b.json
config/estilo.json
config/lancador.json
config/barra_de_menus.json
config/cabecalho.json
config/layout_console.json
config/layout_dado.json
config/layout_menu.json
docs/NOMENCLATURA.md
docs/INDICE.md
docs/adr/
docs/contratos/
docs/backlog.md
docs/issues.md
docs/handoff/
  (exceto o próprio handoff H-0012 que foi criado antes da implementação
   e não deve ser alterado pelo executor)
tela/__init__.py
tela/diagnostico.py
tela/teste_diagnostico.py
tela/demo.py
tela/teste_demo.py
qualquer arquivo não listado como permitido acima
```

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo antes de considerar
a implementação concluída. Nenhum item pode ser ignorado.

### Critérios sobre a tela isolada

```
CA-01. config/telas/grupo_minimo.json existe e é JSON sintaticamente válido.
CA-02. grupo_minimo.id == "grupo_minimo" (coincide com o nome base do arquivo).
CA-03. grupo_minimo possui schema, id, cabecalho, corpo e barra_de_menus.
CA-04. corpo.elementos[0].tipo == "grupo".
CA-05. O grupo tem exatamente 1 elemento interno.
CA-06. O elemento interno do grupo é do tipo "dashboard".
CA-07. O dashboard interno tem pelo menos 1 campo com fonte: "literal" e valor
       textual verificável.
```

### Critérios sobre o loader

```
CA-08. carregar_tela(None, "grupo_minimo") carrega e valida sem erro.
CA-09. O loader rejeita (levanta erro) grupo sem campo "elementos".
CA-10. O loader rejeita grupo com "elementos" sendo lista vazia.
CA-11. O loader rejeita grupo com "elementos" contendo mais de 1 item.
CA-12. O loader rejeita grupo dentro de grupo (tipo interno == "grupo").
CA-12b. O loader rejeita grupo com campo `"arranjo": "lado_a_lado"` (fora de escopo no H-0012).
CA-13. O loader rejeita grupo cujo elemento interno tem tipo desconhecido.
CA-14. Lista plana (orquestrador.json, destino_minimo.json, stub_b.json)
       continua carregando sem erro.
```

### Critérios sobre o modelo

```
CA-15. O modelo construído a partir de grupo_minimo.json expõe o elemento
       funcional interno de forma acessível ao renderer
       (sem manipulação de dict cru do JSON no renderer).
CA-16. O elemento funcional interno do grupo é representado com id, tipo
       e _campos_inertes corretos.
CA-17. ElementoCorpo de elementos funcionais diretos (lista plana) continua
       com o mesmo comportamento anterior.
CA-18. modelo.elemento_por_id("grupo_principal") retorna o elemento grupo.
CA-19. modelo.elementos_por_tipo("grupo") retorna lista com 1 elemento.
```

### Critérios sobre o renderer

```
CA-20. renderizar_tela sobre modelo de grupo_minimo produz saída visual com
       a caixa bordeada do dashboard interno.
CA-21. O texto "Dashboard dentro de grupo estrutural" (ou o valor declarado
       no campo literal do dashboard) aparece na saída visual.
CA-22. O grupo NÃO aparece como caixa visual própria na saída
       (sem borda extra, sem título de grupo, sem linha extra).
CA-23. A saída visual do grupo é indistinguível da saída que seria produzida
       com o dashboard diretamente em corpo.elementos[] (lista plana).
CA-24. Lista plana (orquestrador.json, destino_minimo.json, stub_b.json)
       continua produzindo a mesma saída visual de antes.
```

### Critérios sobre os testes

```
CA-25. python tela/teste_loader.py  →  código de saída 0, sem [FALHOU], sem traceback.
CA-26. python tela/teste_modelo.py  →  código de saída 0, sem [FALHOU], sem traceback.
CA-27. python tela/teste_renderizador.py  →  código de saída 0, sem [FALHOU], sem traceback.
CA-28. python tela/teste_diagnostico.py  →  código de saída 0, sem [FALHOU], sem traceback
       (arquivo não alterado — diagnóstico do Orquestrador preservado).
CA-29. python tela/teste_demo.py  →  código de saída 0, sem [FALHOU], sem traceback
       (arquivo não alterado — demo não foi alterada).
```

### Critérios sobre escopo e rastreabilidade

```
CA-30. config/telas/orquestrador.json não foi alterado.
CA-31. config/telas/destino_minimo.json não foi alterado.
CA-32. config/telas/stub_b.json não foi alterado.
CA-33. Nenhum contrato em docs/contratos/ foi alterado.
CA-34. Nenhuma ADR em docs/adr/ foi alterada.
CA-35. docs/NOMENCLATURA.md não foi alterado.
CA-36. Nenhum arquivo fora da lista de permitidos foi criado ou alterado.
CA-37. docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
       foi criado pelo executor.
CA-38. Nenhum commit foi realizado pelo executor.
CA-39. Nenhum __pycache__ ou .pyc permanece no repositório após os testes.
```

---

## Comandos obrigatórios de verificação

O executor deve executar **todos** os comandos abaixo e confirmar saída limpa.

### Validade do JSON da tela isolada

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
```

### JSONs de produção inalterados (verificação de integridade)

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
python -m json.tool config/telas/stub_b.json >/dev/null && echo "stub_b.json OK"
```

### Testes unitários

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
```

Todos devem encerrar com código de saída 0, não imprimir linhas `[FALHOU]` e não
produzir traceback. Cabeçalhos, seções, resumos e linhas diagnósticas já
existentes nos harnesses de teste são permitidos.

### Pipeline de diagnóstico (integridade do Orquestrador)

```bash
python tela/diagnostico.py
```

A saída deve ser idêntica à saída anterior ao H-0012 (o Orquestrador não mudou).

### Loader sobre a tela isolada

```bash
python -c "
import sys; sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('tela/loader.py').resolve().parent.parent))
from tela.loader import carregar_tela
raw = carregar_tela(None, 'grupo_minimo')
print('id:', raw['id'])
print('grupo tipo:', raw['corpo']['elementos'][0]['tipo'])
print('OK — grupo_minimo carregado')
"
```

### Verificação de cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
```

Ambos devem retornar vazio.

```bash
git status --short
git diff --name-only
```

O executor não faz commit. O relatório IMP-0012 deve descrever os arquivos
alterados observados por esses comandos.

---

## Relatório de implementação obrigatório

O executor deve criar:

```
docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md
```

O relatório deve conter no mínimo:

1. Lista exaustiva de arquivos criados e alterados.
2. Decisões de implementação tomadas (e.g., como o modelo representa o grupo).
3. Saída completa de cada comando de verificação executado.
4. Status final: PASSOU / FALHOU (com detalhe de cada falha).
5. Confirmação de que nenhum arquivo proibido foi alterado.
6. Confirmação de que nenhum commit foi realizado.

O relatório **não cria regra nova**. Apenas evidencia o que foi feito.

---

## Instrução de bloqueio ao executor (OpenCode/GLM)

Leia este handoff integralmente antes de escrever qualquer código.

**Regras de execução obrigatórias:**

1. Não decidir arquitetura nova. Toda decisão arquitetural que não esteja
   coberta por este handoff ou pelos contratos citados deve ser reportada
   como `ARCHITECTURE_REVIEW_REQUIRED`.

2. Não alterar contrato, ADR, NOMENCLATURA nem INDICE.

3. Não resolver lacuna por inferência. Se faltar regra, arquivo permitido
   ou critério verificável, parar com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`
   e descrever o que falta.

4. Não fazer commit.

5. Não implementar nada fora do escopo positivo listado na seção "Escopo positivo".

6. Criar o relatório de implementação `IMP-0012-grupo-estrutural-minimo-tela-isolada.md`
   antes de encerrar.

### Parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

```
- A implementação exigir alterar contrato, ADR ou NOMENCLATURA.
- A implementação exigir criar registry, nova classe de elemento, ou
  novo mecanismo de binding não coberto por este handoff.
- A saída visual do Orquestrador mudar como efeito colateral das
  alterações em loader.py, modelo.py ou renderizador.py.
- A implementação exigir alterar tela/diagnostico.py ou alterar a
  saída do Orquestrador.
- A implementação exigir alterar tela/demo.py.
- Houver contradição entre este handoff e um contrato ou ADR vigente.
- Houver lacuna de especificação que impeça decidir sem assumir arquitetura.
```

### Parar com `BLOCKED` se:

```
- config/telas/grupo_minimo.json não puder ser criado no caminho especificado.
- tela/loader.py, tela/modelo.py ou tela/renderizador.py estiverem ausentes.
- Algum arquivo necessário não estiver na lista de arquivos permitidos.
- Erro de importação em tela/ que impeça executar os testes.
- Algum critério de aceite não puder ser verificado.
```

---

## Regra de granularidade (registro normativo)

Este handoff implementa **uma única capacidade nova de composição**:
suporte de código ao tipo estrutural `grupo` com 1 elemento funcional.

Mudança puramente declarativa em JSON não vira handoff próprio quando o
suporte já existe (`contrato_processo_desenvolvimento.md` seção 9). O H-0012
exige handoff porque introduz suporte de código novo: o tipo `"grupo"` não
existe hoje no loader, no modelo nem no renderer.

**Consequência para ciclos futuros**: adicionar nova tela com `grupo` por JSON
(após o H-0012 estar implementado) não exigirá handoff próprio, pois será
mudança declarativa com suporte já existente.

---

## Resumo de restrições futuras

As restrições abaixo são impostas pelo H-0012 para **este ciclo**. Ciclos
futuros podem remover ou relaxar restrições por ADR ou handoff próprio:

| Restrição | Ciclo atual | Possível relaxação |
|---|---|---|
| Grupo com exatamente 1 elemento | H-0012 | Handoff futuro (H-0013+) |
| Sem grupo dentro de grupo | H-0012 | Handoff futuro |
| Elemento funcional recomendado: `dashboard` | H-0012 | Sem restrição futura — qualquer funcional vale |
| Tela isolada — Orquestrador não migrado | H-0012 | Handoff futuro |
| Sem `lado_a_lado` no grupo | H-0012 | Handoff futuro |
| Sem distribuição percentual | H-0012 | Handoff futuro |
