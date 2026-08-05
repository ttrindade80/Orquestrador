# Relatório QA de implementação — H-0050

## Estado Git

Branch `master`, HEAD `c1efa0c06e7b939dbcd32c86c0c4748677abe031`. Não há
alterações staged nem commit realizado. Os caminhos de implementação do
manifesto aparecem como alterações não staged ou arquivos não rastreados; o
workspace também contém alterações fora do manifesto, preservadas e não
atribuídas nesta auditoria. `git diff --check` não encontrou erro de
whitespace. Não há delta nos arquivos preservados do H-0044.

## Resultado da auditoria

O objeto `controle_execucao` é opcional e fechado para ausência, `executar` e
`dry_run`, sem default nem estado vivo no `_raw`. Propriedade adicional,
ausência de `modo_inicial`, `null`, booleano, número e string desconhecida são
rejeitados. Entretanto, lista em `modo_inicial` produz `TypeError` de
hashability, não `CONFIGURACAO_INVALIDA` com caminho preciso.

O registro é explícito e reutilizável, com as três categorias fechadas,
resolução por referência e compatibilidade declarada na implementação. A
elegibilidade exige os dois modos somente para processos e ocorre antes da
execução; navegação/visualização não recebem essa exigência. Não foi observada
inferência por nome, ID, rótulo, script ou comportamento, nem dispatcher,
plugin system, varredura ou registro configurável no JSON. A ação H-0050 usa o
mesmo registro universal.

O modo é mantido por instância, alterna por `Insert` e não depende de seleção,
foco, cursor, página ou lote. A captura preserva modo e ordem do lote e não
retroage após nova alternância. Porém, o lote vazio ainda chama o executor e
retorna `EXECUTADO`; o requisito é não executar. Além disso, a classe descrita
como privada é aliasada e exportada como `RequisicaoExecucaoCapturada` em
`__all__`, expondo indevidamente a estrutura interna como API.

## Chip, demonstração e preservação

O literal real no código, testes, configurações e saída é `[Insert] Executar`
/ `[Insert] Dry-Run`; o handoff exige `[Ins]`. A ordem real da configuração é
`[Esc]`, controle, seleção, Enter; o controle aparece antes de Enter, embora
devesse aparecer depois de `[⏎]`. O estado ativo nos dois modos e o uso de
`cor_alerta` em `dry_run` estão conformes; `cor_inativo` não é usado.

As duas configurações e a fixture determinística existem. A execução dos dois
comandos de demonstração terminou com código zero e mostrou os rótulos reais,
mas não substitui a prova semântica completa nem validação TTY. Os testes
integrais demonstram alternância, seleção de dois itens, modo/lote recebido,
preservação simulada de retorno e reinicialização de nova sessão; não há prova
automatizada equivalente para o lote vazio, lista inválida, literal aprovado
ou roteiro completo de recarga/redimensionamento.

Não houve delta em `config/telas/demo/h0044_fluxo_execucao_integrado.json`,
`tela/fluxo_execucao.py` ou `tela/teste_fluxo_execucao.py`; a regressão H-0044
permaneceu aprovada. O relatório IMP-0050 corresponde aos caminhos e totais,
mas registra `[Insert]` como comportamento entregue, em conflito factual com
o handoff, e sua afirmação de smoke completo não cobre o roteiro integral.

## Testes e achados

Testes focais obrigatórios: **245 passed**. Suíte completa: **1014 passed**.

Achados materiais: literal e ordem do chip; falha não fechada para lista;
execução indevida de lote vazio; exposição da captura privada. Todos exigem
`I2_IMPLEMENTATION_PATCH_REQUIRED`.

## Bloqueios e validação manual

Não há bloqueio documental. A validação visual continua necessária, não foi
executada e permanece `PENDENTE_USUARIO_TTY`; não pode ser aprovada enquanto
os achados de implementação existirem.

```yaml
status: I2_IMPLEMENTATION_PATCH_REQUIRED
proxima_acao: PATCH_IMPLEMENTATION
```
