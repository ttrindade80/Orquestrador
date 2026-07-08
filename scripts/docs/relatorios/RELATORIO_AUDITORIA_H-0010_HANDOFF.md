# Relatório de Auditoria — H-0010 Lançador visual inerte

## Status final

ARCHITECTURE_REVIEW_REQUIRED

## Escopo auditado

Foi auditado o handoff `docs/handoff/H-0010-lancador-visual-inerte.md`, limitado ao ciclo H-0010 — Lançador visual inerte.

O objetivo declarado do ciclo futuro é fazer a demo mostrar um bloco visual mínimo de `lancador`, com itens simples, sem chamar nenhuma tela e sem ativar navegação real.

Esta auditoria não implementou código e não alterou contratos, ADRs, NOMENCLATURA, índice, backlog, issues, config, testes ou arquivos de produção.

## Arquivos lidos

- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/handoff/H-0010-lancador-visual-inerte.md`
- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0009_HANDOFF.md`
- `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md`
- `docs/relatorios/RELATORIO_QA_H-0009_LAYOUT_TERMINAL_ENTRADA_SEM_ECHO.md`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`

Nenhum contrato adicional, ADR, `NOMENCLATURA.md`, `docs/INDICE.md`, backlog ou issues foi lido.

## Verificações executadas

Comandos Git executados antes da criação deste relatório:

```text
git status --short
?? docs/handoff/H-0010-lancador-visual-inerte.md

git diff --stat
(sem saída)

