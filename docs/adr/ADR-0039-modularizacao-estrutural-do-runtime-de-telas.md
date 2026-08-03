---
name: ADR-0039-modularizacao-estrutural-do-runtime-de-telas
description: "Modularização estrutural do runtime de telas em três handoffs sequenciais, preservando comportamento e fachadas públicas de renderizador.py e loader.py"
metadata:
  type: adr
  status: aceita
  id: ADR-0039
  data: 2026-08-03
  substitui: null
rastreabilidade:
  decisao_usuario: "Decisões fechadas D-MOD-01 a D-MOD-08, transportadas integralmente do prompt de criação desta ADR"
  rfc_origem: null
  issues_relacionadas: []
  contratos_afetados: []
  handoffs_previstos:
    - "Handoff 1 — modularização de tela/renderizador.py"
    - "Handoff 2 — modularização de tela/loader.py"
    - "Handoff 3 — reorganização de tela/teste_renderizador.py e testes diretamente relacionados"
---

# ADR-0039 — Modularização estrutural do runtime de telas

## 1. Status

`aceita`

## 2. Contexto

O runtime de telas do Orquestrador está concentrado em três arquivos de
grande extensão:

- `tela/renderizador.py`, com aproximadamente 4425 linhas;
- `tela/loader.py`, com aproximadamente 3143 linhas;
- `tela/teste_renderizador.py`, com aproximadamente 13000 linhas.

Esses números são contexto motivador, não metas normativas de tamanho. O
problema real é que a localização de trechos relevantes nesses arquivos
passou a exigir exploração ampla antes de qualquer correção focal, mesmo
quando a mudança necessária é pequena e isolada em uma única
responsabilidade.

O ciclo anterior fechado é o `ITEM-0003` (`ADR-0038`, paginação interativa
limitada em console), concluído em 2026-08-03 no commit `26a4365`, com
970 testes e matriz 60/60 aprovados. Esta ADR não reabre nem redefine
paginação — trata exclusivamente da organização estrutural do código que já
implementa as regras vigentes de renderização e carregamento.

O renderizador, o loader, o modelo, o estado de runtime, o console e a
composição declarativa de corpo já possuem fronteiras conceituais fechadas
por `docs/nomenclatura/01_NUCLEO_COMUM.md`,
`docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md`,
`docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`,
`docs/nomenclatura/32_CONSOLE.md`,
`docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`,
`docs/contratos/contrato_tela_json.md`,
`docs/contratos/contrato_composicao_corpo.md`,
`docs/contratos/contrato_console.md` e
`docs/contratos/contrato_json_console.md`. Esta ADR não redefine nenhuma
dessas fronteiras — apenas decide que a organização física dos arquivos de
implementação deve refletir essas fronteiras já normativas.

## 3. Decisão explícita do usuário

Registram-se, sem escolha de alternativa e sem introdução de comportamento,
política, schema ou API nova, as seguintes decisões fechadas:

### D-MOD-01 — Uma ADR e três handoffs

A arquitetura da modularização é definida por esta única ADR. A aplicação é
realizada posteriormente por três handoffs sequenciais:

1. modularização de `tela/renderizador.py`;
2. modularização de `tela/loader.py`;
3. reorganização de `tela/teste_renderizador.py` e dos testes diretamente
   relacionados.

Cada handoff parte do estado validado e fechado pelo handoff anterior.

### D-MOD-02 — Refatoração estritamente estrutural

A atividade preserva integralmente o comportamento vigente. Não são
introduzidas mudanças funcionais, correções oportunistas, novos schemas,
novas políticas, novas interações ou alterações deliberadas de resultado
observável. Defeitos encontrados durante a modularização são registrados e
deferidos para atividades próprias.

### D-MOD-03 — Separação por responsabilidade coesa

A extração de módulos segue responsabilidades funcionais reais. Tamanho de
arquivo é apenas indicador de concentração estrutural, não critério
suficiente para definir módulos. A organização não é determinada por
quantidades semelhantes de linhas nem pela sequência histórica das ADRs.

