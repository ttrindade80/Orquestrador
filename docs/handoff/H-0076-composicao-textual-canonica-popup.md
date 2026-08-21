---
name: H-0076-composicao-textual-canonica-popup
description: Implementação do núcleo canônico de composição textual e migração exclusiva do popup
metadata:
  type: handoff
  id: H-0076
  item: ITEM-0027
  adr: ADR-0049
  qa_adr: ADR_APPROVED
  qa_aplicacao: ADR_APPLICATION_APPROVED
  estado: CONCLUIDO
  decisao_aplicada: D-0027-10
  handoff_patch: P01
  qa_handoff: H1_HANDOFF_APPROVED
  implementacao_patch: P02
  qa_implementacao: I1_IMPLEMENTATION_APPROVED
  regressao_final: 91_passed
  validacao_manual: MANUAL_VALIDATION_APPROVED
  handoffs_planejados_total: 2
---

# H-0076 — Composição textual canônica e migração do popup

## 1. Objetivo e unidade de trabalho

Implementar o núcleo canônico de composição textual da TUI e migrar
exclusivamente o popup para consumi-lo. A unidade inclui o mecanismo comum,
integração inicial, testes unitários do núcleo e regressão do popup.

O núcleo deve receber o parágrafo lógico completo e formar suas linhas a
partir de palavras inteiras. A unidade lógica não muda quando a largura muda:
cada recomposição parte novamente do texto lógico completo, nunca de linhas
físicas previamente produzidas. O popup permanece o consumidor focal deste
handoff.

Este handoff não implementa a migração transversal do caminho de conteúdo
externo nem de seus consumidores. O resultado deve preservar a composição
declarativa, o schema, os dados, a geometria própria, a formação dos itens,
as bordas, os chips, o estado vivo e demais semânticas específicas do popup.

## 2. Autoridades e fronteiras de decisão

Ordem de autoridade:

1. `docs/adr/ADR-0049-composicao-justificacao-global-texto-tui.md`;
2. `docs/contratos/contrato_composicao_textual.md`;
3. `docs/nomenclatura/01_NUCLEO_COMUM.md` e
   `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`;
4. `docs/relatorios/RELATORIO_LEVANTAMENTO_COMPOSICAO_JUSTIFICACAO_GLOBAL_ITEM-0027.md`,
   somente como evidência factual da implementação atual.

A decisão executiva aplicada neste patch é D-0027-10. A localização
executiva futura deste handoff é o novo arquivo
`tela/renderizacao/composicao_textual.py`. A escolha não altera ADR,
contrato ou nomenclatura como regra arquitetural geral.

Não criar fachada, registry, classe abstrata, plugin, adapter ou outra camada
estrutural. O módulo deve materializar uma única implementação da capacidade;
assinatura e organização interna podem ser escolhidas na implementação,
desde que não sejam promovidas a API pública global não definida pelo
contrato.

## 3. Escopo autorizado

### Arquivos futuros autorizados

Criar:

- `tela/renderizacao/composicao_textual.py`;
- `tela/teste_composicao_textual.py`;
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0076.md`.

Alterar funcionalmente:

- `tela/renderizacao/composicao_textual.py`;
- `tela/renderizacao/popup.py`;
- `tela/teste_composicao_textual.py`;
- `tela/teste_popup.py`;
- `demo/teste_demo_popup.py`.

Alteração condicional:

`tela/renderizacao/texto_ansi.py` somente se estritamente necessária para
reutilizar ou tornar coerentes as primitivas ANSI existentes. Se o núcleo
puder reutilizá-las sem alteração, o arquivo permanece intacto.

### Preservar integralmente

Não alterar neste handoff:

- `tela/renderizacao/conteudo_externo.py`;
- `tela/renderizacao/matriz_participantes.py`;
- `tela/renderizacao/paginacao_interna.py`;
- `tela/renderizacao/console.py`;
- `tela/renderizador.py`;
- `tela/renderizacao/barra_menus.py`;
- `tela/renderizacao/lancador.py`;
- `tela/renderizacao/estilo.py`;
- contratos, ADRs, nomenclatura e backlog.

Qualquer arquivo estritamente necessário que não esteja autorizado exige
parada antes da alteração e pedido focal contendo caminho, motivo, mudança e
impacto da não autorização.

## 4. Semântica executiva do núcleo

O núcleo transforma o parágrafo lógico completo em uma sequência ordenada de
linhas físicas, recebendo largura útil efetiva positiva e o modo solicitado
pelo consumidor.

As linhas devem ser formadas por palavras inteiras que caibam na largura útil,
preservando a ordem e o conteúdo. Palavras são unidades indivisíveis para o
compositor: ele não pode dividi-las, alterá-las para fazê-las caber, inserir
hífen, fazer hifenização automática, fazer separação silábica ou realizar
divisão arbitrária por largura visual. Pontuação anexada a uma palavra não
deve ser destacada arbitrariamente apenas para satisfazer a largura.

Se uma palavra individual for maior que a largura útil, o compositor somente
deve mantê-la sem divisão e sem alteração semântica. Este handoff não decide
clipping, overflow, scroll horizontal, erro, fallback, truncamento ou
expansão de container. Se o consumidor ou renderer já tiver comportamento
físico para essa situação, ele pode permanecer atuando, desde que o núcleo
não altere a palavra.

Não existe neste handoff política global para whitespace ou separadores
arbitrários. Não introduzir regra genérica de preservação literal,
normalização, condensação, trimming, tabs ou separadores estruturais. Na
justificação de parágrafo, os pontos de expansão são os vãos entre palavras
da mesma linha.

A justificação só ocorre depois da formação das linhas e somente no modo
solicitado pelo consumidor. Sua expansão atua nos vãos entre palavras das
linhas às quais ela se aplica, sem cortar palavras e sem alterar prefixos,
indicadores, margens, colunas ou padding estrutural. O handoff permanece
neutro quanto à última linha: não exige justificá-la, não justificá-la,
expandí-la, não expandí-la nem qualquer tratamento algorítmico especial. Um
parâmetro histórico da API relativo à última linha, se existir, não vira
requisito normativo comum; compatibilidade local do popup deve ser classificada
como comportamento do consumidor.

O núcleo deve recompor o parágrafo inteiro após qualquer mudança de largura.
Linhas físicas anteriormente renderizadas nunca são entrada lógica da
recomposição seguinte. A saída deve preservar ordem, conteúdo, palavras e
estado ANSI, sem perda ou duplicação.

## 5. ANSI e largura visual

Usar as primitivas existentes de `tela/renderizacao/texto_ansi.py` sempre que
forem suficientes. A largura deve ser calculada por células visuais;
sequências de controle ANSI suportadas não ocupam células e nenhuma sequência
CSI pode ser partida parcialmente na formação das linhas. O estado SGR deve
ser fechado, preservado ou restabelecido entre linhas/regiões sem vazamento
indevido. Não criar política de cores, estilo ou interpretação ANSI além da
segurança necessária para o conteúdo já suportado pela TUI.

## 6. Migração exclusiva do popup

Substituir no popup a autoridade local equivalente de composição e a
autoridade local equivalente de justificação pelo núcleo. O popup deve
fornecer ao núcleo o texto lógico completo do parágrafo, inclusive quando
resize ocorrer, e usar a mesma composição para obter as linhas consumidas e
para renderizar a saída.

Não manter implementação local concorrente de wrap ou justificação de
parágrafo. O popup pode conservar regras próprias de margem, prefixo,
indicadores, chips, itens, formação, caixa, overlay, moldura, largura útil,
geometria e decisão de modo. Essas responsabilidades permanecem no
consumidor e não são transferidas ao núcleo.

Não tocar no caminho de conteúdo externo. Em particular, a autoridade local
de `tela/renderizacao/conteudo_externo.py` permanece fora deste handoff.

## 7. Testes futuros do núcleo

Criar `tela/teste_composicao_textual.py` com testes diretos para:

- duas ou mais palavras que não caibam juntas passarem para linhas diferentes;
- nenhuma palavra ser dividida somente para satisfazer a largura;
- pontuação anexada à palavra não ser arbitrariamente destacada pela largura;
- o mesmo texto lógico completo ser recomposto em larguras diferentes, sem
  reutilizar a saída de uma largura como entrada da largura seguinte;
- uma palavra maior que a largura permanecer sem divisão e sem alteração,
  sem testar clipping, overflow, scroll, erro, fallback, truncamento ou
  expansão de container;
- a justificação ocorrer depois da formação das linhas, atuar nos vãos entre
  palavras e não cortar palavras;
- não haver expectativa normativa sobre última linha, distribuição
  matemática específica, lado que recebe resto ou algoritmo de espaços
  excedentes;
- largura visual ANSI, CSI indivisível, estado SGR e palavras estilizadas sem
  corrupção.

Os testes devem preservar a distinção entre composição de parágrafo,
justificação e padding/alinhamento estrutural. Não prescrever tokenizador
sofisticado nem regra linguística de pontuação além do necessário para não
cortar palavras.

Atualizar `tela/teste_popup.py` para regressão da migração, mantendo as
semânticas próprias do popup. Atualizar `demo/teste_demo_popup.py` para
recomposição após alteração de largura, restauração da largura e preservação
da instância/estado.

## 8. Teste de reprodução e aceite futuro

Os testes ou verificações reproduzíveis devem cobrir um popup com parágrafo
longo justificado, largura larga, redução progressiva da largura, passagem de
uma distribuição de linhas para outra e retorno à largura original. Devem
demonstrar:

1. nenhuma palavra partida;
2. parágrafo inteiro recomposto em cada largura;
3. nenhuma perda ou duplicação de palavras;
4. justificação aplicada às linhas resultantes depois da formação;
5. nenhuma dependência de linhas físicas antigas;
6. moldura e geometria preservadas;
7. ANSI preservado;
8. `popup.py` usando o núcleo sem autoridade local concorrente;
9. medição de linhas e renderização consumindo composição coerente;
10. `conteudo_externo.py` não alterado nem migrado.

O cenário preparado `h0077_texto_amplo_justificado` deve ser usado como
validação manual posterior do popup. Esta etapa não altera a demo. A
validação deverá confirmar visualmente palavras inteiras, recomposição global
do parágrafo e justificação coerente em resize.

Na implementação futura, executar:

```zsh
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q \
  tela/teste_composicao_textual.py \
  tela/teste_popup.py \
  demo/teste_demo_popup.py
```

O relatório de implementação futuro deve registrar somente arquivos
criados/alterados, núcleo, integração do popup, eventual alteração e motivo
em `texto_ansi.py`, testes, demonstração, desvios e bloqueios, em no máximo
900 palavras, no arquivo exatamente
`docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0076.md`.

## 9. Separação do H-0077

O H-0077 não é reconciliado nesta etapa. Consumidores externos dependerão da
nova semântica canônica de palavras indivisíveis, parágrafo completo e
recomposição por largura, e precisarão de regressão posterior quando o núcleo
corrigido de H-0076 estiver aprovado.

Não migrar, antecipar ou alterar funcionalmente consumidores H-0077 neste
patch. H-0076 termina com o mecanismo canônico, a integração do popup e sua
cobertura focal.

## 10. Bloqueios

Nenhum bloqueio documental para este patch. A implementação do núcleo, os
testes futuros, a validação manual posterior e a reconciliação de H-0077
permanecem etapas posteriores.
