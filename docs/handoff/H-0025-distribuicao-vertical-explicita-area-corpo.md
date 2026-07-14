---
name: H-0025-distribuicao-vertical-explicita-area-corpo
description: Handoff de implementacao — distribuicao vertical explicita da altura util do corpo entre filhos diretos de container vertical, modos igual/percentual/fracao conforme ADR-0018; substitui operacionalmente o H-0024 bloqueado; preserva comportamento orientado pelo conteudo quando distribuicao ausente
metadata:
  type: handoff
  status: proposto
  data: 2026-07-11
rastreabilidade:
  adr_base: docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
  adrs_preservadas:
    - docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md
    - docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md
    - docs/adr/ADR-0017-redimensionamento-reativo-tui.md
  qa_aplicacao_aprovado: docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md
  contratos_aplicaveis:
    - docs/contratos/contrato_composicao_corpo.md
    - docs/contratos/contrato_tela_json.md
    - docs/contratos/contrato_json_tela_minima.md
    - docs/contratos/contrato_processo_desenvolvimento.md
    - docs/NOMENCLATURA.md
  handoff_historico: docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
  escopo_permitido:
    - tela/loader.py
    - tela/modelo.py
    - tela/renderizador.py
    - tela/teste_loader.py
    - tela/teste_modelo.py
    - tela/teste_renderizador.py
    - tela/teste_demo.py
    - config/telas/orquestrador.json
    - docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
  escopo_somente_leitura:
    - tela/demo.py
    - docs/templates/TEMPLATE_RELATORIO_IMPL.md
  relatorio_implementacao_esperado: docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
---

# H-0025 — Distribuição vertical explícita da área do corpo

## 1. Identificação e objetivo

Implementar a **distribuição vertical explícita da altura útil do corpo entre
seus filhos diretos** quando `corpo.arranjo = "vertical"` e `corpo.distribuicao`
estiver declarado, aplicando os modos `igual`, `percentual` e `fracao` conforme
a ADR-0018 e os contratos ativos.

**Capacidade coesa (indivisível):**

> Quando `corpo.distribuicao` estiver declarado em container vertical, calcular e
> alocar a altura útil integral entre os filhos diretos nos modos `igual`,
> `percentual` e `fracao`, com preenchimento interno das molduras e soma exata das
> cotas. Quando `distribuicao` estiver ausente, preservar integralmente o
> comportamento orientado pelo conteúdo existente.

Este handoff **não** implementa código, **não** faz QA de si mesmo, **não**
decide arquitetura nova, **não** completa lacunas normativas e **não** prepara
commit. Ele é uma ordem de trabalho fechada para o executor de implementação.

---

## 2. Relação com o H-0024

### 2.1 Bloqueio histórico do H-0024

O handoff H-0024 (`docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`)
foi bloqueado durante a implementação (relatório
`docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`,
status `BLOCKED` / `ARCHITECTURE_REVIEW_REQUIRED`).

O bloqueio foi causado pela colisão entre:

- a semântica então vigente de "ausência de `corpo.distribuicao` ≡ modo `igual`";
- a regressão histórica obrigatória em `tela/teste_demo.py` que preserva o
  empilhamento orientado pelo conteúdo.

### 2.2 Resolução pela ADR-0018

A ADR-0018 (`docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`),
aprovada com notas (`ADR_APPROVED_WITH_NOTES` em
`docs/relatorios/RELATORIO_QA_ADR-0018.md`) e com a aplicação documental
aprovada (`ADR_APPLICATION_APPROVED_WITH_NOTES` em
`docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`), forneceu a
decisão arquitetural que faltava:

- **D2**: ausência de `distribuicao` preserva a construção orientada pelo
  conteúdo; não equivale a `igual`; não dispara repartição automática.
- **D3**: distribuição explícita reparte a altura útil; aloca área, não apenas
  conteúdo.
- **D4**: a sobra fica dentro das molduras dos filhos, não acumulada
  externamente.

Essa decisão eliminou a contradição normativa que causou o bloqueio.

