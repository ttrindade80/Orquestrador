# IMP-0027 — Distribuição horizontal explícita do corpo (percentual e fração)

## 1. Identificação

| Campo | Valor |
|---|---|
| Identificador | IMP-0027 |
| Etapa executada | `IMPLEMENTAR` |
| Handoff implementado | H-0026 |
| Data | 2026-07-11 |

## 2. Etapa executada

`IMPLEMENTAR`, exclusivamente. Não houve QA formal da implementação, não houve
aprovação da própria entrega, não houve correção pós-QA, não houve alteração do
handoff, não houve criação/alteração de ADR, não houve alteração de contratos
ou nomenclatura, não houve fechamento, não houve preparação de commit, não houve
commit ou push, não houve início de outro ciclo.

## 3. Handoff implementado

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
```

## 4. QA que aprovou o handoff

QA pós-patch que liberou o handoff para implementação:

```text
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0026_HANDOFF.md
```

Status final do QA pós-patch: `H1_HANDOFF_READY_FOR_IMPLEMENTATION`.

Os achados anteriores `H0026-QA-A01` e `H0026-QA-M01` foram resolvidos no patch
do handoff e confirmados como resolvidos pelo QA pós-patch. Não foram reabertos.

## 5. Branch e commit-base

```text
branch:        master
commit-base:   1cc0dff feat: implementa distribuicao vertical explicita do corpo
```

## 6. Estado Git inicial

Comandos executados antes de qualquer alteração:

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git status --short` | quatro entradas não rastreadas (handoff, levantamento, QA, QA pós-patch) + `tela/__pycache__/` |
| `git diff --stat` | sem saída |
| `git diff --name-only` | sem saída |
| `git diff --cached --stat` | sem saída |
| `git diff --cached --name-only` | sem saída |

Estado confirmado: branch e commit conferem com a referência informada; stage
vazio; nenhuma alteração rastreada preexistente; não rastreados correspondem ao
estado esperado do ciclo.

## 7. Arquivos alterados

Somente os dois arquivos rastreados permitidos pela lista fechada do handoff
(§9.1):

```text
tela/renderizador.py
tela/teste_renderizador.py
```

Resumo do diff:

```text
 scripts/tela/renderizador.py       |  88 ++++++-
 scripts/tela/teste_renderizador.py | 484 ++++++++++++++++++++++++++++++++++++-
 2 files changed, 556 insertions(+), 16 deletions(-)
```

## 8. Arquivos somente lidos

Lidos integralmente ou em seções aplicáveis, sem alteração:

```text
tela/loader.py
tela/modelo.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_demo.py
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0026_HANDOFF.md
docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
docs/contratos/contrato_composicao_corpo.md
docs/contratos/contrato_tela_json.md
docs/contratos/contrato_json_tela_minima.md
```

Nenhum arquivo normativo, loader, modelo, JSON declarativo ou demo foi alterado.

## 9. Descrição da implementação

Quando `corpo.arranjo = "horizontal"` **e** `corpo.distribuicao` está declarado
com `modo: "percentual"` ou `modo: "fracao"`, o renderizador passa a calcular as
larguras dos filhos diretos proporcionalmente aos valores declarados, aplicando
o algoritmo de maiores restos, em vez do particionamento uniforme anterior.

Quando `corpo.distribuicao` está ausente (`None`), o comportamento horizontal
existente (particionamento uniforme, H-0019/H-0020/H-0021) é preservado
integralmente, sem conversão para modo `igual`.

A distribuição controla exclusivamente as larguras dos filhos diretos do corpo
raiz horizontal. Bordas adjacentes permanecem coladas, sem vão externo; a
largura total da saída é preservada; o preenchimento interno por espaços nas
áreas alocadas é mantido.

## 10. Abordagem técnica escolhida

Opção selecionada entre as autorizadas pelo handoff §13.3.2: **criar um helper
local `_distribuir_larguras` análogo a `_distribuir_alturas`**, reutilizando a
mesma lógica normativa de maiores restos.

Justificativa da escolha:

- O algoritmo de maiores restos é idêntico para qualquer eixo, mas o handoff
  exige explicitamente que a extração seja local e que o comportamento vertical
  aprovado pelo H-0025 não possa ser afetado.
- Um helper independente (`_distribuir_larguras`) evita qualquer risco de
  regressão no helper vertical (`_distribuir_alturas`), que permanece byte a
  byte inalterado.
- A intervenção mínima no ponto de despacho é suficiente: quando
  `distribuicao_corpo` está presente, calculam-se os pesos via
  `_pesos_distribuicao` (helper genérico existente) e as larguras via
  `_distribuir_larguras`, passadas a `_montar_corpo_horizontal` como parâmetro
  opcional `larguras`.

Não houve refatoração ampla, mudança de arquitetura, alteração de API pública,
generalização para grupos horizontais nem criação de abstração futura sem uso
necessário.

## 11. Cálculo de percentual

Para `modo: "percentual"`:

- um valor por filho direto, associado posicionalmente pela ordem declarada;
- valores já validados pelo loader (positivos, soma exatamente 100);
- cota ideal real de cada filho: `total_w * valor_i / 100`;
- conversão para colunas inteiras por maiores restos;
- soma final das cotas inteiras exatamente igual a `total_w`.

Não há repetição de validações normativas pertencentes ao loader. A defesa
interna existente em `_distribuir_larguras` (soma de pesos não positiva) segue o
mesmo padrão defensivo de `_distribuir_alturas`.

Exemplo verificado: `percentual [50, 50]` em `total_w=42` → `[21, 21]`;
`percentual [60, 40]` em `total_w=42` → `[25, 17]`.

## 12. Cálculo de fração

Para `modo: "fracao"`:

- um peso positivo por filho direto, associado posicionalmente;
- denominador implícito igual à soma dos pesos;
- cota ideal real: `total_w * peso_i / soma_dos_pesos`;
- conversão por maiores restos;
- soma final exatamente igual a `total_w`.

Vetores equivalentes por escala produzem as mesmas larguras, pois a
normalização pelo denominador cancela o fator de escala. Verificado:
`[2, 1]` e `[4, 2]` em `total_w=42` produzem ambos `[28, 14]`.

## 13. Maiores restos

Algoritmo normativo (ADR-0015 D8; contrato seção 5.8), implementado em
`_distribuir_larguras`:

1. calcular as cotas ideais reais (`largura_disponivel * peso / soma`);
2. atribuir inicialmente as partes inteiras (`floor`);
3. calcular quantas colunas ainda faltam (`faltam = largura - sum(inteiros)`);
4. ordenar os índices por resto fracionário decrescente;
5. resolver empates pela ordem declarada (menor índice prevalece);
6. distribuir uma coluna por posição até completar a largura;
7. preservar a soma exata (`sum(cotas) == largura_disponivel`).

Invariantes observados: nenhuma coluna perdida, nenhuma coluna externa criada,
nenhuma cota atribuída a filho diferente da posição correspondente.

## 14. Desempate por ordem

Empates de resto fracionário são resolvidos pela ordem declarada em
`corpo.elementos[]`: menor índice prevalece. O `sorted` em `_distribuir_larguras`
usa chave `(-resto, índice)`, garantindo estabilidade determinística.

Caso normativo T07 comprova o desempate: `[1, 1, 1]` em `total_w=101` → partes
inteiras `[33, 33, 33]`, faltam 2, restos empatados, posições 0 e 1 recebem a
unidade extra → `[34, 34, 33]`.

## 15. Integração com o caminho horizontal

Ponto de intervenção: ramo de despacho principal do arranjo horizontal em
`tela/renderizador.py` (após edição, linhas around 1035–1055).

Antes: o ramo chamava `_montar_corpo_horizontal` sem considerar
`distribuicao_corpo`, calculando sempre larguras uniformes.

Depois:

1. quando `distribuicao_corpo is not None`, calculam-se os pesos via
   `_pesos_distribuicao(distribuicao_corpo, len(modelo.corpo.elementos))`;
