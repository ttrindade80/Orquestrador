# QA da implementação H-0029

## 1. Identificação

| Campo | Valor |
|---|---|
| Ciclo | H-0029 |
| Título | Distribuição de containers com cardinalidade unitária |
| Tipo desta etapa | QA_IMPLEMENTACAO |
| Auditor | Codex |
| Raiz Git observada | `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1` |
| Handoff auditado | `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md` |
| Relatório de implementação auditado | `scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md` |
| Status literal recebido | `IMPLEMENTED_PENDING_QA` |
| Status normalizado recebido | `IMPLEMENTATION_COMPLETED` |
| Validação manual declarada | `VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO` |

Esta auditoria não alterou código, testes, JSONs, handoff, ADRs, contratos ou documentação normativa. A única escrita realizada foi este relatório.

## 2. Arquivos e autoridades consultadas

Leitura integral obrigatória realizada:

- `scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md`;
- `scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md`;
- `scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md`.

Autoridades ativas consultadas nos pontos necessários:

- `scripts/docs/contratos/contrato_composicao_corpo.md`: regras de grupo estrutural sem moldura, distribuição por container, ausência de distribuição, modos, área alocada e preenchimento;
- `scripts/docs/adr/ADR-0015-composicao-hierarquica-distribuicao-corpo.md`: composição hierárquica, distribuição por container, contato entre molduras e preenchimento de área alocada;
- `scripts/docs/adr/ADR-0018-semantica-ausencia-distribuicao-alocacao-vertical.md`: ausência não equivale a `igual`, distribuição explícita aloca área e sobra vira preenchimento interno das molduras dos elementos;
- `scripts/docs/adr/ADR-0019-profundidade-grupos-multiplicidade-cardinalidade-dashboard.md`: profundidade e multiplicidade em grupos;
- `scripts/docs/adr/ADR-0020-matriz-de-grupos-coordenadas-explicitas.md`: preservação de `estrutura: livre`, independência de matriz e ausência de distribuição.

Diff real inspecionado:

- `scripts/tela/renderizador.py`;
- `scripts/tela/teste_renderizador.py`.

## 3. Estado Git e escopo observado

Conferência inicial obrigatória:

```text
git rev-parse --show-toplevel
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1
```

```text
git status --short
 M scripts/tela/renderizador.py
 M scripts/tela/teste_renderizador.py
?? scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
?? scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
?? scripts/docs/relatorios/RELATORIO_LEVANTAMENTO_OCUPACAO_CORPO_STUB_B_DESTINO_MINIMO.md
?? scripts/docs/relatorios/RELATORIO_QA_HANDOFF_H-0029_DISTRIBUICAO_CONTAINERS_CARDINALIDADE_UNITARIA.md
?? scripts/tela/__pycache__/
```

```text
git diff --check
sem saída; código de saída 0
```

Arquivos modificados esperados pelo H-0029:

- `scripts/tela/renderizador.py`;
- `scripts/tela/teste_renderizador.py`.

Arquivos não rastreados esperados no fluxo documental do ciclo:

- handoff H-0029;
- relatório de levantamento;
- relatório de QA do handoff;
- relatório de implementação.

Arquivo inesperado observado:

- `scripts/tela/__pycache__/`, contendo `loader.cpython-314.pyc`, `renderizador.cpython-314.pyc`, `__init__.cpython-314.pyc` e `modelo.cpython-314.pyc`.

Na conferência pré-relatório não havia diff em `scripts/config/telas/*.json`, `scripts/docs/adr/`, `scripts/docs/contratos/`, `scripts/tela/loader.py`, `scripts/tela/modelo.py`, `scripts/tela/demo.py`, `scripts/tela/diagnostico.py` ou `scripts/tela/explorar_barra_de_menus.py`.

Na conferência final, após a criação deste relatório, o estado Git passou a incluir também:

```text
 M scripts/config/telas/destino_minimo.json
```

O diff final observado em `scripts/config/telas/destino_minimo.json` adiciona:

```json
"distribuicao": {
  "modo": "igual"
}
```

Essa alteração é fora do escopo do H-0029 e contraria a preservação exigida para JSONs reais.

## 4. Comparação com o handoff aprovado

A implementação em `renderizador.py` respeita o escopo positivo do handoff: corrige o caminho vertical de distribuição explícita em container com filho `grupo`, preserva ausência de distribuição no código, cobre cardinalidade unitária nos modos `igual`, `fracao [1]` e `percentual [100]`, preserva cardinalidade maior que 1, preserva independência entre níveis e mantém testes focais.

