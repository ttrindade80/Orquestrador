---
name: nomenclatura-apresentacoes-e-modos-multinivel-do-console
description: Terminologia das apresentações e modos multinível do console — apresentação por tela, modo verboso, modo não verboso, D23, política de modo, divergência terminológica preservada
metadata:
  type: nomenclatura
  scope: apresentacoes_modos_multinivel_console
  fase_de_aplicacao: VIGENTE
---

# Apresentações e modos multinível do console

## 1. Estado

```yaml
fase_de_aplicacao: VIGENTE
fonte_normativa_do_dominio: este_modulo
fachada_de_navegacao: docs/NOMENCLATURA.md
substituicao_de_autoridade_executada: true
auditoria_pre_fachada_aprovada: true
```

## 2. Responsabilidade

Este módulo é proprietário de:
- apresentação como configuração por tela do console;
- modo verboso e modo não verboso;
- D23 (decisão sobre política de modo);
- política de modo declarada;
- divergência terminológica entre `modo normal` e `modo não verboso` — documentada
  como pendência não resolvida, preservada sem reconciliação.

Este módulo **preserva a divergência terminológica** entre documentos sem resolver.
A decisão de reconciliação está deferida (ADR-0028); qualquer resolução requer
nova ADR.

## 3. Termos proprietários

- apresentação (configuração do console por tela)
- apresentações multinível
- modo verboso
- modo não verboso
- `modo normal` (termo alternativo com divergência ativa — ver seção 4.4)
- D23 (decisão sobre política de modo)
- política de modo declarada
- modo por tela
- modo padrão da tela
- modo configurável

## 4. Definições

### 4.1 Apresentação (ADR-0028)

`apresentação` é a configuração específica de como o console exibe seu conteúdo
em uma tela particular. Cada tela pode declarar uma apresentação diferente para
o mesmo console.

**Apresentações multinível**: capacidade de declarar apresentações distintas por
nível da hierarquia de dados, por tela.

### 4.2 Modo verboso

`modo verboso` é o modo de exibição do console em que todos os campos semânticos
do nível são apresentados na linha do item. Exibe mais informação por linha.

### 4.3 Modo não verboso

`modo não verboso` é o modo de exibição do console em que apenas os campos
essenciais são apresentados na linha do item. Exibe menos informação por linha
e é mais compacto.

### 4.4 Divergência terminológica: `modo normal` × `modo não verboso`

**Esta divergência está documentada e preservada. Não foi reconciliada.**

| Uso | Termo | Fonte |
|---|---|---|
| Modo de exibição padrão/compacto | `modo não verboso` | §19 do monólito; uso predominante |
| Mesmo conceito em alguns contextos | `modo normal` | Uso alternativo presente em documentos históricos |

A ADR-0028 registra a política de modo mas não resolveu a divergência
terminológica entre `modo normal` e `modo não verboso`. Os dois termos coexistem
nos documentos com o mesmo referente. Qualquer reconciliação requer nova ADR.

**Regra de leitura**: ao encontrar `modo normal` em contexto de apresentação do
console, interpretar como `modo não verboso` até que nova ADR resolva a divergência.
Ao encontrar `modo não verboso`, não reescrever como `modo normal`.

### 4.5 D23 e política de modo (ADR-0028)

**D23** é a decisão que estabelece a política de modo para apresentações do console:
- O modo por tela é declarado no schema da tela.
- O modo padrão pode ser sobrescrito por tela.
- A apresentação é configurável por nível.

| Termo | Definição |
|---|---|
| `D23` | Identificador da decisão sobre política de modo (ADR-0028) |
| `política de modo` | Conjunto de regras que determina qual modo é usado em cada tela e nível |
| `modo por tela` | Declaração de modo vinculada à tela específica, não ao console em si |
| `modo padrão da tela` | Modo declarado na tela quando nenhum override por nível está presente |
| `modo configurável` | Modo que pode ser sobrescrito por configuração de tela |

## 5. Distinções obrigatórias

| Par | Distinção normativa |
|---|---|
| `apresentação` × `configuração do console` | Apresentação: configuração por tela de como o console exibe o conteúdo; configuração do console: campos do JSON do console em `contrato_json_console.md` |
| `modo verboso` × `modo não verboso` | Modos opostos de densidade de informação na linha do item — não são modos de erro nem de fallback |
| `modo não verboso` × `modo normal` | Divergência ativa: ambos referenciam o mesmo conceito; reconciliação deferida para nova ADR (ADR-0028) |
| `apresentação por tela` × `schema semântico` | Apresentação por tela: como o dado é exibido; schema semântico (módulo 42): o que o dado significa |
| `apresentações multinível` × `carregamento conjunto` | Apresentações multinível (ADR-0028): como o dado é exibido em cada nível; carregamento conjunto (ADR-0027): como múltiplos envelopes são associados — módulo `43` |

## 6. Relação com contratos

- `contrato_console.md`: autoridade do comportamento normativo das apresentações
  e dos modos do console.
- `contrato_json_console.md`: schema dos campos de apresentação e modo no JSON do console.

## 7. Relação com ADRs

- ADR-0028: apresentações multinível; D23; política de modo por tela.
- ADR-0026: dado externo que alimenta as apresentações (parcial — dado em si no módulo 42).
- ADR-0027: carregamento conjunto que precede as apresentações (parcial — carregamento no módulo 43).

## 8. Aliases ou termos descontinuados relacionados

- `modo normal` — **não é descontinuado**: está ativo em documentos históricos
  e coexiste com `modo não verboso` com divergência não resolvida. Não registrar
  como descontinuado até que nova ADR resolva. Ver seção 4.4.

## 8A. Termos concorrentes deferidos

O termo abaixo aparece em fontes primárias deste domínio mas **não é termo
canônico ativo confirmado**. Registra diferença terminológica ainda não
reconciliada. Não integra a contagem de termos ativos.

| Termo | Correspondência atual no schema | Estado | Localização no módulo `90` |
|---|---|---|---|
| `hierarquia_indentada` | `hierarquia` (campo do schema de apresentação) | TERMO_CONCORRENTE_DEFERIDO | ver `90_ALIASES_E_TERMOS_DESCONTINUADOS.md` |

A reconciliação entre `hierarquia_indentada` e `hierarquia` está deferida
(ADR-0028). Nenhum dos dois nomes venceu definitivamente a disputa. Os campos
do schema não devem ser renomeados com base neste termo concorrente.

## 9. Conteúdo que não pertence a este módulo

- O envelope de dados externo em si → módulo `42`.
- Carregamento e associação do envelope → módulo `43`.
- Schema do JSON do console (campos de configuração) → `contrato_json_console.md`.
- Regras comportamentais completas de apresentação → `contrato_console.md`.
- Reconciliação da divergência `modo normal` × `modo não verboso` → aguarda nova ADR.

## 10. Proveniência da migração

```yaml
origem_no_monolito:
  secao: "§19 (linhas 1721-1856)"
  intervalo_ou_bloco: "NOM-LEV-027, NOM-LEV-028"
origem_normativa: ADR-0028
contratos_relacionados:
  - contrato_console.md
  - contrato_json_console.md
adrs_relacionadas:
  - ADR-0026
  - ADR-0027
  - ADR-0028
tratamento:
  - PRESERVADO
  - SEPARADO_DE_REGRA_COMPORTAMENTAL
partes_NAO_CONFIRMADAS:
  - "Divergência 'modo normal' × 'modo não verboso': dois termos coexistentes para o mesmo conceito, reconciliação deferida para nova ADR (ADR-0028 registra mas não resolve)"
```
