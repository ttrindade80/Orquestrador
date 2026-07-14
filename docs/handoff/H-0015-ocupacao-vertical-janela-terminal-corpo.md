---
name: H-0015-ocupacao-vertical-janela-terminal-corpo
description: Handoff de implementação — propaga altura do terminal ao renderer, preenche o corpo com linhas em branco até ocupar a altura disponível entre cabeçalho e barra_de_menus; implementa ADR-0013; não implementa ADR-0014
metadata:
  type: handoff_implementacao
  status: HANDOFF_READY
  id: H-0015
  data_criacao: 2026-07-09
rastreabilidade:
  adrs_aplicadas:
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
  adrs_fora_de_escopo:
    - docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
  contratos_alvo: []
  handoffs_anteriores:
    - docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
  commit_base: 4762583
---

# H-0015 — Ocupação vertical da janela do terminal pelo corpo

## Status

`HANDOFF_READY`

---

## Metadados de rastreabilidade

| Campo | Valor |
|---|---|
| ID | H-0015 |
| Data de criação | 2026-07-09 |
| HEAD base | `4762583` |
| Handoff anterior aprovado | H-0014 (QA_APPROVED_WITH_NOTES) |
| ADR aplicada | ADR-0013 |
| ADR fora de escopo | ADR-0014 |
| Commit base | `4762583` — docs: registra ocupacao vertical e barra responsiva |
| Sequência futura | H-0016 — distribuição horizontal responsiva da barra_de_menus (ADR-0014) |

---

## Ordem de autoridade

Este handoff segue a hierarquia do `contrato_processo_desenvolvimento.md`:

1. Contrato de processo
2. ADRs aceitas (ADR-0013)
3. Contratos de módulo
4. **Este handoff**
5. Relatório de implementação

Qualquer contradição entre este handoff e um contrato ou ADR deve ser reportada
como `ARCHITECTURE_REVIEW_REQUIRED`. O handoff não pode sobrescrever contrato.

---

## Contexto

O H-0014 foi implementado e aprovado. A base está limpa em `4762583`. O sistema
entrega:

- `demo.py` lê `shutil.get_terminal_size(fallback=(80, 24)).columns` — apenas
  a **largura** do terminal.
- `renderizar_tela(modelo, tipo_borda, largura)` recebe apenas `largura`, sem
  nenhum parâmetro de altura.
- O corpo ocupa a largura disponível, mas **não preenche a altura disponível**
  da janela do terminal.
- O fluxo demonstrável `g / d / b / Esc` funciona corretamente.
- `corpo.arranjo = "vertical"` está em todos os JSONs ativos; significa
  ordem/composição dos elementos (ADR-0011), não ocupação de altura de terminal.

A ADR-0013 normatizou que:
- a tela deve ocupar largura **e** altura disponíveis da janela;
- o corpo deve preencher a área entre cabeçalho e barra_de_menus;
- o preenchimento vertical é responsabilidade do renderer, não do JSON;
- `corpo.arranjo = "vertical"` não é reinterpretado por esta decisão.

Este handoff implementa a ADR-0013. Ele **não implementa** a ADR-0014.

---

## Relação com ADR-0013 e ADR-0014

### ADR-0013 — implementada por este handoff

A ADR-0013 fixa que:
- a altura do terminal deve ser tratada como dimensão explícita do render;
- o corpo ocupa `altura_disponivel = altura - L_cab - L_barra`;
- quando o conteúdo funcional do corpo não preencher toda a
  `altura_disponivel`, o renderer insere linhas em branco;
- o preenchimento não é novo arranjo, não é novo tipo de elemento, não é
  declaração no JSON.

Este handoff fecha a representação exata das linhas em branco (pendência
explícita da ADR-0013, item 9) — ver seção "Contabilidade de linhas e
representação das linhas em branco".

### ADR-0014 — explicitamente fora deste ciclo

Este handoff **não implementa** nenhum item da ADR-0014. Os itens abaixo
pertencem ao H-0016 e são **proibidos** neste ciclo:

```
- barra_de_menus.distribuicao.modo = "horizontal_responsiva"
- quebra multilinha de chips
- coluna_a_coluna
- linha_a_linha
- âncoras de chip
- overflow da barra_de_menus
- erro de layout da barra quando chips não couberem horizontalmente
```

---

## Objetivo

Implementar a ocupação vertical da janela do terminal pelo corpo, de forma
mínima, determinística e testável:

1. A demo captura a altura real do terminal via `.lines` de
   `shutil.get_terminal_size`.
