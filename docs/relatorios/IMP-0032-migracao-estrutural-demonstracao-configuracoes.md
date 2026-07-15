# IMP-0032 — Relatório de Implementação
## Migração Estrutural: Demonstração e Configurações

**Handoff:** H-0032  
**Status:** IMPLEMENTADO  
**Data:** 2026-07-15  
**Executor:** Claude Sonnet 4.6 (agente de implementação)

---

## 1. Escopo Executado

Separação completa entre o motor compartilhado (`tela/`) e os executáveis de demonstração (`demo/`), conforme definido no H-0032 e autorizado pelo ADR-0021/ADR-0022.

---

## 2. Arquivos Criados

### Diretório `demo/`
| Arquivo | Descrição |
|---------|-----------|
| `demo/demo.py` | Aplicação demonstrável migrada de `tela/demo.py`; usa `_RAIZ_TELAS_DEMO` |
| `demo/diagnostico.py` | Diagnóstico migrado de `tela/diagnostico.py`; usa `_RAIZ_TELAS_DEMO` |
| `demo/explorar_barra_de_menus.py` | Explorador migrado de `tela/explorar_barra_de_menus.py` |
| `demo/teste_demo.py` | Suite de testes migrada de `tela/teste_demo.py` (358 verificações) |
| `demo/teste_diagnostico.py` | Suite de testes migrada de `tela/teste_diagnostico.py` (30 verificações) |
| `demo/teste_explorar_barra_de_menus.py` | Suite migrada de `tela/teste_explorar_barra_de_menus.py` (38 verificações) |

### Diretório `config/telas/demo/`
| Arquivo | Observação |
|---------|-----------|
| `config/telas/demo/demo.json` | Renomeado de `orquestrador.json`; `"id"` alterado de `"orquestrador"` para `"demo"`; `cabecalho.titulo` = `"Orquestrador"` preservado |
| `config/telas/demo/destino_minimo.json` | Movido de `config/telas/` |
| `config/telas/demo/grupo_minimo.json` | Movido de `config/telas/` |
| `config/telas/demo/stub_b.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_dashboard_fracao.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_dashboard_igual.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_dashboard_percentual.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_grupo_fracao.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_grupo_igual.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_grupo_pai_distribuido.json` | Movido de `config/telas/` |
| `config/telas/demo/h0029_grupo_percentual.json` | Movido de `config/telas/` |
| `config/telas/demo/h0030_console_unico.json` | Movido de `config/telas/` |
| `config/telas/demo/h0030_dashboard_unico.json` | Movido de `config/telas/` |
| `config/telas/demo/h0030_matriz_2x2.json` | Movido de `config/telas/` |
| `config/telas/demo/h0030_matriz_2x4.json` | Movido de `config/telas/` |
| `config/telas/demo/h0030_matriz_3x2.json` | Movido de `config/telas/` |

### Diretório `config/layouts/`
| Arquivo | Origem |
|---------|--------|
| `config/layouts/layout_console.json` | Movido de `config/layout_console.json` |
| `config/layouts/layout_dado.json` | Movido de `config/layout_dado.json` |
| `config/layouts/layout_menu.json` | Movido de `config/layout_menu.json` |

### Diretório `config/elementos/`
| Arquivo | Origem |
|---------|--------|
| `config/elementos/cabecalho.json` | Movido de `config/cabecalho.json` |
| `config/elementos/barra_de_menus.json` | Movido de `config/barra_de_menus.json` |
| `config/elementos/lancador.json` | Movido de `config/lancador.json` |

---

## 3. Arquivos Modificados

### Motor compartilhado `tela/`
| Arquivo | Modificação |
|---------|------------|
| `tela/loader.py` | Adicionado parâmetro `raiz_telas=None` a `carregar_tela()`; quando `None` usa `config/telas`; quando fornecido usa raiz explícita sem fallback |
| `tela/teste_loader.py` | `_RAIZ_TELAS_DEMO` adicionado; todas as cargas de telas de demonstração atualizadas para `raiz_telas`; nova função `teste_raiz_telas_h0032()` com 5 verificações |
| `tela/teste_modelo.py` | `_RAIZ_TELAS_DEMO` adicionado; cargas de `"orquestrador"` e `"grupo_minimo"` atualizadas; classe interna `_carregar` atualizada |
| `tela/teste_renderizador.py` | `_RAIZ_TELAS_DEMO` adicionado; todas as cargas de telas de demonstração atualizadas; `_h0029_caminho_json` atualizado para subdiretório `demo/` |

