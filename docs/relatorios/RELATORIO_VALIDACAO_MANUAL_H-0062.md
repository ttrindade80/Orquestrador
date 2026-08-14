# Relatório de validação manual H-0062

## rastreabilidade

```yaml
etapa: VALIDACAO_MANUAL
objeto: H-0062
predecessor: docs/relatorios/RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0062_P01.md
```

## resultado

```yaml
status: VALIDACAO_MANUAL_REPROVADA
gates_avaliados:
  - QA-H0062-MANUAL-001
  - QA-H0062-MANUAL-002
```

Os requisitos automatizáveis anteriormente aprovados não são reclassificados
por esta etapa. A validação manual falhou. H-0062 não pode ser considerado
aprovado ou concluído; a reprovação é material e impede o fechamento do
handoff em seu formato atual.

## achados_manuais

### VM-H0062-001 — estrutura incorreta da tela

- descricao: A tela de seleção de Estilo está abrindo/aparecendo como se fosse um popup.
- esperado: A seleção de Estilo deve ser uma tela normal do sistema, contendo Cabeçalho, Console e Barra de Menus. O popup pertence somente à futura confirmação da aplicação do estilo.
- observado: A tela de seleção de Estilo apareceu como se fosse um popup.

### VM-H0062-002 — navegação em dois níveis não funcional

- descricao: A navegação em dois níveis não está funcionando adequadamente.
- esperado: O console da tela de Estilo deve permitir navegação multinível funcional entre as categorias e seus respectivos presets, conforme a política canônica do projeto.
- observado: A navegação em dois níveis não funcionou adequadamente.

### VM-H0062-003 — resize quebra a exibição

- descricao: Ao redimensionar o terminal, a exibição quebra.
- esperado: A tela deve se recompor corretamente ao resize, preservando sua estrutura, conteúdo navegável e apresentação dentro das dimensões disponíveis.
- observado: Ao redimensionar o terminal, a exibição quebrou.

## decisao_gerencial

```yaml
continuar_patches_amplos_h0062: false
reparticionar_trabalho: true
proxima_acao_documental:
  - determinar o estado canônico para substituir/suplantar H-0062
  - somente depois criar novo handoff
```

O trabalho restante deverá ser reparticionado em handoffs menores. Primeiro
deverá ser construída e validada a tela estrutural, com seus níveis visíveis e
navegação multinível. Funcionalidades posteriores serão reparticionadas
somente depois dessa base funcionar. Esta decisão não cria, numera ou substitui
handoff, nem define o termo documental canônico dessa substituição.

## bloqueios

```yaml
bloqueios: []
```