O escopo negativo não está integralmente preservado no estado Git final: `scripts/config/telas/destino_minimo.json` aparece modificado e esse arquivo é proibido pelo handoff. Não foram observadas novas telas permanentes, alterações em contratos, ADRs, nomenclatura, handoff, loader, modelo, demo, diagnóstico ou funcionalidades futuras de console, navegação, seleção ou execução de ações.

Os arquivos alterados estão dentro da lista autorizada para implementação. O relatório de implementação existe no caminho esperado.

## 5. Causa técnica

A causa técnica declarada está confirmada pelo diff e pelo código.

No caminho de distribuição vertical, `_renderizar_container_vertical` calcula pesos por `_pesos_distribuicao`, cotas por `_distribuir_alturas` e passa a cota do filho `grupo` para `_renderizar_container`. Antes do patch, quando esse grupo não tinha distribuição própria, `_renderizar_container` devolvia somente a altura natural dos filhos internos e o bloco era anexado diretamente.

Como `renderizar_tela` marca o corpo como verticalmente distribuído quando `corpo.distribuicao` existe e `altura` foi fornecida, o preenchimento externo do corpo não é inserido. O resultado anterior, portanto, podia ter menos linhas que a altura solicitada.

Não foi encontrado default implícito para `igual`, nem condição especial baseada em `len(elementos) == 1`. A cardinalidade unitária expõe o defeito, mas a causa real é a diferença entre elemento funcional, que recebe `altura_alvo=cota` em `_caixa_de_elemento`, e grupo estrutural, que antes não tinha seu bloco completado até a cota recebida do pai.

## 6. Análise da correção

Diff relevante em `scripts/tela/renderizador.py`:

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

A correção completa o bloco de um filho `grupo` até a cota atribuída pelo pai no caminho vertical distribuído. Isso preserva a soma exata das cotas e impede que o corpo distribuído deixe de ocupar `l_corpo_disponivel`.

Ponto crítico: `grupo` não tem borda nem moldura visual própria segundo o contrato ativo. Portanto, nos casos em que o grupo recebe cota mas não declara distribuição interna, as linhas acrescentadas não são linhas depois de uma caixa de grupo fechada, pois tal caixa não existe. Elas representam área estrutural do grupo depois dos filhos naturais. Nos casos em que o grupo declara distribuição interna, a moldura do elemento funcional interno cresce até a cota, como exigido pela semântica de área alocada.

## 7. Geometria, preenchimento e bordas

Foram renderizados casos focais com `largura=42` e `altura=20`. Nessa geometria:

- cabeçalho ocupa linhas 0-2;
- `l_corpo_disponivel = 14`, linhas 3-16;
- `barra_de_menus` ocupa linhas 17-19.

Caso M05, `corpo.distribuicao = igual`, filho direto é um grupo sem distribuição, com um dashboard:

```text
00 topo cabecalho
02 base cabecalho
03 topo D1
04 base D1
05-16 linhas de espaço da área estrutural do grupo
17 topo Menus
19 base Menus
```

Esse caso comprova que o grupo ocupa a cota de 14 linhas recebida do corpo, mas o filho interno permanece natural, conforme a matriz do handoff para grupo sem distribuição própria.

Caso M10, `corpo.distribuicao = igual` e `grupo.distribuicao = igual`, com um dashboard:

```text
00 topo cabecalho
02 base cabecalho
03 topo D1
04-15 preenchimento interno bordeado do dashboard
16 base D1
17 topo Menus
19 base Menus
```

Esse caso comprova que, quando o grupo também distribui internamente, a borda inferior do elemento funcional fica exatamente no fim da cota do corpo, imediatamente antes da `barra_de_menus`. Não há lacuna externa, sobreposição ou deslocamento da barra.

As linhas não vazias mantêm largura 42. A altura total é 20. A soma das cotas é 14. A posição da barra é 17 nos casos focais.

## 8. Cardinalidade unitária e independência entre níveis

Comportamentos confirmados:

- `igual` com um filho atribui 100% da área distribuível;
- `fracao` com `[1]` atribui 100%;
- `percentual` com `[100]` atribui 100%;
- os três modos são geometricamente equivalentes em cardinalidade unitária;
- um grupo único pode receber toda a cota do corpo;
- um único filho pode receber toda a área interna de um grupo distribuído;
- corpo e grupo distribuídos funcionam em conjunto;
- distribuição em descendente não expande ancestral sem distribuição;
- ausência de distribuição preserva altura natural e preenchimento externo histórico;
- não foi criado default implícito;
- casos com dois ou mais filhos permanecem corretos.