### 2.3 Papel deste handoff

Este handoff **substitui operacionalmente** o H-0024 para a implementação.

O H-0024 **permanece preservado** como evidência histórica e **não deve ser
alterado, renomeado ou removido**.

---

## 3. Estado do repositório esperado no início da implementação

```text
branch:  master
HEAD:    3332773a3f10e716115a164148af323fa86e608f
mensagem: feat: implementa redimensionamento reativo da TUI
stage:   vazio
stash:   stash@{0}: pre-H-0022 recuperado apos drop acidental
stash SHA: 21f98d0f4a479d72e6df21b1dca1511c3ad38937
```

Arquivos não rastreados esperados no início (ciclo ADR-0018 e artefatos do
H-0024 bloqueado):

```text
?? docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md
?? docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
?? docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0018.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md
?? docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md
?? docs/relatorios/RELATORIO_QA_ADR-0018.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0018.md
?? docs/relatorios/RELATORIO_QA_H-0024_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0024_HANDOFF.md
```

Arquivos rastreados modificados (aplicação da ADR-0018 aguardando commit):

```text
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_json_tela_minima.md
 M docs/contratos/contrato_processo_desenvolvimento.md
 M docs/contratos/contrato_tela_json.md
```

O executor deve verificar esse estado antes de iniciar qualquer alteração. Se
o estado divergir, parar com `BLOCKED_REPOSITORY_STATE`.

---

## 4. Autoridades normativas obrigatórias

O executor deve ler integralmente antes de implementar:

1. `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
   (autoridade primária para este ciclo)
2. `docs/relatorios/RELATORIO_QA_POS_PATCH_APLICACAO_ADR-0018.md`
   (confirma aprovação; status `ADR_APPLICATION_APPROVED_WITH_NOTES`)
3. `docs/contratos/contrato_composicao_corpo.md` (versão com ADR-0018 aplicada)
4. `docs/contratos/contrato_tela_json.md` (versão com ADR-0018 aplicada)
5. `docs/contratos/contrato_json_tela_minima.md` (versão com ADR-0018 aplicada)
6. `docs/contratos/contrato_processo_desenvolvimento.md` (versão com ADR-0018)
7. `docs/NOMENCLATURA.md` (versão com ADR-0018 aplicada)

Autoridades relacionadas obrigatórias:

- `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md`
- `docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- `docs/adr/ADR-0017-redimensionamento-reativo-tui.md`

Somente leitura como evidência histórica (sem autoridade normativa):

- `docs/handoff/H-0024-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/IMP-0025-distribuicao-vertical-percentual-fracao-corpo.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_DISTRIBUICAO_VERTICAL_PERCENTUAL_FRACAO.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_BLOQUEIO_H-0024_JSON_ALTURA_MINIMA_STASH.md`

---

## 5. Decisões fechadas

As decisões abaixo foram tomadas pelo usuário e registradas na ADR-0018. O
executor não pode alterá-las nem completar lacunas omitidas.

### 5.1 Ausência de `distribuicao`

Quando `corpo.distribuicao` **não** estiver declarado:

- preservar a construção orientada pelo conteúdo;
- cada filho utiliza sua altura natural;
- não criar objeto `distribuicao` implicitamente;
- não converter ausência em `modo: igual`;
- não repartir automaticamente a altura entre os filhos;
- preservar o preenchimento externo já existente (ADR-0013).

Telas atuais sem distribuição declarada **não devem sofrer alteração
comportamental**.

### 5.2 Distribuição explícita

Quando `corpo.distribuicao` estiver declarado em container com
`arranjo: "vertical"`:

- calcular toda a altura útil distribuível do corpo;
- usar a região entre `cabecalho` e `barra_de_menus`;
- descontar somente linhas estruturais já determinadas pelos contratos;
- repartir essa altura entre os filhos diretos;
- garantir que a soma das cotas seja exatamente a altura distribuível;
- renderizar cada filho na altura atribuída.

