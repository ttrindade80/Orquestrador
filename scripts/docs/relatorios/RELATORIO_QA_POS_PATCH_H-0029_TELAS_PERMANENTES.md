# QA pós-patch H-0029 — telas permanentes

## 1. Identificação

```yaml
ciclo: H-0029
tipo: QA_POS_PATCH
data: 2026-07-13
auditor: Codex
status_literal: QA_POS_PATCH_COMPLETED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Este relatório audita exclusivamente o estado pós-patch das telas permanentes do
H-0029. Nenhum código, teste, JSON, handoff, ADR, contrato ou relatório
histórico foi corrigido por esta auditoria.

## 2. Arquivos e autoridades consultadas

Arquivos consultados:

- `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`;
- `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md`;
- `scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md`;
- `scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md`;
- `scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`;
- `scripts/tela/renderizador.py`;
- `scripts/tela/teste_renderizador.py`;
- `scripts/tela/demo.py`;
- os sete JSONs `scripts/config/telas/h0029_*.json`;
- os quatro JSONs de referência `grupo_minimo.json`, `destino_minimo.json`, `stub_b.json`, `orquestrador.json`.

## 3. Estado Git e escopo

Raiz Git:

```text
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

Conferência inicial, a partir da raiz Git:

```text
 M scripts/tela/renderizador.py
 M scripts/tela/teste_renderizador.py
?? scripts/config/telas/h0029_dashboard_fracao.json
?? scripts/config/telas/h0029_dashboard_igual.json
?? scripts/config/telas/h0029_dashboard_percentual.json
?? scripts/config/telas/h0029_grupo_fracao.json
?? scripts/config/telas/h0029_grupo_igual.json
?? scripts/config/telas/h0029_grupo_pai_distribuido.json
?? scripts/config/telas/h0029_grupo_percentual.json
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_CORRECAO_GRUPO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_POS_PATCH_TELAS_PERMANENTES.md
?? scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```

`git diff --name-only`:

```text
scripts/tela/renderizador.py
scripts/tela/teste_renderizador.py
```

`git diff --check`: sem saída; código de saída `0`.

Arquivos inesperados no escopo substantivo: nenhum. Não há diff em
`scripts/tela/demo.py`, `scripts/tela/loader.py`, `scripts/tela/modelo.py`,
`scripts/docs/adr/`, `scripts/docs/contratos/` ou
`scripts/config/telas/orquestrador.json`.

Caches observados após a execução dos testes de QA, não limpos por instrução:

```text
scripts/tela/__pycache__/teste_renderizador.cpython-314.pyc
scripts/tela/__pycache__/renderizador.cpython-314.pyc
scripts/tela/__pycache__/__init__.cpython-314.pyc
scripts/tela/__pycache__/modelo.cpython-314.pyc
scripts/tela/__pycache__/loader.cpython-314.pyc
```

## 4. Sete JSONs permanentes

Confirmado que existem exatamente os sete JSONs `h0029_*` autorizados:

```text
h0029_dashboard_fracao.json
h0029_dashboard_igual.json
h0029_dashboard_percentual.json
h0029_grupo_fracao.json
h0029_grupo_igual.json
h0029_grupo_pai_distribuido.json
h0029_grupo_percentual.json
```

Não foram encontrados outros JSONs `h0029_*`. Não há integração das telas ao
lançador do `orquestrador.json`.

Os sete JSONs têm sintaxe válida, `schema: tela.v1`, `id` igual ao nome do
arquivo sem extensão, cabeçalho válido, `barra_de_menus` carregável, corpo
vertical com um filho direto, textos visíveis identificando o cenário e
cardinalidade compatível com as distribuições declaradas.

Resumo declarativo:

| Tela | corpo.distribuicao | filho direto | grupo.distribuicao |
|---|---|---|---|
| `h0029_dashboard_igual` | `{"modo": "igual"}` | `dashboard` | n/a |
| `h0029_dashboard_fracao` | `{"modo": "fracao", "valores": [1]}` | `dashboard` | n/a |
| `h0029_dashboard_percentual` | `{"modo": "percentual", "valores": [100]}` | `dashboard` | n/a |
| `h0029_grupo_pai_distribuido` | `{"modo": "fracao", "valores": [1]}` | `grupo` | ausente |
| `h0029_grupo_igual` | `{"modo": "igual"}` | `grupo` | `{"modo": "igual"}` |
| `h0029_grupo_fracao` | `{"modo": "fracao", "valores": [1]}` | `grupo` | `{"modo": "fracao", "valores": [1]}` |
| `h0029_grupo_percentual` | `{"modo": "percentual", "valores": [100]}` | `grupo` | `{"modo": "percentual", "valores": [100]}` |