2. calculam-se as larguras via `_distribuir_larguras(total_w, pesos)`;
3. essas larguras são passadas a `_montar_corpo_horizontal` via parâmetro
   `larguras`;
4. quando `distribuicao_corpo is None`, `larguras` permanece `None` e o
   particionamento uniforme existente é tomado integralmente.

A função `_montar_corpo_horizontal` passou a aceitar `larguras=None` como
parâmetro opcional. Quando `None`, executa o cálculo uniforme anterior
(`base_w = total_w // N`, `resto = total_w % N`). Quando fornecida, usa as
larguras explícitas. Toda a lógica de renderização, preenchimento vertical,
concatenação contígua e verificação de largura mínima permanece inalterada.

## 16. Preservação da ausência

Quando `corpo.distribuicao` está ausente (`None`):

- o particionamento uniforme é preservado integralmente;
- a ausência não é convertida para modo `igual`;
- não há repartição proporcional automática;
- não há criação de distribuição implícita.

Conforme ADR-0018 D2 e contrato seção 5.7. Verificado por T-NR01: sem
distribuição, 2 elementos em `total_w=42` → `[21, 21]`; 3 elementos em
`total_w=100` → `[34, 33, 33]` (uniforme da esquerda).

## 17. Preservação vertical

A implementação horizontal **não modificou** o comportamento vertical do
H-0025:

- `_distribuir_alturas` permanece byte a byte inalterado;
- o ramo vertical de despacho (`elif distribuicao_corpo is not None and altura
  is not None`) permanece inalterado;
- os modos verticais existentes, maiores restos verticais, preenchimento
  vertical e comportamento sem distribuição no eixo vertical são preservados;
- os testes existentes do H-0025 continuam passando integralmente.

O helper `_distribuir_larguras` é uma rotina local e independente; não houve
extração de rotina comum que pudesse afetar o helper vertical.

Verificado por T-NR02 e pela execução integral da suíte
`TestDistribuicaoVerticalH0025`.

## 18. Testes criados ou alterados

### Novos testes (classe `TestDistribuicaoHorizontalH0026`)

| Teste | Conteúdo |
|---|---|
| `test_algoritmo_distribuir_larguras_soma_exata` | Invariante `sum(cotas) == largura` para 10 pares |
| `test_algoritmo_distribuir_larguras_exemplos_normativos` | T06 `[34,33,33]` e T07 `[34,34,33]` no helper |
| `test_percentual_simetrico_50_50` | T01: `[50,50]` → `[21,21]` |
| `test_percentual_assimetrico_60_40` | T02: `[60,40]` → `[25,17]` |
| `test_fracao_simetrico_1_1` | T03: `[1,1]` → `[21,21]` |
| `test_fracao_assimetrico_2_1` | T04: `[2,1]` → `[28,14]` |
| `test_fracao_equivalencia_por_escala` | T05: `[2,1]` == `[4,2]` |
| `test_t06_maiores_restos_largura_100` | T06: `[1,1,1]` em 100 → `[34,33,33]` |
| `test_t07_empate_restos_resolvido_por_ordem_declarada` | T07: `[1,1,1]` em 101 → `[34,34,33]` |
| `test_t08_soma_larguras_igual_distribuivel` | T08: soma == largura em 6 fixtures |
| `test_t09_bordas_em_contato` | T09: `╮╭`, `╯╰`, `││` presentes |
| `test_t10_largura_total_preservada` | T10: todas as linhas com 42 chars |
| `test_t11_preenchimento_interno_conteudo_menor_que_cota` | T11: preenchimento por espaços na área |
| `test_ausencia_distribuicao_preserva_uniforme` | T-NR01: ausência sem regressão |
| `test_distribuicao_vertical_h0025_nao_regride` | T-NR02: vertical H-0025 preservado |
| `test_rejeicoes_loader_preservadas` | T-NR03: loader rejeita inválidos em horizontal |

### Teste alterado

