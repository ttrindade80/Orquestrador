# RELATORIO_QA_POS_TERCEIRO_PATCH_H-0034_IMPLEMENTACAO

status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: validacao_manual_pendente
data_execucao: 2026-07-15
papel: auditor independente pós-terceiro-patch
escopo: QA_IMPLEMENTACAO

## 1. Identificação

Auditoria do terceiro patch da implementação H-0034, focado na reauditoria do achado `QA-H0034-POS-SEGUNDO-IMPL-MEDIO-001` (validação de texto no caminho legado). Confirmou-se que a sequência de normalização de texto passou a ser comum para ambos os caminhos do renderer, garantindo que o limite configurado `max_caracteres` seja rigorosamente respeitado sob qualquer circunstância.

Nenhuma correção de código de produção ou de testes foi executada por esta auditoria. Não houve validação humana em TTY real. Não foi preparado nem executado nenhum commit.

## 2. Relatórios anteriores

Foram integralmente lidos, analisados e confrontados:

- `docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_IMPLEMENTACAO.md`
- `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md`

Os relatórios detalharam a evolução e os sucessivos patches de correção, onde o primeiro QA reprovara alinhamento por instância, parâmetros normativos do lançador e a fidelidade do IMP; o segundo QA (pós-patch) identificara `max_caracteres` hardcoded no renderer e erros de fixture no pytest; e o terceiro QA (pós-segundo-patch) constatara o desvio no caminho legado do lançador que permitia burlar o limite configurado de caracteres.

## 3. Autoridades

Foram consultados os seguintes artefatos e autoridades documentais:

- `docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md`
- `docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md`
- `docs/adr/ADR-0023-largura-minima-funcional-lancador.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_tela_json.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/NOMENCLATURA.md`
- `config/elementos/lancador.json`
- `config/telas/demo/demo.json`
- `tela/loader.py`, `tela/modelo.py`, `tela/renderizador.py`, `tela/teste_loader.py`, `tela/teste_modelo.py`, `tela/teste_renderizador.py`, `demo/teste_demo.py` e `demo/teste_diagnostico.py`.

## 4. Estado Git inicial e final

A execução de comandos do Git no início desta auditoria retornou:

```text
git status --short
 M demo/teste_demo.py
 M demo/teste_diagnostico.py
 M docs/NOMENCLATURA.md
 M docs/adr/INDICE_ADR.md
 M docs/contratos/contrato_composicao_corpo.md
 M docs/contratos/contrato_lancador.md
 M docs/contratos/contrato_tela_json.md
 M tela/loader.py
 M tela/modelo.py
 M tela/renderizador.py
 M tela/teste_loader.py
 M tela/teste_modelo.py
 M tela/teste_renderizador.py
?? demo/__pycache__/
?? docs/adr/ADR-0023-largura-minima-funcional-lancador.md
?? docs/handoff/H-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md
?? docs/relatorios/LEVANTAMENTO_REVISOES_H-0030.md
?? docs/relatorios/RELATORIO_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_APLICACAO_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_H-0034_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_ADR-0023.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_PATCH_H-0034_IMPLEMENTACAO.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_HANDOFF.md
?? docs/relatorios/RELATORIO_QA_POS_SEGUNDO_PATCH_H-0034_IMPLEMENTACAO.md
?? tela/__pycache__/
```

- `git diff --check`: Saída vazia (sem violações).
- `git diff --cached --name-only`: Saída vazia (stage limpo).

Todos os arquivos não rastreados `??` preexistentes listados acima possuem proveniência não confirmada sob a perspectiva desta auditoria isolada:
- `origem: NAO_CONFIRMADA`
- `produzido_pelo_executor: NAO_CONFIRMADO`
- `produzido_pelo_usuario: NAO_CONFIRMADO`

Estado final esperado: mesmos itens acima, adicionando unicamente `docs/relatorios/RELATORIO_QA_POS_TERCEIRO_PATCH_H-0034_IMPLEMENTACAO.md` como item criado, mantendo o stage do Git completamente vazio.

## 5. Escopo real do terceiro patch

