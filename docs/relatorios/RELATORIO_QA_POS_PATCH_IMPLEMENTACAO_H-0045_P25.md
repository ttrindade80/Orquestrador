# QA pós-patch de implementação — H-0045 P25

status: I5_MANUAL_VALIDATION_REQUIRED

## Estado de VM-H0045-R08-001

A issue `VM-H0045-R08-001` permanece aberta até a validação manual interativa pelo usuário. O comportamento de `VM-H0045-R06-001` e `VM-H0045-R07-001` foi preservado.

## Seletividade e Propagação de Erros

A classificação de erros em `demo/demo.py` é extremamente seletiva. Usando expressões regulares ancoradas de correspondência total (`fullmatch`), o sistema distingue erros de geometria reais (overflow da barra e insuficiências de altura do renderer) de qualquer erro estrutural.

Erros de modelo, quebra de invariantes e códigos estruturais (como `DA-01`, `DA-02`, `DA-04` e `DA-099`) não são absorvidos. Eles propagam mantendo tipo e mensagem originais nos três caminhos auditados: `_resolver_conteudo`, `_reconciliar_paginacao_apos_resize` e `_com_geometria_real_do_console`.

## Quadro Controlado e Ajustes Legados

Em dimensões restritas (como `80x8`), o sistema apresenta com sucesso o quadro controlado unificado com as duas mensagens: `Terminal pequeno demais` e `Aumente a janela para continuar`, sem interface parcial ou nova exceção.

Os testes legados em `demo/teste_demo.py` foram devidamente ajustados:
- No teste de `H-0023` (seção 8.12), a propagação de `RenderizadorErro("r")` é confirmada sem mascarar a falha em quadro mínimo.
- No teste de `H-0044` (p01), o cenário pequeno agora valida as duas mensagens do quadro controlado, e a recuperação pós-ampliação permanece garantida.

## Matriz e Sequência Contínua

A matriz técnica de 60 combinações (larguras de 16 a 120 e alturas de 6 a 40) foi integralmente exercitada, operando de forma controlada sem exceções. A sequência contínua foi validada: abertura em tamanho normal, seleção, diminuição até estado controlado (comandos geométricos como no-op), limpeza com primeiro `Esc`, ampliação para 120 (recuperação automática do cursor/foco/página) e encerramento com `Esc`.

## Suítes, Escopo e Diferencial

As execuções dos testes apresentaram resultados perfeitamente verdes:
- Foco P25: 43 passed
- Relacionados: 87 passed
- Focal: 574 passed
- Completa: 970 passed
- `git diff --check`: limpo

Não há alterações não autorizadas no delta do P25. Os arquivos `tela/renderizador.py`, `config/telas/demo/h0045_fluxo_execucao_paginado.json`, `tela/paginacao.py`, `tela/navegacao.py` e `tela/selecao.py` não contêm delta do P25.

## Validação Manual

A validação do roteiro interativo pelo usuário em terminal TTY real permanece pendente como a única etapa restante para a conclusão do ciclo.
