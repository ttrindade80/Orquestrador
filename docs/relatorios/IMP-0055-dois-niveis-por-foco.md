# IMP-0055 — dois níveis por foco

## Arquivos criados ou alterados

- Alterados: `tela/navegacao.py`, `tela/selecao.py`, `tela/renderizacao/console.py`, `demo/demo.py`, `tela/teste_navegacao.py`, `demo/teste_demo_console.py` e, por autorização focal desta execução, `tela/carregamento/envelope_pre_adr_0028.py`.
- Criados: `config/telas/demo/h0055_dois_niveis_por_foco.json` e `config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json`.
- Atualizado: este relatório.

## Comportamento materializado

A implementação materializa a política explícita `dois_niveis_por_foco` sobre a hierarquia existente. O cursor em pré-ordem distingue, sem campo adicional, o toroide de pais e o toroide de filhos do pai corrente. Espaço no pai entra em seus filhos; as quatro setas percorrem somente o toroide ativo com wrap; Esc no filho retorna ao pai. As escolhas reutilizam `selecoes` em runtime e a apresentação `tg`: o primeiro filho direto de cada pai é reconciliado como escolha inicial, Espaço transfere a escolha dentro do mesmo pai, repetir Espaço mantém a escolha e Esc no nível dos pais preserva as escolhas ao usar a saída vigente. A renderização e o mapa físico reutilizam a projeção hierárquica vigente.

As fixtures novas contêm cinco pais com quatro filhos diretos cada, total de 25 itens lógicos, IDs estáveis, dois níveis, `apresentacao: hierarquia`, `politica_paginacao: com`, `politica_selecao: multipla` e D23 com modo alternável iniciado em `nao_verboso`. O carregador reconhece essa combinação nominal somente quando a estrutura e os valores declarativos da fixture H-0055 são válidos; as rejeições gerais de envelopes híbridos permanecem. Nenhum estado é escrito de volta no JSON.

## Testes e demonstração

O comando focal obrigatório foi executado:

`PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_console.py -q`

Resultado: 92 testes passaram.

O carregamento focal foi confirmado semanticamente: modelo H-0055, conteúdo externo em `hierarquia`, tipo explícito `dois_niveis_por_foco`, 25 itens lógicos, cinco pais e quatro filhos diretos por pai, com modo alternável iniciado em `nao_verboso`.

A checagem focal também confirmou a aceitação da combinação válida e a rejeição de uma variante H-0055 inválida e de um híbrido nominal genérico.

Suíte canônica: `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — 1095 testes passaram.

Smoke não interativo: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco` — código 0; a saída exibiu os pais/filhos H-0055, escolhas iniciais `tg` e `[PgUp][PgDn] Páginas`. Isso é somente smoke test, não validação visual ou interativa.

## Desvios e exceções

Por autorização focal, `tela/carregamento/envelope_pre_adr_0028.py` passou a reconhecer apenas a combinação nominal e validada de H-0055 com D23. Não foram criados schema, enum, política ou fallback novos. Não há bloqueio material restante.

## Validação manual pendente

Permanece pendente a validação humana em TTY real do percurso por teclas, geometria, chips e paginação visual/interativa. A demonstração não interativa não constitui essa validação.
