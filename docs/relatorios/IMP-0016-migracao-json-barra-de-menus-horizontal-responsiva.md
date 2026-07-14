# IMP-0016 — Migração JSON da barra_de_menus e renderização horizontal responsiva

## Status

```
IMPLEMENTATION_DONE
```

Ciclo H-0016 implementado de forma coesa em um único fluxo, estritamente
dentro do handoff revisado (AUDIT_APPROVED_WITH_NOTES) e do ADR-0014.
Nenhum contrato, ADR ou NOMENCLATURA foi alterado. Nenhum commit foi feito.

- commit-base: `b2eb458 feat: ocupa altura do terminal pelo corpo`
- ADR normativa: `ADR-0014-barra-horizontal-termos-especificos.md`
- handoff: `scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
- auditorias: `RELATORIO_AUDITORIA_H-0016_HANDOFF.md` (AUDIT_REJECTED → revisado)
  e `RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md` (AUDIT_APPROVED_WITH_NOTES)

---

## Resumo

1. Migrados os 4 JSONs ativos de `barra_de_menus.distribuicao` (string
   `"horizontal"`) para o **objeto canônico** declarativo com
   `modo = "horizontal_responsiva"`, `ordem.politica = "declaracao"` e
   âncoras usando os IDs reais dos chips (`chip_esc` primeiro,
   `chip_ajuda` último). Chips preservados byte-a-byte.
2. Substituída a função `_linhas_barra(barra_de_menus)` (empilhamento
   vertical de um chip por linha) por
   `_linhas_barra(barra_de_menus, content_w)`, que implementa o algoritmo
   normativo mínimo do ADR-0014: normalização → validação → âncoras →
   linha única → multilinha (`coluna_a_coluna`/`linha_a_linha`) →
   `erro_layout` determinístico.
3. Compatibilidade transitória mantida: alias string `"horizontal"` e
   `distribuicao` ausente/`None` continuam aceitos (defaults normativos,
   sem âncoras).
4. H-0015 preservado: `l_barra = len(linhas_barra) + 2` permanece correto;
   com a nova barra horizontal em 1 linha, `L_barra` passou de 4 para 3 e
   `n_minimo` de 16 para 15 (largura 42).
5. Testes/snapshots afetados pela mudança física da barra atualizados,
   preservando a intenção; adicionados novos testes H-0016 (classe
   `TestLinhasBarra`) e asserções em loader/modelo.

---

## Arquivos alterados/criados

Implementação (fonte):

```
scripts/config/telas/orquestrador.json          (migrado)
scripts/config/telas/grupo_minimo.json          (migrado)
scripts/config/telas/destino_minimo.json        (migrado)
scripts/config/telas/stub_b.json                (migrado)
scripts/tela/renderizador.py                    (_linhas_barra + auxiliares + constante)
```

Testes/snapshots:

```
scripts/tela/teste_renderizador.py              (snapshots + TestLinhasBarra + contabilidade)
scripts/tela/teste_demo.py                      (snapshots 80/42 + altura mínima)
scripts/tela/teste_diagnostico.py               (snapshot 42)
scripts/tela/teste_loader.py                    (asserções distribuicao objeto)
scripts/tela/teste_modelo.py                    (asserções distribuicao objeto)
```

Relatório:

```
scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md  (criado)
```

Observações de escopo (alinhadas a PR-N-02):

- `scripts/tela/loader.py` e `scripts/tela/modelo.py` (fonte) **não foram
  alterados** — o dict bruto já preserva o objeto canônico sem
  validação/transformação (essa responsabilidade permanece no renderer).
  Apenas seus testes ganharam asserções de exposição.
- `scripts/tela/demo.py` e `scripts/tela/diagnostico.py` (fonte) **não
  foram alterados** — a renderização é delegada ao renderer.

---

## JSONs migrados

| Arquivo | modo | ordem.politica | ancora primeiro | ancora ultimo | chips (ordem preservada) |
|---|---|---|---|---|---|
| `orquestrador.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` | `chip_esc` (Esc/Sair), `chip_ajuda` (?/Ajuda) |
| `grupo_minimo.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `destino_minimo.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |
| `stub_b.json` | `horizontal_responsiva` | `declaracao` | `["chip_esc"]` | `["chip_ajuda"]` | `chip_esc` (Esc/Voltar), `chip_ajuda` (?/Ajuda) |

Verificação de preservação: os objetos `chips[]` são **idênticos** entre
`HEAD` (pré-migração) e a versão migrada (comparados via
`json.dumps`) — nenhum `id`, `tecla`, `texto`, `acao`,
`regra_existencia`, `regra_ativo`, `forma_exibicao` foi adicionado,
removido, reordenado ou alterado. Apenas `distribuicao` mudou.

Não foi usado `declaracao_validada` (valor rejeitado na auditoria anterior
e removido do handoff revisado).

---

## Implementação realizada

### `_linhas_barra(barra_de_menus, content_w)` (renderizador.py)

Nova assinatura com `content_w` (largura disponível para conteúdo dentro
da caixa, `total_w - 3`). Fluxo:

1. `chips` ausente/vazio ou `barra_de_menus` não-dict → retorna `[]`.
2. `_normalizar_distribuicao`: `None`/ausente ou string `"horizontal"` →
   constante default (`_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`,
   sem âncoras); objeto dict → usado como declarado; demais →
   `RenderizadorErro`.
3. `_validar_distribuicao`: validações defensivas determinísticas (ver
   seção "Validações implementadas").
4. `_validar_ancoras`: valida `primeiro`/`ultimo` contra posições
   iniciais/finais de `chips[]`; id inexistente ou posição errada →
   `RenderizadorErro`. O renderer **não reordena** — a violação é erro.
5. Tenta **linha única** (`"[{tecla}] {texto}"` unidos por
   `vao_entre_chips.minimo` espaços); se `len <= content_w`, retorna.
6. Caso contrário, itera **multilinha** de `2` até `linhas.maximo`,
   aplicando `preenchimento_multilinha` (`coluna_a_coluna` ou
   `linha_a_linha`); retorna na primeira configuração que encaixar.
7. Nenhuma configuração cabe → `RenderizadorErro` com `"erro_layout"` na
   mensagem (nunca omite/trunca/reordena).

### Modos de preenchimento multilinha

- `coluna_a_coluna` (obrigatório, padrão): preenche coluna por coluna;
  largura de cada coluna = maior chip da coluna; colunas separadas por
  `vao_entre_colunas.minimo`. Exemplo com `[A,B,C,D,E]` e `K=2`:
  linha1 = `A  C  E`, linha2 = `B  D` (idêntico ao exemplo do handoff).
- `linha_a_linha` (implementado, pois é simples e está listado em
  `preenchimentos_multilinha_suportados`): preenche linha por linha;
  cada linha recebe até `ceil(N/K)` chips consecutivos. Exemplo com
  `[A,B,C,D,E]` e `K=2`: linha1 = `A B C`, linha2 = `D E`.

Ambos foram implementados deterministicamente (sem rejeição).

### Constantes/auxiliares adicionados

- `_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`: defaults normativos do
  ADR-0014 para o alias string e para `distribuicao` ausente (com
  `ancoras: {}`).
- `_PREENCHIMENTOS_MULTILINHA_VALIDOS`: tupla
  `("coluna_a_coluna", "linha_a_linha")`.
- Helpers: `_texto_chip_barra`, `_normalizar_distribuicao`,
  `_eh_int_nao_bool`, `_validar_distribuicao`, `_validar_ancoras`,
  `_montar_coluna_a_coluna`, `_montar_linha_a_linha`.

### Integração com `renderizar_tela`

A chamada `_linhas_barra(modelo.barra_de_menus)` foi atualizada para
`_linhas_barra(modelo.barra_de_menus, content_w)`. O invariante
`l_barra = len(linhas_barra) + 2` permanece correto. Nenhum outro trecho
de `renderizar_tela` foi alterado (assinatura, `altura`, caixas,
grupo estrutural, `_caixa_de_elemento` etc. preservados).

---

## Validações implementadas

Erros determinísticos via `RenderizadorErro` (todos com mensagem
descritiva):

- modo desconhecido (qualquer valor diferente de `"horizontal_responsiva"`,
  inclusive alias string diferente de `"horizontal"` e tipos inválidos);
- **PR-M-01**: `ordem.politica` diferente de `"declaracao"` (ex.:
  `"grupos_declarados"` ou valor desconhecido);
- **PR-M-02**: `preenchimento_multilinha` fora de
  `("coluna_a_coluna", "linha_a_linha")` ou fora de
  `preenchimentos_multilinha_suportados`;
- **PR-M-03**: `linhas.minimo`/`linhas.maximo` não-int (excluindo bool),
  `< 1`, ou `maximo < minimo`;
- **PR-M-04**: `overflow.quando_nao_couber` diferente de `"erro_layout"`;
  flags `nao_omitir_chips`/`nao_truncar_texto`/`nao_reordenar` não
  booleanas;
- âncora `primeiro`/`ultimo` com id inexistente em `chips[]`;
- âncora `primeiro`/`ultimo` em posição errada;
- `erro_layout`: chips não cabem em nenhuma configuração até
  `linhas.maximo`.

Observação `_eh_int_nao_bool`: `isinstance(True, int)` é `True` em Python,
portanto a validação exclui `bool` ao checar inteiros (flags `true`/`false`
do JSON viram `bool`).

---

## Testes/snapshots atualizados

Snapshots literais atualizados para refletir a barra horizontal (a única
mudança física é a seção `Menus`, agora em 1 linha horizontal com os 2
chips; o restante do layout é inalterado):

- `teste_renderizador.py`: `_EXPECTED_ORQUESTRADOR`,
  `_EXPECTED_ORQUESTRADOR_RETA`; contabilidade `teste_altura_explicita`
  (`l_barra` 4→3, `n_minimo` 16→15, `l_corpo_fill_24` 8→9, `n_overflow`
  15→14, terminal pequeno altura 6→5, índices de fill no CA-08 ajustados
  de `linha 20 = ╭ Menus` para `linha 20 = fill` e `linha 21 = ╭ Menus`).
- `teste_demo.py`: `_EXPECTED_CURVA`, `_EXPECTED_RETA`,
  `_EXPECTED_DIAGNOSTICO_CURVA_42`, `_EXPECTED_DESTINO_MINIMO_CURVA_80`,
  `_EXPECTED_DESTINO_MINIMO_RETA_80`, `_EXPECTED_GRUPO_MINIMO_CURVA_80`,
  `_EXPECTED_GRUPO_MINIMO_RETA_80`; altura mínima 16→15 em
  `teste_renderizar_estado_altura`.
- `teste_diagnostico.py`: `_EXPECTED_ORQUESTRADOR` (seção `Menus`).

A intenção de cada teste foi preservada; apenas o valor esperado foi
espelhado à saída horizontal correta (regra técnica do handoff).

---

## Tratamento das notas da auditoria pós-revisão

### PR-M-01 — `ordem.politica` desconhecida/não suportada

**Tratada.** `_validar_distribuicao` rejeita qualquer `politica`
diferente de `"declaracao"` com `RenderizadorErro` determinístico
(inclusive `"grupos_declarados"`, que existe na ADR-0014 mas não é
implementado neste ciclo). Decisão local, sem nova norma, seguindo o
padrão defensivo de `modo` desconhecido. Coberta por teste
(`test_politica_desconhecida_erro`).

### PR-M-02 — `preenchimento_multilinha` desconhecido

**Tratada.** `_validar_distribuicao` rejeita valor fora de
`("coluna_a_coluna", "linha_a_linha")` e valor fora de
`preenchimentos_multilinha_suportados`. Coberta por teste
(`test_preenchimento_multilinha_desconhecido_erro`).

### PR-M-03 — limites inválidos em `linhas.minimo`/`linhas.maximo`

**Tratada.** `_validar_distribuicao` rejeita `minimo`/`maximo`
não-inteiros (excluindo `bool`), `< 1`, e `maximo < minimo`. Coberta por
testes (`test_linhas_minimo_invalido_erro`,
`test_linhas_maximo_menor_que_minimo_erro`).

### PR-M-04 — `overflow.quando_nao_couber` desconhecido / flags não booleanas

**Tratada.** `_validar_distribuicao` rejeita `quando_nao_couber`
diferente de `"erro_layout"` e qualquer flag de overflow não
booleana. Coberta por testes (`test_overflow_desconhecido_erro`,
`test_overflow_flag_nao_booleana_erro`).

### PR-N-01 — `preenchimentos_multilinha_suportados` como extensão de campo

**Tratada como orientação defensiva, sem alteração normativa.** O campo
foi mantido nos JSONs migrados exatamente como definido no handoff
revisado (lista `["coluna_a_coluna", "linha_a_linha"]`), e o renderer o
consome como metadado (valida que `preenchimento_multilinha` pertence à
lista suportada). **Não foi transformado em alteração normativa fora do
handoff** — nenhum contrato ou ADR foi modificado. O campo permanece
registrado para revisão futura de ADR/contrato, conforme a nota.

### PR-N-02 — `loader.py` e `modelo.py` na lista de permitidos

**Tratada.** Os arquivos de fonte `loader.py` e `modelo.py` **não foram
alterados** — o dict bruto já preserva o objeto canônico como declaração
inerte, e a validação/transformação de `distribuicao` permanece
responsabilidade exclusiva do renderer (alinhado ao escopo negativo do
handoff). Apenas `teste_loader.py` e `teste_modelo.py` ganharam asserções
de que a distribuição é exposta como objeto canônico.

---

## Decisões locais

1. **`linha_a_linha` implementado (não rejeitado).** O handoff autoriza
   implementar ou rejeitar deterministicamente; como ambos os modos
   estão listados em `preenchimentos_multilinha_suportados` e a
   implementação é simples, ambos foram implementados e selecionados
   pelo campo `preenchimento_multilinha` (padrão `coluna_a_coluna`).
2. **Organização dos testes H-0016.** O handoff sugere uma classe
   `TestLinhasBarra`; como a suíte `teste_renderizador.py` usa o padrão
   diagnóstico procedural (`_registrar`) e não `unittest`, a classe foi
   implementada com métodos que delegam ao `_registrar` e um
   `run_all()` acionado por `main()`. Isso honra o nome `TestLinhasBarra`
   e a cobertura exigida, mantendo a infraestrutura existente.
3. **Âncoras com listas.** A validação trata `primeiro`/`ultimo` como
   listas de ids (forma canônica do ADR-0014), validando posições
   iniciais/finais na ordem declarada. Os JSONs ativos usam listas de 1
   elemento; a implementação é genérica para listas maiores.
4. **Sem importações novas no renderer.** Para evitar importar `math`,
   usou-se divisão inteira `(n + k - 1) // k` no lugar de
   `math.ceil`. Apenas biblioteca padrão; nenhuma proibição de import do
   teste de renderer foi violada.