2. A demo propaga a altura ao renderer.
3. O renderer aceita `altura: int | None = None` como novo parâmetro opcional.
4. Quando `altura` for fornecida e suficiente, a saída do renderer tem
   exatamente `altura` linhas.
5. O cabeçalho permanece no topo.
6. A barra_de_menus permanece no rodapé da tela.
7. O corpo ocupa todo o espaço vertical entre cabeçalho e barra_de_menus.
8. Quando o conteúdo real do corpo usar menos linhas que `altura_disponivel`,
   o renderer preenche o restante com linhas em branco conforme especificado
   neste handoff.
9. Quando `altura` for `None`, o comportamento atual é preservado sem
   alteração (nenhuma linha de preenchimento é inserida).
10. O comportamento em terminal pequeno é determinístico: `RenderizadorErro`
    com mensagem descritiva; nunca truncamento silencioso.

---

## Leitura obrigatória

O implementador deve ler, antes de alterar qualquer arquivo:

```
docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
docs/adr/ADR-0014-barra-horizontal-termos-especificos.md
docs/adr/INDICE_ADR.md

docs/contratos/contrato_processo_desenvolvimento.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_barra_de_menus.md
docs/contratos/contrato_lancador.md
docs/contratos/contrato_console.md

docs/handoff/H-0015-ocupacao-vertical-janela-terminal-corpo.md  (este arquivo)
docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md

config/telas/orquestrador.json
config/telas/grupo_minimo.json
config/telas/destino_minimo.json
config/telas/stub_b.json

tela/renderizador.py
tela/demo.py
tela/teste_renderizador.py
tela/teste_demo.py
```

---

## Escopo positivo

O H-0015 deve implementar **apenas** o seguinte:

### 1. Alterar `tela/demo.py`

**1a. `main()`**: ler largura **e** altura do terminal em uma única chamada.

Antes:
```python
largura = shutil.get_terminal_size(fallback=(80, 24)).columns
```

Depois:
```python
tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
largura = tamanho_terminal.columns
altura = tamanho_terminal.lines
```

**1b. `renderizar_estado(estado, modelo, largura=None)`**: adicionar parâmetro
`altura=None` e repassá-lo ao renderer.

Antes:
```python
def renderizar_estado(estado, modelo, largura=None):
    return renderizar_tela(modelo, tipo_borda=estado["tipo_borda"], largura=largura)
```

Depois:
```python
def renderizar_estado(estado, modelo, largura=None, altura=None):
    return renderizar_tela(
        modelo, tipo_borda=estado["tipo_borda"], largura=largura, altura=altura
    )
```

**1c. `main()`**: passar `largura` e `altura` a `renderizar_estado`.

Toda chamada a `renderizar_estado(estado, modelo, largura)` em `main()` deve
passar também `altura=altura`. A variável `altura` é lida uma vez ao início de
`main()` e reutilizada (o terminal pode redimensionar entre chamadas — isso é
aceitável para este ciclo; o fallback já garante comportamento defensivo).

Nenhuma outra linha de `demo.py` deve ser alterada.

### 2. Alterar `tela/renderizador.py`

**2a. Assinatura de `renderizar_tela`**: adicionar `altura: int | None = None`.

Antes:
```python
def renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva", largura: int | None = None) -> str:
```

Depois:
```python
def renderizar_tela(
    modelo: ModeloTela,
    tipo_borda: str = "curva",
    largura: int | None = None,
    altura: int | None = None,
) -> str:
```

**2b. Lógica de preenchimento vertical**: quando `altura` não for `None`,
calcular `altura_disponivel` e inserir linhas de preenchimento entre os boxes
do corpo e a barra_de_menus, conforme a contabilidade especificada na seção
"Contabilidade de linhas e representação das linhas em branco" abaixo.

**2c. Quando `altura` for `None`**: o comportamento atual é preservado
integralmente — nenhuma linha de preenchimento é inserida, a saída é idêntica
à do código atual.

Nenhuma outra mudança em `renderizador.py`.

### 3. Alterar `tela/teste_renderizador.py`

Adicionar casos de teste para `altura` explícita — ver seção "Testes
obrigatórios a exigir no handoff".

Os casos existentes não precisam ser alterados, pois `altura=None` preserva o
comportamento anterior.

### 4. Alterar `tela/teste_demo.py`

Adicionar casos de teste para `renderizar_estado` com `altura` explícita e para
`main()` com terminal de tamanho fixo — ver seção "Testes obrigatórios".

Os casos existentes não precisam ser alterados, pois `altura=None` é o default
e o comportamento sem altura continua idêntico.

### 5. Criar `docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md`

Ver seção "Relatório de implementação".

---

## Contabilidade de linhas e representação das linhas em branco

