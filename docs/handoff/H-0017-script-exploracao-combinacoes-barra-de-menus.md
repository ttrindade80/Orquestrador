# H-0017 — Script de exploração de combinações da barra_de_menus

```
status:        HANDOFF_READY
ciclo:         H-0017
título:        Script de exploração de combinações da barra_de_menus
depende-de:    H-0016 (implementado, IMP-0016, QA aprovado — commit ab5ad68)
commit-base:   ab5ad68  feat: renderiza barra de menus horizontal responsiva
data:          2026-07-09
autor-handoff: Claude Code
executor:      OpenCode / GLM
```

---

## Rastreabilidade

| Item | Referência |
|------|-----------|
| ADR normativo | `scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` |
| Contrato barra de menus | `scripts/docs/contratos/contrato_barra_de_menus.md` (seção 17) |
| Contrato JSON barra de menus | `scripts/docs/contratos/contrato_json_barra_de_menus.md` |
| Contrato chip | `scripts/docs/contratos/contrato_chip.md` |
| Contrato tela JSON | `scripts/docs/contratos/contrato_tela_json.md` |
| Contrato de processo | `scripts/docs/contratos/contrato_processo_desenvolvimento.md` |
| H-0016 (base implementado) | `scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` |
| IMP-0016 (base) | `scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md` |
| QA H-0016 (aprovado) | `scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md` |
| Auditoria H-0016 pós-revisão | `scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md` |
| Relatório a gerar | `scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md` |

---

## Status

```
HANDOFF_READY
```

---

## Contexto operacional temporário

O Codex está indisponível. O fluxo vigente neste ciclo é:

```
Claude Code      → gera handoff (este arquivo)
OpenCode / GLM   → auditoria/QA do handoff + implementação do código
Claude Code      → QA final da implementação
```

O executor **não decide arquitetura**. Toda decisão de design está registrada
no ADR-0014 e nos contratos. Se qualquer item normativo estiver ausente ou
conflitante, bloquear com `ARCHITECTURE_REVIEW_REQUIRED` antes de implementar.

---

## Contexto técnico — estado pós H-0016

O ciclo H-0016 implementou integralmente a renderização horizontal responsiva da
`barra_de_menus` (ADR-0014). Estado atual do código relevante para este ciclo:

- **`renderizador.py`** expõe `_linhas_barra(barra_de_menus, content_w)`: aceita
  um dict de `barra_de_menus` e a largura de conteúdo disponível; executa o
  algoritmo completo (normalização → validação defensiva → âncoras → linha única
  → multilinha → `erro_layout`). Levanta `RenderizadorErro` em todos os casos de
  erro determinístico.
- **Modos suportados**: `coluna_a_coluna` (padrão) e `linha_a_linha` — ambos
  implementados deterministicamente.
- **Validações defensivas**: modo desconhecido, `ordem.politica` inválida,
  `preenchimento_multilinha` inválido, `linhas.minimo`/`maximo` inválidos,
  `overflow.quando_nao_couber` inválido, flags de overflow não booleanas.
- **Âncoras**: `primeiro`/`ultimo` validadas contra posições iniciais/finais de
  `chips[]`; id inexistente ou posição errada → `RenderizadorErro`.
- **Compatibilidade transitória**: alias string `"horizontal"` e `distribuicao`
  ausente/`None` → defaults normativos sem âncoras.
- **Contagem de verificações** (451/451 em 5 suítes): `teste_loader.py`,
  `teste_modelo.py`, `teste_renderizador.py`, `teste_demo.py`,
  `teste_diagnostico.py` — todos passando.
- **`_DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT`**: constante Python com os
  defaults normativos do ADR-0014 (disponível para uso direto no script de
  exploração).
- **`RenderizadorErro`**: classe de exceção única para todos os erros de
  renderização.

O script H-0017 deve **usar** o comportamento implementado no H-0016 sem
alterá-lo. Apenas exercita o renderer com combinações sintéticas geradas em
memória.

---

## Relação com H-0016

H-0017 é um ciclo **de exploração/validação**, não de alteração normativa.

- H-0016 implementou o renderer; H-0017 cria uma ferramenta para exercitá-lo
  sistematicamente.
- H-0017 **não altera** a semântica do renderer.
- Se o script revelar bug no renderer, o implementador deve **registrar** o bug
  no relatório IMP-0017 e, se a correção exigir mudança de comportamento além de
  um ajuste local mínimo, bloquear com `ARCHITECTURE_REVIEW_REQUIRED`.
- Correções pequenas e localizadas no script ou nos seus testes são permitidas.
- Correções no `renderizador.py` **só** são autorizadas se o handoff especificar
  claramente que é um ajuste de acesso (ex.: expor helper já existente) sem
  alterar o comportamento aprovado no H-0016.

---

## Objetivo

Criar um script de exploração/validação das combinações de renderização da
`barra_de_menus`, que:

