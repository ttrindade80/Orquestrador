# Relatório de levantamento documental — reorganização da nomenclatura

## 1. Identificação

```yaml
etapa: LEVANTAMENTO_DOCUMENTAL
artefato_principal: docs/NOMENCLATURA.md
anexo_comparativo: PROPOSTA_ORGANIZACAO_NOMENCLATURA.md
resultado_anexo: NAO_ENCONTRADO
relatorio: docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
data_execucao: 2026-07-20
papel_exercido: levantamento documental neutro
```

## 2. Escopo e limites

fato_documental_comprovado:

- `docs/NOMENCLATURA.md` existe e possui 1856 linhas.
- `PROPOSTA_ORGANIZACAO_NOMENCLATURA.md` nao foi localizado pelo caminho nominal na raiz do repositorio nem por `find . -name 'PROPOSTA_ORGANIZACAO_NOMENCLATURA.md' -print`.
- `docs/INDICE.md`, `docs/backlog.md`, `docs/issues.md` e `docs/adr/INDICE_ADR.md` foram abertos integralmente.
- `docs/contratos/`, `docs/adr/`, `docs/handoff/`, `docs/relatorios/`, `config/`, `demo/` e `tela/` foram inspecionados seletivamente por referencias ao documento, secoes, termos, ADRs e consumidores.

conteudo_atual:

- Este relatorio registra fatos, evidencias e lacunas.
- Este relatorio nao aprova estrutura, nao cria ADR, nao altera contrato e nao escolhe destino documental.

proposta_do_anexo:

- NAO_ENCONTRADO.

decisao_do_usuario:

- NAO_CONFIRMADO para qualquer reorganizacao final.

lacuna:

- A comparacao material com o anexo fica limitada porque o arquivo do anexo nao existe no workspace inspecionado.

## 3. Fontes abertas

| Fonte | Estado | Evidencia |
|---|---|---|
| `docs/NOMENCLATURA.md` | CONFORME aberto | 1856 linhas; frontmatter nas linhas 1-11; titulo na linha 13 |
| `PROPOSTA_ORGANIZACAO_NOMENCLATURA.md` | NAO_ENCONTRADO | `wc` retornou "No such file or directory"; `find` nao retornou caminho |
| `docs/INDICE.md` | CONFORME aberto | ordem de leitura nas linhas 28-46 |
| `docs/backlog.md` | CONFORME aberto | regra de uso como itens planejados, nao contrato, nas linhas 12-15 |
| `docs/issues.md` | CONFORME aberto | regra de issues como impedimentos, bugs e decisoes pendentes, nao contrato, nas linhas 12-14 |
| `docs/adr/INDICE_ADR.md` | CONFORME aberto | regra de ADR nas linhas 11-17; decisoes nas linhas 29-58 |
| `docs/contratos/` | CONFORME inspecao seletiva | contratos citam `origem_especificacao` e secoes de `NOMENCLATURA.md` |
| `docs/adr/` | CONFORME inspecao seletiva | ADR-0001 a ADR-0028 localizadas; indice registra status |
| `docs/handoff/` | CONFORME inspecao seletiva | handoffs H-0019, H-0035, H-0036 e H-0037 demonstram consumo por ciclo |
| `docs/relatorios/` | CONFORME inspecao seletiva | relatorios de aplicacao e QA registram consumo historico e verificacoes |
| `config/` | CONFORME inspecao seletiva | `config/estilo.json`, `config/elementos/*`, `config/layouts/*`, `config/telas/demo/*` contem valores/instancias relacionados |
| `demo/` e `tela/` | CONFORME inspecao seletiva | codigo e testes consomem termos como `distribuicao_matricial`, `politica_modo`, `SIGWINCH`, `barra_de_menus` |

## 4. Caracterização do arquivo atual

| Item | Resultado factual | Evidencia |
|---|---|---|
| Quantidade total de linhas | 1856 | `wc -l docs/NOMENCLATURA.md` |
| Titulo principal | `Nomenclatura — Sistema Novo` | `docs/NOMENCLATURA.md:13` |
| Metadados | `name`, `description`, `metadata.type`, `scope`, `status`, `origem_especificacao`, `atualizado_em`, `reaproveitado_de_legado` | linhas 1-11 |
| Data declarada | `atualizado_em: 2026-07-14` | linha 9 |
| Estado documental declarado | `status: parcial` | linha 7 |
| Regra declarada | unica fonte de nomes validos para contratos derivados | linhas 15-25 |
| Presenca de terminologia | SIM | secoes 1, 2, 4, 5, 6.2, 6.3, 13, 14.2, 15, 16, 17, 18, 19 |
| Presenca de schema | SIM | secoes 0, 1, 2.2, 4.4, 5.1.3, 7.2, 7.3, 8.4, 16.4, 18.2, 19.7.2 |
| Presenca de regras comportamentais | SIM | regras declarativas, runtime, navegacao, paginacao, distribuicao e fallback |
| Presenca de algoritmos | SIM | calculo de colunas do `lancador`, distribuicao de vaos, navegacao toroidal, arredondamento e fallback |
| Presenca de exemplos | SIM | tela de processamento, indicador de pagina, dashboard raiz, exemplos de termos e campos |
| Presenca de decisoes de ADR | SIM | ADR-0008, ADR-0021, ADR-0022 na secao 0; ADR-0001 a ADR-0028 ao longo do arquivo |
| Presenca de aliases | SIM | `sobreposto`, `lado_a_lado`, `barra_de_menus.distribuicao = "horizontal"` |
| Presenca de termos descontinuados | SIM | `menu` como corpo, `dado`, `Info`, `posicao_dashboard`, caminhos transicionais |
| Presenca de pendencias | SIM | secao 11; decisoes deferidas nas secoes 17.5, 18.6, 19.6, 19.7.5 |
| Presenca de levantamentos historicos | SIM | levantamento do Codex sobre `teste_classe_c.py` / `teste_combo.py` nas linhas 1103-1120 |
| Presenca de estados transitorios de artefatos | SIM | tabela de status dos JSONs nas linhas 89-101 |
| Presenca de caminhos futuros ou reservados | SIM | `orquestrador.py`, `config/telas/orquestrador.json`, `config/telas/demo/`, `config/elementos/*` |
| Presenca de decisoes explicitamente deferidas | SIM | secoes 17.5, 18.6, 19.6, 19.7.5 |

Responsabilidades documentais exercidas no arquivo atual:

| Responsabilidade | Presenca | Evidencia |
|---|---|---|
| Glossario terminologico | CONFORME | titulo, regra e multiplas tabelas de termos |
| Schema e semantica | CONFORME | linha 34 define responsabilidade de `NOMENCLATURA.md`; secoes de schema |
| Registro de regras normativas | CONFORME | secoes 0, 4, 5, 6.2, 6.3, 14, 16-19 |
| Registro de historico/transicao | CONFORME | linhas 89-101, 1103-1120, 1132-1142 |
| Registro de pendencias | CONFORME | linhas 1074-1130, 1599-1614, 1703-1717, 1790-1804, 1850-1856 |
| Lista de ADRs aceitas | CONFORME | secao 12 lista ADR-0001 a ADR-0004; indice ADR lista ADR-0001 a ADR-0028 |

## 5. Inventário por bloco