O caminho horizontal não foi alterado. A justificativa é objetiva: o diff toca somente `_renderizar_container_vertical`; `_renderizar_container_horizontal` já normaliza a altura das áreas quando `altura_disponivel` existe, preservando colunas por `altura_alvo` e preenchimento por coluna. Os testes horizontais existentes do H-0026 continuam passando, e o H-0029 não exige alteração artificial nesse caminho.

## 9. Auditoria dos testes adicionados

O diff em `scripts/tela/teste_renderizador.py` adiciona a classe `TestCardinalidadeUnitariaH0029`, com 20 métodos e 60 verificações declaradas.

Os 13 cenários M01-M13 correspondem à matriz mínima do handoff:

- M01 preserva ausência em funcional direto;
- M02-M04 cobrem `igual`, `fracao [1]` e `percentual [100]` em funcional direto;
- M05-M06 cobrem corpo distribuído com grupo sem distribuição;
- M07-M09 cobrem corpo sem distribuição e grupo distribuído;
- M10-M12 cobrem distribuição nos dois níveis;
- M13 preserva dois filhos.

As verificações são materialmente úteis em conjunto: incluem total de linhas, largura das linhas, posição da barra, ausência ou presença de fill externo conforme a semântica, equivalência geométrica entre modos, redimensionamento em duas alturas, área insuficiente determinística e integração com JSON real.

Limitação observada: parte das verificações usa helpers internos, como `_pesos_distribuicao` e `_distribuir_alturas`, para confirmar soma de cotas. Isso é menos independente que uma validação exclusivamente por saída renderizada. A limitação não bloqueia a aprovação automatizada porque os testes focais também verificam a saída final, e a auditoria suplementar acima confirmou índices de linhas e posição das bordas nos casos M05 e M10.

Os testes M05 e M06 falhariam sem a correção por total de linhas. Os testes M10-M12 preservam a geometria quando há distribuição nos dois níveis. Os testes não alteram JSON real e usam `grupo_minimo.json` apenas como integração loader -> modelo -> renderer.

## 10. JSONs reais e integração

Na conferência pré-relatório, `git diff --name-only` e `git status --short` não apontavam alterações em JSONs reais. Na conferência final, essa confirmação deixou de ser verdadeira:

- `scripts/config/telas/grupo_minimo.json` não foi alterado;
- `scripts/config/telas/destino_minimo.json` está alterado;
- `scripts/config/telas/stub_b.json` não foi alterado;
- `scripts/config/telas/orquestrador.json` não foi alterado.

O estado atual de `destino_minimo.json` adiciona `corpo.distribuicao: {"modo": "igual"}`. Isso viola a exigência de preservar esse JSON e faz falhar verificações que confirmavam `modelo.corpo.distribuicao is None` para `destino_minimo`.

A integração com `grupo_minimo.json` exercita loader -> modelo -> renderer sem mascarar o defeito por alteração declarativa. `stub_b.json` permanece sem distribuição.

## 11. Suíte canônica

Execução realizada a partir de `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`, por chamada direta dos seis scripts:

| Comando | Verificações | Falhas | Código de saída |
|---|---:|---:|---:|
| `python tela/teste_loader.py` | 172/172 | 0 | 0 |
| `python tela/teste_modelo.py` | 88/88 | 0 | 0 |
| `python tela/teste_renderizador.py` | 564/564 | 0 | 0 |
| `python tela/teste_demo.py` | 303/303 | 0 | 0 |
| `python tela/teste_diagnostico.py` | 28/28 | 0 | 0 |
| `python tela/teste_explorar_barra_de_menus.py` | 38/38 | 0 | 0 |
| **Total** | **1193/1193** | **0** | **0** |

A soma inicial observada coincidiu com o total declarado.

Após a alteração final detectada em `scripts/config/telas/destino_minimo.json`, `python tela/teste_renderizador.py` foi reexecutado e falhou:

| Comando reexecutado no estado final | Verificações | Falhas | Código de saída |
|---|---:|---:|---:|
| `python tela/teste_renderizador.py` | 562/564 | 2 | 1 |

Falhas finais:

- `destino_minimo: sem distribuicao (distribuicao is None)`;
- `H-0029 preserv: destino_minimo distribuicao is None`.

Portanto, a suíte canônica completa não pode ser considerada verde no estado final do repositório.

