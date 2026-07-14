# Levantamento - H-0012 pos-auditoria

## Status

LEVANTAMENTO_CONCLUIDO

## Escopo

Este relatorio apenas extrai evidencias. Nao implementa codigo e nao altera handoff, contratos ou ADRs.

## Estado inicial do Git

Comandos obrigatorios executados a partir de `/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts`.

```bash
$ git status --short
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
```

```bash
$ git log --oneline -5
6c91279 docs: cancela H-0011 e remove H-0011A
a940fbc docs: fecha base documental de composicao hierarquica
f41bd2f docs: registra validacao declarativa com stub b
36c55d2 feat: implementa fluxo minimo do lancador com tela destino
ec0a59e docs: fecha contratos incrementais de tela json
```

```bash
$ pwd
/home/tiago/Dropbox/UFRGS/Survey/versao_0_1/scripts
```

```bash
$ find . -path '*H-0012*' -o -path '*RELATORIO_AUDITORIA_H-0012*'
./docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
./docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
```

Estado inicial observado: o handoff H-0012 e o relatorio de auditoria estavam nao rastreados, coerente com etapa documental.

## Arquivos lidos

Todos os arquivos obrigatorios existiam e foram consultados.

- `docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md`
- `docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md`
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_json_tela_minima.md`
- `docs/contratos/contrato_json_dashboard.md`
- `config/telas/orquestrador.json`
- `config/telas/destino_minimo.json`
- `config/telas/stub_b.json`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/renderizador.py`
- `tela/diagnostico.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `tela/teste_renderizador.py`
- `tela/teste_diagnostico.py`
- `tela/teste_demo.py`

Nenhum arquivo obrigatorio foi classificado como AUSENTE.

## 1. Saida real dos testes existentes

### Evidencias em codigo

Os testes existentes imprimem cabecalhos, secoes, resumos e detalhes diagnosticos alem de linhas `[PASSOU]`.

- `tela/teste_loader.py`: linhas 483-485 imprimem cabecalho diagnostico, base e Python; 134, 199, 294, 444, 469 e 502 imprimem secoes; 506-508 imprimem `Total de verificacoes`, `Passaram` e `Falharam`; 518-526 imprimem representacao interna carregada.
- `tela/teste_modelo.py`: linhas 346-348 imprimem cabecalho diagnostico, base e Python; 82, 176, 287 e 354 imprimem secoes; 358-360 imprimem resumo; 370-371 imprimem diagnostico do modelo.
- `tela/teste_renderizador.py`: linhas 869-871 imprimem cabecalho diagnostico, base e Python; 149, 282, 351, 412, 426, 510, 552, 610, 654, 804 e 884 imprimem secoes; 888-890 imprimem resumo.
- `tela/teste_diagnostico.py`: linhas 317-319 imprimem cabecalho diagnostico, base e Python; 96, 126, 239, 272 e 300 imprimem secoes; 304-306 imprimem resumo.
- `tela/teste_demo.py`: linhas 986-988 imprimem cabecalho diagnostico, base e Python; 236, 272, 379, 494, 591, 687, 717, 840, 894, 928 e 969 imprimem secoes; 973-975 imprimem resumo.

### Execucao dos testes

```text
python tela/teste_loader.py
- exit code: 0
- apareceu [FALHOU]: nao
- exemplos de linhas nao-[PASSOU]:
  - Diagnostico H-0001 - loader/validador de tela.json
  - == Carregamento do arquivo real config/telas/orquestrador.json ==
  - -- Declaracao inerte preservada (DOC-B008 / DOC-B009) --
  - == Resumo ==
  - Total de verificacoes: 42
  - Passaram: 42
  - Falharam: 0
  - == Representacao interna carregada (resumo) ==
- conclusao: sucesso real e medido por exit code 0, ausencia de [FALHOU] e ausencia de traceback; a saida nao e composta apenas por linhas [PASSOU].
```

```text
python tela/teste_modelo.py
- exit code: 0
- apareceu [FALHOU]: nao
- exemplos de linhas nao-[PASSOU]:
  - Diagnostico H-0002 - modelo interno normalizado de tela
  - == Construcao do modelo para config/telas/orquestrador.json ==
  - -- Declaracao inerte preservada (DOC-B008 / DOC-B009) --
  - == Resumo ==
  - Total de verificacoes: 34
  - Passaram: 34
  - Falharam: 0
  - == Diagnostico do modelo ==
- conclusao: sucesso real e medido por exit code 0, ausencia de [FALHOU] e ausencia de traceback; a saida nao e composta apenas por linhas [PASSOU].
```

```text
python tela/teste_renderizador.py
- exit code: 0
- apareceu [FALHOU]: nao
- exemplos de linhas nao-[PASSOU]:
  - Diagnostico H-0010A - renderer declarativo (curva/reta)
  - == Renderer sobre modelo de config/telas/orquestrador.json ==
  - -- Rejeicao de item de lancador com texto > 15 chars (H-0010A) --
  - == Resumo ==
  - Total de verificacoes: 102
  - Passaram: 102
  - Falharam: 0
