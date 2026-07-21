# Relatório de QA — ADR-0029

## 1. Identificação

```yaml
etapa_executada: QA_ADR
artefato_auditado: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_novo_criado: docs/relatorios/RELATORIO_QA_ADR-0029.md
papel_exercido: auditor documental independente
data_execucao: 2026-07-20
```

## 2. Objetivo e limites

Objetivo: auditar conformidade, autoridade, coerência e completude documental da ADR-0029 contra o conjunto fechado D-NOM-01 a D-NOM-16.

Limites cumpridos:

- A ADR não foi corrigida.
- A ADR não foi aplicada.
- Nenhum módulo de nomenclatura foi criado.
- Nenhum handoff foi criado.
- Nenhum stage ou commit foi preparado.
- A proposta externa não foi usada como fonte documental.

## 3. Estado Git inicial

```text
branch: master
HEAD: c90349c feat: implementa apresentacoes multinivel com modos por tela
status_short:
  ?? docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
cached_name_only: vazio
```

## 4. Autoridades consultadas

Autoridades lidas integralmente:

- `docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md`
- `docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md`
- `docs/NOMENCLATURA.md`
- `docs/INDICE.md`
- `docs/backlog.md`
- `docs/issues.md`
- `docs/adr/INDICE_ADR.md`

Autoridades consultadas seletivamente:

- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_cabecalho.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_chip.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_json_console.md`
- ADRs anteriores citadas na seção 9 da ADR-0029, nos trechos necessários para validar as relações declaradas.

## 5. Estado factual de entrada

CONFORME: `docs/NOMENCLATURA.md` possui 1856 linhas, confirmado por `wc -l`.

CONFORME: o levantamento registra mistura de responsabilidades no monólito: terminologia, schemas, regras comportamentais, algoritmos, aliases, pendências, histórico, decisões deferidas e estados transitórios.

CONFORME: `docs/INDICE.md` ainda exige `docs/NOMENCLATURA.md` como terceiro item da ordem de leitura e fonte de verdade dos nomes.

CONFORME: contratos e consumidores citam seções específicas do monólito, inclusive `#1`, `#3`, `#5`, `#7`, `#13`, `§16.2`, `§17.2` e comentários em `tela/renderizador.py`.

CONFORME: a ADR separa problema observado e solução aprovada em seções distintas e não afirma que o tamanho sozinho determina a modularização.

CONFORME: a ADR declara que a aplicação não foi executada e que migração, QA e conversão da fachada dependem de etapas subsequentes.

## 6. Auditoria das decisões D-NOM-01 a D-NOM-16

| Decisão | Conteúdo fiel | Origem explícita na ADR | Alteração ou ampliação | Resultado |
| ------- | ------------- | ----------------------- | ---------------------- | --------- |
| D-NOM-01 | SIM | SIM, linhas 128-133 | Sem ampliação material | CONFORME |
| D-NOM-02 | SIM | SIM, linhas 135-140 | Sem ampliação material | CONFORME |
| D-NOM-03 | SIM | SIM, linhas 142-147 | Sem ampliação material | CONFORME |
| D-NOM-04 | SIM | SIM, linhas 149-155 | Sem ampliação material | CONFORME |
| D-NOM-05 | SIM | SIM, linhas 157-163 | Acrescenta explicitação de não misturar com definições vigentes, coerente com a decisão | CONFORME |
| D-NOM-06 | SIM | SIM, linhas 165-171 | Explicita validade, processamento, erros e critérios de aceite, coerente com autoridade comportamental | CONFORME |
| D-NOM-07 | SIM | SIM, linhas 173-180 | Explicita que referências não redefinem e que comportamento fica no contrato | CONFORME |
| D-NOM-08 | SIM | SIM, linha 210 | Lista nominal completa sob `docs/nomenclatura/` | CONFORME |
| D-NOM-09 | SIM | SIM, linha 244 | Responsabilidades detalhadas coerentes com 42, 43 e 44 | CONFORME |
| D-NOM-10 | SIM | SIM, linha 257 | Acrescenta formato nominal dos campos, coerente com a decisão | CONFORME |
| D-NOM-11 | PARCIAL | NAO, linhas 259-274 não declaram `origem` | Conteúdo é fiel, mas rastreabilidade local quebra o padrão das decisões anteriores | NAO_CONFORME |
| D-NOM-12 | PARCIAL | NAO, linhas 276-287 não declaram `origem` | Conteúdo é majoritariamente fiel; detalhes sobre âncoras são compatibilidade derivada do levantamento | NAO_CONFORME |
| D-NOM-13 | PARCIAL | NAO, linhas 289-310 não declaram `origem` | Lista concreta do núcleo inclui conceitos não enumerados no conjunto fechado | NAO_CONFORME |
| D-NOM-14 | SIM | NAO, linhas 312-338 não declaram `origem` | Conteúdo corresponde à fronteira 20/40 aprovada | NAO_CONFORME |
| D-NOM-15 | SIM | NAO, linhas 340-358 não declaram `origem` | Conteúdo corresponde às proibições de migração estrutural | NAO_CONFORME |
| D-NOM-16 | SIM | SIM, linha 375 | Sem ampliação material | CONFORME |