Esta seção fecha a decisão de implementação pendente da ADR-0013, item 9.

### Definições

Toda função `_caixa(label, linhas_conteudo, ...)` gera:
- 1 linha de topo (`_linha_topo`)
- `len(linhas_conteudo)` linhas de conteúdo
- 1 linha de base (`_linha_base`)
- Total: `len(linhas_conteudo) + 2` linhas

Portanto:

```
L_cab       = 2 + N_linhas_conteudo_cab
              Para o Orquestrador (descricao = 1 linha): L_cab = 3

L_barra     = 2 + N_chips
              Para o Orquestrador (2 chips): L_barra = 4

L_corpo_i   = 2 + N_linhas_conteudo_i   (para cada caixa de elemento i)
L_corpo_conteudo = soma de L_corpo_i para todos os elementos do corpo
              Para o Orquestrador (ITENS=3, INFO=2, NAVEGAR=4): 9

L_corpo_disponivel = altura - L_cab - L_barra

L_corpo_fill = max(0, L_corpo_disponivel - L_corpo_conteudo)

Total saída = L_cab + L_corpo_conteudo + L_corpo_fill + L_barra = altura
```

### Separadores entre regiões

Não há separadores extras entre cabeçalho, corpo e barra_de_menus. As regiões
são adjacentes: a linha de base de uma caixa é seguida diretamente pela linha
de topo da próxima. Isso já é o comportamento atual (nenhuma mudança neste
ponto).

### Representação exata das linhas em branco (fechada neste handoff)

As linhas de preenchimento são **linhas físicas de `largura` espaços**:

```python
linha_branca = " " * total_w
```

Onde `total_w` é o mesmo calculado por `renderizar_tela` a partir de `largura`
(ou `TOTAL_WIDTH = 42` quando `largura=None`, mas neste caso `altura=None`
também, portanto nenhuma linha de preenchimento é gerada).

As linhas em branco são inseridas **após o último box de elemento do corpo e
antes do box da barra_de_menus** — não estão dentro de nenhuma caixa bordeada,
não são novo elemento do corpo, não são declaradas no JSON.

A justificativa desta representação:
- Linha física (não visual interna a caixa): não exige caixa aberta/fechada
  especial; o corpo não tem uma caixa encapsuladora no modelo atual.
- `largura` espaços: mantém o invariante de que cada linha não vazia da saída
  tem exatamente `total_w` caracteres (linhas de preenchimento têm exatamente
  `total_w` espaços).
- Determinístico: dado `largura` e `altura`, o número e o conteúdo das linhas
  de preenchimento são determinísticos.

### Verificação de altura total

```python
saida = renderizar_tela(modelo, largura=largura, altura=altura)
# saida termina com "\n"
assert saida.count("\n") == altura
```

Ou equivalentemente:
```python
linhas = saida.split("\n")
assert len(linhas) == altura + 1   # N linhas + 1 str vazia do trailing "\n"
assert linhas[-1] == ""            # trailing "\n" → último elemento é vazio
```

### Política para terminal pequeno (determinística)

Se `altura` for fornecida e `L_cab + L_barra > altura`:
```python
raise RenderizadorErro(
    "altura insuficiente: terminal com {0} linhas nao comporta "
    "cabecalho ({1}) + barra_de_menus ({2})".format(altura, L_cab, L_barra)
)
```

Se `altura` for fornecida e `L_corpo_conteudo > L_corpo_disponivel` (conteúdo
do corpo excede a área disponível):
```python
raise RenderizadorErro(
    "altura insuficiente: corpo requer {0} linhas mas area disponivel "
    "e {1} linhas (altura={2}, cabecalho={3}, barra={4})".format(
        L_corpo_conteudo, L_corpo_disponivel, altura, L_cab, L_barra
    )
)
```

Nunca truncar. Nunca omitir caixas silenciosamente. Sempre `RenderizadorErro`.

### Exemplos concretos com o Orquestrador (largura=42)

O Orquestrador em largura=42 gera atualmente 16 linhas:
- L_cab = 3 (1 topo + 1 descricao + 1 base)
- L_corpo_conteudo = 9 (ITENS=3, INFO=2, NAVEGAR=4)
- L_barra = 4 (1 topo + 2 chips + 1 base)

| altura | L_corpo_disponivel | L_corpo_fill | Total saída |
|---|---|---|---|
| `None` | n/a | 0 | 16 linhas (comportamento atual) |
| 16 | 9 | 0 | 16 linhas (sem preenchimento) |
| 20 | 13 | 4 | 20 linhas (4 linhas brancas) |
| 24 | 17 | 8 | 24 linhas (8 linhas brancas) |
| 15 | 8 | — | `RenderizadorErro` (corpo overflow: requer 9, disponível 8) |
| 6 | — | — | `RenderizadorErro` (insuficiente: cab=3 + barra=4 = 7 > 6) |

