# Relatório de Auditoria — H-0006 Handoff

## Status

AUDIT_APPROVED_WITH_NOTES

## Escopo auditado

Auditoria documental e técnica mínima do handoff:

```text
docs/handoff/H-0006-tela-minima-borda-fixa.md
```

O ciclo auditado foi exclusivamente:

```text
H-0006 — Tela mínima com borda fixa
```

Não houve implementação, correção de código, alteração do handoff, alteração
de contratos, alteração de ADRs, alteração de configuração nem execução de
ciclo de implementação.

## Arquivos lidos

Arquivos lidos conforme solicitação:

```text
docs/handoff/H-0006-tela-minima-borda-fixa.md
docs/contratos/contrato_processo_desenvolvimento.md
docs/handoff/H-0005-renderizador-estrutural-tela-raiz.md
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
config/telas/orquestrador.json
```

Arquivo extra lido:

```text
tela/modelo.py
```

Justificativa: o próprio pedido de auditoria exigia verificar a compatibilidade
do uso de `modelo.cabecalho` com a estrutura real atual em `tela/modelo.py`.
A consulta foi restrita à confirmação da definição de `ModeloTela`.

## Verificações realizadas

1. O handoff autoriza apenas o H-0006 e não antecipa H-0007, H-0008 ou H-0009.
2. O formato visual está especificado de modo exato e determinístico.
3. O expected output literal para `tela/teste_renderizador.py` está congelado.
4. A entrada principal permanece `renderizar_tela(modelo: ModeloTela) -> str`.
5. O renderer continua proibido de ler JSON bruto.
6. O renderer continua proibido de ler `config/estilo.json`.
7. O renderer não é orientado a ler `config/barra_de_menus.json`.
8. A borda fixa é apresentada como escopo limitado do H-0006, sem alternância
   ou estilo runtime.
9. `[Esc] Sair` e `[B] Borda` são especificados como texto inerte.
10. O handoff não cria alternância de bordas, estado ativo de borda ou
    persistência.
11. O handoff proíbe navegação, loop de aplicação, bindings, registry, filtros,
    paginação, seleção, pop-up e dashboard real.
12. O handoff não cria contrato, ADR, schema de dashboard ou dados reais de
    dashboard.
13. O handoff proíbe alteração em arquivos normativos.
14. As listas de arquivos permitidos e proibidos estão claras e exaustivas.
15. O relatório de implementação `docs/relatorios/IMP-0006-tela-minima-borda-fixa.md`
    está exigido.
16. Os comandos de verificação obrigatórios estão definidos.

## Achados

### Bloqueantes

Nenhum bloqueante identificado.

### Não bloqueantes

1. Há duas formulações residuais que falam em `modelo.cabecalho.titulo` e
   `modelo.cabecalho.descricao`, enquanto a estrutura real atual de
   `ModeloTela` define `cabecalho: dict`. O próprio handoff, nas regras
   normativas de campos derivados, usa corretamente
   `modelo.cabecalho.get("titulo", "(ausente)")` e
   `modelo.cabecalho.get("descricao", "(ausente)")[:39]`. A ressalva é
   textual, não bloqueante.
2. O handoff limita a borda fixa ao H-0006 por escopo e proibições, mas não
   usa literalmente a formulação "provisória" ou "estágio zero". Como
   `renderer visual final`, alternância, estilo runtime e leitura de
   `config/estilo.json` estão fora de escopo, não há risco operacional imediato.
3. O H-0006 autoriza atualizar `tela/teste_diagnostico.py` além do teste
   principal `tela/teste_renderizador.py`. A justificativa é adequada, pois
   preserva o diagnóstico executável após a troca do formato H-0005.

## Avaliação dos pontos críticos

### Testes H-0005 substituídos por H-0006

A substituição é aceitável. O handoff remove asserções do formato textual
H-0005, mas compensa com expected output literal H-0006, verificação de
determinismo, verificações de inércia e comandos obrigatórios para H-0001,
H-0002, `tela/teste_renderizador.py`, `tela/teste_diagnostico.py` e
`tela/diagnostico.py`.

Os invariantes relevantes permanecem exigidos:

- renderer continua recebendo `ModeloTela`;
- renderer não lê JSON bruto;
- diagnóstico continua executável;
- loader e modelo continuam testados separadamente;
- testes H-0001 e H-0002 continuam obrigatórios;
- saída continua determinística.

### Uso de modelo.cabecalho

Compatível com ressalva textual. Em `tela/modelo.py`, `ModeloTela.cabecalho`
é um `dict`. O renderer atual já usa `modelo.cabecalho.get(...)`, e o H-0006
também especifica essa forma nas regras normativas e no formato visual.

As menções a `modelo.cabecalho.titulo` e `modelo.cabecalho.descricao` devem
ser interpretadas como redação descritiva, não como API a implementar. Não é
necessário alterar `tela/modelo.py`.

### Largura fixa de 42 caracteres

A especificação é clara:

```text
TOTAL_WIDTH   = 42
INNER_WIDTH   = 40
CONTENT_WIDTH = 39
```

O expected output literal foi conferido linha a linha em contagem Python:
linhas visuais com borda têm 42 caracteres; linhas separadoras em branco têm
0 caracteres. A especificação não depende da largura real do terminal e
proíbe cálculo de largura de terminal.

### Hardcoded restrito ao estágio zero

O dashboard e o menu hardcoded estão limitados ao H-0006: dashboard real,
schema de dashboard, registry de dashboard, ações reais, bindings,
navegação, estado de borda, alternância de borda e renderer visual final
estão explicitamente fora de escopo.

A única ressalva é terminológica: o handoff não usa literalmente "estágio
zero", mas o conjunto de proibições impede que os hardcodeds sejam tratados
como regra arquitetural definitiva.

## Conclusão

O handoff H-0006 está suficientemente fechado, consistente e seguro para ser
entregue ao GLM/OpenCode para implementação estrita, desde que o executor siga
as regras normativas do próprio handoff e trate as menções a
`modelo.cabecalho.titulo`/`.descricao` como redação não normativa.

Não há necessidade de revisão arquitetural antes da implementação.

## Recomendação

Seguir para implementação estrita do H-0006 com atenção às ressalvas
não bloqueantes acima, especialmente ao uso de `modelo.cabecalho.get(...)` e
à preservação do escopo hardcoded apenas para este ciclo.
