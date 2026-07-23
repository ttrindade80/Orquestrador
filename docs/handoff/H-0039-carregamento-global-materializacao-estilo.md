---
name: H-0039-carregamento-global-materializacao-estilo
description: Implementa o Bloco 1 da ADR-0030 — carregamento de config/estilo.json como autoridade global exclusiva, materialização de runtime e eliminação dos hardcodings no renderer
metadata:
  type: handoff
  handoff: H-0039
  adr_base: ADR-0030
  bloco: 1
  estado_inicial: BASE_DOCUMENTAL_APROVADA
  estado_final_esperado: HANDOFF_CRIADO_AGUARDANDO_QA
---

# H-0039 — Carregamento global e materialização do estilo

## 1. Identificação

| Campo | Valor |
|---|---|
| Número | H-0039 |
| Título | Carregamento global e materialização do estilo |
| ADR base | ADR-0030 — Carregamento global e materialização do estilo |
| Bloco | 1 de 3 |
| Estado inicial | `BASE_DOCUMENTAL_APROVADA` |
| Estado final esperado | `HANDOFF_CRIADO_AGUARDANDO_QA` |
| Data | 2026-07-22 |

---

## 2. Estado e autoridade

### 2.1 Base documental

A ADR-0030 está `aceita`. A aplicação documental foi concluída e aprovada:

```yaml
adr: ADR-0030-carregamento-global-e-materializacao-do-estilo.md
status_adr: aceita
encerramento_aplicacao: APLICACAO_ADR_CONCLUIDA_AGUARDANDO_QA
qa_aplicacao: ADR_APPLICATION_APPROVED
```

Evidências de aprovação:
- `docs/relatorios/RELATORIO_CORRECAO_ENCERRAMENTO_QA_POS_PATCH_02_ADR-0030.md` → `status_canonico: ADR_APPROVED`
- `docs/relatorios/RELATORIO_CORRECAO_QA_APLICACAO_ADR-0030.md` → `ADR_APPLICATION_APPROVED`

### 2.2 Autoridades consultadas para elaboração deste handoff

| Autoridade | Papel |
|---|---|
| `docs/adr/ADR-0030-carregamento-global-e-materializacao-do-estilo.md` | Fonte primária de todas as decisões D1–D13 |
| `docs/contratos/contrato_estilo.md` | Schema, regras R-1 a R-10, validações D9 |
| `docs/contratos/contrato_chip.md` | Consumo dos cinco campos de chip |
| `docs/contratos/contrato_barra_de_menus.md` | Origem global da aparência dos chips |
| `docs/contratos/contrato_console.md` | Indicadores materializados (fora do escopo de comportamento) |
| `docs/nomenclatura/10_ESTILO.md` | Terminologia de estilo, borda, chip, indicadores, materialização |
| `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md` | Chips como entidades declarativas |
| `docs/nomenclatura/32_CONSOLE.md` | Estrutura do item; indicadores de cursor e seleção |
| `docs/relatorios/RELATORIO_LEVANTAMENTO_ESTILO_INDICADORES_NAVEGACAO_SELECAO.md` | Evidência do estado material atual |
| `docs/relatorios/RELATORIO_APLICACAO_ADR-0030.md` | Confirmação de propagação documental |
| `docs/relatorios/RELATORIO_CORRECAO_QA_APLICACAO_ADR-0030.md` | Aprovação final da base documental |

### 2.3 Artefatos técnicos inspecionados

| Arquivo | Evidência relevante |
|---|---|
| `config/estilo.json` | Estado atual da configuração — confirmado neste handoff |
| `tela/loader.py` | Ausência de loader de estilo; presença de `carregar_tela` |
| `tela/renderizador.py` | `_BORDAS` (153–164), `tipo_borda` (2388–2476), `"[{tecla}]"` (1140–1144) |
| `tela/teste_loader.py` | Suite de testes do loader de tela |
| `tela/teste_renderizador.py` | Testes que usam `tipo_borda` |
| `demo/demo.py` | Estado de execução com `tipo_borda`; chamadas a `renderizar_tela` |
| `demo/teste_demo.py` | Testes do estado de demo que verificam `tipo_borda` |
| `demo/teste_demo_console_modos.py` | Chamadas a `renderizar_tela` com `tipo_borda="curva"` |
| `demo/demo_distribuicao.py` | Chamadas a `renderizar_tela` com `tipo_borda` |
| `demo/diagnostico.py` | Chamada direta a `renderizar_tela` sem `tipo_borda` — consumidor obrigatório identificado pelo QA (QA-H0039-001) |
| `demo/teste_diagnostico.py` | Testes com chamadas diretas a `renderizar_tela` sem `tipo_borda` (linhas 364, 435, 458) — consumidor obrigatório identificado pelo QA |
| `demo/teste_demo_console.py` | Testes com chamadas diretas a `renderizar_tela` sem `tipo_borda` (linhas 199, 210, 221, 233) — consumidor obrigatório identificado pelo QA |

---

## 3. Problema

`config/estilo.json` existe como biblioteca de aparência global, mas nenhum componente ativo a carrega ou usa como autoridade. O estado atual apresenta as seguintes lacunas materialmente confirmadas:

```yaml
loader_de_estilo:                  ausente
materializacao_para_runtime:       ausente
validacao_de_presets:              ausente
consumo_pelo_renderer:             ausente_ou_incompleto

borda:
  preset_default_no_json:          ausente
  escolha_ativa_no_runtime:        hardcoded_via_tipo_borda
  _BORDAS_no_renderer:             presente_em_tela/renderizador.py:153-164
  tipo_borda_como_parametro:       presente_em_renderizar_tela:2390

chip:
  preset_default_no_json:          ausente
  formato_visual_hardcoded:        "[{tecla}]"_em_tela/renderizador.py:1144
  caixa_alta_no_colchete:          true_nao_preserva_aparencia_vigente

indicadores:
  selecionado:
    preset_default:                existente_em_config/estilo.json:104
    materializacao_runtime:        ausente
  incluido:
    preset_default:                existente_em_config/estilo.json:113
    materializacao_runtime:        ausente
  concluido:
    par_direto:                    existente_em_config/estilo.json:98-100
    materializacao_runtime:        ausente
```

O renderer e a demo decidem autonomamente sobre bordas e chips, violando o princípio de autoridade global exclusiva definido pela ADR-0030 D1 e pelo contrato_estilo.md R-2.

---

## 4. Objetivo

Implementar o Bloco 1 da ADR-0030:

```yaml
objetivo:
  - carregar config/estilo.json como autoridade global exclusiva de aparência
  - validar integralmente sua estrutura vigente
  - resolver os presets ativos de todas as categorias com catálogo
  - ler os campos diretos das categorias sem catálogo
  - produzir uma representação de runtime única e plana
  - disponibilizar essa representação ao renderer e demais consumidores
  - eliminar _BORDAS e tipo_borda do renderer
  - eliminar "[{tecla}]" hardcoded do renderer
  - migrar todos os chamadores de renderizar_tela que fornecem tipo_borda
  - preservar a aparência visual inicial
```

Estado final: `config/estilo.json → carregar_estilo() → EstiloResolvido → consumidores`

