---
name: REL-LEV-CLASSIFICACAO-PENDENCIAS-LEGADAS-BUILD-DOCS
description: Classificação factual das pendências legadas sem conclusão em docs/build_docs/to_do.md
metadata:
  type: relatorio_busca_levantamento_verificacao
  tipo_execucao: LEVANTAMENTO
  status: LEVANTAMENTO_CONCLUIDO
  data: 2026-07-27
rastreabilidade:
  etapa: LEVANTAMENTO_CLASSIFICACAO_PENDENCIAS_LEGADAS
  objeto: DOC-0018 DOC-0019 DOC-0022 DOC-B001 DOC-B002 DOC-B003 DOC-B004 DOC-B007 DOC-B008 DOC-B009
  autoridade_principal: null
  cadeia_raiz: null
  predecessor_imediato: null
---

# REL-LEV — Classificação de pendências legadas (build_docs)

> Relatório factual e autocontido.

```yaml
extensao_excepcional:
  motivo: dez itens independentes exigem evidências focais auditáveis
```

## 1. Pergunta e status

```yaml
tipo_execucao: LEVANTAMENTO
pergunta_factual: Qual o estado vigente de cada um dos 10 itens sem conclusão em docs/build_docs/to_do.md?
status_literal: LEVANTAMENTO_CONCLUIDO
```

## 2. Escopo fechado

```yaml
caminhos_consultados: [docs/build_docs/to_do.md, docs/backlog.md, docs/templates/TEMPLATE_RELATORIO_BUSCA_LEVANTAMENTO_VERIFICACAO.md, docs/INDICE.md, docs/adr/, docs/contratos/, docs/nomenclatura/, docs/handoff/, config/, tela/]
buscas_executadas:
  - comando_ou_padrao: rg -n -i -- '<termos/ids do item>'
    caminho: alvos autorizados do manifesto
    finalidade: evidência vigente por item
limites_aplicados: [sem docs/relatorios/** exceto este arquivo, sem outros build_docs/**, sem docs/arquivo/**, sem find/tree/rg na raiz]
```

## 3. Fatos confirmados — classificação por item

### DOC-0018 — ADR-0008 em cabecalho/estilo

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: ATIVO
destino_documental: docs/backlog.md
```

```yaml
arquivo: config/telas/demo/demo.json
linha_ou_trecho: "DOC-0018 — contrato_cabecalho.md e contrato_estilo.md nao revisados formalmente"
fato_comprovado: draft vigente declara DOC-0018 pendente.
```

```yaml
arquivo: docs/contratos/contrato_json_cabecalho.md
linha_ou_trecho: "quando a ADR-0008 for aplicada"
fato_comprovado: aplicação formal ao cabecalho permanece futura.
```

Justificativa: sem materialização formal; contratos não listam ADR-0008 em `adrs_aplicadas`.

### DOC-0019 — Revisar dashboard (ADR-0008)

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: CONCLUIDO_POSTERIORMENTE
destino_documental: docs/HISTORICO.md
```

```yaml
arquivo: docs/nomenclatura/34_DASHBOARD.md
linha_ou_trecho: "não navegável… não obrigatório… moldura própria… posicionamento… sem conteúdo universal fixo"
fato_comprovado: tipo mínimo do dashboard registrado na nomenclatura vigente.
```

```yaml
arquivo: docs/contratos/contrato_composicao_corpo.md
linha_ou_trecho: "antigo Info é o draft dessa instância"
fato_comprovado: Info legado tratado como draft da instância raiz.
```

Justificativa: resultado material de DOC-0019 entregue; alinhamento residual é DOC-B004.

### DOC-0022 — Atualizar INDICE.md (ADR-0008)

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: CONCLUIDO_POSTERIORMENTE
destino_documental: docs/HISTORICO.md
```

```yaml
arquivo: docs/INDICE.md
linha_ou_trecho: "Modelo em migração pela ADR-0008… config/telas/<id>.json"
fato_comprovado: Config descreve modelo por tela, não JSON-por-domínio antigo.
```

Justificativa: estrutura e regra de Config já refletem ADR-0008/0021/0022.

### DOC-B001 — Ajuste do `tx`

```yaml
resultado_da_verificacao: NAO_CONFIRMADO
classificacao: null
destino_documental: NENHUM_ATE_DECISAO
```

Divergência: `32_CONSOLE.md` (“Pendência `tx`… sem decisão vigente”) × `contrato_console.md`/ADR-0028 (truncamento/`...`).

### DOC-B002 — `popup_execucao`

```yaml
resultado_da_verificacao: NAO_CONFIRMADO
classificacao: null
destino_documental: NENHUM_ATE_DECISAO
```

Só “fora de escopo” em ADR-0006/0007 apontando `NOMENCLATURA.md` §11 ausente; sem cancelamento, entrega ou backlog.

### DOC-B003 — Segunda pauta de estilo

```yaml
resultado_da_verificacao: NAO_CONFIRMADO
classificacao: null
destino_documental: NENHUM_ATE_DECISAO
```

Nenhum termo vigente nos alvos descreve a pauta; sem cancelamento explícito.

### DOC-B004 — Corpo × dashboard / alinhamento

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: ATIVO
destino_documental: docs/backlog.md
```