| ID | Seção e intervalo | Tema | Tipo de conteúdo | Termos principais | Estado aparente | Autoridade citada | Autoridade comprovada | Contratos consumidores | Outros consumidores | Duplicações encontradas | Pendências ou histórico misturados | Destino sugerido pelo anexo | Correspondência factual com o anexo | Decisão ainda necessária | Evidências |
| -- | ----------------- | ---- | ---------------- | ----------------- | --------------- | ----------------- | --------------------- | ---------------------- | ------------------- | ----------------------- | ---------------------------------- | --------------------------- | ----------------------------------- | ------------------------ | ---------- |
| NOM-LEV-001 | Frontmatter, linhas 1-11 | Metadados do documento | REFERENCIA_DOCUMENTAL | `nomenclatura`, `sistema_novo`, `parcial` | ATIVO | proprio documento | COMPROVADA | indireto: todos contratos que citam o documento | `docs/INDICE.md` | NAO_CONFIRMADO | status parcial no mesmo arquivo que regras normativas | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir se metadados continuam no documento principal | linhas 1-11 |
| NOM-LEV-002 | Regra, linhas 15-25 | Fonte unica de nomes | REGRA_COMPORTAMENTAL | nomes validos, sinonimo, glossario | ATIVO | decisao explicita do usuario declarada | CONVERSA_DECLARADA_NO_DOCUMENTO | contratos em geral | `docs/INDICE.md` linhas 30-34 | repetida no indice como fonte de verdade | historico do Codex citado como nao decisao | NAO_ENCONTRADO | NAO_VERIFICAVEL | confirmar autoridade futura dessa regra | linhas 17-25 |
| NOM-LEV-003 | 0, linhas 27-56 | Politica schema x dados | SCHEMA | `NOMENCLATURA.md`, `estilo.json`, `tela.json`, runtime | ATIVO | ADR-0008 | COMPROVADA por indice ADR linha 38 e ADR-0008 localizada | `contrato_tela_json`, contratos JSON | `config/`, `tela/loader.py` | duplicada em `docs/INDICE.md` linhas 114-116 | NAO_CONFIRMADO | NAO_ENCONTRADO | NAO_VERIFICAVEL | definir se politica fica no glossario ou contrato/ADR | linhas 29-55 |
| NOM-LEV-004 | 0, linhas 57-87 | Politica estrutural e tela inicial real | TERMO | motor compartilhado, demo, produto real, orquestrador | RESERVADO | ADR-0021, ADR-0022 | COMPROVADA por indice ADR linhas 51-52 | `contrato_tela_json`, `contrato_cabecalho`, `contrato_barra_de_menus` | `demo/`, `config/telas/demo/` | `demo/` existe embora texto diga futuro em linha 62 | estados futuros/reservados misturados com termos | NAO_ENCONTRADO | NAO_VERIFICAVEL | confirmar tratamento de termos reservados | linhas 57-87 |
| NOM-LEV-005 | 0, linhas 89-105 | Status de artefatos JSON | STATUS_TRANSITORIO | `layout_dado`, `layout_menu`, `lancador.json`, `layout_console` | TRANSITORIO | ADR-0008, ADR-0021, ADR-0022 | COMPROVADA | contratos JSON e contratos de componente | arquivos em `config/` | duplicacao com `docs/INDICE.md` estrutura esperada | status de migracao misturado com nomenclatura | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir onde registrar inventario de status | linhas 89-105 |
| NOM-LEV-006 | 1, linhas 109-233 | Estilo universal | SCHEMA | borda, chip, indicadores, `tiling`, `cor_inativo`, `cor_alerta` | ATIVO | ADR-0004, ADR-0011, ADR-0013, ADR-0014 | COMPROVADA por contratos e indice ADR | `contrato_estilo`, `contrato_chip`, `contrato_composicao_corpo` | `config/estilo.json`, renderer | aliases de arranjo tambem em contratos | alias transicional e valores pendentes | NAO_ENCONTRADO | NAO_VERIFICAVEL | definir propriedade unica de aliases | linhas 109-233 |
| NOM-LEV-007 | 2, linhas 234-327 | Estrutura base de tela e `tela.json` | SCHEMA | `cabecalho`, `corpo`, `barra_de_menus`, `console`, `lancador`, `dashboard`, `tela.json` | ATIVO | ADR-0007, ADR-0008, ADR-0019 | COMPROVADA | `contrato_tela_json`, contratos JSON | `tela/loader.py`, `tela/modelo.py` | duplicado em contratos JSON | exemplo de processamento e fora de escopo no mesmo bloco | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir fronteira entre glossario e contrato de tela | linhas 234-327 |
| NOM-LEV-008 | 3, linhas 328-358 | Eixos de composicao por classe | DISTINCAO_TERMINOLOGICA | tipo de conteudo, exibicao, dashboard, arranjo, paginacao, filtro, selecao | ATIVO | ADR-0001, ADR-0010, ADR-0011 | COMPROVADA | `contrato_composicao_corpo`, `contrato_tela_json` | loader/modelo/renderizador | repetido em contratos de corpo e tela minima | inclui algoritmo remetido a 8.3 | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir granularidade de leitura por modulo | linhas 328-358 |
| NOM-LEV-009 | 4.0, linhas 359-398 | Console como container e selecao | TERMO | cursor, grupo, selecao, lote | ATIVO/PENDENTE | sessao declarada | PARCIAL: contrato_console consome; origem usuario declarada no documento | `contrato_console`, `contrato_barra_de_menus` | `tela/modelo.py`, `tela/renderizador.py` | termos tambem em chip/barra | relacao `[#]` x `[ ]` adiada | NAO_ENCONTRADO | NAO_VERIFICAVEL | confirmar relacao filtro/selecao | linhas 359-398 |
| NOM-LEV-010 | 4.1-4.4, linhas 399-531 | Navegacao e layout de console | REGRA_COMPORTAMENTAL | `[✥]`, wrap toroidal, `ec`, `tg`, `tx`, `layout_console.json` | ATIVO/PENDENTE | ADR-0005, sessao declarada | COMPROVADA para ADR-0005; NAO_CONFIRMADO para sessoes | `contrato_console`, `contrato_composicao_corpo`, `contrato_chip` | renderer/testes | regras repetidas em contratos | pendencia de ajuste de `tx`; artefato futuro/transicional | NAO_ENCONTRADO | NAO_VERIFICAVEL | confirmar destino de algoritmo e pendencia | linhas 399-531 |
| NOM-LEV-011 | 5, linhas 532-682 | `barra_de_menus`, chips e distribuicao | CONTEUDO_MISTO | chips canonicos, especificos, horizontal_responsiva, `[Esc]`, `[V]` | ATIVO/PENDENTE | ADR-0012, ADR-0014, ADR-0022 | COMPROVADA | `contrato_barra_de_menus`, `contrato_chip`, `contrato_json_barra_de_menus` | `config/elementos/barra_de_menus.json`, demo/testes | duplicacao extensa em contratos de barra/chip | estrutura `aciona processo` pendente | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir propriedade de ordem e chips | linhas 532-682 |
| NOM-LEV-012 | 6, linhas 683-825 | Layout, largura, redimensionamento, largura do `lancador` | CONTEUDO_MISTO | SIGWINCH, ioctl, quadro minimo, `area_lancador_w` | ATIVO | ADR-0017, ADR-0023 | COMPROVADA | `contrato_tela_json`, `contrato_lancador`, `contrato_composicao_corpo` | `demo/demo.py`, `tela/renderizador.py`, testes TTY | termos repetidos em contratos e codigo | regra e glossario no mesmo bloco | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir se politica operacional fica no glossario | linhas 683-825 |
| NOM-LEV-013 | 7, linhas 826-892 | Cabecalho | SCHEMA | `titulo`, `descricao`, `max_caracteres`, `cabecalho.json` | ATIVO | ADR-0022 | COMPROVADA | `contrato_cabecalho`, `contrato_json_cabecalho` | `config/elementos/cabecalho.json` | duplicado em contrato cabecalho | caminho transicional | NAO_ENCONTRADO | NAO_VERIFICAVEL | confirmar fronteira schema x contrato | linhas 826-892 |
| NOM-LEV-014 | 8, linhas 893-986 | Corpo tipo `lancador` | ALGORITMO | fila, matriz, vaos, colunas, `lancador.json` | ATIVO/TRANSITORIO | ADR-0001, ADR-0002, ADR-0003 | COMPROVADA | `contrato_lancador`, `contrato_json_lancador`, `contrato_composicao_corpo` | `tela/renderizador.py`, `config/elementos/lancador.json` | duplicado em contratos | campos de navegacao pendentes | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir destino de algoritmo | linhas 893-986 |
| NOM-LEV-015 | 9, linhas 987-1045 | `dashboard` | CONTEUDO_MISTO | dashboard, marcadores, campos de resumo, Total | ATIVO/PENDENTE | ADR-0006, ADR-0008, ADR-0019 | COMPROVADA | `contrato_json_dashboard`, `contrato_composicao_corpo` | configs demo | exemplo/instancia junto de definicao universal | alinhamento pendente; draft de instancia | NAO_ENCONTRADO | NAO_VERIFICAVEL | separar definicao universal de instancia raiz | linhas 987-1045 |
| NOM-LEV-016 | 10, linhas 1049-1072 | Tiling | REGRA_COMPORTAMENTAL | `tiling`, `corpo.arranjo`, `posicao_dashboard`, `[⇆]` | ATIVO/PENDENTE | ADR-0010, ADR-0011, ADR-0015 | COMPROVADA | `contrato_composicao_corpo`, `contrato_tela_json` | renderer/modelo | duplicado em contratos | pendencia horizontal + dashboard | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir tratamento de pendencia | linhas 1049-1072 |
| NOM-LEV-017 | 11, linhas 1074-1101 | Pendencias em aberto | PENDENCIA | `tx`, `popup_execucao`, dashboard, estilos de exibicao, navegacao | PENDENTE | usuario/sessao declarada | NAO_CONFIRMADO fora do proprio documento para varios itens | contratos relacionados variam | issues/backlog nao contem esses itens | duplicacao parcial em contratos como pendencias DOC | pendencias explicitamente misturadas | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir se pendencias saem do glossario | linhas 1074-1101 |
| NOM-LEV-018 | 11, linhas 1103-1130 | Levantamento Codex de legado | LEVANTAMENTO_HISTORICO | `teste_classe_c.py`, `teste_combo.py`, legado, wrap | HISTORICO | levantamento do Codex | CONVERSA_DECLARADA_NO_DOCUMENTO; arquivos citados nao localizados neste repo | NAO_CONFIRMADO | relatorios historicos | origem historica no glossario | historico e itens adiados | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir destino de levantamento historico | linhas 1103-1130 |
| NOM-LEV-019 | 12, linhas 1132-1142 | ADRs aceitas iniciais | DECISAO_DE_ADR | ADR-0001 a ADR-0004 | HISTORICO/ATIVO | ADRs | COMPROVADA no indice ADR | contratos estilo/composicao | ADRs | duplicado no indice ADR | lista parcial de ADRs dentro do glossario | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir se listas de ADRs permanecem no glossario | linhas 1132-1142 |
| NOM-LEV-020 | 13, linhas 1146-1215 | Decisao terminologica `lancador` | TERMO_DESCONTINUADO | `lancador`, `menu`, `tela_destino` | ATIVO/DESCONTINUADO | decisao 2026-07-06; ADR-0006/0008/0021 | COMPROVADA parcialmente por contratos | `contrato_lancador`, `contrato_json_lancador` | configs demo/testes | termos antigos ainda aparecem em ADRs historicas | status historico e conclusoes DOC | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir tratamento de historico de renomeacao | linhas 1146-1215 |
| NOM-LEV-021 | 14, linhas 1216-1287 | Composicao hierarquica | REGRA_COMPORTAMENTAL | corpo, grupo, profundidade, distribuicao, fracao | ATIVO | ADR-0015, ADR-0019 | COMPROVADA | `contrato_composicao_corpo`, `contrato_tela_json`, `contrato_json_tela_minima` | loader/modelo/renderizador | regras extensas duplicadas em contrato | NAO_CONFIRMADO | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir onde regra completa reside | linhas 1216-1287 |
| NOM-LEV-022 | 14.1-14.2, linhas 1288-1370 | Ausencia de distribuicao e espaco externo | DISTINCAO_TERMINOLOGICA | `ocupacao_vertical_terminal`, `corpo.distribuicao`, DA-01 a DA-04 | ATIVO | ADR-0018, ADR-0024 | COMPROVADA por indice ADR linhas 48 e 54 | `contrato_composicao_corpo`, `contrato_tela_json` | renderer/testes | duplicado em contratos e relatorios QA | substituicoes parciais de ADRs | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir destino de regras derivadas | linhas 1288-1370 |
| NOM-LEV-023 | 15, linhas 1371-1447 | `grupo` livre/matriz | SCHEMA | `estrutura`, `livre`, `matriz`, coordenada explicita | ATIVO | ADR-0020 | COMPROVADA | `contrato_composicao_corpo`, `contrato_tela_json`, `contrato_json_tela_minima` | loader/modelo/renderizador | duplicado em contratos | termos invalidos no glossario | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir separacao de invalidos/desaconselhados | linhas 1371-1447 |
| NOM-LEV-024 | 16, linhas 1448-1534 | Distribuicao matricial | SCHEMA | `distribuicao_matricial`, formacao, margem, vao, nivel unico | ATIVO | ADR-0025 | COMPROVADA | contratos JSON dashboard/console/lancador, `contrato_tela_json` | `tela/distribuicao_matricial.py`, configs demo H-0035 | duplicado em contratos e codigo | fora de escopo listado | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir leitura seletiva por elemento | linhas 1448-1534 |
| NOM-LEV-025 | 17, linhas 1535-1615 | JSON externo de conteudo para console | CONTEUDO_MISTO | JSON estrutural, JSON externo, conteudo multinivel, produtor | ATIVO/DEFERIDO | ADR-0026 | COMPROVADA | `contrato_console`, `contrato_json_console`, `contrato_tela_json` | `demo/demo.py`, fixtures demo | duplicado em contratos e handoff H-0036 | decisoes deferidas dentro da secao | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir destino de decisoes futuras | linhas 1535-1615 |
| NOM-LEV-026 | 18, linhas 1618-1718 | Carregamento conjunto | CONTEUDO_MISTO | ponto de entrada, associacao externa, fixture, schema semantico | ATIVO/DEFERIDO | ADR-0027 | COMPROVADA | `contrato_json_console`, `contrato_tela_json`, `contrato_console` | `demo/demo.py`, `tela/loader.py` | duplicado em contratos e H-0036 | decisoes deferidas | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir local de protocolo futuro | linhas 1618-1718 |
| NOM-LEV-027 | 19.1-19.6, linhas 1721-1804 | Apresentacoes multinivel e modos | CONTEUDO_MISTO | modo nao verboso, modo verboso, folha, campo, `modo normal` | ATIVO/DEFERIDO | ADR-0028 | COMPROVADA | `contrato_console`, `contrato_json_console`, `contrato_barra_de_menus` | `demo/teste_demo_console_modos.py`, `tela/loader.py` | conflito/equivalencia registrada com `modo normal` | diferencas nao resolvidas e decisoes deferidas | NAO_ENCONTRADO | NAO_VERIFICAVEL | reconciliacao terminologica | linhas 1721-1804 |
| NOM-LEV-028 | 19.7, linhas 1806-1856 | Politica de modo por tela D23 | SCHEMA | `politica_modo`, `somente_verboso`, `somente_nao_verboso`, `alternavel`, `modo_inicial` | ATIVO/DEFERIDO | ADR-0028 D23 | COMPROVADA | contratos console/barra/tela/json_console | configs e testes H-0037 | duplicado em contratos/codigo | estrategia de migracao legada adiada | NAO_ENCONTRADO | NAO_VERIFICAVEL | decidir migracao de telas legadas | linhas 1806-1856 |

