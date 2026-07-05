---
name: backlog-metodologia
description: Trabalho planejado e decisões abertas no nível do sistema metodologia
metadata:
  type: backlog
  scope: metodologia
---

# Backlog — metodologia/

## Contrato 1 — Pesquisa (decisões abertas)

- [ ] **Janela temporal por hipótese**: H1–H3 usam 2019–2026; H4 (digital twin) pode
  iniciar em 2020–2021, quando o termo ganhou tração em IWN. Definir antes de executar
  as buscas.
- [ ] **Overlap entre hipóteses**: artigo que evidencia H1 e H3 simultaneamente entra
  em qual tipo de busca? Registra nas duas? Tem chave única? Definir política antes
  de iniciar triagem.
- [ ] **Critérios formais de inclusão/exclusão**: o contrato de pesquisa traz o
  esqueleto; os critérios específicos por hipótese precisam ser preenchidos antes
  da primeira busca de cada H.
- [ ] **Acessibilidade do corpus atual (41 artigos)**: definir quais dados do corpus
  `versao_1_0` são importados para o novo sistema e em qual formato.
  Ver Contrato 3 — Migração.

- [ ] **PRISMA-ScR vs. SLR clássica**: o GPT sugere enquadrar como "scoping review
  sistemática assistida por IA" (PRISMA-ScR) em vez de SLR clássica com meta-análise.
  É metodologicamente mais honesto para o caso — o objetivo é mapear o espaço e
  identificar lacunas, não sintetizar efeitos. Decidir antes de escrever o capítulo
  metodológico da revisão.

- [ ] **Reclassificação do corpus atual (41 artigos) em A/B/C**: os artigos do
  `versao_1_0` já fichados precisam ser classificados por camada. Nenhum refichamento
  necessário — usar os dados existentes.

## Contrato 2 — Texto (decisões abertas)

- [ ] **Prazo da defesa**: definir data alvo. Determina se o cenário é 60 dias
  (padrão ouro mínimo: protocolo + corpus A + PRISMA + matriz + reescrita) ou
  120 dias (versão robusta com corpus completo, capítulo metodológico, apêndices
  reproduzíveis). As rotas são diferentes.
- [ ] **Escopo da revisão do qualificacao_v3.tex**: corrigir o v3 (ajustes pontuais)
  ou reestruturar em v4 com as seções que faltam (metodologia experimental,
  tabela-síntese do corpus, cronograma)? Condicionado ao prazo.
- [ ] **Prioridade dos itens da crítica**: Claude e GPT convergem em ~5 itens de alto
  impacto. Definir quais entram antes da defesa e quais vão para a tese.
- [ ] **6 perguntas de auditoria de afirmações** (GPT): para cada afirmação central
  do texto — qual depende de evidência primária? qual de survey? qual é inferência?
  qual lacuna é real vs. busca incompleta? Alimenta o `contrato_texto_qualificacao.md`.

## Contrato 3 — Migração (decisões abertas)

- [ ] **Trigger da migração**: o que determina o momento de criar o novo repositório?
  (conclusão do contrato de pesquisa? primeiro ciclo de buscas concluído?)
- [ ] **Definição de "contaminação"**: documentar explicitamente o que não migra —
  logs históricos, estados do `index.json`, outputs de fichamento do corpus antigo,
  estrutura de pastas baseada em `batch_XX`.
- [ ] **Redesenho de "lote"**: no novo sistema, `lote` passa a ser `tipo_busca`
  (H1, H2, H3, H4). Mapear onde o conceito de lote está hardcoded nos scripts
  antes de migrar.
- [ ] **Stack de ferramentas de fichamento**: candidatos identificados — Claude, GPT,
  DeepSeek, GLM-5.2 (Zhipu AI), Llama 4 (Meta), Qwen3-max (Alibaba). Gemini e Grok
  descartados. Para produção com 50–150 artigos, selecionar 3–4 após teste empírico
  (ver item PDF vs. dados extraídos). Critérios de seleção: qualidade de extração,
  custo por artigo, diversidade de perspectiva de treinamento. DeepSeek-R1 tem MIT
  real nos pesos; Llama 4 e Qwen3 têm licenças permissivas (Apache 2.0 / Meta
  custom) — verificar termos antes de publicar metodologia.

- [ ] **PDF vs. dados extraídos no fichamento**: decisão empírica — testar em 5–10
  artigos antes de fechar o contrato. Hipótese: dados extraídos superiores para
  figuras/tabelas; PDF direto superior para discussão/conclusão com nuance
  contextual. Resultado define a estratégia de ingestão no pipeline novo.

- [ ] **Consolidação via API**: avaliar substituir Ollama local (gemma3:12b) por
  API (DeepSeek ou GLM) na etapa de consolidação. Para corpus de 50–150 artigos
  o custo é controlável e a qualidade tende a ser superior.

- [ ] **Refichamento do corpus existente (41 artigos)**: após definir stack e
  estratégia PDF vs. dados, decidir se refaz o fichamento dos artigos A/B do
  corpus atual com o novo pipeline ou mantém o existente.

- [ ] **Contrato de fichamento**: revisar o pipeline e escrever `contrato_fichamento.md`
  antes de iniciar buscas. Campos-base identificados pelo GPT (2026-07-02):
  problema atacado, tipo WSN/IWN, camada (PHY/MAC/roteamento/cross-layer/aplicação),
  técnica ML/RL/DRL, ambiente (simulação/dataset/hardware/testbed), métricas,
  baseline, métrica de energia, overhead de controle (sim/não), energia de inferência
  (sim/não), latência (sim/não), confiabilidade/PDR (sim/não), mobilidade/interferência
  (sim/não), limitações assumidas, trecho bruto do PDF, decisão de relevância.

## Infraestrutura

- [ ] Criar `metodologia/texto/docs/` com contratos de redação geral e bloco por texto
  (qualificacao primeiro).
- [ ] Criar `metodologia/scripts/docs/` com estrutura exportável quando pipeline
  for redesenhado.
- [ ] Criar `metodologia/referencias/docs/` com decisões sobre bases, formatos e
  política de importação.