---

## Escopo negativo

O executor **não deve** implementar nada além do escopo positivo acima.

```
NÃO implementar barra_de_menus.distribuicao.modo = "horizontal_responsiva".
NÃO implementar quebra multilinha de chips.
NÃO implementar coluna_a_coluna nem linha_a_linha.
NÃO implementar âncoras de chip.
NÃO implementar overflow da barra_de_menus.
NÃO implementar erro de layout da barra quando chips não couberem horizontalmente.
NÃO adicionar segundo elemento ao grupo.
NÃO implementar arranjo horizontal.
NÃO implementar aninhamento de grupos.
NÃO implementar percentual ou fração.
NÃO implementar console real.
NÃO implementar foco.
NÃO implementar seleção.
NÃO implementar navegação por [✥].
NÃO implementar paginação.
NÃO implementar filtros.
NÃO implementar modo verboso.
NÃO criar registry novo de ações.
NÃO criar registry novo de telas.
NÃO alterar contratos.
NÃO alterar ADRs.
NÃO alterar NOMENCLATURA.
NÃO alterar semântica dos chips.
NÃO hardcodar chips no renderer.
NÃO reordenar, truncar, omitir ou completar chips automaticamente.
NÃO reinterpretar corpo.arranjo = "vertical" como ocupação vertical de terminal.
NÃO adicionar campo de altura ao JSON das telas.
NÃO persistir a altura do terminal entre chamadas ou sessões.
NÃO fazer commit.
```

Os itens acima que pertencem à ADR-0014 (barra responsiva, chips, overflow)
ficam explicitamente para o **H-0016**.

---

## Preservações obrigatórias

O handoff exige preservação de:

```
- largura dinâmica existente (shutil.get_terminal_size().columns)
- demo manual (python tela/demo.py)
- fluxo g/d/b/Esc
- [g] abrindo grupo_minimo
- [d] abrindo destino_minimo
- [b] alternando borda
- Esc em tela destino voltando
- Esc na raiz saindo
- Orquestrador (config/telas/orquestrador.json)
- grupo_minimo (config/telas/grupo_minimo.json)
- destino_minimo (config/telas/destino_minimo.json)
- stub_b (config/telas/stub_b.json)
- barra_de_menus declarativa (cada tela declara seus chips)
- corpo.arranjo = "vertical" como ordem/composição dos elementos (ADR-0011)
- ausência de segundo elemento funcional no grupo_minimo
- ausência de layout horizontal
- diagnóstico determinístico e não interativo
- comportamento de renderizar_tela quando altura=None idêntico ao atual
```

---

## Especificação funcional por módulo

### F-1. `tela/demo.py` — ALTERAR

**F-1.1. `main()`**: substituir leitura de `largura` por leitura de
`tamanho_terminal` e derivar `largura` e `altura`.

Antes:
```python
largura = shutil.get_terminal_size(fallback=(80, 24)).columns
```

Depois:
```python
tamanho_terminal = shutil.get_terminal_size(fallback=(80, 24))
largura = tamanho_terminal.columns
altura = tamanho_terminal.lines
```

**F-1.2. `renderizar_estado`**: adicionar `altura=None` e repassar.

Apenas a assinatura e o corpo da chamada interna mudam; nenhum outro
comportamento de `renderizar_estado` é alterado.

**F-1.3. Todas as chamadas a `renderizar_estado` em `main()`**: acrescentar
`altura=altura`. As chamadas ocorrem em dois pontos em `main()` — ambas devem
receber `altura`.

**F-1.4. Nenhuma outra linha de `demo.py` deve ser alterada.**

### F-2. `tela/renderizador.py` — ALTERAR

**F-2.1. Assinatura de `renderizar_tela`**: adicionar `altura: int | None = None`.

**F-2.2. Cálculo de preenchimento**: quando `altura is not None`, antes de
montar a parte `partes` correspondente à barra_de_menus:

1. Calcular `L_cab` contando as linhas do cabeçalho já em `partes[0]`
   (`partes[0].count("\n") + 1` — o cabeçalho é a primeira e única caixa
   antes dos elementos do corpo).
2. Calcular `L_barra` contando as linhas que a barra geraria
   (`len(linhas_barra_preview) + 2` onde `linhas_barra_preview` é o resultado
   de `_linhas_barra(modelo.barra_de_menus)` antes de montar a caixa).
3. Calcular `L_corpo_conteudo` contando as linhas de todos os boxes de
   elementos do corpo já em `partes[1:]`.
