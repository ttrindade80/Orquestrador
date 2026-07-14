# Relatório de Auditoria — H-0014 Handoff

## Status

QA_APPROVED

## Contexto

Auditoria do handoff `docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md`, criado para migração/estabilização pós-ADR antes de nova capacidade de composição.

O H-0014 foi verificado contra ADR-0011, ADR-0012, contratos ativos, H-0012, H-0013, JSONs atuais e módulos/testes da tela. A base antes de implementação apresenta apenas o handoff H-0014 como arquivo não rastreado.

## Arquivos lidos

- `docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md`
- `docs/adr/ADR-0011-terminologia-arranjo-vertical-horizontal.md`
- `docs/adr/ADR-0012-barra-de-menus-declarativa-por-tela.md`
- `docs/adr/INDICE_ADR.md`
- `docs/NOMENCLATURA.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md`
- `config/telas/orquestrador.json`
- `config/telas/grupo_minimo.json`
- `config/telas/destino_minimo.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/demo.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`

## Verificações executadas

```bash
git status --short
```

Resultado:

```text
?? docs/handoff/H-0014-migracao-pos-adr-arranjo-barra-declarativa.md
```

```bash
git diff --stat
```

Resultado: sem saída.

```bash
git diff --name-only
```

Resultado: sem saída.

Confirmação: antes da implementação, apenas o handoff H-0014 está não rastreado. Não há arquivos modificados rastreados.

## Verificação do objetivo

O handoff define H-0014 como migração pós-ADR, antes de nova capacidade. O objetivo cobre:

- migrar `grupo_minimo.json` para `arranjo: "vertical"` em `corpo.arranjo` e no grupo;
- alinhar `loader.py` apenas na validação de grupo, rejeitando `horizontal` e `lado_a_lado`;
- reduzir `barra_de_menus.chips[]` do Orquestrador a `chip_esc` e `chip_ajuda`;
- atualizar testes literais e testes de loader/modelo conforme a migração;
- preservar o fluxo demonstrável do H-0013.

A especificação é compatível com o estado atual dos arquivos: `grupo_minimo.json` ainda usa `sobreposto`, o Orquestrador declara 11 chips, e o renderer já renderiza chips declarados sem inventar lista canônica.

## Verificação de rastreabilidade

Rastreabilidade aprovada.

O frontmatter e a seção de metadados rastreiam:

- `H-0014`;
- status `HANDOFF_READY`;
- tipo `handoff_implementacao`;
- ADR-0011;
- ADR-0012;
- H-0012;
- H-0013;
- commit base `ceaf0be`.

## Verificação de escopo permitido

Escopo permitido aprovado.

O handoff limita a implementação a:

- alteração declarativa de `config/telas/grupo_minimo.json`;
- alteração declarativa de `config/telas/orquestrador.json`;
- alteração pontual de `_validar_grupo` em `tela/loader.py`;
- atualização dos testes afetados;
- criação do relatório `docs/relatorios/IMP-0014-migracao-pos-adr-arranjo-barra-declarativa.md`.

`modelo.py` e `renderizador.py` aparecem como condicionais, com expectativa explícita de não alteração se a verificação confirmar que já preservam/renderizam declarativamente. `demo.py` é proibido.

## Verificação de fora de escopo

Fora de escopo aprovado.

O handoff proíbe claramente:

- segundo elemento no grupo e grupo com 2 ou mais elementos;
- arranjo horizontal e `lado_a_lado` como novo caminho;
- aninhamento de grupos;
- distribuição percentual/fração;
- migração do Orquestrador inteiro para grupo;
- novo tipo funcional;
- console real;
- foco, seleção e navegação por `[✥]`;
- novo registry;
- novo mecanismo de chip;
- alteração de ADRs, contratos e `NOMENCLATURA.md`;
- reabertura de H-0011/H-0011A;
- uso de letras na numeração de handoffs.

As menções a grupo com 2 elementos aparecem apenas como ciclo futuro H-0015, explicitamente condicionado à conclusão do H-0014, sem autorizar implementação neste ciclo.

## Verificação de arquivos permitidos/proibidos

A fronteira está clara e implementável.

Arquivos obrigatórios/permitidos estão listados de forma exaustiva. Arquivos proibidos incluem `docs/adr/`, `docs/contratos/`, `docs/NOMENCLATURA.md`, `tela/demo.py`, `tela/diagnostico.py`, JSONs fora do alvo e qualquer arquivo não listado.

O relatório de implementação `IMP-0014` está corretamente exigido em `docs/relatorios/`.

## Verificação de critérios de aceite

Critérios de aceite aprovados.

Os critérios cobrem:

- validade JSON;
- migração de `grupo_minimo` para `vertical`;
- ausência de `sobreposto` em `grupo_minimo`;
- manutenção de campos não alvo;
- redução de chips do Orquestrador;
- preservação de `filtros`, `bindings`, `referencias_de_acoes` e itens `d`/`g` do lançador;
- rejeição de `horizontal` e `lado_a_lado` em grupo;
- aceitação de `vertical` e ausência de `arranjo`;
- preservação do fluxo demonstrável H-0013;
- ausência de alterações fora da lista permitida;
- ausência de commit.

## Verificação de testes obrigatórios

Testes obrigatórios aprovados como especificação de handoff.

O handoff exige execução de:

- `python tela/teste_loader.py`
- `python tela/teste_modelo.py`
- `python tela/teste_renderizador.py`
- `python tela/teste_diagnostico.py`
- `python tela/teste_demo.py`
- `python -m json.tool config/telas/grupo_minimo.json`
- `python -m json.tool config/telas/orquestrador.json`
- verificação de `arranjo` vertical;
- verificação dos 2 chips do Orquestrador;
- verificação de rejeição de `horizontal`;
- verificação por subprocess do fluxo demonstrável;
- verificações de cache e estado Git.

Os critérios exigem exit 0, ausência de `[FALHOU]`, ausência de traceback e JSON válido.

## Achados bloqueantes

0.

## Achados não bloqueantes

0.

## Conclusão

O handoff H-0014 está fechado, rastreável e implementável. Pode seguir para implementação.