## 6. Inventário terminológico

| Termo literal | Definição localizada | Arquivo e seção | Definições adicionais encontradas | Proprietário atual comprovado | Contrato normativo relacionado | ADR de origem | Estado | Conflito ou duplicação | Observação |
| ------------- | -------------------- | --------------- | --------------------------------- | ----------------------------- | ------------------------------ | ------------- | ------ | ---------------------- | ---------- |
| `docs/NOMENCLATURA.md` | Schema e semantica de campos; nao guarda valores concretos | `NOMENCLATURA.md` §0 | `docs/INDICE.md` define fonte de verdade dos nomes | proprio documento; indice | varios contratos | ADR-0008 | ATIVO | responsabilidades tambem em contratos | regra de origem precisa decisao futura se houver divisao |
| `config/estilo.json` | biblioteca global de aparencia | §0, §1 | contrato_estilo | `contrato_estilo.md` | contrato_estilo | ADR-0008/0021 | ATIVO | NAO_CONFIRMADO | arquivo existe |
| `tela.json` | declaracao concreta da tela | §0, §2.2 | `contrato_tela_json.md` | contrato_tela_json | contrato_tela_json | ADR-0008/0009 | ATIVO | termo generico x caminhos concretos | caminhos concretos dependem de ADR-0021/0022 |
| `barra_de_menus` | regiao fixa inferior/lista declarada de chips | §2, §5 | contratos barra/chip/json_barra | contrato_barra_de_menus | contrato_barra_de_menus | ADR-0012/0014 | ATIVO | antigo `menu` causa ambiguidade historica | termo usado no codigo/config |
| `menu` | antigo nome do corpo tipo `lancador` | §13 | ADR-0001 a 0003 usam historicamente `menu` | contrato_lancador para substituto | contrato_lancador | ADR-0006/decisao 2026-07-06 | DESCONTINUADO | ainda aparece em ADRs historicas e nomes de arquivos transicionais | nao decidir remocao |
| `lancador` | membro do corpo; navegacao para telas via `tela_destino` | §2.1, §8, §13 | contrato_lancador | contrato_lancador | contrato_lancador/json_lancador | ADR-0001/0002/0003/0005/0023 | ATIVO | tambem usa chip interno, distinto de chip da barra | contem algoritmos e schema |
| `dado` | antigo tipo preservado pelo `console` | §2.1, §0 status | ADR-0006 | contrato_console para substituto | contrato_console | ADR-0006 | DESCONTINUADO | `layout_dado.json` transicional | nao fonte canonica |
| `console` | corpo interativo/navegavel generico | §2.1, §4, §17-19 | contrato_console/json_console | contrato_console | contrato_console/json_console | ADR-0006/0026/0027/0028 | ATIVO | regras repetidas em contrato e codigo | consome conteudo externo |
| `Info` | antigo `dashboard` | §2.1, ADR-0006 | ADR-0006 | contrato_json_dashboard para substituto | contrato_json_dashboard | ADR-0006 | DESCONTINUADO | NAO_CONFIRMADO | historico |
| `dashboard` | saida passiva formatada; elemento funcional | §2.1, §9 | contrato_json_dashboard/composicao | contrato_json_dashboard e composicao | contrato_json_dashboard | ADR-0008/0010/0019 | ATIVO | secao 9 contem draft de instancia raiz | alinhamento pendente |
| `posicao_dashboard` | eixo separado descontinuado | §3, §10 | contrato_json_dashboard e tela_minima | contrato_json_dashboard | contrato_json_dashboard | ADR-0010 | DESCONTINUADO | ainda aceito por compatibilidade | migracao futura NAO_CONFIRMADA |
| `tiling` | preferencia global de arranjo | §1.4, §10 | contrato_estilo/composicao | contrato_estilo/composicao | contrato_estilo | ADR-0011 | ATIVO | nao confundir com redimensionamento | aliases transicionais |
| `sobreposto` | alias transicional de `vertical` | §1.4, §10 | contratos e handoffs H-0019/H-0021 | contrato_composicao_corpo | contrato_composicao_corpo | ADR-0011 | TRANSITORIO | usado em testes/handoffs | nao termo final |
| `lado_a_lado` | alias transicional de `horizontal` | §1.4, §10 | contratos e handoffs H-0019/H-0021 | contrato_composicao_corpo | contrato_composicao_corpo | ADR-0011 | TRANSITORIO | usado em testes/handoffs | nao termo final |
| `corpo.arranjo = "horizontal"` | composicao horizontal dos filhos | §5, §10, §14.1 | contrato_composicao_corpo/tela_json | contrato_composicao_corpo | contrato_composicao_corpo | ADR-0011/0015 | ATIVO | nao confundir com barra horizontal | termo especifico completo |
| `barra_de_menus.distribuicao = "horizontal"` | alias transitório de distribuicao responsiva | §5 | contrato_barra_de_menus/tela_json | contrato_barra_de_menus | contrato_barra_de_menus | ADR-0014 | TRANSITORIO | valor concreto igual a `horizontal` em outro dominio | precisa termo completo |
| `barra_de_menus.distribuicao.modo = "horizontal_responsiva"` | forma canonica futura | §5 | contrato_barra_de_menus | contrato_barra_de_menus | contrato_barra_de_menus | ADR-0014 | RESERVADO/ATIVO | formato futuro pendente em contratos | nao confundir com linha unica |
| `ocupacao_vertical_terminal` | preenchimento da altura disponivel | §1.4, §6.2, §14.1 | contrato_composicao_corpo/tela_json | contrato_composicao_corpo/tela_json | contrato_tela_json | ADR-0013 | ATIVO | nao confundir com arranjo vertical | termo especifico |
| `cor_inativo` | cor de estado inativo | §1.5 | contrato_estilo/chip/barra | contrato_estilo | contrato_estilo | ADR-0004 | ATIVO | valores concretos nao decididos no glossario | schema sem valor |
| `cor_alerta` | cor de limite/alerta | §1.5 | contrato_estilo | contrato_estilo | contrato_estilo | ADR-0004 | ATIVO | valores concretos nao decididos | schema sem valor |
| `cursor` / `selecionado` | item apontado por navegacao | §4.0 | contrato_console/chip | contrato_console | contrato_console | ADR-0005 parcialmente | ATIVO | `selecionado` tambem indicador visual | NAO_CONFIRMADO para origem completa |
| `grupo` | origem/categoria do dado; tambem no corpo e matriz como no estrutural | §4.0, §14, §15 | contrato_composicao_corpo | contrato_composicao_corpo | contrato_composicao_corpo | ADR-0015/0019/0020 | ATIVO | termo usado em dois dominios: dado e no estrutural | requer contexto |
| `selecao` | conjunto nomeado de elementos | §4.0 | contrato_console/chip/barra | contrato_console | contrato_console | NAO_CONFIRMADO | ATIVO | relacao com filtro adiada | origem declarada como sessao |
| `lote` | unidade de execucao derivada de selecao | §4.0 | contratos console/barra | contrato_console | contrato_console | NAO_CONFIRMADO | ATIVO | explicitamente nao sinonimo de grupo/selecao | uso normativo depende de processo futuro |
| `ec`, `tg`, `tx` | partes de item de console | §4.2 | contrato_console/composicao | contrato_console | contrato_console | NAO_CONFIRMADO | ATIVO/PENDENTE | `tx` tem ajuste pendente | regra e schema |
| `[✥]` | dica visual de navegacao por setas | §4.1, §5.1 | contrato_barra/chip/console | contrato_chip/barra/console | contratos chip/barra/console | ADR-0005 | ATIVO | nao navega lancador/dashboard | simbolo tambem UI |
| `[Esc]` | Sair/Voltar/Limpar conforme estado | §5.1.2 | contrato_barra/chip | contrato_barra_de_menus | contrato_barra_de_menus | NAO_CONFIRMADO/ADR-0022 para tela real | ATIVO | rotulo dinamico | regra comportamental no glossario |
| `[V] Verboso` | alternancia verboso para consoles multinivel alternaveis | §19, §19.7 | contrato_barra/console/json_console | contrato_barra_de_menus e console | contratos barra/console | ADR-0028 | ATIVO | exclusivo de telas alternaveis | codigo/testes consomem |
| `SIGWINCH` | sinal POSIX para resize | §6.2 | contrato_tela_json/demo.py | contrato_tela_json | contrato_tela_json | ADR-0017 | ATIVO | termo tecnico operacional no glossario | implementado em demo |
| `ioctl(TIOCGWINSZ)` | fonte primaria de dimensoes TTY | §6.2 | contrato_tela_json/demo.py | contrato_tela_json | contrato_tela_json | ADR-0017 | ATIVO | NAO_CONFIRMADO | codigo consome |
| `quadro mínimo de terminal pequeno` | estado substituto quando nao cabe | §6.2, §16.2 | contrato_tela_json/lancador/json_* | contrato_tela_json/lancador | varios | ADR-0017/0023/0025 | ATIVO | usado como fallback comum por causas diferentes | nao criar variante concorrente |
| `area_lancador_w` | largura total alocada ao lancador | §6.3 | contrato_lancador/renderizador | contrato_lancador | contrato_lancador | ADR-0023 | ATIVO | nao comparar com coluna_minima sem conversao | regra operacional |
| `lancador_caixa_min_w` | largura minima total da caixa | §6.3 | contrato_lancador | contrato_lancador | contrato_lancador | ADR-0023 | ATIVO | NAO_CONFIRMADO | regra operacional |
| `coluna_minima_content_w` | largura minima de conteudo para coluna valida | §6.3 | contrato_lancador | contrato_lancador | contrato_lancador | ADR-0023 | ATIVO | NAO_CONFIRMADO | regra operacional |
| `popup_execucao` | janela temporaria de saida de execucao | §11 | NAO_CONFIRMADO | NAO_CONFIRMADO | NAO_CONFIRMADO | NAO_CONFIRMADO | PENDENTE | termo usado sem contrato localizado | explicitamente pendente |
| `matriz de grupos` | grade bidimensional de no `grupo` | §15 | contrato_composicao/tela_json | contrato_composicao_corpo | contrato_composicao_corpo | ADR-0020 | ATIVO | nao confundir com matriz do lancador ou distribuicao matricial | contexto obrigatorio |
| `distribuicao_matricial` | grade de participantes imediatos em elemento funcional | §16 | contratos JSON/codigo | contratos JSON | contrato_tela_json/json_* | ADR-0025 | ATIVO | nao confundir com `distribuicao` de area | campo concreto em configs |
| `JSON estrutural da tela` | documento de configuracao da interface | §17-18 | contratos console/tela_json | contrato_tela_json/json_console | contrato_tela_json | ADR-0026/0027 | ATIVO | distinto de JSON externo | termo central |
| `JSON externo de conteúdo` | documento de runtime do console | §17-19 | contrato_json_console/demo | contrato_json_console | contrato_json_console | ADR-0026/0027/0028 | ATIVO | termo duplicado entre secoes 17 e 19 | conteudo externo |
| `conteúdo multinível` | hierarquia declarada explicitamente | §17, §19 | contrato_json_console | contrato_json_console | contrato_json_console | ADR-0026/0027 | ATIVO | nao confundir com distribuicao matricial | termo ativo |
| `folha` | tipo conceitual da ADR-0028 | §19.3 | contrato_json_console registra schema `conteudo` | NAO_CONFIRMADO como nome canonico | contrato_json_console | ADR-0028 | NAO_CONFIRMADO/DEFERIDO | difere de `conteudo` | reconciliacao adiada |
| `campo` | tipo conceitual externo | §19.3 | schema atual `nome_valor` | NAO_CONFIRMADO como nome canonico | contrato_json_console | ADR-0028 | NAO_CONFIRMADO/DEFERIDO | difere de `nome_valor` | reconciliacao adiada |
| `hierarquia_indentada` | apresentacao no contrato externo | §19.3 | schema atual `hierarquia` | NAO_CONFIRMADO como nome canonico | contrato_json_console | ADR-0028 | NAO_CONFIRMADO/DEFERIDO | difere de `hierarquia` | reconciliacao adiada |
| `modo normal` | exibicao compacta em linha unica | §19.4 | contrato_console §6 | contrato_console | contrato_console | anterior a ADR-0028 | ATIVO/HISTORICO | equivalente conceitual a `modo nao verboso`, nao reconciliado | nao decidir prevalencia |
| `modo não verboso` | linha unica com truncamento | §19.2-19.5 | contrato_json_console/console | contratos console/json_console | contratos console/json_console | ADR-0028 | ATIVO | reconciliacao com `modo normal` adiada | nao nome canonico final |
| `politica_modo` | politica por tela no JSON estrutural | §19.7 | contrato_json_console/tela_json/codigo | contrato_json_console/tela_json | contrato_tela_json/json_console | ADR-0028 D23 | ATIVO | campos em codigo e JSON | migracao legada adiada |
| `somente_nao_verboso` | valor de politica de modo | §19.7 | configs H-0037, testes | contrato_json_console | contrato_json_console | ADR-0028 D23 | ATIVO | nao sinonimo automatico de `modo normal` | valor concreto de schema |
| `alternavel` | valor de politica de modo | §19.7 | configs H-0037, testes | contrato_json_console/barra | contrato_json_console | ADR-0028 D23 | ATIVO | exige chip V e modo inicial | valor concreto |

