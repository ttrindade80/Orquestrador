# RELATORIO_VALIDACAO_MANUAL_TTY_H-0028

## 1. Identificação

- handoff: `H-0028-matriz-de-grupos-coordenadas-explicitas`
- implementação: `IMP-0029-matriz-de-grupos-coordenadas-explicitas`
- etapa: `VALIDACAO_MANUAL`
- executor: usuário
- data: `2026-07-12`
- commit-base: `f00b0bb968847205bb0bcca5259af0ae11af1844`
- ambiente: terminal TTY real

## 2. Objetivo

Validar visualmente a renderização de grupos matriciais, incluindo alinhamento das bordas, interseções, proporções, ausência de lacunas e redimensionamento.

A homologação foi executada pelo usuário porque a inspeção visual em terminal real não pode ser substituída por testes automatizados.

## 3. Procedimento

Foi executado o demonstrador temporário:

`/tmp/h0028_visual_v3.py`

O demonstrador reconstruiu o grupo e o modelo a cada redesenho, consultou novamente as dimensões do terminal e chamou `renderizar_tela` com largura e altura atualizadas.

Nenhum JSON ativo ou arquivo de código do repositório foi alterado.

## 4. Resultados

- matriz 2×2: aprovada;
- matriz 2×4 com pesos assimétricos: aprovada;
- matriz 3×3 com restos: aprovada;
- redimensionamento: aprovado;
- bordas verticais: alinhadas;
- bordas horizontais: alinhadas;
- interseções: corretas;
- lacunas: nenhuma;
- sobreposições: nenhuma;
- artefatos visuais: nenhum.

## 5. Área insuficiente

No cenário 2×4, com terminal de `69 × 15` e área de renderização de `68 × 11`, ocorreu:

`RenderizadorErro: altura insuficiente: corpo requer 6 linhas mas area disponivel e 5 linhas (altura=11, cabecalho=3, barra=3)`

A rejeição corresponde ao comportamento global esperado para área insuficiente.

Ela não representa falha, desalinhamento ou regressão da matriz.

## 6. Status final

`MANUAL_VALIDATION_APPROVED`

A implementação do H-0028 foi visualmente homologada em terminal real.

Não foi identificado defeito que exija patch de código, testes, handoff ou documentação normativa.

## 7. Próxima categoria processual

`PRONTO_PARA_FECHAMENTO_MANUAL`