1. Gere cenários sintéticos de `barra_de_menus` em memória.
2. Exercite `_linhas_barra` (ou a menor interface pública necessária) do
   renderer já implementado no H-0016, variando sistematicamente as combinações.
3. Verifique invariantes da renderização para cada cenário.
4. Produza saída textual determinística em modo resumo e detalhado.
5. Classifique resultados como OK, erro esperado ou erro inesperado.
6. Retorne exit codes determinísticos.
7. Sirva como ferramenta diagnóstica/exploratória, sem entrar no fluxo normal
   de execução da aplicação.

---

## Leitura obrigatória antes de implementar

O executor deve ler na íntegra antes de tocar qualquer arquivo:

1. `scripts/docs/handoff/H-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
2. `scripts/docs/relatorios/IMP-0016-migracao-json-barra-de-menus-horizontal-responsiva.md`
3. `scripts/docs/relatorios/RELATORIO_QA_H-0016_MIGRACAO_JSON_BARRA_DE_MENUS_HORIZONTAL_RESPONSIVA.md`
4. `scripts/docs/relatorios/RELATORIO_AUDITORIA_H-0016_HANDOFF_POS_REVISAO.md`
5. `scripts/docs/adr/ADR-0014-barra-horizontal-termos-especificos.md`
6. `scripts/docs/contratos/contrato_barra_de_menus.md` (seção 17)
7. `scripts/docs/contratos/contrato_json_barra_de_menus.md`
8. `scripts/docs/contratos/contrato_chip.md`
9. `scripts/docs/contratos/contrato_tela_json.md`
10. `scripts/docs/contratos/contrato_processo_desenvolvimento.md`
11. `scripts/docs/NOMENCLATURA.md`
12. `scripts/tela/renderizador.py` (integralmente)
13. `scripts/tela/teste_renderizador.py` (integralmente — padrão de teste)
14. `scripts/tela/teste_loader.py` (padrão de infraestrutura de teste)
15. `scripts/tela/teste_modelo.py` (padrão de infraestrutura de teste)
16. `scripts/tela/teste_demo.py` (padrão de infraestrutura de teste)
17. `scripts/tela/teste_diagnostico.py` (padrão de infraestrutura de teste)
18. `scripts/config/telas/orquestrador.json`
19. `scripts/config/telas/grupo_minimo.json`
20. `scripts/config/telas/destino_minimo.json`
21. `scripts/config/telas/stub_b.json`
22. Este handoff até o final.

---

## Script alvo

### Caminho

```
scripts/tela/explorar_barra_de_menus.py
```

### Justificativa

O script exercita diretamente `_linhas_barra` do renderer e usa estruturas de
`barra_de_menus` (chips, distribuição) idênticas às processadas pelo renderer.
O diretório `scripts/tela/` é o local natural por coesão com `renderizador.py`
e com os demais arquivos de teste e diagnóstico da camada de renderização.

Se o executor encontrar, ao inspecionar o projeto, diretório mais adequado para
ferramentas auxiliares (ex.: `scripts/ferramentas/`), pode escolher outro
caminho, mas deve justificar no IMP-0017 e manter o escopo mínimo. A preferência
declarada pelo handoff é `scripts/tela/explorar_barra_de_menus.py`.

### Interface com o renderer

O script deve usar:

```python
from tela.renderizador import _linhas_barra, RenderizadorErro
```

Se `_linhas_barra` não for suficiente para exercitar todos os cenários sem
duplicar lógica do renderer, o implementador pode, excepcionalmente, expor
um helper já existente de forma segura (sem alterar comportamento). Nesse caso,
o escopo de alteração em `renderizador.py` deve ser mínimo e documentado no
IMP-0017. A preferência é **não alterar** `renderizador.py`.

---

## Requisitos funcionais

O script deve gerar cenários sintéticos de `barra_de_menus` em memória e
renderizá-los usando `_linhas_barra` do renderer. Cada cenário é um dict
`barra_de_menus` com `chips[]` e `distribuicao` construídos sinteticamente, mais
um `content_w` que representa a largura disponível.

### Variações obrigatórias na matriz

**1. Quantidade de chips:**
```
1, 2, 3, 4, 5, 6, 8, 10, 12
```

**2. Comprimento dos textos dos chips:**
- curto (ex.: "Ok", "Ir");
- médio (ex.: "Sair", "Ajuda", "Voltar");
- longo dentro do limite aceito pelo renderer/contrato (ex.: "Configurações", "Selecionar");
- misto (combinação de curtos e longos na mesma lista de chips).

**3. Largura disponível (`content_w`):**
- muito estreita: ≤ 20 — esperando `erro_layout` em muitos casos;
- estreita: 25–40 — forçando multilinha;
- média: 50–70 — permitindo duas linhas ou linha única em alguns casos;
- larga: ≥ 80 — permitindo linha única na maioria dos casos.

**4. `linhas.maximo`:**
```
1, 2, 3
```

**5. `preenchimento_multilinha`:**
```
coluna_a_coluna, linha_a_linha
```

**6. Espaçamentos:**
- mínimos: `vao_entre_chips = 2`, `vao_entre_colunas = 2`;
- intermediários: `vao_entre_chips = 3`, `vao_entre_colunas = 4`;
- máximos: `vao_entre_chips = 6`, `vao_entre_colunas = 8`.

**7. Âncoras:**
- âncora válida: `primeiro` e `ultimo` corretos para os chips declarados;
- sem âncoras: `ancoras: {}` ou `ancoras` ausente;
- âncora inexistente: id declarado em âncora não existe em `chips[]`;
- âncora em posição errada: id existe em `chips[]` mas na posição errada.

**8. Overflow:**
- caso que cabe: `content_w` suficiente para todos os chips;
- caso que não cabe: `content_w` pequeno demais para qualquer configuração;
- caso que deve gerar `erro_layout` determinístico.

---

## Parâmetros de linha de comando

O script deve aceitar os seguintes parâmetros via `argparse` (ou equivalente
de biblioteca padrão). Todos são opcionais — sem argumentos, a matriz padrão
é executada.

### Parâmetros obrigatórios mínimos

```
--larguras
    Lista de content_w (larguras de conteúdo) a testar, separadas por vírgula.
    Exemplo: --larguras 20,30,40,60,80,120
    Default: matriz padrão do script.

