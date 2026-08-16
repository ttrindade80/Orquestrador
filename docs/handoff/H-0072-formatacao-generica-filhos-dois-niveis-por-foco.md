# H-0072 — Capacidade genérica de formatação dos filhos de `dois_niveis_por_foco`

## 1. Metadata e rastreabilidade

```yaml
projeto: Orquestrador
adr: ADR-0047
handoff: H-0072
data_criacao: 2026-08-15
data_patch: 2026-08-15
patch: P01
status: CONCLUIDO
prontidao_documental_apos_p01: HANDOFF_APPROVED
predecessor_documental: aplicacao_documental_ADR-0047_pos_P02
estado_documental_transportado:
  ADR-0047:
    patch: P03
    status_qa: ADR_APPROVED_WITH_NOTES
    achado_material_pendente: nenhum
  aplicacao_documental_ADR-0047:
    patch: P02
    status_qa: ADR_APPLICATION_APPROVED
    contratos_reconciliados:
      - docs/contratos/contrato_console.md (secao 25)
      - docs/contratos/contrato_tela_json.md (secao 36)
      - docs/contratos/contrato_json_console.md (secao 15)
    nomenclatura_reconciliada:
      - docs/nomenclatura/32_CONSOLE.md (4.11)
      - docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md (4.6)
  achado_material_pendente: nenhum
  decisao_documental_aberta: nenhuma
dimensionamento_da_atividade:
  H-0072: capacidade_generica_de_formatacao_dos_filhos (este handoff)
  H-0073: aplicacao_da_capacidade_as_telas_existentes_incluindo_h0063
h0073_fora_de_escopo: true
h0073_preservado_neste_patch: true
relatorio_patch_handoff: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0072_P01.md
relatorio_patch_implementacao: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md
relatorio_implementacao_original_nao_sobrescrever: docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md
qa_final_implementacao: I1_IMPLEMENTATION_APPROVED
validacao_manual_final: MANUAL_REVALIDATION_APPROVED
achados_abertos: nenhum
```

Estado final do handoff: capacidade genérica concluída, incluindo tabulação
dinâmica 5..10, designador configurável por `prefixo`/`sufixo`, apresentações
`texto`/`tabela`, alinhamento global, espaçamento 3..8, quebra e resize com
preservação do item lógico. A revalidação manual posterior de H-0073 encerrou
VM-H0073-001 e VM-H0073-002. H-0070 permanece resíduo histórico não causal.

Este handoff autoriza exclusivamente a **implementação da capacidade
genérica** declarada pela ADR-0047: suporte, no sistema já existente de
`dois_niveis_por_foco`, à configuração estrutural
`formato.dois_niveis_por_foco.filho` (tabulação, designador, apresentação
`texto`/`tabela`, colunas e espaçamento). Não autoriza QA do handoff nesta
etapa de patch documental. Não autoriza aplicar a capacidade a `h0055` ou
`h0063`. Não autoriza alterar H-0073.

O patch P01 não redesenha H-0072. Corrige somente a expressividade do
designador estrutural, alinhada à ADR-0047 P03 e à aplicação documental
pós-P02 já aprovada: `designador` passa a admitir `prefixo` e `sufixo`
opcionais, além de `tipo` obrigatório. Tabulação, apresentação
`texto`/`tabela`, colunas, espaçamento, alinhamento global, quebra
multilinha, resize, item lógico, seleção, navegação e a separação
configuração × conteúdo × renderer permanecem integralmente preservados.

---

## 2. Capacidade coesa

Implementar, dentro do renderer e do loader já existentes para
`politica_navegacao.tipo = "dois_niveis_por_foco"` (ADR-0042), a leitura,
validação e aplicação física do bloco declarativo
`formato.dois_niveis_por_foco.filho` do elemento `console`, com:

1. `tabulacao.minimo` / `tabulacao.maximo` — recuo declarativo pai→filho;
2. `designador` — objeto fechado com `tipo` obrigatório
   (`decimal_composto`, `alfabetico_maiusculo`, `nenhum`) e adornos
   opcionais `prefixo` / `sufixo` (strings); o visual dos tipos visuais é
   `prefixo + designador_base_do_tipo + sufixo`;
