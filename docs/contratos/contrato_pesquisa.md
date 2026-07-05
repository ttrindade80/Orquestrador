---
name: contrato-pesquisa
description: Protocolo geral de pesquisa bibliográfica orientada por hipóteses — metodologia, bases, triagem, documentação e requisitos de rigor para a qualificação PPGEE/UFRGS
metadata:
  type: contrato
  scope: metodologia
---

# Contrato de Pesquisa

## Contexto

A pesquisa de doutorado investiga gerenciamento inteligente de WSN industriais (IWN)
com aprendizado de máquina, modelando explicitamente o overhead de controle. A
qualificação identificou lacunas metodológicas na revisão anterior — ausência de
string documentada, critérios formais de inclusão/exclusão, e rastreabilidade de
decisões — que tornam a SLR vulnerável a questionamento da banca. Este protocolo
corrige essas lacunas e orienta toda busca futura.

## Hipóteses-guia

As buscas são estruturadas em torno de quatro frentes. Cada frente é um tipo de
busca independente, não um lote físico.

| ID | Frente | Descrição |
|---|---|---|
| H1 | Overhead de controle + ML | Controle centralizado em WSN/IWN com ML; modelagem explícita do overhead de controle |
| H2 | Alternância TDMA/CSMA | Comutação dinâmica entre protocolos MAC em WSN |
| H3 | Hotspot + controlador externo | Detecção e mitigação de hotspot por gerenciador externo em WSN |
| H4 | Digital twin em WSN/IWN | Uso de gêmeo digital para gestão/controle de redes de sensores industriais |

H4 é frente independente — não cruza filtros com H1–H3 na busca inicial.

## Bases de dados

**Principal:** Scopus — cobre IEEE, ACM, Elsevier, Springer e outros. Justificativa:
cobertura ampla em engenharia elétrica e ciência da computação; exportação CSV
adequada para triagem em volume.

**Complementares** (quando a busca principal indicar lacuna ou cobertura insuficiente):
IEEE Xplore, ACM Digital Library, Springer Link. Uso documentado em `strings_busca.md`
com justificativa.

## Formatos de exportação

| Etapa | Formato | Uso |
|---|---|---|
| Resultados bulk | CSV (Scopus) | Triagem inicial — todos os campos disponíveis |
| Importação por artigo | RIS | Formato canônico de importação individual |
| Entrada no LaTeX | BIB | Convertido de RIS via ferramenta existente |

## Janela temporal

- H1, H2, H3: 2019–2026 (padrão)
- H4: a definir (ver backlog — digital twin ganhou tração em IWN a partir de ~2020)
- Justificativa da janela deve constar em cada entrada de `strings_busca.md`

## Pipeline de busca e triagem

```
1. BUSCA
   Definir string + filtros → executar → exportar CSV
   → registrar em strings_busca.md ANTES de abrir o arquivo

2. TRIAGEM
   Aplicar critérios de inclusão/exclusão ao CSV
   → categorizar cada registro: incluído / excluído / dúvida
   → documentar motivo de exclusão por registro

3. RESOLUÇÃO DE DÚVIDAS
   Registros "dúvida" revisados com acesso ao abstract ou texto completo
   → decisão final documentada

4. OBTENÇÃO
   Para cada incluído: baixar RIS individual da base de origem
   → armazenar em referencias/

5. FICHAMENTO
   Conforme contrato_fichamento.md (a elaborar)
   → saída: anotação estruturada por artigo

6. ANÁLISE DE EVIDÊNCIA
   Mapear cada fichamento para H1/H2/H3/H4
   → classificar relação: confirma / refuta / neutro / misto
   → classificar força: direta / indireta / insuficiente
   → alimentar tabela-síntese e matriz evidência × hipótese
```

## Estratificação do corpus

Todo artigo avaliado recebe uma classificação de camada. A camada determina a
profundidade de fichamento e o uso no texto final.

| Camada | Descrição | Uso |
|---|---|---|
| **A — Núcleo** | Diretamente ligado à hipótese da frente; experimentos ou análise própria; WSN/IWN, ML/RL/DRL, overhead, MAC ou hotspot | Fichamento completo; evidência primária |
| **B — Suporte** | Surveys, protocolos industriais, trabalhos clássicos de energia/comunicação/arquitetura, ML sem WSN específico | Fichamento resumido; fundamentação teórica |
| **C — Excluído** | Segurança/IDS, VANET, IoT genérico, menção superficial ao tema | Registro de exclusão com justificativa obrigatória |

O arquivo de exclusões (C) é produto obrigatório de cada frente — é o que impede a
pergunta da banca: "você escolheu só artigos que confirmam a hipótese?"

