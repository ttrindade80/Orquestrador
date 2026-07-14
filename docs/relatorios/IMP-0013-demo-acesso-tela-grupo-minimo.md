# Implementação — H-0013 Demo de acesso à tela grupo mínimo

## Status

IMPLEMENTATION_COMPLETED

## Objetivo

Tornar a tela `grupo_minimo` (entregue pelo H-0012) acessível pelo fluxo
demonstrável (`python tela/demo.py`) por meio de um item declarativo no
lançador do Orquestrador, sem alterar código de módulos e sem adicionar
segundo elemento ao grupo.

A implementação é majoritariamente declarativa: o item é um valor em
`lancador_principal.itens[]` já suportado pelo binding existente em
`tela/demo.py` (`processar_comando` já percorre `lancador.itens[]` do
modelo).

## Escopo implementado

1. Adicionado item declarativo ao `lancador_principal.itens[]` de
   `config/telas/orquestrador.json` apontando para `grupo_minimo`.
2. Atualizadas as constantes de expected output dos testes que fazem
   comparação estrita com a saída do Orquestrador.
3. Adicionados testes de navegação unitária e de subprocess cobrindo o
   caminho demonstrável `orquestrador → grupo_minimo → orquestrador`.
4. Atualizada a contagem de itens do lançador nos testes de loader e
   modelo (1 → 2 itens) e adicionada verificação do novo item.
5. Criado este relatório.

Nenhum código de runtime foi alterado.

## Arquivos criados

- `docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md`

## Arquivos alterados

- `config/telas/orquestrador.json`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`

## Decisões locais

Não houve decisão arquitetural nova. Todas as escolhas abaixo estão
cobertas pelo handoff H-0013 (seções F-1, F-3, F-4) e não introduzem
novo tipo de chip, novo mecanismo, nova semântica, novo registry nem
novo binding.

- **Item declarativo**: escolhidos os valores recomendados pelo handoff
  em F-1:

  ```json
  {
    "id": "item_grupo_minimo",
    "chip": "g",
    "texto": "Grupo Min.",
    "tela_destino": "grupo_minimo"
  }
  ```

  - `chip == "g"`: único no lançador, não conflita com `d` nem com os
    controles internos da demo (`b`, `s`, `\x1b`).
  - `texto == "Grupo Min."`: 10 caracteres (≤ 15).
  - `tela_destino == "grupo_minimo"`: arquivo já existente.
  - O item existente `item_destino_minimo` (`d → destino_minimo`)
    permanece inalterado e na mesma posição (índice 0); o novo item foi
    anexado após ele (índice 1).

- **Constantes `_EXPECTED_*`**: as strings foram derivadas executando
  `renderizar_tela` sobre o modelo carregado (não calculadas à mão),
  conforme orientação do handoff em F-3. Em todas as larguras, a nova
  linha `│ [g] Grupo Min. <padding> │` foi inserida imediatamente após
  a linha `│ [d] Destino <padding> │`, dentro da caixa `NAVEGAR`.

- **Teste condicional `teste_renderizador.py`**: o relatório de
  auditoria confirmou que o arquivo possui `_EXPECTED_ORQUESTRADOR` e
  `_EXPECTED_ORQUESTRADOR_RETA` (ambas 42 chars) com `[d] Destino`.
  Ambas foram atualizadas para incluir `[g] Grupo Min.`, conforme
  autorizado pela seção "Alterar condicional" do handoff.

- **Testes condicionais `teste_loader.py` e `teste_modelo.py`**: o
  relatório de auditoria confirmou que ambos verificam
  `lancador_principal.itens` / `_campos_inertes["itens"]` com contagem
  1. A contagem foi atualizada para 2 e foram adicionadas verificações
  do novo item (id/chip/texto/tela_destino), conforme autorizado pela
  seção "Alterar condicional" do handoff.

- **Novos testes de navegação** (`teste_demo.py`):

  - Em `teste_navegacao_minima`: casos cobrindo `chip "g"` muda
    `tela_atual` para `"grupo_minimo"`; empilha `"orquestrador"`; não
    altera `tipo_borda` nem `saindo`; Esc em `grupo_minimo` volta para
    `"orquestrador"`; Esc em `grupo_minimo` não define `saindo`;
    ciclo completo.
  - Em `teste_navegacao_subprocess`: caso cobrindo
    `"g\n\x1b\n\x1b\n"` com 3 renders (orq-curva, grupo-curva,
    orq-curva), verificação de `"GRUPO MINIMO"` e `"[Esc] Voltar"` no
    stdout, stderr vazio e `grupo_minimo.json` inalterado.
  - Novas constantes `_EXPECTED_GRUPO_MINIMO_CURVA_80` e
    `_EXPECTED_GRUPO_MINIMO_RETA_80` para os testes de navegação.

## Resumo da implementação

O fluxo demonstrável já existia no código (H-0009/H-0010A/H-0012). A
adição de um item ao JSON do Orquestrador é suficiente para que
`processar_comando` (em `tela/demo.py`) reconheça o chip `g`, empilhe
`orquestrador` e troque para `grupo_minimo`. Esc faz pop da pilha e
volta ao Orquestrador. Nenhuma linha de código de módulo mudou.

```
demo.py main()
  → _carregar_modelo_por_id("orquestrador")
  → processar_comando(estado, "g", modelo)   [reconhece chip "g"]
  → estado["tela_atual"] = "grupo_minimo"; pilha = ["orquestrador"]
  → _carregar_modelo_por_id("grupo_minimo")  [H-0012]
  → renderizar_tela(modelo_grupo, ...)        [H-0012]
  → Esc → pop pilha → volta ao Orquestrador