git diff --name-only
(sem saída)
```

Interpretação: antes da auditoria, apenas o handoff H-0010 estava criado como arquivo não rastreado. Não havia diff em arquivos rastreados.

## Aderência ao contrato de processo

O contrato de processo exige contrato aplicável, handoff fechado, critérios verificáveis e limites claros de arquivos permitidos/proibidos.

O H-0010 tem bons limites operacionais e critérios testáveis, mas não está fechado do ponto de vista da ordem de autoridade: o handoff autoriza comportamento que contraria regras ativas dos contratos-alvo. Como o contrato de processo determina que artefatos superiores prevalecem sobre handoffs, a implementação não deve seguir uma exceção arquitetural criada apenas no handoff.

## Aderência ao contrato de composição de corpo

O H-0010 acerta ao afirmar que `lancador` é elemento do corpo e ao separá-lo da `barra_de_menus`.

Achado bloqueante: o contrato de composição determina que toda propriedade concreta de composição do corpo é declarada no `tela.json`, que o renderer recebe a declaração validada e que o código não decide composição hardcoded. O H-0010, por sua vez, autoriza itens hardcoded, título hardcoded e não leitura dos itens declarados no JSON.

Evidências:

- H-0010 autoriza `_ITENS_LANCADOR` hardcoded e título `"Navegar"` hardcoded.
- `contrato_composicao_corpo.md` define declaração exclusiva no `tela.json` e proíbe composição/lista de itens hardcoded.
- `config/telas/orquestrador.json` contém `lancador_principal.itens: []`, com pendência explícita de definição dos itens.

## Aderência ao contrato do lançador

O H-0010 cobre pontos importantes do contrato do lançador:

- exige título próprio do bloco;
- exige itens com chip e texto;
- preserva limite de texto de 15 caracteres;
- exige rejeição por teste para texto acima de 15 caracteres, sem truncamento;
- proíbe setas, `[✥]`, cursor de lançador, registry, bindings e execução de ação.

Achado bloqueante: o contrato do lançador define que conteúdo concreto, itens, textos, chips, destinos e regras visuais da instância vêm do `tela.json`; também determina que o renderer não decide itens, textos, chips, destinos nem regras visuais. O H-0010 autoriza exatamente esses dados como constantes no código.

Achado bloqueante adicional: o contrato do lançador define `tela_destino` como identificador formal usado pelo sistema de navegação e diz que a tela referenciada deve existir; o H-0010 define `tela_destino` como dado declarativo inativo, nunca validado, resolvido ou acionado. Essa pode ser uma exceção transitória útil para uma demo visual, mas precisa ser autorizada por decisão arquitetural superior ao handoff.

## Preservação do H-0009

O H-0010 preserva explicitamente os comportamentos aprovados em H-0009:

- `b` alternando borda;
- Esc saindo sem Enter/echo em TTY;
- `s` como atalho auxiliar;
- largura dinâmica na demo;
- fallback determinístico de 42 no diagnóstico;
- saída por pipe determinística;
- ausência de linhas em branco entre caixas/regiões visuais;
- diagnóstico não interativo.

Não foi encontrado conflito direto com o H-0009.

## Arquivos permitidos e proibidos

A lista de arquivos permitidos é restrita e adequada ao escopo operacional:

- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `docs/relatorios/IMP-0010-lancador-visual-inerte.md`

O handoff proíbe alteração de `docs/contratos/`, `docs/adr/`, `docs/NOMENCLATURA.md`, `docs/INDICE.md`, `config/`, `docs/backlog.md` e `docs/issues.md`, como esperado.

A ressalva sobre `tela/demo.py` está suficientemente operacional: o handoff informa que provavelmente não exige alteração lógica e manda justificar antes de alterar.

## Critérios de aceite

Os critérios são testáveis item a item quanto à saída visual, largura, ausência de `tela_destino` na saída, preservação de H-0009, ausência de `"\n\n"` e execução das suítes.

Há uma lacuna de autoridade, não de testabilidade: os critérios testam uma implementação que viola ou excepciona regras contratuais ativas sobre origem dos dados do `lancador`.

## Riscos encontrados

1. Itens hardcoded placeholder estão explicitamente limitados ao ciclo visual inerte, mas ainda criam uma fonte concreta de itens fora do `tela.json`, em conflito com os contratos ativos.
2. `tela_destino` nos dicts está bem marcado como preservado/inativo no H-0010, mas essa semântica contraria o contrato do lançador sem decisão superior.
3. A expressão "menu" aparece como referência ao placeholder existente `"Menu"`; o handoff também explica que ele representa a `barra_de_menus`, reduzindo a ambiguidade terminológica. Não é o risco principal.
4. A nota sobre `demo.py` não bloqueia: o handoff delimita quando ela pode ser alterada.
5. As constantes `label_max=38`, `dashes=31` para `"Navegar"` são justificadas pelo estado real do renderer H-0009.
6. Os arquivos permitidos são restritos, mas insuficientes para resolver a divergência arquitetural, porque uma autorização válida exigiria artefato normativo ou decisão superior, que o próprio handoff proíbe alterar.
7. Os critérios de aceite são verificáveis, mas verificam uma exceção contratual não autorizada.

## Achados bloqueantes

1. O H-0010 autoriza dados concretos de `lancador` hardcoded no renderer (`_ITENS_LANCADOR`, chip, texto, `tela_destino` e título), contrariando os contratos ativos que exigem origem no `tela.json` e proíbem hardcoding pelo renderer.
2. O H-0010 redefine `tela_destino` como campo declarativo inativo e nunca validado neste ciclo, contrariando o contrato do lançador, que define `tela_destino` como referência formal à tela a abrir e exige existência validável.

## Achados não bloqueantes

1. O posicionamento "entre dashboard e menu" poderia usar consistentemente o termo `barra_de_menus`, mas o próprio handoff esclarece que a caixa `"Menu"` representa a `barra_de_menus`. Não é bloqueante.
2. O H-0010 mantém `docs/handoff/` como proibido para o executor, incluindo o próprio handoff. Isso é adequado para implementação futura, embora a correção do handoff rejeitado exija um ciclo de engenharia separado.
3. A ausência de leitura de `config/lancador.json` é coerente com o objetivo de não avançar para o compositor real, mas reforça que o ciclo é uma exceção visual transitória e precisa de autorização arquitetural.

## Conclusão

O handoff H-0010 não deve ser liberado para implementação estrita no estado atual.

Embora o escopo visual inerte esteja claro, os arquivos estejam bem delimitados e os critérios sejam testáveis, o handoff cria uma exceção arquitetural ao contrato de composição de corpo e ao contrato do lançador: itens, título, chip, texto e destino passam a existir no código como placeholders, enquanto os contratos ativos exigem declaração no `tela.json` e execução da instância validada.

Status final: `ARCHITECTURE_REVIEW_REQUIRED`.