--chips
    Lista de quantidades de chips a testar, separadas por vírgula.
    Exemplo: --chips 1,2,3,4,5,6,8,10,12
    Default: matriz padrão do script.

--linhas-max
    Lista de valores de linhas.maximo a testar, separadas por vírgula.
    Exemplo: --linhas-max 1,2,3
    Default: matriz padrão do script.

--preenchimentos
    Lista de preenchimentos a testar, separados por vírgula.
    Valores aceitos: coluna_a_coluna, linha_a_linha
    Exemplo: --preenchimentos coluna_a_coluna,linha_a_linha
    Default: matriz padrão do script.

--modo-saida
    Formato de saída.
    Valores: resumo, detalhado
    Default: detalhado
    Em modo "resumo", imprime apenas totais e agrupamentos.
    Em modo "detalhado", imprime cada cenário com representação completa.

--mostrar-ok
    Flag (sem valor). Quando presente, inclui cenários que renderizaram
    corretamente na saída. Em modo detalhado, útil para inspeção visual.
    Em modo resumo, não afeta os totais.

--mostrar-erros
    Flag (sem valor). Quando presente, inclui cenários que geraram erro
    (esperado ou inesperado) na saída.

--limite-casos
    Limita a quantidade total de cenários executados.
    Útil para depuração rápida.
    Exemplo: --limite-casos 20
    Default: sem limite (executa toda a matriz).
```

### Semântica dos flags `--mostrar-ok` e `--mostrar-erros`

Quando nenhum dos dois flags for passado, o script executa toda a matriz e
exibe apenas o resumo final (totais e agrupamentos). Quando `--mostrar-ok`
for passado, exibe os cenários OK no modo detalhado selecionado. Quando
`--mostrar-erros` for passado, exibe os cenários de erro. Ambos podem ser
passados simultaneamente.

### Parâmetros adicionais

O handoff autoriza que o implementador acrescente parâmetros simples se forem
úteis para a exploração (ex.: `--texto-perfil` para selecionar perfis de texto,
`--espacamento-perfil` para selecionar perfis de espaçamento). Esses parâmetros
adicionais são opcionais e não devem transformar o ciclo em CLI complexa. O
implementador deve documentar os parâmetros adicionais no IMP-0017.

---

## Saída esperada do script

### Modo detalhado — por cenário

Para cada cenário a ser exibido (conforme flags), a saída deve conter:

```
--- Cenário <id> ---
chips:         <quantidade>
content_w:     <valor>
linhas.maximo: <valor>
preenchimento: <coluna_a_coluna|linha_a_linha>
espacamento:   <perfil>
texto_perfil:  <curto|medio|longo|misto>
ancoras:       <valida|sem_ancora|inexistente|posicao_errada>
resultado:     OK | ERRO_ESPERADO | ERRO_INESPERADO

[se OK]
  linhas_fisicas:   <n>
  contagem_chips:   <n encontrados>
  chips_corretos:   <True|False>
  ordem_preservada: <True|False>
  largura_maxima:   <largura da linha mais longa>
  representacao:
    <linha 1 da barra renderizada>
    <linha 2 da barra renderizada, se multilinha>
    ...

[se ERRO_ESPERADO ou ERRO_INESPERADO]
  tipo_erro:     <classe do erro>
  mensagem:      <mensagem resumida>
  era_esperado:  <True|False>
