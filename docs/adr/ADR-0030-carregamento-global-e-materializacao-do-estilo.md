---
name: adr-0030-carregamento-global-e-materializacao-do-estilo
description: Formaliza o carregamento global e a materialização integral de config/estilo.json como autoridade exclusiva de aparência do terminal, eliminando hardcodings no renderer e definindo migração com estado final único
metadata:
  type: adr
  scope: estilo_e_runtime
  status: aceita
  data: "2026-07-22"
  substitui: null
rastreabilidade:
  rfc_origem: null
  issues_relacionadas: []

  documentos_normativos_afetados_futuros:
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md
    - docs/nomenclatura/10_ESTILO.md
    - docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md
    - docs/nomenclatura/32_CONSOLE.md
    - docs/adr/INDICE_ADR.md

  artefatos_tecnicos_afetados_futuros:
    - config/estilo.json
    - tela/renderizador.py
    - tela/loader.py

  contratos_afetados:
    - docs/contratos/contrato_estilo.md
    - docs/contratos/contrato_chip.md
    - docs/contratos/contrato_barra_de_menus.md
    - docs/contratos/contrato_console.md

  handoffs_bloqueados: []
---

# ADR-0030 — Carregamento global e materialização do estilo

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | ADR-0030 |
| Título | Carregamento global e materialização do estilo |
| Status | aceita |
| Data | 2026-07-22 |
| Origem | Decisão explícita do usuário |
| Relatório de levantamento | `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md` |

---

## 2. Status

`aceita`

A ADR foi aprovada após QA pós-patch-02 — resultado registrado em
`docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md`
(`status_canonico: ADR_APPROVED`, achado QA-POS-ADR0030-001 `RESOLVIDO`,
sem regressões nem achados novos).

A aplicação documental foi executada neste ciclo: contrato de estilo atualizado,
contratos de chip, barra e console inspecionados, módulo de nomenclatura de
estilo atualizado, índice de ADRs registrado.

**Estado no momento da aplicação documental** (histórico): QA da aplicação
pendente naquele momento; a migração de `config/estilo.json` e a implementação
(loader, renderer, testes) ainda não tinham sido realizadas — pertenciam ao
handoff do Bloco 1.

**Estado atual do ciclo** (pós H-0039):

```yaml
ADR: aceita
aplicacao_documental: aprovada
handoff: H1_HANDOFF_APPROVED
implementacao: I1_IMPLEMENTATION_APPROVED
validacao_manual: VALIDACAO_MANUAL_APROVADA
Bloco_1: concluido
Bloco_2: futuro
Bloco_3: futuro
```

---

## 3. Contexto

### 3.1 Estado material observado

O levantamento `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md` identificou os seguintes fatos sobre o estado atual:

**`config/estilo.json`:**

- Contém catálogos de presets para `borda` (seção `borda.presets`, três presets) e `chip` (seção `chip.presets`, sete presets).
- Contém indicadores de cursor e seleção:
  - `indicadores.selecionado`: catálogo com quatro presets e `preset_default: "Seta"`.
  - `indicadores.incluido`: catálogo com quatro presets e `preset_default: "Círculo"`.
  - `indicadores.concluido`: par direto `on`/`off` sem catálogo.
- `borda` e `chip` possuem catálogos mas **não possuem** campo `preset_default` indicando a opção ativa.
- Status do arquivo: `rascunho_inicial`.

**Loader (`tela/loader.py`):**

- Implementa `carregar_tela` (`tela/loader.py:1093-1155`), que carrega JSONs de tela e retorna `cabecalho`, `corpo`, `barra_de_menus`, `_raw` e `_config_lancador`.
- Não foi identificado loader ativo para `config/estilo.json`.
- Não foi identificada materialização dos campos planos de runtime `selecionado_simbolo`, `selecionado_off`, `incluido_on`, `incluido_off`.

**Renderer (`tela/renderizador.py`):**

- Declara `_BORDAS` como dicionário interno hardcoded (`tela/renderizador.py:153-164`) com chaves `"curva"` e `"reta"`.
- Aceita `tipo_borda: str = "curva"` como parâmetro de `renderizar_tela` (`tela/renderizador.py:2388-2391`).
- Monta chips com o formato `"[{tecla}]"` (`tela/renderizador.py:1140-1144`), sem consultar `config/estilo.json`.
- Não comprova consumo de `config/estilo.json`, nem dos campos materializados de indicadores.

**Testes existentes:**

- Cobrem `tipo_borda` com valores `"curva"` e `"reta"` e verificam caracteres esperados (`tela/teste_renderizador.py`).
- Não comprovam materialização de estilo a partir de `config/estilo.json`.

### 3.2 Correspondência entre hardcodings e presets existentes

| Hardcoding atual | Preset equivalente em `config/estilo.json` | Correspondência |
|---|---|---|
| `_BORDAS["curva"]`: `╭╮╰╯─│` (`tela/renderizador.py:154-158`) | `borda.presets["Borda Curva"]`: `╭╮╰╯─│` | Exata e inequívoca (sete caracteres) |
| Formato `"[{tecla}]"` (`tela/renderizador.py:1144`) | `chip.presets["Colchete"]`: todos os cinco campos — ver D5 | Parcial: delimitadores e cores preservam o visual atual; `caixa_alta: true` no arquivo não preserva — ver D5 |

