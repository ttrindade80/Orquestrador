# Relatório QA do H-0046

Objeto auditado: `docs/handoff/H-0046-modularizacao-estrutural-do-renderizador.md`, aplicação da ADR-0039 ao renderizador.

Verificações focais executadas: leitura da ADR, nomenclatura, contratos e código autorizado; AST de `tela/renderizador.py`; buscas de consumidores, símbolos, estado, imports locais e monkeypatches; conferência dos doze caminhos nominais (todos existem); `pytest --collect-only` dos caminhos nominais (736 testes coletados); `git diff --check`; execução de `demo/demo.py --help` fora de TTY; execução do trecho de demonstração nominal.

## Achados

```yaml
id: QA-H0046-01
requisito_violado: "§8 — demonstração de redimensionamento e assinaturas reais"
evidencia_focal: "O trecho nominal usa renderizar_tela(modelo, largura=80, altura=24), mas a assinatura real exige estilo; adicionando estilo, altura=24 ainda falha com RenderizadorErro (o corpo requer 21 linhas e a geometria efetiva chega a 25 em largura 80). O trecho também importa geometria_console sem invocá-la."
impacto: "A demonstração não é executável e não comprova o cálculo dimensional/autoridade declarada."
correcao_necessaria: "Atualizar o exemplo com o estilo resolvido, uma altura suficiente ou sem cota fixa, e uma chamada/asserção específica de geometria_console; preservar a comparação entre larguras."
```

```yaml
id: QA-H0046-02
requisito_violado: "§3.2–§3.3 — dependências declaradas e direção acíclica"
evidencia_focal: "O código real usa, além das dependências declaradas: RenderizadorErro em geometria_caixa, conteudo_externo, lancador, barra_menus e composicao_corpo; _quebrar_texto em matriz_participantes e paginacao_interna; _console_tem_paginacao em composicao_corpo; DESCONTO_ESTRUTURAL_CONSOLE em matriz_participantes e barra_menus; imports locais de tela.navegacao, tela.selecao, tela.paginacao e tela.modelo. Como DESCONTO_ESTRUTURAL_CONSOLE é atribuído a console.py, enquanto console.py depende de matriz_participantes.py, importar a constante de sua autoridade cria ciclo console ↔ matriz_participantes."
impacto: "A implementação não consegue seguir simultaneamente a lista de proprietários e o grafo declarado sem inventar relocação, duplicação ou dependência não documentada."
correcao_necessaria: "Revisar nominalmente proprietários e dependências, resolver a autoridade compartilhada do desconto estrutural e registrar todas as dependências externas antes da implementação."
```

```yaml
id: QA-H0046-03
requisito_violado: "§5.1 e §7.4 — comando de consumidores externos"
evidencia_focal: "rg -n 'from tela\\.renderizacao|import tela\\.renderizacao' tela demo | grep -v '^tela/renderizador.py' não exclui '^tela/renderizacao/'."
impacto: "Após a extração, imports legítimos entre módulos internos aparecerão como supostos consumidores externos; a saída esperada vazia será inexequível. A mesma falha é repetida na integridade estrutural."
correcao_necessaria: "Excluir explicitamente tela/renderizacao/ da busca ou restringir a busca aos consumidores fora do subpacote."
```

```yaml
id: QA-H0046-04
requisito_violado: "§7.2 e D-MOD-08 item 8 — prova de ciclos"
evidencia_focal: "O script só visita ast.ImportFrom com module iniciado por tela.renderizacao; não trata ast.Import nem imports relativos (level > 0), e o handoff não proíbe imports relativos."
impacto: "Um ciclo formado por import absoluto via ast.Import ou por from .modulo import ... pode ser aprovado pela prova."
correcao_necessaria: "Proibir imports relativos e cobrir todos os imports absolutos, ou resolver níveis relativos no grafo; manter a busca transitiva."
```

```yaml
id: QA-H0046-05
requisito_violado: "§7.6 — fachada sem lógica substantiva"
evidencia_focal: "A condição len(body)==1 e Return/Pass/Expr aprova qualquer lógica dentro da expressão, por exemplo return delegado(x) if condicao else outro(x) ou return transformar(calcular(x))."
impacto: "A fachada pode conter cálculo, condicional ou transformação material e ainda satisfazer o critério estrutural."
correcao_necessaria: "Restringir a prova a delegação mecânica verificável por AST, distinguindo chamada direta com argumentos preservados de expressões substantivas."
```

```yaml
id: QA-H0046-06
requisito_violado: "D-MOD-08 item 10 — localização direta das responsabilidades"
evidencia_focal: "O smoke nominal da §7.7 verifica somente mapa_fisico_de_itens, _linhas_barra e _montar_corpo_horizontal; não verifica os demais módulos e símbolos listados na arquitetura."
impacto: "Módulos previstos podem estar ausentes, vazios ou com responsabilidades trocadas sem falhar a prova."
correcao_necessaria: "Ampliar a prova para todos os módulos e símbolos nominais, ou fornecer verificação AST equivalente que falhe para ausência e localização incorreta."
```

O diagnóstico factual, a fachada nominal, os consumidores vigentes, os cinco ajustes focais, os caminhos de testes e a preservação futura dos Handoffs 2 e 3 foram confirmados. Não foram identificadas decisão funcional nova, migração deliberada de consumidores ou alteração necessária fora do manifesto. O estado `_quadro_minimo_lancador_ativo` exige reset por chamada; o handoff deve explicitar a operação proprietária de reset ao corrigir o achado de dependências/estado, pois os acessores listados cobrem apenas ativação e leitura.

status: H2_HANDOFF_PATCH_REQUIRED
