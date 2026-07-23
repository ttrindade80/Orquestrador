---
name: indice-adr
description: Modelo de indice para Architecture Decision Records
metadata:
  type: indice
  scope: orquestrador
---

# Indice — ADRs

## Regra

ADR registra uma decisao arquitetural aprovada ou rejeitada. Uma ADR aceita nao
deve ser editada para mudar decisao; se a decisao mudar, criar nova ADR que
substitui a anterior.

Este indice registra as ADRs aceitas do projeto.

## Como criar ADR

1. Copiar `docs/templates/TEMPLATE_ADR.md`.
2. Nomear como `ADR-NNNN-descricao-curta.md`.
3. Preencher contexto, decisao, consequencias e contratos afetados.
4. Atualizar este indice.
5. Atualizar os contratos afetados antes de gerar handoffs dependentes.

## Decisoes registradas

| ID | Titulo | Status | Data |
|---|---|---|---|
| ADR-0001 | `menu` suporta modo matriz (múltiplas colunas) | aceita | 2026-07-05 |
| ADR-0002 | `menu` usa sobra à direita | aceita | 2026-07-05 |
| ADR-0003 | Vãos elásticos do `menu` | aceita | 2026-07-05 |
| ADR-0004 | `cor_inativo` e `cor_alerta` no schema de estilo | aceita | 2026-07-05 |
| ADR-0005 | lancador não é corpo navegável por [✥] | aceita | 2026-07-06 |
| ADR-0006 | renomeação `dado` para `console` e `Info` para `dashboard` | aceita | 2026-07-06 |
| ADR-0007 | tela de processamento é composição de tipos existentes | aceita | 2026-07-06 |
| ADR-0008 | modelo de configuração por tela | aceita | 2026-07-07 |
| ADR-0009 | caminho, nomenclatura e formato dos JSONs de tela | aceita | 2026-07-07 |
| ADR-0010 | composição hierárquica do corpo e dashboard como elemento funcional | aceita | 2026-07-08 |
| ADR-0011 | terminologia de arranjo: `vertical`/`horizontal` (aliases transicionais `sobreposto`/`lado_a_lado`) | aceita | 2026-07-08 |
| ADR-0012 | `barra_de_menus` declarativa por tela | aceita | 2026-07-08 |
| ADR-0013 | ocupação vertical da janela do terminal pelo corpo (`ocupacao_vertical_terminal`) — distinta de `corpo.arranjo` | aceita | 2026-07-09 |
| ADR-0014 | distribuição horizontal **responsiva** da `barra_de_menus` (`distribuicao = "horizontal"` como alias transitório de `modo = "horizontal_responsiva"`) + regra de alteração por termo específico completo | aceita | 2026-07-09 |
| ADR-0015 | Composição hierárquica e distribuição de área do corpo | aceita | 2026-07-10 |
| ADR-0016 | Execução em tela cheia (TTY) sem cintilação, com Ctrl+C escopado | aceita | 2026-07-10 |
| ADR-0017 | Redimensionamento reativo da TUI — SIGWINCH, ioctl(TIOCGWINSZ), cadeia de dimensões válidas e quadro mínimo de aviso (complementa ADR-0013 e ADR-0016) | aceita | 2026-07-11 |
| ADR-0018 | Semântica da ausência de distribuição e da alocação vertical de área do corpo — distingue arranjo de distribuição; ausência de `corpo.distribuicao` deixa de equivaler ao modo `igual` e preserva a construção orientada pelo conteúdo; distribuição explícita reparte a altura útil com preenchimento interno das áreas (substitui parcialmente a ADR-0015 no ponto ausência ≡ `igual`) | aceita | 2026-07-11 |
| ADR-0019 | Profundidade contada por aninhamento de grupos, multiplicidade estrutural e remoção da cardinalidade global de dashboard — define contagem por níveis de grupos (não por listas `elementos[]`); permite três níveis de grupos; permite múltiplos grupos irmãos e múltiplos elementos funcionais por grupo inclusive no nível 3; remove restrição global de zero ou um dashboard por tela (supera parcialmente ADR-0007 na cardinalidade de `dashboard`; substitui parcialmente ADR-0015 no critério de contagem de profundidade) | aceita | 2026-07-12 |
| ADR-0020 | Especialização bidimensional do nó `grupo` — formaliza os comportamentos `livre` (hierárquico existente) e `matriz` (grade comum com coordenadas explícitas); seletor declarativo `estrutura`; ausência de `estrutura` equivale a `livre`; distribuições obrigatórias e independentes por eixo (`matriz.linhas.distribuicao`, `matriz.colunas.distribuicao`); dimensões 2–4 por eixo; cobertura completa de células; rejeição determinística sem fallback; compatibilidade retroativa integral (especializa ADR-0015, ADR-0018 e ADR-0019) | aceita | 2026-07-12 |
| ADR-0021 | Separação entre demonstração, produto real e política de caminhos — preserva `tela/` como motor compartilhado; prevê `demo/` como aplicação demonstrativa futura; distingue `config/telas/<id>.json` para produto real e `config/telas/demo/<id>.json` para demonstração; preserva `config/estilo.json`; substitui parcialmente a ADR-0009 no ponto de raiz única de telas | aceita | 2026-07-14 |
| ADR-0022 | Ponto de entrada e tela inicial real do Orquestrador — reserva `orquestrador.py` como ponto de entrada futuro do produto real; reserva `config/telas/orquestrador.json` com `id: "orquestrador"` como tela inicial real; define envelope `cabecalho`, `corpo`, `barra_de_menus`; define corpo inicial com `console` e `dashboard` presentes sem entradas; barra mínima com `Esc`, `?` e acesso a estilos; preserva a separação `demo` sem alias nem fallback | aceita | 2026-07-14 |
| ADR-0023 | Largura mínima funcional do `lancador` — quando `area_lancador_w < lancador_caixa_min_w`, nenhuma representação válida do `lancador` é possível; o quadro mínimo canônico global (ADR-0017) substitui integralmente toda a tela normal; fallback local proibido; recuperação automática por redesenho quando área suficiente for restaurada | aceita | 2026-07-15 |
| ADR-0024 | Proibição de preenchimento vazio externo do corpo — o corpo é região de composição, não elemento visual; toda a área entre `cabecalho` e `barra_de_menus` deve pertencer visualmente a `console`, `dashboard` ou `lancador`; linhas em branco externas ao corpo são proibidas; DA-01 (cardinalidade unitária), DA-02 (múltiplos elementos sem distribuição), DA-03 (grupos e containers estruturais), DA-04 (invariante impossível — rejeição explícita, sem fallback); substitui parcialmente ADR-0013 (cláusula 4) e ADR-0018 (D2); implementação futura pelo H-0033 | aceita | 2026-07-15 |
| ADR-0025 | Distribuição matricial configurável de nível único do conteúdo dos elementos — capacidade genérica adotável explicitamente por `dashboard`, `console` e `lancador`; campo `distribuicao_matricial` no JSON do elemento organizador; formação responsiva (`preferencia_linhas`, `preferencia_colunas`) e fixa (`matriz_fixa`); ordem de preenchimento, dimensionamento, espaçamento (margens e vãos), distribuição do espaço excedente, alinhamento interno e fallback determinísticos e independentes; nível único; paginação e multinível fora do escopo; JSONs existentes não mudam silenciosamente; políticas específicas de `lancador` (ADR-0001, ADR-0002, ADR-0003) preservadas | aceita e aplicada | 2026-07-16 |
| ADR-0026 | Fornecimento externo de dados ao console por JSON multinível — separa configuração estrutural da tela de conteúdo de runtime; console recebe dados por JSON externo com envelope declarativo `{tipo, formato, dados}`; foco inicial em `tipo: "multinivel"`; níveis declarados explicitamente; consumidor não reconstrói hierarquia a partir de dados de domínio não normalizados; renderizador mantém responsabilidade exclusiva sobre geometria, dimensões, quebras, alinhamentos, paginação e posições físicas; script futuro produzirá os dados; protocolo de invocação do script e vínculo entre tela e fonte permanecem para decisão futura | aceita e aplicada | 2026-07-17 |
| ADR-0027 | Carregamento conjunto da tela e do conteúdo externo pelo ponto de entrada — formaliza a responsabilidade do ponto de entrada real `demo/demo.py` pelo carregamento separado do JSON estrutural e do JSON externo de conteúdo; associação externa por cenário sem campo de vínculo no JSON estrutural; schema semântico multinível obrigatório (`tipo: "multinivel"`, três apresentações, três tipos de nível, forma dos nós, designadores, 20 validações mínimas); JSONs permanentes para testes e demonstração; revisão dos JSONs afetados do H-0035 pelo H-0036; protocolo do Pipeline deferido | aceita e aplicada | 2026-07-17 |
| ADR-0028 | Apresentações de conteúdo multinível no console e alternância verbosa — regras normativas das apresentações `tabela`, `hierarquia`, `conjuntos_campos`; modelo hierárquico com raiz única; tipos conceituais de nível (contêiner, folha, campo); modos verboso e não verboso; **D23 — política de modo por tela**: três políticas (`somente_verboso`, `somente_nao_verboso`, `alternavel`) declaradas no JSON estrutural da tela em `formato.excesso.politica_modo`; modo inicial obrigatório para telas alternáveis em `formato.excesso.modo_inicial`; chip `[V] Verboso` e tecla `V` exclusivos de telas alternáveis; telas legadas (pré-D23) preservadas sem reinterpretação; quatro cenários futuros mínimos (§36.2); regra de alinhamento de dois níveis em modo verboso (§36.3); estado visual de sessão isolado e não persistido; quatro cenários de demonstração; 15 validações V-01 a V-15; paginação e contexto por apresentação; impossibilidade geométrica horizontal delegada às ADR-0017/ADR-0023; aplicação documental D1–D22 (2026-07-17) e D23 (2026-07-18); complementa ADR-0026 e ADR-0027 sem substituí-las | aceita e aplicada | 2026-07-17 |
| ADR-0029 | Nomenclatura modular e leitura seletiva — substitui o monólito `docs/NOMENCLATURA.md` por base terminológica modular em `docs/nomenclatura/` com 17 módulos (00–90); leitura seletiva por atividade; fachada permanente preservando `docs/NOMENCLATURA.md`; autoridade dos contratos sobre comportamento normativo; D-NOM-01 a D-NOM-16 fechadas; FASE_1 executada em 2026-07-20 (17 módulos PRE_FACHADA); FASE_2 executada em 2026-07-21 (fachada permanente criada, 17 módulos VIGENTES, 9 contratos com dependências declaradas, referências ativas migradas); QA pós-FASE_1: ADR_APPROVED_WITH_NOTES; QA pós-FASE_2 inicial: APLICACAO_ADR_FASE_2_REJECTED; PATCH_APLICACAO_ADR_FASE_2 aplicado; aguardando QA_POS_PATCH_APLICACAO_ADR_FASE_2 | aceita e aplicada | 2026-07-20/21 |
| ADR-0030 | Carregamento global e materialização do estilo — `config/estilo.json` como autoridade global exclusiva de aparência compartilhada; catálogo + `preset_default` como padrão canônico para `borda` e `chip`; materialização integral de todas as seções (`borda` 7 campos, `chip` 5 campos, `indicadores` 6 campos); preset ativo inicial: `"Borda Curva"` (borda), `"Colchete"` com `caixa_alta: false` (chip), `"Seta"` (cursor), `"Círculo"` (inclusão); escolha global — per-tela proibida neste modelo; aplicação documental aprovada em 2026-07-22; Bloco 1 implementado pelo H-0039 (carregamento global e materialização em runtime, hardcodings de borda e chip do escopo removidos — `_BORDAS` e `tipo_borda` removidos do renderer, validação manual aprovada); Blocos 2 (navegação) e 3 (seleção múltipla) futuros | aceita | 2026-07-22 |

## Exemplo de linha

| ADR-0000 | Escolher formato de persistencia do modulo exemplo | aceita | YYYY-MM-DD |