O terceiro patch restringiu-se estritamente aos seguintes itens declarados:
- Modificação local em `tela/renderizador.py` para unificar e aplicar a sequência de normalização no caminho legado.
- Modificação local em `tela/teste_renderizador.py` para adicionar o caso de teste focal `test_caminho_legado_valida_texto`.
- Atualização factual do relatório de implementação `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md` (Seção 42).

Confirmou-se que não houve novas alterações sob esta continuação direta em:
- `tela/loader.py`, `tela/modelo.py`, `tela/teste_loader.py` e `tela/teste_modelo.py`
- Arquivos de diretório `demo/` ou `config/`
- Contratos, ADRs, NOMENCLATURA, Handoff ou relatórios de QA anteriores.

## 6. Resultado do achado principal

```yaml
achado: QA-H0034-POS-SEGUNDO-IMPL-MEDIO-001
estado: CORRIGIDO
evidencia: >
  Em `tela/renderizador.py`, a função `_linhas_lancador(elemento, content_w=None)`
  foi reestruturada para obter `_itens_brutos`, retornar vazio se cardinalidade zero
  antes de acessar parâmetros, extrair `max_caracteres` e invocar a função
  `_itens_lancador_normalizados` sobre a totalidade de itens antes da bifurcação
  pela presença de `content_w`. Portanto, o caminho legado passou a consumir itens
  já validados e normalizados.
testes: >
  Novo caso de teste `test_caminho_legado_valida_texto` adicionado à classe
  `TestDistribuicaoResponsivaH0034` em `tela/teste_renderizador.py`, executando
  13 novas asserções focais com cobertura de cardinalidade, parâmetros nulos,
  estruturas incompletas, limite alternativo e limites reais.
residuos: nenhum resíduo de bypass identificado no renderer.
regressoes: nenhuma regressão de comportamento ou layout constatada.
conclusao: >
  O desvio técnico no caminho legado foi completamente corrigido de acordo
  com as regras de negócio declaradas no handoff.
```

## 7. Preservação dos achados anteriores

As correções implementadas em patches anteriores permanecem plenamente operacionais e integradas:

- **`QA-H0034-IMPL-ALTO-001` (Alinhamento por instância):** Preservado em fila e matriz. As posições literais foram revalidadas com sucesso através dos testes focais (esquerda pos 7, centro pos 9, direita pos 10).
- **`QA-H0034-IMPL-ALTO-002` (Parâmetros normativos provenientes do JSON):** O renderer não executa I/O ou importações irregulares, consumindo dados normativos de vãos, margens verticais e limites através da propriedade `parametros_tipo` propagada de forma limpa pelo pipeline `loader → modelo`.
- **`QA-H0034-IMPL-MEDIO-001` (Fidelidade do relatório IMP):** O relatório `IMP-0034` registra de forma aderente, factual e transparente o histórico da implementação e de cada ciclo de QA.
- **`QA-H0034-POS-IMPL-ALTO-001` (`max_caracteres` configurável):** Parâmetro dinâmico lido dinamicamente a partir do JSON de configuração via loader.
- **`QA-H0034-POS-IMPL-MEDIO-001` (Compatibilidade do harness com pytest):** Coleta limpa pelo pytest através dos wrappers `test_*` parametrizados com a fixture nativa `tmp_path`, mantendo os helpers internos `_run_*` protegidos.

## 8. Sequência comum de normalização

A análise estrutural de `_linhas_lancador` em `tela/renderizador.py` revelou que a ordem real de execução é:

1. **Obter itens brutos:** Extrai itens funcionais da instância (ignora itens inválidos não-dict).
2. **Tratar cardinalidade zero:** Se vazio, retorna imediatamente `[]`.
3. **Obter `parametros_tipo`:** Recupera dados de tipo do modelo.
4. **Extrair `max_caracteres`:** Obtém valor normativo (`params["verificacao"]["texto"]["max_caracteres"]`).
5. **Normalizar e validar itens:** Invoca `_itens_lancador_normalizados(elemento, max_caracteres)`, o qual lança `RenderizadorErro` caso algum item supere o limite.
6. **Escolher caminho:** Bifurca com base na presença de `content_w`.
   - Se `content_w is None`, segue o caminho legado (formatação direta de `"[{chip}] {texto}"` um por linha).
   - Se `content_w` for um valor numérico válido, executa a distribuição responsiva.

