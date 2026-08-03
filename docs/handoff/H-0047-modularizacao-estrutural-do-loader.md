---
name: H-0047-modularizacao-estrutural-do-loader
description: "Handoff 2/3 da ADR-0039 — modularizacao estrutural de tela/loader.py para tela/carregamento/, preservando a fachada publica e o comportamento observavel"
metadata:
  type: handoff
  id: H-0047
  ADR: ADR-0039
  item: ITEM-0022
  sequencia: "2/3"
  status: criado
---

# H-0047 — Modularização estrutural de `tela/loader.py`

## 1. Estado transportado

```yaml
projeto: Orquestrador
ADR:
  id: ADR-0039
  status: aceita
item:
  id: ITEM-0022
  estado: em_andamento
sequencia:
  passo_1:
    handoff: H-0046
    objeto: modularizacao_estrutural_de_tela_renderizador
    estado: concluido
    commit: 998a133
    testes: 970_passed
  passo_2:
    handoff: H-0047
    objeto: modularizacao_estrutural_de_tela_loader
    estado: atual
  passo_3:
    objeto: reorganizacao_de_tela_teste_renderizador_e_testes_relacionados
    estado: futuro
    dependencia: fechamento_validado_do_passo_2
baseline_confirmado:
  branch: master
  HEAD: 998a133c49d86d4227a467f9b572050debc679dd
  stage: vazio
  alteracoes_rastreadas_pendentes: nenhuma
  residuos_nao_confirmados:
    - tela/__pycache__/__init__.cpython-314.pyc
    - tela/__pycache__/distribuicao_matricial.cpython-314.pyc
    - tela/__pycache__/loader.cpython-314.pyc
    - tela/__pycache__/modelo.cpython-314.pyc
    - tela/__pycache__/renderizador.cpython-314.pyc
```

Este handoff não reabre a arquitetura fechada pelo H-0046 (`tela/renderizacao/`) e
não altera `tela/renderizacao/` nem `tela/renderizador.py` sem defeito material
novo comprovado. É estritamente estrutural (D-MOD-02). Não inicia a
reorganização de `tela/teste_renderizador.py` prevista para o Handoff 3.

---

## 2. Capacidade coesa

Modularizar estruturalmente `tela/loader.py` em módulos internos coesos sob
`tela/carregamento/`, preservando `tela/loader.py` como fachada pública
compatível, sem alteração funcional, normativa ou observável.

---

## 3. Diagnóstico factual

### 3.1 Tamanho e forma atual

`tela/loader.py` tem **3143 linhas** (`wc -l` confirmado), 12 classes de
exceção, ~55 funções de nível superior e ~25 constantes/estruturas de módulo.
Imports de nível superior: `json`, `os` (stdlib), `dataclasses.dataclass`,
`pathlib.Path`. **Nenhum** `import` de outro módulo do pacote `tela` — o
loader não importa `tela.modelo`, `tela.renderizador`, `tela.navegacao`,
`tela.paginacao` nem `tela.selecao`. Diferente do renderizador (H-0046), o
loader **não possui nenhum `global`** e nenhum estado de runtime mutável
compartilhado entre funções — busca `rg -n '^\s*global '` no arquivo devolve
vazio. Isso remove inteiramente a classe de risco que motivou
`contexto_execucao.py` no H-0046: não há necessidade de módulo proprietário
de estado mutável cross-módulo nesta modularização.

### 3.2 Responsabilidades concretas encontradas (levantamento AST)

Levantamento AST (símbolos e intervalos de linha) identificou blocos coesos
distintos, na ordem em que aparecem no arquivo:

1. **Constantes de taxonomia do schema** — `TIPOS_CORPO_VALIDOS` (L26),
   `TIPOS_ESTRUTURAIS_VALIDOS` (L32), `ARRANJOS_CORPO_VALIDOS` (L38),
   `MODOS_DISTRIBUICAO_CORPO_VALIDOS` (L43), `ESTRUTURAS_GRUPO_VALIDAS` (L45),
   `PERFIL_RESULTADO_EXECUCAO` (L50).
2. **Hierarquia de exceções** (domínio `Tela*` + `EstiloErro`) — `TelaErro`
   até `EstiloErro` (L77-175).
3. **Resolução de caminho base** — `_caminho_padrao_base` (L178-180),
   `_para_base` (L838-843).
4. **Validação de `corpo.distribuicao`** (H-0025/ADR-0018) —
   `_eh_numero_nao_bool`, `_validar_distribuicao_corpo` (L183-261).
5. **Validação de `distribuicao_matricial`** (H-0035/ADR-0025, 26 caminhos) —
   constantes `_DM_*` e funções `_dm_int` até `_validar_distribuicao_matricial`
   (L268-563).
6. **Carregamento da config de `lancador`** (H-0034/ADR-0023) —
   `_carregar_e_validar_config_lancador` (L633-835).
7. **Validação do tipo estrutural `grupo`** (ADR-0019/H-0027, inclui matriz de
   grupo ADR-0020) — `_validar_quantidade_matriz` até `_validar_grupo`
   (L846-1181).
8. **Perfil `resultado_execucao`** (H-0043/ADR-0036) —
   `_CAMPOS_CONSOLE_RESULTADO_PERMITIDOS`,
   `_CAMPOS_CLASSICOS_PROIBIDOS_RESULTADO` (L54-74),
   `_validar_perfil_resultado_execucao` (L1184-1340).
9. **Orquestração macro de `tela.json`** — `_tem_lancador_em_elementos`,
   `_iterar_consoles_do_corpo`, `_validar_unicidade_ids_consoles` (L566-630),
   `_ID_TELA_RAIZ` (L47), `_PERFIL_AUSENTE` (L51), `carregar_tela`
   (L1343-1560).
10. **Compatibilidade com envelope pré-ADR-0028** (H0037-IMPL-QAPP5-001) —
    `_TELAS_LEGADAS_D23` (L1635-1646), `_TELAS_VARIANTE2_LEGADAS` (L1659),
    `_CAMPOS_ENVELOPE_PRE_ADR_0028` (L1670-1678),
    `_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028` (L1692-1699),
    `_POLITICA_SELECAO_VALIDOS`, `_POLITICA_PAGINACAO_VALIDOS` (L1702-1703),
    `_validar_valores_envelope_pre_adr_0028` (L1706-1788),
    `_console_em_escopo_d23` (L1791-1964).
11. **Validação D23 de política de modo** (H-0037/ADR-0028) —
    `_POLITICAS_MODO_VALIDAS`, `_MODOS_INICIAIS_VALIDOS` (L1622-1625),
    `_validar_d23_console` (L2058-2124).
12. **Validação e carregamento de conteúdo externo multinível** (H-0036/
    ADR-0026/ADR-0027) — constantes `APRESENTACOES_CONTEUDO_VALIDAS` até
    `_CAMPOS_COLUNA_RECONHECIVEL` (L1579-2022), `_validar_designador_conteudo`,
    `_rejeitar_resultados_fisicos_conteudo`, `_coluna_reconhecivel`,
    `_validar_no_conteudo`, `validar_conteudo_externo`,
    `carregar_conteudo_externo` (L1967-2689).
13. **Materialização do estilo global** (H-0039/ADR-0030) —
    `EstiloResolvido`, `carregar_estilo` e os 11 resolvedores privados
    (L2705-3143).

Estes 13 blocos são orientação do levantamento — a arquitetura-alvo (seção 4)
não cria um módulo por bloco de forma automática; agrupa por coesão e grafo
real de chamadas, conforme decisão fechada 7 do prompt de criação.

### 3.3 Relações de chamada relevantes

- `carregar_tela` (bloco 9) chama diretamente: `_para_base`, `_validar_grupo`
  (bloco 7), `_validar_distribuicao_matricial` (bloco 5, para elementos
  funcionais diretos do corpo), `_console_em_escopo_d23` e `_validar_d23_console`
  (blocos 10/11, para elementos `console` diretos do corpo),
  `_validar_unicidade_ids_consoles`, `_validar_distribuicao_corpo` (bloco 4),
  `_validar_perfil_resultado_execucao` (bloco 8), `_tem_lancador_em_elementos`,
  `_carregar_e_validar_config_lancador` (bloco 6).
- `_validar_grupo` (bloco 7) chama `_validar_matriz_grupo` (que chama
  `_validar_quantidade_matriz`, `_validar_distribuicao_matriz` — esta última
  chama `_validar_distribuicao_corpo`, bloco 4 — e `_validar_celulas_matriz`),
  `_validar_distribuicao_corpo` (bloco 4, para grupos não-matriz) e
  `_validar_distribuicao_matricial` (bloco 5, para elementos funcionais
  internos de grupo). **Fato estrutural verificado**: `_validar_grupo` **não**
  chama `_validar_d23_console` nem `_console_em_escopo_d23` para consoles
  internos de grupo — apenas `carregar_tela` aplica D23 aos elementos diretos
  do corpo raiz. Este é um comportamento pré-existente do código real, não
  alterado por esta modularização (D-MOD-02); registrado aqui como fato
  estrutural, não como defeito a corrigir.
- `_validar_perfil_resultado_execucao` (bloco 8) chama `_console_em_escopo_d23`
  (bloco 10).
- `_console_em_escopo_d23` (bloco 10) chama `_validar_valores_envelope_pre_adr_0028`
  (mesmo bloco) e lê `_TELAS_LEGADAS_D23`, `_TELAS_VARIANTE2_LEGADAS`,
  `_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028`.
- `_validar_d23_console` (bloco 11) lê `_TELAS_LEGADAS_D23` (bloco 10) e
  `_POLITICAS_MODO_VALIDAS`/`_MODOS_INICIAIS_VALIDOS` (mesmo bloco).
- `carregar_conteudo_externo` (bloco 12) chama `_para_base` e
  `validar_conteudo_externo` (mesmo bloco). `validar_conteudo_externo` chama
  `_validar_designador_conteudo`, `_rejeitar_resultados_fisicos_conteudo`,
  `_validar_no_conteudo` (recursiva) e `_coluna_reconhecivel` (mesmo bloco).
  **Nenhuma função do bloco 12 é chamada por `carregar_tela`** — é um ponto de
  entrada irmão, não subordinado à orquestração macro da tela.
- `carregar_estilo` (bloco 13) chama `_para_base` e os 11 resolvedores
  privados do mesmo bloco. Ponto de entrada irmão, sem relação de chamada com
  os blocos 1-12.

### 3.4 Símbolos compartilhados por mais de uma responsabilidade

- `TelaEstruturaInvalida` (e, em menor grau, `TelaCampoObrigatorioAusente`,
  `TelaArquivoNaoEncontrado`, `TelaJsonInvalido`) é levantada em praticamente
  todos os blocos 4-12 — exige módulo de exceções sem dependências, importável
  por todos.
- `_TELAS_LEGADAS_D23` (definida no bloco 10) é lida tanto por
  `_console_em_escopo_d23` (mesmo bloco) quanto por `_validar_d23_console`
  (bloco 11) — a definição permanece no bloco 10; o bloco 11 depende dele
  (ver §4.3).