A distribuição **aloca área**, não apenas tamanho do conteúdo.

### 5.3 Preenchimento interno

Se a cota atribuída a um filho for maior que seu conteúdo natural:

- a moldura ocupa toda a altura da cota;
- a sobra é preenchida por linhas em branco **dentro** da moldura;
- a sobra **não** fica acumulada externamente abaixo do último filho.

No Orquestrador real, o espaço atualmente situado entre a borda inferior de
NAVEGAR e a borda superior de Menus deve ficar dentro das áreas distribuídas
de ITENS, INFO e NAVEGAR quando `distribuicao` for declarada.

### 5.4 Modo `igual` explícito

- somente existe quando declarado;
- atribui pesos iguais aos filhos diretos;
- usa toda a área distribuível;
- **não** é fallback da ausência de `distribuicao`.

### 5.5 Modo `percentual`

- exige um valor por filho direto;
- exige soma igual a 100;
- associa valores posicionalmente à ordem declarada dos filhos;
- usa toda a área distribuível;
- aplica maiores restos e desempate normativo (ordem declarada).

### 5.6 Modo `fracao` genérico

- exige um peso positivo por filho direto;
- associa pesos posicionalmente à ordem declarada;
- usa como denominador a soma dos pesos;
- calcula cada cota proporcionalmente;
- aplica maiores restos e desempate normativo (ordem declarada);
- aceita **qualquer** vetor válido de pesos positivos.

O algoritmo **não pode** ser especializado para `[2, 1, 2]` nem para qualquer
outro vetor concreto. São exemplos de entradas que o algoritmo genérico deve
tratar sem código especial:

```text
[1, 1, 1]
[2, 1, 2]
[1, 3, 1]
[5, 2, 7]
```

### 5.7 Conteúdo maior que a cota

Quando a cota atribuída for menor que a altura natural de um filho em terminal
pequeno: **fora de escopo**. Não criar política de altura mínima, overflow,
truncamento, paginação, rejeição, degradação, redistribuição por altura natural
ou prioridade por tipo.

Um vetor válido **não** se torna inválido porque um terminal pequeno não
comporta o conteúdo.

---

## 6. JSON real do Orquestrador

### 6.1 Arquivo

```text
config/telas/orquestrador.json
```

### 6.2 Ordem dos filhos diretos (comprovada)

A ordem dos filhos diretos do `corpo` do Orquestrador foi confirmada:

```text
1. console_principal
2. dashboard_info
3. lancador_principal
```

Se essa ordem divergir no repositório real no momento da implementação, parar
com `BLOCKED_EVIDENCE`.

### 6.3 Alteração declarativa especificada

Adicionar ao objeto `corpo` do `orquestrador.json`:

```json
"distribuicao": {
  "modo": "fracao",
  "valores": [2, 1, 2]
}
```

Associação posicional pela ordem declarada:

| Posição | Filho | Peso |
|---|---|---|
| 1 | `console_principal` | 2 |
| 2 | `dashboard_info` | 1 |
| 3 | `lancador_principal` | 2 |

Esta é uma **configuração concreta** da tela Orquestrador. Não é default, não é
hardcode no renderer, não é regra especial do renderer para o Orquestrador.

### 6.4 Preservações obrigatórias

- preservar a ordem dos filhos diretos;
- preservar todos os demais campos do JSON;
- validar sintaticamente após a alteração (`python -m json.tool`);
- validar pelo loader;
- comprovar visualmente ou estruturalmente que a distribuição foi aplicada.

---

## 7. Arquivos autorizados

### 7.1 Arquivos alteráveis (lista fechada)

