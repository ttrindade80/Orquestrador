# Relatório de QA da implementação H-0076

## Testes e verificações

- Executado exatamente o comando focal exigido: `94 passed`.
- `git diff --check`: aprovado, sem saída.
- O núcleo, o popup, seus testes e o teste de demonstração foram lidos integralmente.
- Os helpers ANSI efetivamente usados pelo núcleo foram verificados, assim como o diff de `texto_ansi.py`.

## Auditoria do núcleo e do popup

`composicao_textual.py` constitui um núcleo compartilhável e reutiliza as primitivas ANSI existentes para tokens, largura visual e estado SGR. A composição não parte CSI; nas quebras, fecha e restabelece o estado de cor por linha. Os testes demonstram largura visual, CSI indivisível, isolamento SGR, justificação e coerência entre layout e saída.

`popup.py` consome diretamente `compor_texto` para texto e instrução. `_formatar_linha` permanece restrita a padding/alinhamento estrutural; geometria, margens, chips, formação e overlay continuam locais. A recomposição por largura e a preservação de instância/estado foram cobertas. Não há migração funcional ou implementação concorrente equivalente nos consumidores reservados ao H-0077.

## Auditoria das exceções mecânicas

Os 13 diffs autorizados contêm somente remoção do artefato literal final `\\n`; no teste indicado, também foi removida a linha vazia de EOF associada. Não há mudança funcional. Nos cinco arquivos reservados ao H-0077, `conteudo_externo.py`, `matriz_participantes.py` e `console.py` têm somente esse saneamento; `paginacao_interna.py` e `renderizador.py` não têm diff.

## Achado material

`QA-IMPL-H0076-01` — `I2_IMPLEMENTATION_PATCH_REQUIRED`

O núcleo canoniza preservação literal de separadores: `_faixas_de_quebra` agrupa e mantém todos os caracteres whitespace, e o teste `test_nucleo_preserva_ordem_separadores_e_conteudo_sem_insercao` exige `"".join(linhas) == texto` para múltiplos espaços. Os testes do popup reforçam essa regra para separadores múltiplos, espaços somente e extremidades. Portanto, não se trata apenas de compatibilidade local do popup; é uma invariável observável do núcleo compartilhável. O handoff deixou indefinida a política global de espaços/separadores e proíbe promovê-la a contrato. O relatório de implementação também registra essa política como resultado geral.

## Status final

`I2_IMPLEMENTATION_PATCH_REQUIRED`