---

## 4. Problema

Existe uma biblioteca persistida de estilo em `config/estilo.json`, mas o runtime não a usa como autoridade efetiva. O estado atual apresenta as seguintes lacunas:

```yaml
carregamento_de_estilo:         ausente
materializacao_para_runtime:    ausente
validacao_de_presets:           ausente
consumo_pelo_renderer:          ausente_ou_incompleto
borda_no_runtime:               hardcoded_em_renderizador
formato_visual_de_chip:         hardcoded_em_renderizador
preset_ativo_de_borda_no_estilo: ausente
preset_ativo_de_chip_no_estilo:  ausente
indicadores:
  selecionado:
    catalogo:       existente
    preset_default: existente
  incluido:
    catalogo:       existente
    preset_default: existente
  concluido:
    estrutura:      par_direto_on_off
```

Enquanto o `contrato_estilo.md` descreve a transformação dos presets em campos de runtime (seção 3.3), nenhum componente identificado no código ativo executa essa transformação para estilo. O renderer e demais consumidores decidem autonomamente sobre bordas, molduras de chip e símbolos de indicadores — violação do princípio de autoridade global exclusiva definido pelo contrato.

---

## 5. Decisões

### D1 — Autoridade global exclusiva

`config/estilo.json` é a autoridade global exclusiva para a aparência compartilhada do terminal.

Nenhuma classe de tela ou renderer pode hardcodar símbolo, cor, caractere de borda ou moldura de chip. Todo valor de aparência vem do objeto de estilo resolvido em tempo de execução.

JSONs de tela continuarão declarando composição, conteúdo e comportamento. Não declaram presets concorrentes de borda, chip ou indicadores neste ciclo.

### D2 — Catálogo e opção ativa

Cada categoria configurável deve possuir:

- catálogo de opções (`presets`);
- campo indicando a opção ativa (`preset_default`);
- validação da referência ativa pelo loader;
- materialização determinística dos campos de runtime a partir do preset ativo.

O par de campos `presets` + `preset_default` é o padrão canônico — já existente em `indicadores.selecionado` e `indicadores.incluido`. As seções `borda` e `chip` de `config/estilo.json` já possuem `presets`, mas ainda não possuem `preset_default`. A aplicação desta ADR deve incluir `preset_default` em `borda` e em `chip`, conforme os valores definidos nas decisões D4 e D5 abaixo.

### D3 — Escopo integral do estilo

O carregamento deve abranger todas as seções vigentes de `config/estilo.json`:

| Seção | Natureza | Tratamento pelo loader |
|---|---|---|
| `_meta` | Metadado de configuração | Lido; não materializado como campo de runtime visual |
| `borda` | Catálogo com `preset_default` (a adicionar) | Resolve preset ativo → produz sete campos de borda de runtime |
| `chip` | Catálogo com `preset_default` (a adicionar) | Resolve preset ativo → produz cinco campos de chip de runtime |
| `indicadores.concluido` | Par direto `on`/`off` | Lê `on` e `off` diretamente → produz `concluido_on` e `concluido_off` |
| `indicadores.selecionado` | Catálogo com `preset_default` + campo `off` | Resolve preset → extrai `simbolo` → produz `selecionado_simbolo`; lê `off` → produz `selecionado_off` |
| `indicadores.incluido` | Catálogo com `preset_default` | Resolve preset → extrai `on` e `off` → produz `incluido_on` e `incluido_off` |

`indicadores.concluido` não é convertido em catálogo por esta ADR. Estruturas distintas são interpretadas conforme sua natureza real, não uniformizadas por simetria. Uma mudança estrutural de `concluido` exige justificativa e ciclo próprios.

### D4 — Preservação da aparência vigente de borda

O preset de borda que reproduz exatamente a aparência atual é:

```text
"Borda Curva"
```

Correspondência verificada (levantamento, seção 3.2 desta ADR):

| Campo do preset | Valor em `config/estilo.json` | Valor hardcoded em `_BORDAS["curva"]` |
|---|---|---|
| `canto_superior_esquerdo` | `╭` | `tl: "╭"` |
| `canto_superior_direito` | `╮` | `tr: "╮"` |
| `canto_inferior_esquerdo` | `╰` | `bl: "╰"` |
| `canto_inferior_direito` | `╯` | `br: "╯"` |
| `traco_superior` | `─` | `h: "─"` |
| `traco_inferior` | `─` | `h: "─"` |
| `lateral` | `│` | `v: "│"` |

A opção ativa a persistir em `config/estilo.json`:

```json
"borda": {
  "preset_default": "Borda Curva",
  "presets": { ... }
}
```

### D5 — Preservação da aparência vigente de chip

O preset de chip que reproduz a moldura atual é:

```text
"Colchete"
```

Correspondência verificada para todos os cinco campos do preset (levantamento, seção 3.2 desta ADR):

