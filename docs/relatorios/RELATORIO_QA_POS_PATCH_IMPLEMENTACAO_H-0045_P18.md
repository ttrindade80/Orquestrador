---
name: RELATORIO_QA_POS_PATCH_IMPLEMENTACAO_H-0045_P18
metadata:
  tipo: relatorio_qa_pos_patch_implementacao
  status: I2_IMPLEMENTATION_PATCH_REQUIRED
  handoff: H-0045
  patches: [P17, P18]
---

# QA pós-patch — H-0045 P18

## Estado

- `VM-H0045-R07-001`: correção produtiva de largura tecnicamente evidenciada,
  mas permanece pendente; a prova automatizada ainda requer novo patch e a
  validação manual focal continua obrigatória.
- `IMP-H0045-P17-001`: bloqueio numérico tratado pelo P18, porém não encerrado
  em QA devido aos achados semânticos abaixo.

## Verificações cumulativas

P17 está limitado a `tela/renderizador.py` e `tela/teste_renderizador.py`, nas
duas funções autorizadas e seus testes focais. P18 não introduziu código
produtivo e está nominalmente limitado a `demo/teste_demo_paginacao.py` e
`demo/teste_demo_navegacao.py`; o delta cumulativo dos patches é, portanto,
restrito aos quatro arquivos autorizados. O worktree possui outras mudanças
anteriores da cadeia H-0045, não atribuídas a P17/P18.

Medição executada na célula única verbosa:

| terminal | útil | texto | maior linha | resíduo | renderer/mapa |
|---:|---:|---:|---:|---:|---:|
| 80 | 77 | 75 | 76 | 2 | 75/75 |
| 120 | 117 | 115 | 115 | 2 | 115/115 |
| 160 | 157 | 155 | 155 | 2 | 155/155 |
| 200 | 197 | 195 | 194 | 2 | 195/195 |

A largura cresce monotonicamente, o resíduo é somente margem estrutural e o
teto de metade desapareceu. Os testes focais também cobrem as cinco telas
H-0045, H-0037, múltiplas células, indicador, overflow, resize e identidade.

## Testes

- focal: `417 passed`;
- focal com `tela/teste_paginacao.py`: `430 passed`;
- suíte completa: `856 passed`;
- `git diff --check` nos quatro caminhos: saída vazia; inspeção adicional dos
  arquivos não rastreados não encontrou whitespace final.

## Achados

1. **Prova CLI materialmente confundida** (`demo/teste_demo_navegacao.py:478-500`):
   a execução não verbosa usa a fixture original, enquanto a execução verbosa
   usa uma cópia cujo texto de Gamma foi alterado. `p_nv.stdout != p_v.stdout`
   não prova apenas a mudança de modo. O mesmo problema ocorre na comparação
   local: `s_nv` é renderizado antes do alongamento e `s_v` depois
   (`:381-405`). Requer executar ambos os modos sobre o mesmo modelo/conteúdo
   alongado, preservando a fixture original fora do cenário local.

2. **Página somente de continuação não é provada no quadro**
   (`demo/teste_demo_paginacao.py:1858-1907`): a inspeção do plano confirma
   que a página 2 contém apenas a continuação de `permitir_quebra_01`, mas o
   teste só soma fragmentos e verifica o indicador final. Não renderiza cada
   página nem confirma conteúdo visível, zero cursor, ausência de início
   navegável e navegação sem salto automático. Isso deixa incompleta a prova
   exigida para a geometria menor.

3. **Ordem descartada em P10**: os testes P10 comparam
   `sorted(produzidas)` com `sorted(esperadas)` (`:1645` e `:1691`), removendo
   a ordem das páginas/itens como evidência. A prova exata de ordem existente
   em P11 não substitui a verificação perdida nos cenários P10 de repaginação.

## Validação manual

Não executada. Após novo QA técnico conforme, permanece necessária somente:
`python demo/demo.py h0045_validacao_continuacao`.
