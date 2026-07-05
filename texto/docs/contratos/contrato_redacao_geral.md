---
name: contrato-redacao-geral
description: Regras universais de redação acadêmica aplicáveis a qualquer texto produzido neste projeto — língua portuguesa, rigor de conteúdo, elementos flutuantes e fluxo de trabalho
metadata:
  type: contrato
  scope: texto
---

# Contrato de Redação — Geral

Template reutilizável. Textos específicos (qualificação, artigo, tese) herdam estas
regras e adicionam contratos próprios em seu `docs/contratos/`.

## Língua portuguesa

### Regras gramaticais (AO90)

| Erro frequente | Forma correta | Regra |
|---|---|---|
| `onde` após equação ou em contexto não-espacial | `em que` | "onde" reservado para lugar físico |
| `contra-exemplos` | `contraexemplos` | prefixo + vogal diferente sem hífen |
| `não-estacionariedade` | `não estacionariedade` | "não" advérbio sem hífen |
| `fim-a-fim` | `fim a fim` | locução sem hífen (como "dia a dia") |
| vírgula ausente após "por exemplo" | `por exemplo,` | — |
| `esta tese` em proposta/qualificação | `esta proposta de tese` | documento é proposta, não tese concluída |

### Siglas e abreviaturas

- Expandir **uma vez no resumo** e **uma vez no corpo** do texto; depois apenas a sigla
- Nunca expandir novamente no mesmo nível de texto
- Evitar concentrar mais de quatro siglas em uma frase

### Estrangeirismos

- Definir no primeiro uso: `sobrecarga de controle (\textit{overhead})`
- Escolher uma forma predominante e manter até o fim
- Itálico: aplicar consistentemente — se `overhead` não leva itálico por decisão de
  aportuguesamento, nenhum uso leva; se leva, todos levam

### Maiúsculas em termos técnicos

- Em texto corrido: minúsculas (`aprendizado de máquina`, `aprendizado por reforço`)
- Em títulos de seção ou como parte de sigla: conforme convenção da área
- Manter a escolha consistente em todo o documento

### Separador decimal

- Sempre vírgula em texto em português: `45,3%`, `0,5`
- Nunca ponto decimal em tabelas cujo texto é português

## Rigor de conteúdo

### Padrão ouro de afirmações

Antes de incluir qualquer afirmação relevante no texto, verificar:

1. De onde veio essa informação?
2. Qual artigo sustenta?
3. Como foi extraída (campo do fichamento)?
4. Foi auditada contra o PDF?
5. É evidência direta ou inferência do pesquisador?
6. Se inferência — está marcada como tal?

Afirmações sem resposta rastreável para os itens 1–4 são marcadas como inferência
ou hipótese, nunca apresentadas como fato da literatura.

### Símbolos matemáticos

- Cada símbolo tem um único significado em todo o documento
- Colisões proibidas: se γ é fator de desconto em RL, não pode ser peso de penalidade
  na recompensa — renomear para λ, w ou outro símbolo livre
- Tuplas formais (ex.: MDP) usam a definição canônica completa da referência adotada

### Escolhas metodológicas

- Nenhuma escolha relevante fica em aberto no texto final: não "NS-3 ou OMNeT++",
  mas "NS-3 (justificativa)" ou "OMNeT++ (justificativa)"
- Se a escolha depende de estudo piloto, escrever o critério de decisão, não a dúvida

### Afirmações absolutas

- Evitar "garantindo", "ausentes", "garantido" para fenômenos probabilísticos
- Substituir por: "preservando", "raras", "alto" (ou equivalente qualificado)

### Redundâncias

- Definições, afirmações e exemplos aparecem uma vez; nas demais ocorrências, usar
  referência cruzada (`\ref{...}`)
- Três ou mais ocorrências idênticas indicam necessidade de consolidação

## Tipografia LaTeX

### Travessão — proibido no texto visível

Regra prevalente: não introduzir travessão (`—`, `---`) em nenhuma parte do
texto acadêmico (corpo, títulos, legendas, enumerações, hipóteses, objetivos).

| Caso | Substituição |
|---|---|
| Aparte curto no meio da frase | vírgulas: `X, explicação, Y.` |
| Aparte longo com vírgulas internas | duas frases separadas |
| Título com separador | dois-pontos ou parênteses |
| Enumeração `termo — explicação` | `termo, expressão nominal` |

