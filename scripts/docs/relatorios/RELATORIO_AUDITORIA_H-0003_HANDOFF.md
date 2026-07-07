# Relatório de Auditoria — H-0003 Handoff

## Status final

APPROVED_WITH_NOTES

## Escopo auditado

Auditoria documental/técnica do handoff `docs/handoff/H-0003-renderizador-textual-estatico.md`, verificando se ele está fechado, consistente e seguro para implementação estrita do renderer textual estático mínimo por GLM/OpenCode, sem implementar código e sem alterar artefatos normativos.

## Arquivos lidos

- `docs/handoff/H-0003-renderizador-textual-estatico.md`
- `docs/INDICE.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/NOMENCLATURA.md`
- `docs/adr/INDICE_ADR.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/contratos/contrato_lancador.md`
- `docs/contratos/contrato_barra_de_menus.md`
- `docs/contratos/contrato_estilo.md`
- `docs/contratos/contrato_tela_json.md`
- `config/telas/orquestrador.json`
- `config/estilo.json`
- `docs/handoff/H-0001-loader-validador-tela-json.md`
- `docs/handoff/H-0002-modelo-interno-tela.md`
- `docs/relatorios/IMP-0001-loader-validador-tela-json.md`
- `docs/relatorios/IMP-0002-modelo-interno-tela.md`
- `docs/relatorios/RELATORIO_QA_H-0002_MODELO_INTERNO_TELA.md`
- `tela/loader.py`
- `tela/modelo.py`
- `tela/teste_loader.py`
- `tela/teste_modelo.py`
- `docs/backlog.md`
- `docs/issues.md`

Arquivos adicionais citados pelo handoff foram verificados quanto à existência:

- `docs/contratos/contrato_console.md`
- `docs/contratos/contrato_chip.md`
- `docs/adr/ADR-0008-modelo-configuracao-por-tela.md`
- `docs/adr/ADR-0009-caminho-formato-jsons-tela.md`

## Resultado por critério

### C-01 — Escopo estático mínimo
Status: OK
Evidência:
O handoff define o H-0003 como "primeiro renderer textual estático mínimo" e afirma que não renderiza interface visual completa, não calcula layout de terminal, não executa ações e não ativa bindings (`H-0003`, linhas 70-74). A lista de fora de escopo proíbe navegação, ações, registry de ações, bindings, filtros funcionais, paginação, seleção, registry de tipos, execução de chips, navegação por `tela_destino`, dashboard dinâmico, mudança de estilo em runtime, layout responsivo final, cálculo de bordas/colunas/truncamento dependente do terminal, ANSI e estado de runtime (`H-0003`, linhas 205-227).
Conclusão:
O escopo está limitado ao renderer textual estático mínimo e não autoriza comportamento interativo ou arquitetura nova.

### C-02 — Dependência de H-0001/H-0002
Status: OK
Evidência:
O pipeline declarado passa por `carregar_tela`, `construir_modelo`, `ModeloTela` e só então `renderizar_tela` (`H-0003`, linhas 76-85). A pré-condição exige `python tela/teste_loader.py` e `python tela/teste_modelo.py` antes de criar arquivos (`H-0003`, linhas 128-139). Os invariantes herdados preservam as 37 verificações do loader, as 30 do modelo, rejeição de tipo fora de `{console, lancador, dashboard}`, construção de `ModeloTela` a partir do loader, campos inertes, não execução de ações, não ativação de bindings, não alteração de JSON e ausência de `__pycache__`/`.pyc` (`H-0003`, linhas 392-411).
Conclusão:
O handoff preserva explicitamente H-0001 e H-0002.