```text
tela/loader.py
tela/modelo.py
tela/renderizador.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_renderizador.py
tela/teste_demo.py
config/telas/orquestrador.json
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

O executor **não** deve alterar nenhum arquivo fora desta lista. Se durante a
implementação for identificado que outro arquivo de código é indispensável,
registrar a evidência no relatório IMP-0026 e parar com `BLOCKED_EVIDENCE`.

### 7.2 Arquivos somente leitura

```text
tela/demo.py
docs/templates/TEMPLATE_RELATORIO_IMPL.md
```

---

## 8. Escopo positivo obrigatório

A implementação deve cobrir:

- parsing **opcional** de `corpo.distribuicao` em `loader.py`;
- validação de `igual`, `percentual` e `fracao` no loader;
- representação da ausência de `distribuicao` sem materializar `igual`;
- preservação dos valores declarados no modelo (`modelo.py`);
- cálculo de cotas para container vertical com distribuição explícita;
- algoritmo de maiores restos para arredondamento;
- desempate por ordem declarada;
- uso da altura útil integral quando `distribuicao` for explícito;
- renderização de cada filho na cota atribuída;
- preenchimento interno com linhas em branco quando cota > conteúdo natural;
- preservação do caminho sem distribuição (altura natural por filho);
- alteração declarativa de `config/telas/orquestrador.json` conforme §6.3;
- adaptação mínima dos testes conflitantes (ver §10);
- criação do relatório de implementação `IMP-0026`;
- verificações de diff e estado Git.

---

## 9. Escopo negativo obrigatório

Declarado fora de escopo deste ciclo:

- arranjo horizontal distribuído (não é capacidade deste ciclo);
- grupos aninhados com distribuição própria (não necessários para esta entrega);
- altura mínima;
- overflow;
- truncamento;
- paginação de `lancador`;
- política para conteúdo maior que a cota;
- prioridade por tipo de elemento;
- vetor padrão global;
- hardcode de `[2, 1, 2]` no renderer;
- regra especial do renderer para o Orquestrador;
- matriz exaustiva de testes;
- novo handoff de testes separado neste ciclo;
- alteração de contratos ou ADRs;
- manipulação de stash;
- commit.

---

## 10. Testes mínimos exigidos

### 10.1 Escopo

Este ciclo exige somente a cobertura mínima necessária para comprovar a
capacidade implementada e impedir regressão imediata.

A cobertura ampla de combinações pode ser construída em handoff posterior de
testes.

### 10.2 Cobertura mínima obrigatória

Os testes mínimos devem verificar:

1. **Ausência de `distribuicao` preserva altura natural**: fixture sem
   `distribuicao` declarada; cada filho usa sua altura natural; nenhum
   preenchimento de cota é adicionado; sem regressão nas telas atuais.

2. **`igual` explícito divide igualmente**: fixture com
   `distribuicao: {"modo": "igual"}` em altura suficiente; cada filho recebe
   cota igual (com maiores restos quando necessário).

3. **`percentual` explícito**: fixture com `modo: percentual` e valores somando
   100 em altura suficiente; cotas proporcionais aos percentuais.

4. **`fracao` com `[1,1,1]`**: cota igual para todos os filhos; soma exata da
   área distribuível.

5. **`fracao` com `[2,1,2]`**: cotas nas proporções 2:1:2; soma exata.

6. **Outros vetores válidos não dependem de código especial**: o mesmo código
   que trata `[1,1,1]` e `[2,1,2]` deve tratar `[1,3,1]` e `[5,2,7]` sem
   modificação adicional. A verificação pode ser feita testando ao menos um
   terceiro vetor.

7. **Soma exata das cotas**: a soma das cotas calculadas deve ser exatamente
   igual à altura distribuível para cada fixture de distribuição.

8. **Maiores restos**: em ao menos um fixture, a altura distribuível não é
   divisível exatamente pelo denominador; os restos são distribuídos pelas
   maiores frações.

9. **Desempate por ordem declarada**: em ao menos um fixture, dois filhos têm
   frações residuais iguais; o desempate segue a ordem declarada.

10. **Preenchimento interno das molduras**: quando cota > altura natural do
    filho, a saída renderizada do filho ocupa exatamente `cota` linhas;
    as linhas sobrantes ficam dentro da moldura.

11. **Sobra não fica abaixo do último filho**: a soma das linhas renderizadas
    de todos os filhos com distribuição explícita deve ser exatamente a altura
    distribuível; nenhuma linha de espaço vazio externa ao último filho.

12. **JSON real do Orquestrador com `[2,1,2]`**: após a alteração do JSON,
    o cenário real deve distribuir a área entre ITENS, INFO e NAVEGAR;
    verificação visual ou estrutural da distribuição.

13. **Redimensionamento**: em ao menos um cenário com distribuição explícita,
    um redimensionamento para outra altura suficiente recalcula as cotas
    corretamente.

14. **Arranjo horizontal não sofre regressão**: nenhum container horizontal
    existente muda de comportamento.

15. **Telas sem `distribuicao` explícita não sofrem alteração**: os testes
    existentes das telas sem distribuição continuam passando.

### 10.3 Itens não exigidos neste ciclo

Não exigir neste ciclo:

- matriz exaustiva de vetores;
- todas as alturas possíveis;
- todas as quantidades de filhos;
- terminais onde a cota é menor que o conteúdo;
- política de mínimo ou overflow;
- teste combinatório completo.

---

## 11. Teste histórico de altura 15

### 11.1 Identificação precisa

**Arquivo:** `tela/teste_demo.py`

**Função:** `teste_renderizar_estado_altura` (linha 679)

**Trecho problemático:** linhas 695–709

**Conteúdo:**

```python
# CA-01 / CA-03: altura minima (15) sem preenchimento, saida identica
# ao comportamento natural (sem altura). H-0016: com a barra horizontal
# responsiva em 1 linha, L_barra=3 e n_minimo=15.
res_16 = renderizar_estado(
    estado_curva, modelo, largura=42, altura=15
)
_registrar(
    "renderizar_estado(..., altura=15) -> 15 linhas (sem fill)",
    res_16.count("\n") == 15,
    "count={0}".format(res_16.count("\n")),
)
_registrar(
    "renderizar_estado(..., altura=15) == renderizar_estado(..., largura=42)",
    res_16 == renderizar_estado(estado_curva, modelo, largura=42),
)
```

### 11.2 Modelo utilizado

A função recebe `modelo` passado de linha 2986:

```python
modelo = _carregar_modelo()  # carrega orquestrador.json
teste_renderizar_estado_altura(modelo)
```

Portanto o modelo carregado é o **orquestrador real** a partir de
`config/telas/orquestrador.json`.

### 11.3 Expectativa antiga e por que não pode bloquear

**Expectativa antiga:**

1. `res_16.count("\n") == 15` — com largura=42, o conteúdo natural do
   orquestrador ocupa 15 linhas (barra de menus em 3 linhas a essa largura +
   conteúdo dos elementos). Sem distribuição e sem fill, a saída tem exatamente
   15 newlines.

2. `res_16 == renderizar_estado(estado_curva, modelo, largura=42)` — a saída em
   altura=15 é idêntica à saída sem restrição de altura (conteúdo natural).

**Por que não pode bloquear:**

Após declarar `distribuicao: {"modo": "fracao", "valores": [2, 1, 2]}` em
`orquestrador.json`, o modelo carregado por `_carregar_modelo()` terá
distribuição explícita. A `altura=15` com distribuição declarada é o cenário
de **terminal insuficiente** (a cota atribuída a algum filho pode ser menor
que sua altura natural), que está **explicitamente fora de escopo** pela D8 da
ADR-0018.

Essas duas asserções não podem continuar bloqueando a implementação da
distribuição explícita porque:

- a height=15 não é a altura normal de operação — é um terminal insuficiente
  para o conteúdo do orquestrador com distribuição;
- o vetor `[2, 1, 2]` é matematicamente válido; sua invalidade só existiria
  se altura=15 fosse a única altura possível, o que não é o caso;
- a política para terminal insuficiente permanece fora de escopo e não pode
  ser decidida aqui.

### 11.4 Precedente de altura suficiente

A altura padrão de teste já estabelecida no repositório é:

```python
_ALTURA_SUBPROCESS = 24  # tela/teste_demo.py:139
```

Essa constante é usada nos testes de integração via subprocess e representa a
altura do terminal fallback (`shutil.get_terminal_size(fallback=(80, 24))`).
A asserção `renderizar_estado(..., largura=42, altura=24) -> 24 linhas` (linha
690) já confirma que altura=24 é suficiente para o conteúdo natural.

Portanto: **altura=24 é o precedente objetivo disponível no repositório** para
substituir a fixture de altura=15 no cenário que usa o modelo do orquestrador
com distribuição declarada.

### 11.5 Alteração mínima permitida

A correção deve:

1. Substituir o sub-cenário `altura=15` (linhas 695–709) **por um cenário que
   use um modelo sem `distribuicao` declarada** (fixture isolada, carregada de
   uma tela sem distribuição ou construída manualmente no teste), preservando a
   cobertura de "saída em altura insuficiente = saída natural sem fill".

   **OU**, se essa substituição não for viável sem criar política de terminal
   insuficiente, simplesmente remover o sub-cenário `altura=15` e adicionar um
   sub-cenário com `altura=24` usando o modelo do orquestrador com distribuição
   declarada, verificando que as cotas foram aplicadas.

2. Em nenhum caso: criar política de altura mínima; afirmar que altura=15 é
   suportada pela nova distribuição; esconder falha real em terminal suficiente;
   remover cobertura de redimensionamento do H-0023.

### 11.6 O que não é permitido

- Alterar o algoritmo para produzir saída idêntica à saída natural em altura=15
  quando há distribuição declarada (isso seria criar regra para terminal
  insuficiente).
- Tratar o vetor `[2, 1, 2]` como inválido por causa de altura=15.
- Remover os testes de `teste_redimensionamento_reativo_h0023` (função linha
  1716) para compensar.

---

## 12. Critérios de aceite

O executor deve verificar todos os critérios abaixo antes de criar o relatório
IMP-0026:

| # | Critério |
|---|---|
| 1 | JSON sem `distribuicao` continua válido e carregado corretamente |
| 2 | Ausência de `distribuicao` não gera `modo: igual` nem objeto `distribuicao` |
| 3 | `igual` explícito divide a área distribuível igualmente (com maiores restos) |
| 4 | `percentual` exige soma 100; rejeita soma diferente |
| 5 | `fracao` aceita qualquer vetor de pesos positivos |
| 6 | Quantidade de valores/pesos corresponde ao número de filhos diretos |
| 7 | Valores/pesos preservam associação posicional com a ordem declarada |
| 8 | Soma das cotas é exatamente igual à área distribuível |
| 9 | Maiores restos aplicados corretamente |
| 10 | Empates de restos resolvidos pela ordem declarada |
| 11 | A moldura de cada filho ocupa sua cota integralmente |
| 12 | Linhas sobrantes ficam dentro da moldura do filho |
| 13 | Nenhuma linha de espaço vazio fica abaixo do último filho quando há distribuição |
| 14 | O caminho sem `distribuicao` preserva comportamento orientado pelo conteúdo |
| 15 | Vetor `[1,1,1]` é aceito e processado corretamente |
| 16 | Vetor `[2,1,2]` é aceito e processado corretamente |
| 17 | Outros vetores válidos (ex.: `[1,3,1]`, `[5,2,7]`) são processados pelo mesmo código genérico |
| 18 | `config/telas/orquestrador.json` declara `[2,1,2]` após a alteração |
| 19 | `config/telas/orquestrador.json` permanece sintaticamente válido |
| 20 | O loader preserva a declaração de distribuição do JSON real |
| 21 | O modelo preserva os valores de distribuição sem conversão implícita |
| 22 | O cenário real distribui a área entre ITENS, INFO e NAVEGAR |
| 23 | Telas sem `distribuicao` explícita não sofrem alteração de comportamento |
| 24 | Arranjo horizontal não sofre regressão |
| 25 | Nenhuma política de altura mínima ou overflow foi introduzida |
| 26 | A asserção de altura=15 não é usada para invalidar vetor matematicamente válido |
| 27 | Todos os testes mínimos definidos na §10.2 passam |
| 28 | Nenhum arquivo fora da lista fechada da §7.1 foi alterado |

---

## 13. Comandos obrigatórios

Os comandos abaixo devem ser executados durante e ao final da implementação.

**Validação sintática do JSON após alteração:**

```bash
python -m json.tool config/telas/orquestrador.json
```

**Suítes de teste:**

```bash
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_demo.py
```

**Verificações Git:**

```bash
git diff --check
git diff --stat
git diff --name-only
git status --short
```

**Verificação do handoff como arquivo novo (código 1 esperado):**

```bash
git diff --no-index /dev/null docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
```

**Verificação do relatório como arquivo novo (código 1 esperado):**

```bash
git diff --no-index /dev/null docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