---

## 5. Estado inicial confirmado

### 5.1 `config/estilo.json`

Confirmado por inspeção direta do arquivo:

```yaml
_meta:
  status: "rascunho_inicial"
  pendencias:
    - cor_inativo e cor_alerta sem valores concretos
    - tiling sem preset decidido

borda:
  catalogo_presets: existente
  presets_disponiveis: ["Borda Curva", "Borda Reta", "Linha"]
  preset_default: AUSENTE

chip:
  catalogo_presets: existente
  presets_disponiveis: ["Colchete", "Curva", "Ornamental", "Traço", "Ponto", "Destaque Texto", "Destaque Fundo"]
  preset_default: AUSENTE
  "Colchete":
    caractere_esquerdo: "["
    caractere_direito: "]"
    cor_texto: "padrão"
    cor_fundo: "padrão"
    caixa_alta: true  # precisa ser false para preservar aparência vigente

indicadores:
  concluido:
    estrutura: par_direto_on_off
    on: "✓"
    off: " "
  selecionado:
    preset_default: "Seta"
    off: " "
    presets:
      Seta: {simbolo: "→"}
      Mão: {simbolo: "☛"}
      Alvo: {simbolo: "◎"}
      Ponta: {simbolo: "➤"}
  incluido:
    preset_default: "Círculo"
    presets:
      Círculo: {on: "●", off: "○"}
      Quadrado: {on: "■", off: "□"}
      Estrela: {on: "★", off: "☆"}
      Check: {on: "✔", off: "✕"}
```

### 5.2 Loader (`tela/loader.py`)

- `carregar_tela` (linhas 1093–1155) existe e carrega JSONs de tela.
- Loader de `config/estilo.json`: **ausente**.
- Nenhuma materialização de campos planos de indicadores confirmada.

### 5.3 Renderer (`tela/renderizador.py`)

| Elemento | Localização | Estado |
|---|---|---|
| `_BORDAS` | linhas 153–164 | hardcoded com "curva" e "reta" |
| `tipo_borda` como parâmetro | linha 2390 | `tipo_borda: str = "curva"` |
| `borda = _BORDAS[tipo_borda]` | linha 2476 | resolve borda hardcoded |
| `"[{tecla}]"` | linha 1144 | formato de chip hardcoded em `_texto_chip_barra` |

### 5.4 Chamadores de `renderizar_tela`

Confirmado por inspeção e auditoria QA (QA-H0039-001):

**Chamadores com `tipo_borda` (inspeção inicial):**

| Arquivo | Ocorrências relevantes |
|---|---|
| `tela/teste_renderizador.py` | `tipo_borda="curva"`, `tipo_borda="reta"`, teste de tipo_borda inválido |
| `demo/demo.py` | Estado `"tipo_borda": "curva"` + "b" alterna curva↔reta |
| `demo/teste_demo.py` | Verifica `estado["tipo_borda"]`; testa alternância "b" |
| `demo/teste_demo_console_modos.py` | `tipo_borda="curva"` em chamadas a `renderizar_tela` |
| `demo/demo_distribuicao.py` | `tipo_borda` no estado + chamadas a `renderizar_tela` |

**Chamadores sem `tipo_borda` — omitidos na lista nominal original (QA-H0039-001):**

| Arquivo | Ocorrências relevantes |
|---|---|
| `demo/diagnostico.py` | `renderizar_tela(modelo)` sem `tipo_borda` — quebrará com assinatura final |
| `demo/teste_diagnostico.py` | `renderizar_tela(... largura/altura)` nas linhas 364, 435, 458 sem `tipo_borda` |
| `demo/teste_demo_console.py` | `renderizar_tela(... largura/altura)` nas linhas 199, 210, 221, 233 sem `tipo_borda` |

Todos os chamadores acima exigem migração dentro do H-0039 para fornecer `estilo: EstiloResolvido` conforme a assinatura final.

### 5.5 Suite canônica

```yaml
comando: PYTHONDONTWRITEBYTECODE=1 python -m pytest
baseline: 422 passed
```

---

## 6. Decisões técnicas do handoff

A ADR-0030 D8 delega ao handoff as seguintes decisões. Este handoff as registra de forma mínima, justificada e testável.

### 6.1 Função de carregamento: `carregar_estilo`

**Decisão**: a função se chama `carregar_estilo` e reside em `tela/loader.py`.

**Justificativa**: o mesmo módulo já contém `carregar_tela`; manter o loader de configurações concentrado evita dispersão de responsabilidade sem criar abstração desnecessária.

**Assinatura**:

```python
def carregar_estilo(caminho_base: Path | None = None) -> "EstiloResolvido":
```

`caminho_base` segue a convenção de `carregar_tela`: quando `None`, usa a raiz do repositório derivada de `Path(__file__).resolve().parent.parent`.

### 6.2 Representação de runtime: `EstiloResolvido`

**Decisão**: `dataclass(frozen=True)` chamado `EstiloResolvido`, definido em `tela/loader.py`.

**Justificativa**: `frozen=True` impede alteração acidental em runtime (R-4 do contrato); a definição no loader mantém coesão; não requer módulo novo.

**Assinatura completa**:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EstiloResolvido:
    # Borda — 7 campos
    canto_superior_esquerdo: str
    canto_superior_direito: str
    canto_inferior_esquerdo: str
    canto_inferior_direito: str
    traco_superior: str
    traco_inferior: str
    lateral: str
    # Chip — 5 campos
    caractere_esquerdo: str
    caractere_direito: str
    cor_texto: str
    caixa_alta: bool
    cor_fundo: str
    # Indicadores — 6 campos
    concluido_on: str
    concluido_off: str
    selecionado_simbolo: str
    selecionado_off: str
    incluido_on: str
    incluido_off: str
