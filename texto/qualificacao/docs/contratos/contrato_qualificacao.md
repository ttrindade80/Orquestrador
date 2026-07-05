---
name: contrato-qualificacao
description: Contrato específico para o texto de qualificação de doutorado PPGEE/UFRGS — estrutura obrigatória, requisitos por seção, vulnerabilidades da banca e checklist de entrega
metadata:
  type: contrato
  scope: texto-qualificacao
---

# Contrato do Texto de Qualificação

Herda todas as regras de `contrato_redacao_geral.md`. Este contrato adiciona o que
é específico ao gênero "proposta de qualificação de doutorado — PPGEE/UFRGS".

## Correção arquitetural — incorporar em todo o texto

O gerenciador externo é alimentado pela **rede elétrica**. O custo de
inferência do modelo ML é **irrelevante para o tempo de vida da WSN**.

O que afeta os sensores (e deve ser modelado):
- Overhead de transmissão dos pacotes de estado (sensores → gateway):
  CSI, energia residual, contagem de colisões — consomem bateria dos sensores
- Overhead de recepção das decisões do gerenciador (gateway → nós):
  tabelas de roteamento, configuração de slots TDMA — também consomem bateria

A contribuição real: gerenciador que produz decisões melhores com **menor
overhead de controle sobre os sensores**, não um gerenciador que "gasta menos
energia com ML".

Qualquer frase que afirme que o custo de ML impacta o tempo de vida da WSN
deve ser corrigida.

## Contratos de seção

Os contratos detalhados por capítulo (propósito, tom, conteúdo por subseção,
contagem de palavras, referências e critérios de qualidade) estão em:

`qualificacao/docs/contratos_secoes.md`

Esses contratos são a referência operacional para redigir ou revisar cada
capítulo. Na migração para o novo sistema, o arquivo se moverá para
`metodologia/texto/qualificacao/docs/contratos/contratos_secoes.md`.

Resumo dos contratos existentes:

| Contrato | Capítulo/Seção |
|---|---|
| 1 | Cap. 1 — Introdução (motivação, problema, hipóteses, objetivos) |
| 2 | Sec. 2.1 — Redes de Sensores Sem Fio |
| 3 | Sec. 2.2 — Aprendizado de Máquina |
| 4 | Sec. 2.3 — Otimização Cross-Layer |
| 5 | Cap. 3 — Revisão da Literatura |
| 6 | Cap. 4 — Proposta de Pesquisa |
| 7 | Cap. 5 — Etapas de Trabalho |

## Requisitos técnicos

- Classe: `delaetex` com opção `prop-tese`
- Compilação: `cd qualificacao/texto && make`
  (exit code 1 é normal antes do bibtex — confirmar com "Output written on qualificacao.pdf")
- Hifenização: verificar se `babel` com português está carregado no preâmbulo
- `\linespread` requer `\selectfont` para efeito imediato fora de `\maketitle`

## Estrutura obrigatória

```
Resumo (PT) + Abstract (EN)
Lista de abreviaturas
Cap. 1  Introdução
  1.1   Motivação
  1.2   Problema de Pesquisa (pergunta explícita e falsificável)
  1.3   Hipóteses (falsificáveis, com baselines nomeados)
  1.4   Objetivos (OG + OEs numerados)
  1.5   Organização do texto          ← ausente no v3; obrigatório
Cap. 2  Fundamentação Teórica
  (WSN → MAC → Roteamento → QoS → ML → RL/DRL → MARL → Cross-layer)
Cap. 3  Revisão da Literatura
  3.0   Metodologia da revisão        ← ausente no v3; obrigatório
  3.x   Síntese temática
  3.x   Síntese das lacunas
  3.x   Baselines adotados
  3.x   Posicionamento da proposta
Cap. 4  Proposta de Pesquisa
  4.x   Hipótese Central
  4.x   Arquitetura do gerenciador
  4.x   Endereçamento das lacunas
  4.x   Função de recompensa
  4.x   Avaliação Experimental        ← ausente no v3; obrigatório
Cap. 5  Etapas de Trabalho            (não "Objetivos" — evitar duplicação com Cap. 1)
  (referência cruzada para \ref{sec:objetivos})
Referências
```