---

## 14. Relatório de implementação exigido

O executor deve criar ao final:

```text
docs/relatorios/IMP-0026-distribuicao-vertical-explicita-area-corpo.md
```

O relatório deve registrar:

- relação com H-0024 e bloqueio histórico;
- ADR-0018 e aprovação do QA da aplicação;
- arquivos alterados (lista fechada);
- comportamento sem distribuição: o que foi preservado;
- comportamento com distribuição explícita: o que foi implementado;
- algoritmo genérico (maiores restos, desempate);
- modos implementados (`igual`, `percentual`, `fracao`);
- alteração do JSON real e associação `[2,1,2]`;
- testes mínimos executados e resultado;
- eventual alteração do cenário de altura=15 e justificativa;
- limitações de terminal insuficiente (fora de escopo);
- itens não testados neste ciclo (diferidos para handoff de testes);
- estado Git ao final;
- stash preservado (SHA `21f98d0f4a479d72e6df21b1dca1511c3ad38937`);
- validação manual visual, se realizada;
- bloqueios encontrados (se houver).

---

## 15. Condições de bloqueio

O executor deve parar com `BLOCKED_EVIDENCE` se:

- o JSON real tiver ordem de filhos diferente da comprovada na §6.2;
- for necessário hardcodar um vetor concreto no renderer;
- ausência de `distribuicao` precisar ser convertida em `igual` para a
  implementação funcionar;
