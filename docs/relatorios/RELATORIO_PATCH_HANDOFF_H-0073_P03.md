# RELATORIO_PATCH_HANDOFF_H-0073_P03

## Rastreabilidade

```yaml
etapa: PATCH_HANDOFF
objeto: H-0073
patch: P03
achado_resolvido: ACH-001
cadeia_raiz: docs/handoff/H-0073-aplicacao-formatacao-telas-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_QA_PATCH_IMPLEMENTACAO_H-0072_P01.md
data: 2026-08-15
```

## H-0072 corrigido e aprovado

Predecessor imediato: `I1_IMPLEMENTATION_APPROVED`, achados materiais
nenhum. A capacidade genérica agora aceita `designador.tipo` obrigatório e
`prefixo`/`sufixo` opcionais. Tipos visuais emitem
`prefixo + designador_base + sufixo`. H-0073 apenas consome essa
capacidade. Nenhum artefato H-0072 foi alterado neste patch.

## ACH-001 resolvido

O QA pós-P01 exigia preservar `A)` em H-0055. P02 comprovou que o schema
então só-`tipo` não representava `sufixo: ")"` e terminou
`BLOCKED_DOCUMENTATION` sem editar o handoff. `A` não foi aceito como
equivalente. Este P03 remove o bloqueio: a configuração estrutural de
H-0055 declara `sufixo: ")"`. O histórico permanece em §9.3; o estado
ativo é `RESOLVIDO`.

## H-0055 fechado com `sufixo: ")"`

Configuração estrutural autorizada em
`config/telas/demo/h0055_dois_niveis_por_foco.json`:

```yaml
formato.dois_niveis_por_foco.filho:
  tabulacao: {minimo: 5, maximo: 10}
  designador:
    tipo: alfabetico_maiusculo
    sufixo: ")"
  apresentacao: texto
```

O `)` vem da configuração estrutural. Não há herança do conteúdo.
H-0055: `FECHADO_PARA_IMPLEMENTACAO`.

## Expectativa `A)` preservada

Resultado visual obrigatório: `A)`, `B)`, `C)`, `D)`. Critérios, testes e
demonstrações que ainda aceitavam `A`/`B`/`C`/`D` sem `)` foram
corrigidos. Essa forma sem `)` não é resultado correto.

Conteúdo externo
`config/telas/demo/h0055_dois_niveis_por_foco_conteudo.json` permanece
PRESERVADO byte-a-byte, inclusive a declaração histórica de designador.
Não depende de herança automática.

Navegação, toroides, seleção, conteúdo, ordem, identidade lógica e
`apresentacao: texto` permanecem. Só muda a disposição física:
tabulação → `ec` → `tg` → designador → conteúdo, tabulação 5..10.

## H-0063 preservado do P01

Não reaberto. Estrutural: tabulação 5..10, `designador.tipo: nenhum`,
`apresentacao: tabela`, colunas `preset` e `amostra`, espaçamento 3..8.
Projeção: `preset` inalterado; `titulo` inalterado; `amostra` nova, mesmo
valor semântico, sem parsing de `titulo`. Nenhum conteúdo visível muda.
H-0063: `FECHADO_PARA_IMPLEMENTACAO`.

## Escopo nominal final

Lista do P01, alterada só no que ACH-001 exigiu (`A)` / `sufixo: ")"`).

Edição: JSON estrutural H-0055; JSON estrutural H-0063; `tela/estilo.py`;
`tela/teste_navegacao.py`; `demo/teste_demo_console.py`.

Novos: `demo/teste_demo_h0073_h0055_reconciliado.py`;
`tela/teste_estilo_h0073_h0063.py`;
`demo/teste_demo_h0073_h0063_reconciliado.py`.

Leitura/teste: `tela/renderizacao/estilo.py` (sem edição);
`demo/demo.py`; regressões H-0063/H-0064..H-0068; H-0070; H-0072.

Preservados: conteúdo H-0055; `h0062_estilo.json` (precedente histórico,
sem reconciliação); código/fixtures/testes H-0072; navegação; seleção.

Nenhuma descoberta transferida a IMPLEMENTAR.

## Testes e demonstrações

H-0055 deve provar: `sufixo: ")"` estrutural; renderer emite `A)`; `)` da
configuração estrutural; conteúdo byte-a-byte; tabulação 5..10; unidade
deslocada; `texto`; navegação/seleção.

H-0063 preserva os 18 critérios do P01.

Demonstrações reais via `demo/demo.py`, não só helper isolado.

Relatório futuro: `docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0073.md`.

## Regressão H-0070

`tela/teste_estilo_h0070.py::test_filhos_sem_ordinais_cursor_e_indicadores_preservados`
entra na suíte. Assertiva não alterada. Se passar pela tabulação nova,
registrar resolução causal; se falhar, QA da implementação decide.
Maquiagem proibida.

## Regressão H-0072

Obrigatória. Nenhum artefato H-0072 é alterado para obter verde. O caso
`sufixo ")"` já foi aprovado em H-0072.

## Resíduos de bloqueio removidos

Passagens ativas que implicavam ACH-001 pendente, H-0055 bloqueada,
incapacidade de `A)`, necessidade de alterar H-0072 ou nova decisão
documental foram reescritas. O histórico permanece só como contexto.
Estado executivo: H-0055 e H-0063 `FECHADO_PARA_IMPLEMENTACAO`;
bloqueios: nenhum.

## Verificações

- leitura integral do H-0073, P01, P02, QA H-0072 P01,
  `contrato_tela_json.md` e `contrato_console.md`;
- leitura focal dos dois JSON de H-0055 (conteúdo intocado);
- `sufixo: ")"` literal na configuração estrutural de H-0055;
- nenhuma expectativa `A` sem `)` como resultado correto;
- H-0063 continua `preset`/`amostra`;
- H-0072 e arquivos de implementação não alterados neste patch;
- `git diff --check` nos dois artefatos desta etapa.

## Bloqueios restantes

Nenhum.
\n