4. Verificar `L_cab + L_barra <= altura`; se não, `RenderizadorErro`.
5. Calcular `L_corpo_disponivel = altura - L_cab - L_barra`.
6. Verificar `L_corpo_conteudo <= L_corpo_disponivel`; se não, `RenderizadorErro`.
7. Calcular `L_corpo_fill = L_corpo_disponivel - L_corpo_conteudo`.
8. Se `L_corpo_fill > 0`, inserir `L_corpo_fill` linhas de `" " * total_w`
   entre os elementos do corpo e a barra.

**F-2.3. Quando `altura is None`**: nenhuma verificação, nenhum preenchimento.
O caminho atual é tomado integralmente.

**F-2.4. Contagem de linhas de uma caixa já em `partes`**:

```python
def _contar_linhas(caixa_str):
    """Conta o número de linhas de um bloco multi-linha sem trailing newline."""
    return caixa_str.count("\n") + 1
```

Ou equivalentemente: `len(caixa_str.split("\n"))`.

Uma caixa gerada por `_caixa` com `N` linhas de conteúdo contém `N + 2` linhas
(topo + conteúdos + base), separadas por `"\n"`, sem newline final. Portanto:

```python
L_de_uma_caixa = caixa_str.count("\n") + 1
```

**F-2.5. Nenhuma outra linha de `renderizador.py` deve ser alterada.**

### F-3. `tela/modelo.py` — PROIBIDO

`modelo.py` não é alterado neste ciclo. A propagação de altura não exige
mudança no modelo interno.

Se a análise revelar necessidade de alterar `modelo.py`, parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

### F-4. `tela/loader.py` — PROIBIDO

`loader.py` não é alterado neste ciclo. Nenhum novo campo JSON é introduzido.

Se a análise revelar necessidade de alterar `loader.py`, parar com
`ARCHITECTURE_REVIEW_REQUIRED`.

### F-5. `tela/diagnostico.py` — PROIBIDO

`diagnostico.py` não é alterado. Ele chama `renderizar_tela(modelo)` sem
`largura` nem `altura`; o comportamento com `None` é preservado.

### F-6. `config/` — PROIBIDO

Nenhum JSON de tela é alterado neste ciclo. O preenchimento vertical não é
declaração no JSON.

---

## Arquivos permitidos

Lista explícita e exaustiva. O executor **só pode** criar ou alterar arquivos
desta lista.

### Alterar obrigatório

```
tela/renderizador.py
tela/demo.py
tela/teste_renderizador.py
tela/teste_demo.py
```

### Alterar condicional

```
tela/teste_diagnostico.py
  Somente se testes existentes quebrarem por causa das alterações deste ciclo.
  Expectativa: não precisará ser alterado (diagnóstico usa altura=None).
  Se alterado, registrar justificativa objetiva no relatório IMP-0015.
```

### Criar

```
docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
```

---

## Arquivos proibidos

O executor **não pode** criar nem alterar:

```
docs/adr/
docs/contratos/
docs/NOMENCLATURA.md
docs/INDICE.md
docs/backlog.md
docs/issues.md
docs/handoff/
  (exceto o relatório IMP-0015 que o executor deve criar em docs/relatorios/)
config/
  (nenhum JSON de tela ou de configuração pode ser alterado)
tela/loader.py
tela/modelo.py
tela/diagnostico.py
tela/__init__.py
tela/teste_loader.py
tela/teste_modelo.py
qualquer arquivo não listado como permitido acima
```

---

## Critérios de aceite

O executor deve verificar **todos** os itens abaixo.

### Sobre `renderizar_tela` com `altura` explícita

```
CA-01. renderizar_tela(modelo, largura=42, altura=16) retorna str com
       exatamente 16 linhas: saida.count("\n") == 16.
CA-02. renderizar_tela(modelo, largura=42, altura=24) retorna str com
       exatamente 24 linhas: saida.count("\n") == 24.
CA-03. renderizar_tela(modelo, largura=42, altura=N) onde N == L_cab + L_barra
       + L_corpo_conteudo retorna str sem linhas de preenchimento
       (L_corpo_fill == 0): saida.count("\n") == N.
CA-04. Cada linha não vazia da saída tem exatamente largura chars Python.
CA-05. Linhas de preenchimento têm exatamente largura espaços (" " * largura).
CA-06. Cabeçalho continua no topo: primeira linha da saída começa com "╭ " ou
       "┌ " conforme tipo_borda.
CA-07. barra_de_menus termina no rodapé: a última linha não vazia da saída
       termina com "╯" ou "┘" conforme tipo_borda.
CA-08. Linhas de preenchimento ficam entre o último box de elemento do corpo
       e o primeiro topo da barra_de_menus.
CA-09. renderizar_tela(modelo, largura=42, altura=None) produz saída idêntica
       ao comportamento atual sem nenhuma linha de preenchimento.
CA-10. renderizar_tela(modelo, largura=None) — sem altura — produz saída
       idêntica ao comportamento atual (largura fallback 42, sem fill).
```

