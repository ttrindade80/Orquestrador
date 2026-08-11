# Relatório de patch — H-0057 P02

- **Achado manual:** MV-H0057-001 — a justificação podia diferir uma coluna quando o espaço excedente tinha resto.
- **Causa:** o cálculo não explicitava o comprimento físico atual da linha no ponto da justificação, e os casos residuais não estavam fixados por testes.
- **Algoritmo anterior:** calculava a sobra diretamente a partir do comprimento textual e não tinha cobertura específica para distribuição residual, embora já usasse uma distribuição parcial por vãos.
- **Algoritmo corrigido:** calcula `extra = largura_alvo - comprimento_atual`, aplica `base, resto = divmod(extra, numero_de_vaos)` e acrescenta `base + 1` aos primeiros `resto` vãos, da esquerda para a direita. O whitespace original de cada vão é preservado.
- **Regras preservadas:** última linha alinhada à esquerda; linha sem vão não recebe espaços internos inventados; nenhuma alteração em wrapping, centralização, resize, geometria externa ou chips.
- **Testes adicionados/regressados:** distribuição divisível, resto 1, resto maior, viés à esquerda, largura final exata, última linha, linha sem vão e whitespace múltiplo; os testes existentes de wrapping P01 permaneceram verdes.
- **Resultados:** `39 passed` (`tela/teste_popup.py`); `48 passed` (`tela/teste_popup.py demo/teste_demo_popup.py`); `1145 passed` (suíte canônica).
- **Diff:** `git diff --check -- tela/renderizacao/popup.py tela/teste_popup.py` — OK.
- **Bloqueios:** nenhum.
