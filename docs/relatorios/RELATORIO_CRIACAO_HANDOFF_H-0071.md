# Relatório — Criação do Handoff H-0071

## Handoff criado

`docs/handoff/H-0071-correcao-chips-multitecla-barra-menus-estilo.md`,
status `READY_FOR_IMPLEMENTATION`, predecessor funcional `H-0070`, relação
`correcao_pos_validacao_manual_e_pos_patch_normativo`. Fundamenta-se em
`ADR-0046` (status `ADR_APPROVED` após patch `P01`) e na aplicação
documental correspondente (status `ADR_APPLICATION_APPROVED` após patch
`P02`), sem bloqueios documentais vigentes.

## Capacidade

Correção coesa de sete pontos: (1) composição visual de chips com múltiplas
teclas como unidade única com separador `/`, para **todos** os presets de
chip, incluindo os que possuem delimitadores próprios (`Colchete`, `Curva`,
`Ornamental`, `Traço`); (2) aplicação dessa composição aos chips reais da
Barra de Menus, sem mecanismo visual paralelo à demonstração da tela de
Estilo; (3) preset `Ponto` em multitecla (`espaço + PgUp/PgDn + ponto
único`); (4) presets `Destaque Texto` e `Destaque Fundo` em multitecla,
incluindo a assimetria lateral de cor de fundo aprovada para `Destaque
Texto`; (5) contenção/reset de cor e fundo dentro da unidade visual do
chip; (6) largura visual efetiva desconsiderando sequências ANSI; (7)
configuração concreta mínima em `config/estilo.json` para materializar os
campos opcionais já aprovados no schema.

O handoff resolve nominalmente `MF-ITEM0010-001` (composição híbrida
incorreta, ex.: `╭PgUp][PgDn╮`) e `MF-ITEM0010-002` (Barra real não
aplicando cor/fundo dos presets). Deixa explicitamente fora `MF-ITEM0010-003`
e todo o restante já listado como fora de escopo (ordem cursor → toggle →
texto, indentação hierárquica, navegação multinível, tiling, teclas de
função, fullscreen, novo desenho normativo).

## Divergência corrigida em relação a H-0070

H-0070 (§7-§8) havia fixado que presets com delimitadores próprios
preservariam a concatenação individual por tecla (`[PgUp][PgDn]`), sem
separador `/`. O patch normativo `P01` de `ADR-0046`
(`DEC-ITEM0010-CHIP-01`) e `contrato_chip.md` seção 10.1 suplantaram
explicitamente essa decisão: a partir de `ADR-0046`, todos os presets
multitecla — com ou sem delimitadores próprios — usam a unidade única com
`/`. O H-0071 registra essa reversão de forma explícita e instrui a não
preservar a regra antiga de H-0070 nesse ponto específico.

## Arquivos/diretórios autorizados (nominais, sem diretório inteiro)

Código: `tela/renderizacao/barra_menus.py` (`_texto_chip_barra` e o bloco de
agrupamento exclusivo do par `chip_pagina_anterior`/`chip_pagina_proxima`,
H-0051), `tela/renderizacao/estilo.py` (`amostra_chip`),
`tela/carregamento/estilo.py` (`EstiloResolvido`, extensão para os campos
opcionais `cor_fundo_esquerdo`/`cor_fundo_direito`). Configuração:
`config/estilo.json`, restrito a adicionar `cor_fundo_esquerdo: "padrão"` e
`cor_fundo_direito: "azul"` ao preset `"Destaque Texto"` — reaproveitando o
valor de destaque já materializado em `"Destaque Fundo"`, sem novo schema
ou novo preset. Testes: extensão de
`tela/testes_renderizador/barra_menus.py` e `demo/teste_demo_paginacao.py`;
novos `tela/teste_estilo_h0071.py` e `demo/teste_demo_estilo_h0071.py`;
regressão em `tela/teste_popup.py`. Relatório futuro:
`docs/relatorios/IMP-0071-correcao-chips-multitecla-barra-menus-estilo.md`.

## Testes e demonstração definidos

Testes focais para uma tecla, duas teclas por família estrutural, `Ponto`,
`Destaque Texto`, `Destaque Fundo`, contenção/reset ANSI, largura visual sem
ANSI contado, Barra de Menus real e ausência de regressão de ações de uma
tecla, além da suíte canônica completa
(`PYTHONDONTWRITEBYTECODE=1 python -m pytest`). Demonstração reproduzível em
TTY real cobrindo os mesmos pontos, sem fixture nova — reaproveita
`config/telas/demo/h0069_estilo_demonstracao_integrada.json` e a tela de
paginação já existente. A aprovação manual final permanece exclusiva do
usuário e não pode ser declarada pelo agente de implementação.

## Relação com H-0070

H-0070 foi usado exclusivamente como fonte operacional: arquivos e pontos de
implementação já localizados, fixtures reaproveitáveis, testes já mapeados.
Onde H-0070 divergiu das autoridades vigentes (composição multitecla de
presets delimitados), prevaleceram `ADR-0046` e os contratos atuais,
conforme instruído.

## Bloqueios

Nenhum. H-0070 forneceu evidência técnica suficiente para determinar
nominalmente os arquivos de implementação necessários.