### Sobre `RenderizadorErro` em terminal pequeno

```
CA-11. renderizar_tela(modelo, largura=42, altura=6) levanta RenderizadorErro
       quando L_cab + L_barra > 6 (para o Orquestrador: 3+4=7 > 6).
CA-12. renderizar_tela(modelo, largura=42, altura=15) levanta RenderizadorErro
       quando L_corpo_conteudo > L_corpo_disponivel (para o Orquestrador:
       9 > 15-3-4=8).
CA-13. A mensagem de RenderizadorErro é descritiva e não é string vazia.
CA-14. Nenhum truncamento silencioso ocorre: ou a saída é completa com
       altura linhas, ou RenderizadorErro é levantada.
```

### Sobre `demo.py`

```
CA-15. demo.py chama shutil.get_terminal_size() uma vez e deriva .columns e
       .lines na mesma chamada.
CA-16. renderizar_estado aceita largura e altura como argumentos opcionais.
CA-17. Toda chamada a renderizar_estado em main() repassa ambos os valores.
CA-18. corpo.arranjo = "vertical" não é reinterpretado como ocupacao_vertical_terminal.
```

### Sobre o fluxo demonstrável

```
CA-19. Fluxo g/d/b/Esc preservado:
       - "g" continua navegando para grupo_minimo.
       - "d" continua navegando para destino_minimo.
       - "b" continua alternando borda.
       - Esc em grupo_minimo volta ao Orquestrador.
       - Esc em destino_minimo volta ao Orquestrador.
       - Esc no Orquestrador (pilha vazia) sai.
CA-20. Subprocess com input "g\n\x1b\n\x1b\n" encerra com código 0.
CA-21. Stderr vazio no subprocess.
```

### Sobre testes automatizados

```
CA-22. python tela/teste_loader.py     → exit 0, sem [FALHOU], sem traceback.
CA-23. python tela/teste_modelo.py     → exit 0, sem [FALHOU], sem traceback.
CA-24. python tela/teste_renderizador.py → exit 0, sem [FALHOU], sem traceback.
CA-25. python tela/teste_demo.py       → exit 0, sem [FALHOU], sem traceback.
CA-26. python tela/teste_diagnostico.py  → exit 0, sem [FALHOU], sem traceback.
```

### Sobre escopo e rastreabilidade

```
CA-27. tela/loader.py não foi alterado (nenhum diff).
CA-28. tela/modelo.py não foi alterado (nenhum diff).
CA-29. tela/diagnostico.py não foi alterado (nenhum diff).
CA-30. Nenhum JSON em config/ foi alterado.
CA-31. Nenhum contrato em docs/contratos/ foi alterado.
CA-32. Nenhuma ADR em docs/adr/ foi alterada.
CA-33. docs/NOMENCLATURA.md não foi alterado.
CA-34. ADR-0014 não foi implementada: nenhum item de distribuição horizontal
       responsiva da barra_de_menus foi implementado.
CA-35. Nenhum arquivo fora da lista de permitidos foi criado ou alterado.
CA-36. docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
       foi criado pelo executor.
CA-37. Nenhum commit foi realizado pelo executor.
CA-38. Nenhum __pycache__ nem arquivo .pyc deixado no workspace.
```

---

## Testes obrigatórios a exigir no handoff

### Suíte de testes existente

O executor deve executar **todos** os comandos abaixo e confirmar exit 0:

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

### Testes novos a adicionar em `teste_renderizador.py`

O executor deve adicionar os seguintes casos (ou equivalentes verificáveis):

