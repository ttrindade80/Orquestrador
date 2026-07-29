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

### ITEM-0003 — Paginacao interativa do console
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Implementar paginacao interativa do console em ciclo separado da navegacao simples.
**Pre-requisitos:** Navegacao simples e modelo de cursor do console formalizados.
**Proxima acao:** Realizar levantamento focal e criar ADR propria para paginacao.

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

### ITEM-0006 — Selecao multipla no console
**Tipo:** implementacao
**Prioridade:** media
**Status:** em_andamento
**Descricao:** Implementar selecao multipla e fluxo focal de processamento conforme ADR-0034: estado da selecao por conjunto de IDs estaveis, protocolo provisorio de execucao com resultado estruturado, tela padrao de resultado reutilizavel e fluxo focal de abertura/retorno, decompostos em quatro handoffs sequenciais (H1-H4).
**Pre-requisitos:** ADR-0034 aceita e aplicada; Handoff 1 (H-0041) implementado, QA tecnico aprovado e validacao manual TTY aprovada; navegacao simples e selecao unica concluidas (ADR-0031).
**Proxima acao:** Criar o Handoff 2 da ADR-0034, restrito ao protocolo focal do binding e execucao: dry-run, execucao real reversivel, resultado estruturado e restauracao protegida; Enter/Executar permanece inativo na interface.

### ITEM-0018 — Selecionar todos apenas na pagina atual
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Permitir limitar a selecao em massa (`Todos`) aos itens selecionaveis da pagina corrente do console, em vez do conjunto filtrado completo em todas as paginas.
**Pre-requisitos:** Registrado como item bloqueado pela ADR-0034 (D-SEL-24); depende da implementacao do ITEM-0006 e da paginacao interativa do ITEM-0003.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural propria quando o ITEM-0003 e o ITEM-0006 estiverem concluidos.

### ITEM-0019 — Selecao compartilhada entre consoles compativeis
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Permitir um conjunto de selecao comum entre consoles que exibam dados compativeis.
**Pre-requisitos:** Registrado como item bloqueado pela ADR-0034 (D-SEL-24); depende da implementacao do ITEM-0006.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural propria.

### ITEM-0020 — Chip de escolha entre execucao real e dry-run
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Permitir escolher na interface o modo (execucao real ou dry-run) da operacao vinculada ao lote selecionado.
**Pre-requisitos:** Registrado como item bloqueado pela ADR-0034 (D-SEL-24); depende da implementacao do ITEM-0006.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural propria.

### ITEM-0021 — Modos de visualizacao das telas de resultado
**Tipo:** implementacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Permitir telas de resultado somente verbosas, somente nao verbosas ou alternaveis, alem da politica `somente_verboso` fixada pela ADR-0034.
**Pre-requisitos:** Registrado como item bloqueado pela ADR-0034 (D-SEL-24); depende da implementacao do ITEM-0006.
**Proxima acao:** Realizar levantamento focal e decisao arquitetural propria.

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

### ITEM-0011 — Cores de estado inativo e de alerta
**Tipo:** implementacao
**Prioridade:** media
**Status:** planejado
**Descricao:** Definir e implementar a semantica de `cor_inativo` e `cor_alerta`, incluindo sua traducao para o terminal.
**Pre-requisitos:** Decisao contratual sobre significado, consumidores e representacao terminal.
**Proxima acao:** Realizar decisao focal e criar ADR propria.

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

### ITEM-0015 — Aplicar ADR-0008 aos contratos de cabeçalho e estilo
**Tipo:** documentacao
**Prioridade:** media
**Status:** bloqueado
**Descricao:** Verificar e materializar a aplicação documental remanescente da ADR-0008 nos contratos de cabeçalho e estilo.
**Pre-requisitos:** Levantamento focal das alterações ainda ausentes e delimitação da aplicação necessária.
**Proxima acao:** Verificar os contratos vigentes e definir o ciclo documental aplicável.

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
