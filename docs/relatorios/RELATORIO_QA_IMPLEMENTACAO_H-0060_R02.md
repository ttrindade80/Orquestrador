# Relatório QA da implementação H-0060 R02

status: IMPLEMENTATION_APPROVED

## Escopo auditado

Foram lidos integralmente:

- `docs/handoff/H-0060-resize-responsivo-formacoes-popup-marcacao.md`
- `docs/relatorios/IMP-0060-resize-responsivo-formacoes-popup-marcacao-R02.md`
- `tela/renderizacao/tela.py`
- `tela/testes_renderizador/integracao.py`
- `demo/teste_demo_popup.py`
- `tela/teste_popup.py`
- `tela/renderizacao/popup.py` (leitura focal)
- `pytest.ini`
- `demo/fixtures/h0058_popup_lista_marcacao.py`

Também foram executados o diff/status obrigatórios e `git diff --check`.

## Conclusão técnica

`MV-H0060-001` foi corrigido. Em `tela/renderizacao/tela.py:403-427`, somente
quando há pop-up aberto, o bloco do corpo é projetado para exatamente
`l_corpo_disponivel`: linhas excedentes são removidas, linhas faltantes são
complementadas com espaços na largura física do corpo e a mesma cota é passada
como `altura` a `sobrepor_no_corpo`. A largura não é alterada.

A verificação final permanece ativa em `tela/renderizacao/tela.py:450-491` e
continua rejeitando composição maior que a cota física. O caminho sem pop-up
não recebeu a projeção; o teste canônico continua rejeitando o corpo natural
de 14 linhas contra 12 disponíveis em `80x18`.

O `popup.py` não recebeu novo delta atribuível ao R02; seu delta presente no
worktree corresponde à implementação anterior das formações e foi preservado.
As regressões diretas e de integração continuam passando.

## Casos obrigatórios

- **Matriz, `80x18`:** a regressão atravessa `renderizar_tela`, confirma bloco
  e cota `(12, 12)`, formação matriz, seis itens integrais, quadro `80x18`,
  ausência de terminal pequeno, mesma instância, cursor por ID e marcações por
  ID. As políticas exclusiva e múltipla são exercitadas.
- **Linha, `77x14`:** a regressão atravessa `renderizar_tela`, confirma bloco
  e cota `(8, 8)`, formação linha, seis itens integrais, quadro `77x14`,
  ausência de terminal pequeno e preservação da instância, cursor e marcações.
  As duas políticas são exercitadas.
- **Terminal pequeno, `23x6`:** o fluxo runtime produz por igualdade o quadro
  vigente, sem itens parciais, reticências ou paginação, preservando a instância
  aberta.
- **Sem pop-up, `80x18`:** o corpo natural excedente continua sendo rejeitado
  com `corpo requer 14 linhas mas area disponivel e 12 linhas`.

Prioridade coluna → matriz → linha, preservação de IDs, navegação, marcação
exclusiva/múltipla, largura integral, vão de dois espaços, overhead,
reversibilidade e ausência de placeholders permanecem cobertos pelos testes
diretos; não houve novo delta R02 em `popup.py`.

## Resultados quantitativos

| Comando | Resultado |
|---|---:|
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/testes_renderizador/integracao.py` | 23 passed |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py` | 63 passed |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest demo/teste_demo_popup.py` | 15 passed |
| `PYTHONDONTWRITEBYTECODE=1 python -m pytest` | 1175 passed |

`git diff --check`: código de saída 0, sem ocorrências.

## Escopo real do diff/status

No conjunto focal, o diff contém:

- `tela/renderizacao/tela.py` — delta R02 de produção;
- `tela/renderizacao/popup.py` — delta anterior das formações, sem novo delta
  atribuível ao R02;
- `tela/testes_renderizador/integracao.py`;
- `tela/teste_popup.py`;
- `demo/teste_demo_popup.py`.

`demo/fixtures/h0058_popup_lista_marcacao.py` não possui diff e permanece
intacta. Não há arquivo de produção adicional fora da fronteira prevista do
handoff. O status global contém alterações documentais preexistentes, que não
foram alteradas pelo QA nem reabertas nesta auditoria.

## Respostas às questões obrigatórias

1. Sim — `MV-H0060-001` foi corrigido.
2. Sim — o caminho real passa `l_corpo_disponivel` à sobreposição.
3. Sim — a altura natural excedente não é usada pelo layout do pop-up.
4. Sim — o bloco de sobreposição tem a cota física projetada.
5. Sim — a verificação final permanece ativa.
6. Sim — o caminho sem pop-up permanece não especializado.
7. Sim — matriz atravessa `renderizar_tela` e passa.
8. Sim — linha atravessa `renderizar_tela` e passa.
9. Sim — o terminal pequeno real passa.
10. Sim — exclusiva e múltipla estão cobertas.
11. Sim — cursor e marcações são preservados por ID.
12. Sim — não há nova alteração de `popup.py` atribuível ao R02.
13. Sim — a fixture H-0058 permaneceu intacta.
14. Não — não há produção adicional fora da fronteira do handoff.
15. Não — não surgiu regressão nos testes diretos anteriores.
16. Sim — a suíte canônica passa integralmente.
17. Sim — `git diff --check` está limpo.
18. Não — não há novo achado material impeditivo.

## Achados materiais

Nenhum.