```

### Modo resumo — totais e agrupamentos

```
=== RESUMO DA EXPLORAÇÃO ===
Total de cenários executados:   <n>
OK:                             <n>
Erro esperado:                  <n>
Erro inesperado:                <n>
Violações de invariante:        <n>

Por preenchimento_multilinha:
  coluna_a_coluna: OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>
  linha_a_linha:   OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>

Por linhas.maximo:
  1: OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>
  2: OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>
  3: OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>

Por largura (content_w):
  <faixa ou valor>: OK=<n> ERRO_ESP=<n> ERRO_INESP=<n>
  ...
```

O formato exato do resumo pode ser adaptado pelo implementador para legibilidade,
mas deve conter todos os campos acima. A saída deve ser determinística: mesmos
parâmetros → mesma saída.

---

## Exit codes

```
0   — todos os cenários produziram resultado esperado (OK ou erro esperado
      corretamente classificado); nenhuma violação de invariante detectada.
1   — houve erro inesperado, violação de invariante, ou divergência de contagem
      em pelo menos um cenário.
2   — erro de uso: parâmetro inválido, valor fora do conjunto aceito,
      combinação impossível de parâmetros.
```

Definição de "resultado esperado":
- Cenário projetado para caber → OK é esperado.
- Cenário projetado para gerar `erro_layout` (overflow) → `RenderizadorErro`
  com "erro_layout" é esperado.
- Cenário com âncora inválida → `RenderizadorErro` com mensagem de âncora é
  esperado.
- `RenderizadorErro` em cenário projetado para caber → erro inesperado → exit 1.
- Violação de invariante em cenário OK → exit 1.

---

## Invariantes que o script deve verificar

Para todo cenário com resultado OK (sem erro):

```
1.  Cada chip declarado aparece exatamente uma vez na saída.
2.  Nenhum chip ausente é inventado (não aparecem ids não declarados).
3.  Nenhum chip declarado é omitido (todos os ids declarados aparecem).
4.  A ordem declarada é preservada (sequência na saída = sequência em chips[]).
5.  O texto de cada chip não está truncado (texto original presente integralmente).
6.  A quantidade de linhas físicas da barra ≤ linhas.maximo declarado.
7.  A largura de cada linha da barra ≤ content_w declarado.
8.  Chips do lancador não aparecem na saída (apenas chips de barra_de_menus).
9.  A renderização não usa fallback vertical um-chip-por-linha quando o modo
    declarado é horizontal_responsiva, salvo cenário com exatamente 1 chip
    (onde linha única e um-chip-por-linha são equivalentes).
10. Para linha única (1 linha física), todos os chips aparecem na mesma linha.
11. Para multilinha coluna_a_coluna, o padrão de distribuição coluna por coluna
    é observável: os chips preenchem as colunas de cima para baixo antes de
    passar para a próxima coluna.
12. Para multilinha linha_a_linha, o padrão de distribuição linha por linha é
    observável: os chips preenchem as linhas da esquerda para a direita, na
    sequência declarada.
```

Para cenários de erro esperado:

```
1.  O erro deve ser determinístico: mesmo cenário → mesmo tipo de erro.
2.  O erro deve estar associado a overflow (erro_layout), âncora inválida, ou
    parâmetro inválido do cenário.
3.  O script não deve encerrar a matriz inteira ao primeiro erro esperado —
    deve registrar e continuar.
4.  A mensagem de erro de overflow deve conter "erro_layout".
5.  A mensagem de erro de âncora deve identificar o id e a posição.
```

---

## Matriz mínima padrão (executável sem argumentos)

O script deve ter uma **matriz padrão** executável sem argumentos. Quando
executado como `python tela/explorar_barra_de_menus.py`, a matriz padrão cobre:

```
1.  Linha única com 3 chips e largura ampla (content_w >= 80)
    Perfil: curto. Espaçamento: mínimo. Sem âncoras.
    Esperado: OK, 1 linha física.

2.  Linha única com 6 chips e largura ampla (content_w >= 100)
    Perfil: curto. Espaçamento: mínimo. Sem âncoras.
    Esperado: OK, 1 linha física.

3.  Duas linhas com 6 chips e largura estreita (content_w = 40)
    Perfil: médio. Espaçamento: mínimo. linhas.maximo=2.
    preenchimento: coluna_a_coluna. Sem âncoras.
    Esperado: OK, 2 linhas físicas (se caber) ou erro_layout (se não caber).
    O implementador deve ajustar content_w para que o caso caiba em 2 linhas.

4.  Duas linhas com 8 chips e largura estreita (content_w = 50)
    Perfil: curto. Espaçamento: mínimo. linhas.maximo=2.
    preenchimento: coluna_a_coluna. Sem âncoras.
    Esperado: OK, 2 linhas físicas (se caber) ou erro_layout.