3. `apresentacao` — `"texto"` (fluxo já vigente) ou `"tabela"` (apresentação
   tabular local, sem cabeçalho/borda/título);
4. `tabela.colunas[].campo` — referência semântica ordenada aos dados de
   cada coluna, quando `apresentacao = "tabela"`;
5. `tabela.espacamento.minimo` / `.maximo` — vão declarativo entre colunas.

A capacidade é genérica: nenhuma tela concreta de H-0055 ou H-0063 é
alterada por este handoff. A prova de que a capacidade funciona é feita
por fixtures e testes próprios deste handoff (§16, §17, §21.1), nunca por
edição de `h0055` ou `h0063`. H-0055 entra apenas como caso de capacidade
equivalente (`tipo: alfabetico_maiusculo` + `sufixo: ")"` → `A)`).

---

## 3. Autoridades

Autoridade normativa integral, sem reabertura:

- `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md` — decisões
  D-DNF-01 a D-DNF-11; schema literal fechado em §4.13 (P03: `prefixo` e
  `sufixo` no designador estrutural).
- `docs/contratos/contrato_console.md` §22.16 (política `dois_niveis_por_foco`,
  ADR-0042, preservada integralmente) e §25 (comportamento de formatação,
  ADR-0047; §25.3: `prefixo + designador_base + sufixo`).
- `docs/contratos/contrato_tela_json.md` §36 (schema literal declarativo do
  bloco `formato.dois_niveis_por_foco.filho`; §36.4: objeto `designador`
  com `tipo`, `prefixo` e `sufixo`).
- `docs/contratos/contrato_json_console.md` §7.1 (`politica_navegacao.tipo`)
  e §15 (fronteira: documento externo de conteúdo não declara apresentação).
- `docs/nomenclatura/32_CONSOLE.md` §4.4 (`ec`/`tg`/`tx`), §4.10
  (`dois_niveis_por_foco`, ADR-0042) e §4.11 (unidade inteira do filho
  deslocada, ADR-0047).
- `docs/nomenclatura/44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` §4.6
  (apresentação dos filhos, tabulação, colunas, espaçamento).

Nenhuma decisão de schema, localização ou nomenclatura fica em aberto para
este handoff: ADR-0047 §4.13 (P03) e as três seções de contrato acima já
fecham literalmente local, cardinalidade e nomes de campo. Não permanece
decisão documental aberta.

---

## 4. Arquivos nominais do patch de implementação P01

A implementação original de H-0072 já existe e foi aprovada. Este patch
não a redesenha. Levantamento focal restrito aos arquivos listados no
prompt de P01. O menor delta está nominalmente fechado abaixo. Nenhuma
decisão de arquivo permanece para PATCH_IMPLEMENTACAO.

### 4.1 Arquivos a editar no patch de implementação

