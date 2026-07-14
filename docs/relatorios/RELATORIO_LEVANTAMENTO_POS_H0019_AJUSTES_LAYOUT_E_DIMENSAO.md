---
name: relatorio-levantamento-pos-h0019-ajustes-layout-e-dimensao
description: Levantamento técnico pós-H-0019 sobre dois achados manuais — preenchimento vertical das áreas alocadas no corpo horizontal e ausência de configuração declarativa de largura da tela em orquestrador.json
metadata:
  type: relatorio
  scope: scripts
  status: LEVANTAMENTO_CONCLUIDO
  data: "2026-07-10"
---

# RELATORIO_LEVANTAMENTO_POS_H0019_AJUSTES_LAYOUT_E_DIMENSAO

## Status

```
LEVANTAMENTO_CONCLUIDO
```

Relatório auxiliar. Não consome número de handoff.

---

## Base verificada

| Item | Valor |
|---|---|
| HEAD observado | `29a8a79  feat: implementa layout horizontal plano do corpo` |
| Workspace | Limpo |
| Commit esperado | `29a8a79  feat: implementa layout horizontal plano do corpo` |
| Coincidência | SIM |

---

## Objetivo

Mapear, sem corrigir, o estado atual de dois temas identificados manualmente após o commit do H-0019:

- **Tema A**: o layout horizontal distribui a largura corretamente, mas o preenchimento vertical das áreas alocadas não está correto.
- **Tema B**: não foi encontrada em `orquestrador.json` configuração declarativa para ajuste da largura da tela.

---

## Arquivos analisados

### Código

```
tela/renderizador.py   — implementação do renderer (H-0019 incluído)
tela/loader.py         — validação de corpo.arranjo (H-0019)
tela/modelo.py         — estrutura Corpo/ElementoCorpo
tela/demo.py           — ponto de entrada; leitura de shutil.get_terminal_size
tela/diagnostico.py    — (referenciado; não lido integralmente neste ciclo)
```

### Documentação normativa

```
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/NOMENCLATURA.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

### Artefatos do H-0019

```
docs/handoff/H-0019-layout-horizontal-plano-corpo.md
docs/relatorios/IMP-0019-layout-horizontal-plano-corpo.md
docs/relatorios/RELATORIO_QA_H-0019_LAYOUT_HORIZONTAL_PLANO_CORPO.md
```

### JSONs

```
config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json
```

---

## Comandos executados

### Grep A — largura, width, dimensão, terminal_size

```bash
grep -RIn "largura\|width\|dimensao\|dimensão\|ajustado_ao_conteudo\|terminal_size\|get_terminal_size" \
  docs config tela || true