- `TIPOS_CORPO_VALIDOS` é lido por `carregar_tela` (bloco 9), `_validar_grupo`
  (bloco 7) e por `tela/modelo.py` (consumidor externo, via fachada).
  `ARRANJOS_CORPO_VALIDOS` é lido por `carregar_tela` (bloco 9) e
  `_validar_grupo` (bloco 7). Isso exige que as constantes de taxonomia vivam
  num módulo-base sem dependências, comum aos dois consumidores internos, para
  não criar aresta entre a orquestração macro e a validação de grupo além da
  já existente (`carregar_tela` → `_validar_grupo`).
- `PERFIL_RESULTADO_EXECUCAO` é lido por `carregar_tela` (bloco 9),
  `_validar_perfil_resultado_execucao` (bloco 8) e por dois consumidores
  externos (`tela/resultado_execucao.py`, `tela/teste_resultado_execucao.py`).
- `_para_base` (bloco 3) é chamado por `carregar_tela` (bloco 9),
  `carregar_conteudo_externo` (bloco 12) e `carregar_estilo` (bloco 13) — três
  pontos de entrada irmãos que não têm nenhuma outra relação entre si.

### 3.5 Consumidores públicos confirmados (via busca focal)

Busca `rg -n 'from tela\.loader import|import tela\.loader|tela\.loader\.'
tela demo` confirma consumidores em `tela/*.py`, `tela/teste_*.py`,
`demo/*.py` e `demo/teste_*.py`. Símbolos efetivamente importados de
`tela.loader` por código fora do arquivo (imports de nível de módulo e
imports locais dentro de função, ambos contam como consumo real):

```text
carregar_tela, carregar_estilo, carregar_conteudo_externo,
validar_conteudo_externo, EstiloResolvido, EstiloErro,
TelaErro, TelaArquivoNaoEncontrado, TelaJsonInvalido,
TelaCampoObrigatorioAusente, TelaIdNaoCoincideComArquivo, TelaIdIncorreto,
TelaEstruturaInvalida, TelaElementoSemId, TelaElementoSemTipo,
TelaTipoDesconhecido, TelaGrupoInvalido,
TIPOS_CORPO_VALIDOS, TIPOS_ESTRUTURAIS_VALIDOS, ARRANJOS_CORPO_VALIDOS,
MODOS_DISTRIBUICAO_CORPO_VALIDOS, PERFIL_RESULTADO_EXECUCAO,
_validar_d23_console, _console_em_escopo_d23
```

Os dois últimos são símbolos privados consumidos diretamente por
`tela/teste_loader.py` (L3323 e L3638) — não como monkeypatch de ponto de
chamada interno (categoria (b) do H-0046), mas como invocação direta de
função para teste unitário isolado. Isso não cria risco de "chamador e
chamado precisam coabitar o mesmo módulo": o teste importa a função e a
invoca com argumentos sintéticos, sem espionar uma chamada interna feita por
outra função do loader.

Consumidores externos concretos confirmados: `tela/modelo.py`,
`tela/resultado_execucao.py`, `tela/fluxo_execucao.py`,
`tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_navegacao.py`,
`tela/teste_paginacao.py`, `tela/teste_fluxo_execucao.py`,
`tela/teste_resultado_execucao.py`, `tela/teste_renderizador.py` (consumo
apenas via fachada, sem inspeção de fonte do loader — ver §3.6),
`demo/demo.py`, `demo/demo_selecao.py`, `demo/demo_navegacao.py`,
`demo/demo_distribuicao.py`, `demo/diagnostico.py`,
`demo/explorar_barra_de_menus.py`, `demo/teste_demo*.py`,
`demo/teste_diagnostico.py`, `demo/teste_explorar_barra_de_menus.py`.

### 3.6 Riscos de compatibilidade whitebox/monkeypatch — nenhum material encontrado

Busca `rg -n 'loader\.py|tela\.loader|read_text|inspect|getsource|monkeypatch|
patch\(' tela/teste_loader.py tela/teste_*.py demo/teste_*.py`, seguida de
inspeção nominal dos resultados, confirma:

- **Nenhum teste lê `tela/loader.py` como texto puro** (`Path(...).read_text()`
  seguido de asserção de substring). A busca por `"tela/loader.py"` (caminho
  literal) em qualquer `.py` do repositório devolve vazio, exceto dentro do
  próprio `tela/teste_loader.py` como referência textual em docstring/print
  (`"Diagnostico H-0001 - loader/validador de tela.json"`) — não é inspeção de
  fonte. Diferente do H-0046 (que teve três funções de teste inspecionando
  `tela/renderizador.py` como texto), **não há teste equivalente para
  `tela/loader.py`** — nenhum ajuste de teste do tipo (a) do H-0046 é
  necessário aqui.
- **Um único monkeypatch por string do atributo `tela.loader.carregar_tela`**
  existe: `tela/teste_resultado_execucao.py::test_carregamento_unico_e_modelo_em_memoria`
  (L588) faz `monkeypatch.setattr("tela.loader.carregar_tela", spy_tela)`.
  Este mesmo teste **também** faz
  `monkeypatch.setattr("tela.resultado_execucao.carregar_tela", spy_tela)`
  (L587) — que é o patch materialmente ativo, pois `tela/resultado_execucao.py`
  chama `carregar_tela(...)` (L330) resolvendo o nome no namespace do próprio
  módulo `tela.resultado_execucao` (onde `from tela.loader import carregar_tela`
  já bindou uma referência própria), não através de `tela.loader.carregar_tela`
  a cada chamada. O patch em `tela.loader.carregar_tela` é redundante/inerte
  para o comportamento observado do teste — mas precisa continuar **resolvendo
  sem erro** (`setattr` num atributo de módulo existente). Isso é satisfeito
  trivialmente pela reexportação da fachada (seção 5): nenhum ajuste de teste
  é necessário, apenas a garantia de que `carregar_tela` continue sendo
  atributo settable de `tela.loader` após a extração — o que a fachada
  garante por construção (import nominal, sem indireção).
- `tela/teste_loader.py` faz `from tela import loader` (L37) mas **não usa**
  `loader.<atributo>` em nenhum ponto do arquivo (confirmado por busca —
  a única outra ocorrência da palavra `loader.py` é um comentário textual em
  L3814, não código). O import do módulo inteiro permanece válido após a
  extração (o módulo `tela.loader` continua existindo como fachada), sem
  ajuste necessário.

**Conclusão da seção**: ao contrário do H-0046, esta modularização **não
exige nenhum ajuste focal de teste**. A lista de arquivos de teste autorizados
para ajuste (seção 6.3) é vazia.

### 3.7 Imports usados por `tela/modelo.py`

`tela/modelo.py` importa exclusivamente
`from tela.loader import TIPOS_CORPO_VALIDOS, TIPOS_ESTRUTURAIS_VALIDOS`
(única linha de import de `tela.loader` no arquivo, L23). Nenhum outro
símbolo do loader é consumido pelo modelo. `tela/modelo.py` não é alterado
por este handoff (D-MOD-04) e continua importando pelo caminho público
`tela.loader` — nunca por `tela.carregamento.*`.

### 3.8 Ciclos possíveis

O loader não importa `tela.modelo`, `tela.renderizador`, `tela.renderizacao.*`,
`tela.navegacao`, `tela.paginacao` nem `tela.selecao` — confirmado pela busca
`rg -n 'from tela\.loader import|import tela\.loader|from tela\.modelo import|
import tela\.modelo' tela`, cujo único resultado relevante do lado do loader é
`tela/modelo.py` importando **de** `tela.loader` (direção única,
modelo → loader). Nenhum módulo interno de `tela/carregamento/` precisará
importar `tela.modelo` nem qualquer módulo de `tela.renderizacao/` — a
arquitetura-alvo (seção 4) preserva essa ausência total de dependência
externa ao próprio pacote `tela.carregamento`, exceto a stdlib (`json`, `os`,
`dataclasses`, `pathlib`). O risco de ciclo é, portanto, estritamente interno
ao grafo de `tela/carregamento/` (coberto pela prova da seção 7).

### 3.9 Defeito estrutural observado (registrado, não corrigido)

`_CAMPOS_ENVELOPE_PRE_ADR_0028` (L1670-1678) é uma constante materializada e
nomeada como se fosse consumida pela lógica de compatibilidade do envelope
pré-ADR-0028, mas **nenhuma função do arquivo a referencia** — a lógica real
usa exclusivamente `_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028` (L1692-1699), um
subconjunto de 6 dos 7 campos (sem `itens`). Fora do loader, o único hit é um
comentário em `tela/teste_loader.py` (L3526), não código executável. Este é
um defeito estrutural pré-existente (constante morta), não introduzido nem
corrigido por esta modularização (D-MOD-02) — permanece materializado em
`tela/carregamento/envelope_pre_adr_0028.py` (seção 4), preservando byte a
byte o comportamento observável, e é registrado aqui para deferimento
(seção 9 do relatório de implementação futuro).

### 3.10 Pontos que não podem ser extraídos isoladamente

Nenhum símbolo do loader exige tratamento especial equivalente ao
`_navegacao_atual`/`_quadro_minimo_lancador_ativo` do H-0046 (ausência de
`global`, §3.1). O único cuidado estrutural real é de **direção de
dependência**, não de identidade de estado:

- `TIPOS_CORPO_VALIDOS`, `ARRANJOS_CORPO_VALIDOS`, `TIPOS_ESTRUTURAIS_VALIDOS`,
  `MODOS_DISTRIBUICAO_CORPO_VALIDOS`, `ESTRUTURAS_GRUPO_VALIDAS`,
  `PERFIL_RESULTADO_EXECUCAO` precisam de um módulo-base sem dependências
  internas, comum aos módulos de orquestração macro e de validação de grupo,
  para que nenhum dos dois precise importar do outro apenas para reaproveitar
  vocabulário (mesmo raciocínio do `texto_ansi.py`/`contexto_execucao.py` do
  H-0046, §3.3 daquele handoff).
- `_TELAS_LEGADAS_D23` precisa de um único módulo proprietário
  (`envelope_pre_adr_0028.py`, §4), do qual o módulo de validação D23
  (`d23_console.py`) depende — nunca o inverso, pois `_console_em_escopo_d23`
  não chama `_validar_d23_console`.
- `TelaEstruturaInvalida` e as demais exceções precisam de um módulo-base sem
  dependências, importável por todos os módulos de validação.

---

## 4. Arquitetura-alvo nominal

### 4.1 Novos arquivos em `tela/carregamento/`

```text
tela/carregamento/__init__.py
tela/carregamento/erros.py
tela/carregamento/taxonomia.py
tela/carregamento/caminho_base.py
tela/carregamento/distribuicao_corpo.py
tela/carregamento/validacao_matricial.py
tela/carregamento/lancador_config.py
tela/carregamento/grupos.py
tela/carregamento/envelope_pre_adr_0028.py
tela/carregamento/d23_console.py
tela/carregamento/perfil_resultado_execucao.py
tela/carregamento/conteudo_externo.py
tela/carregamento/estilo.py
tela/carregamento/tela_json.py
```