```

Nenhum campo pode ser omitido. A configuração parcialmente resolvida não pode produzir instância de `EstiloResolvido`.

### 6.3 Propagação: parâmetro `estilo` em `renderizar_tela`

**Decisão**: `renderizar_tela` recebe `estilo: EstiloResolvido` em lugar de `tipo_borda: str`.

**Justificativa**: a borda deixa de ser escolha do renderer e passa a ser dado de entrada — o mesmo padrão já aplicado ao `modelo`. Não exige módulo de injeção de dependência.

**Assinatura após migração**:

```python
def renderizar_tela(
    modelo: ModeloTela,
    estilo: EstiloResolvido,
    largura: int | None = None,
    altura: int | None = None,
    verboso: bool = False,
) -> str:
```

O parâmetro `tipo_borda` é removido do estado final. Não existe compatibilidade permanente com chamadas que ainda forneçam `tipo_borda`.

### 6.4 Estratégia de inicialização

**Decisão**: o ponto de entrada (`demo/demo.py`) chama `carregar_estilo()` uma vez antes do loop de renderização e armazena o resultado no estado da sessão.

**Justificativa**: ADR-0030 D8 exige carregamento único por sessão. O ponto de entrada é o local natural para inicialização antes do primeiro render.

### 6.5 Remoção da alternância de borda no demo

**Decisão**: o comando "b" de alternância curva↔reta em `demo/demo.py` e `demo/demo_distribuicao.py` é removido.

**Justificativa**: a alternância usava `tipo_borda` como parâmetro de runtime — mecanismo incompatível com a autoridade global de `config/estilo.json`. A borda agora vem do arquivo de configuração e não é alternável em runtime por este mecanismo. A futura troca de estilo em tempo de execução pertence ao Bloco 1 → tela de escolha de estilo (D12, fora do escopo desta ADR).

### 6.6 Unidade de medição de "1 caractere" (R-6)

**Decisão**: usar `len(s) == 1` (code points Unicode Python) para a validação de caractere único.

**Justificativa**: consistente com o restante do código do projeto; os presets vigentes de `config/estilo.json` usam caracteres de um único code point; a detecção de grapheme clusters exigiria dependência externa não presente no projeto. A ADR-0030 D9 nota explicitamente que esta unidade técnica pertence ao handoff.

**Limite declarado**: `len()` mede code points, não largura visual de terminal (wcwidth). Um caractere de largura visual 2 (full-width CJK) passaria na validação mas quebraria o alinhamento colunar. Os presets vigentes não contêm esses caracteres. Se presets futuros os incluírem, a regra de validação precisará de revisão própria.

### 6.7 Detecção de duplicidade em catálogo JSON

**Decisão**: não implementar detecção de chaves duplicadas no JSON bruto. A validação de duplicidade aplica-se apenas à estrutura materializada.

**Justificativa**: `json.loads()` da biblioteca padrão do Python silencia chaves duplicadas (mantém a última). Detectar duplicidade no JSON bruto exigiria parser customizado não justificado por esta ADR. Conforme ADR-0030 D9, a validação de duplicidade aplica-se ao que for observável na estrutura materializada — e Python `dict` não admite chaves duplicadas, tornando a duplicidade impossível na estrutura resolvida.

---

## 7. Escopo obrigatório

### 7.1 Configuração executável (`config/estilo.json`)

Alterar apenas:

1. Adicionar `"preset_default": "Borda Curva"` à seção `borda`.
2. Adicionar `"preset_default": "Colchete"` à seção `chip`.
3. Mudar `chip.presets["Colchete"].caixa_alta` de `true` para `false`.

Preservar integralmente:

- `chip.presets["Colchete"].caractere_esquerdo: "["`
- `chip.presets["Colchete"].caractere_direito: "]"`
- `chip.presets["Colchete"].cor_texto: "padrão"`
- `chip.presets["Colchete"].cor_fundo: "padrão"`
- `indicadores.selecionado.preset_default: "Seta"`
- `indicadores.incluido.preset_default: "Círculo"`
- `indicadores.concluido.on: "✓"`
- `indicadores.concluido.off: " "`
- `_meta.status: "rascunho_inicial"` — não promover

Não inventar valores para `cor_inativo`, `cor_alerta` ou `tiling`.

### 7.2 Carregamento e materialização (`tela/loader.py`)

Implementar `carregar_estilo` que:

1. Lê `config/estilo.json` (caminho derivado de `caminho_base` ou raiz do repositório).
2. Valida a estrutura: seções obrigatórias, tipos, integridade dos catálogos.
3. Resolve `preset_default` nas categorias `borda`, `chip`, `indicadores.selecionado`, `indicadores.incluido`.
4. Lê campos diretos de `indicadores.concluido` e `indicadores.selecionado.off`.
5. Valida todos os campos de runtime obrigatórios (presença, tipo, comprimento).
6. Produz `EstiloResolvido` como representação única de runtime.
7. Retorna `EstiloResolvido` para o chamador.
8. Não relê `config/estilo.json` a cada chamada de renderização.
9. Não armazena estado vivo de cursor, foco, seleção ou navegação.

### 7.3 Migração do renderer (`tela/renderizador.py`)

Remover do código de produção:

- `_BORDAS` (dicionário hardcoded, linhas 153–164)
- parâmetro `tipo_borda` de `renderizar_tela` (linha 2390)
- uso de `_BORDAS[tipo_borda]` (linha 2476)
- formato `"[{tecla}]"` hardcoded em `_texto_chip_barra` (linha 1144)

Atualizar para consumir do `EstiloResolvido`:

- os sete campos de borda: `canto_superior_esquerdo`, `canto_superior_direito`, `canto_inferior_esquerdo`, `canto_inferior_direito`, `traco_superior`, `traco_inferior`, `lateral`
- os cinco campos de chip: `caractere_esquerdo`, `caractere_direito`, `cor_texto`, `caixa_alta`, `cor_fundo`
- os seis campos de indicadores materializados quando aplicáveis aos caminhos já existentes de renderização

O renderer não deve:

- abrir `config/estilo.json`;
- escolher preset;
- manter catálogo próprio;
- aplicar fallback visual autônomo;
- definir nova política de navegação ou seleção.

### 7.4 Migração dos chamadores (`demo/` e `tela/`)

Cada arquivo que chama `renderizar_tela` deve ser atualizado dentro deste handoff para fornecer `estilo: EstiloResolvido`. A migração integral cobre dois grupos:

**Chamadores com `tipo_borda` (necessidade confirmada na inspeção inicial):**

| Arquivo | Mudança requerida |
|---|---|
| `demo/demo.py` | Carregar `EstiloResolvido` antes do loop; remover estado `tipo_borda`; remover comando "b"; passar `estilo=estilo` a `renderizar_tela` |
| `demo/teste_demo.py` | Atualizar testes que verificam `tipo_borda` no estado; remover testes da alternância "b" |
| `demo/teste_demo_console_modos.py` | Substituir `tipo_borda="curva"` por `estilo=<estilo_carregado>` em todas as chamadas |
| `demo/demo_distribuicao.py` | Remover estado `tipo_borda`; remover comando "b"; usar `estilo` nas chamadas |

**Chamadores sem `tipo_borda` (necessidade confirmada pelo QA — QA-H0039-001):**

| Arquivo | Mudança requerida |
|---|---|
| `demo/diagnostico.py` | Carregar ou receber `EstiloResolvido`; passar `estilo` como argumento obrigatório a `renderizar_tela` |
| `demo/teste_diagnostico.py` | Adaptar chamadas a `renderizar_tela` nas linhas 364, 435, 458 para passar `estilo`; verificar que os testes continuam passando após a mudança de assinatura |
| `demo/teste_demo_console.py` | Adaptar chamadas a `renderizar_tela` nas linhas 199, 210, 221, 233 para passar `estilo`; verificar que os testes continuam passando após a migração |

O estado final não admite nenhuma chamada ativa a `renderizar_tela` sem o argumento `estilo`. Uma busca global posterior deve confirmar zero consumidores incompatíveis.

### 7.5 Relatório de implementação

Criar:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
```

Conteúdo exigido: ver Seção 19.

---

## 8. Fora do escopo

O executor não pode implementar nenhum dos itens abaixo neste handoff:

```yaml
excluido_nominalmente:
  - navegação por setas
  - cursor móvel entre itens
  - seleção única
  - seleção múltipla
  - toggle com espaço
  - ação por Enter
  - registry de ações
  - abertura de outro console por ação
  - chips [✥], [⏎] e [␣] como novos comportamentos
  - reordenação de chips
  - tela de escolha de estilo
  - persistência de escolhas feitas em tela
  - troca de estilo durante a sessão
  - alteração de _meta.status em config/estilo.json
  - definição de valores concretos para cor_inativo
  - definição de valores concretos para cor_alerta
  - definição de valor para tiling
  - Bloco 2 (navegação e seleção única)
  - Bloco 3 (seleção múltipla)
  - refatorações não necessárias ao carregamento do estilo
```

A presença dos campos `selecionado_simbolo`, `incluido_on`, `incluido_off` no `EstiloResolvido` não autoriza implementar os comportamentos que os consumirão futuramente.

---

## 9. Fluxo de carregamento

```
config/estilo.json
  │
  ▼
carregar_estilo(caminho_base)
  ├── 1. abrir e parsear JSON
  ├── 2. validar seções obrigatórias (borda, chip, indicadores)
  ├── 3. validar preset_default em borda, chip, selecionado, incluido
  ├── 4. validar catálogos não vazios
  ├── 5. resolver preset_default → extrair campos do preset ativo
  ├── 6. ler campos diretos de concluido e selecionado.off
  ├── 7. validar tipos, presença e comprimento de todos os campos
  └── 8. construir e retornar EstiloResolvido
           │
           ▼
       EstiloResolvido (frozen dataclass, 18 campos planos)
           │
           ├── renderizar_tela(modelo, estilo, ...)
           └── (consumidores futuros dos Blocos 2 e 3)
```

`carregar_estilo` não é chamada em cada render. O `EstiloResolvido` não armazena estado vivo de execução.

---

## 10. Representação de runtime

### 10.1 Assinatura de `EstiloResolvido`

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class EstiloResolvido:
    # Borda (7 campos obrigatórios — contrato_estilo.md §3.1)
    canto_superior_esquerdo: str
    canto_superior_direito: str
    canto_inferior_esquerdo: str
    canto_inferior_direito: str
    traco_superior: str
    traco_inferior: str
    lateral: str
    # Chip (5 campos obrigatórios — contrato_estilo.md §3.2)
    caractere_esquerdo: str
    caractere_direito: str
    cor_texto: str
    caixa_alta: bool
    cor_fundo: str
    # Indicadores (6 campos obrigatórios — contrato_estilo.md §3.3)
    concluido_on: str
    concluido_off: str
    selecionado_simbolo: str
    selecionado_off: str
    incluido_on: str
    incluido_off: str
```

### 10.2 Mapeamento de seções de `config/estilo.json` para campos de runtime

| Seção JSON | Tratamento | Campos produzidos |
|---|---|---|
| `borda.presets[borda.preset_default]` | Resolve preset → extrai 7 campos | `canto_superior_esquerdo`, `canto_superior_direito`, `canto_inferior_esquerdo`, `canto_inferior_direito`, `traco_superior`, `traco_inferior`, `lateral` |
| `chip.presets[chip.preset_default]` | Resolve preset → extrai 5 campos | `caractere_esquerdo`, `caractere_direito`, `cor_texto`, `caixa_alta`, `cor_fundo` |
| `indicadores.concluido` | Lê `on` e `off` diretamente | `concluido_on`, `concluido_off` |
| `indicadores.selecionado.presets[preset_default]` | Resolve preset → extrai `simbolo` | `selecionado_simbolo` |
| `indicadores.selecionado.off` | Lê diretamente | `selecionado_off` |
| `indicadores.incluido.presets[preset_default]` | Resolve preset → extrai `on` e `off` | `incluido_on`, `incluido_off` |

### 10.3 Valores esperados após a configuração

Com a configuração corrigida conforme Seção 7.1:

```yaml
EstiloResolvido_esperado:
  # Borda "Borda Curva"
  canto_superior_esquerdo: "╭"
  canto_superior_direito: "╮"
  canto_inferior_esquerdo: "╰"
  canto_inferior_direito: "╯"
  traco_superior: "─"
  traco_inferior: "─"
  lateral: "│"
  # Chip "Colchete" com caixa_alta: false
  caractere_esquerdo: "["
  caractere_direito: "]"
  cor_texto: "padrão"
  caixa_alta: false
  cor_fundo: "padrão"
  # Indicadores
  concluido_on: "✓"
  concluido_off: " "
  selecionado_simbolo: "→"
  selecionado_off: " "
  incluido_on: "●"
  incluido_off: "○"
