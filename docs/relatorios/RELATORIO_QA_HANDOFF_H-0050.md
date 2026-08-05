# Relatório QA — H-0050

status: BLOCKED_DOCUMENTATION

## Cadeia e estado auditados

Foram auditados D-DRY-01 a D-DRY-09, a ADR-0040 (`aceita`), os contratos e
módulos de nomenclatura enumerados, o template de handoff, as interfaces
focais autorizadas e o H-0050. A ordem de autoridade e a etapa única
`IMPLEMENTAR` estão corretamente declaradas. `metadata.status:
READY_FOR_IMPLEMENTATION` é compatível com o status normativo do template.

Git observado: branch `master`; HEAD
`c1efa0c06e7b939dbcd32c86c0c4748677abe031`; stage vazio; `git diff --check`
sem saída; verificação direta do handoff: `HANDOFF_FILE_CHECK: OK`. O worktree
contém os nove documentos modificados e os doze artefatos documentais não
rastreados listados como preexistentes no handoff, além do próprio H-0050.
A autoria temporal desses deltas não é independentemente verificável sem
histórico Git, que estava fora do manifesto.

## Resultado formal

O handoff é formalmente completo quanto a objetivo, autoridade, escopo
positivo/negativo, manifesto, testes, demonstração, validação manual,
relatório de implementação, critérios de aceite, bloqueios e resposta
terminal. A segunda configuração `dry_run` é evidência mínima aceitável e o
manifesto não autoriza alteração do H-0044. A barra de testes declarada é o
caminho vigente e o pytest coletou 84 testes.

As decisões de produto permanecem fiéis: dois modos literais, sem default,
sem persistência, um modo por instância, chip específico não canônico,
`Insert`, `cor_alerta`, captura explícita junto ao lote e isolamento da
especialização ADR-0037/H-0044. O ponto de captura físico vigente está em
`demo/demo.py`; não há captura de `Insert` em `tela/renderizador.py`.

## Achados materiais e bloqueios

1. **QA-H0050-03 — `BLOCKED_USER_DECISION`.** O H-0050 exige que
   `controle_execucao` rejeite propriedades internas adicionais. D-DRY-09
   afirma apenas que nenhum outro campo foi decidido. O contrato de
   `tela.json` remete campos desconhecidos à política geral, mas não fecha
   essa política para o objeto; o loader possui fechamento apenas em objetos
   específicos, não uma regra geral aplicável. A implementação não pode
   escolher rejeição ou extensão sem nova autoridade de contrato/produto.

2. **QA-H0050-04/09 — `BLOCKED_DOCUMENTATION`.** Os contratos físicos
   reconhecem `acao_enter`/ações registradas, mas declaram o registry completo
   de ações fora de escopo. As buscas autorizadas não encontraram
   `tipo_execucao`, `acoes_registradas`, `registrar_acao` nem metadado vigente
   que declare aceitação de `executar` e `dry_run`. O contrato provisório
   existente transporta `ids` e usa flag de CLI para `dry-run`; não autoriza o
   novo formato universal como contrato público. Assim, não é possível provar
   a compatibilidade integral de qualquer tela sem inventar schema, registry,
   classificação ou protocolo — precisamente proibido pelo handoff.

Esse segundo bloqueio também impede concluir a universalidade da capacidade:
o controlador, a barra e a demonstração têm proprietários nominais, mas falta
uma autoridade física reutilizável para validar todas as ações de processo.

## Testes, manual e preservação focal

Os comandos pytest declarados são sintaticamente coerentes para a entrega
futura; os novos caminhos ainda não existem. A validação TTY permanece
pendente do usuário, como corretamente declarado. O roteiro deve verificar
semanticamente `cor_alerta` (a configuração atual resolve para amarelo), sem
transformar a cor concreta em regra universal. Não houve implementação,
correção, validação manual ou alteração do H-0044.

## Próxima ação

Resolver a política de propriedades e a autoridade física de compatibilidade;
em seguida, corrigir o handoff e submetê-lo novamente a QA.