`tela/carregamento/__init__.py` fica vazio (apenas marca o pacote) — nenhuma
lógica nem reexportação nele; a reexportação pública vive exclusivamente em
`tela/loader.py` (D-MOD-04), mesma política do H-0046 (§3.1).

`validacao_matricial.py` não colide com o módulo já existente
`tela/distribuicao_matricial.py` (motor geométrico do renderer, consumido por
`tela/renderizacao/matriz_participantes.py`): são pacotes plenamente
qualificados distintos (`tela.carregamento.validacao_matricial` ×
`tela.distribuicao_matricial`), sem relação de import entre si — o loader
apenas **valida** a declaração `distribuicao_matricial` do JSON; não calcula
geometria.

### 4.2 Responsabilidade e símbolos de cada módulo

**`erros.py`** — hierarquia de exceções do domínio, sem dependências.
- `TelaErro`, `TelaArquivoNaoEncontrado`, `TelaJsonInvalido`,
  `TelaCampoObrigatorioAusente`, `TelaIdNaoCoincideComArquivo`,
  `TelaIdIncorreto`, `TelaEstruturaInvalida`, `TelaElementoSemId`,
  `TelaElementoSemTipo`, `TelaTipoDesconhecido`, `TelaGrupoInvalido`,
  `EstiloErro` (hoje L77-175).
- Sem dependência de outro módulo interno — inclusive de `tela_json.py`
  (ver abaixo).
- **Fechamento H0047-QA-004**: `TelaIdIncorreto.__init__(self, encontrado,
  esperado="orquestrador")` usa o **literal** `"orquestrador"` como default
  do parâmetro `esperado`, não uma referência a `_ID_TELA_RAIZ` (proprietário
  nominal único: `tela_json.py`). A duplicação do valor entre os dois módulos
  é deliberada: preserva `erros.py` como módulo-base sem nenhuma dependência
  interna, sem criar aresta `erros.py` → `tela_json.py`. Assinatura, valor
  default e mensagem de erro permanecem idênticos ao código atual
  (`tela/loader.py:112-122`). Prova reproduzível na seção 7, comando 9.

**`taxonomia.py`** — vocabulário fechado de valores válidos do schema macro de
`tela.json`, sem lógica de validação.
- `TIPOS_CORPO_VALIDOS` (L26), `TIPOS_ESTRUTURAIS_VALIDOS` (L32),
  `ARRANJOS_CORPO_VALIDOS` (L38), `MODOS_DISTRIBUICAO_CORPO_VALIDOS` (L43),
  `ESTRUTURAS_GRUPO_VALIDAS` (L45), `PERFIL_RESULTADO_EXECUCAO` (L50).
- Sem dependência de outro módulo interno.

**`caminho_base.py`** — resolução do diretório-raiz do repositório para os três
pontos de entrada de carregamento.
- `_caminho_padrao_base` (L178-180), `_para_base` (L838-843).
- Depende de: stdlib (`pathlib.Path`) apenas. Sem dependência de outro módulo
  interno.

**`distribuicao_corpo.py`** — validação de `corpo.distribuicao` (H-0025/ADR-0018).
- `_eh_numero_nao_bool`, `_validar_distribuicao_corpo` (L183-261).
- Depende de: `erros.py` (`TelaEstruturaInvalida`), `taxonomia.py`
  (`MODOS_DISTRIBUICAO_CORPO_VALIDOS`).

**`validacao_matricial.py`** — validação dos 26 caminhos de
`distribuicao_matricial` (H-0035/ADR-0025). Não calcula geometria; apenas
valida a declaração.
- Constantes `_DM_CAMPOS_VALIDOS`, `_DM_FORMACAO_POLITICAS`, `_DM_ORDENS`,
  `_DM_DIM_COLUNAS`, `_DM_DIM_LINHAS`, `_DM_DIST_H`, `_DM_DIST_V`,
  `_DM_EXPANSAO`, `_DM_RESTO`, `_DM_ALINH_H`, `_DM_ALINH_V` (L268-282).
- Funções `_dm_int`, `_dm_literal`, `_dm_medida`, `_validar_dm_formacao`,
  `_validar_dm_formacao_eixo`, `_validar_dm_dimensionamento`,
  `_validar_dm_dim_eixo`, `_validar_dm_espacamento`,
  `_validar_dm_politica_simples`, `_validar_dm_par_eixos`,
  `_validar_distribuicao_matricial` (L285-563).
- Depende de: `erros.py` (`TelaEstruturaInvalida`).

**`lancador_config.py`** — carregamento e validação de
`config/elementos/lancador.json` (H-0034/ADR-0023).
- `_carregar_e_validar_config_lancador` (L633-835).
- Depende de: `erros.py` (`TelaArquivoNaoEncontrado`, `TelaJsonInvalido`,
  `TelaCampoObrigatorioAusente`, `TelaEstruturaInvalida`). Usa `json`, `os`
  (stdlib). Recebe `base` (Path) como parâmetro — não chama `_para_base`
  diretamente (quem chama já o resolveu).

**`grupos.py`** — invariantes do tipo estrutural `grupo`, incluindo a variante
matricial (ADR-0019/H-0027, ADR-0020).
- `_validar_quantidade_matriz`, `_validar_distribuicao_matriz`,
  `_validar_celulas_matriz`, `_validar_matriz_grupo`, `_validar_grupo`
  (L846-1181).
- Depende de: `erros.py` (`TelaGrupoInvalido`, `TelaEstruturaInvalida`,
  `TelaTipoDesconhecido`), `taxonomia.py` (`ESTRUTURAS_GRUPO_VALIDAS`,
  `ARRANJOS_CORPO_VALIDOS`, `TIPOS_CORPO_VALIDOS`), `distribuicao_corpo.py`
  (`_validar_distribuicao_corpo`), `validacao_matricial.py`
  (`_validar_distribuicao_matricial`).

**`envelope_pre_adr_0028.py`** — compatibilidade estrutural com o envelope
clássico de console anterior à ADR-0028 (H0037-IMPL-QAPP5-001), incluindo a
determinação de escopo D23.
- Constantes `_TELAS_LEGADAS_D23` (L1635-1646), `_TELAS_VARIANTE2_LEGADAS`
  (L1659), `_CAMPOS_ENVELOPE_PRE_ADR_0028` (L1670-1678 — materializada e
  preservada tal como está hoje; defeito de constante não referenciada
  registrado em §3.9, não corrigido aqui), `_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028`
  (L1692-1699), `_POLITICA_SELECAO_VALIDOS`, `_POLITICA_PAGINACAO_VALIDOS`
  (L1702-1703).
- Funções `_validar_valores_envelope_pre_adr_0028` (L1706-1788),
  `_console_em_escopo_d23` (L1791-1964).
- Depende de: `erros.py` (`TelaEstruturaInvalida`).

**`d23_console.py`** — validação da política de modo D23 de elementos console
(H-0037/ADR-0028).
- Constantes `_POLITICAS_MODO_VALIDAS`, `_MODOS_INICIAIS_VALIDOS`
  (L1622-1625).
- Função `_validar_d23_console` (L2058-2124).
- Depende de: `erros.py` (`TelaEstruturaInvalida`), `envelope_pre_adr_0028.py`
  (`_TELAS_LEGADAS_D23`).

**`perfil_resultado_execucao.py`** — estrutura obrigatória do perfil
`resultado_execucao` (H-0043/ADR-0036).
- Constantes `_CAMPOS_CONSOLE_RESULTADO_PERMITIDOS` (L54),
  `_CAMPOS_CLASSICOS_PROIBIDOS_RESULTADO` (L59-74).
- Função `_validar_perfil_resultado_execucao` (L1184-1340).
- Depende de: `erros.py` (`TelaEstruturaInvalida`), `taxonomia.py`
  (`PERFIL_RESULTADO_EXECUCAO`), `envelope_pre_adr_0028.py`
  (`_console_em_escopo_d23`).

**`conteudo_externo.py`** — validação (20 validações semânticas + V-01 a V-15)
e carregamento do documento externo de conteúdo multinível (H-0036/ADR-0026/
ADR-0027).
- Constantes `APRESENTACOES_CONTEUDO_VALIDAS`, `TIPOS_NIVEL_CONTEUDO_VALIDOS`,
  `TIPOS_DESIGNADOR_VALIDOS`, `_BLOCO_ESPECIFICO_POR_APRESENTACAO`,
  `_BLOCOS_ESPECIFICOS_APRESENTACAO`, `CAMPOS_RESULTADO_FISICO_PROIBIDOS`
  (L1579-1618), `_CAMPOS_COLUNA_RECONHECIVEL` (L2022).
- Funções `_validar_designador_conteudo`, `_rejeitar_resultados_fisicos_conteudo`,
  `_coluna_reconhecivel`, `_validar_no_conteudo`, `validar_conteudo_externo`,
  `carregar_conteudo_externo` (L1967-2016, L2025-2208, L2211-2689).
- Depende de: `erros.py` (`TelaEstruturaInvalida`, `TelaCampoObrigatorioAusente`,
  `TelaArquivoNaoEncontrado`, `TelaJsonInvalido`), `caminho_base.py`
  (`_para_base`). Usa `json`, `os` (stdlib).

**`estilo.py`** — materialização de `config/estilo.json` (H-0039/ADR-0030).
- Classe `EstiloResolvido` (L2705-2741, `@dataclass(frozen=True)`).
- Função `carregar_estilo` (L2744-2835) e os 11 resolvedores privados
  `_resolver_cor_inativo`, `_resolver_cor_alerta`, `_exigir_secao`,
  `_resolver_preset_default`, `_resolver_catalogo`, `_resolver_preset_ativo`,
  `_campo_obrigatorio`, `_validar_caractere`, `_resolver_borda`,
  `_resolver_chip`, `_resolver_indicadores` (L2838-3143).
- Depende de: `erros.py` (`EstiloErro`), `caminho_base.py` (`_para_base`).
  Usa `json`, `dataclasses.dataclass` (stdlib).

**`tela_json.py`** — orquestração macro de `tela.json`: ponto de entrada
`carregar_tela` e os verificadores de escopo total do corpo.
- Constantes `_ID_TELA_RAIZ` (L47), `_PERFIL_AUSENTE` (L51). `_ID_TELA_RAIZ`
  tem `tela_json.py` como proprietário nominal único; `erros.py` **não**
  importa `tela_json.py` para obter esse valor — `TelaIdIncorreto` usa o
  literal `"orquestrador"` como default (ver `erros.py` acima), preservando
  a ausência de aresta entre os dois módulos (fechamento H0047-QA-004, prova
  na seção 7, comando 9).
- Funções `_tem_lancador_em_elementos`, `_iterar_consoles_do_corpo`,
  `_validar_unicidade_ids_consoles` (L566-630), `carregar_tela` (L1343-1560).