```

---

## 11. Validações

O loader deve produzir erro explícito e impedir o uso de `EstiloResolvido` parcialmente resolvido em todas as condições abaixo. Não existe fallback silencioso.

### 11.1 Tabela completa de condições de erro

| # | Condição | Tipo de erro esperado |
|---|---|---|
| V-01 | Arquivo `config/estilo.json` ausente | `EstiloErro` (ou equivalente) — encerramento imediato |
| V-02 | Conteúdo do arquivo não é JSON válido | `EstiloErro` — encerramento imediato |
| V-03 | Seção `borda` ausente no JSON | `EstiloErro` — seção obrigatória |
| V-04 | Seção `chip` ausente no JSON | `EstiloErro` — seção obrigatória |
| V-05 | Seção `indicadores` ausente no JSON | `EstiloErro` — seção obrigatória |
| V-06 | `borda.preset_default` ausente | `EstiloErro` — sem fallback |
| V-07 | `chip.preset_default` ausente | `EstiloErro` — sem fallback |
| V-08 | `indicadores.selecionado.preset_default` ausente | `EstiloErro` — sem fallback |
| V-09 | `indicadores.incluido.preset_default` ausente | `EstiloErro` — sem fallback |
| V-10 | `borda.presets` vazio ou ausente | `EstiloErro` — catálogo obrigatório |
| V-11 | `chip.presets` vazio ou ausente | `EstiloErro` — catálogo obrigatório |
| V-12 | `indicadores.selecionado.presets` vazio ou ausente | `EstiloErro` — catálogo obrigatório |
| V-13 | `indicadores.incluido.presets` vazio ou ausente | `EstiloErro` — catálogo obrigatório |
| V-14 | `borda.preset_default` referencia preset inexistente no catálogo | `EstiloErro` — sem fallback para outro preset |
| V-15 | `chip.preset_default` referencia preset inexistente no catálogo | `EstiloErro` — sem fallback |
| V-16 | `indicadores.selecionado.preset_default` referencia preset inexistente | `EstiloErro` — sem fallback |
| V-17 | `indicadores.incluido.preset_default` referencia preset inexistente | `EstiloErro` — sem fallback |
| V-18 | Campo obrigatório ausente no preset ativo de borda | `EstiloErro` — campo faltando |
| V-19 | Campo obrigatório ausente no preset ativo de chip | `EstiloErro` — campo faltando |
| V-20 | `simbolo` ausente no preset ativo de `selecionado` | `EstiloErro` — campo faltando |
| V-21 | `on` ou `off` ausentes no preset ativo de `incluido` | `EstiloErro` — campo faltando |
| V-22 | `on` ou `off` ausentes em `indicadores.concluido` | `EstiloErro` — campo faltando |
| V-23 | `off` ausente em `indicadores.selecionado` | `EstiloErro` — campo faltando |
| V-24 | Campo de caractere de borda não é string | `EstiloErro` — tipo inválido |
| V-25 | Campo `caixa_alta` não é booleano | `EstiloErro` — tipo inválido |
| V-26 | Campo `cor_texto` ou `cor_fundo` não é string | `EstiloErro` — tipo inválido |
| V-27 | Campo de símbolo/caractere com `len() != 1` (code point) | `EstiloErro` — viola R-6 |
| V-28 | Campo de símbolo/caractere é string vazia (`""`) | `EstiloErro` — string vazia |
| V-29 | Configuração parcialmente resolvida (qualquer campo de runtime ausente) | `EstiloErro` — não produz `EstiloResolvido` |

Os erros devem ser levantados como exceção Python de tipo específico (`EstiloErro` ou subclasse). O tipo de exceção deve ser importável de `tela.loader`.

### 11.2 Limite da validação de duplicidade JSON

`json.loads()` da biblioteca padrão silencia chaves duplicadas no JSON bruto. A implementação **não** precisa detectar duplicidade no JSON bruto. A duplicidade na estrutura materializada é impossível em Python `dict` e, portanto, não requer validação adicional. Este limite deve ser registrado no relatório de implementação.

---

## 12. Migração do renderer

### 12.1 O que remover

| Elemento | Localização | Ação |
|---|---|---|
| `_BORDAS` | `tela/renderizador.py:153-164` | Remover |
| `tipo_borda: str = "curva"` | `tela/renderizador.py:2390` | Remover — substituir por `estilo: EstiloResolvido` |
| `if tipo_borda not in _BORDAS:` | `tela/renderizador.py:2457-2462` | Remover |
| `borda = _BORDAS[tipo_borda]` | `tela/renderizador.py:2476` | Remover |
| `"[{tecla}]"` em `_texto_chip_barra` | `tela/renderizador.py:1144` | Substituir pelo consumo do estilo |

### 12.2 O que consumir do `EstiloResolvido`

**Borda**: nos caminhos onde `borda["tl"]`, `borda["tr"]`, etc. eram usados, substituir pelos campos correspondentes do `EstiloResolvido`:

| Chave antiga em `_BORDAS` | Campo do `EstiloResolvido` |
|---|---|
| `borda["tl"]` | `estilo.canto_superior_esquerdo` |
| `borda["tr"]` | `estilo.canto_superior_direito` |
| `borda["bl"]` | `estilo.canto_inferior_esquerdo` |
| `borda["br"]` | `estilo.canto_inferior_direito` |
| `borda["h"]` (superior) | `estilo.traco_superior` |
| `borda["h"]` (inferior) | `estilo.traco_inferior` |
| `borda["v"]` | `estilo.lateral` |

**Chip**: `_texto_chip_barra` deve consumir:

- `estilo.caractere_esquerdo` e `estilo.caractere_direito` em vez de `"["` e `"]"` literais
- `estilo.caixa_alta` para decidir se aplica `.upper()` ao texto do chip
- `estilo.cor_texto` e `estilo.cor_fundo` para aplicar cores (quando o renderer implementar tradução de nome semântico para ANSI — se não implementado neste ciclo, preservar como `"padrão"` sem transformação)

**Indicadores**: os caminhos existentes de renderização que já exibem indicadores de cursor/seleção devem consumir os campos correspondentes do `EstiloResolvido`. Se tais caminhos ainda não existem no renderer (estado atual: campos não renderizados), basta disponibilizar os campos via `EstiloResolvido` sem criar comportamento novo.

### 12.3 Compatibilidade transitória

Durante a edição sequencial dos arquivos, chamadas a `renderizar_tela` com `tipo_borda` podem existir temporariamente. O estado final não admite nenhuma chamada com `tipo_borda`. Todos os chamadores devem ser migrados dentro deste handoff.

---

## 13. Compatibilidade

### 13.1 Preservação da aparência visual

O preset "Borda Curva" reproduz exatamente `_BORDAS["curva"]` — correspondência verificada no levantamento (ADR-0030, seção 3.2). O preset "Colchete" com `caixa_alta: false` preserva:

- delimitadores `[` e `]` — correspondência exata com `"[{tecla}]"`
- capitalização dos rótulos como declarada pelas telas ("Sair", "Voltar", "Ajuda", "Verboso")
- cores: `"padrão"` sem alteração visual

```yaml
preservacao_visual_inicial:
  borda: "Borda Curva" → caracteres ╭╮╰╯─│ preservados
  chip:
    delimitadores: [ e ] preservados
    caixa_alta: false → capitalização atual dos rótulos preservada
    cores: "padrão" → sem nova cor introduzida
  cursor: preset "Seta" → símbolo "→" preservado
  inclusao: preset "Círculo" → símbolos "●"/"○" preservados
```

### 13.2 Telas existentes

JSONs de tela que não declaram aparência não são afetados. `carregar_tela` não é alterado.

### 13.3 Ordem e conteúdo dos chips

A ordem dos chips na `barra_de_menus` não muda. O renderer continua percorrendo `chips[]` conforme declarado no `tela.json`. O conteúdo dos chips não muda.

### 13.4 Ausência de navegação e seleção

Este handoff não introduz navegação por setas, cursor móvel, seleção única, seleção múltipla, toggle por espaço, nem qualquer comportamento de interação novo.

### 13.5 Remoção do comando "b" no demo

O comando "b" que alternava borda curva↔reta em `demo/demo.py` e `demo/demo_distribuicao.py` é removido. O estado da sessão de demo deixa de conter `tipo_borda`. Esta remoção é regressão intencional e necessária para o estado final.

Os testes de `demo/teste_demo.py` que verificam a alternância "b" devem ser removidos ou adaptados.

---

## 14. Lista nominal de arquivos autorizados

O executor somente pode alterar os arquivos abaixo. Qualquer arquivo fora desta lista requer parada e autorização explícita do usuário.

### 14.1 Núcleo mínimo

| Arquivo | Razão |
|---|---|
| `config/estilo.json` | Adicionar `preset_default` em borda e chip; corrigir `caixa_alta` em "Colchete" |
| `tela/loader.py` | Implementar `EstiloResolvido` e `carregar_estilo` |
| `tela/renderizador.py` | Remover `_BORDAS`, `tipo_borda`; adicionar parâmetro `estilo`; consumir campos do estilo |
| `tela/teste_loader.py` | Adicionar testes de `carregar_estilo` e `EstiloResolvido` |
| `tela/teste_renderizador.py` | Atualizar testes para usar `estilo` em vez de `tipo_borda`; remover testes de `tipo_borda` inválido; adicionar testes de consumo do estilo |

### 14.2 Arquivos de demonstração — consumidores obrigatórios

Incluídos porque a inspeção inicial ou a auditoria QA (QA-H0039-001) confirmou chamadas diretas a `renderizar_tela` que devem ser migradas dentro do H-0039. A necessidade de todos os arquivos abaixo foi materialmente verificada; nenhum é condicional.

**Consumidores com `tipo_borda` (inspeção inicial):**

| Arquivo | Necessidade | Símbolo ou fluxo afetado | Motivo de não ser possível concluir sem ele |
|---|---|---|---|
| `demo/demo.py` | Estado `tipo_borda`; chamada `renderizar_tela(modelo, tipo_borda=...)` | `processar_comando`, `renderizar_estado`, loop principal | `renderizar_tela` deixa de aceitar `tipo_borda`; demo quebraria na chamada |
| `demo/teste_demo.py` | Testes de `tipo_borda` no estado de `demo.py` | `processar_comando` testes de "b", "s" | Testes falhariam após remoção do campo `tipo_borda` do estado |
| `demo/teste_demo_console_modos.py` | Chamadas `renderizar_tela(m, tipo_borda="curva", ...)` | Cenários 1–4 | Falhariam com `TypeError` após remoção de `tipo_borda` |
| `demo/demo_distribuicao.py` | Estado `tipo_borda` + chamadas `renderizar_tela` | Loop principal de distribuição | Quebraria após remoção de `tipo_borda` |

**Consumidores sem `tipo_borda` — adicionados pelo patch QA-H0039-001:**

```yaml
arquivo: demo/diagnostico.py
necessidade: chamada direta de renderizar_tela sem estilo resolvido
simbolo_ou_fluxo_afetado: fluxo de diagnóstico e renderização do modelo
motivo_de_nao_ser_possivel_concluir_sem_ele: >
  A assinatura final exige estilo resolvido; a chamada atual quebraria ou
  permaneceria fora da migração integral.