```

## Diff da declaração (orquestrador.json)

```diff
@@ -111,6 +111,12 @@
             "chip": "d",
             "texto": "Destino",
             "tela_destino": "destino_minimo"
+          },
+          {
+            "id": "item_grupo_minimo",
+            "chip": "g",
+            "texto": "Grupo Min.",
+            "tela_destino": "grupo_minimo"
           }
         ]
       }
```

## Constantes `_EXPECTED_*` atualizadas

Em todos os casos, a linha `│ [g] Grupo Min. <padding> │` foi inserida
imediatamente após `│ [d] Destino <padding> │` (mesma caixa `NAVEGAR`).

| Arquivo | Constante | Largura |
|---|---|---|
| `tela/teste_diagnostico.py` | `_EXPECTED_ORQUESTRADOR` | 42 |
| `tela/teste_renderizador.py` | `_EXPECTED_ORQUESTRADOR` | 42 |
| `tela/teste_renderizador.py` | `_EXPECTED_ORQUESTRADOR_RETA` | 42 |
| `tela/teste_demo.py` | `_EXPECTED_CURVA` | 80 |
| `tela/teste_demo.py` | `_EXPECTED_RETA` | 80 |
| `tela/teste_demo.py` | `_EXPECTED_DIAGNOSTICO_CURVA_42` | 42 |

Novas constantes em `tela/teste_demo.py`:

| Constante | Largura | Conteúdo |
|---|---|---|
| `_EXPECTED_GRUPO_MINIMO_CURVA_80` | 80 | `grupo_minimo` curva |
| `_EXPECTED_GRUPO_MINIMO_RETA_80` | 80 | `grupo_minimo` reta |

## Testes executados

### Validade do JSON alterado

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

Resultado: `orquestrador.json OK` (exit 0).

### JSONs de produção inalterados

```bash
python -m json.tool config/telas/grupo_minimo.json >/dev/null && echo "grupo_minimo.json OK"
python -m json.tool config/telas/destino_minimo.json >/dev/null && echo "destino_minimo.json OK"
```

Resultado: ambos `OK` (exit 0).

### Testes unitários

| Comando | Exit code | [FALHOU] | Traceback | Total/Passaram |
|---|---|---|---|---|
| `python tela/teste_loader.py` | 0 | 0 | 0 | 66 / 66 |
| `python tela/teste_modelo.py` | 0 | 0 | 0 | 53 / 53 |
| `python tela/teste_renderizador.py` | 0 | 0 | 0 | 112 / 112 |
| `python tela/teste_demo.py` | 0 | 0 | 0 | 107 / 107 |
| `python tela/teste_diagnostico.py` | 0 | 0 | 0 | 28 / 28 |

### Diagnóstico (integridade do Orquestrador)

```bash
python tela/diagnostico.py
```

Resultado: exit 0. A saída agora reflete o novo item do lançador
(inclui a linha `│ [g] Grupo Min.                         │` na caixa
`NAVEGAR`) e bate com `_EXPECTED_ORQUESTRADOR` atualizado em
`tela/teste_diagnostico.py`.

### Verificação do novo chip via loader

```bash
python -c "from tela.loader import carregar_tela; r=carregar_tela(None,'orquestrador'); itens=r['corpo']['elementos'][2]['itens']; print([i['chip'] for i in itens], [i['tela_destino'] for i in itens])"
```

Resultado: `['d', 'g'] ['destino_minimo', 'grupo_minimo']` (exit 0).

### Verificação de navegação via subprocess (demo)

```bash
python -c "import subprocess,sys,os; env={k:v for k,v in os.environ.items() if k!='COLUMNS'}; p=subprocess.run([sys.executable,'tela/demo.py'],cwd='.',input='g\n\x1b\n\x1b\n',capture_output=True,text=True,env=env); print('exit',p.returncode,'GRUPO MINIMO' in p.stdout, '[Esc] Voltar' in p.stdout, p.stderr=='')"
```

Resultado: `exit 0 True True True` — `grupo_minimo` é exibida, `[Esc]
Voltar` aparece na barra, stderr vazio.

### Cache e estado Git

```bash
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
```

Resultado: nenhum `__pycache__` nem `.pyc` permanece. `git status --short`:

```text
 M config/telas/orquestrador.json
 M tela/teste_demo.py
 M tela/teste_diagnostico.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? docs/handoff/H-0013-demo-acesso-tela-grupo-minimo.md