- conclusao: sucesso real e medido por exit code 0, ausencia de [FALHOU] e ausencia de traceback; a saida nao e composta apenas por linhas [PASSOU].
```

```text
python tela/teste_diagnostico.py
- exit code: 0
- apareceu [FALHOU]: nao
- exemplos de linhas nao-[PASSOU]:
  - Diagnostico H-0004 - ponto de entrada executavel da tela raiz
  - == Invariantes dos ciclos anteriores (subprocess) ==
  - == gerar_diagnostico_tela sobre orquestrador.json ==
  - == Resumo ==
  - Total de verificacoes: 28
  - Passaram: 28
  - Falharam: 0
- conclusao: sucesso real e medido por exit code 0, ausencia de [FALHOU] e ausencia de traceback; a saida nao e composta apenas por linhas [PASSOU].
```

```text
python tela/teste_demo.py
- exit code: 0
- apareceu [FALHOU]: nao
- exemplos de linhas nao-[PASSOU]:
  - Diagnostico H-0010A - aplicacao demonstravel com borda/sair/navegacao
  - == Secao 1 - Estado inicial ==
  - == Secao 2 - processar_comando ==
  - == Resumo ==
  - Total de verificacoes: 95
  - Passaram: 95
  - Falharam: 0
- conclusao: sucesso real e medido por exit code 0, ausencia de [FALHOU] e ausencia de traceback; a saida nao e composta apenas por linhas [PASSOU].
```

### Recomendacao documental

Substituir no H-0012 a regra:

```text
Todos devem encerrar com codigo de saida 0 e imprimir apenas linhas [PASSOU].
```

por:

```text
Todos devem encerrar com codigo de saida 0, nao imprimir linhas [FALHOU] e nao produzir traceback; cabecalhos, secoes, resumos e detalhes diagnosticos existentes sao permitidos.
```

Nao alterar os testes para satisfazer a redacao antiga. A redacao antiga contradiz o comportamento real e validado dos testes existentes.

## 2. Grupo em corpo.elementos[]

### Evidencias documentais

- `docs/contratos/contrato_json_tela_minima.md`, secao 6: `corpo.elementos[]` aceita apenas `console`, `dashboard` e `lancador`; tipo desconhecido e erro de validacao.
- `docs/contratos/contrato_tela_json.md`, secao `corpo`: a taxonomia atual do corpo e `console`, `dashboard`, `lancador`; extensoes futuras exigem ADR. A mesma secao registra que, por ADR-0010, `elementos[]` pode evoluir para agrupamentos e composicao hierarquica preservando compatibilidade com lista plana.
- `docs/adr/ADR-0010-composicao-hierarquica-corpo-dashboard.md`: declara que `console`, `lancador` e `dashboard` sao os elementos funcionais do corpo e que a taxonomia fechada permanece inalterada; tambem declara que `corpo.elementos[]` pode evoluir para estrutura com agrupamentos e composicao hierarquica.
- `docs/contratos/contrato_composicao_corpo.md`, secao 3: a taxonomia funcional permanece fechada nos tres tipos `console`, `lancador`, `dashboard`; a secao 4 ainda descreve `tipo (console | lancador | dashboard)` para cada elemento.
- O H-0012 ja contem uma boa formulacao em `Definicao de grupo estrutural`: "`grupo` e um container estrutural - nao e elemento funcional do corpo"; tambem separa tipos funcionais (`console`, `lancador`, `dashboard`) do tipo estrutural.

### Interpretacao recomendada

`grupo` deve ser descrito como container estrutural de composicao, nao como elemento funcional do corpo. Os tipos funcionais permanecem exatamente `console`, `dashboard` e `lancador`.

H-0012 pode definir suporte minimo ao grupo como container estrutural limitado, rastreado pela ADR-0010, desde que o handoff deixe isso explicito em todos os pontos onde falar de `tipo = "grupo"` em `corpo.elementos[]`.

### Precisa alterar contrato agora?

Nao ha necessidade de alterar contrato nesta tarefa. A recomendacao e resolver no proprio H-0012 por regra limitada e rastreada na ADR-0010, sem ampliar a taxonomia funcional.

O cuidado documental e evitar frasear `grupo` como quarto tipo funcional. Quando necessario, usar termos como:

```text
tipo estrutural permitido no H-0012, separado da taxonomia funcional fechada.
```

## 3. Dashboard campos[] versus conteudo

### Evidencias em JSON/codigo

- `config/telas/orquestrador.json` usa `dashboard_info.campos[]` e tambem mantem `posicao_dashboard` transicional.
- `config/telas/destino_minimo.json` usa `dashboard_teste.campos[]` com campo literal `valor`.
- `config/telas/stub_b.json` usa `dashboard_teste.campos[]` com campo literal `valor`.
- `tela/renderizador.py` implementa `_linhas_dashboard(elemento)` lendo `elemento._campos_inertes.get("campos", [])`; campos com `fonte == "literal"` geram linhas de conteudo, campos pendentes sao ignorados sem erro.
- `tela/modelo.py` preserva todos os campos alem de `id` e `tipo` em `_campos_inertes`, incluindo `campos[]`.

### Evidencias contratuais

`docs/contratos/contrato_json_dashboard.md` descreve envelope minimo com:

```json
{
  "id": "dashboard_principal",
  "tipo": "dashboard",
  "titulo": "Resumo",
  "conteudo": {
    "tipo": "placeholder",
    "binding": null
  },
  "regras_exibicao": {
    "posicao_dashboard": "vertical"
  }
}
```

O mesmo contrato declara `conteudo` e `regras_exibicao` como campos obrigatorios do envelope minimo, enquanto os JSONs reais e o renderer atual operam com `campos[]`.

### Interpretacao recomendada para H-0012

Para o H-0012, usar o formato operacional ja validado pelo H-0010A: `dashboard.campos[]`. Esse e o formato que os JSONs reais usam e que `modelo.py`/`renderizador.py` suportam hoje.

O exemplo de `grupo_minimo.json` no H-0012 deve manter `campos[]` se a implementacao esperada e exercitar o renderer atual sem mudar contrato nem criar harmonizacao ampla.

### Harmonizacao futura

Registrar no H-0012 que a harmonizacao entre `contrato_json_dashboard.md` (`conteudo`/`regras_exibicao`) e JSONs reais (`campos[]`) fica fora de escopo, salvo se for bloqueante para a implementacao.

Nao alterar contrato nem JSON no ciclo de levantamento.

## 4. Diagnostico.py

### Evidencias

- H-0012 declara que `diagnostico.py` encadeia `carregar_tela -> construir_modelo -> renderizar_tela` para a tela raiz `orquestrador`.
- H-0012 declara que o Orquestrador nao e alterado e que o comportamento externo de `diagnostico.py` nao deve mudar.
- H-0012, F-4, linhas 521-523: se o output do diagnostico do Orquestrador mudar, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.
- H-0012 lista `tela/diagnostico.py` como proibido com excecao "se o output do Orquestrador mudar", criando ambiguidade menor: a propria F-4 manda parar se o output mudar.
- A execucao atual de `python tela/teste_diagnostico.py` retornou 0, sem `[FALHOU]`, validando que o diagnostico atual nao precisa mudar para o escopo de tela isolada.

### Recomendacao documental

Como H-0012 deve usar tela isolada e nao migrar o Orquestrador, `tela/diagnostico.py` deve permanecer proibido.

Se a implementacao exigir alterar `tela/diagnostico.py` ou alterar output do Orquestrador, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`. A excecao em `Arquivos proibidos` deve ser removida ou reformulada para nao autorizar alteracao direta.