| Campo do preset | Valor em `config/estilo.json` | Comportamento atual do renderer | Análise de preservação visual |
|---|---|---|---|
| `caractere_esquerdo` | `[` | Formato hardcoded `"[{tecla}]"` — caractere `[` | Exata e inequívoca |
| `caractere_direito` | `]` | Formato hardcoded `"[{tecla}]"` — caractere `]` | Exata e inequívoca |
| `caixa_alta` | `true` (valor atual no arquivo) | Renderer não aplica caixa alta; textos como "Sair", "Voltar", "Ajuda", "Verboso" preservam a capitalização declarada pelas telas | Não preserva: consumir `true` alteraria a aparência inicial |
| `cor_texto` | `"padrão"` | Renderer não aplica cor diferenciada de texto | Preserva: `"padrão"` não introduz nova cor concreta |
| `cor_fundo` | `"padrão"` | Renderer não aplica cor de fundo diferenciada | Preserva: `"padrão"` não introduz nova cor concreta |

Registro do campo `caixa_alta`:

```yaml
preset_ativo: "Colchete"
caractere_esquerdo: "["
caractere_direito: "]"
caixa_alta:
  valor_atual_no_arquivo: true
  valor_final_decidido: false
  motivo: preservar_capitalizacao_atual_dos_rotulos
cor_texto: "padrão"
cor_fundo: "padrão"
```

Implicações para a migração:

- Os delimitadores `[` e `]` já correspondem ao visual atual; não requerem alteração nos delimitadores.
- `caixa_alta: true` no arquivo atual **não preserva** o visual vigente: ao ser consumido pelo renderer, aplicaria maiúsculas a textos como "Sair", "Voltar", "Ajuda" e "Verboso", alterando a aparência inicial.
- A migração deve mudar `chip.presets["Colchete"].caixa_alta` de `true` para `false`. Essa alteração em `config/estilo.json` pertence ao ciclo de implementação do Bloco 1 (seção 10.2); não pertence à aplicação documental.
- `cor_texto: "padrão"` e `cor_fundo: "padrão"` não introduzem nova cor concreta neste ciclo e preservam a aparência vigente.
- O renderer deverá consumir os cinco campos do preset resolvido (`caractere_esquerdo`, `caractere_direito`, `caixa_alta`, `cor_texto`, `cor_fundo`).
- O estado inicial continuará visualmente equivalente ao atual somente após a mudança de `caixa_alta` para `false`.

A opção ativa a persistir em `config/estilo.json`:

```json
"chip": {
  "preset_default": "Colchete",
  "presets": { ... }
}
```

### D6 — Indicador do cursor

Preservar como escolha global ativa:

```yaml
indicadores:
  selecionado:
    preset_default: "Seta"
```

O símbolo resultante é obtido do catálogo:

```text
config/estilo.json → indicadores.selecionado.presets["Seta"].simbolo → "→"
```

O símbolo `→` não pode ser repetido como constante operacional no renderer. A documentação pode citar `→` como valor vigente do preset ativo sem transformá-lo em autoridade paralela.

### D7 — Indicador de inclusão

Preservar como escolha global ativa:

```yaml
indicadores:
  incluido:
    preset_default: "Círculo"
```

Os valores resultantes são obtidos do catálogo:

```text
config/estilo.json → indicadores.incluido.presets["Círculo"] → on: "●", off: "○"
```

Esses valores serão consumidos futuramente pelo mecanismo de seleção múltipla (Bloco 3). O comportamento de seleção não pertence a esta ADR.

### D8 — Carregamento e materialização

O loader executará um carregamento único do estilo com as seguintes responsabilidades, nesta ordem:

1. Ler `config/estilo.json`.
2. Validar a estrutura (seções obrigatórias, tipos, integridade dos catálogos).
3. Resolver a opção ativa de cada categoria com catálogo (`borda`, `chip`, `selecionado`, `incluido`).
4. Ler campos diretos das categorias sem catálogo (`concluido`, `off` de `selecionado`).
5. Produzir uma representação de runtime com os campos planos esperados pelo contrato.
6. Disponibilizar essa representação aos consumidores (renderer e demais).
7. Não reler nem redecidir presets em cada chamada de renderização.
8. Não armazenar estado vivo de navegação, seleção, cursor ou foco.

A responsabilidade de carregamento, validação e materialização pertence ao loader ou camada equivalente. A ADR não escolhe nome de função, classe ou módulo específico — essa escolha pertence ao handoff de implementação.

### D9 — Validações obrigatórias do loader

O loader deve produzir erro explícito e impedir a renderização com estilo parcialmente resolvido nas seguintes situações:

| Condição | Comportamento |
|---|---|
| Arquivo `config/estilo.json` ausente | Erro explícito; encerramento imediato |
| JSON inválido (parse error) | Erro explícito; encerramento imediato |
| Seção obrigatória ausente (`borda`, `chip`, `indicadores`) | Erro explícito; encerramento imediato |
| `preset_default` ausente em categoria com catálogo | Erro explícito; encerramento imediato |
| Catálogo vazio em categoria que exige opções | Erro explícito; encerramento imediato |
| Preset referenciado por `preset_default` inexistente no catálogo | Erro explícito; sem fallback silencioso |
| Campos obrigatórios ausentes no preset escolhido | Erro explícito; encerramento imediato |
| Símbolo ou caractere com comprimento diferente de 1, conforme R-6 do contrato | Erro explícito; encerramento imediato |
| Símbolo vazio (string de comprimento zero) | Erro explícito; encerramento imediato |
| Tipo inválido para campo (ex.: não-string onde string é esperada, não-booleano em `caixa_alta`) | Erro explícito; encerramento imediato |
| Identificadores ou nomes duplicados na estrutura materializada, quando a estrutura materializada permita a observação | Erro explícito |

