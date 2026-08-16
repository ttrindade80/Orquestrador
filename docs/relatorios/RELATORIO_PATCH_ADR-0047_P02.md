# Relatório — Patch Documental P02 da ADR-0047

## Metadata

- Etapa: `PATCH_ADR`
- Objeto: ADR-0047
- Patch: P02
- Artefato alterado: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- Artefato criado: `docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md` (este arquivo)

## Rastreabilidade

- `cadeia.raiz`: `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
- `cadeia.predecessor_imediato`: `docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0073.md`

## Causa

Bloqueio documental descoberto durante a criação do H-0073
(`docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0073.md`, seção "Campos reais
de H-0063 identificados" e "Bloqueios"): a ADR-0047 (§4.11, incluindo o
bloco YAML de exemplo e o item de checklist correspondente em §10)
pressupunha que a tela `h0063_estilo_estrutura_navegacao_dois_niveis.json`
já possuía dois campos semânticos separados — um de texto/nome e outro de
exemplo visual — prontos para alimentar as duas colunas da apresentação
tabular local. Essa suposição não corresponde ao estado real do produtor de
conteúdo, o que impedia H-0073 de fechar `tabela.colunas` para H-0063 sem
inventar um nome de campo (proibido) ou sem violar a redação anterior de
§4.11 ("não inventa nem renomeia esses campos reais de conteúdo").

## Fato corrigido

Leitura focal confirmou:

- `tela/estilo.py::ControladorTelaEstilo._construir_conteudo` (linhas
  146–213) é o produtor real do conteúdo dinâmico de H-0063. Para cada nó
  filho, popula exatamente os campos `navegavel`, `selecionavel`, `titulo`,
  `categoria` e `preset` — nenhum campo isolado de amostra visual.
- `campos["titulo"]` é o retorno direto de
  `tela/renderizacao/estilo.py::compor_titulo_com_amostra` (linhas
  164–175), que concatena `nome_preset` (ajustado a `largura_nome`), o
  separador canônico e o resultado de `amostra_de_preset(categoria, dados)`
  em uma única string lógica.
- Logo, a amostra visual já é calculada hoje dentro do fluxo de composição
  (`amostra_de_preset`), mas só é exposta embutida em `titulo` — não existe
  campo separado contendo apenas essa amostra.

A afirmação anterior da ADR-0047 de que H-0063 já possuía dois campos
semânticos separados para alimentar as duas colunas não corresponde a esse
estado real. Esse é o fato material corrigido por este patch.

## Decisão `preset` + `amostra`

Fechado por este patch, em nova subseção §4.11.1:

- Primeira coluna: `campo: preset`, referenciando `campos["preset"]`,
  já existente, preservado integralmente.
- Segunda coluna: `campo: amostra`, referenciando `campos["amostra"]`,
  campo novo somente como campo da projeção de conteúdo entregue ao
  console. Seu valor semântico já existe hoje no fluxo — é o mesmo
  resultado hoje calculado por `amostra_de_preset` dentro de
  `compor_titulo_com_amostra` — e deve ser obtido a partir desse
  valor/componente semântico real já disponível no fluxo de composição.
  É expressamente proibido obter `amostra` por parsing posterior de
  `titulo`.
- O bloco YAML de exemplo em §4.11 e o item de checklist correspondente em
  §10 foram atualizados para fixar literalmente `preset` e `amostra` como
  nomes das duas colunas, fechando o schema estrutural da configuração
  futura de H-0063:

```yaml
formato.dois_niveis_por_foco.filho:
  tabulacao:
    minimo: 5
    maximo: 10
  designador:
    tipo: nenhum
  apresentacao: tabela
  tabela:
    colunas:
      - campo: preset
      - campo: amostra
    espacamento:
      minimo: 3
      maximo: 8