5.  Três linhas com 10 chips e largura estreita (content_w = 40)
    Perfil: curto. Espaçamento: mínimo. linhas.maximo=3.
    preenchimento: coluna_a_coluna. Sem âncoras.
    Esperado: OK, ≤ 3 linhas físicas (se caber) ou erro_layout.

6.  Overflow forçado: 10 chips, largura muito estreita (content_w = 20)
    Perfil: médio. Espaçamento: mínimo. linhas.maximo=2. Sem âncoras.
    Esperado: RenderizadorErro com "erro_layout". Classificado como erro esperado.

7.  Overflow forçado: 12 chips, largura muito estreita (content_w = 15)
    Perfil: curto. Espaçamento: mínimo. linhas.maximo=2. Sem âncoras.
    Esperado: RenderizadorErro com "erro_layout". Classificado como erro esperado.

8.  coluna_a_coluna com 5 chips, content_w = 60
    Perfil: misto. Espaçamento: mínimo. linhas.maximo=2. Sem âncoras.
    Esperado: OK; verificar padrão de distribuição coluna_a_coluna.

9.  linha_a_linha com 5 chips, content_w = 60
    Perfil: misto. Espaçamento: mínimo. linhas.maximo=2. Sem âncoras.
    Esperado: OK; verificar padrão de distribuição linha_a_linha.

10. Âncora válida: 2 chips, chip_esc primeiro, chip_ajuda último
    content_w = 39. âncoras declaradas e respeitadas.
    Esperado: OK; validação de âncora não levanta erro.

11. Âncora inexistente: 2 chips, âncora primeiro com id "chip_x" (inexistente)
    Esperado: RenderizadorErro com menção ao id inexistente.
    Classificado como erro esperado.

12. Âncora em posição errada: 2 chips, chip_ajuda declarado primeiro mas
    âncora primeiro exige chip_esc.
    Esperado: RenderizadorErro com menção à posição errada.
    Classificado como erro esperado.

13. Espaçamentos mínimos: 4 chips, content_w = 60, linhas.maximo=2
    vao_entre_chips=2, vao_entre_colunas=2. preenchimento: coluna_a_coluna.
    Esperado: OK; verificar invariantes de largura e chips.

14. Espaçamentos máximos: 4 chips, content_w = 80, linhas.maximo=2
    vao_entre_chips=6, vao_entre_colunas=8. preenchimento: coluna_a_coluna.
    Esperado: OK (se caber) ou erro_layout (se não caber).
    O implementador deve ajustar content_w para que caiba.
```

O implementador pode ajustar os valores concretos de `content_w` e `linhas.maximo`
dos cenários acima para que as expectativas declaradas sejam satisfeitas — desde
que os ajustes não alterem a **natureza** do cenário (ex.: "largura estreita
forçando multilinha" deve continuar sendo um cenário que força multilinha).
Qualquer ajuste deve ser documentado no IMP-0017.

---

## Teste automatizado do script

### Caminho

```
scripts/tela/teste_explorar_barra_de_menus.py
```

### Padrão de implementação

O teste deve seguir o padrão procedural existente nas suítes de teste do projeto:
- `sys.dont_write_bytecode = True` no topo.
- Infraestrutura de `_registrar(ok, descricao)` ou equivalente.
- Executável via `python tela/teste_explorar_barra_de_menus.py`.
- Exit code 0 quando todos os testes passam; exit code não-zero quando falha.
- Apenas biblioteca padrão do Python.

Se o teste precisar invocar o script `explorar_barra_de_menus.py` como
subprocesso (para verificar exit codes), deve usar `subprocess.run` de forma
determinística e sem dependência de terminal real.

### Casos obrigatórios do teste automatizado

```
1.  O script roda com matriz padrão (sem argumentos) e retorna exit code 0.
    Verificado via subprocess.run.

2.  O modo resumo é determinístico: duas chamadas com mesmos parâmetros
    produzem saída idêntica.
    Verificado via subprocess.run com captura de stdout.

3.  Um caso válido de linha única passa:
    Barra com 3 chips curtos em content_w amplo → OK, 1 linha física.
    Verificado via chamada direta a _linhas_barra (sem subprocess).

4.  Um caso válido de multilinha coluna_a_coluna passa:
    Barra com 4 chips em content_w estreito, linhas.maximo=2 →
    OK, 2 linhas físicas, padrão coluna_a_coluna.
    Verificado via chamada direta a _linhas_barra.

5.  Um caso válido de multilinha linha_a_linha passa:
    Barra com 4 chips em content_w estreito, linhas.maximo=2,
    preenchimento=linha_a_linha → OK, 2 linhas físicas.
    (Testado apenas se linha_a_linha foi confirmado como implementado no H-0016.
    Conforme IMP-0016, linha_a_linha foi implementado deterministicamente.)
    Verificado via chamada direta a _linhas_barra.

