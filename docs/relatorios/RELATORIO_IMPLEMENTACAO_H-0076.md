# Relatório de implementação H-0076

## Arquivos criados

- `tela/renderizacao/composicao_textual.py`
- `tela/teste_composicao_textual.py`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0076.md`

## Arquivos alterados funcionalmente

- `tela/renderizacao/popup.py`

O núcleo canônico compõe texto em linhas físicas por largura visual, preserva
ordem e separadores, reparte segmentos maiores que a largura, reutiliza as
primitivas ANSI existentes e justifica somente quando o modo é solicitado.
CSI não é partido e o estado SGR é fechado/reaberto entre linhas. A
justificação não faz padding quando não há vãos internos.

O popup passou a consumir `compor_texto` para texto e instrução, com o modo
escolhido pelo próprio consumidor. Geometria, margens, chips, formação,
alinhamento estrutural e overlay permaneceram no popup. O fallback histórico
de completar uma linha justificada sem vãos ficou restrito ao padding
estrutural de `_formatar_linha`. Os nomes internos de quebra e justificação
foram mantidos apenas como referências diretas ao núcleo, sem implementação
concorrente.

## Testes e demonstração

Executado exatamente:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_composicao_textual.py tela/teste_popup.py demo/teste_demo_popup.py
```

Resultado: `94 passed`.

`tela/teste_composicao_textual.py` demonstra diretamente as larguras curta,
exata e ampla, preservação de conteúdo, justificação, ANSI, CSI indivisível,
isolamento SGR, uso real pelo popup e coerência entre linhas calculadas e
linhas renderizadas. A regressão focal do popup e `demo/teste_demo_popup.py`
demonstram recomposição por largura, restauração da largura, altura e
preservação da mesma instância/estado.

## Exceções preexistentes de desbloqueio

O levantamento sintático de 123 arquivos `.py` em `tela/` e `demo/` encontrou
resíduos finais idênticos: o literal sintático `\n`. Foram removidos somente
esses artefatos, sem alteração semântica, nos arquivos:

- `tela/carregamento/tela_json.py`
- `tela/carregamento/formato_dois_niveis_por_foco.py`
- `tela/estilo.py`
- `tela/renderizacao/texto_ansi.py`
- `tela/renderizacao/console.py`
- `tela/renderizacao/conteudo_externo.py`
- `tela/renderizacao/matriz_participantes.py`
- `tela/teste_estilo_h0073_h0063.py`
- `tela/teste_formato_filho_dois_niveis_por_foco.py`
- `demo/teste_demo_console.py`
- `demo/teste_demo_h0072_formatacao_generica.py`
- `demo/teste_demo_h0073_h0055_reconciliado.py`
- `demo/teste_demo_h0073_h0063_reconciliado.py`

Cada diff focal contém somente saneamento de material residual no fim do
arquivo, sem alteração de código; em um teste, a linha em branco de EOF
imediatamente associada ao resíduo também foi removida para que
`git diff --check` permanecesse limpo. `py_compile` foi confirmado nos
arquivos afetados e a varredura posterior dos 123 arquivos retornou zero
`SyntaxError`. Essas correções foram necessárias somente para
liberar a coleta dos testes; não integram funcionalmente o ITEM-0027.

Em particular, `conteudo_externo.py` não recebeu migração, preparação ou
refatoração: apenas o saneamento sintático autorizado. Os consumidores
reservados ao H-0077 permanecem fora da composição canônica.

## Desvios, bloqueios e exceções

Não houve desvio funcional nem bloqueio após as autorizações de saneamento.
`texto_ansi.py` não recebeu mudança de comportamento; suas primitivas foram
reutilizadas pelo novo núcleo.