- Depende de: `erros.py` (todas as exceções `Tela*` usadas diretamente por
  `carregar_tela`), `taxonomia.py` (`TIPOS_CORPO_VALIDOS`,
  `TIPOS_ESTRUTURAIS_VALIDOS`, `ARRANJOS_CORPO_VALIDOS`,
  `PERFIL_RESULTADO_EXECUCAO`), `caminho_base.py` (`_para_base`),
  `distribuicao_corpo.py` (`_validar_distribuicao_corpo`),
  `validacao_matricial.py` (`_validar_distribuicao_matricial`), `grupos.py`
  (`_validar_grupo`), `lancador_config.py`
  (`_carregar_e_validar_config_lancador`), `perfil_resultado_execucao.py`
  (`_validar_perfil_resultado_execucao`), `envelope_pre_adr_0028.py`
  (`_console_em_escopo_d23`), `d23_console.py` (`_validar_d23_console`). Usa
  `json`, `os` (stdlib).

### 4.3 Direção de dependências (acíclica)

A ordem abaixo é uma ordem topológica válida: cada módulo depende apenas de
módulos listados ANTES dele.

```text
erros.py                 (base, sem deps)
taxonomia.py              (base, sem deps)
caminho_base.py            (base, sem deps de outro modulo interno)
        │
        ▼
distribuicao_corpo.py     ← erros.py, taxonomia.py
validacao_matricial.py    ← erros.py
lancador_config.py        ← erros.py
envelope_pre_adr_0028.py  ← erros.py
        │
        ▼
grupos.py                 ← erros.py, taxonomia.py, distribuicao_corpo.py,
                             validacao_matricial.py
d23_console.py            ← erros.py, envelope_pre_adr_0028.py
conteudo_externo.py       ← erros.py, caminho_base.py
estilo.py                 ← erros.py, caminho_base.py
        │
        ▼
perfil_resultado_execucao.py ← erros.py, taxonomia.py, envelope_pre_adr_0028.py
        │
        ▼
tela_json.py               ← erros.py, taxonomia.py, caminho_base.py,
                              distribuicao_corpo.py, validacao_matricial.py,
                              grupos.py, lancador_config.py,
                              perfil_resultado_execucao.py,
                              envelope_pre_adr_0028.py, d23_console.py
```

`conteudo_externo.py` e `estilo.py` são pontos de entrada irmãos de
`tela_json.py` (nenhum dos três importa os outros dois — §3.3 confirma que
`carregar_tela` não chama nada do bloco 12 nem do bloco 13). Nenhum módulo
mais baixo importa um módulo mais alto; nenhum módulo interno importa
`tela.loader` (a fachada) nem `tela.modelo`, `tela.renderizador` ou
`tela.renderizacao.*` — condição obrigatória de D-MOD-08 item 9, verificada
na seção 7.

`erros.py` **não** depende de `tela_json.py`. A única relação entre os dois
módulos que poderia sugerir uma aresta invertida (módulo-base → módulo mais
alto) é o valor default de `TelaIdIncorreto.esperado`, hoje igual a
`_ID_TELA_RAIZ`; a arquitetura-alvo fecha essa relação por **duplicação
literal deliberada** (`"orquestrador"` em ambos os módulos), não por import
— ver `erros.py` e `tela_json.py` em §4.2 e a prova reproduzível do comando 9
da seção 7 (fechamento H0047-QA-004).

### 4.4 Conteúdo que permanece em `tela/loader.py` (fachada)

Apenas: docstring de módulo (adaptada para descrever a fachada e apontar para
`tela/carregamento/`); imports de reexportação dos módulos internos listados
acima; no máximo atribuições simples de alias necessárias à reexportação;
`__all__`, quando usado, apenas como lista literal nominal de exportações.
Nenhum caso desta análise exige um wrapper de função: todos os 24 símbolos
públicos consumidos (seção 5) mapeiam diretamente para um símbolo interno de
mesmo nome, importável por `from tela.carregamento.<modulo> import <nome>`.
A prova normativa (§7, comando 6) exige **zero funções, zero funções
assíncronas, zero lambdas e zero classes definidas na fachada, em qualquer
profundidade** — mesma política do H-0046 (§3.4). Se a implementação, durante
a extração, encontrar um caso concreto em que a assinatura pública não possa
ser preservada por reexportação direta ou por alias simples, deve **parar
antes de criar o wrapper** e solicitar a exceção operacional focal (§11).

---

## 5. Fachada pública

### 5.1 Lista nominal completa de reexportação

```text
TelaErro                                          ← erros
TelaArquivoNaoEncontrado                          ← erros
TelaJsonInvalido                                  ← erros
TelaCampoObrigatorioAusente                       ← erros
TelaIdNaoCoincideComArquivo                       ← erros
TelaIdIncorreto                                   ← erros
TelaEstruturaInvalida                             ← erros
TelaElementoSemId                                 ← erros
TelaElementoSemTipo                               ← erros
TelaTipoDesconhecido                              ← erros
TelaGrupoInvalido                                 ← erros
EstiloErro                                        ← erros
TIPOS_CORPO_VALIDOS                               ← taxonomia
TIPOS_ESTRUTURAIS_VALIDOS                         ← taxonomia
ARRANJOS_CORPO_VALIDOS                            ← taxonomia
MODOS_DISTRIBUICAO_CORPO_VALIDOS                  ← taxonomia
PERFIL_RESULTADO_EXECUCAO                         ← taxonomia
carregar_tela                                     ← tela_json
carregar_conteudo_externo                         ← conteudo_externo
validar_conteudo_externo                          ← conteudo_externo
carregar_estilo                                   ← estilo
EstiloResolvido                                   ← estilo
_validar_d23_console                              ← d23_console
_console_em_escopo_d23                            ← envelope_pre_adr_0028
```

24 símbolos. Todo símbolo interno não listado acima permanece acessível
apenas via seu módulo interno (`tela.carregamento.<modulo>.<simbolo>`) e
**não** é reexportado pela fachada, salvo se a implementação encontrar,
durante a extração, outro consumidor externo real não capturado nesta busca
— nesse caso, o símbolo adicional deve ser reexportado e registrado no
relatório de implementação (seção 6.5), não descartado silenciosamente.
Em particular, `_ID_TELA_RAIZ` (proprietário `tela_json.py`) **não** é
reexportado pela fachada — nenhum consumidor externo comprovado (§3.5); sua
relação fechada com o default de `TelaIdIncorreto.esperado` está registrada
em §4.2/§4.3 e comprovada pelo comando 9 da seção 7.

### 5.2 Prova reproduzível — imports públicos e consumidores existentes

```zsh
# Nenhum consumidor externo foi migrado para tela.carregamento.*
rg -n 'from tela\.carregamento|import tela\.carregamento' tela demo \
  | grep -v '^tela/loader.py:' \
  | grep -v '^tela/carregamento/'
# saida esperada: vazia
```

```zsh
# Todos os simbolos hoje importados de tela.loader continuam resolvendo,
# com o mesmo comportamento, atraves da fachada.
python3 - <<'PY'
import tela.loader as f
nomes = [
    "TelaErro", "TelaArquivoNaoEncontrado", "TelaJsonInvalido",
    "TelaCampoObrigatorioAusente", "TelaIdNaoCoincideComArquivo",
    "TelaIdIncorreto", "TelaEstruturaInvalida", "TelaElementoSemId",
    "TelaElementoSemTipo", "TelaTipoDesconhecido", "TelaGrupoInvalido",
    "EstiloErro", "TIPOS_CORPO_VALIDOS", "TIPOS_ESTRUTURAIS_VALIDOS",
    "ARRANJOS_CORPO_VALIDOS", "MODOS_DISTRIBUICAO_CORPO_VALIDOS",
    "PERFIL_RESULTADO_EXECUCAO", "carregar_tela", "carregar_conteudo_externo",
    "validar_conteudo_externo", "carregar_estilo", "EstiloResolvido",
    "_validar_d23_console", "_console_em_escopo_d23",
]
faltando = [n for n in nomes if not hasattr(f, n)]
assert not faltando, faltando
print("OK: todos os", len(nomes), "simbolos publicos preservados")
PY
```

```zsh
# Hierarquia de excecoes permanece intacta (subclasses de TelaErro/Exception).
python3 -c "
import tela.loader as f
assert issubclass(f.TelaArquivoNaoEncontrado, f.TelaErro)
assert issubclass(f.TelaJsonInvalido, f.TelaErro)
assert issubclass(f.TelaCampoObrigatorioAusente, f.TelaErro)
assert issubclass(f.TelaIdNaoCoincideComArquivo, f.TelaErro)
assert issubclass(f.TelaIdIncorreto, f.TelaErro)
assert issubclass(f.TelaEstruturaInvalida, f.TelaErro)
assert issubclass(f.TelaElementoSemId, f.TelaErro)
assert issubclass(f.TelaElementoSemTipo, f.TelaErro)
assert issubclass(f.TelaTipoDesconhecido, f.TelaErro)
assert issubclass(f.TelaGrupoInvalido, f.TelaErro)
assert issubclass(f.TelaErro, Exception)
assert issubclass(f.EstiloErro, Exception)
assert not issubclass(f.EstiloErro, f.TelaErro)
print('OK: hierarquia de excecoes intacta')
"
```

```zsh
# tela/modelo.py continua importando pelos caminhos publicos vigentes.
python3 -c "
import ast
arv = ast.parse(open('tela/modelo.py', encoding='utf-8').read())
alvo = [n for n in ast.walk(arv) if isinstance(n, ast.ImportFrom) and n.module == 'tela.loader']
assert len(alvo) == 1, alvo
nomes = {a.name for a in alvo[0].names}
assert nomes == {'TIPOS_CORPO_VALIDOS', 'TIPOS_ESTRUTURAIS_VALIDOS'}, nomes
print('OK: tela/modelo.py importa exclusivamente da fachada tela.loader')
"
```

```zsh
# Nenhum consumidor externo foi migrado para caminhos internos (repete acima
# com escopo mais amplo, incluindo demo/).
rg -n 'tela\.carregamento\.' tela demo | grep -v '^tela/loader.py:'
# saida esperada: vazia
```

### 5.3 Ausência de importação inversa

A prova **normativa** desta propriedade é o script AST do comando 3 da
seção 7 (H0047-QA-003): cobre as formas estáticas (`import tela.loader`,
`import tela.loader as alias`, `from tela.loader import simbolo`,
`from tela import loader`, `from tela import loader as alias`, cadeia de
atributos `tela.loader` alcançada via `import tela`) e as formas dinâmicas
literais (`importlib.import_module("tela.loader")`,
`__import__("tela.loader")`). Carregamento dinâmico da fachada é **proibido**
nos módulos internos de `tela/carregamento/`. A busca abaixo é mantida
apenas como evidência auxiliar (não normativa — não cobre `from tela import
loader`, cadeia de atributos nem carregamento dinâmico):

```zsh
rg -n 'from tela\.loader import|import tela\.loader' tela/carregamento
# saida esperada: vazia (evidencia auxiliar, nao normativa)
```

---

## 6. Manifesto nominal da futura implementação

### 6.1 Arquivos autorizados para criação

