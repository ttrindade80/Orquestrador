# RELATÓRIO — IMPLEMENTAÇÃO H-0073

## 1. Metadata

```yaml
etapa: IMPLEMENTAR
objeto: H-0073 — aplicação da formatação de dois_niveis_por_foco às telas reais
handoff: docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md
status: IMPLEMENTATION_COMPLETED
```

## 2. Arquivos efetivamente criados nesta execução

- `demo/teste_demo_h0073_h0055_reconciliado.py`
- `tela/teste_estilo_h0073_h0063.py`
- `demo/teste_demo_h0073_h0063_reconciliado.py`
- `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md`

## 3. Arquivos efetivamente alterados nesta execução

- `config/telas/demo/h0055_dois_niveis_por_foco.json`
- `config/telas/demo/h0063_estilo_estrutura_navegacao_dois_niveis.json`
- `tela/estilo.py`
- `tela/teste_navegacao.py`
- `demo/teste_demo_console.py`

Nenhum arquivo fora de §7.1/§7.2. H-0072, ADR, contratos, nomenclatura, `demo/demo.py` e `tela/renderizacao/estilo.py` não foram editados.

## 4. H-0055

`formato.dois_niveis_por_foco.filho` materializado exatamente como §8.1: tabulação 5..10, `designador.tipo: alfabetico_maiusculo`, `sufixo: ")"`, `apresentacao: texto`. `formato.excesso` preservado.

Conteúdo externo `h0055_dois_niveis_por_foco_conteudo.json`: byte-a-byte idêntico a `HEAD`. A declaração histórica de designador permanece; o `)` visível vem da configuração estrutural.

Resultado visual: `A)`, `B)`, `C)`, `D)`. `A` sem `)` não é aceito. Tabulação medida pela diferença de coluna do cursor pai→filho (intervalo 5..10). Unidade `ec`/`tg`/designador/conteúdo deslocada junta. Navegação e seleção preservadas.

## 5. H-0063

Bloco `formato.dois_niveis_por_foco.filho` materializado exatamente como §8.3: tabulação 5..10, `designador.tipo: nenhum`, `apresentacao: tabela`, colunas `preset` e `amostra`, espaçamento 3..8.

Em `ControladorTelaEstilo._construir_conteudo`, `campos["amostra"]` passa a ser `amostra_de_preset(categoria, preset.dados)`. `campos["preset"]` e `campos["titulo"]` permanecem com o mesmo valor e significado. `amostra` não é obtida por parsing de `titulo`.

`h0062_estilo.json` permanece byte-a-byte idêntico a `HEAD`.

## 6. Suíte focal (§10.5)

```
236 passed, 1 failed
```

Falhou somente `tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados` (`index("→")` obtido 2, esperado `>= 4`).

Demais itens nominais, inclusive H-0055, H-0063 novo, regressões H-0063..H-0068 e H-0072, passaram.

## 7. Regressão H-0070

Assertiva não alterada. Continua falhando com o mesmo valor histórico (`2 >= 4`).

Causalidade aparente: o teste chama `_linhas_apresentacao_hierarquia_com_mapa` (caminho antigo), não o renderer de `formato_filho_dois_niveis`. A configuração nova de H-0063 não é exercitada por essa assertiva; H-0073 não resolve essa falha. Encaminhado ao QA_IMPLEMENTACAO.

## 8. Regressão H-0072

`tela/teste_formato_filho_dois_niveis_por_foco.py` e `demo/teste_demo_h0072_formatacao_generica.py`: passaram sem alteração de fixture, código ou testes H-0072.

## 9. Demonstrações

- H-0055 (`demo/teste_demo_h0073_h0055_reconciliado.py`): ponto de entrada real `demo/demo.py`; tela carregada; `sufixo: ")"` estrutural; `A)` na saída; tabulação 5..10; navegação/seleção preservadas. Passou.
- H-0063 (`demo/teste_demo_h0073_h0063_reconciliado.py`): fluxo real via `demo/demo.py`; projeção `preset`/`amostra`; tabela de duas colunas; sem designador visual; alinhamento entre pais; navegação/seleção; saída física. Passou.

## 10. Suíte canônica

```
PYTHONDONTWRITEBYTECODE=1 python -m pytest -q
→ 1452 passed, 1 failed
```

Única falha: H-0070, mesma da suíte focal. Nenhuma falha nova causal a H-0073 exigiu arquivo fora do escopo.

## 11. Preservação §7.4

Intocados: conteúdo H-0055, `h0062_estilo.json`, fixtures H-0072, `tela/modelo.py`, carregamento/renderer/navegação/seleção H-0072, `tela/renderizacao/estilo.py`.

## 12. Desvios e bloqueios

Desvios: nenhum. Bloqueios: nenhum.

```yaml
H-0055: IMPLEMENTADO
H-0063: IMPLEMENTADO
ACH-001: consumido via sufixo estrutural ")"
bloqueios: nenhum
```
\n