# Relatório QA — H-0049

```yaml
jsons_reais: 74
lista_nominal: correspondencia_exata
duplicatas_na_lista: 0
arquivos_inexistentes_na_lista: 0
telas_com_cabecalho_omitidas: 0
causa_divergencia_72_74: "o relatório técnico anterior contou 72 e deixou fora config/telas/demo/resultado_execucao.json e config/telas/demo/stub_b.json; ambos existem, têm cabecalho e completam os 74"
baseline_visual: incompatível_com_a_preservacao_exigida
fixture_persistente: desnecessaria
status: H3_BLOCKED_DOCUMENTATION
```

## Achados

```yaml
id: H49-QA-01
requisito: fidelidade aos tipos e limites do contrato
evidencia_focal: "contrato_cabecalho.md:104-105 fixa descrição máxima de 200 caracteres; contrato_cabecalho.md:170 e handoff:52 registram apenas inteiro > 0 para max_caracteres"
impacto: "o manifesto não fecha o limite superior contratual; uma implementação poderia aceitar max_caracteres acima de 200"
correcao_necessaria: "patch do handoff para declarar o domínio completo e testá-lo, sem deixar a decisão ao implementador"
```

```yaml
id: H49-QA-04
requisito: compatibilidade entre migração do baseline e preservação visual
evidencia_focal: "handoff:69-72 exige recuo_lateral=3 e recuo=10; config/elementos/cabecalho.json:3-12 contém esses valores, mas rg não encontrou consumidor operacional; geometria_caixa.py:41-45 usa um espaço fixo no topo e :62-72 usa um espaço fixo e alinhamento à esquerda no conteúdo; fundamentos.py:92-98 registra esse quadro"
impacto: "a aplicação semântica de 3 e 10 desloca título e descrição em relação ao quadro vigente. O arquivo global não consumido não pode ser chamado de baseline visual vigente. Preservar o quadro antigo, aplicar os valores documentais ou reinterpretar recuos são requisitos incompatíveis"
correcao_necessaria: "H2_HANDOFF_PATCH_REQUIRED para eliminar explicitamente a contradição antes da implementação; este QA não escolhe a alternativa"
```

```yaml
id: H49-QA-06
requisito: fixture de teste nominalmente fechada
evidencia_focal: "handoff:231-234 autoriza fixture persistente condicional sem caminho; teste_loader.py já fabrica documentos temporários e fundamentos.py:361-370 fabrica ModeloTela, suficientes para duas apresentações locais"
impacto: "a autorização aberta permite criar arquivo adicional sem controle de escopo, embora a evidência focal mostre que nenhum fixture persistente é necessário"
correcao_necessaria: "patch do handoff proibindo fixture persistente para esta capacidade"
```

```yaml
id: H49-QA-09
requisito: semântica contratual determinística das transformações
evidencia_focal: "contrato_cabecalho.md:147 e :173 definem inicio_de_frase apenas como transformação; handoff:57-58 diz que preserva a capitalização de início de frase e não é upper(), sem definir operação, texto inicial/minúsculo, múltiplas frases ou espaços iniciais"
impacto: "renderer e testes exigiriam uma decisão material do implementador; não há uma saída única para comprovar a ordem e o efeito da capitalização"
correcao_necessaria: "H3_BLOCKED_DOCUMENTATION: a autoridade deve fechar a semântica operacional de inicio_de_frase antes da implementação"
```

Os símbolos autorizados existem, os erros `TelaCampoObrigatorioAusente` e
`TelaEstruturaInvalida` são reutilizáveis com caminho na mensagem, e os dois
caminhos de geometria passam por `_caixa`. Os comandos `-k h0049` selecionarão
testes novos com prefixo `test_h0049_`; não há tais testes ainda porque a
implementação está expressamente bloqueada nesta etapa.