5. **Não houve necessidade de `ARCHITECTURE_REVIEW_REQUIRED`.** Nenhum
   arquivo proibido precisou ser alterado; nenhum critério de bloqueio
   do handoff foi disparado.

---

## Testes executados

Comandos executados a partir de `scripts/`:

```bash
cd scripts
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

Resultados (códigos de saída):

```
tela/teste_loader.py:        exit 0
tela/teste_modelo.py:        exit 0
tela/teste_renderizador.py:  exit 0
tela/teste_demo.py:          exit 0
tela/teste_diagnostico.py:   exit 0
```

---

## Resultados

Todas as 5 suítes passam (451 verificações no total):

```
tela/teste_loader.py:        79/79   (12 novas H-0016)
tela/teste_modelo.py:        56/56   (3 novas H-0016)
tela/teste_renderizador.py:  171/171 (38 novas H-0016 em TestLinhasBarra + snapshots/contabilidade)
tela/teste_demo.py:          117/117 (snapshots atualizados)
tela/teste_diagnostico.py:   28/28   (snapshot atualizado)
```

Casos H-0016 cobertos em `TestLinhasBarra`: linha única quando cabe;
multilinha quando linha única não cabe; `erro_layout`; alias string
`"horizontal"`; `distribuicao` ausente; `chips` vazia; âncoras
primeiro/último válidas/violadas/id inexistente; ordem preservada;
chips declarados aparecem exatamente uma vez; chips do `lancador` não
entram na barra; `coluna_a_coluna`; `linha_a_linha`; modo desconhecido;
PR-M-01 a PR-M-04 (validações defensivas); `renderizar_tela` com
canônico; preservação da altura H-0015; altura mínima (15) com barra
horizontal; fluxo `g/d/b/Esc` preservado.

Cobertura cruzada: `teste_loader.py` verifica que os 4 JSONs migrados
carregam e expõem `distribuicao` como objeto com `modo`/`politica`/
âncoras corretas; `teste_modelo.py` verifica que o modelo expõe
`distribuicao` como objeto.

---

## Limitações conhecidas

1. **`grupos_declarados` não implementado.** Valor normativo da
   ADR-0014 para `ordem.politica`, mas fora de escopo do H-0016. É
   rejeitado deterministicamente (`RenderizadorErro`) quando presente,
   seguindo PR-M-01. Não há testes com `grupos_declarados` porque ele
   não existe nos JSONs ativos nem é implementado.
2. **`linhas.maximo > 2` não é caso testado adicionalmente.** O handoff
   proíbe tratar `linhas.maximo > 2` como caso testado adicional; a
   implementação itera de 2 até `maximo` genericamente, mas os JSONs
   ativos usam `maximo = 2`.
3. **Alinhamento diferente de `"esquerda"` não implementado.** Apenas
   `"esquerda"` é suportado neste ciclo (alinhamento natural de
   `str.ljust`/`rstrip`); `"centro"`/`"direita"`/`"justificado"` não são
   tratados (fora de escopo explícito do handoff). O campo
   `alinhamento_linhas` é lido mas não força outro alinhamento.
4. **`preenchimentos_multilinha_suportados` é extensão (PR-N-01).**
   Permanece como campo nos JSONs consumido pelo renderer; revisão
   futura de ADR/contrato pode formalizá-lo ou internalizá-lo.
5. **`vao_entre_chips`/`vao_entre_colunas` usam o `minimo`.** A
   responsividade usa os mínimos normativos para maximizar o encaixe
   (preferir menor número de linhas), coerente com o handoff. Os
   `maximo` dos vãos são preservados como declaração, mas não
   influenciam o layout neste ciclo.

---

## Confirmação de fora de escopo

Confirmo explicitamente que **não** foram implementados:

```
corpo.arranjo horizontal
composição horizontal do corpo
distribuição de altura entre elementos do corpo
correção do preenchimento vertical do H-0015
console real
paginação
filtros
seleção
registry novo de ações
registry novo de telas
```

Adicionalmente, não foram implementados (fora de escopo absoluto do
handoff): grupo com 2 elementos, aninhamento, percentual/fração, foco
entre elementos, navegação por `[✥]`, modo verboso, mudança semântica de
`Esc`/`g`/`d`/`b`/`Enter`, mudança na navegação do lancador, alteração
de contratos/ADRs/NOMENCLATURA/INDICE, hardcoding de lista canônica
global de chips, truncamento de texto de chip, omissão de chip para
caber, reordenação heurística de chips, fallback vertical
um-chip-por-linha, uso de regras do lancador como regras da
`barra_de_menus`, e inclusão de chips do lancador na `barra_de_menus`.

Nenhum arquivo proibido foi alterado. Nenhum commit foi feito.