- a implementação exigir decisão de altura mínima;
- a implementação exigir política de overflow;
- for necessário alterar contrato ou ADR;
- for necessário alterar arquivo fora da lista fechada da §7.1;
- o teste de altura=15 só puder passar mediante criação de política normativa
  ausente.

O executor deve parar com `BLOCKED_REPOSITORY_STATE` se:

- o estado Git no início divergir do descrito na §3;
- o stash não resolver para `21f98d0f4a479d72e6df21b1dca1511c3ad38937`;
- existir operação Git ativa (MERGE_HEAD, REBASE_HEAD etc.);
- outra sessão estiver modificando o workspace.

O executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED` se:

- surgir contradição entre a ADR-0018 e os contratos ativos que não possa ser
  resolvida dentro do escopo autorizado.

---

## 16. Verificações documentais deste handoff

```bash
git diff --check
git status --short
git diff --no-index /dev/null docs/handoff/H-0025-distribuicao-vertical-explicita-area-corpo.md
```

O código de saída 1 é esperado para o último comando (arquivo novo com
conteúdo). Essas verificações não constituem QA formal.

---

## 17. Encerramento desta etapa

Criado somente este arquivo de handoff. Nenhuma outra alteração foi realizada
nesta etapa.

O executor de implementação deve:

1. verificar o estado do repositório (§3);
2. ler as autoridades obrigatórias (§4);
3. implementar o escopo positivo (§8) nos arquivos autorizados (§7.1);
4. executar os testes mínimos (§10) e todos os comandos obrigatórios (§13);
5. criar o relatório IMP-0026 (§14);
6. parar em qualquer condição de bloqueio (§15).

Não fazer QA do handoff, não alterar o H-0024, não alterar JSON fora da §6.3,
não alterar código antes de verificar o estado, não manipular stash, não
preparar commit.