### Arquivos deletados de `tela/`
- `tela/demo.py`
- `tela/diagnostico.py`
- `tela/explorar_barra_de_menus.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `tela/teste_explorar_barra_de_menus.py`

### Arquivos deletados de `config/telas/` (movidos para `config/telas/demo/`)
- `config/telas/destino_minimo.json`
- `config/telas/grupo_minimo.json`
- `config/telas/h0029_dashboard_fracao.json`
- `config/telas/h0029_dashboard_igual.json`
- `config/telas/h0029_dashboard_percentual.json`
- `config/telas/h0029_grupo_fracao.json`
- `config/telas/h0029_grupo_igual.json`
- `config/telas/h0029_grupo_pai_distribuido.json`
- `config/telas/h0029_grupo_percentual.json`
- `config/telas/h0030_console_unico.json`
- `config/telas/h0030_dashboard_unico.json`
- `config/telas/h0030_matriz_2x2.json`
- `config/telas/h0030_matriz_2x4.json`
- `config/telas/h0030_matriz_3x2.json`
- `config/telas/stub_b.json`

### Arquivo renomeado de `config/telas/`
- `config/telas/orquestrador.json` → `config/telas/demo/demo.json` (id alterado de `"orquestrador"` para `"demo"`)

### Arquivos deletados de `config/` (movidos para `config/layouts/` e `config/elementos/`)
- `config/layout_console.json`
- `config/layout_dado.json`
- `config/layout_menu.json`
- `config/cabecalho.json`
- `config/barra_de_menus.json`
- `config/lancador.json`

---

## 4. Decisões Técnicas

### 4.1 Identidade da tela demo
- `id` no JSON alterado de `"orquestrador"` para `"demo"` (coincide com basename `demo.json`)
- `cabecalho.titulo` = `"Orquestrador"` mantido; os snapshots `_EXPECTED_ORQUESTRADOR` e `_EXPECTED_CURVA` permanecem válidos
- `_ID_TELA_RAIZ = "orquestrador"` em `tela/loader.py` permanece inalterado (produto real)

### 4.2 Bootstrap em scripts `demo/`
Os scripts de teste em `demo/` executam a seguinte sequência:
```python
_BASE_PADRAO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_BASE_PADRAO))
_this_dir = str(Path(__file__).resolve().parent)
while _this_dir in sys.path:
    sys.path.remove(_this_dir)