6.  Um caso de overflow esperado é classificado como erro esperado e não
    quebra a matriz:
    Barra com 10 chips em content_w = 15, linhas.maximo=2 →
    RenderizadorErro com "erro_layout".
    O script continua depois do erro.
    Verificado via subprocess.run com verificação de saída.

7.  Um caso de âncora inexistente é classificado como erro esperado:
    id inexistente em âncora → RenderizadorErro com menção ao id.
    Verificado via chamada direta a _linhas_barra.

8.  Um caso de âncora em posição errada é classificado como erro esperado:
    id presente em posição errada → RenderizadorErro com menção à posição.
    Verificado via chamada direta a _linhas_barra.

9.  O script retorna exit code 1 quando uma violação inesperada é detectada:
    Simulado via parâmetro que force um cenário de violação controlada, ou
    verificado por inspeção do código do script (se não for possível simular
    via subprocess de forma determinística).
    Observação: se a simulação via subprocess não for determinística ou exigir
    estado externo, o implementador pode verificar apenas via inspeção do código
    do script e registrar no IMP-0017.

10. O script retorna exit code 2 para parâmetro inválido:
    Ex.: --preenchimentos valor_invalido → exit code 2.
    Verificado via subprocess.run.
```

---

## Integração futura

Este script é uma **ferramenta diagnóstica/exploratória**. Neste ciclo:

- **Não** deve ser acoplado automaticamente ao diagnóstico principal
  (`diagnostico.py`).
- **Não** deve ser chamado automaticamente pela demo (`demo.py`).
- **Não** deve ser requisito de execução normal da aplicação.
- **Não** deve mudar contratos.
- **Não** deve criar formato normativo definitivo de validação de telas futuras.

**Possibilidade de integração futura** (apenas como registro):
O script poderá futuramente entrar em um pipeline de validação de telas criadas,
servindo como ferramenta de smoke test para novas configurações de
`barra_de_menus`. Essa possibilidade fica documentada aqui apenas para
rastreabilidade; não deve influenciar as decisões de implementação deste ciclo.

---

## Escopo positivo

H-0017 pode e deve implementar:

```
- Criar o script explorar_barra_de_menus.py no caminho definido.
- Criar o teste automatizado teste_explorar_barra_de_menus.py.
- Usar _linhas_barra e RenderizadorErro do renderizador.
- Usar _DISTRIBUICAO_HORIZONTAL_RESPONSIVA_DEFAULT do renderizador como base
  para construção sintética de barra_de_menus com defaults normativos.
- Criar helpers internos no script (ex.: _fabricar_chips, _fabricar_distribuicao,
  _fabricar_cenario, _verificar_invariantes) para evitar duplicação interna.
- Gerar barras sintéticas e chips sintéticos em memória.
- Validar invariantes da renderização conforme seção "Invariantes".
- Produzir saída em modo resumo e detalhado.
- Implementar os parâmetros de linha de comando mínimos definidos neste handoff.
- Criar o relatório IMP-0017.
- Ajustar minimamente renderizador.py apenas se for necessário expor função
  já existente de forma segura, sem alterar comportamento do H-0016.
```

---

## Escopo negativo

H-0017 **não deve** implementar:

```
- Nova regra normativa da barra_de_menus.
- Alteração de ADR (nenhuma).
- Alteração de contrato (nenhuma).
- Alteração de NOMENCLATURA.md.
- Alteração dos JSONs ativos (orquestrador.json, grupo_minimo.json,
  destino_minimo.json, stub_b.json).
- Mudança no comportamento do renderer aprovado no H-0016.
- Mudança de semântica de chips.
- Mudança no lancador.
- Uso de chips do lancador na barra.
- Composição horizontal do corpo.
- corpo.arranjo = "horizontal".
- Distribuição de altura entre elementos do corpo.
- Correção do preenchimento vertical do H-0015.
- Console real.
- Paginação.
- Filtros.
- Seleção.
- Registry novo de ações.
- Registry novo de telas.
- Integração automática ao diagnóstico principal (diagnostico.py).
- Integração automática à demo (demo.py).
- Geração de arquivos temporários rastreados.
- Dependência de terminal real (sem curses, sem termios).
- Formato normativo definitivo de validação de telas futuras.
```

---

## Arquivos permitidos

O executor pode criar ou editar **somente** os seguintes arquivos:

```
scripts/tela/explorar_barra_de_menus.py              (criar)
scripts/tela/teste_explorar_barra_de_menus.py        (criar)
scripts/tela/renderizador.py                         (apenas se necessário
                                                      expor helper já existente
                                                      sem alterar comportamento)
scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
                                                     (criar)