Não foram identificadas telas 2x2, 3x2 ou 2x4, nem funcionalidades novas de
navegação, seleção ou execução do console nos JSONs do H-0029.

## 5. Preservação dos JSONs de referência

Comandos executados:

```bash
git diff -- scripts/config/telas/grupo_minimo.json
git diff -- scripts/config/telas/destino_minimo.json
git diff -- scripts/config/telas/stub_b.json
git diff -- scripts/config/telas/orquestrador.json
```

Resultado: os quatro diffs estão vazios.

Os testes nominais carregam `grupo_minimo`, `destino_minimo` e `stub_b` pelo
loader/modelo reais sem exigir alteração temporária nesses arquivos. O mecanismo
documentado do `demo.py` também não edita JSON, embora contenha o achado
funcional registrado na seção 15.

## 6. Geometria dos dashboards diretos

Telas auditadas:

- `h0029_dashboard_igual`;
- `h0029_dashboard_fracao`;
- `h0029_dashboard_percentual`.

Para largura `42` e alturas `20` e `30`, a renderização pelo caminho real
`carregar_tela -> construir_modelo -> renderizar_tela` confirmou:

| Tela | altura | linhas | topos | bases | barra |
|---|---:|---:|---|---|---:|
| `h0029_dashboard_igual` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_dashboard_igual` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |
| `h0029_dashboard_fracao` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_dashboard_fracao` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |
| `h0029_dashboard_percentual` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_dashboard_percentual` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |

Conclusão: dashboard no topo correto do corpo, borda inferior imediatamente
antes da barra, altura total correta, barra nas posições declaradas, sem linhas
externas indevidas, bordas laterais contínuas e equivalência geométrica entre os
três modos.

## 7. Grupo pai distribuído sem distribuição interna

Tela auditada:

```text
h0029_grupo_pai_distribuido
```

Confirmado:

- corpo com `{"modo": "fracao", "valores": [1]}`;
- único grupo direto sem campo `distribuicao`;
- dashboard interno em altura natural;
- sobra como área estrutural do grupo;
- altura total correta;
- barra final em `17` para altura `20` e `27` para altura `30`;
- ausência de sobreposição;
- ausência de desaparecimento de linhas;
- teste nominal não exige incorretamente que a borda do dashboard chegue até a barra.

Evidência geométrica:

| altura | linhas | topos | bases | barra | linhas estruturais |
|---:|---:|---|---|---:|---:|
| 20 | 20 | `[0, 3, 17]` | `[2, 5, 19]` | 17 | 11 |
| 30 | 30 | `[0, 3, 27]` | `[2, 5, 29]` | 27 | 21 |

Esse cenário exercita o caminho corrigido no renderer: grupo estrutural recebe a
cota do pai distribuído, mas, por ausência de distribuição interna, mantém o
dashboard em altura natural e completa a cota com preenchimento estrutural.

## 8. Grupos distribuídos nos dois níveis

Telas auditadas:

- `h0029_grupo_igual`;
- `h0029_grupo_fracao`;
- `h0029_grupo_percentual`.

Confirmado:

- distribuição explícita no corpo;
- distribuição explícita no grupo;
- único dashboard recebendo toda a área interna;
- borda inferior imediatamente antes da barra;
- equivalência geométrica dos três modos;
- comportamento correto nas alturas `20` e `30`.

Evidência geométrica:

| Tela | altura | linhas | topos | bases | barra |
|---|---:|---:|---|---|---:|
| `h0029_grupo_igual` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_grupo_igual` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |
| `h0029_grupo_fracao` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_grupo_fracao` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |
| `h0029_grupo_percentual` | 20 | 20 | `[0, 3, 17]` | `[2, 16, 19]` | 17 |
| `h0029_grupo_percentual` | 30 | 30 | `[0, 3, 27]` | `[2, 26, 29]` | 27 |

## 9. Auditoria dos testes nominais

Classe auditada:

```text
TestTelasPermanentesH0029
```

Confirmado:

- 12 métodos `test_*`;
- 256 verificações nominais;
- 256 aprovadas ao executar a classe isoladamente;
- carregamento nominal dos sete arquivos;
- uso do loader, modelo e renderer reais;
- renderização pelo caminho real;
- testes para alturas `20` e `30`;
- verificação de índices de bordas;
- posição da barra;
- continuidade lateral;
- ausência de lacuna ou sobreposição;
- equivalência geométrica;
- preservação do cenário natural;
- cobertura que falharia diante da regressão visual de desaparecimento/encurtamento do grupo pai distribuído.

Métodos:

```text
test_existencia_e_sintaxe
test_carregamento_modelo
test_distribuicao_corpo_declarada
test_tipo_do_filho_do_corpo
test_distribuicao_interna_do_grupo
test_geometria_altura_largura_barra
test_geometria_dashboard_preenche_area
test_geometria_grupo_pai_distribuido_natural
test_equivalencia_dashboard_tres_modos
test_equivalencia_grupo_tres_modos
test_area_adicional_absorvida
test_ausencia_sobreposicao
```

Classificação dos testes: adequados para o objetivo nominal. Há verificações
auxiliares de `len(saida)` e largura uniforme, mas elas não são a única evidência:
a classe também inspeciona posições de bordas, barra, continuidade lateral,
gaps, equivalência e cenário natural. Não foram classificados como tautológicos
os testes que usam `renderizar_tela`, pois o objetivo desta etapa é integração
nominal pelo renderer real.

## 10. Correção acumulada do renderer

Diff acumulado em `scripts/tela/renderizador.py`:

```diff
+                fill_linha = " " * total_w
                 if bloco:
-                    partes.append(bloco)
+                    linhas_bloco = bloco.split("\n")
+                    while len(linhas_bloco) < cota:
+                        linhas_bloco.append(fill_linha)
+                    partes.append("\n".join(linhas_bloco))
+                elif cota > 0:
+                    partes.append("\n".join(fill_linha for _ in range(cota)))
```

Conclusão técnica:

- alteração limitada ao caminho vertical distribuído;
- completa a cota recebida por grupo estrutural quando o bloco natural tem menos linhas que a cota;
- não cria distribuição implícita no grupo;
- não altera a semântica de ausência de distribuição interna;
- não propaga distribuição entre níveis;
- não altera o caminho horizontal;
- não há evidência de impacto indevido em cardinalidade maior que um;
- efetivamente exercitada por `h0029_grupo_pai_distribuido`.

## 11. Comandos e mecanismo do demo.py

A seção 15.8 do relatório de implementação documenta sete comandos `python3 -c`
que substituem `tela.demo.criar_estado_inicial` no namespace do módulo e chamam
`d.main()`.

O mecanismo pretendido é válido em conceito: `demo.main()` usa o loop real da
demo e carrega a tela atual por `_carregar_modelo_por_id`, que por sua vez usa
`carregar_tela` e `construir_modelo`; a renderização passa por
`renderizar_estado -> renderizar_tela`. A substituição no namespace do módulo,
se correta, apenas selecionaria a tela inicial e não mascararia o comportamento
do renderer.

Porém, os sete comandos documentados não selecionam a tela alvo. A expressão
usada é:

```python
lambda: (_o().__setitem__('tela_atual', '<id>') or _o())
```

`_o()` é chamado duas vezes. A primeira chamada cria um estado, altera
`tela_atual` e retorna `None` via `__setitem__`; por causa do `or`, a segunda
chamada cria e retorna um novo estado padrão com `tela_atual: "orquestrador"`.
Assim, os comandos abrem a TUI real, mas abrem a tela raiz, não as telas
`h0029_*`.

Resultado: mecanismo do `demo.py` não aprovado como documentado.

## 12. Smoke tests

Smoke tests não visuais dos sete comandos documentados, executados em modo pipe
com entrada `s\n`, sem homologação visual:

| Comando alvo | código | alvo apareceu no stdout | raiz renderizada |
|---|---:|---|---|
| `h0029_dashboard_igual` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_dashboard_fracao` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_dashboard_percentual` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_grupo_pai_distribuido` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_grupo_igual` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_grupo_fracao` | 0 | não | sim, `ORQUESTRADOR` |
| `h0029_grupo_percentual` | 0 | não | sim, `ORQUESTRADOR` |

Também foi confirmada, por auditoria direta de loader/modelo/renderer, que os
sete JSONs existem, carregam, constroem modelo e renderizam sem erro imediato.
O defeito está no comando documentado para seleção inicial da tela pelo
`demo.py`.

## 13. Suíte canônica

Suíte executada diretamente a partir de `scripts/`, sem `pytest`:

| Script | Resultado | Código de saída |
|---|---:|---:|
| `python tela/teste_loader.py` | 172/172 | 0 |
| `python tela/teste_modelo.py` | 88/88 | 0 |
| `python tela/teste_renderizador.py` | 820/820 | 0 |
| `python tela/teste_demo.py` | 303/303 | 0 |
| `python tela/teste_diagnostico.py` | 28/28 | 0 |
| `python tela/teste_explorar_barra_de_menus.py` | 38/38 | 0 |
| **Total** | **1449/1449** | **0** |

## 14. Validação manual TTY

Não foi executada validação visual humana. A validação manual continua pendente:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Como há achado funcional no mecanismo documentado dos comandos, a classificação
final não pode ser `I5_MANUAL_VALIDATION_REQUIRED` neste estado.

## 15. Achados

```yaml
- id: QA-POS-H0029-001
  severidade: alto
  arquivo: scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
  local: "seção 15.8, comandos python3 -c das sete telas"
  regra_ou_criterio: "O comando deve abrir a TUI real na tela h0029_* indicada, usando o pipeline real do demo.py."
  evidencia: "Smoke em modo pipe com entrada 's\\n' retornou código 0, mas stdout não continha o identificador/título da tela alvo e iniciou com '╭ ORQUESTRADOR'. A expressão documentada usa lambda: (_o().__setitem__('tela_atual','<id>') or _o()), chamando _o() duas vezes e retornando o segundo estado padrão."
  problema: "Os comandos documentados não selecionam as sete telas permanentes; abrem a tela raiz orquestrador."
  impacto: "O usuário não recebe mecanismo real e repetível, como documentado, para validação manual das sete telas H-0029 pela TUI real."
  correcao_necessaria: "Corrigir a construção do estado inicial nos sete comandos ou documentar mecanismo equivalente que retorne o mesmo dict modificado, sem editar JSONs e sem integrar as telas ao lançador."

- id: QA-POS-H0029-002
  severidade: observação
  arquivo: scripts/tela/__pycache__/
  local: "estado Git após execução da suíte de QA"
  regra_ou_criterio: "Registrar caches, .pyc ou temporários sem limpar o estado durante o QA."
  evidencia: "Após a execução dos testes, git status passou a listar scripts/tela/__pycache__/ como não rastreado."
  problema: "Arquivos .pyc foram gerados pela execução/importação Python durante a auditoria."
  impacto: "Ruído no estado Git; não altera código, JSON, contratos ou relatórios históricos."
  correcao_necessaria: "Limpeza deve ser decidida em etapa autorizada posterior; esta auditoria não removeu os caches."
```

Não há achados bloqueantes. Não há achados médios ou baixos.

## 16. Classificação final

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

Justificativa: os sete JSONs, a geometria, a preservação dos JSONs de
referência, a correção acumulada do renderer e a suíte canônica estão aprovados.
Entretanto, os sete comandos documentados para abrir as telas pelo `demo.py` não
abrem as telas alvo, o que impede aprovar o mecanismo real e repetível exigido
para a validação manual em TTY.

## 17. Próxima categoria permitida

```text
PATCH_IMPLEMENTACAO
```

Não gerar prompt da próxima etapa neste relatório.

---

```yaml
status_literal: QA_POS_PATCH_COMPLETED
status_normalizado: I2_IMPLEMENTATION_PATCH_REQUIRED
relatorio: scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md
handoff_auditado: scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
relatorio_implementacao_auditado: scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
sete_jsons_aprovados: true
jsons_referencia_preservados: true
testes_nominais: "TestTelasPermanentesH0029: 256/256; teste_renderizador.py: 820/820"
mecanismo_demo: reprovado_por_comandos_documentados_nao_selecionarem_telas_h0029
smoke_tests: "sete comandos retornam 0, mas renderizam ORQUESTRADOR em vez da tela alvo"
achados_bloqueantes: 0
achados_altos: 1
achados_medios: 0
achados_baixos: 0
observacoes: 1
suite_canonica: "1449/1449"
codigo_saida: 0
git: "diff rastreado somente em scripts/tela/renderizador.py e scripts/tela/teste_renderizador.py; sete JSONs h0029_* não rastreados; documentos do ciclo não rastreados; __pycache__ observado após QA"
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
proxima_categoria: PATCH_IMPLEMENTACAO
arquivos_alterados:
  - scripts/docs/relatorios/RELATORIO_QA_POS_PATCH_H-0029_TELAS_PERMANENTES.md
```