## 5. Ajustes recomendados no H-0012

### Bloqueante

- Substituir a regra "imprimir apenas linhas `[PASSOU]`" pela regra de sucesso observavel: codigo de saida 0, nenhuma linha `[FALHOU]` e ausencia de traceback; cabecalhos, secoes, resumos e detalhes diagnosticos existentes sao permitidos.

### Limpeza recomendada

- Reforcar em todos os pontos do H-0012 que `grupo` e container estrutural, nao tipo funcional. Manter os tipos funcionais como `console`, `lancador`, `dashboard`.
- Manter `dashboard.campos[]` no exemplo e nos criterios de H-0012, registrando que esse e o formato operacional atual validado por testes.
- Ajustar a permissao de `tela/diagnostico.py`: deve ficar proibido; se o output do Orquestrador mudar, parar com `ARCHITECTURE_REVIEW_REQUIRED`.
- Orientar o executor a reconhecer os arquivos nao rastreados esperados antes de alterar. Ao final da proxima etapa, o status deve conter apenas os arquivos documentais ou de implementacao explicitamente permitidos pela etapa, salvo se a etapa pedir commit.

### Fora de escopo

- Alterar contratos para harmonizar `dashboard.campos[]` com `conteudo`/`regras_exibicao`.
- Alterar ADR-0010 ou NOMENCLATURA.
- Alterar JSONs existentes do Orquestrador, `destino_minimo` ou `stub_b`.
- Alterar testes existentes apenas para remover cabecalhos, secoes, resumos ou diagnosticos.
- Criar H-0013 ou qualquer outro handoff.
- Fazer commit.

## 6. Verificacoes finais

```bash
$ git status --short
?? docs/handoff/H-0012-grupo-estrutural-minimo-tela-isolada.md
?? docs/relatorios/LEVANTAMENTO_H-0012_POS_AUDITORIA.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0012_HANDOFF.md
```

```bash
$ git diff --stat
```

Sem saida. Observacao: `git diff --stat` nao lista arquivos untracked.

```bash
$ git diff --name-only
```

Sem saida. Observacao: `git diff --name-only` nao lista arquivos untracked.

## Resultado final

Apenas este relatorio foi criado.