```text
tela/carregamento/__init__.py
tela/carregamento/erros.py
tela/carregamento/taxonomia.py
tela/carregamento/caminho_base.py
tela/carregamento/distribuicao_corpo.py
tela/carregamento/validacao_matricial.py
tela/carregamento/lancador_config.py
tela/carregamento/grupos.py
tela/carregamento/envelope_pre_adr_0028.py
tela/carregamento/d23_console.py
tela/carregamento/perfil_resultado_execucao.py
tela/carregamento/conteudo_externo.py
tela/carregamento/estilo.py
tela/carregamento/tela_json.py
docs/relatorios/IMP-0047-modularizacao-estrutural-do-loader.md
```

### 6.2 Arquivos autorizados para alteração

```text
tela/loader.py
```

### 6.3 Arquivos de teste com ajuste focal

```yaml
arquivos_de_teste_com_ajuste_focal: []
```

Vazio — a seção 3.6 confirmou, por inspeção nominal de todos os testes que
tocam `tela.loader`, ausência de inspeção whitebox do texto-fonte de
`tela/loader.py` e ausência de monkeypatch cujo funcionamento dependa da
coabitação física de chamador e chamado dentro do arquivo. Se a
implementação, durante a extração, encontrar um caso real não capturado por
esta busca (dependência de localização física do símbolo, leitura literal de
`tela/loader.py`, monkeypatch aplicado ao namespace antigo que efetivamente
intercepta uma chamada interna, ou teste estrutural que precise apontar ao
novo proprietário interno), deve **parar** e solicitar a exceção operacional
focal (§11) antes de alterar qualquer teste — a reorganização geral, divisão
ou renomeação de testes permanece proibida e pertence exclusivamente ao
Handoff 3.

### 6.4 Arquivos preservados (leitura apenas, sem alteração)

```text
tela/modelo.py
tela/renderizador.py
tela/renderizacao/
tela/navegacao.py
tela/paginacao.py
tela/selecao.py
tela/distribuicao_matricial.py
tela/execucao_focal.py
tela/fluxo_execucao.py
tela/resultado_execucao.py
tela/teste_loader.py
tela/teste_modelo.py
tela/teste_navegacao.py
tela/teste_paginacao.py
tela/teste_fluxo_execucao.py
tela/teste_resultado_execucao.py
tela/teste_renderizador.py
tela/teste_distribuicao_matricial.py
tela/teste_selecao.py
tela/teste_execucao_focal.py
demo/demo.py
demo/demo_selecao.py
demo/demo_navegacao.py
demo/demo_distribuicao.py
demo/diagnostico.py
demo/explorar_barra_de_menus.py
demo/teste_demo*.py
demo/teste_diagnostico.py
demo/teste_explorar_barra_de_menus.py
demo/teste_executor_sintetico.py
config/
```

### 6.5 Relatório de implementação

```text
docs/relatorios/IMP-0047-modularizacao-estrutural-do-loader.md
```

Deve registrar, em até 900 palavras: arquivos criados e alterados;
responsabilidades extraídas por módulo; conteúdo final da fachada;
compatibilidade pública comprovada (seção 5); testes focais e suíte completa
executados (seção 8) com resultado; verificação de ciclos e de importação
inversa (seção 7) com resultado; redução estrutural observada (linhas antes/
depois, funções por módulo); qualquer símbolo público adicional descoberto
durante a extração e reexportado além da lista da seção 5.1; o defeito
estrutural de `_CAMPOS_ENVELOPE_PRE_ADR_0028` (§3.9) confirmado como
preservado, não corrigido; defeitos funcionais adicionais eventualmente
encontrados e **deferidos** (não corrigidos); bloqueios ou desvios frente a
este handoff, incluindo eventuais pedidos de exceção operacional (seção 11)
e sua resolução.

---

## 7. Integridade estrutural

```zsh
# 1. Importacao de todos os modulos internos, isoladamente
python3 -c "
import importlib
for m in [
    'tela.carregamento.erros', 'tela.carregamento.taxonomia',
    'tela.carregamento.caminho_base', 'tela.carregamento.distribuicao_corpo',
    'tela.carregamento.validacao_matricial', 'tela.carregamento.lancador_config',
    'tela.carregamento.grupos', 'tela.carregamento.envelope_pre_adr_0028',
    'tela.carregamento.d23_console', 'tela.carregamento.perfil_resultado_execucao',
    'tela.carregamento.conteudo_externo', 'tela.carregamento.estilo',
    'tela.carregamento.tela_json',
]:
    importlib.import_module(m)
print('OK: todos os modulos internos importam isoladamente')
"
```

```zsh
# 2. Ausencia de ciclos de importacao (checagem estatica por grafo).
#
# Mesma politica do H-0046 (§7 comando 2): imports relativos e
# 'from tela.carregamento import <modulo>' sao PROIBIDOS dentro do pacote,
# pois ocultariam a aresta real do grafo. Toda dependencia interna usa uma
# das formas absolutas e nominais abaixo, normalizadas para o mesmo no de
# grafo "tela.carregamento.<modulo>":
#
#   import tela.carregamento.<modulo>
#   from tela.carregamento.<modulo> import <simbolo>
#
# Correcao H0047-QA-001: antes do DFS, toda aresta do grafo deve apontar
# para um modulo real existente no pacote (arquivo .py sob
# tela/carregamento/). Dependencia interna para modulo ausente e FALHA da
# prova estrutural, nao tratada como folha valida do DFS.
python3 - <<'PY'
import ast, pathlib, sys

PREFIXO = "tela.carregamento"


def analisar_arquivo(src, origem="<sintetico>"):
    arv = ast.parse(src, filename=origem)
    deps, violacoes = set(), []
    for no in ast.walk(arv):
        if isinstance(no, ast.ImportFrom):
            if no.level and no.level > 0:
                violacoes.append(("import relativo (level > 0)", no.lineno))
            elif no.module == PREFIXO:
                violacoes.append((
                    "from tela.carregamento import <modulo> oculta o "
                    "submodulo real no grafo", no.lineno,
                ))
            elif no.module and no.module.startswith(PREFIXO + "."):
                deps.add(no.module)
        elif isinstance(no, ast.Import):
            for alias in no.names:
                if alias.name == PREFIXO:
                    violacoes.append((
                        "ast.Import simples de tela.carregamento (sem "
                        "submodulo) oculta o submodulo real no grafo",
                        no.lineno,
                    ))
                elif alias.name.startswith(PREFIXO + "."):
                    deps.add(alias.name)
    return deps, violacoes


def validar_referencias_internas(grafo, modulos_reais):
    """Toda aresta do grafo deve apontar para um modulo real do pacote."""
    ausentes = []
    for origem, deps in grafo.items():
        for destino in sorted(deps):
            if destino not in modulos_reais:
                ausentes.append((origem, destino))
    return ausentes


_, v1 = analisar_arquivo("from .modulo import simbolo\n")
assert v1, "REGRESSAO: import relativo deveria ser rejeitado"
_, v2 = analisar_arquivo("from tela.carregamento import modulo\n")
assert v2, "REGRESSAO: 'from tela.carregamento import modulo' deveria ser rejeitado"
_, v3 = analisar_arquivo("import tela.carregamento\n")
assert len(v3) == 1, "REGRESSAO: 'import tela.carregamento' deveria ser rejeitado"
d4, v4 = analisar_arquivo("import tela.carregamento.modulo\n")
assert not v4 and d4 == {"tela.carregamento.modulo"}, (
    "REGRESSAO: 'import tela.carregamento.modulo' deveria ser aceito"
)
d5, v5 = analisar_arquivo("from tela.carregamento.modulo import simbolo\n")
assert not v5 and d5 == {"tela.carregamento.modulo"}, (
    "REGRESSAO: 'from tela.carregamento.modulo import simbolo' deveria ser aceito"
)
print("OK: verificacoes sinteticas do detector")

modulos_reais_sinteticos = {"tela.carregamento.a"}
grafo_sintetico = {
    "tela.carregamento.a": {"tela.carregamento.inexistente"},
}
ausentes_sinteticos = validar_referencias_internas(grafo_sintetico, modulos_reais_sinteticos)
assert ausentes_sinteticos == [("tela.carregamento.a", "tela.carregamento.inexistente")], (
    "REGRESSAO: dependencia para modulo interno inexistente deveria ser "
    "rejeitada pelo detector, nao tratada como folha valida do grafo"
)
print("OK: verificacao sintetica de rejeicao de modulo interno inexistente")

pkg = pathlib.Path("tela/carregamento")
grafo, todas_violacoes = {}, []
for arq in pkg.glob("*.py"):
    nome = f"{PREFIXO}.{arq.stem}"
    deps, violacoes = analisar_arquivo(arq.read_text(encoding="utf-8"), str(arq))
    grafo[nome] = deps
    todas_violacoes.extend((nome, linha, motivo) for motivo, linha in violacoes)

if todas_violacoes:
    print("FALHA: forma de import proibida dentro de tela/carregamento/:", todas_violacoes)
    sys.exit(1)

# Conjunto completo dos modulos reais do pacote (arquivos .py existentes em
# disco). Toda dependencia interna registrada no grafo precisa pertencer a
# este conjunto ANTES do DFS assumir a aresta como valida.
modulos_reais = set(grafo)
ausentes = validar_referencias_internas(grafo, modulos_reais)
if ausentes:
    print("FALHA: dependencia interna para modulo inexistente:")
    for origem, destino in ausentes:
        print(
            "  aresta completa: {0} -> {1}  (modulo de origem: {0}; "
            "modulo de destino ausente: {1})".format(origem, destino)
        )
    sys.exit(1)
print("OK: toda dependencia interna registrada aponta para um modulo real existente")

visitado, pilha = set(), set()

def dfs(n, caminho):
    if n in pilha:
        raise SystemExit("CICLO detectado: {0}".format(" -> ".join(caminho + [n])))
    if n in visitado:
        return
    pilha.add(n)
    for d in sorted(grafo.get(n, ())):
        dfs(d, caminho + [n])
    pilha.discard(n)
    visitado.add(n)

for n in sorted(grafo):
    dfs(n, [])
print("OK: nenhum ciclo de importacao entre modulos de tela/carregamento")
PY
```

```zsh
# 3. Nenhum modulo interno importa a fachada, tela.modelo, tela.renderizador
#    nem tela.renderizacao.* — evidencia auxiliar por regex. NAO normativa
#    para a parte de importacao inversa da fachada (tela.loader): a prova
#    normativa dessa parte e o script AST logo abaixo (H0047-QA-003).
rg -n \
  'from tela\.loader import|import tela\.loader|from tela\.modelo import|import tela\.modelo|from tela\.renderizador|import tela\.renderizador|from tela\.renderizacao|import tela\.renderizacao' \
  tela/carregamento
# saida esperada: vazia
```