| Arquivo | Papel atual | Delta causal P01 |
|---|---|---|
| `tela/carregamento/formato_dois_niveis_por_foco.py` | `_validar_designador_filho` aceita somente a chave `tipo` | Aceitar exatamente `tipo`, `prefixo` e `sufixo`. `tipo` obrigatório. `prefixo`/`sufixo` opcionais string. Chaves desconhecidas rejeitadas. `tipo: nenhum` não admite `prefixo` nem `sufixo`. |
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` | Fixture genérica; `console_h0072_tabela` declara só `tipo: alfabetico_maiusculo` | Acrescentar `prefixo: "("` e `sufixo: ")"` nesse console. Preservar `console_h0072_texto` (`decimal_composto` sem adornos) e `console_h0072_sem_designador` (`nenhum` sem adornos). Continua fixture genérica; não vira especialização de H-0055. |
| `tela/teste_formato_filho_dois_niveis_por_foco.py` | Suíte original (18 casos, V-DNF-01..11) | Manter a regressão aprovada. Acrescentar os testes de §21.1, inclusive o caso de capacidade equivalente a H-0055 (`A)`). |
| `demo/teste_demo_h0072_formatacao_generica.py` | Demonstração pelo ponto de entrada real | Comprovar adornos genéricos `(A)` / `(B)` no console de tabela, sem alterar navegação entre os três consoles. |

### 4.2 Arquivos avaliados e não autorizados a editar

Leitura focal comprovou ausência de mudança causal. PATCH_IMPLEMENTACAO
não os edita.

| Arquivo | Motivo |
|---|---|
| `tela/modelo.py` | Já transporta o dict inteiro `formato.dois_niveis_por_foco.filho` em `formato_filho_dois_niveis`, sem decompor `designador`. `prefixo`/`sufixo` fluem automaticamente. |
| `tela/renderizacao/designadores.py` | `_texto_designador` já emite `prefixo + nucleo + sufixo` e retorna vazio para `nenhum`. Reutilizar; não duplicar lógica. |
| `tela/renderizacao/conteudo_externo.py` | `_linhas_dois_niveis_formatado_com_mapa` já passa `designador_cfg` integral a `_texto_designador`. Não mescla o designador do documento de conteúdo. |
| `tela/carregamento/tela_json.py` | Já conecta `_validar_formato_dois_niveis_filho`. A assinatura não muda. |
| `tela/navegacao.py` | `formato_filho_dois_niveis()` devolve o dict transportado. Sem nova política de navegação. |
| `tela/selecao.py` | Semântica de seleção preservada. |
| `tela/renderizacao/console.py` | Despacho vigente; geometria já delegada. |
| `tela/renderizacao/matriz_participantes.py` | Sem eixo causal de designador. |
| `demo/demo.py` | Catálogo do cenário H-0072 já registrado; o id da tela não muda. |

### 4.3 Arquivos somente para teste/leitura

| Arquivo | Papel |
|---|---|
| `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json` | Documento externo de conteúdo: permanece dados. Não alterar. O sufixo `")"` não é obtido daqui. |
| `tela/teste_navegacao.py` | Regressão de navegação `dois_niveis_por_foco`. Não exigir edição. |
| `tela/teste_loader.py` | Os novos casos de schema ficam no teste dedicado de §4.1. Não exigir edição. |
| `demo/teste_demo_console.py` | H-0055 concreto permanece fora deste patch. |

### 4.4 Arquivos preservados (não alterar neste handoff nem no patch de implementação P01)

- `config/telas/demo/h0055_dois_niveis_por_foco.json`
- `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `config/telas/demo/h0062_estilo.json`
- `docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md`
- `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- `docs/contratos/contrato_console.md`, `contrato_tela_json.md`,
  `contrato_json_console.md`
- `docs/nomenclatura/32_CONSOLE.md`,
  `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md`

H-0055 não é configurado concretamente neste patch. A aplicação concreta
continua pertencendo a H-0073, retomado somente após QA deste handoff,
PATCH_IMPLEMENTACAO H-0072 P01 e QA dessa implementação.

---

## 5. Decisão da fixture genérica H-0072

Alterar a fixture estrutural é necessário para a demonstração genérica
comprovar adornos pelo ponto de entrada real (`contrato_console.md` §20.5).

Decisão nominal:

- `console_h0072_texto`: preservar `designador: { tipo: decimal_composto }`
  sem `prefixo`/`sufixo` (compatibilidade da ausência).
- `console_h0072_tabela`: conservar `tipo: alfabetico_maiusculo` e
  acrescentar `prefixo: "("` e `sufixo: ")"`. Resultado `(A)`, `(B)`.
  Teste da capacidade genérica; não é a forma de H-0055 (que usa somente
  `sufixo: ")"`).
- `console_h0072_sem_designador`: preservar `tipo: nenhum` sem adornos.
- Nenhum dado semântico existente é reescrito. Os três consoles, títulos,
  colunas `responsavel`/`prazo` e a distribuição `[1, 1, 1]` permanecem.
- O documento externo de conteúdo permanece integralmente inalterado.

O caso `A)` / `B)` / `C)` / `D)` (H-0055) não entra nesta fixture. Fica
no teste de capacidade de §21.1 item 2.

---

## 6. Escopo positivo

- Extração e validação do bloco `formato.dois_niveis_por_foco.filho`
  (`tabulacao`, `designador`, `apresentacao`, `tabela.colunas`,
  `tabela.espacamento`) no elemento `console` do JSON estrutural da tela.
- Cálculo físico, pelo renderer, de: tabulação efetiva dentro do intervalo
  declarado; deslocamento da unidade inteira do filho (`ec`, `tg`,
  designador, conteúdo); designador concreto (`1.1`, `A`, `A)` quando
  `sufixo: ")"`, `(A)` quando prefixo+sufixo, ou ausente); largura de
  colunas a partir do conteúdo real; espaçamento efetivo entre colunas
  dentro do intervalo declarado; quebra multilinha quando necessário;
  recálculo em resize.
- Alinhamento global das colunas sobre todos os filhos do console,
  independentemente do pai corrente.
- Validação fechada do schema, com rejeição determinística de configuração
  inválida — inclusive adornos não string, chave desconhecida em
  `designador` e `tipo: nenhum` com `prefixo` ou `sufixo`.
- Demonstração reproduzível da capacidade por fixture e teste próprios,
  acessível pelo ponto de entrada real (`demo/demo.py`), incluindo adornos.

## 7. Escopo negativo

- Não aplicar a nova configuração a `h0055` ou a `h0063` — isso é H-0073.
- Não alterar H-0073 neste patch.
- Não alterar `politica_navegacao.tipo`, a navegação de
  `dois_niveis_por_foco`, o toroide de pais, o toroide de filhos por pai ou
  a seleção exclusiva obrigatória de filho por pai (ADR-0042).
- Não criar terceiro nível, não tornar o console passivo, não transformar a
  apresentação tabular local em política `tabela`.
- Não introduzir campo de largura física final, posição final, quebra
  pronta ou geometria calculada no JSON.
- Não mover configuração de apresentação para o documento externo de
  conteúdo, nem mover dados para o JSON estrutural da tela.
- Não criar herança automática do documento de conteúdo, campo `fonte`,
  campo `herdar`, parsing de designador do conteúdo nem nova política de
  navegação.
- Não criar fallback silencioso para configuração inválida.
- Não fazer QA_HANDOFF nem PATCH_IMPLEMENTACAO nesta etapa documental.

---

## 8. Configuração de entrada (JSON estrutural da tela)

Local literal (`contrato_tela_json.md` §36.2), dentro de `console.formato`:

```json
"formato": {
  "dois_niveis_por_foco": {
    "filho": {
      "tabulacao": { "minimo": 5, "maximo": 10 },
      "designador": {
        "tipo": "decimal_composto",
        "prefixo": "<string opcional>",
        "sufixo": "<string opcional>"
      },
      "apresentacao": "tabela",
      "tabela": {
        "colunas": [
          { "campo": "<campo_semantico_do_conteudo>" },
          { "campo": "<campo_semantico_do_conteudo>" }
        ],
        "espacamento": { "minimo": 3, "maximo": 8 }
      }
    }
  }
}
```

Regras de forma (já fechadas, apenas propagadas):

- existe somente quando `politica_navegacao.tipo = "dois_niveis_por_foco"`;
- `tabulacao.minimo`/`.maximo`: inteiros positivos, `minimo <= maximo`;
- `designador` é objeto fechado:
  - `tipo` obrigatório: `decimal_composto` \| `alfabetico_maiusculo` \|
    `nenhum`;
  - `prefixo`: opcional, string; ausência equivale a vazio para tipos
    visuais;
  - `sufixo`: opcional, string; ausência equivale a vazio para tipos
    visuais;
  - tipos visuais: `designador_visual = prefixo + designador_base_do_tipo
    + sufixo`;
  - `tipo: nenhum`: não emitir designador; `prefixo` e `sufixo` devem
    estar ausentes;
  - chaves desconhecidas são inválidas;
- `apresentacao`: exatamente `"texto"` ou `"tabela"`;
- bloco `tabela` existe se e somente se `apresentacao = "tabela"`;
- `tabela.colunas`: array com mínimo 1 elemento, cada um com exatamente o
  campo `campo`; ordem do array = ordem visual; quantidade = número de
  colunas; `numero_colunas` não existe;
- `tabela.espacamento.minimo`/`.maximo`: inteiros positivos,
  `minimo <= maximo`;
- declarado uma única vez por tela, nunca repetido por item filho.

Caso de capacidade equivalente a H-0055 (teste, não fixture concreta):

```yaml
designador:
  tipo: alfabetico_maiusculo
  sufixo: ")"