?? docs/relatorios/IMP-0013-demo-acesso-tela-grupo-minimo.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0013_HANDOFF.md
```

Os `M` (alterados) e o `??` criado pelo executor (este relatório) estão
todos dentro da lista de arquivos permitidos do H-0013. Os demais `??`
(handoff H-0013 e relatório de auditoria) são os documentos não
rastreados esperados, anteriores à implementação, e não foram tocados.

## Preservações

- `tela/demo.py` não foi alterado (nenhum diff).
- `tela/loader.py` não foi alterado (nenhum diff).
- `tela/modelo.py` não foi alterado (nenhum diff).
- `tela/renderizador.py` não foi alterado (nenhum diff).
- `tela/diagnostico.py` não foi alterado (nenhum diff).
- `config/telas/grupo_minimo.json` não foi alterado (nenhum diff).
- `config/telas/destino_minimo.json` não foi alterado (nenhum diff).
- Nenhum contrato em `docs/contratos/` foi alterado.
- Nenhuma ADR em `docs/adr/` foi alterada.
- `docs/NOMENCLATURA.md` e `docs/INDICE.md` não foram alterados.
- `docs/handoff/` não foi alterado pelo executor.
- Nenhum commit foi realizado.
- Nenhum `__pycache__` ou `.pyc` permanece no repositório.
- `grupo_minimo` continua com exatamente 1 elemento funcional interno.
- Nenhum segundo elemento foi adicionado ao grupo.
- Nenhuma composição horizontal foi implementada.

## Cobertura dos critérios de aceite

- **CA-01..CA-06** (declaração no Orquestrador): atendidos. JSON válido;
  item com `id`/`chip`/`texto`/`tela_destino`; `tela_destino ==
  "grupo_minimo"`; `texto` com 10 chars (≤ 15); `chip "g"` único; item
  `destino_minimo` preservado.
- **CA-07..CA-09** (fluxo demonstrável): atendidos por `teste_demo.py`
  (subprocess `g\n\x1b\n\x1b\n` exibe `grupo_minimo` com
  `GRUPO MINIMO` e `[Esc] Voltar`; Esc volta sem `saindo`).
- **CA-10** (`destino_minimo` continua funcionando): atendido — todos
  os testes existentes de `destino_minimo` permanecem passando.
- **CA-11..CA-12** (Esc): atendidos — testes existentes preservados.
- **CA-13** (`b` alterna borda): atendido — não há mudança de código.
- **CA-14..CA-16** (grupo com 1 elemento; sem segundo elemento; sem
  composição horizontal): atendidos — `grupo_minimo.json` inalterado.
- **CA-17..CA-22** (testes exit 0): atendidos.
- **CA-23..CA-36** (escopo/rastreabilidade): atendidos — código de
  módulo, JSONs de produção, contratos, ADRs, NOMENCLATURA, INDICE
  intactos; sem commit; sem `__pycache__`/`.pyc`; IMP-0013 criado.

## Resultado final

PASSOU.

Todos os comandos obrigatórios encerram com código de saída 0, sem
linhas `[FALHOU]` e sem traceback. Somente arquivos permitidos foram
criados/alterados. O fluxo demonstrável para `grupo_minimo` funciona
via item declarativo do lançador, sem alteração de código de runtime.

O teste manual via TTY real (sequência descrita no handoff) não foi
executado por impossibilidade de automação neste ambiente; os critérios
automatizáveis (unitário + subprocess) cobrem integralmente o fluxo.
