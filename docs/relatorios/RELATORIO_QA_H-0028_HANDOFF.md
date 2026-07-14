# RELATORIO_QA_H-0028_HANDOFF

## 1. Identificação

- handoff auditado: `scripts/docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md`
- etapa: `QA_HANDOFF`
- papel: `auditor independente de handoff`
- raiz Git: `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1`
- branch: `master`
- commit-base: `f00b0bb`

## 2. Estado Git inicial

- **HEAD**: `f00b0bb` (f00b0bb docs: registra substituicao do H-0024 pelo H-0025)
- **Status do stage**: Vazio
- **Arquivos modificados rastreados**:
  - `M scripts/docs/NOMENCLATURA.md`
  - `M scripts/docs/adr/INDICE_ADR.md`
  - `M scripts/docs/contratos/contrato_composicao_corpo.md`
  - `M scripts/docs/contratos/contrato_json_tela_minima.md`
  - `M scripts/docs/contratos/contrato_tela_json.md`
- **Arquivos não rastreados (untracked)**:
  - `?? scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
  - `?? scripts/docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md`
  - `?? scripts/docs/relatorios/RELATORIO_APLICACAO_ADR-0020.md`
  - `?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`
  - `?? scripts/docs/relatorios/RELATORIO_QA_ADR-0020.md`
  - `?? scripts/docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0020.md`
  - `?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0020.md`
  - `?? scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_LEVANTAMENTO_MATRIZ_DE_GRUPOS.md`

Nenhum arquivo de código, teste ou configuração ativa do sistema foi alterado no estado de entrada.

## 3. Autoridades consultadas

- **Nomenclatura**: `scripts/docs/NOMENCLATURA.md` (seção 15)
- **Contrato de Composição de Corpo**: `scripts/docs/contratos/contrato_composicao_corpo.md` (seções 3.3, 5.13–5.24, R-25–R-32)
- **Contrato Tela JSON**: `scripts/docs/contratos/contrato_tela_json.md` (seção 8)
- **Contrato JSON Tela Mínima**: `scripts/docs/contratos/contrato_json_tela_minima.md` (seção 6.4)
- **ADR-0020 (autoridade primária)**: `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`
- **ADR-0015 (composição, maiores restos)**: `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`
- **ADR-0018 (ausência de distribuição)**: `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`
- **ADR-0019 (profundidade, 3 níveis)**: `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`

## 4. Evidências processuais

Foram verificadas as seguintes evidências processuais correspondentes às etapas anteriores:
- `adr_0020`:
  - `status_no_arquivo`: `aceita`
  - `status_no_indice`: `aceita`
  - `qa_pos_patch`: `ADR_APPROVED_WITH_NOTES` (conforme `RELATORIO_QA_POS_PATCH_ADR-0020.md`)
  - `aplicacao`: `ADR_APPLICATION_COMPLETED` (conforme `RELATORIO_APLICACAO_ADR-0020.md`)
  - `qa_aplicacao`: `ADR_APPLICATION_APPROVED` (conforme `RELATORIO_QA_APLICACAO_ADR-0020.md`)

O estado da ADR-0020 está formalmente consolidado como base normativa estável.

## 5. Estado comprovado

O ciclo precedente H-0027 está formalmente fechado e consolidado:
- `H-0027`:
  - `commit`: `c003f3e`
  - `qa_handoff`: `H1_HANDOFF_APPROVED` (conforme `RELATORIO_QA_POS_PATCH_H-0027_HANDOFF.md`)
  - `qa_implementacao`: `I1_IMPLEMENTATION_APPROVED` (conforme `RELATORIO_QA_POS_PATCH_H-0027_IMPLEMENTACAO.md`)
  - `testes`: `1004/1004` (conforme `RELATORIO_VERIFICACAO_FECHAMENTO_H-0027.md`)
  - `estado`: `fechado`

O handoff H-0028 estende essa base técnica de forma totalmente coerente e incremental, sem substituir as decisões e a arquitetura vigentes.

## 6. Status e autoaprovação

O handoff `H-0028` atende integralmente os critérios de controle de status:
- Frontmatter declara `status: proposto`.
- Corpo declara `status: proposto`.
- O documento não tenta realizar autoaprovação e é estruturado como uma ordem de trabalho técnica limpa e fechada para o futuro executor de implementação.

## 7. Capacidade coesa

O handoff H-0028 planeja exclusivamente uma única capacidade coesa:
- **Matriz declarativa de grupos com coordenadas explícitas e grade compartilhada**.

Estão marcados estritamente como fora de escopo (seção 7 e 29) quaisquer tópicos independentes ou concorrentes, incluindo:
- Células vazias em qualquer forma;
- Mesclagem de células (`rowspan`/`colspan`);
- Paginação ou rolagem da matriz;
- Novo tipo funcional;
- Alteração na lógica de navegação ou chips existentes;
- Nova política de terminal pequeno ou redefinições da `ADR-0017`/`SIGWINCH`;
- Correção da divergência documental da `ADR-0018`.

## 8. Fidelidade a D1–D16

Todas as dezesseis decisões arquiteturais estabelecidas pela `ADR-0020` são rigorosamente mantidas e preservadas pelo handoff:

| Decisão | Evidência no handoff | Autoridade | Resultado |
|---|---|---|---|
| **D1** | Seção 4 e 12 descrevem os comportamentos `livre` e `matriz` do grupo. | `ADR-0020` §D1 | `FIEL` |
| **D2** | Seção 12.1 estabelece o seletor declarativo `estrutura` e proíbe termos concorrentes. | `ADR-0020` §D2 | `FIEL` |
| **D3** | Seção 12.1 formaliza que a omissão de `estrutura` resulta no comportamento `livre`. | `ADR-0020` §D3 | `FIEL` |
| **D4** | Seção 11 e 22 determinam a preservação completa do comportamento `livre` e da `ADR-0018`. | `ADR-0020` §D4 | `FIEL` |
| **D5** | Seção 12.2 e 13 planejam limites de 2 a 4 por eixo sem fallbacks silenciosos. | `ADR-0020` §D5 | `FIEL` |
| **D6** | Seção 12.2 e 13 exigem distribuições obrigatórias nos dois eixos matriciais, sem defaults. | `ADR-0020` §D6 | `FIEL` |
| **D7** | Seção 15 planeja o cálculo de uma única grade comum de cortes por container. | `ADR-0020` §D7 | `FIEL` |
| **D8** | Seção 12.2 e 13 estabelecem as coordenadas explícitas, indexação 1-based e proibições de duplicidade. | `ADR-0020` §D8 | `FIEL` |
| **D9** | Seção 12.2 e 18 estendem o suporte a console, lançador, dashboard e grupo em células matriciais. | `ADR-0020` §D9 | `FIEL` |
| **D10** | Seção 12.3 e 18 proíbem terminantemente células vazias ou placeholders nesta versão. | `ADR-0020` §D10 | `FIEL` |
| **D11** | Seção 7 e 29 listam mesclagem e `rowspan`/`colspan` como estritamente fora de escopo. | `ADR-0020` §D11 | `FIEL` |
| **D12** | Seção 13.3 veda correções silenciosas e impõe rejeição determinística para matrizes inválidas. | `ADR-0020` §D12 | `FIEL` |
| **D13** | Seção 12.3 e 13 proíbem o uso do campo `arranjo` em estrutura matricial. | `ADR-0020` §D13 | `FIEL` |
| **D14** | Seção 20 e 27 preservam `SIGWINCH` e colocam políticas de insuficiência como bloqueios normativos. | `ADR-0020` §D14 | `FIEL` |
| **D15** | Seção 11 e 22 garantem retrocompatibilidade total com todos os JSONs e grupos existentes. | `ADR-0020` §D15 | `FIEL` |
| **D16** | Seção 4, 14.1 e 18 mantêm que o grupo matricial é uma especialização sem novo tipo funcional. | `ADR-0020` §D16 | `FIEL` |

## 9. Arquivos permitidos

O handoff define de forma nominal, restrita e suficiente na seção 8 exatamente os 6 arquivos existentes alteráveis e o relatório novo de implementação:
1. `scripts/tela/loader.py` (estende `_validar_grupo`)
2. `scripts/tela/modelo.py` (estende `_construir_elementos_recursivo` se necessário)
3. `scripts/tela/renderizador.py` (adiciona `_renderizar_container_matriz` e estende `_renderizar_container`)
4. `scripts/tela/teste_loader.py` (adiciona testes de validação matricial)
5. `scripts/tela/teste_modelo.py` (adiciona testes de modelo matricial)
6. `scripts/tela/teste_renderizador.py` (adiciona testes de renderização e alinhamento da matriz)
7. `scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md` (novo arquivo a criar)

A lista é precisa e nominal, não inclui curingas, diretórios ou documentos normativos.

## 10. Arquivos proibidos

O handoff proíbe terminantemente edições fora da lista declarada na seção 9, mencionando explicitamente os arquivos de demonstração (`demo.py`, `teste_demo.py`), diagnóstico (`diagnostico.py`, `teste_diagnostico.py`), JSONs ativos de produção (`orquestrador.json`, `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json`), estilo, cabeçalho e todos os documentos normativos (ADRs, contratos, nomenclatura e índice).

## 11. Loader e validações

A seção 13 planeja uma sequência estrita e detalhada de 17 validações determinísticas para o loader, cobrindo:
- Valor aceito em `estrutura`;
- Proibição de `arranjo` em `"matriz"`;
- Validação do `arranjo` em `"livre"`;
- Presença e tipo do objeto `matriz`;
- Dimensões de `linhas` e `colunas` dentro de [2, 4];
- Obrigatoriedade e validade das distribuições dos dois eixos;
- Presença de `celulas` com comprimento `linhas × colunas`;
- Tipos de dados e limites das coordenadas (1-based);
- Ausência de duplicidade de coordenada ou de elemento;
- Referências consistentes com `elementos[]` do grupo;
- Cobertura completa sem filhos não associados ou excedentes;
- Validação recursiva de profundidade máxima de 3 níveis de grupo.

As mensagens de erro seguem o padrão de diagnóstico do sistema (caminho estrutural afetado) e usam as exceções existentes `TelaGrupoInvalido` e `TelaEstruturaInvalida` de forma fiel.

## 12. Modelo e `_campos_inertes`

O handoff determina nominalmente na seção 14 que o modelo não necessita de alterações estruturais, visto que a infraestrutura `_campos_inertes` do `ElementoCorpo` já captura e preserva integralmente todos os campos extras de um grupo (incluindo `estrutura` e `matriz`).
A inspeção técnica confirmou essa propriedade em `scripts/tela/modelo.py` (linhas 168-172). Caso nenhuma alteração seja feita no arquivo `modelo.py` pelo implementador, o relatório `IMP-0029` deverá documentar essa decisão técnica legítima de forma nominal.

## 13. Renderer e fluxo de chamadas

O handoff propõe na seção 16.1 a criação de `_renderizar_container_matriz` e a extensão limpa de `_renderizar_container` na seção 16.2.
O fluxo de chamadas internas dos containers horizontal e vertical é estendido na seção 16.3 para propagar `estrutura_g` e `matriz_g` aos grupos aninhados. O caminho de execução para grupos `livre` (comportamento recursivo legado) permanece totalmente preservado e intacto.

## 14. Grade compartilhada

O handoff estabelece que o container matricial calcula e aplica uma única grade comum de cortes por eixo (seção 15).
As células pertencentes à mesma matriz compartilham a mesma grade bidimensional calculada uma única vez pelo pai, garantindo alinhamento físico estrito de todas as divisórias internas, impedindo que cada célula calcule suas coordenadas isoladamente.

## 15. Maiores restos

O algoritmo de arredondamento por maiores restos é reutilizado diretamente a partir das funções utilitárias existentes em `renderizador.py` (`_pesos_distribuicao`, `_distribuir_alturas` e `_distribuir_larguras`) — conforme seção 15.1.
O arredondamento de maiores restos é processado de forma isolada por eixo na matriz (seção 15.2 e 15.3).

## 16. Bordas e interseções

As divisórias de células adjacentes compartilham coordenadas e são posicionadas de forma contígua no renderer, mantendo o comportamento de caixas em contato do arranjo horizontal já existente (seção 17).
O handoff indica que o sistema de bordas existente deve ser preservado e que não deve ser inventada lógica ad-hoc de interseção (como caracteres `┼` no lugar de `││`) para as bordas compartilhadas nesta versão.

## 17. Hierarquia e profundidade

O limite máximo de 3 níveis de grupos estruturais da `ADR-0019` é preservado integralmente:
- Linhas, colunas e células não acrescentam níveis de profundidade.
- Um nó `grupo` aninhado dentro de uma célula da matriz é verificado normalmente e conta para o limite de profundidade (seção 18).
- Um grupo no quarto nível dentro de uma célula é rejeitado pelo loader com erro estrutural (`EX-MAT-I8` e seção 18).

## 18. Diagnósticos

Os diagnósticos de invalidade estrutural da matriz seguem o padrão existente, gerando mensagens com indicação precisa do caminho do campo afetado (como `g1.matriz.linhas.distribuicao`) e do valor recebido, utilizando `TelaGrupoInvalido` e `TelaEstruturaInvalida` de forma consistente (seção 19).

## 19. Terminal pequeno e SIGWINCH

O handoff mantém e preserva integralmente as diretrizes da `ADR-0017`:
- Detecção de `SIGWINCH` e redesenho reativo;
- Exibição de quadro global de terminal pequeno quando as dimensões físicas da janela forem insuficientes (< 10 colunas ou < 6 linhas);
- Rejeição e erro (`RenderizadorErro` ou `RenderizadorErro` propagado) se a área de cota calculada para uma célula for inferior a 10 colunas (mínimo físico útil);
- Nenhuma política ad-hoc inventada além da `ADR-0017`. Qualquer necessidade de nova decisão arquitetural deve forçar a parada com `ARCHITECTURE_REVIEW_REQUIRED` (seção 20).

## 20. Alterações declarativas

As alterações em arquivos JSON ativos de produção são proibidas:
- `alteracoes_declarativas_em_json_ativo: nenhuma` (seção 21).
Todas as configurações de matriz para suítes de testes são especificadas como dicionários inline nos arquivos de testes, preservando a totalidade das configurações estáveis da TUI original.

## 21. Testes

O handoff planeja na seção 23 uma suíte exaustiva e excelente de testes automatizados, cobrindo detalhadamente:
- **Testes de compatibilidade (regressão)**: grupos sem `estrutura` (ausente → `livre`), `estrutura: "livre"` explícita, ausência de distribuição seguindo a `ADR-0018` e todos os testes anteriores passando;
- **Matrizes válidas**: combinações de 2x2 a 4x4, modos iguais, percentuais, fracionários, assimétricos, eixos com modos distintos, células em ordem embaralhada no JSON, células contendo consoles, lançadores, dashboards e grupos nos limites de profundidade permitidos;
- **Matrizes inválidas**: rejeição de valor desconhecido, objeto `matriz` ausente, dimensões 1 e 5, ausência de qualquer das distribuições, percentuais que não somam 100, pesos negativos, coordenadas fora dos limites, duplicidade de elemento ou coordenada, células faltantes ou excedentes, presença de `arranjo` em matriz, e grupo no quarto nível em célula;
- **Renderização**: testes determinísticos que analisam as linhas da string de saída e asseguram alinhamento estrito das divisórias horizontais e verticais por colunas e linhas da mesma matriz, cotas assimétricas, arredondamentos com restos, redimensionamento reativo e terminal pequeno.

## 22. Baseline

O baseline técnico de testes estabelecido do H-0027 de **1004/1004** testes passando é formalmente identificado (seção 22 e 23.6). O handoff determina que o total de testes futuro seja estendido de forma incremental (`1004 + N`), não fixado, mantendo a integridade da suíte histórica.

## 23. Validação manual

A validação manual na seção 24 é planejada de forma completa, detalhando:
- Os cenários visuais a verificar em sessão TTY (matrizes 2x2, 2x4 assimétricas, arredondamento com restos e redimensionamento);
- Critérios visuais objetivos de aprovação (divisórias perfeitamente alinhadas, ausência de lacunas, recálculo sob redimensionamento);
- Critérios objetivos de reprovação (divisórias desalinhadas, lacunas ou inconsistência reativa);
- Mitigação de risco para não alterar JSONs ativos: recomendação da Opção A (construção de ModeloTela ad-hoc inline no teste).

## 24. Relatório IMP-0029

O arquivo de relatório de implementação é especificado e nomeado nominalmente na seção 25 como:
`scripts/docs/relatorios/IMP-0029-matriz-de-grupos-coordenadas-explicitas.md`

Os campos de conteúdo obrigatórios enumerados na seção 25.1 cobrem detalhadamente todas as necessidades de documentação, integridade de stage, baseline de testes e bloqueios.

## 25. Critérios de aceite

O handoff planeja na seção 26 dezesseis critérios de aceite estruturais, objetivos, verificáveis, estritamente limitados ao escopo, complementares e suficientes para embasar a futura aprovação ou reprovação da implementação técnica.

## 26. Condições de bloqueio

As condições processuais de controle de fluxo de implementação e bloqueios na seção 27 estão mapeadas de forma extremamente limpa, coerente e sem contradições:
- `ARCHITECTURE_REVIEW_REQUIRED`: acionado em caso de lacuna normativa, contradição nos contratos ou se a lista nominal de arquivos permitidos para edição for insuficiente;
- `BLOCKED_EVIDENCE`: acionado em caso de ausência de autoridades de leitura ou se o baseline de testes não puder ser comprovado;
- `BLOCKED_REPOSITORY_STATE`: acionado se os arquivos do sistema apresentarem alterações inesperadas.

O executor de implementação é obrigado a interromper a tarefa de forma clara e segura sob qualquer uma dessas condições.

## 27. Ausência de implementação antecipada

O handoff H-0028 contém pseudocódigos conceituais (seções 15 e 16), comandos e assinaturas propostas, mas não apresenta remendos de código, código-fonte finalizado como concluído no repositório, testes modificados antecipadamente ou relatórios de implementação preenchidos de forma precoce. O repositório permanece limpo e em contexto de design intocado.

## 28. Coerência interna

O documento H-0028 é materialmente consistente em toda a sua extensão:
- Não possui decisões repetidas ou divergentes;
- A lista de arquivos permitidos é idêntica nos cabeçalhos e nas seções correspondentes;
- As validações planejadas coincidem perfeitamente com os exemplos inválidos descritos;
- O schema da matriz é idêntico em todas as seções e condiz integralmente com a base contratual aprovada;
- Não há contradições internas ou requisitos mutuamente exclusivos.

## 29. Escopo Git

Não foram gerados commits ou preenchimentos de stage. O repositório mantém-se totalmente limpo de resíduos ou edições experimentais indevidas em código ou testes.

## 30. Achados

Nenhum achado de severidade `BLOQUEANTE`, `ALTO`, `MEDIO` ou `BAIXO` foi identificado no arquivo de handoff `scripts/docs/handoff/H-0028-matriz-de-grupos-coordenadas-explicitas.md`.

### OBSERVAÇÕES

- **OBS-001 — Identificação fidedigna de pendências do ciclo anterior**
  - *Descrição*: O handoff descreve de forma fidedigna e precisa o histórico de design da `ADR-0020`, identificando a rejeição inicial do ciclo ADR, a resolução do `ACH-001` pelo patch de distribuição obrigatória e a preservação da divergência documental da `ADR-0018` como pendência histórica externa, demonstrando maturidade metodológica.

## 31. Estado Git final

O repositório mantém-se totalmente íntegro e em conformidade com o commit-base `f00b0bb` de entrada, acrescido exclusivamente da criação do presente relatório canônico de QA do handoff:
- **Estado do stage**: Vazio (limpo)
- **HEAD**: `f00b0bb` (confirmado)

## 32. Status final

```yaml
status_final: H1_HANDOFF_APPROVED
bloqueantes: 0
altos: 0
medios: 0
baixos: 0
observacoes: 1
```

## 33. Próxima categoria processual

```text
IMPLEMENTAR
```