`test_arranjo_horizontal_nao_regride_com_distribuicao` (em
`TestDistribuicaoVerticalH0025`): atualizado para verificar larguras reais.
Antes verificava apenas ausência de erro e particionamento contíguo; agora
verifica que `fracao [1, 1]` em `total_w=42` produz área A com 21 colunas
(`char[20] == '╮'`) e área B iniciando na coluna 21 (`char[21] == '╭'`), além
das verificações originais de `╮╭` presente e largura total preservada.

## 19. Atualização do teste histórico horizontal

O teste `test_arranjo_horizontal_nao_regride_com_distribuicao` foi atualizado
conforme §16.2 do handoff. O comentário agora registra que o H-0026 implementa a
distribuição horizontal (antes dizia que H-0025 não a implementava). O teste
passa a verificar o comportamento horizontal distribuído aprovado, sem afrouxar
asserts e sem remover cobertura válida.

As três verificações originais foram mantidas (renderiza sem erro, `╮╭`
presente, cada linha com 42 chars) e três novas foram adicionadas (linha de
topo do corpo encontrada, área A com 21 colunas, área B inicia na coluna 21).

## 20. Comandos executados

### Suíte principal

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
```

### Suítes de regressão

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_loader.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_modelo.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_renderizador.py
PYTHONDONTWRITEBYTECODE=1 python tela/teste_demo.py
```

### Verificações de diff

```bash
git diff --check
git diff --stat
git diff --name-only
git diff -- tela/renderizador.py
git diff -- tela/teste_renderizador.py
git diff --cached --stat
git diff --cached --name-only
git status --short
```

## 21. Resultados e códigos de saída

| Comando | Verificações | Resultado | Exit |
|---|---|---|---|
| `python tela/teste_renderizador.py` | 434 | 434 passaram, 0 falharam | 0 |
| `python tela/teste_loader.py` | 105 (PASSOU) | 0 FALHOU | 0 |
| `python tela/teste_modelo.py` | 58 (PASSOU) | 0 FALHOU | 0 |
| `python tela/teste_demo.py` | 303 | 303 passaram, 0 falharam | 0 |

## 22. Contagens antes e depois

| Suíte | Antes (verificações) | Depois (verificações) | Delta |
|---|---|---|---|
| `teste_renderizador.py` | 385 | 434 | +49 |

O acréscimo de 49 verificações corresponde aos novos testes da classe
`TestDistribuicaoHorizontalH0026` e às três verificações adicionais no teste
histórico atualizado. As suítes loader, modelo e demo não tiveram alteração de
contagem (nenhum arquivo dessas suítes foi modificado).

## 23. Regressões verificadas

- **T-NR01** (ausência de `corpo.distribuicao` preserva uniforme): passou.
  Verificado em 2 e 3 elementos.
- **T-NR02** (distribuição vertical H-0025 não regride): passou. Helper
  `_distribuir_alturas` inalterado; exemplos normativos `[23,23,22]` e
  `[27,14,27]` confirmados.
- **T-NR03** (rejeições do loader preservadas): passou. Loader rejeita
  `percentual` soma != 100 e `fracao` com peso zero em arranjo horizontal.
- Suíte `TestDistribuicaoVerticalH0025` integral: passou (sem alteração).
- Suíte `TestArranjoH0019` integral: passou (sem alteração).
- Suíte `teste_loader.py` integral: passou (105 PASSOU, 0 FALHOU).
- Suíte `teste_modelo.py` integral: passou (58 PASSOU, 0 FALHOU).
- Suíte `teste_demo.py` integral: passou (303 verificações, 0 falhas).

## 24. Limitações preservadas

- **Grupos horizontais**: continuam fora de escopo. O loader ainda rejeita
  grupo com `arranjo = "horizontal"` (barragem em `tela/loader.py` não
  removida). Nenhuma generalização para grupos foi introduzida.
- **Política para conteúdo maior que a cota horizontal**: permanece fora de
  escopo normativo (contrato seção 5.7.1). Nenhuma política de overflow,
  truncamento, rejeição ou degradação foi introduzida.
- **Composição em três níveis**: fora de escopo. Não houve ampliação hierárquica.
- **Outros arranjos**: fora de escopo.

