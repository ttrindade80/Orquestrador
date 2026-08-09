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

### ITEM-0007 — Navegacao multinivel do console
**Tipo:** implementacao
**Prioridade:** media
**Status:** em_andamento
**Descricao:** Implementar as politicas de navegacao multinivel do console com foco estrito em cursor, percurso e semantica de Espaco: preservar `nivel_unico`; manter `tabela` nao navegavel; implementar `arvore_colapsavel`; implementar `selecao_multinivel` com uma unica navegacao reunindo todos os niveis e selecao recursiva dos descendentes; implementar `dois_niveis_por_foco` com toroide dos pais e toroide proprio de filhos por pai, usando a apresentacao de selecao ja existente. O ciclo deve ser decomposto em quatro handoffs sequenciais e nao pode reaproveitar a tentativa defeituosa preservada em branch de erro.
**Estado dos handoffs:** H-0052: concluido; H-0053: concluido; H-0054: futuro; H-0055: futuro.
**Pre-requisitos:** Ciclo universal de paginacao por `PageUp`/`PageDown` e chips `[PgUp]`/`[PgDn]` concluido pela ADR-0041 e pelo H-0051, com QA tecnico e validacao manual aprovados. ADR-0042 aceita (`ADR-0042_ACEITA`) e aplicada (`APLICACAO_DOCUMENTAL: CONCLUIDA`), QA da aplicacao aprovado (`QA_DA_APLICACAO: ADR_APPLICATION_APPROVED`), H-0052 concluido com QA resolvido por validacao manual (`IMPLEMENTACAO: IMPLEMENTED`, `VALIDACAO_MANUAL: MANUAL_VALIDATION_APPROVED`). ADR-0043 aceita e aplicada, com QA da aplicacao aprovado (`QA_APLICACAO: ADR_APPLICATION_APPROVED`). H-0053 concluido com QA do handoff, QA da implementacao, QA da alteracao declarativa e validacao manual aprovados. H-0054 (`selecao_multinivel`) e H-0055 (`dois_niveis_por_foco`) permanecem futuros. A integracao conjunta de arvore, multiline e paginacao sera atribuida a item futuro proprio.
**Proxima acao:** Verificar a especificacao e iniciar, em ciclo proprio, a integracao futura de `arvore_colapsavel` com multiline e paginacao. Nao iniciar H-0054 ou H-0055 nesta etapa; nao reabrir apresentacao de filho ativo, distribuicao geometrica de grupos, Enter, execucao, confirmacao ou persistencia neste item.

### ITEM-0025 — Integração de arvore_colapsavel com multiline e paginação
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** BACKLOG / FUTURO. Validar `arvore_colapsavel` com conteúdo multilinha e paginação real, incluindo PageUp/PageDown vigentes, mudança de página, projeção visível por página, cursor válido antes/depois da mudança de página, expansão/recolhimento com recomputação da projeção, alteração do número/distribuição de páginas causada pelo estado da árvore, renderer e mapa físico usando a mesma projeção e demonstração TTY focal.
**Pre-requisitos:** ITEM-0007 concluído; ciclo próprio de especificação e validação. Exclui nova política universal de paginação, H-0054, H-0055, nova geometria geral multinível, seleção, Enter e execução.
**Proxima acao:** Criar especificação própria e planejar o ciclo sem criar ADR ou handoff nesta etapa.

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

### ITEM-0010 — Tela de escolha do estilo global
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Implementar uma tela para visualizar, escolher, pre-visualizar, persistir e restaurar presets do estilo global.
**Pre-requisitos:** Carregamento global e materializacao do estilo concluidos pelo H-0039.
**Proxima acao:** Realizar levantamento focal da interacao e criar ADR propria.

### ITEM-0012 — Tiling de elementos ou conteudo
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir e implementar a finalidade e o comportamento do atributo `tiling`.
**Pre-requisitos:** Decisao sobre escopo, consumidores e interacao com as regras de distribuicao existentes.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural.

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

### ITEM-0017 — Avaliar a necessidade de popup_execucao
**Tipo:** documentacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Determinar se `popup_execucao` ainda representa uma necessidade do sistema.
**Pre-requisitos:** Caso real de uso ou decisão explícita sobre sua necessidade.
**Proxima acao:** Apresentar a questão ao usuário em ciclo focal de especificação.