```zsh
# 3 (prova normativa). Deteccao AST de importacao inversa da fachada
# tela.loader em qualquer modulo de tela/carregamento/ — cobre as formas
# estaticas (import tela.loader[.x][ as alias], from tela.loader import x,
# from tela import loader[ as alias], cadeia de atributos tela.loader
# alcancada via "import tela") e o carregamento dinamico literal
# (importlib.import_module("tela.loader"), __import__("tela.loader")).
# Carregamento dinamico da fachada e proibido nos modulos internos.
python3 - <<'PY'
import ast, pathlib, sys


def analisar_importacao_inversa(codigo, origem="<sintetico>"):
    arv = ast.parse(codigo, filename=origem)
    violacoes = []
    for no in ast.walk(arv):
        if isinstance(no, ast.Import):
            for alias in no.names:
                if alias.name == "tela.loader" or alias.name.startswith("tela.loader."):
                    violacoes.append(("import tela.loader (forma estatica)", no.lineno))
        elif isinstance(no, ast.ImportFrom):
            if no.level == 0 and no.module == "tela.loader":
                violacoes.append(("from tela.loader import ...", no.lineno))
            elif no.level == 0 and no.module == "tela" and any(
                a.name == "loader" for a in no.names
            ):
                violacoes.append(("from tela import loader", no.lineno))
        elif isinstance(no, ast.Attribute):
            if no.attr == "loader" and isinstance(no.value, ast.Name) and no.value.id == "tela":
                violacoes.append(("cadeia de atributos tela.loader", no.lineno))
        elif isinstance(no, ast.Call):
            alvo = None
            if isinstance(no.func, ast.Attribute) and no.func.attr == "import_module":
                alvo = "importlib.import_module"
            elif isinstance(no.func, ast.Name) and no.func.id == "__import__":
                alvo = "__import__"
            if alvo and no.args and isinstance(no.args[0], ast.Constant) and isinstance(no.args[0].value, str):
                if no.args[0].value == "tela.loader" or no.args[0].value.startswith("tela.loader."):
                    violacoes.append(("carregamento dinamico via {0}('tela.loader')".format(alvo), no.lineno))
    return violacoes


casos_rejeitados = [
    "import tela.loader\n",
    "import tela.loader as f\n",
    "from tela.loader import carregar_tela\n",
    "from tela import loader\n",
    "from tela import loader as f\n",
    "import tela\ntela.loader\n",
    "import tela\nx = tela.loader.carregar_tela\n",
    "import importlib\nimportlib.import_module('tela.loader')\n",
    "__import__('tela.loader')\n",
]
for codigo in casos_rejeitados:
    assert analisar_importacao_inversa(codigo), (
        "REGRESSAO: deveria rejeitar importacao inversa em: {0!r}".format(codigo)
    )

casos_aceitos = [
    "import os\nimport json\nfrom pathlib import Path\nfrom dataclasses import dataclass\n",
    "import tela.carregamento.erros\n",
    "from tela.carregamento.taxonomia import TIPOS_CORPO_VALIDOS\n",
    "import tela\nx = tela.modelo\n",
    "import tela\nx = tela.carregamento\n",
]
for codigo in casos_aceitos:
    violacoes = analisar_importacao_inversa(codigo)
    assert not violacoes, (
        "FALSO POSITIVO: nao deveria rejeitar: {0!r} -> {1}".format(codigo, violacoes)
    )
print("OK: verificacoes sinteticas do detector AST de importacao inversa")

violacoes_reais = []
for arq in pathlib.Path("tela/carregamento").glob("*.py"):
    for motivo, linha in analisar_importacao_inversa(arq.read_text(encoding="utf-8"), str(arq)):
        violacoes_reais.append((str(arq), linha, motivo))

if violacoes_reais:
    print("FALHA: importacao inversa da fachada tela.loader detectada:", violacoes_reais)
    sys.exit(1)
print("OK: nenhum modulo de tela/carregamento importa ou acessa tela.loader, estatica ou dinamicamente")
PY
```

```zsh
# 4. Nenhum consumidor externo migrado para caminhos internos (repete a
#    secao 5.2 com escopo mais amplo)
rg -n 'tela\.carregamento\.' tela demo | grep -v '^tela/loader.py:'
```

```zsh
# 5. Reducao material da concentracao de tela/loader.py
wc -l tela/loader.py
# esperado: modulo reduzido a fachada de reexportacao (ordem de dezenas de
# linhas, nao centenas) — nenhuma funcao com corpo de logica de dominio.
```

```zsh
# 6. Fachada sem funcoes, lambdas ou classes — prova normativa unica (§4.4).
python3 - <<'PY'
import ast, importlib

reexportacoes_autorizadas = {
    "tela.carregamento.erros": {
        "TelaErro", "TelaArquivoNaoEncontrado", "TelaJsonInvalido",
        "TelaCampoObrigatorioAusente", "TelaIdNaoCoincideComArquivo",
        "TelaIdIncorreto", "TelaEstruturaInvalida", "TelaElementoSemId",
        "TelaElementoSemTipo", "TelaTipoDesconhecido", "TelaGrupoInvalido",
        "EstiloErro",
    },
    "tela.carregamento.taxonomia": {
        "TIPOS_CORPO_VALIDOS", "TIPOS_ESTRUTURAIS_VALIDOS",
        "ARRANJOS_CORPO_VALIDOS", "MODOS_DISTRIBUICAO_CORPO_VALIDOS",
        "PERFIL_RESULTADO_EXECUCAO",
    },
    "tela.carregamento.tela_json": {"carregar_tela"},
    "tela.carregamento.conteudo_externo": {
        "carregar_conteudo_externo", "validar_conteudo_externo",
    },
    "tela.carregamento.estilo": {"carregar_estilo", "EstiloResolvido"},
    "tela.carregamento.d23_console": {"_validar_d23_console"},
    "tela.carregamento.envelope_pre_adr_0028": {"_console_em_escopo_d23"},
}
publicos_fachada = {
    simbolo: modulo
    for modulo, simbolos in reexportacoes_autorizadas.items()
    for simbolo in simbolos
}
assert len(publicos_fachada) == 24 == sum(
    len(s) for s in reexportacoes_autorizadas.values()
), "mapa nominal da fachada nao tem 24 simbolos ou contem duplicados"


def eh_alias_simples(no):
    if isinstance(no, ast.Name):
        return True
    if isinstance(no, ast.Attribute):
        return eh_alias_simples(no.value)
    return False


def eh_lista_literal_de_strings(no):
    return isinstance(no, (ast.List, ast.Tuple)) and all(
        isinstance(el, ast.Constant) and isinstance(el.value, str) for el in no.elts
    )


def analisar_fachada(fonte):
    arv = ast.parse(fonte, filename="<fachada-sintetica>")
    violacoes, importados, atribuicoes = [], {}, {}
    nomes_all = None
    for idx, stmt in enumerate(arv.body):
        if (
            idx == 0 and isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and isinstance(stmt.value.value, str)
        ):
            continue
        if isinstance(stmt, ast.Import):
            for alias in stmt.names:
                violacoes.append("ast.Import nao autorizado: {0}".format(alias.name))
            continue
        if isinstance(stmt, ast.ImportFrom):
            if stmt.level:
                violacoes.append("ImportFrom relativo nao autorizado")
                continue
            if stmt.module not in reexportacoes_autorizadas:
                violacoes.append("modulo nao autorizado: {0}".format(stmt.module))
                continue
            permitidos = reexportacoes_autorizadas[stmt.module]
            for alias in stmt.names:
                if alias.name == "*":
                    violacoes.append("importacao curinga nao autorizada")
                    continue
                if alias.name not in permitidos:
                    violacoes.append(
                        "simbolo nao autorizado em {0}: {1}".format(stmt.module, alias.name)
                    )
                    continue
                local = alias.asname or alias.name
                importados[local] = (stmt.module, alias.name, alias.asname)
            continue
        if (
            isinstance(stmt, ast.Assign) and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)
        ):
            alvo = stmt.targets[0].id
            if alvo == "__all__":
                if not eh_lista_literal_de_strings(stmt.value):
                    violacoes.append("__all__ deve ser lista/tupla literal")
                else:
                    nomes_all = [el.value for el in stmt.value.elts]
                continue
            if not eh_alias_simples(stmt.value) or not isinstance(stmt.value, ast.Name):
                violacoes.append("atribuicao invalida: {0}".format(alvo))
                continue
            if alvo not in publicos_fachada:
                violacoes.append("alias nao autorizado: {0}".format(alvo))
                continue
            atribuicoes[alvo] = stmt.value.id
            continue
        violacoes.append("instrucao nao autorizada: {0}".format(type(stmt).__name__))
    return arv, violacoes, importados, atribuicoes, nomes_all


def all_fechado(nomes_all):
    return nomes_all is None or set(nomes_all) == set(publicos_fachada)


src = open("tela/loader.py", encoding="utf-8").read()
arv, violacoes, importados, atribuicoes, nomes_all = analisar_fachada(src)
assert not violacoes, "fachada possui import/alias fora da politica: {0}".format(violacoes)
assert all_fechado(nomes_all), "__all__ deve conter exatamente a lista nominal publica"
for simbolo, modulo in publicos_fachada.items():
    direto = importados.get(simbolo)
    via_alias = atribuicoes.get(simbolo)
    assert (
        (direto is not None and direto[:2] == (modulo, simbolo))
        or (
            via_alias is not None and importados.get(via_alias) is not None
            and importados[via_alias][:2] == (modulo, simbolo)
        )
    ), "reexportacao nominal ausente ou incorreta: {0}".format(simbolo)

fachada = importlib.import_module("tela.loader")
for simbolo, modulo in publicos_fachada.items():
    proprietario = importlib.import_module(modulo)
    assert hasattr(proprietario, simbolo), "proprietario nao expoe {0}.{1}".format(modulo, simbolo)
    assert hasattr(fachada, simbolo), "fachada nao reexporta: {0}".format(simbolo)
    assert getattr(fachada, simbolo) is getattr(proprietario, simbolo), (
        "reexportacao nao preserva identidade: {0}".format(simbolo)
    )

proibidos = [
    n for n in ast.walk(arv)
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda, ast.ClassDef))
]
assert not proibidos, (
    "fachada nao pode conter FunctionDef/AsyncFunctionDef/Lambda/ClassDef: {0}"
).format([getattr(n, "name", "<lambda>") for n in proibidos])

print(
    "OK: fachada contem somente imports nominais fechados, aliases simples e "
    "__all__ fechado — zero FunctionDef, AsyncFunctionDef, Lambda e ClassDef"
)
PY
```