As fronteiras relevantes incluem, conforme o código real de cada handoff:
composição; geometria física; largura e altura; geração de linhas;
paginação; carregamento; validação; conversão; associação de conteúdo;
outras responsabilidades coesas comprovadamente existentes. Não se criam
módulos artificiais apenas para reduzir contagem de linhas.

### D-MOD-04 — Fachadas públicas compatíveis

Os arquivos `tela/renderizador.py` e `tela/loader.py` permanecem como
fachadas públicas compatíveis. Imports, funções, classes, constantes e
demais pontos públicos consumidos pelo código vigente continuam disponíveis
pelos caminhos atuais. Consumidores não são migrados para novos caminhos
apenas para justificar a modularização. As fachadas delegam às
implementações extraídas e não acumulam nova lógica substantiva.

### D-MOD-05 — Subpacotes por domínio

As responsabilidades extraídas são organizadas, respectivamente, nos
subpacotes:

```text
tela/renderizacao/
tela/carregamento/
```

Não se usa um subpacote genérico `tela/interno/`. Não se espalha a
implementação principalmente em módulos irmãos com prefixos como
`renderizador_*` e `loader_*` diretamente em `tela/`. Os nomes internos
finais devem refletir responsabilidades reais comprovadas no código, sem
criar arquitetura além da necessária.

### D-MOD-06 — Preservação das fronteiras conceituais

A modularização respeita as seguintes distinções vigentes, cuja autoridade
comportamental completa permanece nos módulos e contratos citados:

- o renderizador produz a representação física, incluindo linhas, colunas,
  posições, alinhamentos, dimensões, quebras, truncamentos e paginação
  (`docs/nomenclatura/01_NUCLEO_COMUM.md` §4.15;
  `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`);
- o loader lê, valida, converte e prepara documentos e conteúdo para o
  modelo (`docs/nomenclatura/01_NUCLEO_COMUM.md` §4.13;
  `docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`);
- o modelo preserva a estrutura semântica (`docs/nomenclatura/01_NUCLEO_COMUM.md` §4.14);
- o estado de runtime permanece distinto da configuração concreta
  (`docs/nomenclatura/01_NUCLEO_COMUM.md` §4.6–§4.7);
- composição declarativa não é decidida pelo renderizador
  (`docs/nomenclatura/20_TELA_CORPO_E_COMPOSICAO.md` §4.3;
  `docs/contratos/contrato_composicao_corpo.md` §2);
- página, foco, cursor e seleção são camadas distintas do estado do console
  (`docs/nomenclatura/32_CONSOLE.md` §4.2, §4.5, §4.6, §4.8;
  `docs/contratos/contrato_console.md` §22–§24);
- carregamento e associação de conteúdo não se confundem com apresentação
  física (`docs/nomenclatura/43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md`;
  `docs/contratos/contrato_json_console.md` §11 e §12).

Esta ADR referencia esses módulos e contratos proprietários sem reproduzir
integralmente suas regras.

### D-MOD-07 — Reorganização dos testes por responsabilidade

Os testes são reorganizados pelas mesmas responsabilidades funcionais
adotadas pelos módulos de produção. O terceiro handoff separa o conteúdo
atualmente concentrado em `tela/teste_renderizador.py` e testes diretamente
relacionados.

Devem ser preservados: casos testados; fixtures; entradas; expectativas;
cobertura comportamental; critérios de regressão; resultados observáveis.
Não se realiza reescrita generalizada da suíte. Não se divide testes apenas
em arquivos numerados ou em blocos de tamanho semelhante.

### D-MOD-08 — Critérios estruturais e comportamentais de conclusão

Cada handoff deve comprovar:

1. preservação da API pública aplicável;
2. preservação do comportamento observável;
3. execução dos testes focais do domínio;
4. execução da suíte canônica completa;
5. redução material da concentração do arquivo original;
6. fachadas pequenas e sem nova lógica substantiva;
7. responsabilidades extraídas para módulos nomeados por domínio;
8. ausência de dependências circulares;
9. ausência de importação inversa em que os módulos internos dependam da
   fachada pública;
10. localização mais direta das responsabilidades modificadas.

Não se estabelece limite arbitrário ou universal de linhas por arquivo.
Suíte verde é condição necessária, mas não é suficiente para aprovar a
modularização.

## 4. Decisão

Fica decidida a modularização estrutural do runtime de telas do
Orquestrador, restrita à reorganização física do código existente, sem
alteração de comportamento, schema, política ou API pública, conduzida em
três handoffs sequenciais (D-MOD-01), cada um sujeito aos critérios de
conclusão de D-MOD-08, a serem materializados nos critérios de aceite
definidos na criação e na implementação de cada handoff.

Os handoffs extraem responsabilidades coesas comprovadas no código real
(D-MOD-03) para os subpacotes `tela/renderizacao/` e `tela/carregamento/`
(D-MOD-05), preservando `tela/renderizador.py` e `tela/loader.py` como
fachadas públicas compatíveis que delegam às implementações extraídas
(D-MOD-04), e respeitando integralmente as fronteiras conceituais já
fixadas pela nomenclatura e pelos contratos vigentes (D-MOD-06). Os testes
concentrados em `tela/teste_renderizador.py` são reorganizados no terceiro
handoff pela mesma lógica de responsabilidade, sem perda de cobertura
(D-MOD-07).

A definição da lista final de módulos internos, seus nomes exatos e a
distribuição precisa de funções e classes entre eles não são fechadas por
esta ADR — são levantadas focalmente durante a criação de cada handoff, a
partir da leitura do código real correspondente.

## 5. Consequências

### Positivas

- Menor custo de localização de código.
- Menor necessidade de exploração ampla antes de patches focais.
- Isolamento mais claro de regressões.
- Handoffs menores e reversíveis.
- Preservação dos caminhos públicos vigentes.

### Custos e restrições

- Aumento controlado da quantidade de módulos internos.
- Necessidade de verificar ausência de ciclos de importação a cada handoff.
- Necessidade de comprovar equivalência da suíte de testes a cada handoff.
- Handoffs subsequentes dependem do fechamento validado do handoff anterior
  (D-MOD-01), o que introduz sequenciamento obrigatório na execução.

### Artefatos afetados

| Artefato | Aplicação necessária |
|---|---|
| `tela/renderizador.py` | Handoff 1 — passa a atuar como fachada pública compatível, delegando a `tela/renderizacao/` |
| `tela/loader.py` | Handoff 2 — passa a atuar como fachada pública compatível, delegando a `tela/carregamento/` |
| `tela/teste_renderizador.py` | Handoff 3 — reorganizado por responsabilidade, preservando cobertura integral |
| `tela/renderizacao/` (novo subpacote) | Handoff 1 — recebe as implementações extraídas de `renderizador.py` |
| `tela/carregamento/` (novo subpacote) | Handoff 2 — recebe as implementações extraídas de `loader.py` |

## 6. Compatibilidade e transição

- Compatibilidade obrigatória com os imports públicos vigentes de
  `tela/renderizador.py` e `tela/loader.py`.
- Compatibilidade comportamental integral: nenhum resultado observável do
  runtime de telas muda em decorrência desta atividade.
- Nenhuma migração pública de consumidores é feita neste ciclo.
- Nenhuma depreciação de `tela/renderizador.py` ou `tela/loader.py` é
  declarada por esta ADR.
- Nenhuma alteração normativa dos contratos de tela, console, paginação ou
  carregamento é feita ou implicada por esta ADR.
- Movimentação interna de símbolos é possível somente quando o símbolo
  permanece reexportado pela fachada aplicável (`tela/renderizador.py` ou
  `tela/loader.py`).