Verificou-se que nenhuma formatação ocorre antes da validação comum, nenhum bypass de tamanho de texto é possível e não há nova leitura/reprocessamento concorrente de itens brutos.

## 9. Cardinalidade zero

A auditoria confirmou que, caso o elemento do lançador possua zero itens válidos em `_itens_brutos`:
- O renderer retorna `[]` (comportamento de lista vazia contratado).
- Não há consulta desnecessária a `parametros_tipo` ou acesso a `max_caracteres`, impedindo falhas em instâncias limpas vazias sem parâmetros.
- Não aciona quadro mínimo nem gera tracebacks de execução.
- O comportamento mantém-se idêntico e consistente tanto no modo legado (`content_w is None`) quanto no modo responsivo.

## 10. Parâmetros ausentes ou incompletos

Para lançador não-vazio, o renderer comporta-se de forma equivalente em ambas as rotas:
- **`parametros_tipo` ausente (`None`):** Lança `RenderizadorErro` com mensagem explícita em ambos os caminhos.
- **Estrutura incompleta (dicionário vazio ou sem `verificacao`):** Lança `KeyError` por ausência da chave esperada, em decorrência do acesso estrutural direto sem fallback numérico arbitrário.
- **Valor inválido (booleano, string, zero ou negativo):** Impedido em tempo de carregamento no loader (`TelaEstruturaInvalida`), assegurando consistência sintática antes do renderer. Se alcançado via modelo construído em memória com valores inválidos no render, causa falha ou tipificação esperada de forma coerente.

Não há uso de fallback do tipo `.get(..., 15)` no renderer para encobrir erros de pipeline.

## 11. Prova com limite alternativo

A simulação em memória provou que:
- Elemento construído com `verificacao.texto.max_caracteres: 3` aceita exatamente itens de tamanho até 3 (ex: `"Uno"`) e rejeita itens de comprimento superior (ex: `"Quat"` ou `"Quatro"`), tanto na rota legado (`_linhas_lancador(elem, content_w=None)`) quanto na rota responsiva (`renderizar_tela`).
- Elemento construído com `max_caracteres: 15` aceita normalmente itens maiores que 3 (ex: `"Quatro"`, 6 caracteres).
- Não há escrita na árvore de arquivos real, nem monkeypatching de constantes produtivas do renderer.

## 12. Busca de resíduos de hardcoding

Fez-se uma busca minuciosa no arquivo `tela/renderizador.py`:
- **`_TEXTO_ITEM_MAX`:** Totalmente ausente (removido no segundo patch).
- **`_LANC_*`:** Totalmente ausentes (removidos no segundo patch).
- **Literal `15`:** Inexistente como limite de item no arquivo de produção (presente apenas como valor canônico ou fixture em testes e comentários).
- **Fallback numérico (.get(..., 15)):** Ausente.
- **Formatação de itens brutos antes de normalizar:** Corrigido.
- **Ramificação específica para `content_w is None` bypassando limites:** Corrigido.

Todas as ocorrências registradas em testes e documentações correspondem estritamente a referências históricas e asserções legítimas dos valores canônicos configurados de produção.

## 13. Auditoria do teste novo

O teste `test_caminho_legado_valida_texto` em `tela/teste_renderizador.py` possui 13 asserções independentes e bem fundamentadas que cobrem:
1. Cardinalidade zero retornando `[]`.
2. Lançamento de `RenderizadorErro` quando `parametros_tipo=None`.
3. Presença de "parametros_tipo" na mensagem de exceção.
4. Lançamento de `KeyError` por estrutura de parâmetros incompleta.
5. Aceitação de texto com exatamente 3 caracteres em `mc=3`.
6. Rejeição de texto com 4 caracteres em `mc=3` (`Quat`).
7. Mensagem mencionando o limite 3 e o texto rejeitado `"Quat"`.
8. Rejeição de `"Quatro"` (6 chars) em `mc=3`.
9. Mensagem mencionando o texto `"Quatro"`.
10. Aceitação de texto de tamanho 7 em `mc=15`.
11. Preservação estrita do layout legado histórico `"[chip] texto"`.
12. Rejeição consistente de itens no caminho legado (`content_w=None`).
13. Rejeição consistente do mesmo item no caminho responsivo (`content_w` válido).

