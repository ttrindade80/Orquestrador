# Relatório QA — Implementação H-0062

## rastreabilidade

```yaml
etapa: QA_IMPLEMENTACAO
objeto: H-0062
handoff: docs/handoff/H-0062-tela-selecao-interativa-presets-estilo.md
implementacao: docs/relatorios/IMP-0062-tela-selecao-interativa-presets-estilo.md
```

## resultado

```yaml
status: I2_IMPLEMENTATION_PATCH_REQUIRED
verificacoes_executadas:
  - leitura integral do manifesto e leitura focal de H-0061.
  - git diff focal, git diff de config/estilo.json, git diff --cached --name-only e git status; stage vazio e config/estilo.json sem delta.
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_estilo.py demo/teste_demo_estilo.py — 13 passed.
  - PYTHONDONTWRITEBYTECODE=1 python -m pytest — 1191 passed.
  - demo direta com h0062_estilo e entrada non-TTY; F4 a partir da raiz; navegação, alteração, Aplicar contextual e saída observados.
  - probes objetivos de F4 físico normalizado, catálogo dinâmico, default, candidato/baseline/global, solicitação isolada, amostras e fronteira H-0063.
achados:
  - id: QA-H0062-001
    requisito_violado: "Amostra de chip deve refletir delimitadores, capitalização e campos visuais, incluindo cores, do próprio preset."
    evidencia_focal: "tela/estilo.py:168-176 usa apenas caractere_esquerdo, caractere_direito e caixa_alta; não consome cor_texto ou cor_fundo. config/estilo.json:50-51 e os presets de destaque fornecem esses campos. Probe com cores distintas retornou somente ('<Aa>',)."
    impacto: "Destaque Texto e Destaque Fundo podem produzir a mesma amostra textual; cores de um preset novo também não são representadas. A tela não demonstra integralmente os dados visuais do catálogo."
    camada_responsavel: "tela/estilo.py e renderer específico de H-0062"
    correcao_necessaria: "Derivar/aplicar cor_texto e cor_fundo do registro do preset usando a tradução canônica de cores, sem catálogo ou hardcode paralelo, e adicionar teste que diferencie ambos os campos."
validacao_manual_necessaria:
  - id: QA-H0062-MANUAL-001
    requisito: "Reconhecimento físico de F4 em TTY real."
    motivo_de_nao_ser_comprovavel_automaticamente: "O teste independente cobre bytes/sequências no descritor, mas não a emissão da sequência pelo terminal físico."
    comando_fixture: "PYTHONDONTWRITEBYTECODE=1 python demo/demo.py; fixture config/telas/demo/h0062_estilo.json; acionar F4 no TTY."
    resultado_esperado: "Abrir h0062_estilo pelo dispatcher vigente, sem ação para F1/F2/F3/F5/F11."
  - id: QA-H0062-MANUAL-002
    requisito: "Redesenho, geometria de largura/altura e legibilidade das miniaturas em TTY real."
    motivo_de_nao_ser_comprovavel_automaticamente: "A saída non-TTY comprova conteúdo e transições, mas não prova células visuais, ausência de resíduos após redesenho ou legibilidade sob redimensionamento real."
    comando_fixture: "PYTHONDONTWRITEBYTECODE=1 python demo/demo.py; fixture config/telas/demo/h0062_estilo.json; abrir por F4, navegar e redimensionar o TTY."
    resultado_esperado: "Quadro com quatro categorias, amostras legíveis, Aplicar contextual e redesenho sem resíduos, mantendo a tela dentro da largura/altura disponíveis."
bloqueios: []
```

Os demais requisitos funcionais auditados estão conformes pelos testes e pela
inspeção objetiva; não foram observados persistência, publicação, popup,
estados ABORTADO/CONFIRMADO ou demonstração integrada de H-0063.
