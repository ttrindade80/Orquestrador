# Relatório — Criação do Handoff H-0073

## Metadata

- Etapa: `CRIAR_HANDOFF`
- Objeto: H-0073
- ADR: ADR-0047
- Predecessor funcional: H-0072 (`I1_IMPLEMENTATION_APPROVED`, achado
  material pendente: nenhum)
- Artefatos criados:
  - `docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md`
  - `docs/relatorios/RELATORIO_CRIACAO_HANDOFF_H-0073.md` (este arquivo)

## Telas reais encontradas

Busca focal (`rg -l 'dois_niveis_por_foco' config/telas/demo`; confirmação
com `rg -n 'politica_navegacao' config/telas/demo -A2`) localizou quatro
arquivos estruturais com `politica_navegacao.tipo = "dois_niveis_por_foco"`:

- `h0055_dois_niveis_por_foco.json` — tela real legada, conteúdo estático.
  **Alvo fechado** para implementação.
- `h0063_estilo_estrutura_navegacao_dois_niveis.json` — tela real, conteúdo
  dinâmico (Estilo). **Alvo bloqueado documentalmente** (ver abaixo).
- `h0062_estilo.json` — achado além dos dois alvos conhecidos, investigado
  focalmente conforme exigido. É um shell estrutural sem produtor de
  conteúdo ativo (nenhuma referência Python a `console_h0062_estilo`; ausente
  do catálogo `_CATALOGO_CONTEUDO_EXTERNO` de `demo/demo.py`) e já
  classificado por `docs/handoff/H-0066-acao-aplicar-candidato-estilo.md`
  como "precedente declarativo histórico", superado por H-0063. Excluído da
  reconciliação — não há filhos reais a formatar.
- `h0072_formatacao_generica_dois_niveis_por_foco{,_conteudo}.json` —
  fixture de referência da própria capacidade genérica de H-0072, não tratada
  como migração legada, conforme instrução explícita.

## Campos reais de H-0063 identificados

Cadeia de descoberta: `tela/estilo.py::ControladorTelaEstilo._construir_conteudo`
(produtor real do conteúdo dinâmico de H-0063) e
`tela/renderizacao/estilo.py::compor_titulo_com_amostra`. Achado: o "nome" e
o "exemplo visual" do preset são compostos em uma única string (`campos["titulo"]`)
antes de chegar ao nó de conteúdo; não existe campo separado de "exemplo
visual" em `campos` (apenas `titulo`, `categoria`, `preset`, `navegavel`,
`selecionavel`). Confirmado pelo próprio consumidor da capacidade genérica
(`tela/renderizacao/conteudo_externo.py:356-357`, leitura silenciosa via
`.get(campo, "")`) e por teste existente
(`tela/teste_estilo_h0070.py::test_amostras_de_cada_categoria_...`) que só
referencia `campos["titulo"]`/`campos["preset"]`. Como a ADR-0047 §4.11
pressupõe dois campos já separados, e inventar um nome de campo é
expressamente proibido, este achado foi registrado como
`BLOCKED_DOCUMENTATION` dentro do handoff (§9), sem fechar
`tabela.colunas` de H-0063.

## Arquivos futuros autorizados

Edição: `config/telas/demo/h0055_dois_niveis_por_foco.json` (adicionar bloco
`formato.dois_niveis_por_foco.filho`). Extensão de testes existentes:
`tela/teste_navegacao.py` (seção H-0055) e `demo/teste_demo_console.py`
(cenário `h0055_dois_niveis_por_foco`). Arquivo novo: `demo/teste_demo_h0073_h0055_reconciliado.py`.
Nenhuma edição de `h0063_estilo_estrutura_navegacao_dois_niveis.json`,
`h0062_estilo.json` ou das fixtures de H-0072 é autorizada.

## Conteúdo explicitamente preservado

`h0055_dois_niveis_por_foco_conteudo.json` permanece byte-a-byte inalterado
— verificado mecanicamente: com `apresentacao = "texto"`, o renderer lê
`niveis[1].conteudo` (`"titulo"`, já existente), sem consumir campo novo.
Conteúdo de H-0063 (presets, textos, exemplos, símbolos, ordem, candidato,
baseline, aplicação, persistência, publicação) integralmente preservado —
nenhuma edição foi autorizada para essa tela.

## Tratamento planejado de H-0070

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
permanece classificado como não causal a este handoff: o escopo
efetivamente alterado (H-0055) não toca `tela/estilo.py` nem
`h0063_estilo_estrutura_navegacao_dois_niveis.json`. Não entra no conjunto
de regressão do H-0073; nenhuma correção por conveniência foi autorizada.

## Verificações executadas

- `rg -l`/`rg -n` restritos a `config/telas/demo` para o levantamento
  focal (nenhum `find .`, `tree` ou busca em `docs/relatorios`).
- Cadeia de descoberta de H-0063 restrita aos identificadores da própria
  tela e aos arquivos diretamente na cadeia de produção de conteúdo.
- Leitura completa de ADR-0047, H-0072, `contrato_tela_json.md` §36,
  `contrato_console.md` §22.16/§25, `contrato_json_console.md` §7.1/§15,
  `32_CONSOLE.md` §4.10/§4.11, `44_APRESENTACOES_...md` §4.6/§8B.
- Confirmação de que `apresentacao = "tabela"` teria exigido dois `campo`
  reais e distintos para H-0063, indisponíveis hoje — evitando invenção de
  transformação.
- `git diff --check` executado sobre os dois artefatos desta etapa (sem
  problemas de espaço em branco).

## Bloqueios

Um bloqueio documental registrado no handoff (§9/§15): H-0063 não pode ser
reconciliada nesta etapa por ausência de campo separado de "exemplo visual"
no conteúdo dinâmico produzido por `tela/estilo.py`. Resolução depende de
decisão documental prévia, fora do escopo desta criação de handoff. O
escopo de H-0055 está integralmente fechado e não possui bloqueios.
\n