```yaml
arquivo: docs/nomenclatura/34_DASHBOARD.md
linha_ou_trecho: "Alinhamento (pendência)… lancador… ou mantém centralização"
fato_comprovado: alinhamento horizontal do dashboard pendente.
```

```yaml
arquivo: docs/contratos/contrato_json_dashboard.md
linha_ou_trecho: "Pendência de alinhamento horizontal… tarefa futura"
fato_comprovado: contrato JSON vigente preserva a pendência.
```

Justificativa: parte (a) sem decisão material; compatível com autoridades.

### DOC-B007 — Arquivar históricos/transicionais

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: ATIVO
destino_documental: docs/backlog.md
```

```yaml
arquivo: docs/adr/ADR-0008-modelo-configuracao-por-tela.md
linha_ou_trecho: "Artefatos históricos/transicionais devem ser arquivados no fechamento da Fase 0"
fato_comprovado: obrigação normativa de arquivamento permanece.
```

```yaml
arquivo: config/layouts/layout_dado.json
linha_ou_trecho: presente (e layout_menu.json); INDICE marca obsoleto/transicional
fato_comprovado: arquivamento físico não materializado.
```

Justificativa: necessidade vigente sem arquivamento executado.

### DOC-B008 — Itens internos de console

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: ATIVO
destino_documental: docs/backlog.md
```

```yaml
arquivo: docs/contratos/contrato_console.md
linha_ou_trecho: "Contratos específicos dos tipos internos de item (DOC-B008)"
fato_comprovado: contrato vigente declara DOC-B008 pendente.
```

```yaml
arquivo: config/telas/demo/demo.json
linha_ou_trecho: "DOC-B008 — tipos internos de item de console nao definidos"
fato_comprovado: draft vigente preserva a pendência.
```

Justificativa: necessidade explícita sem contratos dos tipos internos.

### DOC-B009 — Registry de tipos válidos

```yaml
resultado_da_verificacao: CONFIRMADO
classificacao: ATIVO
destino_documental: docs/backlog.md
```

```yaml
arquivo: docs/contratos/contrato_console.md
linha_ou_trecho: "Registry completo de ações (DOC-B009)"
fato_comprovado: registry formal permanece pendente.
```

```yaml
arquivo: docs/backlog.md
linha_ou_trecho: "Realizar levantamento focal de DOC-B009"
fato_comprovado: ITEM-0004 trata DOC-B009 como predecessora aberta, não duplicata concluída.
```

Justificativa: registry não fechado; ITEM-0004 depende dele.

## 4. Não confirmados

```yaml
nao_confirmados:
  - id: DOC-B001
    afirmacao: regras de tx decididas ou abertas
    evidencia_ausente_ou_insuficiente: divergência nomenclatura × contrato_console/ADR-0028
  - id: DOC-B002
    afirmacao: popup_execucao segue necessário
    evidencia_ausente_ou_insuficiente: sem definição vigente, cancelamento ou entrega
  - id: DOC-B003
    afirmacao: segunda pauta de estilo segue necessária
    evidencia_ausente_ou_insuficiente: objeto ausente nos alvos autorizados
```

## 5. Achados e bloqueios

```yaml
achados:
  - id: A1
    fato: 7 classificações confirmadas; 3 NAO_CONFIRMADO
    evidencia_focal: seções por item
  - id: A2
    fato: nenhuma classificação usou só o status legado de to_do.md
    evidencia_focal: cada CONFIRMADO cita artefato vigente fora de build_docs
bloqueios: []
```

## 6. Quadro final

| Classificação | Qtd | Itens |
|---|---:|---|
| ATIVO | 5 | DOC-0018, DOC-B004, DOC-B007, DOC-B008, DOC-B009 |
| CONCLUIDO_POSTERIORMENTE | 2 | DOC-0019, DOC-0022 |
| SUBSTITUIDO | 0 | — |
| INCOMPATIVEL | 0 | — |
| CANCELADO | 0 | — |
| DUPLICADO | 0 | — |
| NAO_CONFIRMADO (`null`) | 3 | DOC-B001, DOC-B002, DOC-B003 |

```yaml
itens_verificados: 10
```
