# Relatório de patch de implementação — H-0057/P01

- **Raiz da implementação:** `docs/relatorios/IMP-0057-popup-geometria-dinamica-wrapping-resize.md`
- **Predecessor imediato:** `docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0057.md`
- **Achado:** `QA-H0057-IMP-001 — wrapping descarta separadores e não preserva integralmente o conteúdo`.

## Causa técnica

`_quebrar_texto` mantinha whitespace entre palavras em um acumulador pendente,
mas o descartava quando a palavra seguinte não cabia na linha corrente. Para
uma entrada somente de espaços, o caminho final materializava apenas o
primeiro fragmento limitado à largura útil.

## Correção aplicada

O wrapping agora consome cada token de whitespace fisicamente, ocupando o
espaço disponível e dividindo o próprio separador somente quando necessário.
Palavras continuam sendo mantidas inteiras quando cabem na próxima linha e
são divididas em blocos apenas quando excedem a largura útil.

Regra adotada: a concatenação ordenada das linhas físicas produzidas é
exatamente a string de entrada; cada caractere é consumido uma única vez, sem
`.strip()`, normalização, truncamento ou reticências.

## Testes e resultados

Foram adicionados testes para `a  b`, `a   b`, `aa  bb`, string somente de
espaços, whitespace nas extremidades e reconstrução integral da frase comum.

- Teste focal: `33 passed`, código 0.
- Conjunto H-0057: `42 passed`, código 0.
- Suíte canônica: `1139 passed`, código 0.
- Diff focal: `git diff --check -- tela/renderizacao/popup.py tela/teste_popup.py` sem apontamentos.

## Bloqueios

Nenhum. Não houve alteração fora dos arquivos permitidos, stage ou commit.