classificacao: AUTORIZADO_E_OBRIGATORIO
```

```yaml
arquivo: demo/teste_diagnostico.py
necessidade: testes com chamadas diretas de renderizar_tela
simbolo_ou_fluxo_afetado: cenários de renderização do diagnóstico
motivo_de_nao_ser_possivel_concluir_sem_ele: >
  Os testes precisam fornecer o estilo resolvido e validar o comportamento
  após a mudança de assinatura.
classificacao: AUTORIZADO_E_OBRIGATORIO
```

```yaml
arquivo: demo/teste_demo_console.py
necessidade: testes com chamadas diretas de renderizar_tela
simbolo_ou_fluxo_afetado: cenários de console e dimensões de renderização
motivo_de_nao_ser_possivel_concluir_sem_ele: >
  As chamadas atuais não fornecerão o novo argumento obrigatório e quebrarão
  após a migração.
classificacao: AUTORIZADO_E_OBRIGATORIO
```

### 14.3 Relatório de implementação

| Arquivo | Razão |
|---|---|
| `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md` | Artefato obrigatório do processo |

---

## 15. Testes

### 15.1 Novos testes em `tela/teste_loader.py`

**Positivos — materialização:**

- `carregar_estilo()` retorna instância de `EstiloResolvido`
- todos os 18 campos estão presentes e não são `None`
- `canto_superior_esquerdo == "╭"` (preset "Borda Curva" ativo)
- `caractere_esquerdo == "["` e `caractere_direito == "]"` (preset "Colchete" ativo)
- `caixa_alta == False` (após correção de `config/estilo.json`)
- `selecionado_simbolo == "→"` (preset "Seta" ativo)
- `selecionado_off == " "` (campo direto)
- `incluido_on == "●"` e `incluido_off == "○"` (preset "Círculo" ativo)
- `concluido_on == "✓"` e `concluido_off == " "` (par direto)

**Negativos — cada condição de erro (V-01 a V-29):**

- V-01: arquivo ausente → levanta `EstiloErro`
- V-02: JSON inválido → levanta `EstiloErro`
- V-03 a V-05: seção obrigatória ausente → levanta `EstiloErro`
- V-06 a V-09: `preset_default` ausente em categoria com catálogo → levanta `EstiloErro`
- V-10 a V-13: catálogo vazio → levanta `EstiloErro`
- V-14 a V-17: preset referenciado inexistente → levanta `EstiloErro`; **sem fallback silencioso**
- V-18 a V-23: campo obrigatório ausente no preset ativo → levanta `EstiloErro`
- V-24 a V-26: tipo inválido → levanta `EstiloErro`
- V-27: `len(caractere) != 1` → levanta `EstiloErro`
- V-28: string vazia → levanta `EstiloErro`
- V-29: configuração parcialmente resolvida → não produz `EstiloResolvido`

**Prova de ausência de fallback silencioso:**

- Para cada condição V-14 a V-17, verificar que `EstiloErro` é levantado E que nenhum `EstiloResolvido` foi produzido (não apenas que o erro foi capturável).

### 15.2 Testes atualizados em `tela/teste_renderizador.py`

- Remover todos os testes de `tipo_borda="curva"` e `tipo_borda="reta"`.
- Remover testes de `tipo_borda` inválido (e.g., `tipo_borda="invalida"`, `tipo_borda="CURVA"`).
- Adicionar testes com `estilo=EstiloResolvido(...)` explícito nos casos de renderização.
- Provar que o renderer não contém `_BORDAS` (inspeção de fonte ou teste de ausência de atributo).
- Provar que o renderer não aceita mais `tipo_borda` (chamada com `tipo_borda` deve levantar `TypeError`).
- Provar que borda vem do `EstiloResolvido`: substituir campo de borda por valor alternativo e verificar que a saída muda.
- Provar que chip vem do `EstiloResolvido`: substituir `caractere_esquerdo` e verificar que a saída muda.
- Provar que `caixa_alta=False` preserva capitalização original dos rótulos.
- Provar que `caixa_alta=True` aplica maiúsculas.
- Verificar regressão das telas existentes: `demo.json`, `destino_minimo.json` com o estilo real carregado.

### 15.3 Adaptações em `demo/diagnostico.py`, `demo/teste_diagnostico.py` e `demo/teste_demo_console.py`

Os três arquivos identificados pelo QA (QA-H0039-001) devem ser adaptados para fornecer `estilo: EstiloResolvido` à nova assinatura de `renderizar_tela`:

- `demo/diagnostico.py`: adaptar chamada a `renderizar_tela` para carregar ou receber e passar `estilo`.
- `demo/teste_diagnostico.py`: adaptar chamadas nas linhas 364, 435, 458 para incluir `estilo` obrigatório; confirmar que os testes continuam passando após a adaptação.
- `demo/teste_demo_console.py`: adaptar chamadas nas linhas 199, 210, 221, 233 para incluir `estilo` obrigatório; confirmar que os testes continuam passando após a adaptação.

Nenhuma chamada ativa a `renderizar_tela` pode permanecer incompatível com a assinatura final ao término da implementação.

### 15.4 Suite focal

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py tela/teste_renderizador.py -v
```

### 15.5 Suite canônica