```

Resultados relevantes (seleção):

```
docs/contratos/contrato_tela_json.md:246:largura **e** a altura disponíveis da janela do terminal. A largura já é
docs/contratos/contrato_tela_json.md:247:tratada dinamicamente; a `altura_disponivel` passa a ser **dimensão futura**
docs/contratos/contrato_json_tela_minima.md:97:  composição por largura de terminal.
docs/contratos/contrato_json_tela_minima.md:166:- O renderer não inventa arranjo, não cria fallback próprio baseado em largura
docs/NOMENCLATURA.md:648:## 6. Layout e largura
docs/NOMENCLATURA.md:650:- **Largura de tela**: sempre dinâmica, calculada a partir da largura real
docs/NOMENCLATURA.md:653:  depende de largura fixa.
tela/demo.py:217:    tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
tela/demo.py:218:    largura = tamanho_terminal.columns
```

Nenhuma ocorrência de `largura` ou campo de dimensão dentro de `config/telas/*.json`.

### Grep B — arranjo horizontal, altura, preenchimento

```bash
grep -RIn "arranjo.*horizontal\|_montar_corpo_horizontal\|altura\|height\|preench" \
  tela docs/contratos docs/adr docs/NOMENCLATURA.md || true
```

Resultados relevantes (seleção):

```
tela/renderizador.py:686:def _montar_corpo_horizontal(elementos, borda, total_w):
tela/renderizador.py:740:    # Normalizar altura com preenchimento inferior (ADR-0015 D10)
tela/renderizador.py:741:    altura_max = max(...)
tela/renderizador.py:746:        while len(linhas) < altura_max:
tela/renderizador.py:747:            linhas.append(" " * larguras[i])
tela/demo.py:172:    preserva o comportamento atual (sem preenchimento vertical); quando
tela/demo.py:219:    altura = tamanho_terminal.lines
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:129:- distribuição aloca área, não apenas conteúdo;
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:131:- sobra horizontal vira padding/espaços em branco;
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:132:- sobra vertical vira linhas em branco.
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:244:Horizontal: preencher com espaços; preservar largura da faixa.
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md:246:Vertical: preencher com linhas em branco; preservar altura da faixa.
```

### Testes

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
```

```
Total de verificacoes: 89
Passaram: 89
Falharam: 0
```

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
```

```
Total de verificacoes: 261
Passaram: 261
Falharam: 0
```

Base atual: **89/89 + 261/261** — sem regressões.

---

## Tema A — Preenchimento vertical no layout horizontal

### Comportamento esperado pela ADR-0015

**Decisão 5** (Distribuição por container):
> - distribuição aloca área, não apenas conteúdo;
> - elemento funcional deve preservar a área alocada;
> - sobra vertical vira linhas em branco.

**Decisão 10** (Preenchimento de espaço vazio):
> **Vertical:** preencher com linhas em branco; preservar altura da faixa.

Portanto, quando o corpo horizontal tem área disponível maior do que o conteúdo mais alto das colunas, cada coluna deve ser preenchida com linhas em branco **dentro de sua faixa alocada**, até a altura total disponível do corpo.

### Comportamento observado no código

#### `_montar_corpo_horizontal` — `renderizador.py` linhas 686–760

```python
# Passo 4 — Normalizar altura com preenchimento inferior (ADR-0015 D10)
altura_max = max(
    (len(linhas) for linhas in todas_as_linhas_por_area), default=0
)
for i, linhas in enumerate(todas_as_linhas_por_area):
    while len(linhas) < altura_max:
        linhas.append(" " * larguras[i])
```

A função calcula `altura_max` como o máximo de linhas entre as áreas do bloco horizontal — i.e., a altura do elemento mais alto entre os filhos diretos. O preenchimento vai **somente até esse máximo interno**, não até a altura disponível do corpo.

A função não recebe `altura` nem `l_corpo_disponivel` como parâmetro. Sua assinatura atual:

```python
def _montar_corpo_horizontal(elementos, borda, total_w):
```

#### `renderizar_tela` — H-0015 preenchimento vertical

```python
# renderizador.py linhas 907–938
if altura is not None:
    l_cab = _contar_linhas(partes[0])
    l_barra = len(linhas_barra) + 2
    l_corpo_conteudo = sum(_contar_linhas(p) for p in partes[1:])
    ...
    l_corpo_fill = l_corpo_disponivel - l_corpo_conteudo
    if l_corpo_fill > 0:
        partes.append(
            "\n".join(" " * total_w for _ in range(l_corpo_fill))
        )
```

Quando `altura` é fornecido (terminal real em `demo.py`), o preenchimento vertical de H-0015 insere linhas `" " * total_w` **fora do bloco horizontal** — plain strings de `total_w` espaços, sem divisão em colunas, sem bordas.

#### Consequência visual observável

Quando o terminal tem altura maior que o conteúdo das caixas horizontais:

1. O bloco horizontal fecha suas bordas inferiores (`╯╰╯╰`) na altura da caixa mais alta.
2. As caixas mais baixas (`╰─╯`) fecham antes do final da área do corpo.
3. O preenchimento de H-0015 insere linhas de espaços abaixo do bloco — sem estrutura de coluna.
4. Sobram linhas vazias "fora das caixas" na área do corpo.

Este comportamento contraria as Decisões 5 e 10 da ADR-0015:
- A área alocada a cada coluna não é preservada até a altura total disponível.
- A sobra vertical vira linhas em branco, mas fora da faixa, não dentro dela.

### Lacuna identificada

| Aspecto | Estado atual | Estado esperado (ADR-0015) |
|---|---|---|
| Altura das colunas | Normalizada até `altura_max` (máximo entre colunas) | Normalizada até `l_corpo_disponivel` (altura disponível do corpo) |
| Preenchimento de coluna mais curta | Preenchida até `altura_max` com `" " * larguras[i]` | Preenchida até `l_corpo_disponivel` com `" " * larguras[i]` |
| Preenchimento H-0015 no modo horizontal | Linhas `" " * total_w` adicionadas após o bloco, sem estrutura de coluna | Deveria ser absorvido dentro de `_montar_corpo_horizontal` |
| Borda inferior das caixas | Fecha em `altura_max` (abaixo do conteúdo mais alto) | Deve fechar em `l_corpo_disponivel` |
| Linhas vazias fora das caixas | Existem quando `l_corpo_disponivel > altura_max` | Não devem existir — fill vai para dentro das colunas |

### Arquivos provavelmente envolvidos

| Arquivo | Função | Mudança necessária |
|---|---|---|
| `tela/renderizador.py` | `_montar_corpo_horizontal` (linha 686) | Aceitar `altura_disponivel_corpo: int \| None = None`; quando fornecido, usar no lugar de `altura_max` para preenchimento inferior |
| `tela/renderizador.py` | `renderizar_tela` (linha 763) | Passar `l_corpo_disponivel` para `_montar_corpo_horizontal` quando `altura` for fornecido; não adicionar fill H-0015 adicional quando o bloco horizontal já consumiu toda a área |

O cálculo de `l_corpo_fill` em `renderizar_tela` precisaria ser condicionado: se o arranjo é horizontal e o fill já foi absorvido dentro do bloco, `l_corpo_fill` deve ser 0.

### Risco para `barra_de_menus`

Baixo. A correção toca apenas `_montar_corpo_horizontal` e o ponto em `renderizar_tela` onde `l_corpo_fill` é calculado. As funções protegidas da barra — `_normalizar_distribuicao`, `_validar_distribuicao`, `_linhas_barra`, `_validar_ancoras` — não precisam ser tocadas. A barra permanece como último item em `partes`, exatamente como no fluxo atual.

### Próximo ciclo recomendado

```
H-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal
```

Justificativa: é ajuste direto de renderização. Não exige novo tipo de container, novo modelo de área nem nova regra arquitetural. A estrutura necessária (a passagem de `altura_disponivel_corpo` para `_montar_corpo_horizontal`) é uma extensão da lógica existente, sem redesenho de interface.

Não se classifica como `ARCHITECTURE_REVIEW_REQUIRED` porque:
- `modelo.py` não precisa ser alterado;
- a interface de `renderizar_tela` já recebe `altura` — o parâmetro apenas precisa ser propagado internamente;
- `_montar_corpo_horizontal` pode absorver o fill com uma extensão de assinatura simples;
- a correção não muda nenhuma regra normativa — apenas implementa o que ADR-0015 D10 já exige.

---

## Tema B — Configuração declarativa da largura da tela

### Estado em `orquestrador.json`

O arquivo `config/telas/orquestrador.json` não possui nenhum campo declarativo de largura ou dimensão. Os campos presentes são:

```
schema, id, metadados, cabecalho, corpo, barra_de_menus, filtros, bindings, referencias_de_acoes
```

Nenhum dos JSONs ativos (`orquestrador.json`, `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json`) possui campo de largura, dimensão ou preferência de terminal.

### Estado nos contratos

**`contrato_tela_json.md`** (seção 9, linha 246):

> A tela deve ocupar a largura **e** a altura disponíveis da janela do terminal. A largura já é tratada dinamicamente; a `altura_disponivel` passa a ser **dimensão futura** da renderização da tela.

Observação: o contrato registra largura como tratada dinamicamente (via terminal), mas não define campo JSON para declarar largura. O campo `altura_disponivel` é mencionado como "dimensão futura" — nunca implementado como campo JSON.

**`contrato_json_tela_minima.md`** (seções 4 e 5):

- `corpo.arranjo` é campo opcional, mas não há campo `largura` nem `dimensao` definido.
- Linha 97: "O renderer não inventa arranjo, não cria fallback próprio baseado em largura de terminal."
- Linha 166: "O renderer não cria fallback próprio baseado em largura de terminal e não decide composição por condição de ambiente."

Os contratos proibem que o renderer tome decisões baseadas na largura do terminal, mas não definem campo JSON para declarar largura.

### Estado em ADR/NOMENCLATURA

**`NOMENCLATURA.md`** — Seção 6 "Layout e largura" (linha 648):

> **Largura de tela**: sempre dinâmica, calculada a partir da largura real do terminal. Nenhuma parte do sistema depende de largura fixa.

A NOMENCLATURA afirma explicitamente que a largura é **sempre dinâmica** — sem largura fixa e sem campo declarativo.

**ADR-0015** — Decisão 11 "Regras dinâmicas de dimensão":

> Conceitos futuros registrados:
> - `minimo`: menor dimensão permitida
> - `preferido`: dimensão desejada
> - `maximo`: maior dimensão permitida
> - `restante`: recebe espaço remanescente
> - `conteudo`: dimensão ajustada ao conteúdo renderizado
>
> **Decisão:** `ajustado ao conteúdo` deve ser tratado como `preferido`, não como `minimo`.

Esses conceitos são registrados como futuros. A semântica de `largura` como campo JSON não está fechada nesta ADR — nem definida como min, nem como preferido, nem como máximo.

### Estado no código

**`tela/demo.py`** (linhas 217–219):

```python
tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
largura = tamanho_terminal.columns
altura = tamanho_terminal.lines
```

A largura vem inteiramente do terminal/runtime via `shutil.get_terminal_size`.

**`tela/renderizador.py`** — assinatura de `renderizar_tela` (linha 763):

```python
def renderizar_tela(
    modelo: ModeloTela,
    tipo_borda: str = "curva",
    largura: int | None = None,
    altura: int | None = None,
) -> str:
```

Existe parâmetro Python `largura` na função do renderer, mas ele é passado pelo chamador (demo/diagnostico), não lido do JSON.

**Suporte parcial via Python, ausente no JSON**: o renderer aceita `largura` como parâmetro Python, mas nenhuma parte do pipeline lê largura do JSON da tela. Não existe caminho `JSON → modelo → renderer.largura`.

### Lacuna identificada

| Aspecto | Estado atual |
|---|---|
| Campo `largura` em JSONs de tela | Ausente em todos os JSONs ativos |
| Contrato que define campo `largura` no JSON | Inexistente |
| `contrato_tela_json.md` | Menciona largura como dinâmica; não define campo declarativo |
| `NOMENCLATURA.md` | Afirma largura sempre dinâmica (seção 6) |
| ADR-0015 D11 | Registra conceitos futuros (min/preferred/max/content) sem fechar semântica |
| Código — parâmetro Python | `renderizar_tela(largura=...)` aceita largura, mas não lida do JSON |
| Código — fonte de largura | Exclusivamente `shutil.get_terminal_size` em `demo.py` |

Para implementar largura declarativa seria necessário:

1. Definir a semântica do campo: é largura fixa? Largura mínima? Largura preferida? Largura máxima? Ou alguma combinação via ADR-0015 D11 (min/preferred/max)?
2. Atualizar `contrato_tela_json.md` com o campo e suas regras.
3. Atualizar `contrato_json_tela_minima.md` incluindo o campo como opcional.
4. Provavelmente atualizar `NOMENCLATURA.md` seção 6, que atualmente afirma largura sempre dinâmica — contradição direta com campo declarativo.
5. Possivelmente emitir ou estender ADR (ADR-0015 D11 ou nova ADR) formalizando como largura declarativa interage com largura do terminal e com as regras dinâmicas.

Apenas depois desse ciclo documental a implementação em código seria válida.

### Próximo ciclo recomendado

```
CICLO_DOCUMENTAL_PREVIO_REQUERIDO
```

Justificativa: os contratos ativos (`contrato_tela_json.md`, `contrato_json_tela_minima.md`) não definem campo de largura no JSON; `NOMENCLATURA.md` seção 6 contradiz explicitamente a ideia de largura fixa; ADR-0015 D11 registra os conceitos como futuros mas não fecha a semântica. Implementar `largura` declarativa sem fechar esses documentos violaria o protocolo de desenvolvimento (`contrato_processo_desenvolvimento.md`).

O ciclo documental deve preceder o ciclo de código. Só após o fechamento documental o ciclo receberia número de handoff próprio (H-0021 candidato).

---

## Separação recomendada entre H-0020 e H-0021

| Ciclo | Tema | Tipo | Pré-requisito |
|---|---|---|---|
| **H-0020** | Preenchimento vertical das áreas alocadas no corpo horizontal | Implementação (renderização) | Nenhum — segue diretamente do H-0019 com base nos contratos atuais |
| **H-0021** | Dimensão declarativa da tela no JSON | Implementação (loader + renderer) | Ciclo documental prévio — contrato, NOMENCLATURA, ADR/extensão ADR-0015 D11 |

Os dois temas são independentes: H-0020 não afeta nem depende da semântica de largura declarativa. H-0021 não depende do preenchimento vertical.

A separação é obrigatória: H-0020 é ajuste direto de renderização com base em contratos existentes; H-0021 exige abertura de documentação antes de qualquer linha de código.

---

## Riscos

### R-A1 — Confundir `altura_max` de bloco com `l_corpo_disponivel`

O H-0019 implementou `altura_max` como normalização interna do bloco horizontal (máximo entre colunas). Para H-0020, será necessário distinguir claramente:

- `altura_max`: normaliza colunas de alturas diferentes dentro do bloco (invariante do H-0019, a preservar)
- `l_corpo_disponivel`: altura total disponível do corpo para o fill vertical (nova responsabilidade do H-0020)

O algoritmo de H-0020 deve reter `altura_max` como passo intermediário e depois estender cada coluna de `altura_max` até `l_corpo_disponivel`.

### R-A2 — Duplo preenchimento

Se H-0020 absorver o fill vertical dentro de `_montar_corpo_horizontal`, a lógica de `l_corpo_fill` em `renderizar_tela` (H-0015) deve ser neutralizada para o modo horizontal. O risco é inserir fill duplo: um dentro do bloco e outro por H-0015 após o bloco.

Mitigação: `renderizar_tela` deve detectar que o bloco horizontal já consumiu `l_corpo_disponivel` e não adicionar `l_corpo_fill` adicional nesse caso.

### R-A3 — Regressão em testes de `test_arranjo_horizontal_padding_inferior`

O teste atual verifica que a área mais curta é preenchida até `altura_max`. Com H-0020, o comportamento muda: a área mais curta deve ser preenchida até `l_corpo_disponivel`. Testes existentes que dependem de `altura_max` como referência precisarão ser revistos.

### R-B1 — Contradição futura de `NOMENCLATURA.md` seção 6

Qualquer implementação de largura declarativa que não atualize a seção 6 de `NOMENCLATURA.md` ("Largura de tela: sempre dinâmica") criará contradição normativa documentada. O ciclo documental de H-0021 deve tratar essa seção explicitamente.

### R-B2 — Ambiguidade semântica de largura declarativa

Sem definir se `largura` é mínima, preferida, máxima ou fixa, o código pode implementar uma semântica que o usuário não pretendia. A ADR-0015 D11 usa os conceitos `minimo/preferido/maximo/restante/conteudo` — o campo `largura` em JSON deve ser mapeado explicitamente para um desses conceitos.

---

## Conclusão

O H-0019 implementou corretamente o particionamento horizontal da largura entre filhos diretos do corpo. Dois achados manuais pós-implementação revelam trabalho pendente:

**Tema A**: a função `_montar_corpo_horizontal` não recebe a altura disponível do corpo e normaliza apenas até `altura_max` (a caixa mais alta). O preenchimento H-0015 posterior insere linhas de espaços fora das colunas, sem preservar a estrutura de faixas. Isso contradiz ADR-0015 D5 e D10. A correção é ajuste direto de renderização em `renderizador.py` — sem toque em `modelo.py` e sem risco para `barra_de_menus`. Classificado como **H-0020 — Preenchimento vertical das áreas alocadas no corpo horizontal**.

**Tema B**: não existe campo declarativo de largura em nenhum JSON de tela ativo. `NOMENCLATURA.md` seção 6 afirma explicitamente que a largura é sempre dinâmica. `contrato_tela_json.md` não define campo de largura no JSON. ADR-0015 D11 registra os conceitos min/preferred/max como futuros sem fechar semântica. A largura vem exclusivamente de `shutil.get_terminal_size` no runtime. Antes de qualquer implementação, é necessário ciclo documental que feche a semântica, atualize contratos e NOMENCLATURA, e possivelmente estenda a ADR-0015 D11. Classificado como **CICLO_DOCUMENTAL_PREVIO_REQUERIDO** (candidato a H-0021 pós-documentação).