## 12. Validação automatizada, pseudo-TTY e TTY real

Validação automatizada:

- suíte canônica passou integralmente;
- testes H-0029 passaram integralmente;
- índices de linhas e bordas foram conferidos por renderização controlada.

Pseudo-TTY:

- a suíte `teste_demo.py` contém validação pseudo-TTY histórica de redimensionamento e passou;
- não foi executada validação pseudo-TTY específica adicional para H-0029, pois a geometria auditada é determinística por `renderizar_tela(..., largura, altura)`.

TTY real humano:

```text
VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO
```

Esta auditoria não declara aprovação visual humana.

## 13. Achados

```yaml
id: ACH-I-001
severidade: observação
arquivo: scripts/tela/__pycache__/
local: estado Git
regra_ou_criterio: escopo Git do QA_IMPLEMENTACAO
evidencia: git status --short lista "?? scripts/tela/__pycache__/"
problema: há cache Python não rastreado fora da lista acumulada documental do H-0029.
impacto: não altera comportamento, testes, JSONs ou documentação normativa; deve ser classificado antes de fechamento/commit.
correcao_necessaria: nenhuma nesta etapa de QA; não limpar durante a auditoria.
```

```yaml
id: ACH-I-002
severidade: observação
arquivo: scripts/tela/teste_renderizador.py
local: TestCardinalidadeUnitariaH0029.test_soma_cotas_exata
regra_ou_criterio: auditoria de testes independentes e materialmente úteis
evidencia: o teste chama _pesos_distribuicao e _distribuir_alturas diretamente para confirmar soma de cotas.
problema: essa parte da cobertura é menos independente que testes baseados apenas na saída renderizada.
impacto: baixo risco residual, mitigado pelos testes de renderização final e pela conferência objetiva de linhas M05/M10 nesta auditoria.
correcao_necessaria: nenhuma obrigatória para aprovação; registrar a limitação.
```

```yaml
id: ACH-I-003
severidade: bloqueante
arquivo: scripts/config/telas/destino_minimo.json
local: corpo.distribuicao
regra_ou_criterio: handoff H-0029, escopo negativo e seção de JSONs reais
evidencia: git diff final adiciona corpo.distribuicao {"modo": "igual"}; teste_renderizador.py reexecutado no estado final retorna 562/564, código 1.
problema: arquivo JSON real proibido foi alterado e a preservação de ausência de distribuição em destino_minimo deixou de ser verdadeira.
impacto: a implementação não pode ser aprovada no estado Git final; a suíte canônica não permanece verde e a auditoria não pode confirmar JSONs reais preservados.
correcao_necessaria: patch de implementação/escopo para remover ou resolver a alteração fora do handoff antes de nova QA; esta auditoria não corrige o arquivo.
```

Não há achados altos, médios ou baixos de implementação. Há um achado bloqueante de escopo/estado Git e duas observações.

## 14. Classificação final

```text
I2_IMPLEMENTATION_PATCH_REQUIRED
```

Justificativa: a causa técnica do código está confirmada e a correção em `renderizador.py` é compatível com a semântica auditada, mas o estado Git final contém alteração proibida em `scripts/config/telas/destino_minimo.json`. Essa alteração quebra a preservação exigida dos JSONs reais e faz `teste_renderizador.py` falhar no estado final.

## 15. Próxima categoria permitida

```text
PATCH_IMPLEMENTACAO
```

Resumo de saída:

```text
status_literal: I2_IMPLEMENTATION_PATCH_REQUIRED
status_normalizado: IMPLEMENTATION_PATCH_REQUIRED
relatorio: scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
handoff_auditado: scripts/docs/handoff/H-0029-distribuicao-containers-cardinalidade-unitaria.md
relatorio_implementacao_auditado: scripts/docs/relatorios/RELATORIO_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
causa_tecnica_confirmada: sim
achados_bloqueantes: 1
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 2
testes: suite_canonica_inicial_1193/1193; estado_final_teste_renderizador_562/564_codigo_1
git: destino_minimo.json_modificado_fora_do_escopo; pycache_nao_rastreado_observado
validacao_manual: VALIDACAO_MANUAL_TTY_PENDENTE_USUARIO_nao_alcancada_por_bloqueio_de_patch
proxima_categoria: PATCH_IMPLEMENTACAO
arquivos_alterados: scripts/docs/relatorios/RELATORIO_QA_IMPLEMENTACAO_H-0029_DISTRIBUICAO_CARDINALIDADE_UNITARIA.md
```