```zsh
# 7. Proprietario nominal INTEGRAL e unico por AST (nao apenas hasattr) —
#    prova integral, nao amostral (H0047-QA-002): cobre TODOS os 96 simbolos
#    de nivel superior descritos na secao 4.2 (classes, funcoes publicas e
#    privadas, constantes publicas e privadas, dataclasses e sentinelas de
#    modulo), incluindo os nao reexportados pela fachada.
python3 - <<'PY'
import ast, importlib, pathlib

pkg = pathlib.Path("tela/carregamento")
PREFIXO = "tela.carregamento"

# Mapa fechado por modulo -> lista nominal completa de simbolos (secao 4.2).
# Nenhuma reticencia, agrupamento abreviado ou intervalo: cada simbolo
# aparece nominalmente.
modulos_previstos = {
    "erros": [
        "TelaErro", "TelaArquivoNaoEncontrado", "TelaJsonInvalido",
        "TelaCampoObrigatorioAusente", "TelaIdNaoCoincideComArquivo",
        "TelaIdIncorreto", "TelaEstruturaInvalida", "TelaElementoSemId",
        "TelaElementoSemTipo", "TelaTipoDesconhecido", "TelaGrupoInvalido",
        "EstiloErro",
    ],
    "taxonomia": [
        "TIPOS_CORPO_VALIDOS", "TIPOS_ESTRUTURAIS_VALIDOS",
        "ARRANJOS_CORPO_VALIDOS", "MODOS_DISTRIBUICAO_CORPO_VALIDOS",
        "ESTRUTURAS_GRUPO_VALIDAS", "PERFIL_RESULTADO_EXECUCAO",
    ],
    "caminho_base": ["_caminho_padrao_base", "_para_base"],
    "distribuicao_corpo": [
        "_eh_numero_nao_bool", "_validar_distribuicao_corpo",
    ],
    "validacao_matricial": [
        "_DM_CAMPOS_VALIDOS", "_DM_FORMACAO_POLITICAS", "_DM_ORDENS",
        "_DM_DIM_COLUNAS", "_DM_DIM_LINHAS", "_DM_DIST_H", "_DM_DIST_V",
        "_DM_EXPANSAO", "_DM_RESTO", "_DM_ALINH_H", "_DM_ALINH_V",
        "_dm_int", "_dm_literal", "_dm_medida", "_validar_dm_formacao",
        "_validar_dm_formacao_eixo", "_validar_dm_dimensionamento",
        "_validar_dm_dim_eixo", "_validar_dm_espacamento",
        "_validar_dm_politica_simples", "_validar_dm_par_eixos",
        "_validar_distribuicao_matricial",
    ],
    "lancador_config": ["_carregar_e_validar_config_lancador"],
    "grupos": [
        "_validar_quantidade_matriz", "_validar_distribuicao_matriz",
        "_validar_celulas_matriz", "_validar_matriz_grupo", "_validar_grupo",
    ],
    "envelope_pre_adr_0028": [
        "_TELAS_LEGADAS_D23", "_TELAS_VARIANTE2_LEGADAS",
        "_CAMPOS_ENVELOPE_PRE_ADR_0028", "_CAMPOS_ENVELOPE_BASE_PRE_ADR_0028",
        "_POLITICA_SELECAO_VALIDOS", "_POLITICA_PAGINACAO_VALIDOS",
        "_validar_valores_envelope_pre_adr_0028", "_console_em_escopo_d23",
    ],
    "d23_console": [
        "_POLITICAS_MODO_VALIDAS", "_MODOS_INICIAIS_VALIDOS",
        "_validar_d23_console",
    ],
    "perfil_resultado_execucao": [
        "_CAMPOS_CONSOLE_RESULTADO_PERMITIDOS",
        "_CAMPOS_CLASSICOS_PROIBIDOS_RESULTADO",
        "_validar_perfil_resultado_execucao",
    ],
    "conteudo_externo": [
        "APRESENTACOES_CONTEUDO_VALIDAS", "TIPOS_NIVEL_CONTEUDO_VALIDOS",
        "TIPOS_DESIGNADOR_VALIDOS", "_BLOCO_ESPECIFICO_POR_APRESENTACAO",
        "_BLOCOS_ESPECIFICOS_APRESENTACAO", "CAMPOS_RESULTADO_FISICO_PROIBIDOS",
        "_CAMPOS_COLUNA_RECONHECIVEL", "_validar_designador_conteudo",
        "_rejeitar_resultados_fisicos_conteudo", "_coluna_reconhecivel",
        "_validar_no_conteudo", "validar_conteudo_externo",
        "carregar_conteudo_externo",
    ],
    "estilo": [
        "EstiloResolvido", "carregar_estilo", "_resolver_cor_inativo",
        "_resolver_cor_alerta", "_exigir_secao", "_resolver_preset_default",
        "_resolver_catalogo", "_resolver_preset_ativo", "_campo_obrigatorio",
        "_validar_caractere", "_resolver_borda", "_resolver_chip",
        "_resolver_indicadores",
    ],
    "tela_json": [
        "_ID_TELA_RAIZ", "_PERFIL_AUSENTE", "_tem_lancador_em_elementos",
        "_iterar_consoles_do_corpo", "_validar_unicidade_ids_consoles",
        "carregar_tela",
    ],
}

proprietario_esperado = {
    simbolo: "{0}.{1}".format(PREFIXO, modulo)
    for modulo, simbolos in modulos_previstos.items()
    for simbolo in simbolos
}
assert len(proprietario_esperado) == sum(len(s) for s in modulos_previstos.values()), (
    "mapa fechado contem simbolo duplicado entre modulos previstos da secao 4.2"
)
assert len(proprietario_esperado) == 96, (
    "mapa fechado da secao 4.2 deve conter exatamente 96 simbolos nominais de "
    "nivel superior — divergencia indica secao 4.2 desatualizada ou mapa incompleto"
)


def definicoes_de_nivel_superior(caminho):
    arv = ast.parse(caminho.read_text(encoding="utf-8"), filename=str(caminho))
    nomes = set()
    for stmt in arv.body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            nomes.add(stmt.name)
        elif isinstance(stmt, ast.Assign):
            nomes.update(t.id for t in stmt.targets if isinstance(t, ast.Name))
        elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            nomes.add(stmt.target.id)
    return nomes


# Indexacao por AST de todas as definicoes/atribuicoes de nivel superior dos
# modulos previstos — registra, para cada simbolo, TODOS os modulos que o
# materializam (nao apenas o primeiro encontrado).
materializados = {}
for nome_modulo in modulos_previstos:
    caminho = pkg / "{0}.py".format(nome_modulo)
    assert caminho.is_file(), "arquivo previsto ausente: {0}".format(caminho)
    for simbolo in definicoes_de_nivel_superior(caminho):
        materializados.setdefault(simbolo, []).append("{0}.{1}".format(PREFIXO, nome_modulo))

for simbolo, modulo_esperado in proprietario_esperado.items():
    donos = materializados.get(simbolo, [])
    assert donos, (
        "{0} nao e materializado (FunctionDef/AsyncFunctionDef/ClassDef/"
        "atribuicao de nivel superior) por nenhum modulo previsto — pode "
        "estar apenas importado no proprietario esperado {1}, nao definido "
        "ali".format(simbolo, modulo_esperado)
    )
    assert len(donos) == 1, (
        "{0} materializado em mais de um modulo: {1} — proprietario nominal "
        "unico violado".format(simbolo, donos)
    )
    assert donos[0] == modulo_esperado, (
        "{0} materializado em {1}, mas a secao 4.2 declara proprietario "
        "{2}".format(simbolo, donos[0], modulo_esperado)
    )

# Nenhum simbolo de nivel superior materializado em tela/carregamento/ pode
# ficar fora do fechamento da secao 4.2.
extras = sorted(set(materializados) - set(proprietario_esperado))
assert not extras, (
    "simbolos de nivel superior materializados em tela/carregamento/ e "
    "ausentes do mapa fechado da secao 4.2: {0}".format(extras)
)

for nome_modulo in modulos_previstos:
    importlib.import_module("{0}.{1}".format(PREFIXO, nome_modulo))

init_path = pkg / "__init__.py"
assert init_path.is_file(), "tela/carregamento/__init__.py nao existe"
init_mod = importlib.import_module(PREFIXO)
init_arv = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
corpo_nao_docstring = [
    stmt for i, stmt in enumerate(init_arv.body)
    if not (
        i == 0 and isinstance(stmt, ast.Expr)
        and isinstance(stmt.value, ast.Constant) and isinstance(stmt.value.value, str)
    )
]
assert not corpo_nao_docstring, "__init__.py deve conter apenas docstring, sem logica"
_amostra_fachada = {"carregar_tela", "carregar_estilo", "TelaEstruturaInvalida"}
assert not any(hasattr(init_mod, s) for s in _amostra_fachada), (
    "__init__.py nao deve reexportar simbolos publicos da fachada"
)

print(
    "OK: proprietario nominal integral e unico por AST para os",
    len(proprietario_esperado),
    "simbolos de nivel superior da secao 4.2 — nenhum simbolo materializado "
    "fora do fechamento, nenhuma duplicacao entre modulos",
)
PY
```

```zsh
# 8. Nenhum simbolo mutavel duplicado (copia independente de constante)
#    entre um modulo interno e a fachada: a identidade de objeto deve
#    coincidir para toda estrutura mutavel reexportada.
python3 -c "
import tela.loader as f
import tela.carregamento.taxonomia as tax
assert f.TIPOS_CORPO_VALIDOS is tax.TIPOS_CORPO_VALIDOS
assert f.TIPOS_ESTRUTURAIS_VALIDOS is tax.TIPOS_ESTRUTURAIS_VALIDOS
assert f.ARRANJOS_CORPO_VALIDOS is tax.ARRANJOS_CORPO_VALIDOS
assert f.MODOS_DISTRIBUICAO_CORPO_VALIDOS is tax.MODOS_DISTRIBUICAO_CORPO_VALIDOS
print('OK: identidade de objeto preservada para constantes mutaveis reexportadas')
"
```

```zsh
# 9. Fechamento H0047-QA-004: relacao entre _ID_TELA_RAIZ (tela_json.py) e o
#    default do parametro `esperado` de TelaIdIncorreto (erros.py). erros.py
#    usa o literal "orquestrador" como default, NAO uma referencia a
#    _ID_TELA_RAIZ — preserva erros.py como modulo-base sem dependencias
#    internas e tela_json.py como proprietario nominal unico de
#    _ID_TELA_RAIZ. Assinatura, default, identidade e mensagem da excecao
#    permanecem identicos ao codigo atual (tela/loader.py:112-122).
python3 -c "
import inspect

import tela.loader as fachada
import tela.carregamento.erros as erros
import tela.carregamento.tela_json as tela_json

assert fachada.TelaIdIncorreto is erros.TelaIdIncorreto
assert tela_json._ID_TELA_RAIZ == 'orquestrador'

assinatura = inspect.signature(erros.TelaIdIncorreto.__init__)
parametro = assinatura.parameters['esperado']
assert parametro.default == 'orquestrador'

erro = erros.TelaIdIncorreto('outro')
assert erro.esperado == 'orquestrador'
assert str(erro) == (
    \"id esperado para tela raiz: 'orquestrador'; \"
    \"encontrado: 'outro'\"
)

print('OK: assinatura, default, identidade e mensagem de TelaIdIncorreto preservados')
"
```

---

## 8. Equivalência comportamental — testes focais e suíte completa

Todos os caminhos abaixo foram confirmados existentes nesta correção
(`ls tela/teste_*.py demo/teste_*.py`). Comandos nominais, executados nesta
ordem:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_loader.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_modelo.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_paginacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_fluxo_execucao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_resultado_execucao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_distribuicao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_navegacao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_selecao.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_diagnostico.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_explorar_barra_de_menus.py -q
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