## 7. Rastreamento de consumidores

| Arquivo consumidor | Tipo do artefato | Referência encontrada | Bloco ou termo consumido | Dependência realmente demonstrada | Leitura integral aparentemente exigida | Autoridade do vínculo | Impacto potencial de futura divisão | Evidência |
| ------------------ | ---------------- | --------------------- | ------------------------ | --------------------------------- | -------------------------------------- | --------------------- | ----------------------------------- | --------- |
| `docs/INDICE.md` | indice | `docs/NOMENCLATURA.md` como fonte de verdade | documento inteiro; secao 0 | SIM, ordem de leitura | SIM para fluxo documental inicial | indice | divisao pode exigir atualizar ordem de leitura | linhas 28-46 |
| `docs/contratos/contrato_estilo.md` | contrato | `origem_especificacao: docs/NOMENCLATURA.md#1-estilo-universal` | secao 1 | SIM | NAO, secao 1 e dependencias | contrato | mudanca de secao quebra ancora | linhas 10, 25-26 |
| `docs/contratos/contrato_composicao_corpo.md` | contrato | origem inclui secoes 3, 6, 8, 9, 10 | blocos de corpo/layout/lancador/dashboard/tiling | SIM | PARCIAL, varias secoes | contrato | divisao exigiria mapeamento multiplo | linhas 10, 47 |
| `docs/contratos/contrato_barra_de_menus.md` | contrato | origem secao 5 | barra/chips/distribuicao | SIM | NAO, secao 5 e estilo | contrato | quebra de ancora secao 5 | linhas 10, 39 |
| `docs/contratos/contrato_cabecalho.md` | contrato | origem secao 7 | cabecalho | SIM | NAO | contrato | baixa se houver redirecionamento | linhas 10, 25 |
| `docs/contratos/contrato_lancador.md` | contrato | origem secao 13 | decisao `lancador`; regras do lancador | SIM | PARCIAL, tambem secoes 6/8 | contrato | divisao precisa preservar historico de renomeacao | linhas 10, 36 |
| `docs/contratos/contrato_console.md` | contrato | origem secao 4 e ADR-0008 | console; selecao; modos | SIM | PARCIAL, tambem secoes 17-19 | contrato | console consome multiplos blocos atuais | linhas 10-21, 592-594, 672-673 |
| `docs/contratos/contrato_chip.md` | contrato | origem secao 5 e ADR-0008 | chip, barra, estado dinamico | SIM | PARCIAL, secoes 1.5 e 5 | contrato | divisao precisa preservar dupla dependencia | linhas 10-19, 59, 307 |
| `docs/contratos/contrato_tela_json.md` | contrato | origem ADR-0008; referencia politicas da nomenclatura | tela_json, paths, corpo, barra, dados externos | SIM | PARCIAL | contrato/ADR | varios blocos migrariam juntos | linhas 10-17, 389-401, 676-695 |
| `docs/contratos/contrato_json_console.md` | contrato JSON | referencias a secoes 17, 18 e regras ADR-0028 | JSON externo, schema multinivel, politica_modo | SIM | PARCIAL | contrato | divisao de conteudo externo precisaria dependencia declarada | linhas 483-485, 868-870, 874-988 |
| `docs/adr/INDICE_ADR.md` | indice ADR | registra ADR-0001 a ADR-0028 | autoridade das decisoes citadas | SIM | NAO | indice ADR | se glossario dividir, referencias a ADR permanecem | linhas 29-58 |
| `docs/adr/ADR-0013-ocupacao-vertical-janela-terminal-corpo.md` | ADR | cita `docs/NOMENCLATURA.md` | `ocupacao_vertical_terminal` | SIM | NAO | ADR | mover termo exige preservar rastreabilidade | linhas 13, 185-197 |
| `docs/adr/ADR-0014-barra-horizontal-termos-especificos.md` | ADR | cita `docs/NOMENCLATURA.md` | regra de termo especifico e barra horizontal | SIM | NAO | ADR | mover regra sem redirecionamento pode perder autoridade | linhas 13, 516-521 |
| `docs/handoff/H-0035-distribuicao-matricial-nivel-unico-conteudo-elementos.md` | handoff | referencia `NOMENCLATURA.md` §16.2 | distribuicao_matricial e fallback | SIM | NAO | handoff derivado de ADR | divisao deve preservar consulta operacional | busca `NOMENCLATURA.md` e `§16.2` |
| `docs/handoff/H-0036-fornecimento-externo-dados-console-json-multinivel.md` | handoff | referencia `NOMENCLATURA.md` §17.2 | JSON externo e representacao fisica | SIM | NAO | handoff | divisao de conteudo externo exige dependencia explicita | busca `NOMENCLATURA.md` §17.2 |
| `docs/handoff/H-0037-apresentacao-multinivel-console-alternancia-verbosa.md` | handoff | referencia `NOMENCLATURA.md` e contratos | modo nao verboso, politica_modo, V | SIM | NAO | handoff | dependencias com secoes 19 e contratos | busca H-0037 |
| `tela/renderizador.py` | codigo | comentarios citam `NOMENCLATURA.md 6.3/8.1-8.3` | lancador, quadro minimo | SIM | NAO | codigo/teste | referencias por secao podem ficar obsoletas | linha localizada por `rg`: comentario perto de testes/renderizador |
| `tela/loader.py` | codigo | implementa termos `distribuicao_matricial`, `politica_modo` | secoes 16 e 19 | SIM por nomes de campos | NAO | contratos/ADRs, nao o glossario diretamente | mudanca de nome teria impacto de schema | `rg` em loader |
| `demo/demo.py` | codigo | usa SIGWINCH, ioctl e politica_modo | secoes 6.2 e 19.7 | SIM por termos concretos | NAO | contratos/ADRs | divisao documental nao impacta codigo se schema preservado | `rg` em demo.py |
| `config/telas/demo/*.json` | config | campos `barra_de_menus`, `distribuicao_matricial`, `politica_modo` | secoes 5, 16, 19 | SIM por schema | NAO | contratos JSON | divisao documental requer preservar contratos de schema | `rg` em config/telas/demo |