Não há fallback silencioso para preset inexistente. Configuração inválida não produz estilo degradado.

**Nota sobre comprimento de caractere (R-6):** A restrição de "exatamente 1 caractere" vem do contrato R-6 e existe para preservar alinhamento colunar. A ADR não redefine "caractere" como code point, grapheme cluster ou largura visual de terminal; não introduz nova política de largura de terminal. A unidade técnica de medição e o tratamento de casos de borda Unicode são decisões do handoff de implementação. Se a implementação demonstrar que a autoridade contratual vigente é insuficiente ou contraditória, deve ser registrado bloqueio documental antes de avançar.

**Nota sobre duplicidade em catálogo:** Chaves duplicadas no JSON bruto podem ser descartadas pelo parser antes de chegarem à estrutura materializada — dependendo do mecanismo de parse utilizado. A ADR não exige parser raw especial apenas para detectar duplicidade de chaves no JSON bruto. A validação de duplicidade se aplica ao que for observável na estrutura materializada: identificadores ou nomes que permaneçam duplicados nessa estrutura devem ser rejeitados. A unidade e o mecanismo de detecção pertencem ao handoff de implementação.

### D10 — Consumidores

O renderer e demais consumidores devem receber a representação de runtime já resolvida pelo loader. Devem deixar de decidir autonomamente sobre:

- caracteres das bordas;
- preset visual de borda;
- moldura/formato visual compartilhado de chips;
- símbolos globais dos indicadores (`selecionado`, `incluido`, `concluido`).

**Distinção fundamental:**

| Categoria | Origem | Não confundir com |
|---|---|---|
| Configuração global de aparência | `config/estilo.json` via loader | Estado vivo de execução |
| Estado vivo de execução | Produzido e mantido pela execução corrente | Configuração declarativa |
| Declaração comportamental da tela | `tela.json` | Configuração de aparência global |

**Exemplos de estado vivo que não pertencem a `config/estilo.json`:**
- item sob o cursor;
- itens incluídos na seleção;
- tela em foco;
- página atual;
- modo verboso ativo;
- escolha temporária feita por uma futura tela de estilo antes de ser persistida.

### D11 — Edição centralizada

A inclusão de uma nova opção dentro de uma categoria já suportada deve ser possível por edição centralizada de `config/estilo.json`, desde que respeite o schema vigente.

Limites desta garantia:
- Vale para opções dentro de categorias existentes (`borda`, `chip`, `indicadores.selecionado`, `indicadores.incluido`).
- Não implica que toda categoria visual completamente nova seja reconhecida sem implementação — categoria nova exige loader, validação e consumidor correspondentes.

### D12 — Tela futura de escolha de estilo

Registrar como decisão deferida, fora do escopo desta ADR e deste ciclo:

- criação de tela para visualizar e alterar o estilo global aplicado;
- mecanismo de persistência da escolha feita nessa tela;
- pré-visualização antes da confirmação;
- restauração do padrão;
- troca de estilo durante uma sessão;
- necessidade ou não de reinicialização após troca.

Essa tela será tratada somente após o Bloco 1.

### D13 — Blocos funcionais posteriores (fora do escopo desta ADR)

#### Bloco 2 — Navegação e seleção única

- navegação por setas no `console`;
- cursor do `console` (item sob o cursor);
- seleção única pelo item sob o cursor;
- chip `[✥] Navegar`;
- Enter sobre item em foco;
- ação registrada que abre outro `console`;
- conteúdo multinível da tela de destino.

#### Bloco 3 — Seleção múltipla

- seleção múltipla;
- toggle pela barra de espaço;
- chip `[␣] Selecionar`;
- conjunto de itens marcados;
- uso de `incluido_on` e `incluido_off`;
- execução sobre a seleção;
- tela com a lista dos itens selecionados.

Esta ADR apenas prepara a infraestrutura de estilo que esses blocos consumirão. Os valores de `incluido_on` e `incluido_off` serão resolvidos pelo loader, mas o mecanismo de toggle pertence ao Bloco 3.

Esclarecimento preservado para o futuro Bloco 2: esta ADR não redefine a ordem
dos chips. A autoridade continua sendo `contrato_barra_de_menus.md`. Quando
`ordem.politica = "declaracao"`, o renderer preserva a ordem de
`barra_de_menus.chips[]`; a declaração deve respeitar a ordem canônica; âncoras
validam a ordem; e o renderer não reordena automaticamente.

Para uma tela com navegação, Enter, modo verboso e ajuda, a ordem canônica é:

```text
[Esc] → [✥] → [⏎] → [V] → [?]
```

Esse esclarecimento pertence ao futuro Bloco 2 e não amplia o escopo funcional
da ADR-0030.

---

## 6. Tabela das decisões