## 25. Itens fora de escopo

Não foram implementados (nem total, nem parcialmente):

- grupos horizontais;
- composição em três níveis;
- política para conteúdo maior que a cota;
- largura mínima por tipo de elemento;
- distribuição automática quando `corpo.distribuicao` está ausente;
- outros arranjos além de `horizontal`;
- JSON demonstrativo de `corpo.arranjo = "horizontal"` com distribuição;
- alteração do loader ou do modelo;
- alteração de contratos, ADRs ou nomenclatura;
- QA formal da implementação;
- aprovação da própria entrega;
- commit ou push.

## 26. Estado Git final

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git diff --name-only` | `tela/renderizador.py`, `tela/teste_renderizador.py` |
| `git diff --cached --stat` | sem saída (stage vazio) |
| `git diff --cached --name-only` | sem saída (stage vazio) |
| `git diff --check` | sem saída (exit 0) |

O commit-base não avançou. O stage permanece vazio. Somente os dois arquivos
rastreados permitidos foram alterados.

## 27. Arquivos não rastreados

```text
docs/handoff/H-0026-distribuicao-horizontal-percentual-fracao-corpo.md
docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_HORIZONTAL_PERCENTUAL_FRACAO.md
docs/relatorios/RELATORIO_QA_H-0026_HANDOFF.md
docs/relatorios/RELATORIO_QA_POS_PATCH_H-0026_HANDOFF.md
docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
tela/__pycache__/
```

Os quatro primeiros são não rastreados preexistentes do ciclo (preservados). O
relatório `IMP-0027` é o novo arquivo criado por esta etapa (esperado). O
diretório `tela/__pycache__/` é cache Python preexistente.

Quanto a cache: `PYTHONDONTWRITEBYTECODE=1` foi usado em todos os comandos de
teste. Nenhum arquivo `.pyc` novo foi produzido pelos testes (os arquivos em
`tela/__pycache__/` preservam data/hora anterior a esta sessão). O diretório
não foi removido silenciosamente.

## 28. Bloqueios ou ressalvas

Nenhum bloqueio encontrado. A implementação foi concluída dentro do escopo
autorizado, sem necessidade de alterar loader, modelo, contratos, ADRs,
nomenclatura ou qualquer arquivo fora da lista fechada.

Não houve necessidade de decidir política nova: a semântica horizontal de
`percentual` e `fracao` estava fechada nas autoridades ativas (ADR-0015 D5–D10;
ADR-0018 D6/D7; contrato seções 4.9, 5.7, 5.8).

## 29. Declaração explícita de ausência de commit

**Não houve commit.** Não houve preparação de commit. Não houve `git add`, não
houve `git stash`, não houve alteração de branch, não houve push. O stage
permanece vazio. A implementação termina com o relatório `IMP-0027` criado e os
testes passando.

---

## Saída final

```text
status: IMPLEMENTATION_COMPLETED
handoff_implementado: H-0026
relatorio: docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
arquivos_alterados: tela/renderizador.py, tela/teste_renderizador.py
arquivos_criados: docs/relatorios/IMP-0027-distribuicao-horizontal-percentual-fracao-corpo.md
abordagem_tecnica: helper local _distribuir_larguras analogo a _distribuir_alturas, independente, preservando o helper vertical
comportamento_percentual: cota = total_w * valor / 100, maiores restos, soma exata
comportamento_fracao: cota = total_w * peso / soma_pesos, maiores restos, soma exata
maiores_restos: floor + distribuicao da sobra por resto decrescente, desempate por ordem declarada
testes_adicionados_ou_ajustados: classe TestDistribuicaoHorizontalH0026 (16 metodos) + atualizacao de test_arranjo_horizontal_nao_regride_com_distribuicao
testes_executados: teste_renderizador.py, teste_loader.py, teste_modelo.py, teste_demo.py
resultados: renderizador 434/434, loader 105 PASSOU/0 FALHOU, modelo 58 PASSOU/0 FALHOU, demo 303/303
regressoes: T-NR01 ausencia, T-NR02 vertical H-0025, T-NR03 rejeicoes loader — todas passaram
git: branch master, commit 1cc0dff, stage vazio
arquivos_nao_rastreados: handoff H-0026, levantamento, QA, QA pos-patch, IMP-0027, tela/__pycache__/
bloqueios: nenhum
observacoes: nao houve commit; nao houve QA formal; nao houve aprovacao da propria entrega
```

---

## Patch pós-QA: H0026-CLOSE-O01

### Identificação

ID do achado corrigido: `H0026-CLOSE-O01`

Achado herdado de: `H0026-IMPL-QA-O01` (QA da implementação, seção 29) e
`H0026-CLOSE-O01` (verificação de fechamento, seção 19).

### Decisão explícita do usuário

O usuário decidiu remover a mensagem histórica de validação TTY real pendente
emitida pela suíte da demo, junto ao seu bloco explicativo obsoleto. A mensagem
foi herdada de ciclo anterior e não representa pendência material do H-0026. A
decisão não substitui a mensagem por outra pendência, aviso ou nova política.

### Arquivo alterado

```text
tela/teste_demo.py
```

### Descrição da alteração

Removidas as seguintes linhas de saída informativa histórica da função
`teste_redimensionamento_reativo_h0023` em `tela/teste_demo.py`:

```python
    print("")
    print("-- Validacao humana TTY real: PENDENTE --")
    print("VALIDACAO_HUMANA_TTY_REAL: PENDENTE")
    print("Criterios pendentes: reducao, ampliacao, resize rapido, residuos,")
    print("scroll, linha adicional, flicker, quadro pequeno, recuperacao,")
    print("echo, navegacao, restauracao apos Esc, estado final do terminal.")
    print("Pseudo-TTY executado: {0}".format(
        "sim" if _pseudo_pty_executado[0] else "nao (ver limitacoes)"
    ))
    if _pseudo_pty_limitacoes:
        print("Limitacoes pseudo-TTY: {0}".format("; ".join(_pseudo_pty_limitacoes)))