## 7. Alternativas consideradas

Não se registra escolha entre alternativas nesta ADR. As decisões acima
foram fornecidas já fechadas; esta ADR apenas as documenta.

## 8. Itens fora de escopo

- Implementar a modularização.
- Definir a lista final de módulos internos sem leitura do código real.
- Corrigir defeitos funcionais encontrados durante a modularização.
- Alterar contratos comportamentais.
- Alterar schemas.
- Alterar APIs públicas.
- Migrar consumidores.
- Criar ou aplicar handoffs.
- Reorganizar arquivos nesta etapa.
- Atualizar backlog, histórico, índice de nomenclatura ou contratos.
- Executar testes.
- Fazer commit.

## 9. Critérios para aplicação

Estes critérios regem exclusivamente a aplicação documental desta ADR. Não
regem a criação, a implementação nem o aceite dos handoffs.

- [ ] A decisão foi propagada somente aos documentos realmente afetados.
- [ ] Não restaram contradições normativas ativas.
- [ ] Nenhuma implementação de código foi feita durante a aplicação
      documental.
- [ ] Caminhos permanecem relativos à raiz do Orquestrador.
- [ ] Diretórios previstos (`tela/renderizacao/`, `tela/carregamento/`) e
      diretórios já criados foram distinguidos em cada handoff.
- [ ] Os três handoffs sequenciais (D-MOD-01) permanecem registrados nesta
      ADR.
- [ ] A natureza estritamente estrutural desta atividade permanece
      explícita no documento.
- [ ] Nenhum contrato comportamental vigente foi redefinido por esta
      aplicação documental.

Os dez critérios de D-MOD-08 (seção 3) e as preservações específicas de
cada handoff — incluindo fachadas pequenas sem nova lógica substantiva e a
preservação integral da suíte de testes tratada no Handoff 3 — não são
critérios da aplicação documental. Devem ser materializados como critérios
de aceite na criação e na implementação de cada um dos três handoffs.

## 10. Bloqueios

Nenhum.

## Riscos e medidas de contenção

| Risco | Medida de contenção |
|---|---|
| Extração introduzir dependência circular entre `tela/renderizacao/`, `tela/carregamento/` e as fachadas | Cada handoff verifica explicitamente ausência de dependências circulares (D-MOD-08, item 8) antes do fechamento |
| Fachada acumular lógica substantiva ao invés de apenas delegar | Cada handoff verifica explicitamente que a fachada permanece pequena e sem nova lógica substantiva (D-MOD-08, item 6) |
| Módulo interno importar de volta a fachada pública, criando importação inversa | Cada handoff verifica explicitamente a ausência dessa importação inversa (D-MOD-08, item 9) |
| Reorganização dos testes (Handoff 3) perder cobertura ou alterar critérios de regressão | D-MOD-07 exige preservação integral de casos, fixtures, entradas, expectativas e critérios; reescrita generalizada é proibida |
| Fronteiras conceituais (renderizador × loader × modelo × estado de runtime × console) se confundirem durante a extração | D-MOD-06 fixa as distinções vigentes como obrigatórias, remetendo à nomenclatura e aos contratos como autoridade comportamental |
| Definição prematura da lista de módulos internos, sem base no código real | Esta ADR não fecha a lista final; cada handoff levanta focalmente as responsabilidades no início da sua própria execução |

## Relação com ADR-0038

A ADR-0038 fechou, para o `ITEM-0003`, a especificação da paginação
interativa limitada em console, concluída pelo H-0045 e registrada como
último ciclo fechado antes desta atividade (commit `26a4365`). Esta ADR não
redefine paginação, não reabre a ADR-0038 e não altera nenhuma das decisões
D-PAG-01 a D-PAG-14 nela fixadas. A relação com a ADR-0038 é estritamente de
sucessão temporal de ciclo — o código que implementa essas decisões é um dos
alvos da reorganização estrutural aqui decidida, sem mudança de
comportamento.