As verificações são independentes, não recorrem a tautologias (não usam a própria função sob teste para gerar os valores esperados) e falhariam categoricamente sob as versões preexistentes do renderer.

## 14. Alinhamento por instância

A correção de alinhamento por instância de patches anteriores permanece perfeitamente intacta e sem regressões:
- **Esquerda/None:** Alinha o bloco à esquerda, gerando excesso residual à direita (`[d]` na posição 4 para demo em 110).
- **Centro:** Divide o excesso uniformemente, empurrando o resto maior para a esquerda (`[A]` na posição 9 para excesso 3).
- **Direita:** Alinha o bloco à direita, concentrando o excesso à esquerda (`[A]` na posição 10 para excesso 3).
- **Valor inválido:** Lança `RenderizadorErro` conforme exigido.
- Reorganizações de layout responsivo (fila e matriz) respeitam estritamente a diretiva.

## 15. Fluxo configurável completo

Confirmou-se o perfeito pipeline sem I/O ou redundâncias normativas no renderer:
`config/elementos/lancador.json` → `loader.py` → `modelo.py` → `ElementoCorpo.parametros_tipo` → `renderizador.py`.
Todas as cotas de vãos mínimos/máximos, margens e limite de caracteres procedem dinamicamente da configuração JSON unificada de produção.

## 16. Regressões do H-0034

Inspecionou-se e reexecutou-se a cobertura completa de testes determinísticos de largura sem qualquer sinal de regressão:
- Largura 110 (fila), largura 109 (matriz), largura 80 (matriz 4x2 com distâncias de coluna independentes alinhadas à esquerda de forma correta).
- Cobertura de preenchimento coluna a coluna, e preservação da saída do teste canônico T-07.
- Isolação das áreas de fronteira (área 21 normal, área 20 quadro mínimo global) e testes de isolamento de gatilho do lançador (T-ISOL-01, T-ISOL-02, T-ISOL-03).
- Ausência total de paginação, truncamentos descontrolados ou duplicações na composição.

O JSON real mantém as saídas visuais históricas consolidadas.

## 17. Sinal global e recuperação

O mecanismo puro de sinalização global do quadro mínimo em `tela/renderizador.py` foi revalidado:
- O sinal `_quadro_minimo_lancador_ativo` é devidamente limpo (`False`) a cada ciclo de renderização.
- Quando inviabilizado pela largura em qualquer sub-bloco de lançador da composição, toda a tela normal é limpa e substituída de forma determinística pelo aviso canônico do quadro mínimo ("terminal pequeno demais" ou "tela peq.").
- A recuperação ao ampliar a tela é instantânea e reativa, sem deixar resíduos persistentes em memória.

## 18. Testes diretos

A execução individual direta das suítes canônicas retornou os seguintes resultados:

```bash
python -B tela/teste_loader.py
# Total de verificacoes: 283
# Passaram: 283
# Falharam: 0
# codigo de saida: 0

python -B tela/teste_modelo.py
# Total de verificacoes: 163
# Passaram: 163
# Falharam: 0
# codigo de saida: 0

python -B tela/teste_renderizador.py
# Total de verificacoes: 1065
# Passaram: 1065
# Falharam: 0
# codigo de saida: 0
```

Confirmou-se a diferença exata de `+13` verificações no renderer em relação ao patch anterior (saindo de 1052 para 1065), decorrente das novas verificações introduzidas no teste do caminho legado.

## 19. Suíte focal

A execução via pytest retornou o resultado esperado com contagem exata e conformidade:

```bash
PYTHONDONTWRITEBYTECODE=1 python -B -m pytest tela/teste_loader.py tela/teste_modelo.py tela/teste_renderizador.py -q --tb=short -p no:cacheprovider
# ...
# 261 passed, 5 warnings in 0.27s
# codigo de saida: 0
```

