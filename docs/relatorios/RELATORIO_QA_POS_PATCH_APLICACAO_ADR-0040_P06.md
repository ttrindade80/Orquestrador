---
name: REL-QA-POS-PATCH-APLICACAO-0040-P06
description: QA independente da aplicação documental P06 da ADR-0040
metadata:
  type: relatorio_qa
  status: ADR_APPLICATION_REJECTED
  data: 2026-08-05
---

# Relatório QA pós-patch de aplicação — ADR-0040 P06

```yaml
cadeia:
  raiz: docs/relatorios/RELATORIO_APLICACAO_ADR-0040.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_APLICACAO_ADR-0040_P06.md
achados_retestados:
  - QA-H0050-03
  - QA-H0050-04
  - QA-H0050-09
decisoes_auditadas:
  - D-DRY-10
  - D-DRY-11
```

## Resultado por achado

- `QA-H0050-03`: resolvido. `controle_execucao` é objeto raiz opcional fechado,
  com exatamente `modo_inicial`, sem default, com enumeração fechada e rejeição
  de propriedades internas adicionais.
- `QA-H0050-04`: resolvido. A compatibilidade pertence à implementação
  registrada; `categoria` é obrigatória e fechada em `processo`, `navegacao` e
  `visualizacao`.
- `QA-H0050-09`: resolvido. Ações de processo declaram
  `modos_execucao_aceitos`, com valores fechados; registro ausente ou
  insuficiente falha de forma fechada. A ressalva autorizada para navegação e
  visualização foi preservada.

## Fechamento material

O contrato da tela separa configuração concreta e runtime, não cria campo de
compatibilidade nem atribui categoria à tela. A elegibilidade exige resolução
autoritativa de todas as ações relevantes; processo deve aceitar os dois modos,
enquanto navegação e visualização ficam fora dessa exigência. O contrato do
registro é semântico e independente da arquitetura física, não cria dispatcher,
registry físico obrigatório, protocolo público ou migração global. Também não
obriga presença ou ausência de `modos_execucao_aceitos` para navegação e
visualização, nem atribui semântica nova a esse campo nessas categorias.

O JSON do console mantém as referências vigentes e não declara categoria ou
compatibilidade. O console somente referencia ou aciona ações; o modo capturado
acompanha a requisição e o lote reconciliado quando aplicável, sem integrar a
identidade do lote. Captura imutável, executor sem consulta à interface e
representação interna reversível permanecem preservados. Foco, cursor, seleção
e paginação não foram alterados.

As nomenclaturas 02 e 32 registram as fronteiras requeridas sem escolher módulo
físico, atribuir compatibilidade à tela ou exigir migração. O índice contém
ADR-0040 uma única vez, com estado aceito e aplicação aguardando QA; o backlog
mantém `ITEM-0020` em `em_andamento` e a ordem QA P06, patch do H-0050, novo QA
e implementação. O diff do H-0050 é vazio. As verificações de arquivos novos e
`git diff --check` foram conformes.

## Avaliação do relatório P06 e novo achado material

Os arquivos declarados, decisões, achados tratados, status e próxima ação do
P06 correspondem à aplicação observada. Contudo, o bloco `delta_terminologico`
é factualmente inconsistente: `controle_execucao` e
`controle_execucao.modo_inicial` são termos ausentes no conteúdo anterior do
módulo 02 e foram adicionados nesta execução, mas aparecem em
`termos_alterados`; `controle_execucao` aparece simultaneamente em
`termos_adicionados` e `termos_alterados`. Não há justificativa factual
inequívoca para essa dupla classificação.

```yaml
novo_achado_material:
  id: QA-P06-NEW-01
  resultado: aberto
  classificacao: defeito_do_relatorio_P06
  causa: delta_terminologico_classifica_termos_novos_como_alterados
  correcao_exigida: patch_do_relatorio_P06
```

O defeito não exige decisão de usuário nem altera contratos, nomenclatura,
H-0050 ou implementação. Não há bloqueio documental para o próximo patch.

```yaml
status: ADR_APPLICATION_REJECTED
proxima_acao: PATCH_APLICACAO_ADR
```