Preservar sem alteração: `--` para intervalos (`10--20`), `-` para compostos,
sinal matemático de subtração, separadores de comentário LaTeX (`% ---`).

Verificação: `rg -n --fixed-strings -- "---" arquivo.tex` — aceito somente
em comentários.

### `\textbf{}` no corpo do texto

| Caso | Ação |
|---|---|
| Título, cabeçalho, tabela, legenda, macro do template | preservar |
| Ênfase retórica no corpo do parágrafo | remover |
| Termo realmente definido naquele ponto | substituir por `\emph{}` |
| Resíduo de conversão `**markdown**` | remover |

### Parênteses

Preservar quando contiverem: sigla na primeira ocorrência, unidade, métrica,
variável, símbolo, referência cruzada, citação, termo técnico, condição
experimental, intervalo ou observação técnica indispensável.

Revisar apenas "apostos de recheio": parêntese que repete ou dilui a frase
sem acrescentar conteúdo técnico (`(ou seja, ...)` redundante).

### Hífen como separador de oração

`texto - aparte - texto` é erro tipográfico — reescrever com vírgulas ou
trocar por `---` (mas `---` também é proibido no corpo — logo: reescrever).

### Regra de decisão tipográfica

```
classificar → proteger → preservar em dúvida → corrigir só o que é seguramente não técnico
```

Nunca corrigir marca gráfica antes de verificar se ela cumpre função técnica,
matemática, estrutural ou autoral deliberada.

## Elementos flutuantes

### Figuras

- Toda figura referenciada no texto com `\ref{fig:...}` antes de aparecer
- Legenda autoexplicativa — a figura deve ser compreensível sem ler o parágrafo
- Fonte obrigatória (mesmo que "elaborado pelo autor")

### Tabelas

- Separador decimal: vírgula
- Cabeçalhos descritivos (não apenas siglas)
- Itens de `enumerate` relevantes recebem `\label` para permitir `\ref` — evitar
  numeração manual que quebra silenciosamente se a ordem mudar

### Equações

- Espaçamento com `\;` — nunca `;` literal dentro de ambiente matemático
- Variáveis definidas logo após a equação com "onde" substituído por "em que"
- Toda equação referenciada no texto

## Tom e consistência narrativa

### O que nunca fazer
- Linguagem avaliativa negativa sobre trabalhos individuais: não "os autores
  ignoram X", "a literatura falha em Y"
- Substituir por: "X não é abordado nesta linha", "abre-se espaço para Y"
- "garantindo", "ausentes", "garantido" para fenômenos probabilísticos →
  "preservando", "raras", "alto"

### O que sempre fazer
- Citar livros para fatos estabelecidos (princípios, definições, algoritmos
  canônicos)
- Citar artigos para resultados numéricos específicos e para baselines
- Encerrar cada seção com frase que conecta ao que vem a seguir (ponte narrativa)
- Escolher um termo técnico e mantê-lo em todo o documento — não alternar
  entre sinônimos (ex: "gerenciador externo" — não usar "controlador",
  "agente", "orquestrador" alternadamente)

## Uso de ferramentas de IA

**Status: pendente** — ver `metodologia/docs/issues.md` [I001].

Enquadramento proposto (aplicar após aval do orientador):

> As ferramentas de inteligência artificial foram utilizadas para auxiliar a extração
> preliminar de dados e a triangulação de leituras entre múltiplas ferramentas. As
> decisões de classificação e as afirmações do texto foram consolidadas por regras
> documentadas e validadas contra o texto integral dos artigos pelo pesquisador.

Nunca usar: "as ferramentas decidiram", "o modelo classificou", "segundo a IA".

## Fluxo de trabalho

- Claude gera texto sugerido com LaTeX pronto e indica o ponto exato de inserção
- Usuário aplica com modificações próprias de voz, precisão e estilo
- Edição direta no arquivo `.tex` apenas quando explicitamente solicitado
- Padrões de melhoria do usuário a preservar:
  - Frases longas → duas sentenças curtas
  - Abertura genérica → abertura direta com autor ("Yildiz et al. mostram que...")
  - "independentes" → "complementares" quando os mecanismos se reforçam
  - "forçando" → "podendo gerar" para relações probabilísticas

## Changelog

| Data | Alteração |
|---|---|
| 2026-07-03 | Versão inicial |
