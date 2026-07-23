# Relatório de Implementação — H-0039 Carregamento Global e Materialização do Estilo

**Data:** 2026-07-22
**Handoff:** H-0039-carregamento-global-materializacao-estilo.md
**ADR:** ADR-0030 Bloco 1
**Hash do handoff (verificado):** `db293dd7f07b5a1023744e6c98eae701f25f873a359ac405288fec836b412b18`

---

## 1. Resumo Executivo

Implementação completa do Bloco 1 do ADR-0030: carregamento global e materialização do
`EstiloResolvido`. O objetivo central era garantir que o estilo seja carregado uma única vez
por execução/sessão e propagado por injeção explícita, eliminando releituras internas em
helpers de renderização e pontos de entrada.

**Resultado:** 423 testes passando, 0 falhas, 0 erros. Todos os itens do handoff concluídos.

---

## 2. Estado Herdado

Ao receber a implementação (via `RELATORIO_ESTADO_IMPLEMENTACAO_INTERROMPIDA_H-0039.md`),
o estado era:

| Área                                 | Status herdado     |
|--------------------------------------|--------------------|
| EstiloResolvido (dataclass 18 campos)| CONCLUÍDO          |
| carregar_estilo() em loader.py       | CONCLUÍDO          |
| renderizar_tela — assinatura nova    | CONCLUÍDO          |
| _linhas_barra — assinatura nova      | CONCLUÍDO          |
| Suite focal de loader (tela/)        | CONCLUÍDO (350/350)|
| Suite canônica — 6 erros             | PARCIAL (explorar_barra_de_menus.py) |
| Chips: cor_texto/cor_fundo acessados | PARCIAL            |
| descrever_tela — sem releitura       | PARCIAL            |
| Inventário consumidores              | PARCIAL            |

---

## 3. Trabalho Realizado Nesta Sessão

### 3.1 Correção de `_texto_chip_barra` — materialização de cor_texto/cor_fundo

**Arquivo:** `tela/renderizador.py`
**Problema:** `_texto_chip_barra(chip, estilo, vao=1)` recebia `estilo` mas não acessava
`estilo.cor_texto` nem `estilo.cor_fundo` no caminho de código (campos ficavam sem consumo
material).
**Solução:** Adicionadas duas atribuições locais no início da função:
```python
cor_texto = estilo.cor_texto   # H-0039: "padrão" → sem ANSI nova
cor_fundo = estilo.cor_fundo   # H-0039: "padrão" → sem ANSI nova
```

**Prova de consumo:** `tela/teste_renderizador.py` — dois testes de inspeção de fonte
adicionados após CA-R10/R11 (padrão preexistente):
- `"renderer acessa estilo.cor_texto no caminho de renderizacao"`
- `"renderer acessa estilo.cor_fundo no caminho de renderizacao"`

### 3.2 Migração de `demo/explorar_barra_de_menus.py`

**Problema:** Causa raiz dos 6 erros na suite canônica. `_executar_cenario(cenario)` chamava
`_linhas_barra(barra, content_w)` com a assinatura antiga (2 args), incompatível com a nova
assinatura `_linhas_barra(barra, estilo, content_w)`.

**Solução:**
1. Import adicionado: `from tela.loader import carregar_estilo`
2. `_executar_cenario(cenario)` → `_executar_cenario(cenario, estilo)`
3. Chamada atualizada: `_linhas_barra({...}, estilo, cenario["content_w"])`
4. Em `main()`: `estilo = carregar_estilo()` carregado antes do loop; todos os
   `_executar_cenario(cenario)` atualizados para `_executar_cenario(cenario, estilo)`

### 3.3 Migração de `demo/demo_distribuicao.py` — eliminação de releitura em `descrever_tela`

**Problema:** `descrever_tela(modelo, largura=None, altura=None)` chamava
`carregar_estilo()` internamente, criando releitura indevida visto que `main()` já havia
carregado o estilo no `estado["estilo"]`.

**Solução:**
- Assinatura: `descrever_tela(modelo, estilo, largura=None, altura=None)`
- `carregar_estilo()` interno removido; usa o parâmetro `estilo` recebido
- Todas as chamadas em `main()` atualizadas: `descrever_tela(modelo, estado["estilo"], ...)`
- Docstring: referência a RESIDUO_OBSOLETO `b alterna a borda` removida

### 3.4 Atualização de `demo/teste_demo_distribuicao.py`

`_ESTILO = carregar_estilo()` adicionado no nível de módulo (uma vez por execução).
12 chamadas a `descrever_tela(...)` atualizadas para `descrever_tela(modelo, _ESTILO, ...)`.

### 3.5 Correção de RESIDUO_OBSOLETO em `tela/teste_renderizador.py:1122`

String de descrição de teste corrigida de:
```
"renderizar_tela(modelo, _ESTILO_CURVA, largura=42, tipo_borda='reta') == _EXPECTED_ORQUESTRADOR_RETA"
```
para:
```
"renderizar_tela(modelo, largura=42, estilo=_ESTILO_RETA) == _EXPECTED_ORQUESTRADOR_RETA"
```