O corpus anterior de 41 artigos do `versao_1_0` é reclassificado em A/B/C neste
sistema, sem necessidade de refichamento — os dados já existem.

## Critérios de inclusão

Aplicáveis a todas as frentes salvo indicação contrária:

1. Publicado no período definido para a frente
2. Idioma: inglês ou português
3. Tipo: artigo de periódico ou artigo de conferência
4. Texto completo acessível
5. Aborda explicitamente o tema da frente (verificado no título + abstract)

## Critérios de exclusão

1. Artigos que mencionam o tema apenas marginalmente (sem experimentos ou análise)
2. Surveys ou revisões (salvo se forem meta-análises relevantes para a frente)
3. Resumos expandidos sem texto completo
4. Duplicatas entre bases

_Critérios específicos por hipótese: a detalhar em cada ciclo de busca antes de
iniciar a triagem._

## Documentação obrigatória

Todo ato de pesquisa gera registro antes de ser executado:

| Ato | Registro |
|---|---|
| Executar busca | Entrada em `strings_busca.md` |
| Excluir registro | Motivo no campo `notas` da triagem |
| Alterar critério durante triagem | Issue em `issues.md` + atualização do contrato |
| Incluir base complementar | Justificativa em `strings_busca.md` + atualização deste contrato |

## Uso de ferramentas de IA

As ferramentas de IA (LLMs) são usadas para extração preliminar e triangulação de
leitura entre múltiplas ferramentas. As decisões finais são consolidadas por regras
explícitas definidas no `contrato_fichamento.md` e auditadas contra o texto integral
dos artigos.

A apresentação na qualificação e na tese deve ser:

> As ferramentas foram utilizadas para auxiliar a extração de dados e a detecção de
> inconsistências entre leituras. As decisões de classificação foram tomadas por
> regras documentadas e validadas contra o PDF original.

Nunca apresentar como "as ferramentas decidiram" ou "o modelo classificou".

## Padrão ouro de auditabilidade

Para cada afirmação relevante do texto final, deve ser possível responder:

1. De onde veio essa informação?
2. Qual artigo sustenta?
3. Como foi extraída (campo do fichamento)?
4. Qual ferramenta interpretou e como foi consolidado?
5. Foi auditado contra o PDF?
6. A hipótese é evidência direta ou inferência do pesquisador?

Se qualquer uma dessas perguntas não tiver resposta rastreável, a afirmação não pode
ser apresentada como evidência — deve ser marcada como inferência ou hipótese.

## Produto esperado

Para cada frente H1–H4:

1. **Tabela-síntese dos incluídos (camada A)**: técnica/abordagem, escala experimental,
   modelo de canal, overhead de controle modelado (sim/não), baseline comparado,
   relação com a hipótese (confirma/refuta/neutro/misto), força da evidência
   (direta/indireta/insuficiente).

2. **Arquivo de exclusões (camada C)**: registro de cada artigo excluído com
   justificativa por critério aplicado.

3. **Diagrama de triagem** (PRISMA-like): registros identificados → excluídos por
   critério → incluídos para fichamento → incluídos na análise final.

4. **Matriz evidência × hipótese**: síntese por H do que a literatura confirma,
   refuta ou deixa em aberto, com força da evidência.

## Requisitos de rigor derivados da qualificação

Os itens abaixo respondem diretamente às vulnerabilidades apontadas pelas análises
críticas do qualificacao_v3.tex (Claude e GPT, 2026-07-02):

| Vulnerabilidade | Requisito deste contrato |
|---|---|
| String não documentada | String exata registrada em `strings_busca.md` antes da execução |
| Data de consulta ausente | Data obrigatória em cada entrada do log |
| Critérios I/E informais | Critérios escritos antes de iniciar triagem de cada frente |
| Viés de sort por citação | Buscas por relevância temática, não por citação; janela temporal explícita |
| Base única sem justificativa | Scopus justificado; complementares documentados com motivo |
| Sem fluxograma de triagem | Diagrama PRISMA-like obrigatório por frente |
| Sem rastreabilidade de exclusão | Motivo de exclusão registrado por registro |
| Tabela-síntese ausente | Produto obrigatório de cada frente |
| H sem critério de refutação | Classificação confirma/refuta/neutro/misto + força direta/indireta/insuficiente |
| Uso de IA sem enquadramento | Regra explícita de apresentação do papel das ferramentas |
| Sem arquivo de exclusões | Camada C com justificativa é produto obrigatório |

## Changelog

| Data | Alteração |
|---|---|
| 2026-07-03 | Versão inicial |
| 2026-07-03 | Adicionados: estratificação A/B/C, força da evidência, enquadramento de IA, padrão ouro de auditabilidade |