```bash
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

**Baseline**: 422 passed.

**Exigências do estado final**:

- código de saída zero;
- nenhum teste anterior perdido sem justificativa documentada no relatório;
- novos testes descobertos automaticamente pelo `pytest`;
- contagem final registrada no relatório;
- falhas internas convertidas em falhas reais pelo gate vigente.

O total final pode ser maior que 422 (novos testes adicionados). O total final **não pode ser menor** que 422 sem justificativa explícita para cada teste perdido.

---

## 16. Demonstração

### 16.1 Ponto de entrada real

O ponto de entrada obrigatório é `demo/demo.py`.

Verificar antes da implementação que `demo/demo.py` ainda está funcional para confirmar o comportamento inicial.

### 16.2 Tela de demonstração

Usar a tela real `config/telas/demo/demo.json`, que expõe bordas, chips e rótulos na barra de menus.

### 16.3 Sequência de validação manual

1. Executar `python demo/demo.py` após a implementação completa.
2. Observar a tela inicial: bordas, chips e rótulos.
3. Comparar com o comportamento anterior (registrado antes da implementação).
4. Redimensionar a janela do terminal livremente.
5. Maximizar, restaurar e reduzir a janela real.
6. Confirmar que os rótulos dos chips ("Sair", "Voltar", "Ajuda", "Verboso") **não** foram convertidos para maiúsculas.
7. Confirmar que as bordas (╭╮╰╯─│) e os delimitadores de chip ([]) permanecem iguais ao estado anterior.
8. Registrar o resultado no relatório de implementação.

### 16.4 Responsabilidade da validação TTY

A validação visual no terminal real é exclusiva do usuário. O executor e o QA não podem alegar aprovação visual. Até o usuário informar o resultado, o campo correspondente no relatório deve conter:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

---

## 17. Validação manual

### 17.1 Itens a confirmar

| # | Item | Critério |
|---|---|---|
| M-01 | Bordas preservadas | Caracteres ╭╮╰╯─│ visíveis idênticos ao estado anterior |
| M-02 | Delimitadores de chip preservados | [ e ] visíveis como antes |
| M-03 | Capitalização dos rótulos | "Sair", "Voltar", "Ajuda", "Verboso" — sem maiúsculas forçadas |
| M-04 | Redimensionamento | Layout ajusta sem erro visual após redimensionar |
| M-05 | Maximizar/restaurar | Layout recalcula corretamente |
| M-06 | Ausência de regressão visual | Nenhum elemento da barra ou da tela desaparece ou muda de posição |

### 17.2 Itens fora da competência do executor

- Validação de largura visual de caracteres Unicode em terminais específicos.
- Comparação visual entre terminais diferentes.
- Validação de cores `"padrão"` — o renderer atual não aplica cores diferenciadas; esta característica é preservada sem necessidade de validação especial.

---

## 18. Critérios de aceitação

Os critérios abaixo são verificáveis de forma objetiva. O QA deve checar cada um.

### 18.1 Configuração

- [ ] CA-C1: `config/estilo.json` contém `"borda": { "preset_default": "Borda Curva", "presets": {...} }`
- [ ] CA-C2: `config/estilo.json` contém `"chip": { "preset_default": "Colchete", "presets": {...} }`
- [ ] CA-C3: `config/estilo.json["chip"]["presets"]["Colchete"]["caixa_alta"] == false`
- [ ] CA-C4: `config/estilo.json["chip"]["presets"]["Colchete"]["cor_texto"] == "padrão"`
- [ ] CA-C5: `config/estilo.json["chip"]["presets"]["Colchete"]["cor_fundo"] == "padrão"`
- [ ] CA-C6: `config/estilo.json["_meta"]["status"] == "rascunho_inicial"` (inalterado)
- [ ] CA-C7: `config/estilo.json` não contém `cor_inativo`, `cor_alerta` ou `tiling` com valores inventados

### 18.2 Loader

- [ ] CA-L1: `carregar_estilo()` retorna `EstiloResolvido` com 18 campos populados
- [ ] CA-L2: todos os presets ativos são resolvidos (borda, chip, selecionado, incluido)
- [ ] CA-L3: `canto_superior_esquerdo == "╭"` após carregar configuração corrigida
- [ ] CA-L4: `caixa_alta == False` após carregar configuração corrigida
- [ ] CA-L5: `selecionado_simbolo == "→"`, `selecionado_off == " "`
- [ ] CA-L6: `incluido_on == "●"`, `incluido_off == "○"`
- [ ] CA-L7: `concluido_on == "✓"`, `concluido_off == " "`
- [ ] CA-L8: arquivo ausente levanta `EstiloErro`
- [ ] CA-L9: JSON inválido levanta `EstiloErro`
- [ ] CA-L10: seção obrigatória ausente levanta `EstiloErro`
- [ ] CA-L11: `preset_default` ausente levanta `EstiloErro`
- [ ] CA-L12: catálogo vazio levanta `EstiloErro`
- [ ] CA-L13: preset referenciado inexistente levanta `EstiloErro` sem fallback
- [ ] CA-L14: campo obrigatório ausente no preset ativo levanta `EstiloErro`
- [ ] CA-L15: tipo inválido (ex.: `caixa_alta` não booleano) levanta `EstiloErro`
- [ ] CA-L16: string vazia levanta `EstiloErro`
- [ ] CA-L17: `len(caractere) != 1` levanta `EstiloErro`
- [ ] CA-L18: configuração inválida não produz `EstiloResolvido` (parcialmente resolvido não é aceito)

### 18.3 Renderer

- [ ] CA-R1: `_BORDAS` não existe mais em `tela/renderizador.py`
- [ ] CA-R2: `tipo_borda` não é mais parâmetro de `renderizar_tela`
- [ ] CA-R3: chamada a `renderizar_tela` com `tipo_borda` levanta `TypeError`
- [ ] CA-R4: `renderizar_tela` aceita `estilo: EstiloResolvido` como parâmetro
- [ ] CA-R5: `"[{tecla}]"` não existe mais como literal em `_texto_chip_barra`
- [ ] CA-R6: borda renderizada deriva de `estilo.canto_superior_esquerdo` etc.
- [ ] CA-R7: delimitador de chip deriva de `estilo.caractere_esquerdo` e `estilo.caractere_direito`
- [ ] CA-R8: `caixa_alta=False` preserva capitalização declarada pelos chips
- [ ] CA-R9: `caixa_alta=True` aplica `.upper()` ao texto dos chips
- [ ] CA-R10: renderer não abre `config/estilo.json`
- [ ] CA-R11: renderer não escolhe preset autonomamente

### 18.4 Compatibilidade

- [ ] CA-T1: `demo.json` renderiza sem erro com o estilo carregado
- [ ] CA-T2: `destino_minimo.json` renderiza sem erro com o estilo carregado
- [ ] CA-T3: aparência inicial é visualmente equivalente ao estado anterior (validação pelo usuário)
- [ ] CA-T4: rótulos dos chips sem maiúsculas forçadas
- [ ] CA-T5: ordem e conteúdo dos chips inalterados
- [ ] CA-T6: nenhum comportamento de navegação ou seleção foi introduzido
- [ ] CA-T7: nenhum chamador no repositório passa `tipo_borda` a `renderizar_tela`
- [ ] CA-T8: `demo/diagnostico.py` fornece o estilo resolvido a `renderizar_tela`
- [ ] CA-T9: todas as chamadas a `renderizar_tela` em `demo/teste_diagnostico.py` passam `estilo` obrigatório
- [ ] CA-T10: todas as chamadas a `renderizar_tela` em `demo/teste_demo_console.py` passam `estilo` obrigatório
- [ ] CA-T11: nenhuma chamada ativa de `renderizar_tela` no repositório permanece incompatível com a assinatura final
- [ ] CA-T12: busca global confirma ausência de consumidores obrigatórios fora da lista nominal

```yaml
inventario_final_de_consumidores:
  busca_global_executada: true
  consumidores_incompativeis_restantes: 0
  consumidores_necessarios_fora_da_lista_nominal: 0