```

## Preservação de `titulo`

Fixado explicitamente em §4.11.1: `campos["titulo"]` permanece
integralmente inalterado, com o mesmo valor e significado atuais, para
consumidores preexistentes (inclusive o modo `apresentacao = "texto"` já
usado por outras telas e o teste existente
`tela/teste_estilo_h0070.py::test_amostras_de_cada_categoria_...`, citado em
`RELATORIO_CRIACAO_HANDOFF_H-0073.md`). Nenhum campo existente é removido,
renomeado ou redefinido.

## Distinção: extensão da projeção × alteração de conteúdo

Fixado em §4.11.1: a criação de `campos["amostra"]` é uma extensão
compatível da projeção de dados entregue ao console — não constitui
alteração do conteúdo visível ou do significado dos dados. Permanecem
idênticos: nomes de categorias, nomes de presets, textos existentes,
amostras visuais existentes, símbolos, ordem, valores de estilo, seleção,
candidato, baseline, aplicação, persistência e publicação. A existência de
`campos["amostra"]` na projeção não transfere configuração visual para os
dados: a decisão de exibi-lo como segunda coluna continua pertencendo
exclusivamente à configuração estrutural da tela (§4.13, §5), preservando
integralmente a fronteira já aprovada entre JSON estrutural (declara COMO
apresentar), conteúdo/dados (fornece O QUE apresentar) e renderer (calcula
geometria física).

## Trechos materiais corrigidos

Em `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`:

1. §1 (Status) — adicionado parágrafo registrando o patch P02, sua causa e
   seu efeito, com `QA_POS_PATCH_ADR` como pendência declarada.
2. §4.11 — bloco YAML de exemplo: os dois campos-placeholder
   (`<campo_existente_de_texto_nome_do_preset>` e
   `<campo_existente_de_exemplo_visual_do_preset>`) substituídos pelos
   nomes literais `preset` e `amostra`.
3. §4.11 — parágrafo que afirmava/pressupunha dois campos já separados e
   proibia a extensão da projeção ("Esta ADR não inventa nem renomeia
   esses campos reais de conteúdo...") substituído por remissão aos nomes
   literais fechados em §4.11.1, preservando intacta a frase de proibição
   de alteração de conteúdo/presets/textos/etc.
4. Nova subseção §4.11.1 — registra o fato corrigido, a decisão fechada
   `preset`/`amostra`, a preservação de `titulo` e a distinção entre
   extensão da projeção e alteração de conteúdo.
5. §10 (Critérios para aplicação) — item de checklist referente a H-0063
   reescrito para citar os nomes literais `preset`/`amostra`, a
   proveniência de `amostra` (mesmo valor semântico já existente,
   proibição de parsing de `titulo`) e a preservação explícita de
   `campos["titulo"]`.

Nenhuma outra seção da ADR-0047 foi alterada. D-DNF-01 a D-DNF-11 (§3),
incluindo D-DNF-09, permanecem transportadas verbatim, sem reabertura de
substância — apenas a lacuna de nomenclatura literal e o pressuposto factual
incorreto em §4.11/§10 foram corrigidos, seguindo o mesmo padrão já usado
pela correção de fronteira QA-ADR-0047-001 (§4.13), que também corrigiu por
adição de seção nova em vez de reescrever a decisão original.

## Verificações

- Leitura integral de `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
  e de `docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0073.md`.
- Leitura focal confirmada por grep (`rg -n "_construir_conteudo"
  tela/estilo.py`; `rg -n "def compor_titulo_com_amostra"
  tela/renderizacao/estilo.py`) seguida de leitura das linhas 140–213 de
  `tela/estilo.py` e 164–205 de `tela/renderizacao/estilo.py` — nenhum
  outro arquivo de código, teste, contrato, nomenclatura, config ou
  relatório foi lido.
- `git status --short` confirmado antes e depois do patch: nenhum arquivo
  além de `docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md`
  (alterado) e `docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md` (criado)
  foi tocado nesta execução.
- `git diff --check -- docs/adr/ADR-0047-formatacao-filhos-dois-niveis-por-foco.md
  docs/relatorios/RELATORIO_PATCH_ADR-0047_P02.md` executado (ambos os
  arquivos estão untracked no repositório local, portanto sem base de
  comparação para o Git; nenhum problema de espaço em branco identificado
  na inspeção manual do conteúdo escrito).

## Bloqueios

nenhum
\n