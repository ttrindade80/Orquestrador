# RELATÓRIO — IMPLEMENTAÇÃO H-0072

## 1. Metadata

```yaml
etapa: IMPLEMENTAR
objeto: H-0072 — capacidade genérica de formatação dos filhos de dois_niveis_por_foco
handoff: docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md
status: IMPLEMENTATION_COMPLETED
```

## 2. Arquivos efetivamente criados

- `tela/carregamento/formato_dois_niveis_por_foco.py` — validador do bloco
  `formato.dois_niveis_por_foco.filho`, análogo em forma a `d23_console.py`.
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco.json` —
  fixture estrutural com 3 consoles `dois_niveis_por_foco` (2 pais cada),
  cobrindo apresentação `texto`, apresentação `tabela` (2 colunas) e os três
  designadores (`decimal_composto`, `alfabetico_maiusculo`, `nenhum`).
- `config/telas/demo/h0072_formatacao_generica_dois_niveis_por_foco_conteudo.json`
  — documento externo compartilhado pelos 3 consoles (campos `titulo`,
  `responsavel`, `prazo`).
- `tela/teste_formato_filho_dois_niveis_por_foco.py` — 29 testes cobrindo os
  18 critérios do §21.
- `demo/teste_demo_h0072_formatacao_generica.py` — 5 testes provando a
  demonstração pelo ponto de entrada real (`demo/demo.py`).

## 3. Arquivos efetivamente alterados

- `tela/carregamento/tela_json.py` — conecta o novo validador para todo
  elemento `console`, independente do escopo D23.
- `tela/modelo.py` — novo campo `ElementoCorpo.formato_filho_dois_niveis`
  (dict|None), extraído de `formato.dois_niveis_por_foco.filho` nos dois
  pontos de construção de elementos (raiz e dentro de grupo).
- `tela/navegacao.py` — acessor puro `formato_filho_dois_niveis(elemento)`;
  navegação, seleção e toroides não foram tocados.
- `tela/renderizacao/conteudo_externo.py` — novas funções
  `_linhas_dois_niveis_formatado_com_mapa` / `_linhas_dois_niveis_formatado`,
  isoladas de `_linhas_apresentacao_hierarquia_com_mapa` (não modificada).
- `tela/renderizacao/console.py` — dispatch condicional: quando o console
  declara `formato_filho_dois_niveis`, usa a nova função; caso contrário
  preserva o caminho vigente (h0055/h0063 intocados).
- `demo/demo.py` — uma entrada nova em `_CATALOGO_CONTEUDO_EXTERNO`.
- `demo/teste_demo_console.py` — extensão autorizada (§4.3): dict `esperado`
  de `teste_catalogo` atualizado com a nova associação.

Não foi necessário alterar `tela/selecao.py`,
`tela/renderizacao/designadores.py`, `tela/renderizacao/matriz_participantes.py`
nem `tela/teste_loader.py`: os mecanismos de designador vigentes
(`_texto_designador`) foram reutilizados sem novo tipo, e os 11 casos de
schema inválido (V-DNF-01..11) foram integralmente cobertos no novo arquivo
de teste dedicado.

## 4. Comportamento entregue

Leitura, validação e aplicação física de `formato.dois_niveis_por_foco.filho`
exclusivamente do elemento `console` do JSON estrutural: tabulação efetiva
(maior valor do intervalo que couber, sobra à direita), designador do filho
(`decimal_composto`, `alfabetico_maiusculo`, `nenhum`, via `_texto_designador`
já vigente), apresentação `texto` (fluxo já vigente) ou `tabela` local
(colunas por `campo` semântico, alinhamento global calculado sobre todos os
filhos do console — inclusive de pais diferentes — espaçamento efetivo no
intervalo declarado, quebra em linhas físicas adicionais preservando um único
item lógico). A ordem física `tabulação → ec → tg → designador → conteúdo` é
aplicada como unidade inteira exclusivamente aos filhos; os pais preservam a
composição já vigente (recuo zero — fora de escopo deste handoff). Nenhuma
geometria é persistida no JSON; tudo é recalculado a cada render (resize
incluso).

## 5. Validações de schema implementadas

V-DNF-01 a V-DNF-11 (§20), com falha fechada via `TelaEstruturaInvalida` e
sem fallback silencioso: intervalos `tabulacao`/`espacamento` (min≤max,
inteiros positivos), `apresentacao` fechada a `texto`/`tabela`, bloco `tabela`
obrigatório sse `apresentacao=="tabela"` (e proibido caso contrário),
`tabela.colunas` não vazio com campo `campo` obrigatório por item,
`designador.tipo` fechado a três valores, e V-DNF-11 (bloco presente exige
`politica_navegacao.tipo=="dois_niveis_por_foco"`).

## 6. Testes executados e resultados

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_formato_filho_dois_niveis_por_foco.py demo/teste_demo_h0072_formatacao_generica.py tela/teste_navegacao.py tela/teste_loader.py demo/teste_demo_console.py -q
→ 216 passed

PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
→ 1415 passed, 1 failed (tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados)
```