| Decisão | Assunto | Estado final |
|---|---|---|
| D1 | Autoridade global exclusiva de `config/estilo.json` | Definido |
| D2 | Catálogo + `preset_default` como padrão canônico | Definido |
| D3 | Escopo integral do estilo (todas as seções) | Definido |
| D4 | Preset ativo de borda: `"Borda Curva"` | Definido |
| D5 | Preset ativo de chip: `"Colchete"`; `caixa_alta: false` para preservar capitalização atual dos rótulos | Definido |
| D6 | Preset ativo de cursor: `"Seta"` | Preservado |
| D7 | Preset ativo de inclusão: `"Círculo"` | Preservado |
| D8 | Carregamento único, validação, materialização, disponibilização | Definido |
| D9 | Validações obrigatórias; sem fallback silencioso; unidade de medição e duplicidade raw ao handoff | Definido |
| D10 | Consumidores recebem valores resolvidos; não decidem autonomamente | Definido |
| D11 | Edição centralizada para novas opções em categorias existentes | Definido |
| D12 | Tela de escolha de estilo: deferida | Deferida |
| D13 | Blocos 2 e 3 (navegação, seleção): fora do escopo | Fora do escopo |

---

## 7. Alternativas rejeitadas

### A1 — Manter hardcodings no renderer

**Rejeitada.** O renderer decide autonomamente sobre bordas e chips, violando o contrato de estilo (R-2) e impedindo que a biblioteca persistida em `config/estilo.json` seja efetivamente usada. A manutenção de duas fontes paralelas de verdade é insustentável.

### A2 — Usar `config/estilo.json` apenas como documentação

**Rejeitada.** Um arquivo de configuração que não é lido em runtime é documentação disfarçada de dado. A lacuna entre o contrato de estilo e o runtime atual é o problema central desta ADR.

### A3 — Permitir escolha visual independente por tela neste ciclo

**Rejeitada.** A escolha é global por decisão explícita do usuário. JSONs de tela declaram composição e comportamento; não escolhem aparência. Múltiplas fontes de decisão de estilo introduziriam inconsistência visual e complexidade desnecessária.

### A4 — Carregar somente os indicadores agora

**Rejeitada.** A lacuna de borda e chip é igualmente material. Carregar apenas indicadores deixaria bordas e chips hardcoded, preservando dois dos três problemas identificados. O carregamento integral é mais simples e mais correto.

### A5 — Misturar o Bloco 1 com navegação e seleção

**Rejeitada.** Navegação e seleção dependem de estado vivo de cursor e foco — infraestrutura que não existe no modelo atual. Misturar os blocos criaria uma entrega sem estado final claro. Os blocos são sequencialmente dependentes.

### A6 — Criar imediatamente a tela de escolha de estilo

**Rejeitada.** A tela de escolha depende de estilo carregado e materializado. Criar a tela antes da infraestrutura é inverter a ordem. A tela também exige persistência de escolha — mecanismo não decidido.

### A7 — Aplicar fallback silencioso para preset inválido

**Rejeitada.** Fallback silencioso mascara erros de configuração e produz comportamento inesperado sem diagnóstico. O sistema deve falhar explicitamente e com mensagem clara quando a configuração for inválida.

### A8 — Escolher novos presets visuais durante a migração

**Rejeitada.** A migração altera a origem da configuração, não o resultado visual. Escolher novos presets neste ciclo misturaria uma mudança de infraestrutura com uma mudança de aparência — escopo diferente, decisão diferente.

---

## 8. Consequências

### 8.1 Positivas

- O runtime passará a ter uma única fonte de verdade para aparência: `config/estilo.json` via objeto de estilo resolvido.
- O renderer deixará de ter lógica de decisão sobre bordas, chips e indicadores.
- A inclusão de novo preset em categoria existente passa a ser declarativa.
- Testes que hoje verificam constantes hardcoded passam a verificar comportamento derivado do arquivo de estilo.

### 8.2 Negativas / Riscos

- O loader precisará carregar `config/estilo.json` em todas as sessões — falha no arquivo impede a inicialização.
- Testes existentes que usam `tipo_borda` como parâmetro precisarão ser revisados.
- O parâmetro `tipo_borda` em `renderizar_tela` terá vida útil limitada ao ciclo de migração.

---

## 9. Compatibilidade

### 9.1 Preservação da aparência inicial

A migração preserva a aparência atual:

- O preset "Borda Curva" reproduz exatamente `_BORDAS["curva"]` — correspondência exata nos sete caracteres de borda, verificada no levantamento.
- O preset "Colchete" preserva a aparência vigente dos chips com as seguintes condições:
  - Os delimitadores `[` e `]` correspondem exatamente ao formato `"[{tecla}]"` hardcoded no renderer.
  - `cor_texto: "padrão"` e `cor_fundo: "padrão"` não introduzem nova cor; preservam a aparência atual.
  - `caixa_alta: true` no arquivo atual **não preserva** o visual vigente: o renderer atual não aplica caixa alta, e os textos dos chips ("Sair", "Voltar", "Ajuda", "Verboso") mantêm a capitalização declarada pelas telas. A preservação visual completa exige mudar esse campo para `false` (ver D5 e seção 10.2).

### 9.2 JSONs de tela

JSONs de tela que não declaram aparência não são afetados. A separação entre configuração de aparência (`config/estilo.json`) e declaração de tela (`tela.json`) se mantém.

### 9.3 Parâmetro `tipo_borda`

O parâmetro `tipo_borda` de `renderizar_tela` é um hardcoding de runtime identificado pelo levantamento. Ele deve ser eliminado ao final do ciclo de implementação do Bloco 1. Não haverá coexistência permanente entre `tipo_borda` e a escolha global de borda.

