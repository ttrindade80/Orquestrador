# QA de implementação H-0058

Escopo real conferido pelo `git status`, delta autorizado e `git diff --check`.
O delta material da implementação coincide com o IMP-0058: `popup.py`, seus
testes, `demo.py`, seus testes, `demo.json` e a fixture H-0058. Os arquivos
autorizados apenas para preservação (`tela.py` e a fixture H-0057) não foram
alterados. Os demais itens no status são documentos de processo do ciclo e
não constituem desvio material da implementação auditada.

Foram confirmados no código e nos testes: envelope fechado e falha antes de
estado parcial; separação entre declaração, envelope e estado vivo; cursor,
formações coluna/matriz/linha, preenchimento vertical, navegação toroidal e
eixos inativos; marcação exclusiva/múltipla; recomposição por ID na mesma
instância; regressão textual; modalidade, moldura, chips, terminal pequeno,
restauração e `ABORTADO`; e ausência de confirmação/payload H-0059 para
`Enter`, `\r` e `\n`.

Testes executados: focais `59 passed`; suíte canônica `1156 passed`; `git
diff --check` sem achados.

A validação visual e interativa em TTY real prevista no handoff não foi
executada nesta auditoria automática.

status: I5_MANUAL_VALIDATION_REQUIRED
