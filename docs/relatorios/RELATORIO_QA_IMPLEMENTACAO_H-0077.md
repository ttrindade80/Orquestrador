# Relatório de QA de implementação H-0077

## Resultado dos testes

O comando focal definido pelo H-0077 foi executado literalmente:

```text
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tela/teste_renderizador.py tela/teste_formato_filho_dois_niveis_por_foco.py tela/teste_paginacao.py tela/teste_navegacao.py tela/teste_estilo_h0070.py tela/teste_estilo_h0071.py tela/teste_estilo_h0073_h0063.py tela/teste_composicao_textual.py tela/teste_popup.py
```

Resultado: `621 passed, 11 failed` (exit code 1).

As regressões isoladas de H-0076 foram executadas com
`tela/teste_composicao_textual.py`, `tela/teste_popup.py` e
`demo/teste_demo_popup.py`: `87 passed`.

`git diff --check`: aprovado, sem saída e com exit code 0.

## Tabela de classificação das falhas

| Teste falho | Causa factual | Categoria | Achado |
|---|---|---|---|
| `tela/teste_paginacao.py::test_p16_fluxo_continuo_comeca_na_proxima_linha_disponivel` | O fixture sintético monta quatro tokens de 38 caracteres. A quebra antiga por palavras produzia quatro linhas; a composição canônica, na largura 77, produz três (`[77, 77, 1]`). O plano, portanto, não cria a continuação esperada para `b`. O ponto de paginação foi alterado diretamente de `_quebrar_texto` para `compor_texto`. | B | QA-IMPL-H0077-01 |
| `tela/teste_paginacao.py::test_p16_condicional_move_inteiro_quando_nao_cabe_no_residuo` | Pela mesma mudança deliberada de unidade física, `a` e `b` ocupam menos linhas sob a composição canônica e `b` cabe no resíduo; a expectativa exige a contagem derivada da quebra antiga. | B | QA-IMPL-H0077-01 |
| `tela/teste_paginacao.py::test_p16_item_maior_que_pagina_nas_tres_politicas` | O item sintético que a expectativa considera ter nove linhas ocupa cinco linhas quando composto canonicamente na largura 77. A asserção depende da antiga quebra por palavras. | B | QA-IMPL-H0077-01 |
| `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados` | A falha é `index("→") == 2`, contra o mínimo 4. O teste percorre o caminho não verboso; a implementação H-0077 só substituiu chamadas de wrap no caminho verboso, e o prefixo/recuo relevante não foi alterado no diff. | C | QA-IMPL-H0077-03 |
| `tela/teste_estilo_h0073_h0063.py::test_06_07_08_09_10_configuracao_estrutural_tabulacao_tabela` | `json.loads` falha com `JSONDecodeError: Extra data: line 191 column 1 (char 5419)`. O fixture H-0063 termina com o literal `\\n` fora do objeto JSON. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_11_alinhamento_entre_pais_diferentes` | `carregar_tela` falha pelo mesmo `JSONDecodeError` no mesmo fixture, antes de exercitar o alinhamento. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_12_13_unidade_deslocada_sem_designador_visual` | `carregar_tela` falha pelo mesmo `JSONDecodeError` no mesmo fixture, antes de exercitar a unidade deslocada. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_14_conteudo_visual_preset_e_amostra_preservados` | `carregar_tela` falha pelo mesmo `JSONDecodeError` no mesmo fixture, antes de exercitar a preservação do conteúdo visual. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_15_navegacao_e_selecao_preservadas` | `carregar_tela` falha pelo mesmo `JSONDecodeError` no mesmo fixture, antes de exercitar navegação e seleção. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_17_resize_recalcula_disposicao_preservando_item` | `carregar_tela` falha pelo mesmo `JSONDecodeError` no mesmo fixture, antes de exercitar resize e preservação do item. | D | QA-IMPL-H0077-02 |
| `tela/teste_estilo_h0073_h0063.py::test_18_configuracao_visual_fora_dos_dados` | `json.loads` falha pelo mesmo `JSONDecodeError` no mesmo fixture. | D | QA-IMPL-H0077-02 |

Os três testes P16 são obsoletos quanto à expectativa de quebra por palavras,
mas estão em `tela/teste_paginacao.py`, fora da lista de testes que o handoff
autoriza alterar. A reconciliação exige patch do handoff ou autorização focal;
não é válido manter essas falhas sem decisão.

O fixture H-0063 não foi alterado pelo diff H-0077. A comparação do trecho
final com `HEAD` mostra o mesmo literal `\\n` extra em ambos. O arquivo de
fixture está fora do escopo autorizado e impede a validação dos sete testes de
formatação/navegação que fazem parte da superfície autorizada de H-0077.

O teste H-0070 é independente: sua falha está no caminho não verboso e não há
alteração correspondente no diff funcional H-0077. Ele é registrado, mas não
invalida por si só a demonstração de H-0077.

## Auditoria funcional

### Conteúdo externo

`conteudo_externo.py` não define mais `_quebrar_texto` e não importa
`_quebrar_sem_ansi` para esse papel. As chamadas comuns de hierarquia, dois
níveis por foco, tabela e conjuntos usam `compor_texto`. Prefixos,
designadores, indicadores, indentação, escolha de campos e estrutura de
coluna continuam locais. `_truncar_com_marcador` permanece uma função separada
e continua sendo usada nos caminhos não verbosos. O diff não introduz política
global de whitespace ou separadores.

### Matriz, altura e mapa físico

`_altura_quebra_item` usa `compor_texto`; o caminho de
`_renderizar_participante_com_indicador` usa a mesma composição quando há
quebra; e `_larguras_mapa_fisico_matricial` recalcula alturas com
`_altura_quebra_item` após conhecer a largura real da célula. Para conteúdo
externo, o mapa usa a quantidade de linhas efetivamente produzida pelas
entradas de apresentação, em vez de uma regra antiga de quebra. Os testes
focais aprovados cobrem as coerências de mapa, renderização e fragmentação,
mas a evidência da superfície H-0073 permanece incompleta pelo fixture D.

### Paginação

`_linhas_texto_item_para_pagina` usa diretamente `compor_texto`; o recorte usa
`mapa_fisico_de_itens` e as linhas físicas do mapa. A cadeia está convergida
para a autoridade canônica, mas os três testes P16 continuam com expectativas
da autoridade antiga e precisam ser reconciliados conforme QA-IMPL-H0077-01.

### Truncamento

`_truncar_com_marcador` não foi absorvido pela composição, não foi transformado
em wrap e não ganhou semântica concorrente. A distinção entre truncamento de
linha única e composição multilinear permanece local ao consumidor.

### Reexport `_quebrar_texto`

`tela/renderizador.py` importa `_quebrar_texto` diretamente de
`tela.renderizacao.composicao_textual`. A verificação de identidade confirmou
que `tela.renderizador._quebrar_texto is
tela.renderizacao.composicao_textual._quebrar_texto`. Não há wrapper,
implementação própria ou política adicional, e o nome preserva a fachada
existente sem constituir uma segunda autoridade.

### Política de whitespace

As substituições do H-0077 apenas trocam a primitiva de composição nos
consumidores. Não foi criada política global de preservação, normalização,
condensação, trimming ou inserção/remoção sistemática de separadores. A
normalização já existente de valores de campos permanece uma semântica local
de `nome_valor`, não uma política do núcleo.

### H-0076

`tela/teste_composicao_textual.py`, `tela/teste_popup.py` e
`demo/teste_demo_popup.py` passaram separadamente (`87 passed`). O diff
funcional de H-0077 não altera o núcleo canônico nem o popup. O working tree
contém outras mudanças preexistentes de handoffs anteriores; elas não foram
atribuídas ao H-0077. Nos arquivos condicionais `console.py` e
`texto_ansi.py`, a diferença observada é apenas de final de linha, sem
alteração funcional atribuível a este handoff.

## Diff e escopo

O diff funcional solicitado para os cinco arquivos declarados mostra somente
as migrações para `compor_texto`, a remoção da implementação local e a
reconciliação do import no teste de estilo. Não há alteração funcional H-0077
em arquivo fora dessa lista identificada no diff escopado. O estado global do
working tree está sujo por alterações de etapas anteriores, portanto a
atribuição temporal de cada alteração fora do delta declarado não pode ser
inferida apenas por `git diff`; essas alterações não foram consideradas como
delta H-0077.

## Achados

### QA-IMPL-H0077-01 — expectativas P16 não reconciliadas

Categoria B. A implementação aplicou deliberadamente a composição canônica à
paginação, mas três testes fora da lista autorizada ainda codificam a contagem
da quebra por palavras. É necessário patch do handoff ou autorização focal
para reconciliar as expectativas/fixtures e demonstrar as políticas P16.

### QA-IMPL-H0077-02 — fixture H-0063 inválido fora do escopo

Categoria D. O literal `\\n` extra, comprovadamente presente em `HEAD`, faz
sete testes falharem antes da validação funcional. Corrigir o fixture exige
alterar arquivo fora da lista autorizada; a evidência de dois níveis e da
superfície H-0073 fica incompleta sem essa decisão.

### QA-IMPL-H0077-03 — resíduo independente H-0070

Categoria C. A expectativa de recuo mínimo falha em caminho não verboso não
alterado pelo H-0077. O resíduo é registrado separadamente e não é causa do
status de implementação.

## Status final

`I3_HANDOFF_PATCH_REQUIRED`