EVIDENCIA: D-NOM-11 a D-NOM-15 são decisões centrais e não possuem origem explícita local, enquanto D-NOM-01 a D-NOM-10 e D-NOM-16 possuem `DECISAO_EXPLICITA_USUARIO`.

IMPACTO: a ADR perde rastreabilidade justamente nos pontos que o prompt mandou auditar com atenção especial. Coerência interna não substitui autoridade.

## 7. Auditoria da estrutura modular

CONFORME: todos os módulos aprovados aparecem nominalmente, com grafia correta e sem módulo inventado:

```text
00_INDICE.md
01_NUCLEO_COMUM.md
02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md
10_ESTILO.md
20_TELA_CORPO_E_COMPOSICAO.md
21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md
30_CABECALHO.md
31_BARRA_DE_MENUS_E_CHIPS.md
32_CONSOLE.md
33_LANCADOR.md
34_DASHBOARD.md
40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md
41_DISTRIBUICAO_MATRICIAL.md
42_DADOS_EXTERNOS_MULTINIVEL.md
43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md
44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md
90_ALIASES_E_TERMOS_DESCONTINUADOS.md
```

CONFORME: a fronteira entre `20_TELA_CORPO_E_COMPOSICAO.md` e `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` é coerente com D-NOM-14.

CONFORME: a fronteira entre `42`, `43` e `44` é coerente com D-NOM-09 e com ADR-0026, ADR-0027 e ADR-0028.

NAO_CONFORME: a estrutura está correta, mas D-NOM-14 não preserva origem explícita local.

## 8. Autoridade terminológica e comportamental

CONFORME: a ADR preserva a separação de autoridade:

| Autoridade | Itens preservados | Evidência |
|---|---|---|
| módulo de nomenclatura | termo, significado, tipo, distinção | seção 6, linhas 437-438 |
| contrato | comportamento completo | seção 6, linha 438; D-NOM-06 |
| ADR | decisão, motivação, alternativas | seção 6, linha 439 |

OBSERVACAO: a expressão "contrato proprietário" aparece no sentido de proprietário da declaração de dependências, não do termo. Esse uso é compatível quando lido junto com D-NOM-07 e D-NOM-10, mas exige redação precisa na aplicação futura para evitar colisão com "módulo proprietário do termo".

## 9. Dependências e papel do índice

CONFORME: D-NOM-10 declara o contrato como proprietário da declaração de dependências obrigatórias e condicionais.

CONFORME: D-NOM-11 proíbe o índice de redefinir termos ou manter segunda lista normativa independente.

NAO_CONFORME: o frontmatter `rastreabilidade.contratos_afetados` lista `docs/NOMENCLATURA.md`, `docs/INDICE.md` e `docs/adr/INDICE_ADR.md`, mas esses não são contratos. A própria ADR identifica contratos consumidores na seção 7, e o levantamento identifica `contrato_estilo`, `contrato_composicao_corpo`, `contrato_barra_de_menus`, `contrato_cabecalho`, `contrato_lancador`, `contrato_console`, `contrato_chip`, `contrato_tela_json` e `contrato_json_console` como consumidores diretos ou relacionados.

IMPACTO: a lista do frontmatter não é apenas resumida; ela é materialmente contraditória ao campo em que está inserida e incompleta diante de D-NOM-10 e dos critérios de aplicação.