```
- altura explícita maior que o conteúdo atual:
    renderizar_tela(modelo_orq, largura=42, altura=24)
    → saida.count("\n") == 24
    → "│ [Esc] Sair" na saída (barra preservada)

- altura explícita exatamente mínima (sem fill):
    Calcular N_minimo = L_cab + L_corpo_conteudo + L_barra para o Orquestrador
    renderizar_tela(modelo_orq, largura=42, altura=N_minimo)
    → saida.count("\n") == N_minimo
    → L_corpo_fill == 0

- altura insuficiente para corp (corpo overflow):
    Encontrar N_overflow = L_cab + L_barra + L_corpo_conteudo - 1
    renderizar_tela(modelo_orq, largura=42, altura=N_overflow)
    → levanta RenderizadorErro

- altura insuficiente para cabeçalho + barra:
    renderizar_tela(modelo_orq, largura=42, altura=6)
    → levanta RenderizadorErro
    (para o Orquestrador: L_cab=3 + L_barra=4 = 7 > 6)

- altura=None preserva comportamento atual:
    saida_sem = renderizar_tela(modelo_orq, largura=42)
    saida_com = renderizar_tela(modelo_orq, largura=42, altura=None)
    → saida_sem == saida_com

- linhas de preenchimento são exatamente " " * largura:
    saida = renderizar_tela(modelo_orq, largura=42, altura=24)
    # identificar linhas de preenchimento e verificar
    # que cada uma tem exatamente 42 espaços
```

### Testes novos a adicionar em `teste_demo.py`

```
- renderizar_estado aceita altura:
    estado = criar_estado_inicial()
    modelo = ...
    saida = renderizar_estado(estado, modelo, largura=42, altura=24)
    → saida.count("\n") == 24

- renderizar_estado com altura=None igual a sem altura:
    saida_sem = renderizar_estado(estado, modelo, largura=42)
    saida_com = renderizar_estado(estado, modelo, largura=42, altura=None)
    → saida_sem == saida_com

- fluxo g/d/b/Esc preservado com altura explícita (subprocess):
    subprocess com input "g\n\x1b\n\x1b\n"
    → exit 0, stderr vazio, "GRUPO MINIMO" no stdout
```

### Verificação determinística de altura via linha de comando

```bash
python -c "
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela

modelo = construir_modelo(carregar_tela(None, 'orquestrador'))
saida = renderizar_tela(modelo, largura=42, altura=24)
n = saida.count(chr(10))
print('linhas:', n)
assert n == 24, 'FALHOU: esperado 24, obtido {}'.format(n)
print('OK — 24 linhas confirmadas')
"
```

```bash
python -c "
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela, RenderizadorErro

modelo = construir_modelo(carregar_tela(None, 'orquestrador'))
try:
    renderizar_tela(modelo, largura=42, altura=6)
    print('FALHOU: nao levantou RenderizadorErro para altura=6')
except RenderizadorErro as e:
    print('OK — RenderizadorErro para terminal pequeno:', e)
"
```

```bash
python -c "
import sys
sys.dont_write_bytecode = True
from pathlib import Path
sys.path.insert(0, str(Path('.').resolve()))
from tela.loader import carregar_tela
from tela.modelo import construir_modelo
from tela.renderizador import renderizar_tela

modelo = construir_modelo(carregar_tela(None, 'orquestrador'))
saida_sem = renderizar_tela(modelo, largura=42)
saida_com = renderizar_tela(modelo, largura=42, altura=None)
assert saida_sem == saida_com, 'FALHOU: altura=None mudou comportamento'
print('OK — altura=None preserva comportamento atual')
"
```

```bash
python -c "
import sys, os, subprocess
env = {k: v for k, v in os.environ.items() if k != 'COLUMNS'}
p = subprocess.run(
    [sys.executable, 'tela/demo.py'],
    cwd='.',
    input='g\n\x1b\n\x1b\n',
    capture_output=True, text=True, env=env
)
print('exit:', p.returncode)
print('GRUPO MINIMO no stdout:', 'GRUPO MINIMO' in p.stdout)
print('stderr vazio:', p.stderr == '')
assert p.returncode == 0
assert 'GRUPO MINIMO' in p.stdout
assert p.stderr == ''
print('OK — fluxo demonstravel preservado com altura')
"
```

### Cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --name-only
```

---

## Relatório de implementação

O executor deve criar:

```
docs/relatorios/IMP-0015-ocupacao-vertical-janela-terminal-corpo.md
```

O relatório deve conter no mínimo:

1. **Status**: IMPLEMENTATION_COMPLETED ou BLOCKED/ARCHITECTURE_REVIEW_REQUIRED.

2. **Resumo**: o que foi alterado, em qual base (commit/HEAD).

3. **Arquivos criados e alterados**: lista exaustiva com diff descritivo de
   cada arquivo.

4. **Decisões locais**: se qualquer detalhe de implementação não coberto por
   este handoff exigiu decisão local, **o implementador deve bloquear**. Não
   há decisão local permitida neste ciclo. Se o relatório registrar decisão
   local, a sessão deve conter `ARCHITECTURE_REVIEW_REQUIRED`.

5. **Contabilidade de linhas verificada**: L_cab, L_barra, L_corpo_conteudo e
   L_corpo_fill efetivamente calculados para o Orquestrador com largura=42 e
   altura=24.

6. **Testes executados**: saída de cada comando de verificação.

7. **Confirmação de que ADR-0014 não foi implementada**: declaração explícita
   de que nenhum item de barra_de_menus.distribuicao.modo = "horizontal_responsiva"
   foi implementado.

8. **Limitações conhecidas**: comportamento em caso de redimensionamento do
   terminal durante a sessão (a demo lê o tamanho uma vez em `main()`; isso é
   aceitável para este ciclo).

9. **Status final**: PASSOU / FALHOU (com detalhe de cada falha, se houver).

---

## Critérios de bloqueio

O executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

```
- A implementação exigir alterar contrato, ADR ou NOMENCLATURA.
- A propagação de altura exigir mudança no loader, modelo ou diagnostico.
- A ocupação vertical exigir declarar campo novo no JSON das telas.
- For necessário implementar barra_de_menus.distribuicao.modo = "horizontal_responsiva".
- For necessário criar grupo com 2 elementos.
- For necessário reabrir horizontal, aninhamento, percentual/fração ou console real.
- A API atual do renderer ou da demo impedir a propagação de altura sem mudança
  fora dos arquivos permitidos.
- Houver contradição entre este handoff e um contrato ou ADR vigente.
- A contabilidade de linhas levada a cabo revelar ambiguidade não resolvida por
  este handoff.
```

O executor deve parar com `BLOCKED` se:

```
- tela/renderizador.py, tela/demo.py, tela/teste_renderizador.py ou
  tela/teste_demo.py estiverem ausentes.
- Algum critério de aceite não puder ser verificado pelos meios disponíveis.
- Os testes passando no HEAD base quebrarem por motivo não relacionado às
  alterações deste handoff (estado inconsistente pré-existente).
- A função renderizar_tela não tiver a assinatura esperada (modelo, tipo_borda,
  largura) ou a demo não tiver a função renderizar_estado.
```

---

## Instrução explícita ao executor

Leia este handoff integralmente antes de alterar qualquer arquivo.

**Regras obrigatórias:**

1. Não decidir arquitetura nova. Toda decisão não coberta por este handoff ou
   pelos contratos/ADRs citados deve ser reportada como
   `ARCHITECTURE_REVIEW_REQUIRED`.

2. Não alterar contrato, ADR, NOMENCLATURA, INDICE, backlog, issues ou
   qualquer arquivo fora da lista de permitidos.

3. Não resolver lacuna por inferência. Se faltar regra, arquivo permitido ou
   critério verificável, parar com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED`.

4. Não fazer commit.

5. Não implementar nenhum item da ADR-0014 (distribuição horizontal responsiva
   da barra_de_menus). Esses itens pertencem ao H-0016.

6. Criar o relatório `IMP-0015-ocupacao-vertical-janela-terminal-corpo.md`
   antes de encerrar.

7. Verificar que `saida.count("\n") == altura` para toda chamada com `altura`
   fornecida e suficiente.

8. Verificar que `RenderizadorErro` é levantada (não truncamento silencioso)
   quando `altura` for insuficiente.

9. `corpo.arranjo = "vertical"` não deve ser alterado, removido nem
   reinterpretado. Ele continua significando ordem/composição dos elementos
   (ADR-0011).

---

## Saída final esperada

Após a implementação bem-sucedida do H-0015, o sistema deve:

- Produzir, dado `largura=42` e `altura=24`, a saída abaixo para o Orquestrador
  (as 8 linhas de preenchimento são visualmente indistinguíveis de linhas em
  branco entre o último box do corpo e o box Menus):

```
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
╰────────────────────────────────────────╯
╭ ITENS ─────────────────────────────────╮
│ (console)                              │
╰────────────────────────────────────────╯
╭ INFO ──────────────────────────────────╮
╰────────────────────────────────────────╯
╭ NAVEGAR ───────────────────────────────╮
│ [d] Destino                            │
│ [g] Grupo Min.                         │
╰────────────────────────────────────────╯
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
                                          ← linha em branco (42 espaços)
╭ Menus ─────────────────────────────────╮
│ [Esc] Sair                             │
│ [?] Ajuda                              │
╰────────────────────────────────────────╯
```

Total: 24 linhas (`saida.count("\n") == 24`).

- O fluxo `g / d / b / Esc` continua funcional.
- Todos os cinco suítes de teste passam com exit 0 e sem `[FALHOU]`.
- `IMP-0015-ocupacao-vertical-janela-terminal-corpo.md` existe em
  `docs/relatorios/`.
- Nenhum arquivo fora da lista de permitidos foi alterado.
- Nenhum commit foi realizado.
