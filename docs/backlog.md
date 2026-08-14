---
name: backlog-orquestrador
description: Modelo neutro para registrar trabalho planejado
metadata:
  type: backlog
  scope: orquestrador
---

# Backlog — Modelo

## Regra

Este arquivo deve conter somente trabalho ativo, nos estados `planejado`,
`bloqueado`, `em_andamento` ou `pronto_para_handoff`. Item encerrado
(concluido, cancelado, substituido ou incompativel) nao permanece neste
arquivo — no mesmo fechamento documental em que for encerrado, e removido
daqui e registrado em `docs/HISTORICO.md`. Este arquivo nao e contrato, nao
e autorizacao de implementacao e nao substitui handoff.

Ao copiar este padrao para um projeto novo, manter apenas exemplos ou limpar
esta lista.

## Formato

```markdown
### ITEM-NNNN — [Titulo curto]
**Tipo:** contrato | implementacao | qa | documentacao | infraestrutura
**Prioridade:** alta | media | baixa
**Status:** planejado | bloqueado | em_andamento | pronto_para_handoff
**Descricao:** [O que precisa existir]
**Pre-requisitos:** [Contratos, ADRs ou decisoes necessarias]
**Proxima acao:** [A menor acao documental verificavel]
```

## Itens planejados

> A ordem dos itens deste backlog nao representa prioridade nem sequencia de execucao. Cada item somente podera avancar pelo fluxo documental aplicavel.

### ITEM-0004 — Registro e execucao declarativa de acoes individuais
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir e implementar o registro controlado de acoes declarativas associadas aos itens do console.
**Pre-requisitos:** Fechamento documental do catalogo, parametros permitidos, validacao e despacho das acoes.
**Proxima acao:** Realizar levantamento focal do catalogo ou registro vigente de acoes antes da ADR especializada.

### ITEM-0005 — Abertura e retorno entre telas por acao
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Permitir que acoes declarativas abram telas conhecidas pelo sistema e que o usuario retorne ao contexto anterior.
**Pre-requisitos:** Registro de acoes individuais formalizado.
**Proxima acao:** Levantar as regras vigentes de abertura, pilha de telas, retorno e preservacao de estado.

### ITEM-0018 — Selecionar todos apenas na pagina atual
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Permitir limitar a selecao em massa (`Todos`) aos itens selecionaveis da pagina corrente do console, em vez do conjunto filtrado completo em todas as paginas.
**Pre-requisitos:** Registrado pela ADR-0034 (D-SEL-24); `ITEM-0006` concluido em 2026-07-29; `ITEM-0003` concluido em 2026-08-03 pela ADR-0038 e pelo H-0045, com QA tecnico e validacao manual aprovados.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural propria para a especializacao de `Todos` à pagina atual.

### ITEM-0019 — Selecao compartilhada entre consoles compativeis
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Permitir um conjunto de selecao comum entre consoles que exibam dados compativeis.
**Pre-requisitos:** Registrado pela ADR-0034 (D-SEL-24); `ITEM-0006` concluido em 2026-07-29.
**Proxima acao:** Realizar levantamento focal e criar ADR propria para identidade, compatibilidade e ciclo de vida da selecao compartilhada.

### ITEM-0021 — Modos de visualizacao das telas de resultado
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Permitir telas de resultado somente verbosas, somente nao verbosas ou alternaveis, alem da politica `somente_verboso` fixada pela ADR-0034.
**Pre-requisitos:** Registrado pela ADR-0034 (D-SEL-24); `ITEM-0006` concluido em 2026-07-29.
**Proxima acao:** Realizar levantamento focal e criar ADR propria para as politicas e transicoes de modo das telas de resultado.

### ITEM-0025 — Integração de arvore_colapsavel com multiline e paginação
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** BACKLOG / FUTURO. Validar `arvore_colapsavel` multinivel com conteúdo multilinha e paginação quando o conteúdo exceder a área disponível, incluindo PageUp/PageDown vigentes, mudança de página, projeção visível por página, cursor válido antes/depois da mudança de página, expansão/recolhimento com recomputação da projeção, alteração do número/distribuição de páginas causada pelo estado da árvore, renderer e mapa físico usando a mesma projeção e demonstração TTY focal. A paginação deve consumir a autoridade universal vigente da ADR-0041, usando PageUp/PageDown e a representação `[PgUp][PgDn] Páginas`; as setas continuam pertencendo à navegação interna da árvore e não paginam. A integração com multiline e paginação permanece trabalho futuro; esta alteração não implementa a capacidade.
**Pre-requisitos:** ITEM-0007 concluído; ciclo próprio de especificação e validação. Exclui nova política universal de paginação, H-0054, H-0055, nova geometria geral multinível, seleção, Enter e execução.
**Proxima acao:** Criar especificação própria e planejar o ciclo sem criar ADR ou handoff nesta etapa.