```

**Observação sobre `renderizador.py`**: só deve ser alterado se for
estritamente necessário expor um helper já existente ou corrigir um acesso
público sem alterar o comportamento aprovado no H-0016. Se a implementação
puder ser feita sem alterar `renderizador.py`, essa é a opção preferida e deve
ser documentada no IMP-0017.

---

## Arquivos proibidos

O executor **não deve tocar** em nenhum dos seguintes arquivos:

```
scripts/docs/contratos/              ← todos os arquivos de contrato
scripts/docs/adr/                    ← todos os ADRs
scripts/docs/NOMENCLATURA.md
scripts/docs/INDICE.md

scripts/config/telas/                ← todos os JSONs de tela ativos
scripts/config/estilo.json
scripts/config/lancador.json
scripts/config/layout_console.json

scripts/tela/loader.py
scripts/tela/modelo.py
scripts/tela/demo.py
scripts/tela/diagnostico.py

scripts/tela/teste_loader.py
scripts/tela/teste_modelo.py
scripts/tela/teste_renderizador.py
scripts/tela/teste_demo.py
scripts/tela/teste_diagnostico.py
```

Se qualquer arquivo desta lista precisar ser alterado para concluir a
implementação, o executor deve bloquear com `ARCHITECTURE_REVIEW_REQUIRED` e
**não alterar o arquivo**.

---

## Critérios de aceite

O ciclo H-0017 é considerado **concluído** quando todos os critérios abaixo
forem atendidos:

```
 1. Script criado no caminho scripts/tela/explorar_barra_de_menus.py
    (ou caminho alternativo justificado no IMP-0017).
 2. Script executa sem argumentos com matriz padrão e exit code 0.
 3. Script aceita --larguras, --chips, --linhas-max, --preenchimentos,
    --modo-saida, --mostrar-ok, --mostrar-erros, --limite-casos.
 4. Script varia quantidade de chips (mínimo: 1, 2, 3, 4, 5, 6, 8, 10, 12).
 5. Script varia largura disponível (muito estreita, estreita, média, larga).
 6. Script varia linhas.maximo entre 1, 2 e 3.
 7. Script testa coluna_a_coluna.
 8. Script testa linha_a_linha.
 9. Script testa espaçamentos mínimos.
10. Script testa espaçamentos máximos.
11. Script testa cenário de linha única.
12. Script testa cenário de duas linhas.
13. Script testa cenário de três linhas quando linhas.maximo=3.
14. Script testa overflow determinístico (erro_layout).
15. Script testa âncora válida.
16. Script testa âncora inexistente.
17. Script testa âncora em posição errada.
18. Script verifica que cada chip declarado aparece exatamente uma vez.
19. Script verifica ausência de chip inventado.
20. Script verifica ausência de truncamento do texto dos chips.
21. Script verifica preservação da ordem declarada.
22. Script verifica que a largura de cada linha ≤ content_w.
23. Script verifica que a quantidade de linhas físicas ≤ linhas.maximo.
24. Script classifica erro esperado (overflow, âncora inválida) sem abortar
    a matriz.
25. Script retorna exit code 0 quando todos os cenários produzem resultado
    esperado.
26. Script retorna exit code 1 para violação de invariante inesperada.
27. Script retorna exit code 2 para parâmetro inválido.
28. Teste automatizado teste_explorar_barra_de_menus.py passa com exit code 0.
29. Testes existentes continuam passando (451/451 verificações em 5 suítes).
30. Nenhum JSON ativo é alterado.
31. Nenhum contrato, ADR ou NOMENCLATURA é alterado.
32. Nenhum __pycache__ ou .pyc fica no workspace.
```

---

## Testes obrigatórios

### Suítes existentes (devem continuar passando)

```bash
cd scripts
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
python tela/teste_diagnostico.py
```

### Suíte nova

```bash
cd scripts
python tela/teste_explorar_barra_de_menus.py
```

### Execuções manuais obrigatórias do script

O implementador deve executar manualmente e registrar a saída completa no
IMP-0017:

```bash
cd scripts

# Execução sem argumentos (matriz padrão)
python tela/explorar_barra_de_menus.py

# Modo resumo com parâmetros explícitos
python tela/explorar_barra_de_menus.py \
  --modo-saida resumo \
  --larguras 30,40,80 \
  --chips 3,6,10 \
  --linhas-max 1,2,3 \
  --preenchimentos coluna_a_coluna,linha_a_linha

# Modo detalhado com limite de casos e mostrar erros
python tela/explorar_barra_de_menus.py \
  --modo-saida detalhado \
  --mostrar-erros \
  --limite-casos 20
```

---

## Relatório de implementação

O implementador deve criar o arquivo:

```
scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md
```

Com a seguinte estrutura mínima:

```markdown
# IMP-0017 — Script de exploração de combinações da barra_de_menus

## Status

## Resumo

## Arquivos alterados/criados

## Script criado

## Parâmetros implementados

## Matriz de cenários

## Invariantes verificadas

## Testes automatizados

## Execuções manuais

## Resultados

## Limitações conhecidas