Seções marcadas **ausente no v3; obrigatório** são as adições de maior impacto
para a defesa. Implementar nesta ordem de prioridade.

## Seção de Metodologia da Revisão (Cap. 3.0)

Conteúdo mínimo obrigatório:

- Pergunta de pesquisa e subperguntas
- Base(s) de dados utilizadas com justificativa
- String(s) de busca exatas
- Período coberto com justificativa
- Tipos de documento aceitos
- Critérios de inclusão (numerados)
- Critérios de exclusão (numerados)
- Fluxograma de triagem (PRISMA-like): identificados → triados → elegíveis → incluídos
- Limitações e vieses reconhecidos (ex.: base única, janela temporal, idioma)
- Declaração de uso de IA — ver issue [I001]; aplicar após aval do orientador

## Seção de Avaliação Experimental (Cap. 4)

Conteúdo mínimo obrigatório:

- Simulador escolhido com justificativa (não "NS-3 ou OMNeT++")
- Modelo de canal com justificativa (não "Rayleigh ou Riciano")
- Definição operacional de "condições físicas realistas" (quais fenômenos, quais modelos)
- Escalas experimentais com justificativa (por que 20/50/100 nós?)
- Modelo de energia e de tráfego
- Número de rodadas, sementes aleatórias, intervalo de confiança
- Métricas de resposta por hipótese
- Baselines concretos por hipótese

## Tabela de hipóteses (obrigatória em Cap. 4)

Para cada hipótese H1–H3:

| Campo | Conteúdo |
|---|---|
| Hipótese | Enunciado falsificável |
| Condição experimental | Cenário que ativa esta hipótese |
| Métrica | O que medir |
| Baseline | Contra quem comparar |
| Experimento | Qual rodada/variante |
| Critério de refutação | Valor ou condição que refuta |

H2 precisa de critério quantitativo explícito para "sem comprometer a latência"
(quanto de degradação refuta a hipótese?).

## Palavras-chave

Manter consistência PT ↔ EN:

| PT | EN |
|---|---|
| Redes de Sensores Sem Fio Industriais | Industrial Wireless Sensor Networks |
| Aprendizado por Reforço | Reinforcement Learning |
| Gerenciamento Cross-Layer | Cross-Layer Management |
| Eficiência Energética | Energy Efficiency |
| Overhead de Controle | Control Overhead |

## Checklist de vulnerabilidades da banca

Itens que a banca tem alta probabilidade de questionar — cada um deve ter resposta
escrita no texto antes da entrega:

- [ ] Escolha do simulador (critério documentado)
- [ ] Escolha do modelo de canal (critério documentado)
- [ ] Escala 20/50/100 nós justificada (ou escala maior adicionada)
- [ ] Metodologia da SLR com string, data, base e fluxo de triagem
- [ ] Viés de seleção: critérios I/E pré-definidos e documentados
- [ ] Colisão de símbolos matemáticos eliminada (γ, α com uso único)
- [ ] MDP com tupla completa (S, A, P, R, γ)
- [ ] Faixas de energia consistentes (10²–10⁵ ou corrigir conforme dados)
- [ ] H2 com critério quantitativo de refutação
- [ ] Mapeamento H1–H3 para condições (a)–(c) completo (H2 não pode ficar sem condição)
- [ ] Novidade em relação a SDWSN e DOS-RL explicitada
- [ ] Custo energético do gateway declarado (fora do escopo ou justificado)
- [ ] Treinamento do agente: online ou offline? Custo da exploração em rede industrial?
- [ ] Espaço de estado e ação do gerenciador dimensionados para 100 nós
- [ ] Substrato MAC: 802.15.4e/TSCH, WirelessHART, ou MAC próprio — declarar
- [ ] Tabela-síntese dos artigos do núcleo analítico (≥ 23 artigos com lacunas)
- [ ] Declaração de uso de IA — aguardando [I001]

## Ameaças à validade

Opcional — decidir conforme prazo e perfil da banca. Se incluída, cobrir:
- Validade interna (vieses da revisão)
- Validade externa (generalização dos resultados simulados)
- Validade de constructo (métricas medem o que a hipótese afirma?)

## Changelog

| Data | Alteração |
|---|---|
| 2026-07-03 | Versão inicial — baseada nas análises críticas Claude + GPT de 2026-07-02 |
