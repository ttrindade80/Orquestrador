# Relatório QA — ADR-0044

```yaml
adr: ADR-0044
item: ITEM-0017
status: ADR_APPROVED
```

## Resultado

A ADR-0044 preserva semanticamente as decisões fechadas auditadas. Não foram
identificados achados materiais.

As verificações focais foram atendidas: o pop-up permanece distinto de
`console`, do corpo e de região permanente; não executa ação de negócio; recebe
conteúdo pronto em runtime, separado da configuração; não usa `seleção única`
do console; mantém `marcacao: exclusiva` com exatamente uma marcação válida;
produz `ABORTADO` em `Esc`; não permite paginação; reutiliza o quadro geral de
terminal pequeno; e mantém a decomposição incremental em quatro entregas sem
reduzir o contrato integral.

Também foram preservadas as regras de geometria, wrapping, chips próprios,
IDs, navegação toroidal, retorno por IDs, validação fechada, resize reativo e
preservação do estado lógico.

## Achados

Nenhum.