### C-03 — Entrada `ModeloTela`, não JSON bruto
Status: OK
Evidência:
O handoff exige `renderizar_tela(modelo: ModeloTela) -> str` (`H-0003`, linhas 111 e 231-237), proíbe acessar `config/telas/orquestrador.json`, chamar `carregar_tela` ou importar `json`, `os`, `pathlib` para leitura no renderer (`H-0003`, linhas 87-92 e 249-255). O expected output literal é usado no teste do pipeline completo sobre o JSON atual (`H-0003`, linhas 331-368), mas a função renderizadora em si recebe o modelo. O teste com modelo fabricado exige `id="teste_fabricado"` e saída começando com `TELA: teste_fabricado` (`H-0003`, linhas 456-480).
Conclusão:
O handoff realmente impede consulta direta ao JSON dentro do renderer por regra explícita e por proibição de import/call. A observação não bloqueante é que o teste fabricado descrito prova diretamente o uso do `modelo.id`, mas não prova sozinho que todos os demais campos vêm do modelo; essa lacuna é compensada pelas proibições de importação/leitura e pelos critérios de aceite.

### C-04 — Formato textual determinístico
Status: OK
Evidência:
O formato é declarado como exato e obrigatório, incluindo linhas, espaços, separadores, ordem dos elementos e chips, `\n` e linha final (`H-0003`, linhas 281-308). O template explicita identificação da tela, schema, seção `CABEÇALHO`, seção `CORPO`, elementos com `id` e `tipo`, seção `BARRA_DE_MENUS` e chips com `id` e `texto` (`H-0003`, linhas 309-329). O expected output literal corresponde aos campos presentes em `config/telas/orquestrador.json`: `id`, `schema`, `cabecalho.titulo`, `cabecalho.descricao`, `corpo.arranjo`, três elementos e onze chips (`orquestrador.json`, linhas 2-3, 19-25, 27-28, 64-65, 101-102, 113-238).
Conclusão:
O formato está suficientemente especificado e depende de campos disponíveis em `ModeloTela`.

### C-05 — `RenderizadorErro`
Status: OK
Evidência:
`RenderizadorErro` é delimitado para argumento inválido, como `None` ou objeto que não seja `ModeloTela`; em operação normal com `ModeloTela` válido não deve lançar exceção (`H-0003`, linhas 267-277). As validações macro continuam pertencendo ao loader e ao modelo (`H-0003`, linhas 392-411).
Conclusão:
A exceção não cria política nova de validação documental e não duplica responsabilidades do loader/modelo.

### C-06 — Campos inertes
Status: OK
Evidência:
O handoff lista como inertes `bindings`, `referencias_de_acoes`, `filtros`, ações/regras de chips, `tela_destino`, `origem_dados`, `regra_geracao_itens`, itens vazios de `lancador_principal` e `_campos_inertes` (`H-0003`, linhas 372-389). Também afirma que essas pendências não devem ser erro e devem ser listadas como dados estáticos sem execução (`H-0003`, linhas 94-105).
Conclusão:
Os campos pendentes permanecem declarativos e inertes, sem navegação, filtragem, execução ou interpretação ativa.

### C-07 — Arquivos permitidos/proibidos
Status: OK
Evidência:
Arquivos permitidos: `tela/renderizador.py`, `tela/teste_renderizador.py` e `docs/relatorios/IMP-0003-renderizador-textual-estatico.md` (`H-0003`, linhas 143-152). `tela/__init__.py` é permitido somente com justificativa explícita e mínima, com preferência por não alterar (`H-0003`, linhas 154-156). O handoff proíbe alterações em `docs/NOMENCLATURA.md`, `docs/INDICE.md`, backlog, issues, contratos, ADRs, handoffs, templates, `config/`, loader/modelo/testes anteriores (`H-0003`, linhas 171-199).
Conclusão:
O conjunto de arquivos está fechado e protege contratos, ADRs, nomenclatura, configs e implementações anteriores.

