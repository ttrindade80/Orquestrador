---
name: nomenclatura-indice
description: Índice da base terminológica modular — localiza módulos proprietários, explica leitura seletiva e serve como ponto de entrada da navegação terminológica
metadata:
  type: nomenclatura
  scope: indice
  fase_de_aplicacao: VIGENTE
---

# Índice — Nomenclatura modular

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
funcao: indice_e_roteador
nao_proprietario_de_definicoes: true
dependencias_dos_contratos_materializadas: true
leitura_seletiva_ativa: true
leitura_preventiva_de_todos_os_modulos: PROIBIDA
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

Este índice é o ponto de entrada para localizar módulos proprietários.
Ele **não é proprietário de definições terminológicas** — cada definição
vive no módulo proprietário do seu domínio.
Este índice **não mantém lista normativa independente de dependências** dos
contratos. Os contratos declaram suas próprias dependências; este índice
serve como visão de navegação derivada.
A leitura deve partir do contrato ou da atividade — **não da leitura integral
de todos os módulos** (D-NOM-03, ADR-0029).
`docs/NOMENCLATURA.md` é a fachada permanente de compatibilidade e navegação.

## 2. Propósito deste índice

Este índice localiza o módulo proprietário de cada domínio terminológico.
Ele não redefine termos. Ele não duplica definições. Ele não mantém lista
normativa independente de dependências dos contratos.

Quando um termo necessário não estiver nos módulos já carregados:
1. Consultar este índice.
2. Localizar o módulo proprietário do domínio.
3. Carregar somente esse módulo.
4. Não carregar todos os módulos preventivamente.

## 3. Leitura seletiva

A leitura seletiva parte do artefato ou contrato alvo da atividade, não da
leitura preventiva de todos os módulos.

```yaml
ordem_de_leitura:
  1: ler a documentação inicial do processo (docs/INDICE.md)
  2: consultar este índice
  3: ler docs/nomenclatura/01_NUCLEO_COMUM.md
  4: identificar o artefato ou contrato alvo da atividade
  5: ler os módulos obrigatórios e condicionais declarados pelo contrato alvo
  6: consultar módulo adicional somente quando um termo necessário ainda não estiver carregado
```

**Módulo obrigatório**: deve ser lido em toda atividade que envolva terminologia
do sistema novo.

**Módulo condicional**: deve ser lido somente quando a atividade envolver o
domínio coberto por aquele módulo.

As dependências individuais de cada contrato foram declaradas em cada contrato
na FASE_2 da ADR-0029 (2026-07-21). Este índice apresenta a visão de navegação
por domínio; a lista autoritativa de módulos requeridos está em cada contrato.

## 4. Módulos obrigatórios

| Módulo | Domínio |
|---|---|
| `01_NUCLEO_COMUM.md` | Conceitos transversais a todos os módulos |

## 5. Módulos por domínio

### 5.1 Configuração e runtime

| Módulo | Domínio |
|---|---|
| `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` | Artefatos de configuração, diferença schema/dados/runtime, separação demo/produto |

### 5.2 Estilo

| Módulo | Domínio |
|---|---|
| `10_ESTILO.md` | Estilo universal, aparência, bordas, chips visuais, cores, tiling como preferência global |

### 5.3 Tela, corpo e layout

| Módulo | Domínio |
|---|---|
| `20_TELA_CORPO_E_COMPOSICAO.md` | Tela e regiões, elementos funcionais, containers, composição genérica |
| `21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md` | Dimensões, largura, altura, redimensionamento reativo, paginação |

### 5.4 Componentes da tela

| Módulo | Domínio |
|---|---|
| `30_CABECALHO.md` | Cabeçalho, título, descrição, schema de apresentação |
| `31_BARRA_DE_MENUS_E_CHIPS.md` | Barra de menus, chips canônicos e específicos, distribuição da barra |
| `32_CONSOLE.md` | Console como container interativo, cursor, seleção, lote, partes do item |
| `33_LANCADOR.md` | Lançador, itens de navegação, fila, matriz, grandezas de largura |
| `34_DASHBOARD.md` | Dashboard, saída passiva, marcadores, campos de resumo |

### 5.5 Distribuição de área e grupos

| Módulo | Domínio |
|---|---|
| `40_GRUPOS_E_DISTRIBUICAO_DE_AREA.md` | Grupo como nó estrutural, profundidade, distribuição entre filhos, espaço externo |
| `41_DISTRIBUICAO_MATRICIAL.md` | Distribuição matricial de nível único dos participantes imediatos de um elemento |

### 5.6 Dados externos e apresentações multinível

| Módulo | Domínio |
|---|---|
| `42_DADOS_EXTERNOS_MULTINIVEL.md` | JSON estrutural vs externo, envelope declarativo, níveis, produtor, consumidor |
| `43_CARREGAMENTO_E_ASSOCIACAO_DE_CONTEUDO.md` | Ponto de entrada, carregamento separado, associação externa, loader, fixture |
| `44_APRESENTACOES_E_MODOS_MULTINIVEL_DO_CONSOLE.md` | Apresentações (tabela, hierarquia, conjuntos_campos), modos verboso/não verboso, política de modo |

### 5.7 Aliases e termos descontinuados

| Módulo | Domínio |
|---|---|
| `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` | Aliases transicionais, termos descontinuados, histórico de substituições |

## 6. Como localizar um termo não carregado

1. Identificar o domínio conceitual do termo.
2. Localizar o módulo proprietário na seção 5 acima.
3. Ler somente esse módulo.
4. Se o termo não aparecer no módulo esperado, verificar `90_ALIASES_E_TERMOS_DESCONTINUADOS.md`
   para identificar se é alias ou termo descontinuado.
5. Não carregar todos os módulos para resolver o termo.

## 7. Dependências dos contratos

As listas de `dependencias_obrigatorias` e `dependencias_condicionais` de cada
contrato foram materializadas na FASE_2 da aplicação da ADR-0029 (2026-07-21).
Cada contrato declara nominalmente os módulos de nomenclatura que requer.

Para identificar os módulos necessários para uma atividade:
1. Localizar o contrato alvo da atividade.
2. Ler as `dependencias_obrigatorias` e as `dependencias_condicionais` aplicáveis.
3. Carregar somente esses módulos.

Os roteiros de leitura seletiva demonstrativos estão em
`docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-1.md`, seção 15.6.
O relatório de aplicação da FASE_2 está em
`docs/relatorios/RELATORIO_APLICACAO_ADR-0029_FASE-2.md`.