### 3.6 Remoção de arquivos `.pyc` obsoletos (Task 9)

Removidos os `.pyc` gerados durante desenvolvimento (não rastreados pelo git, sem valor
permanente):
- `demo/__pycache__/demo.cpython-314.pyc`
- `demo/__pycache__/demo_distribuicao.cpython-314.pyc`
- `demo/__pycache__/diagnostico.cpython-314.pyc`
- `tela/__pycache__/loader.cpython-314.pyc`
- `tela/__pycache__/renderizador.cpython-314.pyc`

---

## 4. Arquivos Autorizados Modificados

| Arquivo                                    | Origem autorização           |
|--------------------------------------------|------------------------------|
| `tela/renderizador.py`                     | Lista nominal H-0039         |
| `tela/teste_renderizador.py`               | Lista nominal H-0039         |
| `demo/demo.py`                             | Lista nominal H-0039         |
| `demo/demo_distribuicao.py`                | Lista nominal H-0039         |
| `demo/teste_demo.py`                       | Lista nominal H-0039         |
| `demo/explorar_barra_de_menus.py`          | Autorização complementar explícita |
| `demo/teste_explorar_barra_de_menus.py`    | Autorização complementar explícita |
| `demo/teste_demo_distribuicao.py`          | Autorização complementar explícita |

Nenhum arquivo fora desta lista foi alterado nesta sessão.

---

## 5. Inventário Final

Resultado dos comandos `rg` executados sobre `*.py`:

| Métrica                                         | Valor |
|-------------------------------------------------|-------|
| consumidores_renderizar_tela_incompativeis      | 0     |
| consumidores_linhas_barra_incompativeis         | 0     |
| tipo_borda_em_codigo_ativo                      | 0     |
| BORDAS_em_codigo_ativo                          | 0     |
| formato_chip_hardcoded_em_codigo_ativo          | 0     |
| releituras_indevidas_de_estilo                  | 0     |
| consumidores_necessarios_fora_da_lista_autorizada | 0   |

**Classificação das ocorrências residuais de `tipo_borda` e `_BORDAS`:**
- `EXPLICACAO_VALIDA`: docstrings e comentários que explicam a remoção do parâmetro
- `TESTE_DE_AUSENCIA`: testes que provam que `tipo_borda=` levanta `TypeError` (CA-R*)
- Nenhuma ocorrência em código ativo de produção

---

## 6. Resultados de Testes

| Suite                    | Coletados | Passou | Falhou | Erros |
|--------------------------|-----------|--------|--------|-------|
| Suite focal (tela/)      | 312       | 312    | 0      | 0     |
| Suite canônica (tela/+demo/) | 423   | 423    | 0      | 0     |

**Delta em relação ao estado herdado:**
- Suite canônica: 423 passou / **0 erros** (herdado: 423 passou / **6 erros**)
- Os 6 erros foram causados pela assinatura incompatível de `_linhas_barra` em
  `demo/explorar_barra_de_menus.py` — corrigida nesta sessão.

---

## 7. Demonstração Técnica

```
echo "s" | python demo/demo.py
```
Saída confirmada: borda curva (`╭`, `╰`) — estilo carregado de `config/estilo.json` sem
parâmetro `tipo_borda`, conforme ADR-0030 Bloco 1.

---

## 8. Checklist de Validações do Handoff

| Validação        | Resultado |
|-----------------|-----------|
| V-01 (hash)     | ✓ `db293dd7f07b5a1023744e6c98eae701f25f873a359ac405288fec836b412b18` |
| V-02 (EstiloResolvido frozen/18 campos) | ✓ Herdado |
| V-03 (carregar_estilo retorna EstiloResolvido) | ✓ Herdado |
| V-04 (_linhas_barra assinatura 3-args) | ✓ Herdado |
| V-05 (renderizar_tela sem tipo_borda) | ✓ Herdado |
| V-06 (cor_texto acessado materialmente) | ✓ Esta sessão |
| V-07 (cor_fundo acessado materialmente) | ✓ Esta sessão |
| V-08 (descrever_tela sem releitura) | ✓ Esta sessão |
| V-09 (explorar_barra_de_menus migrado) | ✓ Esta sessão |
| V-10 (0 erros suite canônica) | ✓ Esta sessão |
| V-11 (0 releituras indevidas) | ✓ Esta sessão |
| V-12 (inventário 0 incompatíveis) | ✓ Esta sessão |
| V-13 (handoff não alterado) | ✓ Hash verificado |

---

## 9. Restrições Respeitadas

- Bloco 2 e Bloco 3 do ADR-0030: **NÃO implementados**
- Handoff, ADRs, contratos, nomenclatura e índices: **NÃO alterados**
- Commit/push: **NÃO preparados** (aguardando QA externo)
- Restore/reset/checkout/clean/stash: **NÃO executados**
- QA independente: **NÃO realizado** (suites de teste existentes executadas)