```

Resultado: `A)`, `B)`, `C)`, `D)` — nunca `A`, `B`, `C`, `D`. O conteúdo
externo não participa da obtenção do sufixo.

## 9. Conteúdo/dados como entrada separada

O documento externo de conteúdo (envelope multinível, `contrato_json_console.md`
§12) continua fornecendo exclusivamente os dados: os nós de nível filho
expõem os campos semânticos referenciados por `tabela.colunas[].campo`. O
documento de conteúdo **não** declara tabulação, apresentação, colunas,
espaçamento, `prefixo` nem `sufixo` — essas declarações pertencem
exclusivamente ao JSON estrutural da tela (§8). A fixture de conteúdo desta
atividade permanece dados e não é alterada por P01.

## 10. Estado de runtime

Não são estado de runtime: os valores declarados em
`formato.dois_niveis_por_foco.filho` (configuração fixa da tela). São estado
de runtime, calculados a cada render e nunca persistidos no JSON: tabulação
efetiva, largura efetiva de cada coluna, espaçamento efetivo, quebras
físicas, posições finais, texto concreto do designador visual. Cursor, foco,
escolha exclusiva do filho por pai e página permanecem os mecanismos de
runtime já fechados por ADR-0031, ADR-0038 e ADR-0042 — não redefinidos por
este handoff.

## 11. Saída física esperada

Para cada filho: uma unidade lógica única, deslocada da margem do pai por
uma tabulação efetiva (§12), iniciando por `ec`, seguida por `tg` quando
existir, designador quando existir, e conteúdo — em `texto` (uma linha,
salvo modo verboso já vigente) ou em `tabela` local (colunas alinhadas,
sem cabeçalho/borda/título, com espaçamento efetivo entre colunas). Quando a
largura não permitir, o conteúdo quebra em linhas físicas adicionais sem
criar novo cursor, toggle ou identidade lógica.

O designador visual, quando o tipo é visual, é
`prefixo + designador_base + sufixo`, reutilizando
`tela/renderizacao/designadores.py::_texto_designador`. Adornos apenas
envolvem o designador-base; não modificam a geração de `1.1` nem de `A`.

---

## 12. Regras de tabulação

- Toda apresentação de `dois_niveis_por_foco` que declarar filhos deve
  declarar `tabulacao.minimo` e `.maximo`; para as fixtures desta atividade,
  mínimo 5 e máximo 10 — não hardcoded no renderer.
- O renderer usa o maior valor que couber dentro do intervalo: mínimo se só
  o mínimo couber, valor intermediário se este couber, máximo se o máximo
  couber.
- Sobra de largura após o máximo permanece à direita da apresentação — sem
  ampliação artificial de tabulação.

## 13. Relação tabulação × `ec` × `tg` × designador × conteúdo

Ordem física obrigatória:

```text
tabulação → ec → tg (quando existir) → designador (quando existir) → conteúdo
```

- a tabulação começa antes de `ec`;
- `ec`, `tg`, designador e conteúdo do filho deslocam-se juntos, como
  unidade inteira — nunca apenas o texto;
- o cursor do filho (`ec`) fica sempre para dentro do primeiro caractere
  visual do item pai;
- é defeito deixar `ec` ou `tg` alinhado ao pai enquanto só o texto recua;
- `ec` e `tg`, quando ambos existem, continuam coexistindo em posições
  distintas e adjacentes, sem sobreposição (`32_CONSOLE.md` §4.4).

## 14. Apresentação `texto`

Quando `apresentacao = "texto"`: preserva integralmente o fluxo de
apresentação de filho já vigente (uma linha em modo não verboso, expansão
em modo verboso conforme já fechado). O bloco `tabela` não é exigido nem
usado.

## 15. Apresentação `tabela` (local)

Quando `apresentacao = "tabela"`: usa `tabela.colunas` (mínimo 1 coluna;
ordem do array = ordem visual; quantidade = número de colunas; sem
`numero_colunas`; configuração declarada uma única vez por tela). Cada
filho continua sendo um único item lógico — cada linha física da tabela
local pertence a esse mesmo item lógico. A tabela local não tem cabeçalho,
linha separadora, borda própria nem título próprio. Não transforma
`politica_navegacao.tipo` em `"tabela"` — a política permanece
`dois_niveis_por_foco`.

## 16. Alinhamento global das colunas

Para uma mesma instância de console: a largura de cada coluna é calculada
considerando todos os filhos do console, inclusive filhos de pais
diferentes — nunca uma grade independente por pai. Trocar o pai corrente
não desloca horizontalmente as colunas.

## 17. Espaçamento 3..8

`tabela.espacamento.minimo = 3`, `.maximo = 8` para as fixtures desta
atividade. O renderer usa o maior valor que couber: 3 se só 3 couber, valor
intermediário se este couber, 8 se 8 couber. Se sobrar largura após 8, a
sobra fica à direita de toda a tabela — sem ampliação artificial das
colunas.

## 18. Quebra multilinha

Quando a tabela não couber horizontalmente mesmo após reduzir tabulação e
espaçamento a seus mínimos: o conteúdo das células quebra em múltiplas
linhas físicas. A quebra não cria novo item lógico, novo cursor, novo
toggle nem nova identidade/seleção. Somente a primeira linha física do item
recebe os indicadores aplicáveis (cursor, toggle, designador).

## 19. Resize

Ao redimensionar: preservar o item lógico corrente; recalcular tabulação
efetiva, largura das colunas, espaçamento efetivo e quebras; recalcular
posições físicas. Nenhuma geometria calculada é persistida no JSON.

---

## 20. Validações de schema

O loader deve rejeitar de forma fechada, sem fallback silencioso, ao menos:

| Caso | Condição inválida |
|---|---|
| V-DNF-01 | `tabulacao.minimo > tabulacao.maximo` |
| V-DNF-02 | `tabulacao.minimo`/`.maximo` não inteiro ou não positivo |
| V-DNF-03 | `apresentacao` fora de `"texto"` \| `"tabela"` |
| V-DNF-04 | bloco `tabela` ausente quando `apresentacao = "tabela"` |
| V-DNF-05 | bloco `tabela` presente quando `apresentacao = "texto"` (redundante — proibido) |
| V-DNF-06 | `tabela.colunas` vazio (array com 0 elementos) |
| V-DNF-07 | item de `tabela.colunas` sem o campo `campo` |
| V-DNF-08 | `tabela.espacamento.minimo > tabela.espacamento.maximo` |
| V-DNF-09 | `tabela.espacamento.minimo`/`.maximo` não inteiro ou não positivo |
| V-DNF-10 | `designador.tipo` fora de `decimal_composto` \| `alfabetico_maiusculo` \| `nenhum` |
| V-DNF-11 | bloco `formato.dois_niveis_por_foco.filho` presente quando `politica_navegacao.tipo` ≠ `"dois_niveis_por_foco"` |
| V-DNF-12 | `designador.prefixo` presente e não string |
| V-DNF-13 | `designador.sufixo` presente e não string |
| V-DNF-14 | chave desconhecida em `designador` (além de `tipo`, `prefixo`, `sufixo`) |
| V-DNF-15 | `designador.tipo = nenhum` com `prefixo` presente |
| V-DNF-16 | `designador.tipo = nenhum` com `sufixo` presente |

V-DNF-01 a V-DNF-11 permanecem da implementação original. V-DNF-12 a
V-DNF-16 são o delta P01. Configurações existentes só com `tipo` continuam
válidas.

---

## 21. Testes unitários e integrados necessários

A implementação original deve continuar demonstrando, no mínimo:

1. cursor de filho recuado junto com toggle e conteúdo (unidade deslocada);
2. tabulação no mínimo declarado;
3. tabulação no máximo declarado;
4. tabulação em valor intermediário;
5. designador `decimal_composto` sem adornos (`1.1`);
6. designador `alfabetico_maiusculo` sem adornos (`A`, `B` — nunca `A)`
   por default);
7. filho sem designador (`nenhum`);
8. apresentação `texto` preservando o fluxo vigente;
9. apresentação `tabela` com no mínimo 2 colunas;
10. alinhamento de colunas entre filhos de pais diferentes;
11. espaçamento entre colunas no mínimo declarado;
12. espaçamento entre colunas no máximo declarado;
13. sobra de largura à direita depois de aplicado o máximo (tabulação e/ou
    espaçamento);
14. quebra multilinha quando o conteúdo não cabe mesmo após compactação;
15. linha de continuação sem novo cursor, toggle ou identidade lógica;
16. resize preservando o item lógico corrente;
17. rejeição de cada um dos onze casos originais de schema inválido
    (§20, V-DNF-01 a V-DNF-11);
18. preservação integral da navegação de `dois_niveis_por_foco` (toroide de
    pais, toroide de filhos por pai, seleção exclusiva obrigatória) com a
    nova configuração presente.

O caso 6 original documentava `A)` como resultado de `alfabetico_maiusculo`
só com `tipo`. Isso era insuficiente. P01 corrige: sem adornos o resultado
é `A`; `A)` exige `sufixo: ")"` na configuração estrutural.

### 21.1 Testes obrigatórios adicionais P01

Além da regressão dos 18 casos, o patch de implementação deve exigir:

1. `alfabetico_maiusculo` sem adornos permanece `A`, `B`;
2. `alfabetico_maiusculo` + `sufixo: ")"` produz `A)`, `B)` — caso de
   capacidade equivalente a H-0055; nunca `A` / `B`; o conteúdo externo
   não fornece o sufixo;
3. `prefixo` funciona (`prefixo: "("` + `alfabetico_maiusculo` → `(A)`);
4. `prefixo` e `sufixo` juntos (`"("` + `")"` → `(A)`, `(B)`);
5. `decimal_composto` sem adornos permanece `1.1`;
6. `decimal_composto` com adornos apenas envolve o valor-base (ex.:
   `prefixo: "["`, `sufixo: "]"` → `[1.1]`; a geração de `1.1` não muda);
7. `prefixo` não string é rejeitado (V-DNF-12);
8. `sufixo` não string é rejeitado (V-DNF-13);
9. chave desconhecida em `designador` é rejeitada (V-DNF-14);
10. `tipo: nenhum` com `prefixo` é rejeitado (V-DNF-15);
11. `tipo: nenhum` com `sufixo` é rejeitado (V-DNF-16);
12. `tipo: nenhum` sem adornos continua sem designador visual;
13. ausência de `prefixo`/`sufixo` permanece compatível com as fixtures
    `console_h0072_texto` e `console_h0072_sem_designador`;
14. navegação/seleção permanecem inalteradas;
15. apresentação `texto`/`tabela` permanece inalterada.

Os itens 2, 3, 4 e 6 pertencem a
`tela/teste_formato_filho_dois_niveis_por_foco.py`. O item 2 não edita
`h0055_dois_niveis_por_foco.json`. Os itens 7–11 estendem o mesmo arquivo
de schema. O item 4 é também comprovado pela demonstração de §22 após a
alteração da fixture de tabela.

Todos os casos continuam executáveis por `pytest`, sem TTY real.

## 22. Demonstração reproduzível da capacidade genérica

- Fixture estrutural: `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json`
  (§5): texto com `decimal_composto` sem adornos; tabela com
  `alfabetico_maiusculo` + `prefixo: "("` + `sufixo: ")"`; sem designador
  com `nenhum`.
- Documento de conteúdo: `..._conteudo.json`, inalterado.
- Registro do cenário em `demo/demo.py` (já existente), acessível pelo
  ponto de entrada real (`contrato_console.md` §20.5).
- `demo/teste_demo_h0072_formatacao_generica.py` prova o carregamento e a
  renderização por `demo/demo.py`, inclusive `(A)` / `(B)` no console de
  tabela.

---

## 23. Critérios de aceite

Critérios originais, preservados:

- [ ] `formato.dois_niveis_por_foco.filho` é lido exclusivamente do elemento
  `console` do JSON estrutural da tela, nunca do documento externo.
- [ ] Os onze casos originais de schema inválido (§20, V-DNF-01 a V-DNF-11)
  são rejeitados de forma fechada, sem fallback silencioso.
- [ ] Tabulação efetiva usa o maior valor que couber no intervalo
  declarado; sobra permanece à direita.
- [ ] `ec`, `tg`, designador e conteúdo do filho deslocam-se juntos; nenhum
  caso de recuo isolado do texto.
- [ ] Designadores `decimal_composto`, `alfabetico_maiusculo` e `nenhum`
  funcionam sem criar identidade lógica nova.
- [ ] Apresentação `texto` preserva o fluxo vigente sem exigir bloco
  `tabela`.
- [ ] Apresentação `tabela` produz colunas alinhadas sem cabeçalho, borda,
  linha separadora ou título próprios, sem alterar
  `politica_navegacao.tipo`.
- [ ] Alinhamento de colunas é calculado sobre todos os filhos do console,
  inclusive de pais diferentes; trocar o pai corrente não desloca colunas.
- [ ] Espaçamento efetivo usa o maior valor que couber entre 3 e 8; sobra
  fica à direita de toda a tabela.
- [ ] Conteúdo maior que a largura disponível quebra em múltiplas linhas
  físicas sem criar novo item lógico, cursor, toggle ou identidade.
- [ ] Resize recalcula tabulação, colunas, espaçamento e quebras
  preservando o item lógico corrente; nenhuma geometria é persistida no
  JSON.
- [ ] A navegação, o toroide de pais, o toroide de filhos por pai e a
  seleção exclusiva obrigatória de filho por pai permanecem integralmente
  preservados (ADR-0042) com a nova configuração presente.
- [ ] `h0055` e `h0063` permanecem intocados por este handoff.
- [ ] Os dezoito casos de teste de §21 estão implementados e passam.
- [ ] A demonstração de §22 é acessível e reproduzível por `demo/demo.py`.

Critérios adicionais obrigatórios pós-P01:

- [ ] O schema aceita `prefixo` e `sufixo` opcionais string em `designador`.
- [ ] A validação está fechada (V-DNF-12 a V-DNF-16).
- [ ] H-0055 pode ser representado como `A)` por configuração estrutural
  equivalente (`tipo: alfabetico_maiusculo`, `sufixo: ")"`), comprovada
  por teste de capacidade; `h0055_dois_niveis_por_foco.json` não é editado.
- [ ] `tipo: nenhum` com adornos é rejeitado; sem adornos continua sem
  designador visual.
- [ ] O designador-base é preservado; adornos apenas o envolvem.
- [ ] Nenhum comportamento não relacionado regrediu.
- [ ] A suíte H-0072 continua verde.
- [ ] A demonstração genérica comprova adornos (`(A)`, `(B)`).
- [ ] O conteúdo externo continua sem configuração visual.

## 24. Relatórios

O relatório original da implementação,
`docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0072.md`, é histórico e **não**
deve ser sobrescrito.

O patch futuro de implementação P01 deve criar exclusivamente:

`docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0072_P01.md`

registrando: arquivos efetivamente alterados frente a §4.1; confirmação de
que §4.2 não foi editado; resultado da regressão de §21 e dos testes
adicionais de §21.1; confirmação de que `h0055`/`h0063`/H-0073 permanecem
intocados; confirmação de que o conteúdo externo da fixture H-0072 não foi
alterado; comando(s) de execução e resultado. Máximo normal: 900 palavras.

## 25. Política para temporários

Nenhum arquivo temporário de produção é necessário para esta capacidade —
a geometria calculada nunca é persistida (§10, §19). Arquivos temporários
eventualmente usados por testes (ex.: `tmp_path` do `pytest`) não podem ser
commitados nem deixar resíduo no repositório. Nenhum script auxiliar
descartável deve permanecer fora dos arquivos nominalmente autorizados em
§4.

## 26. Bloqueios

nenhum
\n