Compatibilidade transitória durante a migração, se necessária para a execução sequencial das mudanças, deve ser explicitamente limitada ao ciclo de implementação. O estado final é: a escolha de borda vem exclusivamente do objeto de estilo resolvido.

### 9.4 Testes existentes

Testes que verificam caracteres de borda esperados com base em `tipo_borda = "curva"` ou `tipo_borda = "reta"` precisarão ser revisados. O handoff de implementação deve incluir atualização dos testes para verificar comportamento derivado do arquivo de estilo, não de constantes hardcoded.

### 9.5 Ausência de fallback silencioso

Nenhum componente pode aplicar estilo parcialmente resolvido. Se a validação do loader falhar, a sessão não é iniciada com valores de fallback.

---

## 10. Migração

A migração tem estado final único: o objeto de estilo resolvido a partir de `config/estilo.json` é a única fonte de aparência para o renderer.

### 10.1 Aplicação documental (a executar em ciclo próprio)

A aplicação documental altera somente documentos normativos (contratos e módulos de nomenclatura). Alterações em `config/estilo.json` são configuração executável e pertencem ao ciclo de implementação (seção 10.2).

1. Atualizar `contrato_estilo.md` para registrar a exigência de `preset_default` em `borda` e `chip` e a materialização integral com todos os cinco campos de chip.
2. Inspecionar `contrato_chip.md` quanto ao consumo integral dos cinco campos do preset de chip; atualizar se o contrato precisar de ajuste para refletir o consumo completo.
3. Inspecionar `contrato_barra_de_menus.md` quanto à origem global da aparência e capitalização dos chips; atualizar se afetado.
4. Inspecionar `contrato_console.md` quanto aos indicadores materializados; atualizar se afetado, sem introduzir navegação ou seleção neste ciclo.

A promoção de `_meta.status` em `config/estilo.json` não pertence a esta aplicação documental. O critério de promoção é deferido (seção 12).

### 10.2 Implementação (a executar em ciclo próprio)

Inclui as alterações em `config/estilo.json` e a implementação do loader e do renderer.

**Alterações em `config/estilo.json`:**

1. Adicionar `preset_default: "Borda Curva"` à seção `borda`.
2. Adicionar `preset_default: "Colchete"` à seção `chip`.
3. Mudar `chip.presets["Colchete"].caixa_alta` de `true` para `false` — necessário para preservar a capitalização atual dos rótulos ("Sair", "Voltar", "Ajuda", "Verboso").

**Implementação:**

4. Implementar loader de estilo: lê `config/estilo.json`, valida, resolve presets, produz objeto de runtime.
5. Implementar as validações definidas em D9.
6. Disponibilizar o objeto de estilo ao renderer e demais consumidores.
7. Remover `_BORDAS` e o parâmetro `tipo_borda` de `renderizar_tela`.
8. Atualizar o renderer para consumir os campos de borda do objeto de estilo.
9. Atualizar o renderer para consumir os cinco campos de chip do objeto de estilo (`caractere_esquerdo`, `caractere_direito`, `caixa_alta`, `cor_texto`, `cor_fundo`).
10. Atualizar testes que verificam constantes hardcoded de borda e chip.

A promoção de `_meta.status` em `config/estilo.json` não está incluída neste ciclo. O critério de promoção é deferido (seção 12).

### 10.3 Política de chamadas que ainda fornecem `tipo_borda`

Durante o ciclo de migração, chamadas a `renderizar_tela` que ainda fornecem `tipo_borda` podem ser toleradas transitoriamente, desde que o handoff de implementação especifique o prazo de eliminação. O estado final não admite `tipo_borda` como parâmetro.

---

## 11. Validações

Ver D9 (seção 5) para a lista completa de validações obrigatórias do loader.

Critérios mínimos de conclusão do Bloco 1:

- [x] `config/estilo.json` contém `preset_default` em `borda` e `chip`.
- [x] `chip.presets["Colchete"].caixa_alta` é `false` após a migração.
- [x] Loader carrega, valida e produz objeto de estilo resolvido a partir de `config/estilo.json`.
- [x] Loader produz erro explícito para cada condição listada em D9, sem fallback silencioso.
- [x] `_BORDAS` foi removido do renderer.
- [x] Parâmetro `tipo_borda` foi removido de `renderizar_tela`.
- [x] Renderer consome caracteres de borda do objeto de estilo.
- [x] Renderer consome os cinco campos de chip do objeto de estilo (`caractere_esquerdo`, `caractere_direito`, `caixa_alta`, `cor_texto`, `cor_fundo`).
- [x] Campos planos `concluido_on`, `concluido_off`, `selecionado_simbolo`, `selecionado_off`, `incluido_on`, `incluido_off` estão disponíveis no objeto de estilo.
- [x] Nenhum símbolo, cor ou caractere de estilo aparece hardcoded no código de produção.
- [x] Testes atualizados verificam comportamento derivado do arquivo de estilo, não constantes hardcoded.
- [x] A aparência visual inicial é preservada (borda curva, chips com colchetes e capitalização original dos rótulos, cursor com seta).
- [x] Suíte canônica: `423 passed`.
- [x] QA técnico: `I1_IMPLEMENTATION_APPROVED`.
- [x] Validação manual: `VALIDACAO_MANUAL_APROVADA`.

