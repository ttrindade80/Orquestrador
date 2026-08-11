# Relatório de patch de implementação — H-0055 P02

```yaml
cadeia:
  raiz: docs/relatorios/IMP-0055-dois-niveis-por-foco.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0055_P01.md

achados_tratados:
  - MV-H0055-001
  - MV-H0055-002
```

## Arquivos alterados

- `tela/navegacao.py`
- `demo/demo.py`
- `tela/carregamento/envelope_pre_adr_0028.py`
- `config/telas/demo/h0055_dois_niveis_por_foco.json`
- `tela/teste_navegacao.py`
- `demo/teste_demo_console.py`

Relatório criado neste caminho: `docs/relatorios/RELATORIO_PATCH_IMPLEMENTACAO_H-0055_P02.md`.

## Delta material

`MV-H0055-001`: foi adicionada a derivação contextual do rótulo de Esc a
partir do nível corrente de `dois_niveis_por_foco`. A projeção da demo usa
`Sair` no toroide de pais e `Voltar` no toroide de filhos, recalculando o
rótulo após entrada e retorno. O despacho de Esc para filhos continua
retornando ao pai, sem limpar ou modificar as escolhas; o ramo genérico de
limpeza permanece aplicável aos demais consoles.

`MV-H0055-002`: a fixture passou a declarar exclusivamente
`formato.excesso.politica_modo: somente_nao_verboso`, sem
`formato.excesso.modo_inicial` e sem o chip `V`. A exceção focal de carregamento
reconhece somente essa combinação H-0055/D23 e rejeita a forma alternável
anterior, além de rejeitar `modo_inicial` quando reapresentado. A alternância
de verbosidade de contextos que continuam `alternavel` não foi alterada.

## Verificações

- Testes focais: `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_navegacao.py demo/teste_demo_console.py -q` — `94 passed`.
- Suíte canônica: `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — `1097 passed`.
- Smoke: `PYTHONDONTWRITEBYTECODE=1 python demo/demo.py h0055_dois_niveis_por_foco` — código zero; carregou os 25 itens, exibiu duas páginas, paginação, `[Esc] Sair` e nenhum chip `[V]`.
- `git diff --check` — passou, sem saída.

Os testes verificaram entrada e retorno repetidos, atualização dos dois rótulos,
preservação das escolhas, transferência exclusiva e idempotência, isolamento
entre pais, foco/redimensionamento, paginação, ausência de `[Esc] Limpar`,
ausência de `V` em H-0055 e rejeições anteriores do loader. As regressões de
seleção multinível e dos demais modos de console passaram na suíte canônica.

Não houve bloqueio material. A validação manual focal em TTY permanece
necessária na etapa posterior; não foi executada neste patch.
