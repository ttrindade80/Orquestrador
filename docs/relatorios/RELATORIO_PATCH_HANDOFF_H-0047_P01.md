---
name: relatorio-patch-handoff-h0047-p01
description: "Relatorio do patch P01 sobre H-0047, tratando os quatro achados materiais do QA (ciclo, proprietario nominal, importacao inversa, default de TelaIdIncorreto)"
metadata:
  type: relatorio
  handoff: H-0047
  patch: P01
---

# Relatório do patch P01 — H-0047

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0047
  origem:
    - docs/relatorios/RELATORIO_QA_HANDOFF_H-0047.md
  patch: P01

execucao:
  status: aplicado
  arquivos_alterados:
    - docs/handoff/H-0047-modularizacao-estrutural-do-loader.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0047_P01.md

resultado:
  achados_tratados:
    - H0047-QA-001
    - H0047-QA-002
    - H0047-QA-003
    - H0047-QA-004
  alteracoes_realizadas: []
  desvios: []
  bloqueios: []
```

## Correções realizadas

**H0047-QA-001** (comando 2, §7): o detector de ciclos agora constrói o
conjunto completo dos módulos reais do pacote (`set(grafo)`, dos `.py`
existentes em `tela/carregamento/`) e valida, antes do DFS, que toda aresta
aponta para um módulo desse conjunto — falha informa origem, destino ausente
e a aresta completa. Verificação sintética com `grafo_sintetico` (aresta
para `tela.carregamento.inexistente`) comprova a rejeição; política de
imports relativos/`from tela.carregamento import modulo` inalterada.

**H0047-QA-002** (comando 7, §7, e §4.2): prova amostral substituída por
mapa fechado `proprietario_esperado` com os 96 símbolos nominais de nível
superior da seção 4.2 (sem reticências ou grupos abreviados). §4.2 de
`validacao_matricial.py` passou a listar nominalmente as 11 constantes
`_DM_*`, antes abreviadas como "até". A prova indexa por AST as
definições/atribuições de nível superior de cada módulo previsto, exige
exatamente um proprietário por símbolo igual ao de 4.2, e falha em
duplicação ou símbolo fora do fechamento. Identidade das 24 reexportações
da fachada (comando 6) permanece separada e inalterada.

**H0047-QA-003** (comando 3, §7, e §5.3): adicionado detector AST normativo
de importação inversa da fachada (`tela.loader`), cobrindo formas estáticas
(`import tela.loader[.x][ as alias]`, `from tela.loader import x`, `from
tela import loader[ as alias]`, cadeia `tela.loader` via `import tela`) e
dinâmicas literais (`importlib.import_module`, `__import__`). O `rg`
original virou evidência auxiliar em ambas as seções, eliminando a
definição concorrente do critério; carregamento dinâmico da fachada foi
declarado proibido. Verificações sintéticas de rejeição, aceitação de
stdlib/imports internos e ausência de falso positivo foram incluídas.

**H0047-QA-004** (§4.2, §4.3, comando 9 em §7): fechada a relação entre
`_ID_TELA_RAIZ` (proprietário único `tela_json.py`) e o default do parâmetro
`esperado` de `TelaIdIncorreto` (`erros.py`), que passa a usar o literal
`"orquestrador"` em vez de referenciar `_ID_TELA_RAIZ` — preserva `erros.py`
sem dependências internas e a assinatura/mensagem atuais
(`tela/loader.py:112-122`). Prova reproduzível (comando 9) confirma
identidade, default e mensagem; §5.1 registra que `_ID_TELA_RAIZ` não é
reexportado pela fachada.

## Verificação interna

Os quatro achados foram corrigidos exclusivamente no H-0047; nenhuma
correção exige código (`tela/loader.py` permaneceu leitura focal). Os
blocos Python inseridos/alterados foram validados por `ast.parse`; os
comandos 2 e 3 (com autoteste sintético) foram executados contra o
repositório real e capturaram corretamente as falhas simuladas. O mapa do
comando 7 foi executado isoladamente e confirmado com 96 símbolos sem
duplicatas, coincidindo com §4.2. Tabela de critérios (§10, linhas 8–11)
atualizada. Frontmatter permanece `status: criado`; nenhuma arquitetura,
manifesto ou regra funcional foi alterada; apenas os dois arquivos
autorizados foram escritos.
