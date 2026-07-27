---
name: backlog-orquestrador
description: Modelo neutro para registrar trabalho planejado
metadata:
  type: backlog
  scope: orquestrador
---

# Backlog — Modelo

## Regra

Este arquivo deve conter somente itens planejados ainda nao iniciados. Ele nao
e contrato, nao e autorizacao de implementacao e nao substitui handoff.

Ao copiar este padrao para um projeto novo, manter apenas exemplos ou limpar
esta lista.

## Formato

```markdown
### ITEM-NNNN — [Titulo curto]
**Tipo:** contrato | implementacao | qa | documentacao | infraestrutura
**Prioridade:** alta | media | baixa
**Status:** planejado | bloqueado | pronto_para_handoff
**Descricao:** [O que precisa existir]
**Pre-requisitos:** [Contratos, ADRs ou decisoes necessarias]
**Proxima acao:** [A menor acao documental verificavel]
```

## Exemplos

### ITEM-0000 — Criar contrato do modulo exemplo
**Tipo:** contrato
**Prioridade:** media
**Status:** planejado
**Descricao:** Especificar entradas, saidas, estados e erros do `modulo_exemplo`.
**Pre-requisitos:** Nenhum.
**Proxima acao:** Escrever `docs/contratos/contrato_modulo_exemplo.md` a partir do template acordado.

### ITEM-0001 — Preparar handoff de implementacao exemplo
**Tipo:** implementacao
**Prioridade:** baixa
**Status:** bloqueado
**Descricao:** Gerar handoff para implementar comportamento ja contratado.
**Pre-requisitos:** Contrato do modulo aprovado.
**Proxima acao:** Criar `H-0001-descricao-curta.md`.

## Itens planejados

> A ordem dos itens deste backlog nao representa prioridade nem sequencia de execucao. Cada item somente podera avancar pelo fluxo documental aplicavel.

### ITEM-0002 — Navegacao simples e selecao unica em console
**Tipo:** implementacao
**Prioridade:** media
**Status:** implementado; aguardando fechamento Git
**Descricao:** Implementar foco entre consoles focalizaveis, navegacao simples entre itens de nivel unico e selecao unica do item atual. Estado factual do ciclo: implementacao e validacao manual concluidas; aguarda QA pos-patch da consistencia documental e, apos aprovacao, fechamento Git manual. (Descricao factual do item; a taxonomia global do backlog permanece `planejado | bloqueado | pronto_para_handoff`.)
**Pre-requisitos:** ADR-0031 aceita; aplicacao documental aprovada com notas apos patch.
**ADR:** ADR-0031 (aceita)
**Aplicacao_documental:** CONCLUIDA
**QA_da_aplicacao:** APROVADA_COM_NOTAS_POS_PATCH
**Handoff:** H-0040 (criado: true; aprovado: true)
**Implementacao:** CONCLUIDA
**QA_da_implementacao:** I1_IMPLEMENTATION_APPROVED
**Validacao_manual:** MANUAL_VALIDATION_APPROVED
**Consistencia_documental:** PATCH_EM_QA_APOS_ESTA_CORRECAO
**Commit:** NAO_EXECUTADO
**Proxima acao:** QA pós-patch da consistência documental do ciclo ADR-0031/H-0040; após aprovação, fechamento Git manual.

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
**Proxima acao:** Realizar levantamento focal de `DOC-B009` e criar ADR especializada.

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
**Status:** planejado
**Descricao:** Implementar inclusao e retirada de multiplos itens e execucao de operacoes sobre o conjunto selecionado.
**Pre-requisitos:** Navegacao simples e selecao unica concluidas; acoes declarativas formalizadas quando necessarias.
**Proxima acao:** Criar ciclo documental proprio para selecao multipla.

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