Classificacao das referencias observadas:

```yaml
referencia_ao_documento_inteiro:
  - docs/INDICE.md
  - multiplos handoffs que listam docs/NOMENCLATURA.md como fonte proibida/consultada
referencia_a_secao:
  - contratos com origem_especificacao para secoes 1, 3, 5, 7, 13
  - handoffs H-0035/H-0036 com secoes 16/17
referencia_a_termo:
  - codigo/config por campos como distribuicao_matricial, politica_modo, barra_de_menus
referencia_a_regra_normativa:
  - contratos de composicao, tela_json, lancador, barra, console
referencia_historica:
  - relatorios de QA e aplicacao documental
referencia_em_relatorio:
  - relatorios de aplicacao/QA de ADR-0013 a ADR-0028 e levantamentos H-0030/H-0035/H-0036/H-0037
```

## 8. Autoridade normativa

| regra | localizacao_no_NOMENCLATURA | origem_tipo | origem_evidencia | contrato_relacionado | adr_relacionada | estado_da_adr | coerencia_entre_fontes | partes_NAO_CONFIRMADAS |
|---|---|---|---|---|---|---|---|---|
| Documento como unica fonte de nomes validos | linhas 15-25 | CONVERSA_DECLARADA_NO_DOCUMENTO | "decisao explicita do usuario nesta sessao" | todos | NAO_CONFIRMADO | NAO_CONFIRMADO | indice repete fonte de verdade | aprovacao externa alem do texto |
| Schema x dados; JSON por tela | §0 linhas 27-56 | ADR | ADR-0008 e indice ADR linha 38 | contrato_tela_json | ADR-0008 | aceita | coerente | nenhuma material sobre ADR |
| JSONs em `config/`, nao `docs/` | §0 linhas 53-55 | ADR/CONTRATO | ADR-0008/INDICE | contrato_tela_json | ADR-0008/0009/0021 | aceita | coerente | NAO_CONFIRMADO sobre todos caminhos futuros |
| Motor `tela/`, demo e produto real separados | §0 linhas 57-72 | ADR | ADR-0021, indice linha 51 | contrato_tela_json | ADR-0021 | aceita | coerente | `demo/` ja existe apesar de texto "futuro" em linha 62 |
| Tela inicial real reservada | §0 linhas 74-87 | ADR | ADR-0022, indice linha 52 | contratos cabecalho/barra/tela_json | ADR-0022 | aceita | coerente | materializacao futura |
| Estilo universal nao hardcoded | §1 linhas 109-233 | CONTRATO/ADR | contrato_estilo e ADR-0004 | contrato_estilo | ADR-0004 | aceita | coerente | valores concretos de cor |
| Aliases de arranjo transicionais | §1.4 e §10 | ADR | ADR-0011, indice linha 41 | contrato_composicao_corpo | ADR-0011 | aceita | coerente | estrategia de migracao completa |
| `[✥]` restrito a console | §4.1/§5.1 | ADR | ADR-0005 | contrato_console/chip/barra | ADR-0005 | aceita | coerente | NAO_CONFIRMADO para todos usos historicos |
| Barra declarativa por tela | §5 | ADR | ADR-0012, indice linha 42 | contrato_barra_de_menus | ADR-0012 | aceita | coerente | chips sempre presentes futuros |
| Alteracao por termo especifico completo | §5 | ADR | ADR-0014, contrato_processo §11 | contrato_processo, contrato_barra | ADR-0014 | aceita | coerente | NAO_CONFIRMADO para todas auditorias antigas |
| Redimensionamento reativo | §6.2 | ADR | ADR-0017, indice linha 47 | contrato_tela_json | ADR-0017 | aceita | coerente | comportamento nao-TTY completo fora de consulta atual |
| Largura minima do lancador | §6.3 | ADR | ADR-0023, indice linha 53 | contrato_lancador | ADR-0023 | aceita | coerente | NAO_CONFIRMADO para todos cenarios de implementacao |
| Composicao hierarquica | §14 | ADR | ADR-0015/0019 | contrato_composicao_corpo | ADR-0015/0019 | aceita | coerente | sincronizacao futura |
| Ausencia de distribuicao nao equivale a `igual` | §14.1 | ADR | ADR-0018, indice linha 48 | contrato_composicao_corpo | ADR-0018 | aceita | coerente no indice atual | arquivo ADR-0018 possui frontmatter `status: proposta`; divergencia factual |
| Proibicao de espaco externo vazio | §14.2 | ADR | ADR-0024, indice linha 54 | contrato_composicao_corpo/tela_json | ADR-0024 | aceita | coerente com indice | NAO_CONFIRMADO para todos JSONs |
| `estrutura: matriz` em grupo | §15 | ADR | ADR-0020, indice linha 50 | contrato_composicao_corpo | ADR-0020 | aceita | coerente | NAO_CONFIRMADO para todos validadores |
| `distribuicao_matricial` | §16 | ADR | ADR-0025, indice linha 55 | contratos JSON | ADR-0025 | aceita e aplicada | coerente | precedencia completa por elemento fora do glossario |
| JSON externo de conteudo | §17 | ADR | ADR-0026, indice linha 56 | contrato_console/json_console/tela_json | ADR-0026 | aceita e aplicada | coerente | protocolo produtor deferido |
| Carregamento conjunto | §18 | ADR | ADR-0027, indice linha 57 | contrato_json_console/tela_json | ADR-0027 | aceita e aplicada | coerente | protocolo Pipeline deferido |
| Apresentacoes e politica de modo | §19 | ADR | ADR-0028, indice linha 58 | contrato_console/json_console/barra | ADR-0028 | aceita e aplicada | coerente | reconciliacao terminologica e migracao legada |