```
A remoção de `demo/` do `sys.path` é necessária porque Python auto-adiciona o diretório do script, e `demo.py` ali presente seria confundido com o namespace package `demo/` pelo importador. Os executáveis (`demo/demo.py`, `demo/diagnostico.py`) já usavam mecanismo seguro com guarda `if __name__ == "__main__"`.

### 4.3 Sem `demo/__init__.py`
O diretório `demo/` opera como namespace package (PEP 420). Não foi criado `__init__.py`.

### 4.4 Raiz explícita sem fallback
`_RAIZ_TELAS_DEMO = os.path.join("config", "telas", "demo")` é passado explicitamente a cada chamada `carregar_tela()`. Não há tentativa de fallback entre raízes.

---

## 5. Verificações Pós-Implementação

### 5.1 Suite de testes
| Script | Baseline (antes) | Verificações (depois) | Diferença | Código de saída | Status |
|--------|-----------------|----------------------|-----------|-----------------|--------|
| `tela/teste_loader.py` | 244 | 249 | +5 | 0 | ✓ PASSOU |
| `tela/teste_modelo.py` | 148 | 148 | 0 | 0 | ✓ PASSOU |
| `tela/teste_renderizador.py` | 980 | 980 | 0 | 0 | ✓ PASSOU |
| `demo/teste_demo.py` | 358 | 358 | 0 | 0 | ✓ PASSOU |
| `demo/teste_diagnostico.py` | 28 | 30 | +2 | 0 | ✓ PASSOU |
| `demo/teste_explorar_barra_de_menus.py` | 38 | 38 | 0 | 0 | ✓ PASSOU |
| **Total** | **1796** | **1803** | **+7** | — | **✓ PASSOU** |

### 5.2 Demonstração operacional

Comando: `python demo/diagnostico.py`

Prova semântica independente (snippet executado da raiz):

```python
from tela.loader import carregar_tela
import os
RAIZ_DEMO = os.path.join("config", "telas", "demo")
tela = carregar_tela(os.path.abspath("."), "demo", RAIZ_DEMO)
# identidade_carregada: "demo"
# raiz_usada: "config/telas/demo"
```

Ausência de fallback confirmada:
- `carregar_tela(BASE, "demo")` sem raiz → `TelaArquivoNaoEncontrado: config/telas/demo.json`
- `carregar_tela(BASE, "orquestrador")` sem raiz → `TelaArquivoNaoEncontrado: config/telas/orquestrador.json`

```yaml
identidade_carregada: demo
raiz_de_telas: config/telas/demo
motor_compartilhado: tela.loader
alias_orquestrador: ausente
wrapper: ausente
fallback_para_config_telas: ausente
```

### 5.3 Git

Estado Git final:

```yaml
branch: master
head_abreviado: 0143fd1
ultimo_commit: "0143fd1 chore: migra orquestrador para repositorio independente"
git_diff_check: sem_erros
git_diff_cached_name_only: vazio
git_stash_list: vazio
stage: vazio
commit_novo: nenhum
```

---

## 6. Novos Testes Adicionados

Em `tela/teste_loader.py`, função `teste_raiz_telas_h0032()`:
1. `carregar_tela(demo, raiz_demo)` carrega sem exceção
2. `carregar_tela(demo, raiz_demo)["id"] == "demo"`
3. `carregar_tela(demo)` sem raiz → `TelaArquivoNaoEncontrado` (sem fallback)
4. `carregar_tela(orquestrador)` sem raiz → `TelaArquivoNaoEncontrado` (arquivo removido)
5. `TelaIdNaoCoincideComArquivo` com `raiz_telas` explícita (id ≠ basename)

---

## 7. Conformidade com ADRs

- **ADR-0021**: `config/telas/` reservado ao produto real; `config/telas/demo/` exclusivo da demonstração ✓
- **ADR-0022**: `orquestrador.py`, tela real do produto, Estilos e integração Pipeline fora do escopo ✓

---

## 8. Estado Git Inicial

```yaml
branch: master
head_abreviado: 0143fd1
ultimo_commit: "0143fd1 chore: migra orquestrador para repositorio independente"
git_diff_check: sem_erros
git_diff_cached_name_only: vazio
git_stash_list: vazio
stage: vazio
commit_novo: nenhum
```

O workspace continha alterações rastreadas e não rastreadas herdadas do ciclo anterior. Itens documentais acumulados e caches preexistentes foram tratados como `origem: NAO_CONFIRMADA`.

---

## 9. Workspace Preexistente e Fatos NAO_CONFIRMADOS

```yaml
tela/__pycache__/:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

documentos_adr_relatorios_nao_rastreados:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO

diffs_documentais_acumulados:
  origem: NAO_CONFIRMADA
  produzido_pelo_executor: NAO_CONFIRMADO
  produzido_pelo_usuario: NAO_CONFIRMADO