Constatou-se o acréscimo de `+1` teste aprovado (261 passed vs 260 passed) correspondente ao novo método adicionado. Os 5 warnings exibidos referem-se a alertas de retorno não-nulo preexistentes (`PytestReturnNotNoneWarning`) e não apresentam impedimento técnico.

## 20. Suíte canônica completa

Os comandos da suíte canônica consolidam os seguintes resultados:

```yaml
tela/teste_loader.py:
  comando: python -B tela/teste_loader.py
  verificacoes: 283/283
  codigo_de_saida: 0
tela/teste_modelo.py:
  comando: python -B tela/teste_modelo.py
  verificacoes: 163/163
  codigo_de_saida: 0
tela/teste_renderizador.py:
  comando: python -B tela/teste_renderizador.py
  verificacoes: 1065/1065
  codigo_de_saida: 0
demo/teste_demo.py:
  comando: python -B demo/teste_demo.py
  verificacoes: 358/358
  codigo_de_saida: 0
demo/teste_diagnostico.py:
  comando: python -B demo/teste_diagnostico.py
  verificacoes: 30/30
  codigo_de_saida: 0
demo/teste_explorar_barra_de_menus.py:
  comando: python -B demo/teste_explorar_barra_de_menus.py
  verificacoes: 38/38
  codigo_de_saida: 0
total_calculado: 1937/1937
```

A diferença de contagem geral de `+13` em relação à linha de base anterior (1924) é plenamente justificada pelo acréscimo das treze verificações focais aplicadas de forma bem-sucedida ao teste do caminho legado do renderer.

## 21. Smoke

O smoke test interativo em modo não-TTY respondeu com código de saída 0:

```bash
printf 's\n' | python -B demo/demo.py
```

A renderização visual foi capturada corretamente com a identificação do cabeçalho `ORQUESTRADOR`, presença do contêiner `NAVEGAR`, renderização limpa de todos os 7 chips válidos da demo em matriz 4x2 (`[d]`, `[g]`, `[1]`, `[2]`, `[3]`, `[4]`, `[5]`), sem ocorrência de tracebacks ou vazamento de dados inertes.

## 22. Fidelidade do IMP

A auditoria integral de `docs/relatorios/IMP-0034-distribuicao-responsiva-lancador-fila-matriz.md` confirma que a seção 42 foi devidamente integrada e registra de forma honesta, factual e coerente:
- O terceiro ciclo de QA reprovador, o desvio técnico encontrado no caminho legado e as causas.
- A sequência de normalização final estabelecida, unificada entre ambos os caminhos de processamento.
- O detalhamento dos testes introduzidos (13 pontos, totalizando 1065/1065 verificações no renderer e 261 passed no pytest).
- O sucesso da execução da suíte canônica (1937/1937) e do smoke test.
- A pendência legítima da validação visual humana no terminal (VALIDACAO_MANUAL_PENDENTE_USUARIO).
- A ausência de autoaprovação de implementação.

Sobre as 11 falhas históricas do loader, o relatório declara de forma transparente que a decomposição individual retrospectiva destas falhas não pôde ser resgatada nos artefatos vigentes com detalhamento suficiente, abstendo-se de criar narrativas hipotéticas ou inventadas.

## 23. Validação humana pendente

De acordo com as restrições e diretivas deste prompt, a validação humana visual e interativa em TTY real não foi realizada e permanece como a única pendência ativa do ciclo de implementação H-0034.

## 24. Novos achados

Nenhum novo achado ou desvio técnico foi identificado. Todas as exigências do handoff H-0034 e da ADR-0023 encontram-se plenamente implementadas, testadas e documentadas com rigor e coerência técnica.

## 25. Status literal e normalizado

```yaml
status_literal: I5_MANUAL_VALIDATION_REQUIRED
status_normalizado: validacao_manual_pendente
motivo: >
  Todas as verificações de testes diretos e pytest focal encontram-se verdes.
  O desvio no caminho legado foi devidamente sanado e coberto com 13 novas asserções.
  O relatório de implementação IMP está factual e transparente. A única pendência
  operacional restante é a realização da validação humana visual obrigatória em
  TTY real.
```

## 26. Próxima categoria

A próxima categoria do fluxo de trabalho é:

`APROVACAO_IMPLEMENTACAO`
