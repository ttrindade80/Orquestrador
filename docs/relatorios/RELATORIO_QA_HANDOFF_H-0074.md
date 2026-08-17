# Relatório QA de Handoff — H-0074

status: H2_HANDOFF_PATCH_REQUIRED

## Escopo auditado

ADR-0048, contratos e nomenclatura estão coerentes quanto a `filho_default`,
baseline/candidato, separação do JSON externo, ausência de persistência,
preservação visual e de navegação, e exclusão factual de H-0063: `demo.py` não
cataloga H-0063, enquanto `tela/estilo.py` projeta a árvore a partir de
`preset_default`. `NoConteudo.campos` realmente preserva o campo integralmente.
Não há antecipação de H-0075, ITEM-0023 ou ITEM-0024.

## Achados

### QA-H0074-001 — validação limitada ao ponto de entrada da demo

- Requisito: a validação deve cobrir a carga real de todo consumidor da
  estrutura, sem depender exclusivamente da demonstração.
- Evidência focal: `tela/carregamento/conteudo_externo.py:645-697` valida
  somente o schema genérico e declara não associar tela e conteúdo;
  `tela/modelo.py:396` recebe conteúdo já validado e não revalida a estrutura;
  o handoff determina a única chamada em `demo/demo.py::_carregar_modelo_por_id`
  (§6.1, linha 234), embora `tela/navegacao.py` seja módulo de navegação pura.
- Impacto: a localização em `navegacao.py` e a chamada pela demo são escolha
  arquitetural nova, não consequência necessária comprovada. Modelos obtidos
  por outro caminho podem alcançar seleção/navegação sem validação de
  `filho_default`, inclusive com fallback.
- Correção necessária: fechar no handoff uma fronteira comum de correlação e
  listar todos os consumidores/caminhos que a invocam, autorizando os arquivos
  materialmente necessários. Não escolher alternativa nesta QA.

### QA-H0074-002 — fallback posicional preservado

- Requisito: ausência ou invalidade nunca pode produzir escolha pelo primeiro
  filho.
- Evidência focal: `tela/navegacao.py:669-687` mantém
  `next(..., filhos[0][0])`; o handoff reconhece esse caminho (§5.1), mas o
  torna opcional (§6.1). A futura alteração de
  `tela/selecao.py::_reconciliar_ids_dois_niveis` não elimina esse fallback.
- Impacto: estado sem seleção válida pode mascarar dado inválido e posicionar
  o cursor no primeiro filho, contrariando ADR-0048.
- Correção necessária: o handoff deve exigir a remoção ou uma guarda não
  posicional para todo caminho de entrada, com teste explícito de estado ausente.

### QA-H0074-003 — fixture aplicável não enumerada

- Requisito: enumerar todas as fixtures reais sujeitas ao schema.
- Evidência focal: `demo/demo.py:247-268` registra conteúdo externo para H-0055
  e também para `h0072_formatacao_generica_dois_niveis_por_foco`, descrito no
  próprio código como cenário de formatação de `dois_niveis_por_foco`. O
  handoff declara H-0072 fora da lista (§6.3 e §8), embora a obrigatoriedade de
  `filho_default` não dependa da apresentação.
- Impacto: a futura validação pode rejeitar ou deixar sem baseline uma fixture
  real catalogada, quebrando a cobertura nominal do schema.
- Correção necessária: enumerar H-0072 e fechar sua reconciliação ou uma
  exclusão baseada na estrutura efetiva; não alterar a fixture nesta QA.

### QA-H0074-004 — evidência de teste e demonstração incompleta

- Requisito: provar duplicidade/ambiguidade quando aplicável e provar ausência
  de escrita.
- Evidência focal: §7.3 delega duplicidade a
  `estrutura_dois_niveis_valida`, mas os testes H-0055 listados não exercitam
  ID duplicado; §11 apenas afirma que o arquivo não será reescrito, sem
  procedimento observável de comparação antes/depois.
- Impacto: não há prova executável completa para dois critérios obrigatórios.
- Correção necessária: acrescentar teste negativo de identidade duplicada e
  um passo reproduzível, somente leitura, de digest/conteúdo antes e depois da
  demonstração.

Os demais itens de escopo, arquivos nominais, fixtures H-0055 e fronteiras
documentais foram considerados coerentes, condicionados às correções acima.
