# Relatório de aplicação — ADR-0045

## Arquivos efetivamente criados/alterados

- Alterado `docs/contratos/contrato_popup.md`.
- Alterado `docs/nomenclatura/35_POPUP.md`.
- Alterado `docs/nomenclatura/21_LAYOUT_REDIMENSIONAMENTO_E_PAGINACAO.md`.
- Alterado somente o bloco do `ITEM-0028` em `docs/backlog.md`.
- Criado este relatório.

`docs/adr/ADR-0045-resize-responsivo-formacoes-popup-marcacao.md` não foi
reescrito: não possui campo ou seção própria de estado documental a atualizar.
`docs/INDICE.md` não foi alterado porque registra o diretório de ADRs, não cada
ADR individual, e não havia registro nominal da ADR-0045 a inserir.

## Mudanças materiais

O contrato passou a normatizar a preferência por `coluna`, a matriz com o
maior número de colunas fisicamente ocupadas e pelo menos duas linhas, a
condição restrita de `linha`, o vão de `2` espaços no cálculo e na
representação, o encaixe pela largura integral e pelo overhead real, além de
recomposição reversível com preservação lógica. O módulo `35` recebeu apenas
o resumo compatível dessas formações. O módulo `21` delimita a exceção física
do pop-up dentro da autoridade geral de resize. O `ITEM-0028` foi movido para
`em_andamento` sem encerramento.

## Conflito normativo reconciliado

A regra conflitante do menor número de colunas foi substituída no contrato
pela maximização das colunas reais em matrizes válidas, sem placeholders,
células artificiais ou redefinição de `linha` como matriz de uma linha.

## Delta terminológico

```yaml
delta_terminologico:
  modulos_alterados: []
  termos_adicionados: []
  termos_alterados: []
  distincoes_adicionadas: []
  fronteiras_alteradas: []
  dependencias_condicionais_adicionadas: []
```

## Verificações executadas

- Confirmada a remoção da regra concorrente do menor número de colunas no
  contrato.
- Confirmado que `linha` não foi redefinida como matriz de uma linha.
- Confirmado o vão de `2` espaços no cálculo e na apresentação de matriz e
  linha.
- Confirmado que a matriz conta somente colunas ocupadas por itens reais.
- Confirmado que o pop-up não recebe `distribuicao_matricial`.
- Confirmado que apenas arquivos do manifesto foram criados ou alterados.
- Confirmada a existência deste relatório no caminho nominal.

## Bloqueios

Nenhum.