### C-08 — Testes exigidos
Status: ATENÇÃO
Evidência:
`tela/teste_renderizador.py` é exigido, sem framework externo, com `sys.dont_write_bytecode = True`, saída `[PASSOU]`/`[FALHOU]`, totais e código de saída adequado (`H-0003`, linhas 415-431). As 18 verificações são pequenas e objetivas (`H-0003`, linhas 433-455). O teste fabricado cria `ModeloTela` manual e verifica `TELA: teste_fabricado` e `SCHEMA: tela.v0` (`H-0003`, linhas 456-480).
Conclusão:
Os testes são executáveis e auditáveis. Atenção não bloqueante: o teste anti-regressão com modelo fabricado poderia ser mais forte se comparasse também corpo e chips fabricados; como está, ele demonstra o uso de `id`/`schema` do modelo, enquanto a garantia contra leitura de JSON depende também das proibições e da inspeção do módulo.

### C-09 — Comandos de verificação
Status: OK
Evidência:
O handoff exige validação de `config/telas/orquestrador.json`, validação de `config/estilo.json`, `python tela/teste_loader.py`, `python tela/teste_modelo.py`, `python tela/teste_renderizador.py`, busca por `__pycache__`, busca por `.pyc`, `git status --short` e `git diff --stat` (`H-0003`, linhas 484-509).
Conclusão:
Os comandos exigidos são suficientes para verificar JSONs, invariantes anteriores, testes novos, bytecode e estado do repositório.

### C-10 — Relatório de implementação
Status: OK
Evidência:
O relatório `docs/relatorios/IMP-0003-renderizador-textual-estatico.md` é obrigatório (`H-0003`, linhas 516-522). O conteúdo exigido cobre objetivo, arquivos alterados, assinatura/imports, saída real do pipeline, invariantes H-0001/H-0002, comportamento fora de escopo, pendências preservadas, saída de comandos e resultado final (`H-0003`, linhas 524-540).
Conclusão:
O relatório futuro está bem especificado e auditável.

### C-11 — Bloqueios documentais
Status: OK
Evidência:
O handoff manda parar com `BLOCKED` ou `ARCHITECTURE_REVIEW_REQUIRED` se falharem testes anteriores, se exigir arquivo fora do permitido, mudança normativa, dependência externa, largura real de terminal, comportamento interativo, decisão arquitetural local ou informação indisponível em `ModeloTela` (`H-0003`, linhas 598-617). Os artefatos adicionais citados em ordem de autoridade existem: `contrato_tela_json.md`, `contrato_console.md`, `contrato_chip.md`, `ADR-0008` e `ADR-0009`.
Conclusão:
Não foi encontrado bloqueio documental. O handoff não depende de arquivo inexistente nem força semântica pendente.

## Achados

### A-001 — Teste fabricado poderia cobrir mais campos do modelo
Severidade: observação
Descrição:
O teste anti-regressão com modelo fabricado é útil, mas a verificação obrigatória descrita só exige provar o prefixo `TELA: teste_fabricado` e, no exemplo, `SCHEMA: tela.v0`. Isso não demonstra isoladamente que corpo e chips também vêm do modelo fabricado em vez do JSON real.
Evidência:
Verificação obrigatória: saída usando modelo fabricado começa com `TELA: teste_fabricado` (`H-0003`, linha 453). Exemplo adicional verifica `SCHEMA: tela.v0` (`H-0003`, linhas 477-480).
Correção recomendada:
Não é bloqueante para implementação. Em ajuste futuro, o Claude Code pode fortalecer o handoff exigindo que o teste fabricado também verifique `arranjo: linear`, `id: e1 | tipo: console` e `id: c1 | texto: Ok`.

## Conclusão

O handoff H-0003 pode seguir para implementação estrita por GLM/OpenCode. Ele delimita corretamente o renderer textual estático mínimo, preserva os invariantes de H-0001 e H-0002, exige consumo de `ModeloTela`, define formato textual determinístico, mantém campos pendentes como inertes e fecha arquivos, testes, comandos e relatório.

Classificação final: `APPROVED_WITH_NOTES`. Não há achados bloqueantes; há uma observação não bloqueante sobre fortalecimento futuro do teste fabricado.
