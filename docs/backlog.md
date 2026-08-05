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

### ITEM-0020 — Chip de escolha entre execucao real e dry-run
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Padronizar genericamente a escolha entre execucao real e dry-run.
**Pre-requisitos:** Registrado pela ADR-0034 (D-SEL-24); `ITEM-0006` concluido em 2026-07-29. O `[Ins] Dry-Run` da ADR-0037 e especializacao focal do Handoff 4 e nao encerra este item.
**Proxima acao:** Realizar levantamento focal e criar ADR propria para a padronizacao universal do toggle de execucao real e dry-run.

### ITEM-0021 — Modos de visualizacao das telas de resultado
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Permitir telas de resultado somente verbosas, somente nao verbosas ou alternaveis, alem da politica `somente_verboso` fixada pela ADR-0034.
**Pre-requisitos:** Registrado pela ADR-0034 (D-SEL-24); `ITEM-0006` concluido em 2026-07-29.
**Proxima acao:** Realizar levantamento focal e criar ADR propria para as politicas e transicoes de modo das telas de resultado.

### ITEM-0007 — Conteudo multinivel colapsavel no console
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Implementar conteudo multinivel com nos expansiveis e recolhiveis no console.
**Pre-requisitos:** Definicao documental do conteudo colapsavel e da navegacao entre niveis.
**Proxima acao:** Realizar levantamento focal e criar ADR propria.

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