---

## 12. Decisões deferidas

| Decisão deferida | Razão |
|---|---|
| Tela de escolha de estilo | Depende do Bloco 1; tem escopo, mecanismo de persistência e pré-visualização próprios |
| Mecanismo de persistência da escolha de estilo | Pertence à tela de escolha; não decidido |
| Restauração de padrão e troca durante sessão | Pertence à tela de escolha; não decidido |
| Necessidade de reinicialização após troca de estilo | Pertence à tela de escolha; não decidido |
| Valores concretos de `cor_inativo` e `cor_alerta` | Não decididos; pendências registradas em `config/estilo.json._meta` |
| Valor concreto de `tiling` | Preferência do usuário não decidida; pendência registrada em `config/estilo.json._meta` |
| Símbolo estático em `tg` para item navegável sem seleção real | Não decidido; depende do Bloco 2 |
| Bloco 2 — navegação e seleção única | ADR, handoff e implementação próprios |
| Bloco 3 — seleção múltipla | ADR, handoff e implementação próprios |
| Conversão de `indicadores.concluido` em catálogo | Não exige conversão agora; mudança exige justificativa própria |
| Promoção de `_meta.status` de `config/estilo.json` | Critério de promoção não definido; pendências de `cor_inativo`, `cor_alerta` e `tiling` ainda registradas no arquivo; a promoção pertence a ciclo futuro com critério explícito |
| Unidade técnica de medição de "1 caractere" (R-6) | Code point, grapheme cluster ou largura visual: escolha técnica do handoff de implementação |
| Mecanismo de detecção de duplicidade raw em JSON | Depende do parser escolhido no handoff; não exige parser especial por esta ADR |

---

## 13. Rastreabilidade

### 13.1 Origem das decisões

| Decisão | Origem | Referência |
|---|---|---|
| D1 | Decisão do usuário | `config/estilo.json` é fonte global e exclusiva da aparência |
| D2 | Decisão do usuário | A escolha é global; novas opções por edição centralizada |
| D3 | Decisão do usuário | Primeira implementação preserva aparência vigente |
| D4 | Decisão do usuário + evidência do levantamento | Preset "Borda Curva" identificado por correspondência exata |
| D5 | Decisão do usuário + evidência do levantamento | Preset "Colchete" para delimitadores (correspondência exata); `caixa_alta: false` por decisão do usuário para preservar capitalização atual |
| D6 | Decisão do usuário | Preservar `preset_default: "Seta"` |
| D7 | Decisão do usuário | Preservar `preset_default: "Círculo"` |
| D8 — carregamento único e disponibilização | Decisão do usuário (cascade de D1) | Fonte global exclusiva implica carregamento único; consumidores recebem objeto resolvido |
| D8 — validação e materialização | Regra contratual preexistente | `contrato_estilo.md` §3.3, R-3: completude do schema; materialização esperada pelo contrato |
| D8 — nome/módulo do loader; não reler por render | Decisão técnica do handoff | Mecanismo concreto não decidido por esta ADR; pertence ao handoff |
| D9 — validações de schema e ausência de fallback | Regra contratual preexistente + decisão do usuário | `contrato_estilo.md` R-3, R-6; ausência de fallback conforme rejeição de A7 |
| D9 — unidade técnica de medição; duplicidade raw | Decisão técnica do handoff | Não decidido pela ADR; pertence ao handoff |
| D10 — proibição de hardcoding; objeto único por sessão | Regra contratual preexistente | `contrato_estilo.md` R-2 (proibição de hardcoding), R-1 (unicidade do objeto de estilo por sessão) |
| D11 | Decisão do usuário | Edição centralizada para novas opções em categorias existentes |
| D12 | Decisão do usuário | Tela futura de escolha é deferida |
| D13 | Decisão do usuário | Blocos 2 e 3 são posteriores e separados |

### 13.2 Separação genealógica

```yaml
decisao_do_usuario:
  - fonte_global_exclusiva          # D1
  - catalogos_com_opcao_ativa       # D2
  - escolha_global                  # D1, D3
  - edicao_centralizada             # D11
  - preservacao_visual              # D3, D4, D5
  - tela_futura_de_estilo           # D12
  - divisao_em_tres_blocos          # D13

regra_contratual_preexistente:
  - campos_de_estilo                # contrato_estilo.md §3.1–§3.5
  - materializacao_dos_indicadores  # contrato_estilo.md §3.3
  - proibicao_de_hardcoding_de_aparencia  # contrato_estilo.md R-2
  - objeto_de_estilo_ativo          # contrato_estilo.md R-1
  - restricao_contratual_de_um_caractere  # contrato_estilo.md R-6

evidencia_do_levantamento:
  - estrutura_real_de_config_estilo   # catálogos sem preset_default em borda/chip
  - ausencia_de_loader                # loader de estilo não confirmado como existente
  - hardcodings_atuais                # _BORDAS, "[{tecla}]", tipo_borda
  - correspondencias_de_presets       # "Borda Curva" ↔ _BORDAS["curva"]; "Colchete" delimitadores

decisao_tecnica_de_handoff:
  - nome_e_local_do_loader            # nome de função/classe/módulo não decidido
  - assinatura_do_objeto_de_runtime   # campos concretos do objeto de runtime
  - estrategia_interna_de_transicao   # tolerância transitória de tipo_borda
  - detalhes_de_integracao            # unidade de medição de caractere; mecanismo de duplicidade raw
```