### ITEM-0026 — Persistência da escolha de filho por pai
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** persistir no JSON de dados a escolha runtime de exatamente um filho por pai em `dois_niveis_por_foco`, sem alterar a semântica deste ciclo.
**Pre-requisitos:** ITEM-0007 concluído e especificação/decisão própria para persistência.
**Proxima acao:** Iniciar especificação própria, sem implementar nesta etapa.

### ITEM-0023 — Apresentacao de filho ativo em grupos multinivel
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Implementar em ciclo futuro a apresentacao `Pai: filho_ativo`, preservando o filho ativo como filho logico e estrutural, promovendo-o somente visualmente e sem duplica-lo na lista inferior; quando outro filho se tornar ativo, recompor a apresentacao conforme as definicoes fechadas. Este item nao define Enter, execucao, confirmacao, cancelamento, previa ou persistencia.
**Pre-requisitos:** ITEM-0007 concluido. Definicoes fechadas preservadas externamente em `DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md`, a ser fornecido pelo usuario ao futuro gerente.
**Proxima acao:** Apos ITEM-0007, iniciar especificacao propria somente para as partes ainda abertas desta capacidade, preservando as definicoes ja fechadas.

### ITEM-0024 — Distribuicao geometrica de grupos multinivel
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Definir e implementar em ciclo futuro a distribuicao visual dos blocos de pais e filhos multinivel, incluindo multiplas colunas e linhas, preservacao da ordem, quebra horizontal, margens, espacamentos, compactacao local de um unico grupo e continuidade entre paginas, sem alterar a semantica dos toroides de navegacao.
**Pre-requisitos:** ITEM-0007 concluido. Definicoes fechadas preservadas externamente em `DEFINICOES_DIFERIDAS_MULTINIVEL_PARA_CICLOS_FUTUROS.md`, a ser fornecido pelo usuario ao futuro gerente.
**Proxima acao:** Apos ITEM-0007, iniciar ciclo proprio de especificacao de geometria e layout, preservando as definicoes ja fechadas e sem incorporar apresentacao de filho ativo.

### ITEM-0008 — Conteudo composto e heterogeneo no console
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Avaliar e implementar conteudos compostos por uma sequencia ordenada de blocos de tipos diferentes, incluindo a possibilidade de tabelas em niveis de conteudo multinivel.
**Pre-requisitos:** Definicao dos tipos de bloco permitidos e de sua composicao.
**Proxima acao:** Realizar levantamento focal da necessidade e criar decisao arquitetural propria.

### ITEM-0009 — Dashboard passivo de resumo de estagio ou pipeline
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Implementar o dashboard como elemento auxiliar e passivo para apresentar resumos do estagio atual ou do pipeline, incluindo resumos, estados, dados, resultados, dry-run, indicadores, conteudo tabular e apresentacao com titulo ou cabecalho.
**Pre-requisitos:** Existencia de uma tela e de dados reais que justifiquem o primeiro contrato especializado.
**Proxima acao:** Definir o primeiro caso real de uso e criar o contrato de conteudo correspondente.

### ITEM-0012 — Tiling por tela
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir e implementar alteracao contextual do tiling/arranjo somente da tela corrente. O tiling fica fora do ITEM-0010 e nao sera oferecido como preferencia global na tela de estilos. O acionamento futuro previsto e a tecla `|`; ao aciona-la, a funcionalidade devera partir do tiling/arranjo da tela corrente e afetar somente essa tela. Persistencia, contrato de alteracao e demais detalhes permanecem para especificacao propria deste item.
**Pre-requisitos:** Semantica vigente de `corpo.arranjo` e decisao propria sobre ciclo de vida/persistencia da alteracao por tela.
**Proxima acao:** Realizar especificacao focal propria antes de ADR ou implementacao.

### ITEM-0013 — Promocao do estado dos metadados de estilo
**Tipo:** documentacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir o criterio formal para promover `_meta.status` de `rascunho_inicial` para outro estado documental.
**Pre-requisitos:** Criterios de maturidade e autoridade do estado aprovados.
**Proxima acao:** Realizar decisao documental focal.