A suíte canônica completa (`python -m pytest`, sem filtro) é condição
necessária, mas não suficiente (D-MOD-08) — os critérios de aceite da
seção 10 e as verificações estruturais da seção 7 também devem ser
satisfeitos. O baseline é **970 testes aprovados** (herdado do H-0046,
§1). A quantidade final pode variar somente por testes estruturais
autorizados (nenhum previsto por esta análise, §6.3), nunca por remoção ou
perda de casos.

---

## 9. Demonstração reproduzível

Não interativa (nenhum `input()`/TTY é aberto), cobrindo carregamento de
tela válida/inválida, conteúdo externo válido/inválido, estilo válido/
inválido e construção do modelo pela fachada pública. Usa fixtures já
existentes (`config/telas/demo/demo.json`,
`config/telas/demo/h0036_hierarquia_conteudo.json`, `config/estilo.json`) —
nenhuma configuração normativa nova é criada. O caso de estilo inválido usa
um diretório temporário vazio, técnica já empregada em
`tela/teste_loader.py` (ex.: L2833) para simular arquivo ausente sem
alterar `config/`.

```zsh
python3 - <<'PY'
import tempfile
from pathlib import Path

from tela.loader import (
    carregar_tela, TelaArquivoNaoEncontrado,
    carregar_conteudo_externo, validar_conteudo_externo,
    TelaCampoObrigatorioAusente,
    carregar_estilo, EstiloErro, EstiloResolvido,
)
from tela.modelo import construir_modelo, ModeloTela

# 1. Carregamento de tela valida.
tela_raw = carregar_tela(None, "demo", "config/telas/demo")
assert tela_raw["id"] == "demo"

# 2. Erro deterministico de tela invalida (arquivo inexistente).
try:
    carregar_tela(None, "tela_inexistente_xyz9", "config/telas/demo")
    raise AssertionError("deveria ter levantado TelaArquivoNaoEncontrado")
except TelaArquivoNaoEncontrado:
    pass

# 3. Carregamento de conteudo externo valido.
conteudo = carregar_conteudo_externo(
    None, "h0036_hierarquia_conteudo", "config/telas/demo"
)
assert conteudo["tipo"] == "multinivel"

# 4. Erro deterministico de conteudo externo invalido (campo obrigatorio
#    ausente — sem inventar fixture nova: dict sintetico em memoria).
try:
    validar_conteudo_externo({"tipo": "multinivel"})
    raise AssertionError("deveria ter levantado TelaCampoObrigatorioAusente")
except TelaCampoObrigatorioAusente:
    pass

# 5. Carregamento de estilo valido.
estilo = carregar_estilo()
assert isinstance(estilo, EstiloResolvido)

# 6. Erro deterministico de estilo invalido (diretorio sem config/estilo.json).
with tempfile.TemporaryDirectory() as tmp:
    try:
        carregar_estilo(caminho_base=Path(tmp))
        raise AssertionError("deveria ter levantado EstiloErro")
    except EstiloErro:
        pass

# 7. Construcao do modelo continuando a consumir a fachada publica.
modelo = construir_modelo(tela_raw)
assert isinstance(modelo, ModeloTela)
assert modelo.id == "demo"

print("OK: demonstracao reproduzivel — 7/7 verificacoes passaram")
PY
```

---

## 10. Critérios de aceite (D-MOD-08, materializados para H-0047)

| # | Critério | Prova reproduzível |
|---|---|---|
| 1 | API pública preservada | Comando da seção 5.2 (todos os símbolos presentes) |
| 2 | Comportamento observável preservado | Suíte completa da seção 8 verde |
| 3 | Testes focais do domínio aprovados | Comandos nominais da seção 8 (arquivos individuais) verdes |
| 4 | Suíte canônica completa aprovada | `PYTHONDONTWRITEBYTECODE=1 python -m pytest` verde, seção 8 |
| 5 | Concentração do arquivo original reduzida materialmente | Comando 5 da seção 7 (`wc -l`) + comando 6 da seção 7 (zero funções de domínio na fachada) |
| 6 | Fachada pequena e sem nova lógica substantiva | Comando 6 da seção 7 (zero funções, funções assíncronas, lambdas e classes na fachada, em qualquer profundidade; nenhum wrapper admitido nesta versão — exceção operacional focal, §11, se necessário) |
| 7 | Módulos nomeados por responsabilidade | Lista nominal da seção 4.2, cada módulo com responsabilidade explícita de uma frase |
| 8 | Ausência de dependências circulares | Comando 2 da seção 7 (grafo de imports; toda aresta validada contra o conjunto real de módulos do pacote antes do DFS — H0047-QA-001) |
| 9 | Ausência de importação inversa | Prova normativa AST — comando 3 da seção 7 (formas estáticas e dinâmicas de importação de `tela.loader`, H0047-QA-003); seção 5.3 e o `rg` do comando 3 mantidos apenas como evidência auxiliar |
| 10 | Localização mais direta das responsabilidades | Comandos 6 e 7 da seção 7 (autoridade nominal fechada para a fachada, existência física de `__init__.py` e de todos os módulos; comando 7 é prova **integral**, não amostral, de proprietário nominal único por AST para os 96 símbolos de nível superior da seção 4.2 — H0047-QA-002) + mapeamento completo da seção 4.2 |

Critérios específicos adicionais (decisões fechadas 3, 5, 6, 9, 10 do prompt
de criação):

| # | Critério específico | Prova reproduzível |
|---|---|---|
| 11 | Mesmas classes e mensagens de erro | Suíte completa (seção 8) verde — `TelaEstruturaInvalida`/demais exceções continuam sendo levantadas com o mesmo texto, pois nenhuma string de mensagem é alterada (apenas movimentação física); comando 9 da seção 7 comprova especificamente assinatura, default, identidade e mensagem de `TelaIdIncorreto` (H0047-QA-004) |
| 12 | Mesmos documentos aceitos e rejeitados | Suíte completa (seção 8) verde + demonstração (seção 9, itens 1-2) |
| 13 | Mesma estrutura retornada por `carregar_tela` | Suíte completa (seção 8) verde + demonstração (seção 9, item 1: chaves `id`/`schema`/`perfil`/`cabecalho`/`corpo`/`barra_de_menus`/`_raw`/`_config_lancador` inalteradas) |
| 14 | Mesmo conteúdo devolvido por `carregar_conteudo_externo` | Suíte completa (seção 8) verde + demonstração (seção 9, itens 3-4) |
| 15 | Mesma materialização de `EstiloResolvido` | Suíte completa (seção 8) verde + demonstração (seção 9, itens 5-6) |
| 16 | Mesma fronteira com `tela/modelo.py` | Comando da seção 5.2 (`tela/modelo.py` importa exclusivamente `TIPOS_CORPO_VALIDOS`/`TIPOS_ESTRUTURAIS_VALIDOS` da fachada) + demonstração (seção 9, item 7) |
| 17 | Ausência de leitura de arquivos pelo modelo | Inspeção nominal já registrada em §3.7 (`tela/modelo.py` não é alterado; não abre arquivo, não é tocado por este handoff) |
| 18 | Ausência de lógica geométrica no carregamento | Verificado pela ausência de dependência com `tela.distribuicao_matricial`, `tela.renderizador` e `tela.renderizacao.*` (comando 3 da seção 7) — o loader só valida a declaração, não calcula geometria (§4.1) |
| 19 | Nenhuma alteração em `tela/renderizacao/` | `git diff --stat` não deve listar nenhum arquivo sob `tela/renderizacao/` nem `tela/renderizador.py` (fora do manifesto, seção 6.4) |
| 20 | Nenhuma reorganização geral de testes | `arquivos_de_teste_com_ajuste_focal` vazio (seção 6.3); nenhum arquivo de teste é criado, dividido ou renomeado |
| 21 | Nenhuma alteração de schema, política ou configuração | Nenhum arquivo sob `config/` é criado ou alterado (seção 6.4); `git diff --stat` restrito a `tela/loader.py`, `tela/carregamento/*` e `docs/relatorios/IMP-0047-*.md` |

---

## 11. Exceção operacional focal

Se a implementação identificar necessidade estrita de alterar um arquivo não
autorizado pelo manifesto (seção 6), a implementação deve **parar antes da
alteração** e solicitar autorização informando:

- caminho exato do arquivo;
- motivo da necessidade;
- mudança esperada;
- impacto de não alterar (o que fica quebrado, incompleto ou incorreto sem
  essa mudança);
- relação estrita com o H-0047 (por que a modularização estrutural, por si
  só, exige esse arquivo).

Nenhuma alteração fora do manifesto pode ocorrer sem essa autorização
explícita registrada no relatório de implementação (seção 6.5).

---

## 12. Fora de escopo

- Alterar comportamento observável de qualquer função do loader.
- Corrigir defeitos funcionais encontrados durante a modularização —
  incluindo o defeito registrado em §3.9 (`_CAMPOS_ENVELOPE_PRE_ADR_0028`
  não referenciada), que deve ser preservado tal como está e apenas
  registrado no relatório de implementação.
- Alterar mensagens de erro.
- Alterar contratos comportamentais ou nomenclatura.
- Alterar qualquer JSON de configuração (`config/`).
- Alterar `tela/modelo.py`, salvo exceção documental posterior comprovada
  (seção 11).
- Alterar `tela/renderizador.py` ou `tela/renderizacao/` sem defeito material
  novo comprovado (não reabre o H-0046).
- Migrar consumidores externos para `tela.carregamento.*`.
- Reorganizar, dividir ou renomear a suíte de testes (pertence
  exclusivamente ao Handoff 3).
- Iniciar o Handoff 3 (reorganização de `tela/teste_renderizador.py` e
  testes diretamente relacionados).
- Executar a implementação descrita neste handoff.
- Fazer QA da própria entrega documental.
- Preparar ou realizar commit.

---

## 13. Consolidação final do Handoff 2

Esta seção registra o estado documental final deste handoff após a aprovação
técnica definitiva. O status inicial do frontmatter permanece como registro
da autorização emitida; o estado vigente é o desta consolidação.

```yaml
estado_final: IMPLEMENTATION_APPROVED
handoff:
  id: H-0047
  sequencia: 2 de 3
  estado: concluido
item:
  id: ITEM-0022
  estado: em_andamento
  passo_1: concluido
  passo_2: concluido
  passo_3: proximo
  dependencia_passo_2: fechamento_validado_do_passo_1
  dependencia_passo_3: fechamento_validado_do_passo_2
ADR:
  id: ADR-0039
  status: aceita
implementacao:
  status_final: IMPLEMENTATION_APPROVED
  testes_focais: 311_passed
  suite_completa: 970_passed
  demonstracao: 7_de_7
  validacao_manual: dispensada
  bloqueios: []
proximo_handoff: reorganizacao_de_tela_teste_renderizador_e_testes_relacionados
atividade_global_concluida: false
```
