# Relatório de criação do H-0056

## Registro

O arquivo `docs/handoff/H-0056-popup-basico-exibicao-voltar.md` foi
materializado para `ITEM-0017`/`ADR-0044` com status explícito
`BLOCKED_USER_DECISION`.

## Escopo material

Foi registrado somente o primeiro incremento: pop-up modal sobreposto ao
corpo da tela ativa, conteúdo textual curto pronto em runtime, moldura,
título, área própria de chips, `[Esc] Voltar`, bloqueio da tela subjacente e
retorno `ABORTADO` sem payload. H-0057, H-0058 e H-0059 foram mantidos fora.

## Caminhos de implementação resolvidos

Foram resolvidos os pontos existentes `tela/renderizacao/tela.py`,
`tela/renderizacao/geometria_caixa.py`, `tela/renderizacao/composicao_corpo.py`,
`tela/carregamento/estilo.py`, `tela/renderizacao/barra_menus.py`,
`demo/demo.py` e `config/telas/demo/demo.json`, além dos novos caminhos de
renderer, testes, stub demonstrativo e relatório de implementação descritos
no handoff. A área de chips do pop-up foi explicitamente separada da
`barra_de_menus`.

## Testes/demonstração definidos

Foram definidos testes focais para domínios declarativos, geometria simples,
centralização, preservação, captura modal, `Esc`, retorno sem payload,
independência da barra e ausência de paginação, seguidos da suíte canônica.
Também foi definida demonstração reproduzível com abertura, tecla ignorada,
fechamento e reativação da mesma tela.

## Verificações

Os quatro documentos obrigatórios foram lidos integralmente. As buscas foram
restritas aos focos e caminhos autorizados; não foram lidos relatórios,
outras ADRs, outros contratos, handoffs históricos ou módulos de nomenclatura
adicionais. Nenhum código, configuração, teste ou contrato foi alterado.

## Bloqueio

`contrato_tela_json.md`, seção 35, deixa em aberto nome, localização,
cardinalidade, forma de coleção e identidade da declaração estrutural do
pop-up. O loader apenas preserva campos desconhecidos em `_raw`; isso não
fecha schema. Escolher uma forma no handoff violaria a autoridade vigente.
O desbloqueio exige decisão do usuário/autoridade antes de qualquer
implementação ou configuração demonstrativa nominal.