## 9. Conteúdo com responsabilidade documental distinta

| ID | Conteúdo | Localização atual | Responsabilidade documental exercida | Documento que atualmente também trata o tema | Destino candidato no anexo | Destino aprovado | Decisão necessária | Evidência |
| -- | -------- | ----------------- | ------------------------------------ | -------------------------------------------- | -------------------------- | ---------------- | ------------------ | --------- |
| CDIST-001 | Status dos artefatos JSON | §0 linhas 89-101 | inventario/transicao | `docs/INDICE.md`, contratos JSON | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir local de status transitorio | linhas 89-101 |
| CDIST-002 | Caminhos futuros/reservados `orquestrador.py` e `config/telas/orquestrador.json` | §0 linhas 74-87 | planejamento/reserva | ADR-0022, contrato_tela_json | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir tratamento de reservado | linhas 74-87 |
| CDIST-003 | Regras completas de redimensionamento | §6.2 | politica operacional | contrato_tela_json, ADR-0017 | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir se regra completa fica no glossario | linhas 748-785 |
| CDIST-004 | Algoritmo de colunas do lancador | §8.3 | algoritmo | contrato_lancador, contrato_composicao_corpo | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir destino de algoritmo | linhas 935-956 |
| CDIST-005 | Draft de instancia de dashboard raiz | §9 | exemplo/instancia | contrato_json_dashboard | NAO_ENCONTRADO | NAO_CONFIRMADO | separar definicao universal de instancia | linhas 987-1045 |
| CDIST-006 | Pendencias do console/lancador/dashboard | §11 | backlog/issue/decisao pendente | backlog/issues modelos; contratos com pendencias | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir onde pendencias vivem | linhas 1074-1101 |
| CDIST-007 | Levantamento Codex de legado | §11 | historico/levantamento | relatorios de levantamento | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir arquivo historico | linhas 1103-1120 |
| CDIST-008 | Lista de ADRs aceitas ADR-0001 a ADR-0004 | §12 | indice/registro ADR | `docs/adr/INDICE_ADR.md` | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir se duplicar lista | linhas 1132-1142 |
| CDIST-009 | Historico DOC-0008/DOC-0009 em decisao `lancador` | §13 | historico de migracao | relatorios/contrato_lancador | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir preservacao historica | linhas 1193-1215 |
| CDIST-010 | Termos invalidos/desaconselhados de matriz | §15.5 | regra de validacao | contrato_composicao_corpo/tela_json | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir se validacao fica em contrato | linhas 1435-1447 |
| CDIST-011 | Fora de escopo da ADR-0025 | §16.5 | escopo/decisao futura | ADR-0025/contratos JSON | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir local de fora de escopo | linhas 1519-1534 |
| CDIST-012 | Decisoes deferidas ADR-0026 | §17.5 | decisoes futuras | ADR-0026/contratos | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir local das decisoes futuras | linhas 1599-1614 |
| CDIST-013 | Decisoes deferidas ADR-0027 | §18.6 | decisoes futuras | ADR-0027/contratos | NAO_ENCONTRADO | NAO_CONFIRMADO | idem | linhas 1703-1717 |
| CDIST-014 | Diferencas terminologicas nao resolvidas | §19.3-19.4 | conflito/reconciliacao | contrato_console/json_console | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir nome canonico futuro | linhas 1752-1776 |
| CDIST-015 | Itens D23 ainda deferidos | §19.7.5 | estrategia de migracao | ADR-0028/contratos/relatorios QA | NAO_ENCONTRADO | NAO_CONFIRMADO | decidir migracao de legados | linhas 1850-1856 |