## 10. Fachada e compatibilidade

CONFORME: a ADR mantém `docs/NOMENCLATURA.md` como fachada permanente e proíbe novas definições nela.

CONFORME: a ADR distingue caminho preservado de âncora não preservada e exige migração nominal de referências antigas antes da substituição do monólito.

CONFORME: a ADR proíbe simular âncoras antigas com definições duplicadas.

CONFORME: a ADR diferencia referências ativas, históricas e explicativas.

NAO_CONFORME: D-NOM-12 não declara origem explícita local para a política de fachada.

## 11. Histórico, pendências e migração estrutural

CONFORME: a ADR distingue histórico de regra vigente, issue de backlog e relatório de evidência.

CONFORME: a ADR não determina antecipadamente a classificação individual de pendências, histórico ou estados transitórios.

CONFORME: a ADR preserva lista e estado das ADRs no `docs/adr/INDICE_ADR.md`.

CONFORME: aliases e termos descontinuados permanecem localizáveis em `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`.

CONFORME: a migração futura é descrita como predominantemente estrutural e proíbe renomear termos, alterar schema, reconciliar deferimentos, modificar comportamento, introduzir defaults, remover compatibilidade e reescrever regras por preferência editorial.

CONFORME: a ADR trata regra completa duplicada entre glossário e contrato sem autorizar perda de obrigação.

## 12. Relação com ADRs anteriores

CONFORME: a relação declarada com ADR-0008, ADR-0011, ADR-0014, ADR-0015, ADR-0017, ADR-0018, ADR-0019, ADR-0020, ADR-0021, ADR-0022, ADR-0023, ADR-0024, ADR-0025, ADR-0026, ADR-0027 e ADR-0028 é coerente nos trechos consultados.

CONFORME: a ADR-0029 declara alterar organização documental e política de leitura, sem reabrir decisão funcional anterior.

CONFORME: a divergência da ADR-0018 permanece observação documental externa e deferida, não requisito corretivo desta ADR.

CONFORME: o mapeamento de ADR-0024 entre módulos `20` e `40` é coerente com D-NOM-14.

CONFORME: ADR-0026, ADR-0027 e ADR-0028 estão separadas coerentemente entre `42`, `43` e `44`.

## 13. Deferimentos e fora de escopo

CONFORME: permanecem deferidos:

- mapeamento termo a termo;
- texto final dos módulos;
- dependências exatas de cada contrato;
- classificação individual de pendências;
- localização de cada levantamento histórico;
- reconciliações terminológicas anteriores;
- migração de telas legadas;
- correção da divergência da ADR-0018.

CONFORME: a ADR não cria módulos fisicamente, não altera contratos, não altera índice, não altera nomenclatura, não altera código, não cria handoff e não executa migração.

## 14. Alternativas e genealogia semântica

CONFORME: "Manter o monólito como única fonte" contradiz D-NOM-01, D-NOM-02 e D-NOM-03.

CONFORME: "Mover todo conteúdo para os contratos e eliminar o glossário" contradiz a separação entre autoridade terminológica e comportamental.

CONFORME: "Criar módulos e manter cópia normativa também na fachada" contradiz D-NOM-07 e D-NOM-12.

NAO_CONFORME: "Dividir por tipo de conteúdo sem separação por domínio" está rejeitada de forma coerente com D-NOM-04, mas o motivo "fragmenta a leitura sem reduzir dependências" é formulação argumentativa sem genealogia explícita no conjunto fechado de decisões.

IMPACTO: a alternativa pode permanecer, mas sua motivação precisa ser marcada como inferência documental ou reescrita para derivar diretamente da decisão aprovada.

## 15. Critérios da futura aplicação

CONFORME: os 14 critérios da seção 11 são verificáveis, não executam a próxima etapa, exigem relatório e QA documental, mantêm a conversão da fachada como última ação e preservam contratos como autoridade comportamental.

OBSERVACAO: o critério 10 combina perda e duplicação de obrigação normativa. A intenção é coerente com D-NOM-15 e D-NOM-16, mas a redação futura deve distinguir "definição ativa duplicada" de "regra comportamental completa preservada no contrato".

## 16. Achados

### QA-ADR0029-ALTO-001 — Origem explícita ausente em D-NOM-11 a D-NOM-15