Os 29 casos do arquivo dedicado mapeiam os 18 critérios do §21 (1–4:
unidade deslocada e tabulação min/max/intermediária; 5–7: os três
designadores; 8: apresentação texto; 9–12: tabela, alinhamento entre pais
diferentes, espaçamento min/max; 13: sobra à direita; 14–15: quebra
multilinha e continuação sem novo cursor/toggle/identidade; 16: resize;
17: os onze V-DNF, um teste por caso + um caso válido; 18: navegação
preservada — toroides de pais/filhos, seleção exclusiva).

**Falha pré-existente não causal**: `tela/teste_estilo_h0070.py` — teste
`test_filhos_sem_ordinais_cursor_e_indicadores_preservados`, assertiva
`linhas[corrente].index("→") >= 4`, obtido `2`. Evidência de não
causalidade: reproduzida de forma idêntica em `git stash` (árvore de
trabalho anterior a esta implementação, sem nenhum arquivo do H-0072
presente). Nenhum arquivo lido ou alterado por este handoff é exercitado
por esse teste (`tela/estilo.py` e `ControladorTelaEstilo` não constam da
lista nominal §4 nem foram tocados). Não corrigida, por estar fora do
escopo nominal desta implementação.

## 7. Demonstração executada e resultado

`demo/teste_demo_h0072_formatacao_generica.py` carrega o cenário via
`demo._carregar_modelo_por_id` (catálogo → loader → `construir_modelo`) e
renderiza via `processar_comando`/`renderizar_estado` (ponto de entrada
real), confirmando: fluxo entrada declarativa → carregamento → modelo →
renderização → saída física; designador `1.1` e conteúdo textual visíveis;
ausência do placeholder `(console)`; alternância de foco entre os 3
consoles via Tab; alinhamento de coluna idêntico entre filhos de pais
diferentes no console tabular. Resultado: 5/5 testes passando.

## 8. Desvios e interpretações

- `formato.dois_niveis_por_foco.filho.designador` foi validado como schema
  fechado a `{"tipo": ...}` (sem `prefixo`/`sufixo`), por ser exatamente a
  forma literal do exemplo em H-0072 §8 e não haver campo adicional citado
  em §6/§20. Não é uma decisão de schema nova — apenas a leitura mais
  restrita e literal do exemplo já fechado pelo handoff.
- `corpo.distribuicao` (`{"modo":"fracao","valores":[1,1,1]}`) foi
  necessário na fixture nova para 3 elementos visuais concorrentes no eixo
  vertical (ADR-0024/DA-02), preexistente e ortogonal a este handoff.

## 9. Validação manual ainda necessária

Nenhuma: os 18 critérios são verificáveis por asserção sobre a saída física
calculada, sem necessidade de TTY real (§21, confirmado).

## 10. Bloqueios

Nenhum.
\n