---
name: relatorio-patch-aplicacao-adr-0049-p01
description: Registro do patch corretivo aplicado ao contrato de composição textual em resposta ao QA da aplicação da ADR-0049
metadata:
  type: relatorio
  item: ITEM-0027
  adr: ADR-0049
---

# Relatório — Patch de aplicação da ADR-0049 (P01)

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0049.md
  predecessor_imediato: docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0049.md
achados_tratados:
  - QA-APP-0049-01
  - QA-APP-0049-02
  - QA-APP-0049-03
```

## Delta material aplicado

Arquivo alterado: `docs/contratos/contrato_composicao_textual.md`.

- **§5 (Resultado):** removida a regra concreta que determinava produzir uma
  linha física vazia para texto vazio (tratamento concreto de entrada não
  autorizado pela ADR).
- **§6 (Regra de wrap):** removida a política normativa concreta de
  preservação de espaços/separadores (proibição explícita de condensar,
  remover, reordenar ou acrescentar). Substituída por registro de que
  peculiaridade histórica de espaços/separadores não é preservada
  automaticamente, só permanece mediante requisito semântico real do
  consumidor ou decisão posterior, e que o mecanismo canônico não infere essa
  política da implementação histórica.
- **§7 (Justificação de parágrafo):** removido o algoritmo concreto de
  distribuição do excesso ("tão uniforme quanto possível", resto
  determinístico a partir do primeiro vão, regra para ausência de vãos
  suficientes) e a regra específica de que a última linha nunca recebe
  expansão. Mantido apenas o requisito autorizado: justificação só ocorre sob
  solicitação explícita, o mecanismo canônico a produz distribuindo o excesso
  entre vãos internos, a forma algorítmica concreta (incluindo tratamento de
  ausência de vãos e da última linha) permanece indefinida até decisão
  própria, e justificação segue distinta de padding/alinhamento estrutural.
- **§11 (Erros e limites de entrada):** removida toda a política normativa
  concreta de validação/rejeição/erro para largura, texto, modo, ANSI e
  limites técnicos. Substituída por registro de que a implementação futura
  deve ser determinística no seu domínio válido e que validação, rejeição,
  exceção, fallback e tratamento de entrada inválida (incluindo texto vazio
  fora do domínio válido) pertencem à definição executiva posterior, quando
  dependerem da API concreta.
- **§12 (Critérios de aceite):** ajustado o critério de justificação para
  remover as referências a "resto determinístico", "última linha sem
  expansão" e "linha sem vãos válida", mantendo apenas distribuição do
  excesso entre vãos elegíveis sem alteração de padding estrutural.

## Requisitos indevidamente canonizados que foram removidos

- Algoritmo concreto de distribuição de excesso de justificação (uniformidade,
  resto a partir do primeiro vão, regra para ausência de vãos, regra de
  última linha).
- Política concreta de preservação/não alteração de espaços e separadores
  herdada dos helpers históricos.
- Política concreta de validação, rejeição, exceção, fallback e tratamento de
  entrada inválida (largura, texto, modo/alinhamento, ANSI malformado,
  limites técnicos, texto vazio).

## Confirmação de ausência de política substituta inventada

Nenhuma das remoções acima foi substituída por uma nova regra material
equivalente. Em cada ponto, o contrato passou a registrar apenas que a
decisão concreta correspondente ainda não existe e pertence a decisão própria
ou à definição executiva posterior — sem fixar algoritmo, exceção, valor de
fallback, default ou política alternativa de normalização.

## Verificações focais

Busca focal repetida após o patch:

```
rg -n -i 'uniform|uniforme|resto|primeiro vão|primeiro vao|última linha|ultima linha|espaços|espacos|separador|condens|remov|reorden|acrescent|inválid|invalid|rejeit|erro|exceç|excec|fallback|não positiv|nao positiv|não inteiro|nao inteiro|texto vazio|ANSI malform|limite técnico|limite tecnico' docs/contratos/contrato_composicao_textual.md
```

Ocorrências remanescentes revisadas semanticamente: todas correspondem a (a)
definições já autorizadas pela ADR (ex.: definição de "vão interno" em §3,
garantia geral de não perda/duplicação/condensação de conteúdo em §5) ou a
(b) frases que negam explicitamente a existência de política concreta (§6,
§7, §11) — nenhuma reintroduz prescrição normativa dos três achados.

`docs/contratos/contrato_composicao_textual.md` é arquivo ainda não
versionado (untracked) nesta árvore de trabalho, portanto `git diff`/`git
diff --check` contra `HEAD` não produzem saída para ele; o conteúdo pós-patch
foi conferido por leitura direta do arquivo.

## Bloqueios

Nenhum. Não foi necessário escolher política material nova para viabilizar
nenhuma das três remoções.