### 13.3 Evidências materiais

| Evidência | Caminho | Linhas |
|---|---|---|
| Catálogo e `preset_default` de `selecionado` | `config/estilo.json` | 102–110 |
| Catálogo e `preset_default` de `incluido` | `config/estilo.json` | 112–119 |
| Par direto de `concluido` | `config/estilo.json` | 98–100 |
| Catálogo de borda (sem `preset_default`) | `config/estilo.json` | 13–42 |
| Catálogo de chip (sem `preset_default`) | `config/estilo.json` | 44–95 |
| `caixa_alta: true` no preset "Colchete" | `config/estilo.json` | 51 |
| Hardcoding `_BORDAS` no renderer | `tela/renderizador.py` | 153–164 |
| Parâmetro `tipo_borda` em `renderizar_tela` | `tela/renderizador.py` | 2388–2391 |
| Formato `"[{tecla}]"` hardcoded | `tela/renderizador.py` | 1140–1144 |
| Ausência de loader de estilo | `tela/loader.py` | 1093–1155, 1264–1283 |
| Transformação esperada pelo contrato | `docs/contratos/contrato_estilo.md` | 149–174 |

### 13.4 Autoridades consultadas

| Autoridade | Papel nesta ADR |
|---|---|
| `docs/nomenclatura/01_NUCLEO_COMUM.md` | Definições transversais |
| `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | Separação `config/estilo.json` vs estado de runtime |
| `docs/nomenclatura/10_ESTILO.md` | Terminologia de estilo, borda, chip, indicadores |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Chips como entidade declarativa |
| `docs/nomenclatura/32_CONSOLE.md` | Estrutura do item (`ec`, `tg`, `tx`); indicadores |
| `docs/contratos/contrato_estilo.md` | Schema de estilo, transformação de presets, R-1 a R-8 |
| `docs/contratos/contrato_chip.md` | Aparência visual do chip vem do estilo |
| `docs/contratos/contrato_barra_de_menus.md` | `cor_inativo`, `cor_alerta` do schema de estilo |
| `docs/contratos/contrato_console.md` | `ec`, `tg`, indicadores de cursor e seleção |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md` | Evidência do estado material atual |

### 13.5 Separação entre os três blocos

| Bloco | Escopo | ADR |
|---|---|---|
| Bloco 1 (esta ADR) | Carregamento global e materialização do estilo | ADR-0030 |
| Bloco 2 | Navegação e seleção única no `console` | ADR futura |
| Bloco 3 | Seleção múltipla | ADR futura |

---

## 14. Propagação documental

Matriz explícita de documentos afetados e ação esperada em ciclos futuros.
Distingue documentos realmente afetados de autoridades apenas consultadas.

| Arquivo | Classificação | Tratamento futuro |
|---|---|---|
| `docs/contratos/contrato_estilo.md` | ATUALIZAR | Refletir `preset_default` de borda e chip e a materialização integral, incluindo os cinco campos do chip resolvido |
| `docs/contratos/contrato_chip.md` | ATUALIZAR_SE_AFETADO | Atualizar se sua regra de consumo dos cinco campos precisar de ajuste |
| `docs/contratos/contrato_barra_de_menus.md` | INSPECIONAR_E_PRESERVAR | Inspecionar origem global da aparência e capitalização; preservar autoridade sobre ordem canônica |
| `docs/contratos/contrato_console.md` | INSPECIONAR_E_PRESERVAR | Inspecionar indicadores materializados sem introduzir navegação ou seleção nesta ADR |
| `docs/nomenclatura/10_ESTILO.md` | ATUALIZAR_SE_AFETADO | Alterar somente se a terminologia vigente não comportar as decisões desta ADR |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | ATUALIZAR_SE_AFETADO | Alterar somente se a terminologia vigente não comportar origem global da aparência/capitalização |
| `docs/nomenclatura/32_CONSOLE.md` | ATUALIZAR_SE_AFETADO | Alterar somente se a terminologia vigente não comportar indicadores materializados |
| `docs/adr/INDICE_ADR.md` | ATUALIZAR | Atualizar somente depois de parecer favorável do QA, durante a aplicação documental |

`config/estilo.json`, `tela/loader.py`, `tela/renderizador.py` e testes são
artefatos da futura migração de configuração executável/implementação, não da
aplicação documental.

---

## 15. Encerramento

```yaml
status_literal: aceita
aplicacao_documental: CONCLUIDA
qa_da_aplicacao: ADR_APPLICATION_APPROVED
configuracao_executavel_migrada: true
implementacao_Bloco_1_executada: true
QA_tecnico: I1_IMPLEMENTATION_APPROVED
validacao_manual: VALIDACAO_MANUAL_APROVADA
patch_implementacao_necessario: false
Bloco_1_concluido: true
Bloco_2_concluido: false
Bloco_3_concluido: false
consistencia_documental_pos_ciclo:
  estado: PATCH_EXECUTADO_AGUARDANDO_QA
```

DOCUMENTATION_CONSISTENCY_PATCHED_AWAITING_QA