NAO_CONFORME.

EVIDENCIA: D-NOM-11, D-NOM-12, D-NOM-13, D-NOM-14 e D-NOM-15 não possuem `origem: DECISAO_EXPLICITA_USUARIO` nem formulação equivalente imediatamente associada às suas decisões. As demais decisões usam origem explícita.

IMPACTO: quebra rastreabilidade de políticas centrais: papel do índice, fachada, núcleo comum, fronteira 20/40 e migração estrutural.

### QA-ADR0029-ALTO-002 — `contratos_afetados` do frontmatter é contraditório e incompleto

NAO_CONFORME.

EVIDENCIA: o frontmatter lista `docs/NOMENCLATURA.md`, `docs/INDICE.md` e `docs/adr/INDICE_ADR.md` em `contratos_afetados`. Esses artefatos não são contratos. A seção 7 da ADR e o levantamento apontam contratos consumidores que não aparecem no frontmatter.

IMPACTO: a rastreabilidade da ADR fica incompatível com D-NOM-10, com os consumidores identificados e com a futura obrigação de declarar dependências por contrato.

### QA-ADR0029-MEDIO-001 — Núcleo comum contém lista concreta sem autoridade local suficiente

NAO_CONFORME.

EVIDENCIA: D-NOM-13 lista termos como `configuração concreta`, `elemento funcional`, `container estrutural`, `conteúdo`, `produtor`, `consumidor`, `loader`, `modelo`, `renderizador` e `regra de consulta ao módulo proprietário`. O conjunto fechado aprovado informa que o núcleo comum deve ficar restrito à terminologia transversal aprovada, mas não traz essa lista nominal.

IMPACTO: a ADR pode transformar uma restrição geral em conteúdo terminológico específico sem autoridade explícita.

### QA-ADR0029-MEDIO-002 — Alternativa considerada contém motivação não genealogicamente marcada

NAO_CONFORME.

EVIDENCIA: a alternativa "Dividir por tipo de conteúdo (schema, regra, histórico) sem separação por domínio" é rejeitada com o motivo "fragmenta a leitura sem reduzir dependências". A rejeição por não usar módulos por domínio deriva de D-NOM-04; o motivo operacional adicional não é identificado como inferência.

IMPACTO: a ADR atribui motivação decisória sem autoridade explícita suficiente.

### QA-ADR0029-BAIXO-001 — Critério 10 precisa distinguir definição duplicada de obrigação preservada

NAO_CONFORME.

EVIDENCIA: o critério 10 exige que regras comportamentais completas continuem nos contratos e que nenhuma obrigação normativa seja perdida ou duplicada. D-NOM-16 fala em definição ativa duplicada; D-NOM-15 fala em obrigação não desaparecida quando regra completa já estiver no glossário e no contrato.

IMPACTO: risco baixo de leitura excessiva na futura aplicação.

## 17. Estado Git final

```text
branch: master
HEAD: c90349c feat: implementa apresentacoes multinivel com modos por tela
status_short:
  ?? docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
  ?? docs/relatorios/RELATORIO_LEVANTAMENTO_REORGANIZACAO_NOMENCLATURA.md
  ?? docs/relatorios/RELATORIO_QA_ADR-0029.md
cached_name_only: vazio
```

## 18. Status final

```yaml
status_literal: ADR_REJECTED
achados_bloqueantes: 0
achados_altos: 2
achados_medios: 2
achados_baixos: 1
observacoes: 2
bloqueios: nenhum
```

## 19. Próxima categoria

```yaml
proxima_categoria: PATCH_ADR
executar_proxima_categoria: false
```

## 20. Encerramento

```yaml
etapa_executada: QA_ADR
artefato_auditado: docs/adr/ADR-0029-nomenclatura-modular-e-leitura-seletiva.md
relatorio_novo_criado: docs/relatorios/RELATORIO_QA_ADR-0029.md
status_literal: ADR_REJECTED
ultima_linha_ou_encerramento_literal: "status_literal: ADR_REJECTED"
achados_bloqueantes: 0
achados_altos: 2
achados_medios: 2
achados_baixos: 1
observacoes: 2
bloqueios: nenhum
estado_git: "master; HEAD c90349c; três arquivos não rastreados; nada staged"
```

status_literal: ADR_REJECTED