## Confirmação de fora de escopo
```

### Seção "Confirmação de fora de escopo" — conteúdo obrigatório

A seção deve confirmar explicitamente que **não** foram implementados:

```
- Nova regra normativa da barra_de_menus.
- Alteração de ADR.
- Alteração de contrato.
- Alteração de NOMENCLATURA.
- Alteração dos JSONs ativos.
- Mudança no comportamento aprovado do renderer H-0016.
- Composição horizontal do corpo.
- Distribuição de altura entre elementos do corpo.
- Integração automática ao diagnóstico principal.
- Integração automática à demo.
```

---

## Critérios de bloqueio — ARCHITECTURE_REVIEW_REQUIRED

O executor deve bloquear a implementação e registrar `ARCHITECTURE_REVIEW_REQUIRED`
nos seguintes casos:

```
1. For necessário alterar contrato, ADR ou NOMENCLATURA para implementar o script.
2. For necessário alterar os JSONs ativos (orquestrador.json, grupo_minimo.json,
   destino_minimo.json, stub_b.json).
3. For necessário mudar o comportamento do renderer aprovado no H-0016
   (não apenas expor um helper já existente).
4. For necessário alterar loader.py, modelo.py, demo.py ou diagnostico.py
   (fonte, não testes).
5. For necessário depender de terminal real (curses, termios, tty) para
   exercitar os cenários.
6. For necessário criar formato normativo definitivo de validação de telas
   (estrutura que comprometa decisões de ADR futuras).
7. O renderer atual não permitir exercitar os cenários definidos sem
   alteração arquitetural.
8. For necessário alterar teste_loader.py, teste_modelo.py,
   teste_renderizador.py, teste_demo.py ou teste_diagnostico.py.
```

**Ao bloquear**, o executor deve:
- Registrar `ARCHITECTURE_REVIEW_REQUIRED` no topo do relatório IMP-0017.
- Descrever precisamente qual decisão arquitetural está faltando.
- **Não implementar código** além do que já está especificado sem bloqueio.

---

## Instrução explícita ao executor

Você é o OpenCode / GLM atuando como **executor de implementação**.

Hierarquia de autoridade (não negociável):

```
contrato_processo_desenvolvimento.md
  > ADRs aceitos (especialmente ADR-0014)
    > contratos de módulo
      > este handoff
        > decisões de implementação locais
```

**Regras operacionais**:

- Ler toda a seção "Leitura obrigatória" antes de tocar qualquer arquivo.
- Implementar **exatamente** o que este handoff especifica — sem funcionalidades
  extras, sem refatorações não solicitadas, sem abstrações adicionais.
- **Não alterar** nenhum arquivo da lista "Arquivos proibidos".
- **Não alterar** o comportamento do renderer implementado no H-0016.
- **Não decidir arquitetura** — qualquer dúvida arquitetural → `ARCHITECTURE_REVIEW_REQUIRED`.
- Se o script revelar bug no renderer, registrar no IMP-0017 e bloquear se a
  correção exigir mudança de comportamento; se for ajuste local mínimo, documentar.
- Criar o relatório IMP-0017 ao final.
- Não fazer commit — o commit é responsabilidade de outra etapa do fluxo.

**Ordem de implementação recomendada**:

1. Ler toda a leitura obrigatória (especialmente `renderizador.py` integralmente).
2. Criar `explorar_barra_de_menus.py` com a infraestrutura mínima (argparse,
   _registrar ou equivalente, exit codes).
3. Implementar os helpers de fabricação sintética de cenários (_fabricar_chips,
   _fabricar_distribuicao, _fabricar_cenario).
4. Implementar a verificação de invariantes.
5. Implementar a geração da matriz de cenários e execução.
6. Implementar a saída em modo detalhado e modo resumo.
7. Executar manualmente os três modos obrigatórios e verificar exit codes.
8. Criar `teste_explorar_barra_de_menus.py` e garantir que todos os 10 casos
   do teste automatizado passam.
9. Executar todas as 5 suítes existentes e confirmar que continuam passando.
10. Criar IMP-0017.

---

## Saída final esperada

Ao concluir, o executor deve reportar:

```
IMPLEMENTATION_COMPLETED

arquivos-criados:
  scripts/tela/explorar_barra_de_menus.py
  scripts/tela/teste_explorar_barra_de_menus.py
  scripts/docs/relatorios/IMP-0017-script-exploracao-combinacoes-barra-de-menus.md

[se renderizador.py foi alterado]
arquivos-alterados:
  scripts/tela/renderizador.py — <justificativa em uma linha>

testes:
  teste_loader.py:                 <N>/<N>
  teste_modelo.py:                 <N>/<N>
  teste_renderizador.py:           <N>/<N>
  teste_demo.py:                   <N>/<N>
  teste_diagnostico.py:            <N>/<N>
  teste_explorar_barra_de_menus.py: <N>/<N>

verificacoes:
  <git status --short>
  <git diff --stat>
```