## 10. Verificação factual da proposta

Arquivo `PROPOSTA_ORGANIZACAO_NOMENCLATURA.md`: NAO_ENCONTRADO.

| ID da proposta | Afirmação ou agrupamento proposto | Evidência no arquivo atual | Evidência nos consumidores | Resultado factual | Divergência | Decisão necessária |
| -------------- | --------------------------------- | -------------------------- | -------------------------- | ----------------- | ----------- | ------------------ |
| PROP-001 | estimativa de tamanho do arquivo | `docs/NOMENCLATURA.md` tem 1856 linhas | NAO_CONFIRMADO | NAO_VERIFICAVEL quanto a proposta; tamanho atual CONFIRMADO | anexo ausente | decidir se estimativa externa e relevante |
| PROP-002 | responsabilidades atribuidas ao arquivo | arquivo atual declara schema e semantica; tambem contem regras, pendencias, historico e status | contratos consomem secoes especificas | NAO_VERIFICAVEL quanto a proposta | anexo ausente | decidir responsabilidades futuras |
| PROP-003 | ordem de leitura declarada em `docs/INDICE.md` | `NOMENCLATURA.md` e terceiro item da ordem | indice linhas 28-46 | NAO_VERIFICAVEL quanto a proposta; fato atual CONFIRMADO | anexo ausente | decidir se ordem muda |
| PROP-004 | responsabilidade atual de `backlog.md` | backlog e modelo para itens planejados nao iniciados | nao contrato | NAO_VERIFICAVEL quanto a proposta; fato atual CONFIRMADO | anexo ausente | decidir se pendencias migrariam para backlog |
| PROP-005 | responsabilidade atual de `issues.md` | issues registram impedimentos, bugs e decisoes pendentes | nao altera contrato | NAO_VERIFICAVEL quanto a proposta; fato atual CONFIRMADO | anexo ausente | decidir se decisoes pendentes viram issues |
| PROP-006 | correspondencia entre secoes atuais e modulos propostos | secoes 0-19 mapeadas neste levantamento | contratos consomem secoes 1,3,4,5,7,13,16-19 | NAO_VERIFICAVEL | anexo ausente | decidir criterios de modularizacao |
| PROP-007 | existencia dos contratos citados | contratos ativos encontrados em `docs/contratos/` | indice lista contratos ativos | NAO_VERIFICAVEL quanto aos citados pelo anexo | anexo ausente | confirmar lista de contratos dependentes |
| PROP-008 | dependencias sugeridas para cada contrato | dependencias atuais comprovadas por `origem_especificacao` e referencias | tabela de rastreamento | NAO_VERIFICAVEL quanto a sugestao | anexo ausente | decidir declaracao futura de dependencias |
| PROP-009 | presenca de pendencias e historico | confirmado nas secoes 11, 17.5, 18.6, 19.6, 19.7.5 | contratos/relatorios tambem registram pendencias | NAO_VERIFICAVEL quanto ao agrupamento | anexo ausente | decidir tratamento |
| PROP-010 | presenca da lista de ADRs | secao 12 lista ADR-0001 a ADR-0004; indice ADR lista ADR-0001 a ADR-0028 | indice ADR | NAO_VERIFICAVEL quanto a proposta | anexo ausente | decidir se lista parcial permanece |
| PROP-011 | existencia de referencias antigas por secao | consumidores citam secoes especificas | contratos e codigo | NAO_VERIFICAVEL quanto a proposta | anexo ausente | decidir preservacao de ancoras |
| PROP-012 | possibilidade de manter `docs/NOMENCLATURA.md` como fachada sem quebrar referencias | referencias por documento e secao foram localizadas | contratos/codigo/handoffs | NAO_CONFIRMADO | anexo ausente; nao ha decisao aprovada | decidir fachada e redirecionamentos |
| PROP-013 | abrangencia real dos dominios propostos | dominios atuais incluem estilo, tela, corpo, console, barra, layout, cabecalho, lancador, dashboard, tiling, ADRs, pendencias, dados externos | contratos e codigo | NAO_VERIFICAVEL | anexo ausente | decidir escopo dos dominios |
| PROP-014 | termos ou dominios atuais nao cobertos pela proposta | NAO_VERIFICAVEL | NAO_VERIFICAVEL | NAO_VERIFICAVEL | anexo ausente | comparar quando anexo existir |
| PROP-015 | modulos propostos que combinam conteudos com autoridades diferentes | NAO_VERIFICAVEL | NAO_VERIFICAVEL | NAO_VERIFICAVEL | anexo ausente | comparar quando anexo existir |

## 11. Lacunas

```yaml
lacuna_001:
  tema: anexo comparativo
  fato_documental_comprovado: PROPOSTA_ORGANIZACAO_NOMENCLATURA.md nao existe no workspace inspecionado
  impacto: comparacao material da proposta fica NAO_VERIFICAVEL
  evidencia: wc e find sem caminho localizado
```

```yaml
lacuna_002:
  tema: autoridade da regra "unica fonte de nomes"
  fato_documental_comprovado: o proprio documento atribui origem a decisao explicita do usuario em sessao
  impacto: origem externa a conversa/sessao permanece NAO_CONFIRMADO
  evidencia: docs/NOMENCLATURA.md linhas 17-25
```

```yaml
lacuna_003:
  tema: divergencia de status da ADR-0018
  fato_documental_comprovado: indice ADR registra ADR-0018 como aceita; arquivo ADR-0018 contem frontmatter status: proposta
  impacto: autoridade normativa requer conciliacao documental
  evidencia: docs/adr/INDICE_ADR.md linha 48; docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md frontmatter
```

```yaml
lacuna_004:
  tema: referencias por secao
  fato_documental_comprovado: contratos e codigo citam secoes especificas de NOMENCLATURA.md
  impacto: divisao futura pode quebrar ancoras e referencias sem fachada ou mapa
  evidencia: contratos com origem_especificacao; tela/renderizador.py comentario com NOMENCLATURA.md 6.3/8.1-8.3
```

```yaml
lacuna_005:
  tema: termos equivalentes nao reconciliados
  fato_documental_comprovado: modo normal e modo nao verboso sao equivalentes conceitualmente, mas reconciliacao definitiva esta adiada
  impacto: divisao sem decisao pode cristalizar sinonimos concorrentes
  evidencia: docs/NOMENCLATURA.md linhas 1766-1776
```

## 12. Decisões indispensáveis ainda não confirmadas