```

### 18.5 Testes

- [ ] CA-S1: testes positivos de materialização existem e passam
- [ ] CA-S2: testes negativos para cada condição V-01 a V-17 existem e passam
- [ ] CA-S3: prova de ausência de fallback silencioso existe e passa
- [ ] CA-S4: prova de consumo do estilo pelo renderer existe e passa (borda alternativa produz saída alternativa)
- [ ] CA-S5: prova de remoção de `_BORDAS` existe e passa
- [ ] CA-S6: regressão das telas existentes confirmada
- [ ] CA-S7: suite canônica completa (`PYTHONDONTWRITEBYTECODE=1 python -m pytest`) com código de saída zero
- [ ] CA-S8: contagem final de testes registrada no relatório
- [ ] CA-S9: nenhum teste anterior perdido sem justificativa

---

## 19. Relatório de implementação

Criar ao final da implementação:

```text
docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0039_CARREGAMENTO_ESTILO.md
```

O relatório deve conter obrigatoriamente:

1. **Estado inicial confirmado**: valores reais de `config/estilo.json` antes da alteração.
2. **Decisões técnicas adotadas**: resumo das decisões da Seção 6, com justificativas se divergirem.
3. **Arquivos alterados**: lista com o que mudou em cada arquivo.
4. **Materialização produzida**: instância `EstiloResolvido` com os 18 valores reais após a configuração.
5. **Hardcodings removidos**: `_BORDAS`, `tipo_borda`, `"[{tecla}]"` — confirmar remoção e localização original.
6. **Chamadas migradas**: lista de todas as chamadas a `renderizar_tela` migradas de `tipo_borda` para `estilo`, incluindo os arquivos adicionados pelo patch QA-H0039-001 (`demo/diagnostico.py`, `demo/teste_diagnostico.py`, `demo/teste_demo_console.py`).
6a. **Inventário final de consumidores**: confirmar o resultado das buscas executadas ao término da implementação:

```bash
rg -n --glob '*.py' 'renderizar_tela\s*\(' .
rg -n --glob '*.py' 'tipo_borda' .
rg -n --glob '*.py' '_BORDAS' .
```

Registrar no relatório: todas as ocorrências encontradas; arquivos adaptados; ocorrências históricas ou de teste justificadamente preservadas; ausência de consumidores incompatíveis.

7. **Testes criados ou atualizados**: lista nominal de novos testes e testes modificados, incluindo adaptações em `demo/teste_diagnostico.py` e `demo/teste_demo_console.py`.
8. **Suite focal**: resultado de `pytest tela/teste_loader.py tela/teste_renderizador.py -v`.
9. **Suite canônica**: resultado de `PYTHONDONTWRITEBYTECODE=1 python -m pytest` com contagem final.
10. **Demonstração preparada**: comando exato para reproduzir a demonstração.
11. **Validação manual TTY**: resultado informado pelo usuário ou `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO`.
12. **Limite de duplicidade JSON**: declarar explicitamente que duplicidade raw não é detectada (conforme Seção 11.2).
13. **Stage vazio**: confirmação de que nenhum arquivo extra foi acrescentado ao stage.
14. **Encerramento**: estado final da implementação.

---

## 20. Riscos e bloqueios

### 20.1 Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Regressão visual em bordas | Média | Alta | Confirmar correspondência `_BORDAS["curva"]` ↔ "Borda Curva" antes de remover `_BORDAS` |
| Rótulos em maiúsculas forçadas | Alta (se `caixa_alta` não corrigido) | Alta | Confirmar `caixa_alta: false` em `config/estilo.json` antes de executar demo |
| Testes que verificam caracteres hardcoded | Alta | Média | Atualizar testes em `tela/teste_renderizador.py` como parte da implementação |
| Quebra em `demo/demo.py` sem "b" | Alta | Baixa | Remoção é intencional e documentada; teste `demo/teste_demo.py` deve ser atualizado |
| `demo/demo_distribuicao.py` fora da lista nominal | Sem risco | — | Arquivo está na lista nominal Seção 14.2 |
| Chamador não detectado de `renderizar_tela` | Baixa | Média | QA confirmou 8 arquivos (4 com `tipo_borda` + 3 sem + `tela/teste_renderizador.py`); busca global (Seção 19 item 6a) deve confirmar zero consumidores incompatíveis restantes |

### 20.2 Bloqueios potenciais

| Situação de bloqueio | Ação |
|---|---|
| `contrato_estilo.md` R-6 interpretado como largura visual de terminal (wcwidth), não como `len()` | Registrar bloqueio documental e parar — não avançar com medição alternativa sem decisão do usuário |
| Chamador de `renderizar_tela` descoberto na implementação que não consta da lista nominal (Seção 14) | Parar e obter autorização do usuário para incluir na lista nominal — a busca global (Seção 19 item 6a) deve confirmar o inventário completo antes de encerrar |
| Arquivo fora da lista nominal que precisa ser alterado | Parar e obter autorização do usuário |
| `config/estilo.json` com estrutura diferente do estado confirmado na Seção 5.1 | Investigar antes de alterar; reportar ao usuário |

### 20.3 Não são bloqueios

- A ausência de implementação de `cor_inativo` e `cor_alerta` (pendências deferidas na ADR-0030 D12).
- A ausência de implementação de `tiling` (pendência deferida).
- A remoção do comando "b" no demo (decisão da Seção 6.5).
- A contagem final de testes maior que 422 (esperada pela adição de testes).

---

## 21. Estado final esperado

```yaml
config_estilo:
  preset_default_borda: "Borda Curva"
  preset_default_chip: "Colchete"
  caixa_alta_colchete: false
  status_meta: "rascunho_inicial"  # inalterado

loader:
  EstiloResolvido: implementado
  carregar_estilo: implementado
  validacoes_D9: implementadas
  fallback_silencioso: ausente

renderer:
  _BORDAS: removido
  tipo_borda: removido
  formato_chip_hardcoded: removido
  borda_do_estilo: consumida
  chip_do_estilo: consumido

chamadores:
  tipo_borda: zero_ocorrencias_no_repositorio
  renderizar_tela_sem_estilo: zero_ocorrencias_ativas_incompativeis

inventario_consumidores:
  busca_global_executada: true
  consumidores_incompativeis_restantes: 0
  consumidores_necessarios_fora_da_lista_nominal: 0

aparencia:
  visualmente_equivalente_ao_estado_anterior: confirmado_pelo_usuario

suite_canonica:
  codigo_saida: 0
  testes_perdidos_sem_justificativa: nenhum
  contagem_final: registrada_no_relatorio
```

---

## 22. Encerramento

Este handoff está pronto para execução de implementação. O estado do handoff é:

```yaml
handoff: H-0039
estado: HANDOFF_CRIADO_AGUARDANDO_QA
proxima_etapa: QA_INDEPENDENTE_DO_HANDOFF
```

HANDOFF_CREATED_AWAITING_QA