```

Nenhuma asserção, contador, condição de sucesso ou falha, código de saída,
validação automatizada, fixture ou comportamento funcional da demo foi alterado.

### Confirmação de preservação

Nenhum teste foi alterado. Nenhum `_registrar()` foi removido. A contagem de
verificações permanece 303/303 e a estrutura da suíte é idêntica à anterior ao
patch.

### Comando de teste executado

```bash
PYTHONDONTWRITEBYTECODE=1 python tela/teste_demo.py
```

### Resultado e código de saída

```text
Total de verificacoes: 303
Passaram: 303
Falharam: 0
exit: 0
```

### Verificação de resíduo

```bash
rg -n 'Validacao humana TTY real|Validação humana TTY real|PENDENTE' tela/teste_demo.py
```

Resultado: sem ocorrência. Código de saída do `rg`: 1 (esperado — sem match).

### Estado Git após o patch

| Comando | Resultado |
|---|---|
| `git branch --show-current` | `master` |
| `git log -1 --oneline` | `1cc0dff feat: implementa distribuicao vertical explicita do corpo` |
| `git diff --name-only` | `tela/renderizador.py`, `tela/teste_demo.py`, `tela/teste_renderizador.py` |
| `git diff --cached --stat` | sem saída (stage vazio) |
| `git diff --cached --name-only` | sem saída (stage vazio) |
| `git diff --check` | sem saída (exit 0) |

Alterações anteriores do H-0026 preservadas: `tela/renderizador.py` (+88/-1) e
`tela/teste_renderizador.py` (+484/-16). Alteração nova deste patch:
`tela/teste_demo.py` (11 remoções).

### Declaração de ausência de commit

Não houve commit. Não houve `git add`, não houve alteração de branch, não houve
push. O stage permanece vazio.

### Entrega pendente de QA pós-patch

Este patch não foi aprovado por esta etapa. A entrega ainda depende de QA
pós-patch independente antes de qualquer preparação de commit.