```yaml
- id: DEC-NOM-001
  tema: divisao ou nao do arquivo
  fato_que_exige_decisao: o arquivo atual acumula 1856 linhas e responsabilidades distintas
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: docs/NOMENCLATURA.md e docs/INDICE.md definem o estado atual
  impacto_da_ausencia: qualquer autoria normativa futura pode mover regra sem autoridade
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: caracterizacao e inventario por bloco
- id: DEC-NOM-002
  tema: criterios de modularizacao
  fato_que_exige_decisao: blocos misturam termo, schema, algoritmo, historico e pendencia
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: NAO_CONFIRMADO
  impacto_da_ausencia: agrupamentos podem combinar autoridades diferentes
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: NOM-LEV-001 a NOM-LEV-028
- id: DEC-NOM-003
  tema: nomes e quantidade de modulos
  fato_que_exige_decisao: anexo nao encontrado; consumidores atuais citam secoes e nao modulos
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: NAO_CONFIRMADO
  impacto_da_ausencia: referencias futuras ficariam instaveis
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: PROP-006 a PROP-015
- id: DEC-NOM-004
  tema: nucleo comum
  fato_que_exige_decisao: regra geral de fonte unica, schema x dados, aliases e politica de termo especifico atravessam varios contratos
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: docs/NOMENCLATURA.md atual
  impacto_da_ausencia: contratos podem precisar ler multiplos blocos para termos comuns
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: secoes 0, 1.4, 5, 14.1
- id: DEC-NOM-005
  tema: permanencia de fachada
  fato_que_exige_decisao: consumidores citam o documento e secoes numeradas
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: NAO_CONFIRMADO
  impacto_da_ausencia: referencias podem quebrar
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: secao 7 deste relatorio
- id: DEC-NOM-006
  tema: leitura inicial obrigatoria
  fato_que_exige_decisao: docs/INDICE.md coloca NOMENCLATURA.md como terceiro item da ordem
  alternativas_ja_documentadas: ordem atual apenas
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: docs/INDICE.md
  impacto_da_ausencia: modularizacao pode contradizer ordem de leitura
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: docs/INDICE.md linhas 28-46
- id: DEC-NOM-007
  tema: leitura seletiva por contrato
  fato_que_exige_decisao: contratos ja citam secoes especificas
  alternativas_ja_documentadas: referencias por origem_especificacao
  alternativas_realmente_aprovadas: estado atual
  autoridade_existente: contratos ativos
  impacto_da_ausencia: cada contrato pode depender de mapa nao documentado
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: contrato_estilo, contrato_barra, contrato_composicao, contrato_console
- id: DEC-NOM-008
  tema: declaracao de dependencias em contratos
  fato_que_exige_decisao: alguns contratos citam NOMENCLATURA.md diretamente; outros citam ADRs/contratos
  alternativas_ja_documentadas: origem_especificacao atual
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: contratos
  impacto_da_ausencia: consumidores podem perder origem terminologica
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: secao 7 deste relatorio
- id: DEC-NOM-009
  tema: propriedade unica dos termos
  fato_que_exige_decisao: termos como grupo, modo normal/nao verboso, dashboard, JSON externo aparecem em varios contextos
  alternativas_ja_documentadas: distincao por contexto
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: contratos e ADRs
  impacto_da_ausencia: duplicacoes podem virar conflitos
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: inventario terminologico
- id: DEC-NOM-010
  tema: regras comportamentais no glossario
  fato_que_exige_decisao: secoes contem algoritmos e regras completas
  alternativas_ja_documentadas: contratos tambem tratam regras
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: contratos/ADRs
  impacto_da_ausencia: regra ativa pode ser movida para documento sem autoridade
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: NOM-LEV-010, NOM-LEV-012, NOM-LEV-014, NOM-LEV-021
- id: DEC-NOM-011
  tema: aliases
  fato_que_exige_decisao: aliases transicionais ainda consumidos
  alternativas_ja_documentadas: manter aliases ate migracao especifica
  alternativas_realmente_aprovadas: ADR-0011/0014 para estado atual
  autoridade_existente: ADR-0011, ADR-0014
  impacto_da_ausencia: alias pode sumir sem redirecionamento
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: sobreposto, lado_a_lado, barra_de_menus.distribuicao="horizontal"
- id: DEC-NOM-012
  tema: pendencias, historico e status transitorio
  fato_que_exige_decisao: arquivo contem secoes de pendencia, historico e status
  alternativas_ja_documentadas: backlog/issues existem como modelos, mas nao contem esses itens
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: docs/backlog.md, docs/issues.md como modelos
  impacto_da_ausencia: pendencia pode ser confundida com regra
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: secoes 9 e 11 deste relatorio
- id: DEC-NOM-013
  tema: estrategia de migracao
  fato_que_exige_decisao: referencias por documento/secao existem em contratos, codigo, handoffs e relatorios
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: NAO_CONFIRMADO
  impacto_da_ausencia: alteracao simultanea de estrutura e semantica
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: rastreamento de consumidores
- id: DEC-NOM-014
  tema: necessidade de ADR
  fato_que_exige_decisao: reorganizacao pode alterar autoridade normativa, referencias e ordem de leitura
  alternativas_ja_documentadas: NAO_CONFIRMADO
  alternativas_realmente_aprovadas: NAO_CONFIRMADO
  autoridade_existente: docs/adr/INDICE_ADR.md regra de ADR
  impacto_da_ausencia: mudanca arquitetural documental pode ocorrer sem registro
  bloqueia_ADR: NAO_CONFIRMADO
  evidencia: docs/adr/INDICE_ADR.md linhas 11-25
```

## 13. Riscos factuais de migração

| Risco factual | Evidência | Superfície afetada |
|---|---|---|
| perda de regra normativa | regras completas de redimensionamento, `lancador`, composicao, JSON externo e politica de modo estao no glossario | contratos, handoffs, codigo |
| definicao duplicada | contratos repetem secoes de `NOMENCLATURA.md` por origem_especificacao | contratos ativos |
| referencia por numero de secao | contratos citam `#1`, `#3`, `#5`, `#7`, `#13`; codigo cita 6.3/8.1-8.3 | contratos/codigo |
| contrato dependente de documento inteiro | `docs/INDICE.md` manda ler NOMENCLATURA.md como fonte de verdade | fluxo documental |
| referencia historica confundida com ativa | levantamento Codex e lista de ADRs dentro do glossario | secao 11 e secao 12 |
| alias sem redirecionamento | `sobreposto`, `lado_a_lado`, `barra_de_menus.distribuicao = "horizontal"` | JSONs, loader, contratos |
| alteracao simultanea de estrutura e semantica | mover blocos com regras e termos sem ADR/contrato | todos contratos consumidores |
| modulo criado sem proprietario inequivoco | termos atravessam contratos: `grupo`, `modo normal`, `JSON externo` | composicao, console, dados externos |
| pendencia transformada em regra | secoes 11, 17.5, 18.6, 19.6, 19.7.5 | backlog/issues/contratos futuros |
| regra ativa movida para documento sem autoridade | regras derivadas de ADRs dentro do glossario | ADRs e contratos |
| fachada incapaz de preservar referencias por secao | consumidores usam secoes numeradas e ancoras markdown | contratos, handoffs, relatorios, codigo |
| dependencia circular | glossario declara contratos derivados; contratos tambem redefinem/repetem regras | NOMENCLATURA.md e contratos |
| modulos que exigiriam leitura conjunta apesar da divisao | barra depende de estilo/chip/console; console depende de dados externos e politica de modo | contratos barra/chip/console/json_console |
| divergencia entre terminologia conceitual e schema concreto | `folha` x `conteudo`, `campo` x `nome_valor`, `hierarquia_indentada` x `hierarquia`; `modo normal` x `modo nao verboso` | ADR-0028, contrato_console/json_console |
| divergencia de status de ADR | ADR-0018 no indice como aceita, arquivo com `status: proposta` | autoridade normativa de §14.1 |

## 14. Síntese factual

CONFORME:

- `docs/NOMENCLATURA.md` e arquivo central de terminologia, schema e regras conforme sua propria regra declarada.
- O arquivo tambem exerce responsabilidades de contrato auxiliar, historico, backlog de pendencias, status transitorio, indice parcial de ADR e registro de decisoes deferidas.
- Contratos ativos consomem secoes especificas do arquivo, nao apenas o documento inteiro.
- Handoffs, relatorios, codigo e configs consomem termos concretos definidos ou estabilizados no arquivo.

NAO_CONFORME / divergencia factual:

- `PROPOSTA_ORGANIZACAO_NOMENCLATURA.md` esta NAO_ENCONTRADO.
- O indice ADR registra ADR-0018 como aceita, mas o arquivo `docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md` foi encontrado com frontmatter `status: proposta`.

NAO_CONFIRMADO:

- Qualquer destino futuro de bloco.
- Qualquer estrutura final aprovada.
- Qualquer nome, quantidade de modulos, fachada ou estrategia de migracao.
- Qualquer autoridade externa ao proprio documento para decisoes declaradas como "sessao" ou levantamento.

## 15. Estado Git

Comando executado antes da criacao do relatorio:

```bash
git status --short
```

Saida:

```text

```

Comandos a registrar apos a criacao do relatorio:

```bash
git status --short
git diff -- docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
```

Saida de `git status --short` apos criacao:

```text
?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
```

Saida de `git diff -- docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md` apos criacao:

```text

```

Observacao factual: o arquivo esta nao rastreado; por isso `git diff -- <arquivo>` nao exibiu diff.

## 16. Encerramento

```yaml
etapa_executada: LEVANTAMENTO_DOCUMENTAL
artefato_principal_analisado: docs/NOMENCLATURA.md
anexo_comparativo: PROPOSTA_ORGANIZACAO_NOMENCLATURA.md
relatorio_criado: docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
estrutura_final_aprovada: false
adr_criada: false
arquivos_normativos_alterados: false
decisoes_materiais_abertas: true
status_literal: LEVANTAMENTO_DOCUMENTAL_CONCLUIDO
proxima_categoria: DECISAO_DO_USUARIO
```