### ITEM-0014 — Cabecalho em largura reduzida
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Definir e implementar o comportamento do cabecalho quando a largura disponivel for insuficiente.
**Pre-requisitos:** Decisao do usuario sobre quebra, truncamento, reticencias, fallback e relacao com `max_caracteres`.
**Proxima acao:** Apresentar alternativas visuais e obter decisao focal do usuario.

### ITEM-0016 — Reconciliar o comportamento de tx no console
**Tipo:** documentacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Reconciliar a contradição documental vigente sobre o comportamento de `tx` no console.
**Pre-requisitos:** Levantamento focal da nomenclatura, contrato e ADRs que tratam truncamento e apresentação textual.
**Proxima acao:** Identificar a contradição exata e obter decisão documental própria.

### ITEM-0027 — Composição e justificação global de texto da TUI
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Adotar algoritmo canônico/global de composição de parágrafo e justificação para todas as ocorrências de texto justificado da TUI, evitando soluções locais independentes por componente.
**Pre-requisitos:** Ciclo próprio de especificação.
**Proxima acao:** Iniciar ciclo futuro próprio, sem implementar nesta etapa.

### ITEM-0029 — Ajuda global por F1 e ajuda declarativa dos chips
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Padronizar F1 como tecla universal de Ajuda, substituindo o acionamento universal atualmente associado a `?`, e tornar a ajuda derivável das declarações reais da interface. O trabalho deve cobrir F1 como comando universal de Ajuda; substituição de `[?] Ajuda` pelo acionamento correspondente a F1; texto de ajuda correspondente à função do chip em toda declaração de chip; apresentação, em cada tela, das funções das teclas/chips efetivamente mostrados na `barra_de_menus`; apresentação de todas as teclas F globais formalmente definidas; e prevenção de uma segunda lista manual de ajuda desconectada das declarações vigentes.
**Pre-requisitos:** Contratos vigentes de chip, barra de menus e mecanismo de ajuda.
**Proxima acao:** Especificar schema declarativo do texto de ajuda, composição da ajuda contextual e migração de `?` para F1.

### ITEM-0030 — F11 para tela cheia
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Avaliar e implementar F11 como comando global associado à experiência de tela cheia do Orquestrador, respeitando as capacidades e limitações reais do terminal/ambiente hospedeiro.
**Pre-requisitos:** Levantamento focal do tratamento de F11 pelo terminal e do limite de responsabilidade do Orquestrador.
**Proxima acao:** Realizar levantamento e especificação focal antes de ADR.

### ITEM-0031 — Mapa global de teclas de função
**Tipo:** documentacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Consolidar o mapa global de teclas de função, registrando as teclas já reservadas: F1 = Ajuda, F4 = Estilo e F11 = Tela Cheia. A implementação e a definição comportamental de F11 continuam subordinadas ao trabalho específico de tela cheia, ITEM-0030. F2, F3 e F5 ainda estão sem função: não recebem função concreta neste momento; qualquer reserva futura depende de necessidade real e deve considerar convenções conhecidas dessas teclas, que não devem ser ocupadas apenas porque estão disponíveis.
**Relações:** ITEM-0029 — política de Ajuda por F1 e exposição das teclas F na ajuda; ITEM-0030 — definição própria de F11/tela cheia.

### ITEM-0032 — Organização global da Barra de Menus
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir e implementar a política sistêmica de organização/ordenação global da Barra de Menus, cobrindo a ordenação global dos itens canônicos, a posição global de `[✥]` e o algoritmo futuro que preserve a ordem canônica independentemente da declaração local da tela. Origem documental: deferimento histórico em H-0054 §10.1; observação manual `O-H0063-MANUAL-002` classificada como `TRABALHO_FUTURO_DEFERIDO` após `VALIDACAO_MANUAL_APROVADA_FINAL` de H-0063. Este item não altera H-0063, não fecha o ITEM-0010 e não cobre ajuda por F1 (`ITEM-0029`) nem o mapa de teclas F (`ITEM-0031`).
**Pre-requisitos:** Contrato vigente de `barra_de_menus` (ordem canônica §7 e política de ordem por declaração §17); deferimento H-0054 §10.1; ciclo próprio de especificação/ADR antes de handoff.
**Proxima acao:** Realizar levantamento focal e especificação própria da política global, sem criar ADR nem implementar nesta etapa.