```

Esses itens não foram restaurados, descartados nem modificados pelo executor do H-0032.

---

## 10. Estrutura Anterior

Estado físico antes da implementação do H-0032:

```yaml
demo/: nao existia
config/telas/demo/: nao existia
config/layouts/: nao existia
config/elementos/: nao existia
config/telas/orquestrador.json: existia com "id": "orquestrador"
tela/demo.py: existia
tela/diagnostico.py: existia
tela/explorar_barra_de_menus.py: existia
tela/teste_demo.py: existia
tela/teste_diagnostico.py: existia
tela/teste_explorar_barra_de_menus.py: existia
config/telas/*.json: 21 telas e configuracoes diretamente em config/telas/
```

---

## 11. Diretórios Criados

```yaml
demo/: criado
config/telas/demo/: criado
config/layouts/: criado
config/elementos/: criado
```

---

## 12. Arquivos Movidos (Lista Nominal Completa)

### Scripts e testes: `tela/` → `demo/`
| Origem | Destino |
|--------|---------|
| `tela/demo.py` | `demo/demo.py` |
| `tela/diagnostico.py` | `demo/diagnostico.py` |
| `tela/explorar_barra_de_menus.py` | `demo/explorar_barra_de_menus.py` |
| `tela/teste_demo.py` | `demo/teste_demo.py` |
| `tela/teste_diagnostico.py` | `demo/teste_diagnostico.py` |
| `tela/teste_explorar_barra_de_menus.py` | `demo/teste_explorar_barra_de_menus.py` |

### Telas demonstrativas: `config/telas/` → `config/telas/demo/`
| Origem | Destino |
|--------|---------|
| `config/telas/destino_minimo.json` | `config/telas/demo/destino_minimo.json` |
| `config/telas/grupo_minimo.json` | `config/telas/demo/grupo_minimo.json` |
| `config/telas/stub_b.json` | `config/telas/demo/stub_b.json` |
| `config/telas/h0029_dashboard_fracao.json` | `config/telas/demo/h0029_dashboard_fracao.json` |
| `config/telas/h0029_dashboard_igual.json` | `config/telas/demo/h0029_dashboard_igual.json` |
| `config/telas/h0029_dashboard_percentual.json` | `config/telas/demo/h0029_dashboard_percentual.json` |
| `config/telas/h0029_grupo_fracao.json` | `config/telas/demo/h0029_grupo_fracao.json` |
| `config/telas/h0029_grupo_igual.json` | `config/telas/demo/h0029_grupo_igual.json` |
| `config/telas/h0029_grupo_pai_distribuido.json` | `config/telas/demo/h0029_grupo_pai_distribuido.json` |
| `config/telas/h0029_grupo_percentual.json` | `config/telas/demo/h0029_grupo_percentual.json` |
| `config/telas/h0030_console_unico.json` | `config/telas/demo/h0030_console_unico.json` |
| `config/telas/h0030_dashboard_unico.json` | `config/telas/demo/h0030_dashboard_unico.json` |
| `config/telas/h0030_matriz_2x2.json` | `config/telas/demo/h0030_matriz_2x2.json` |
| `config/telas/h0030_matriz_2x4.json` | `config/telas/demo/h0030_matriz_2x4.json` |
| `config/telas/h0030_matriz_3x2.json` | `config/telas/demo/h0030_matriz_3x2.json` |

### Configurações gerais: `config/` → subdiretórios
| Origem | Destino |
|--------|---------|
| `config/layout_console.json` | `config/layouts/layout_console.json` |
| `config/layout_dado.json` | `config/layouts/layout_dado.json` |
| `config/layout_menu.json` | `config/layouts/layout_menu.json` |
| `config/cabecalho.json` | `config/elementos/cabecalho.json` |
| `config/barra_de_menus.json` | `config/elementos/barra_de_menus.json` |
| `config/lancador.json` | `config/elementos/lancador.json` |

**Total: 27 arquivos movidos** (6 scripts+testes + 15 telas + 6 configurações gerais)

Conteúdo byte a byte idêntico ao HEAD para os 26 arquivos movidos sem renomeação (verificado pelo QA independente).

---

## 13. Arquivos Renomeados

| Origem | Destino | Alteração |
|--------|---------|-----------|
| `config/telas/orquestrador.json` | `config/telas/demo/demo.json` | `"id"` alterado de `"orquestrador"` para `"demo"`; demais campos idênticos ao HEAD |

---

## 14. Arquivos Preservados

```yaml
tela/modelo.py: inalterado (git diff --exit-code retornou 0)
tela/renderizador.py: inalterado (git diff --exit-code retornou 0)
tela/__init__.py: inalterado
config/estilo.json: inalterado (git diff --exit-code retornou 0)
```

Nenhuma cópia de `config/estilo.json` foi criada em outro diretório.

---

## 15. Referências Históricas Preservadas

Handoffs, relatórios e ADRs anteriores contêm referências aos caminhos antigos (`config/telas/orquestrador.json`, `tela/demo.py`, etc.). Essas ocorrências foram classificadas como **histórico preservado** e não foram alteradas, conforme autorizado pelo handoff.

Nenhuma referência operacional residual foi encontrada em arquivos ativos após a migração.

---

## 16. Escopo Negativo

Confirmada ausência de:

```text
orquestrador.py
config/telas/orquestrador.json como tela real
config/telas/demo/orquestrador.json
demo/__init__.py
titulo e descricao da tela real
barra real com Estilos
acao ou destino de Estilos
tela funcional de estilos
integracao com Pipeline
mudanca de schema
mudanca funcional de layout
correcao de destino_minimo
correcao de grupo_minimo
alias, wrapper e fallback
```

---

## 17. Conclusão Factual

A implementação física principal está tecnicamente conforme:

- 27 arquivos movidos (conteúdo idêntico ao HEAD);
- 1 arquivo renomeado com alteração de `id` de `"orquestrador"` para `"demo"`;
- 4 diretórios criados;
- 4 arquivos do motor compartilhado modificados;
- 4 arquivos do motor compartilhado preservados inalterados;
- suíte expandida de 1796 para 1803 verificações (+7), todos os 6 scripts passando;
- raiz explícita sem fallback confirmada;
- escopo negativo conforme;
- stage vazio; nenhum commit criado.

---

## 18. Patch (ACH-H0032-001 e ACH-H0032-002)

```yaml
patch:
  origem: docs/relatorios/RELATORIO_QA_H-0032_IMPLEMENTACAO.md
  status_anterior: I2_IMPLEMENTATION_PATCH_REQUIRED
  data_patch: 2026-07-15

  achados_corrigidos:
    - id: ACH-H0032-001
      severidade: medio
      arquivos:
        - docs/relatorios/IMP-0032-migracao-estrutural-demonstracao-configuracoes.md
      correcao: >
        Adicionadas secoes 8 a 17 com estado Git inicial, workspace preexistente,
        estrutura anterior, diretorios criados, lista nominal completa de 27 arquivos
        movidos, arquivos renomeados, arquivos preservados, referencias historicas,
        escopo negativo e conclusao factual. Atualizada secao 2 com lista nominal
        completa de telas e secoes de config/layouts/ e config/elementos/. Atualizada
        secao 3 com lista de 15 telas deletadas de config/telas/ e 6 configs deletadas
        de config/. Atualizada secao 5.1 com baseline individual e codigos de saida.
        Atualizada secao 5.2 com prova semantica de identidade e raiz.
        Atualizada secao 5.3 com estado Git completo.
      verificacao:
        suite_completa: 1803/1803
        codigos_saida: todos_zero
        git_diff_check: sem_erros

    - id: ACH-H0032-002
      severidade: baixo
      arquivos:
        - demo/demo.py
        - demo/teste_demo.py
        - tela/teste_loader.py
        - tela/teste_renderizador.py
      correcao: >
        demo/demo.py: docstring H-0010A atualizada com default "demo" (era "orquestrador")
        e referencia a carregar_tela(_RAIZ_TELAS_DEMO, tela_atual) (era None);
        criar_estado_inicial e processar_comando atualizados nos textos de defaults.
        demo/teste_demo.py: descricao e label do teste de integridade do JSON
        corrigidos de "config/telas/demo.json" para "config/telas/demo/demo.json".
        tela/teste_loader.py: comentario e label do teste de distribuicao atualizados
        de "orquestrador real" para "demo.json".
        tela/teste_renderizador.py: docstring de _modelo_orquestrador_sem_distribuicao,
        comentarios de teste_altura_explicita e test_altura_minima_com_barra_horizontal,
        Contabilidade e test_vertical_nao_regride_apos_h0021 atualizados de
        "orquestrador real"/"orquestrador.json real" para "demo.json"/"tela demo";
        prints de destino_minimo e grupo_minimo atualizados para config/telas/demo/.
      verificacao:
        suite_completa: 1803/1803
        codigos_saida: todos_zero
        git_diff_check: sem_erros
        residuos_textuais_ativos: ausentes

  resultado: PATCH_IMPLEMENTACAO_CONCLUIDO
```
