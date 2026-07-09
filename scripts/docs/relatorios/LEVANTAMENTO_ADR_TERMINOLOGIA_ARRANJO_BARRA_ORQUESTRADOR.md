# Levantamento — ADR de terminologia de arranjo e barra_de_menus do Orquestrador

## Status

LEVANTAMENTO_CONCLUIDO

## Escopo

Este relatório apenas pesquisa evidências. Não altera código, JSON, contratos, ADRs ou handoffs.

Observação operacional: o pedido inicial proibia alterações, mas a seção "Relatório a criar" determinou a criação deste arquivo único. Nenhum outro arquivo foi alterado intencionalmente.

## Estado inicial

Comandos iniciais executados:

```text
pwd
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts

git status --short
(sem saída)

git log --oneline -8
ab48702 feat: adiciona acesso demonstravel ao grupo minimo
0bcb477 feat: implementa grupo estrutural minimo em tela isolada
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
57f36d2 feat: ajusta layout terminal e entrada sem echo
```

Arquivos centrais consultados:

- `config/telas/orquestrador.json`
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/modelo.py`
- `tela/loader.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `docs/NOMENCLATURA.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/handoff/H-0010A-fluxo-minimo-lancador-tela-destino.md`
- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`
- `docs/relatorios/IMP-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/RELATORIO_QA_H-0012_GRUPO_ESTRUTURAL_MINIMO_TELA_ISOLADA.md`
- `docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md`
- `docs/relatorios/RELATORIO_QA_H-0013_DEMO_ACESSO_TELA_GRUPO_MINIMO.md`

## 1. Terminologia atual de arranjo

### 1.1 Ocorrências de `lado_a_lado`

Categorias encontradas:

- ADR: `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md` ainda usa `lado_a_lado` como nome do arranjo horizontal planejado e como alvo de correção do H-0011.
- Contratos: `docs/contratos/contrato_composicao_corpo.md:136`, `docs/contratos/contrato_json_tela_minima.md:148` e `docs/NOMENCLATURA.md:131` listam `lado_a_lado` como valor válido/esperado junto de `sobreposto`.
- Handoff: `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md` é histórico/cancelado pelo ciclo posterior, mas contém a especificação mais extensa do termo; `docs/handoff/H-0012...` e `H-0013...` proíbem implementar `lado_a_lado` no escopo desses ciclos.
- Relatórios: vários relatórios de auditoria e implementação registram a passagem histórica H-0011/H-0012.
- Código: `tela/loader.py:150-158` rejeita explicitamente grupo estrutural com `arranjo == "lado_a_lado"`.
- Testes: `tela/teste_loader.py:628-633` testa rejeição de grupo com `arranjo="lado_a_lado"`.
- JSON de produção: não há `lado_a_lado` ativo nos JSONs de produção em `config/telas/*.json`.

Classificação:

- É valor ativo de JSON? Não.
- É valor aceito pelo loader? Parcialmente. No `corpo.arranjo` principal, o loader preserva qualquer string sem validar vocabulário. Em grupo estrutural, `lado_a_lado` é rejeitado.
- É valor testado? Sim, como caso inválido para grupo.
- É só documentação histórica? Não totalmente; ainda aparece em contratos ativos como valor permitido, embora sem JSON ativo.
- Aparece em contrato ativo? Sim.
- Aparece em ADR aceita? Sim, ADR-0010.

### 1.2 Ocorrências de `sobreposto`

Categorias encontradas:

- JSON de produção: `config/telas/orquestrador.json:24`, `config/telas/destino_minimo.json:9`, `config/telas/stub_b.json:9`, `config/telas/grupo_minimo.json:9` e `config/telas/grupo_minimo.json:14`.
- Contratos: `docs/contratos/contrato_composicao_corpo.md:136`, `docs/contratos/contrato_json_tela_minima.md:109` e `docs/contratos/contrato_json_tela_minima.md:148`.
- Nomenclatura: `docs/NOMENCLATURA.md:131`, `docs/NOMENCLATURA.md:283`, `docs/NOMENCLATURA.md:874-879`.
- Código: não há lógica de renderização condicionada por `sobreposto`; o valor é preservado por `loader.py` e `modelo.py`.
- Testes: `tela/teste_loader.py:168-170`, `tela/teste_modelo.py:119-120`, `tela/teste_renderizador.py:535` e outros casos fabricados usam `sobreposto`.
- Handoffs/relatórios: recorrente como valor padrão histórico de telas mínimas.

Classificação:

- É valor ativo de JSON? Sim.
- É valor aceito pelo loader? Sim, por preservação inerte.
- É valor testado? Sim.
- É só documentação histórica? Não; é o valor ativo atual dos JSONs de tela.
- Aparece em contrato ativo? Sim.
- Aparece em ADR aceita? Indiretamente via ADR-0010 e documentação aplicada.

### 1.3 Ocorrências de `empilhado`

Categorias encontradas:

- Handoff/relatório histórico: aparece em `docs/handoff/H-0011-renderizacao-lado-a-lado-barra-minima-orquestrador.md` e `docs/relatorios/RELATORIO_AUDITORIA_H-0011_HANDOFF.md`, descrevendo o comportamento visual empilhado.
- Código: não encontrado como valor de `arranjo` nem como branch funcional.
- Testes: não encontrado como valor testado.
- JSON de produção: não encontrado.
- Contratos ativos: não encontrado como valor formal de `arranjo`.

Classificação:

- É valor ativo de JSON? Não.
- É valor aceito pelo loader? Seria preservado se usado no `corpo.arranjo` principal, porque não há validação de vocabulário, mas não é valor contratual.
- É valor testado? Não.
- É só documentação histórica? Sim, no estado atual.
- Aparece em contrato ativo? Não como valor formal.
- Aparece em ADR aceita? Não como decisão final.

### 1.4 Ocorrências de `horizontal`

Categorias encontradas:

- JSON de produção: `barra_de_menus.distribuicao = "horizontal"` em `config/telas/orquestrador.json:126`, `config/telas/destino_minimo.json:27`, `config/telas/grupo_minimo.json:34` e `config/telas/stub_b.json:27`; também aparece em descrições de `config/lancador.json` e layouts.
- JSON de produção transicional: `posicao_dashboard` admite/usa `horizontal` em contratos e aparece como eixo descontinuado; o Orquestrador usa `posicao_dashboard = "vertical"` hoje.
- Contratos: `docs/contratos/contrato_composicao_corpo.md:157` lista `horizontal|vertical` apenas para `posicao_dashboard` descontinuado; `docs/contratos/contrato_json_dashboard.md:120` reforça o mesmo. `docs/contratos/contrato_tela_json.md:195-196` fala em arranjo horizontal planejado.
- ADR: `docs/adr/ADR-0010...:112-113` usa "layout horizontal plano" como etapa futura, mas não troca o valor final para `horizontal`.
- Código: `tela/renderizador.py:258` usa `vertical/horizontal` em comentário de bordas, sem semântica de arranjo.
- Testes: `tela/teste_loader.py:91` usa `"distribuicao": "horizontal"` na barra mínima.

Classificação:

- É valor ativo de JSON? Sim, mas hoje como `barra_de_menus.distribuicao` e não como `corpo.arranjo`.
- É valor aceito pelo loader? Sim por preservação, se declarado em `corpo.arranjo`, mas sem semântica específica no renderer.
- É valor testado? Sim como distribuição da barra, não como arranjo de corpo.
- É só documentação histórica? Não; é ativo em outros campos.
- Aparece em contrato ativo? Sim, mas com significados diferentes.
- Aparece em ADR aceita? Sim como descrição de layout futuro, não como valor final de `arranjo`.

### 1.5 Ocorrências de `vertical`

Categorias encontradas:

- JSON de produção: `config/telas/orquestrador.json:67` usa `posicao_dashboard = "vertical"`.
- Contratos: `docs/contratos/contrato_composicao_corpo.md:157` e `docs/contratos/contrato_json_dashboard.md:120` listam `vertical|horizontal` para `posicao_dashboard` descontinuado; `contrato_barra_de_menus.md:397` usa verticalmente em descrição visual.
- ADR: `docs/adr/ADR-0010...:112` fala em layout hierárquico vertical compatível.
- Handoff/relatório: `H-0012` e seus relatórios descrevem saída vertical/compatível.
- Código: `tela/renderizador.py:258` menciona vertical/horizontal como caracteres de borda.
- JSON de layout: `config/lancador.json`, `config/layout_console.json`, `config/layout_dado.json` e `config/layout_menu.json` usam `vertical` para regras de alinhamento/espaçamento.

Classificação:

- É valor ativo de JSON? Sim, mas em `posicao_dashboard` e layouts, não em `corpo.arranjo`.
- É valor aceito pelo loader? Sim por preservação, caso declarado em `corpo.arranjo`, sem validação nem execução especial.
- É valor testado? Não como `corpo.arranjo`; sim como texto/saída vertical documentada.
- É só documentação histórica? Não; há campo ativo/transicional.
- Aparece em contrato ativo? Sim, com significado de dashboard/layout.
- Aparece em ADR aceita? Sim como descrição de etapa vertical compatível.

### 1.6 Ocorrências de `tiling`

Categorias encontradas:

- JSON de produção: `config/estilo.json:10` registra `tiling` como preferência do usuário sem preset padrão decidido.
- Contratos: `docs/contratos/contrato_composicao_corpo.md`, `contrato_tela_json.md`, `contrato_json_tela_minima.md`, `contrato_json_dashboard.md` e `contrato_estilo.md` definem `tiling` como default quando `corpo.arranjo` não é declarado.
- Nomenclatura: `docs/NOMENCLATURA.md:129-149` define preferência de tiling.
- ADR: ADR-0008 e ADR-0010 tratam `tiling` no modelo por tela e na composição de dashboard.
- Código: não há leitura efetiva de `config/estilo.json` pelo renderer atual; `loader.py` e `modelo.py` apenas preservam `arranjo`.
- Testes: não há teste de fallback real de `tiling` no renderer atual.

Classificação:

- É valor ativo de JSON? Sim como campo de estilo/documentação em `config/estilo.json`; não como `corpo.arranjo`.
- É valor aceito pelo loader? Não é validado no loader de tela; pertence ao estilo.
- É valor testado? Não como fallback executável.
- É só documentação histórica? Não; é contrato ativo, mas ainda sem execução no renderer atual.
- Aparece em contrato ativo? Sim.
- Aparece em ADR aceita? Sim.

### 1.7 Síntese de termos ativos

- Valores ativos de `corpo.arranjo` hoje: `sobreposto` nos JSONs `orquestrador`, `destino_minimo`, `stub_b` e `grupo_minimo`; além de `grupo_minimo` usar `arranjo = "sobreposto"` no grupo estrutural.
- Valores ativos em outros campos: `horizontal` em `barra_de_menus.distribuicao`; `vertical` em `posicao_dashboard`; `tiling` em estilo/contrato.
- Valores aceitos pelo loader: o loader preserva `corpo.arranjo` sem validar vocabulário; o único bloqueio específico é grupo estrutural com `arranjo == "lado_a_lado"`.
- Valores testados: `sobreposto` é testado como preservado; `lado_a_lado` é testado como inválido em grupo; `horizontal` é usado em testes como distribuição da barra; `linear` aparece em modelo fabricado para demonstrar que o renderer não decide pelo JSON.
- Valores apenas históricos/documentais: `empilhado` e grande parte das ocorrências de `lado_a_lado` ligadas ao H-0011 cancelado/replanejado.
- Contratos ativos ainda dizem que `arranjo` aceita `sobreposto|lado_a_lado`, enquanto a terminologia desejada quer migrar para `vertical|horizontal`.

## 2. Impacto de migrar para `horizontal` e `vertical`

Impacto normativo:

- `docs/NOMENCLATURA.md` precisa substituir a tabela de "Preferência de tiling" e "Arranjo de múltiplos corpos" para `vertical|horizontal`.
- `docs/contratos/contrato_composicao_corpo.md` precisa trocar `sobreposto|lado_a_lado` por `vertical|horizontal` em 4.2, 5.6, regras e critérios de validação.
- `docs/contratos/contrato_json_tela_minima.md` precisa atualizar exemplo e tabela de `corpo.arranjo`.
- `docs/contratos/contrato_tela_json.md` precisa harmonizar "tiling ou arranjo equivalente" e o plano H-0011B.
- `docs/contratos/contrato_json_dashboard.md` precisa evitar ambiguidade entre `posicao_dashboard = "vertical|horizontal"` transicional e `arranjo = "vertical|horizontal"` final.
- `docs/contratos/contrato_estilo.md` e `config/estilo.json` precisam ser revisados se `tiling` também passar a usar os novos valores.

Impacto em JSONs:

- `config/telas/orquestrador.json`: `corpo.arranjo` migraria de `"sobreposto"` para `"vertical"` no estado atual, ou para `"horizontal"` quando houver composição horizontal definida.
- `config/telas/destino_minimo.json`, `config/telas/stub_b.json` e `config/telas/grupo_minimo.json`: `corpo.arranjo` migraria de `"sobreposto"` para `"vertical"`.
- `config/telas/grupo_minimo.json`: o `arranjo` do grupo estrutural também migraria para `"vertical"` se o campo continuar declarado.
- Não há JSON ativo com `lado_a_lado` a migrar.

Impacto em código:

- `tela/loader.py` precisaria trocar a regra especial de grupo: hoje rejeita apenas `arranjo == "lado_a_lado"`; após a ADR, deveria rejeitar `arranjo == "horizontal"` para grupo, ou aceitar aliases transicionais se decidido.
- `tela/modelo.py` preserva o valor e não exigiria alteração estrutural.
- `tela/renderizador.py` hoje não executa `corpo.arranjo`; a troca direta de valor não muda o comportamento visual, mas os comentários/docstrings devem ser ajustados se a ADR passar a exigir execução futura.
- Se houver validação futura de vocabulário, o loader passará de preservador inerte para validador parcial, exigindo cuidado de compatibilidade.

Impacto em testes:

- `tela/teste_loader.py` espera `arranjo == "sobreposto"` no Orquestrador e em telas mínimas; precisará ser atualizado para `vertical`.
- `tela/teste_modelo.py` espera `modelo.corpo.arranjo == "sobreposto"` e preservação de grupo com `arranjo == "sobreposto"`; precisará mudar.
- `tela/teste_renderizador.py` usa modelos fabricados com `sobreposto`; a maioria pode migrar para `vertical` sem mudança de comportamento.
- Teste de rejeição de grupo com `lado_a_lado` deve migrar para rejeição de `horizontal` ou cobrir alias transicional.

Aliases transicionais:

- Recomendação técnica: a ADR deve permitir aliases transicionais por um ciclo curto: `sobreposto -> vertical` e `lado_a_lado -> horizontal`, apenas no loader/normalização ou em validação documental, com prazo explícito de remoção.
- Motivo: contratos ativos, handoffs recentes e testes ainda usam `sobreposto|lado_a_lado`; troca direta é viável nos JSONs ativos, mas arriscada para documentação e artefatos históricos usados como referência.
- Se a decisão for troca direta, o escopo do handoff seguinte deve incluir JSONs, testes e contratos na mesma unidade de trabalho.

Riscos de compatibilidade:

- `horizontal` já significa `barra_de_menus.distribuicao` e aparece em regras de layout; a ADR precisa declarar que `corpo.arranjo = "horizontal"` é outro campo, não substitui distribuição da barra.
- `vertical` já aparece em `posicao_dashboard`; a ADR precisa separar `arranjo` final do campo transicional `posicao_dashboard`.
- O renderer atual não consulta `tiling` real; se a ADR decidir atualizar `tiling`, é necessário decidir se o fallback será implementado agora ou só documentado.

## 3. Barra_de_menus do Orquestrador

### 3.1 Chips declarados no JSON

`config/telas/orquestrador.json` declara 11 chips em `barra_de_menus.chips[]`:

| Ordem | id | tecla | texto |
|---:|---|---|---|
| 1 | `chip_esc` | `Esc` | `Sair` |
| 2 | `chip_paginas` | `<>` | `Páginas` |
| 3 | `chip_colunas` | `-+` | `Colunas` |
| 4 | `chip_grupos` | `#` | `Grupos` |
| 5 | `chip_alternar` | `⇆` | `Alternar` |
| 6 | `chip_navegar` | `✥` | `Navegar` |
| 7 | `chip_selecionar` | `␣` | `Selecionar` |
| 8 | `chip_enter` | `⏎` | `Todos` |
| 9 | `chip_estilo` | `|` | `Estilo` |
| 10 | `chip_verboso` | `V` | `Verboso` |
| 11 | `chip_ajuda` | `?` | `Ajuda` |

Os chips visualmente exibidos no Orquestrador são exatamente esses 11, porque o renderer percorre todos os chips declarados e não avalia `regra_existencia` nem `regra_ativo` neste ciclo.

### 3.2 Origem visual dos chips

Origem por camada:

- JSON: origem direta. `config/telas/orquestrador.json:125-247` declara a lista concreta.
- Loader: preserva `barra_de_menus` como dict em `tela/loader.py:305-353`; não adiciona chip.
- Modelo: copia `barra_de_menus=tela_raw["barra_de_menus"]` em `tela/modelo.py:270`; não adiciona chip.
- Renderer: `_linhas_barra` em `tela/renderizador.py:185-204` lê `barra_de_menus.get("chips", [])` e monta `"[{tecla}] {texto}"`; não gera lista própria.
- Demo: `tela/demo.py` interpreta comandos internos `b`, `s`/Esc e itens do `lancador` em `processar_comando`; não adiciona chip visual à `barra_de_menus`.
- Navegação H-0013: adicionou item de lançador `g -> grupo_minimo`, não chip da barra.

Resposta objetiva:

1. Quantos chips existem hoje em `config/telas/orquestrador.json`? 11.
2. Quais chips aparecem visualmente no Orquestrador? `[Esc] Sair`, `[<>] Páginas`, `[-+] Colunas`, `[#] Grupos`, `[⇆] Alternar`, `[✥] Navegar`, `[␣] Selecionar`, `[⏎] Todos`, `[|] Estilo`, `[V] Verboso`, `[?] Ajuda`.
3. O renderer lê exatamente `barra_de_menus.chips[]` ou gera chips próprios? Lê exatamente `chips[]`; não gera chips próprios.
4. `demo.py` adiciona algum chip? Não.
5. `loader/modelo` adicionam algum chip? Não.
6. Testes esperam todos os chips canônicos ou apenas os declarados? Na intenção declarativa, esperam chips declarados; na prática, os expected literals atuais do Orquestrador esperam os 11 chips hoje declarados.
7. H-0010A/H-0013 mudaram a origem dos chips? H-0010A mudou de hardcoded para JSON/modelo; H-0013 não mudou a origem da barra, só adicionou item de lançador `g`.
8. O excesso de chips é problema de JSON atual, contrato, renderer ou teste? Principalmente JSON atual, com testes congelando a saída atual. Contrato já afirma que lista concreta vem do `tela.json`, mas contém linguagem de chips "sempre presentes" que merece ajuste para não ser lida como obrigação global de declarar todos em toda tela.

### 3.3 Testes que exigem esses chips

Testes relevantes:

- `tela/teste_renderizador.py`: `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_ORQUESTRADOR_RETA` contêm os 11 chips; também verifica explicitamente `[Esc] Sair`, `[<>] Páginas`, `[?] Ajuda` e ausência de `[B] Borda`.
- `tela/teste_demo.py`: `_EXPECTED_CURVA`, `_EXPECTED_RETA` e `_EXPECTED_DIAGNOSTICO_CURVA_42` contêm os 11 chips do Orquestrador.
- `tela/teste_diagnostico.py`: expected do diagnóstico contém os chips do Orquestrador e verifica ausência de `[B] Borda`.
- `tela/teste_loader.py`: não exige todos os chips, mas preserva `chip_estilo` e verifica `barra_de_menus` como dict.
- `tela/teste_modelo.py`: não exige todos visualmente, mas procura `chip_estilo` preservado no modelo.

Conclusão de teste: não há teste que obrigue o renderer a inventar um conjunto canônico global. Há testes que obrigam o output literal atual a conter os 11 chips porque o JSON atual contém os 11.

### 3.4 Conclusão sobre chips extras

Classificação:

- Problema de JSON: Sim, principal. O Orquestrador declara chips condicionais/específicos que hoje o usuário considera não aplicáveis ou extras.
- Problema de renderer: Não como origem dos chips. O renderer está aderente ao modelo declarativo: renderiza o que recebe.
- Problema de contrato: Parcial. `contrato_barra_de_menus.md` já diz que a lista concreta pertence ao `tela.json`, mas seções como "chips canônicos de existência sempre presente" podem induzir a declaração global obrigatória. A ADR deve resolver essa leitura.
- Problema de teste: Parcial. Os testes cristalizam o JSON atual em outputs literais e precisarão mudar junto com o JSON, mas não são a fonte primária do excesso.
- Herança de handoff/documentação anterior: Sim. H-0011 já propunha barra mínima do Orquestrador com `[Esc] Sair` e `[?] Ajuda`, mas foi cancelado/replanejado. H-0010A formalizou a origem declarativa dos chips; H-0013 não alterou a barra.

## 4. Recomendação para ADR

Recomendação: criar uma ADR única.

Justificativa: os dois assuntos são coesos porque ambos reforçam a mesma decisão arquitetural: a tela declara sua composição e seus controles aplicáveis; contratos definem semântica, não forçam nomes finais ambíguos nem listas globais concretas. A ADR pode se chamar:

```text
ADR-0011-terminologia-arranjo-e-barra-de-menus-declarativa-por-tela.md
```

Decisões recomendadas:

- Substituir os valores finais de `corpo.arranjo` por `vertical` e `horizontal`.
- Declarar `sobreposto` e `lado_a_lado` como aliases transicionais por período definido, com normalização ou aceitação apenas para compatibilidade documental/JSON legado.
- Definir `vertical` como sucessor de `sobreposto`.
- Definir `horizontal` como sucessor de `lado_a_lado`.
- Separar explicitamente `corpo.arranjo = "horizontal"` de `barra_de_menus.distribuicao = "horizontal"`.
- Definir que `barra_de_menus` é declarativa por tela: só contém chips aplicáveis àquela tela.
- Definir que o Orquestrador não deve declarar chips canônicos que não se aplicam a ele no ciclo atual.
- Definir que o renderer não gera chips canônicos por conta própria.
- Definir que testes devem esperar chips declarados, não um conjunto global obrigatório.
- Ajustar a linguagem contratual para que "canônico" signifique semântica/ordem quando presente, não obrigatoriedade de presença em toda tela, exceto quando a ADR decidir explicitamente.

Decisão pendente para gerente:

- Se a barra mínima do Orquestrador deve ser exatamente `[Esc] Sair` e `[?] Ajuda`, como H-0011 sugeria, ou se algum chip adicional já é aplicável ao Orquestrador por declaração funcional atual.

## 5. Arquivos afetados prováveis

ADR nova:

- `docs/adr/ADR-0011-terminologia-arranjo-e-barra-de-menus-declarativa-por-tela.md` ou próximo número disponível.
- `docs/adr/INDICE_ADR.md`

Contratos/NOMENCLATURA:

- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_estilo.md` se `tiling` também migrar seus valores.

JSONs:

- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/grupo_minimo.json`
- `config/telas/stub_b.json`
- `config/estilo.json` se `tiling` deixar de usar `sobreposto|lado_a_lado`.

Código:

- `tela/loader.py` para regra de grupo e, se decidido, aliases/normalização.
- `tela/modelo.py` apenas se a normalização ocorrer no modelo.
- `tela/renderizador.py` principalmente docstrings; lógica só se a ADR exigir execução de `horizontal`.
- `tela/demo.py` não deve precisar mudar para chips da barra; pode mudar apenas se navegação/ações forem ampliadas.

Testes:

- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`

Handoffs futuros:

- Handoff para aplicar ADR em contratos e nomenclatura.
- Handoff para migrar JSONs ativos.
- Handoff para atualizar testes literais.
- Handoff separado, se necessário, para implementar `arranjo = "horizontal"` no renderer.
- Handoff separado, se necessário, para remover aliases transicionais.

## 6. Riscos e bloqueios

- Decidir se `sobreposto|lado_a_lado` serão aliases transicionais ou removidos imediatamente.
- Decidir se `tiling` muda seus valores junto com `corpo.arranjo` ou se permanece como camada separada temporariamente.
- Resolver a ambiguidade de `horizontal` em três lugares: arranjo do corpo, distribuição da barra e posicionamento/layout.
- Resolver a ambiguidade de `vertical` entre arranjo do corpo e `posicao_dashboard` transicional.
- Decidir quais chips são aplicáveis ao Orquestrador agora. O levantamento prova a origem dos 11 chips, mas não decide a política funcional final.
- Confirmar se `[Esc]` e `[?]` continuam sempre presentes em toda tela ou se até esses devem ser declarativos por tela com obrigatoriedade contratual mínima.
- Cuidar para relatórios/handoffs históricos não serem reescritos; devem permanecer como histórico, salvo documentos ativos.

## 7. Verificações finais

Comandos executados após a criação deste relatório:

```text
git status --short
?? docs/relatorios/LEVANTAMENTO_ADR_TERMINOLOGIA_ARRANJO_BARRA_ORQUESTRADOR.md

git diff --stat
(sem saída; arquivo novo ainda não rastreado)

git diff --name-only
(sem saída; arquivo novo ainda não rastreado)
```

## Resultado

Apenas este relatório foi criado.
