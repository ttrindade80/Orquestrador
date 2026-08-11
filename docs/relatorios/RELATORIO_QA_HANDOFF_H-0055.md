status: H2_HANDOFF_PATCH_REQUIRED
handoff: H-0055
etapa: QA_HANDOFF
achados:
  - id: QA-H0055-001
    requisito_violado: "D-MULTI-09 e contrato_console.md §22.16 exigem exatamente um filho escolhido por pai em todo estado válido."
    evidencia_focal: "H-0055 §2.1 e §4 exigem exatamente um filho por pai, mas deixam a inicialização como condição a verificar e determinam parar apenas se a infraestrutura não conseguir estabelecer o estado."
    impacto: "Fixture, testes e demonstração não têm estado inicial válido fechado; a implementação pode introduzir decisão nova ou deixar pai sem escolha."
    correcao_necessaria: "Fechar documentalmente a materialização do estado inicial obrigatório usando somente autoridades vigentes, ou registrar o bloqueio objetivo antes da implementação, sem criar política de inicialização nova."
  - id: QA-H0055-002
    requisito_violado: "D-MULTI-08, D-MULTI-09 e contrato_console.md §23.4 exigem retorno contextual por Esc sem violar a escolha obrigatória nem criar cancelamento novo."
    evidencia_focal: "H-0055 §3.2 e §8.1 fecham Esc apenas no retorno do nível dos filhos e deixam o nível dos pais sob regras transversais; §23.4 limpa seleção ativa por Esc, enquanto D-MULTI-09 exige uma escolha por pai."
    impacto: "A compatibilidade declarativa com multipla pode limpar escolhas e produzir pai sem escolha; suprimi-la sem fechamento criaria semântica de cancelamento ou retorno não delimitada."
    correcao_necessaria: "Fechar o despacho contextual de Esc nos dois níveis em conformidade simultânea com D-MULTI-08, D-MULTI-09 e §23.4, sem introduzir cancelamento, Enter ou ação nova."
  - id: QA-H0055-003
    requisito_violado: "contrato_console.md §3 e §8 e contrato_json_console.md §5 exigem politica_selecao; tg e o chip de seleção vigentes dependem da declaração multipla."
    evidencia_focal: "H-0055 §4 trata politica_selecao: multipla como condicional, embora a fixture precise reutilizar tg e o Espaço de seleção existente."
    impacto: "A fixture pode ser inválida ou deixar indefinida a compatibilidade declarativa necessária, confundindo o mecanismo fechado com política alternativa."
    correcao_necessaria: "Fechar nominalmente na fixture a declaração existente compatível, incluindo politica_selecao: multipla ao reutilizar tg/[␣], sem criar enum, schema ou política nova."
  - id: QA-H0055-004
    requisito_violado: "D23 e contrato_json_console.md §13.13.1–§13.13.6 exigem formato.excesso.politica_modo e, quando alternavel, formato.excesso.modo_inicial em tela nova ou revisada."
    evidencia_focal: "H-0055 §3.2 apenas preserva modos; §4 não fecha na fixture estrutural a declaração D23 nem o modo inicial."
    impacto: "A fixture nova pode violar o contrato e não torna reproduzíveis os testes de modo e redimensionamento; a declaração permanece aberta para inferência."
    correcao_necessaria: "Materializar na fixture estrutural combinação D23 válida e requisitos de modo inicial/alternância, preservando modo normal × modo não verboso e sem renomear hierarquia."
  - id: QA-H0055-005
    requisito_violado: "ADR-0041 D-PGU-01–D-PGU-03 e H-0055 §9 exigem demonstração executável de PageUp/PageDown e [PgUp][PgDn] Páginas quando a demonstração inclui paginação."
    evidencia_focal: "H-0055 §3.3 e §6 subordinam paginação à ADR-0041, mas §4 deixa sua declaração condicional e não fecha politica_paginacao nem conteúdo suficiente para páginas múltiplas, embora §9 exija regressão visível de paginação."
    impacto: "python demo/demo.py h0055_dois_niveis_por_foco não tem garantia documental de exercitar PageUp/PageDown e [PgUp][PgDn] Páginas; testes e demonstração ficam não reproduzíveis."
    correcao_necessaria: "Fechar na fixture declaração de paginação e quantidade nominal de conteúdo suficiente para exercitar PageUp/PageDown, preservando ADR-0041 e sem paginação concorrente."
