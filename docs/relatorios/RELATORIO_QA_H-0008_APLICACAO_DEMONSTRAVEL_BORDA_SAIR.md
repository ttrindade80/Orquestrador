# Relatório de QA — H-0008 Aplicação demonstrável mínima com borda/sair

## Status

QA_APPROVED

## Escopo auditado

Foi auditada a implementação do ciclo:

```text
H-0008 — Aplicação demonstrável mínima com borda/sair
```

Objetivo verificado: criação de uma aplicação demonstrável mínima em
`tela/demo.py`, com alternância local de borda por comando interno `b`,
saída por comando interno `s`, estado mantido somente em memória e
preservação do diagnóstico não interativo de H-0004/H-0006/H-0007.

Não foram feitas correções em código, testes ou documentação existente.
Este relatório é o único arquivo criado durante o QA.

## Arquivos lidos

Arquivo de solicitação do QA:

```text
/home/tiago/.codex/attachments/4e1bd7df-c7c4-41fb-b33d-56c18b0783d7/pasted-text.txt
```

Arquivos do escopo autorizado:

```text
docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
docs/relatorios/RELATORIO_AUDITORIA_H-0008_HANDOFF.md
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
tela/demo.py
tela/teste_demo.py
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
tela/teste_diagnostico.py
config/telas/orquestrador.json
```

Nenhum contrato, ADR, `NOMENCLATURA.md`, `config/estilo.json`,
`config/barra_de_menus.json`, `config/layout_console.json` ou
`config/lancador.json` foi lido.

## Comandos executados

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
python tela/teste_loader.py
python tela/teste_modelo.py
python tela/teste_renderizador.py
python tela/teste_diagnostico.py
python tela/teste_demo.py
python tela/diagnostico.py
printf 'b\ns\n' | python tela/demo.py
grep -R "config/estilo.json\|config/barra_de_menus.json\|config/layout_console.json\|config/lancador.json" -n tela docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md || true
grep -R "curses\|textual\|rich\|get_terminal_size\|shutil.get_terminal_size\|resize\|terminal" -n tela || true
grep -R "registry\|binding\|bindings\|tela_destino\|naveg" -n tela/demo.py tela/teste_demo.py || true
find tela -type d -name '__pycache__' -print
find tela -type f -name '*.pyc' -print
git status --short
git diff --stat
git diff --name-only
```

## Resultado dos testes

Todos os comandos obrigatórios encerraram com código `0`.

```text
orquestrador.json OK
python tela/teste_loader.py         Total: 37 | Passaram: 37 | Falharam: 0
python tela/teste_modelo.py         Total: 30 | Passaram: 30 | Falharam: 0
python tela/teste_renderizador.py   Total: 58 | Passaram: 58 | Falharam: 0
python tela/teste_diagnostico.py    Total: 26 | Passaram: 26 | Falharam: 0
python tela/teste_demo.py           Total: 49 | Passaram: 49 | Falharam: 0
```

`python tela/diagnostico.py` imprimiu a saída default curva e encerrou com
código `0`, sem solicitar entrada do usuário.

## Demonstração controlada

Comando executado:

```bash
printf 'b\ns\n' | python tela/demo.py
```

Resultado: código de saída `0`, stdout com exatamente dois renders
consecutivos, primeiro com borda curva e depois com borda reta após `b`.
O comando `s` encerrou a execução sem render adicional.

Trecho inicial e ponto de alternância observados:

```text
╭ ORQUESTRADOR ──────────────────────────╮
│ Tela raiz do sistema — ponto de entrada│
...
╰────────────────────────────────────────╯
┌ ORQUESTRADOR ──────────────────────────┐
│ Tela raiz do sistema — ponto de entrada│
...
└────────────────────────────────────────┘
```

A igualdade estrita com `_EXPECTED_CURVA + _EXPECTED_RETA` também foi
verificada por `python tela/teste_demo.py`.

## Verificação de escopo Git

Antes da criação deste relatório, `git status --short` mostrou somente os
artefatos esperados do ciclo:

```text
?? docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
?? docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
?? docs/relatorios/RELATORIO_AUDITORIA_H-0008_HANDOFF.md
?? tela/demo.py
?? tela/teste_demo.py
```

`git diff --stat` e `git diff --name-only` não produziram saída.

Não há modificação rastreada em `tela/renderizador.py`,
`tela/diagnostico.py`, `config/telas/orquestrador.json`, contratos, ADRs,
`NOMENCLATURA.md`, índice, backlog ou issues.

Após este QA, espera-se que este arquivo também apareça como `??`:

```text
docs/relatorios/RELATORIO_QA_H-0008_APLICACAO_DEMONSTRAVEL_BORDA_SAIR.md
```

## Verificação de aderência ao handoff

1. `tela/demo.py` foi criado como aplicação demonstrável mínima.
2. `tela/teste_demo.py` foi criado com testes automatizados.
3. `tela/diagnostico.py` permanece não interativo e determinístico.
4. `tela/renderizador.py` não aparece em `git status` nem em `git diff`.
5. A demo usa `renderizar_tela(modelo, tipo_borda=...)`.
6. A demo não reimplementa lógica de renderização; delega ao renderizador.
7. `criar_estado_inicial()` retorna `{"tipo_borda": "curva", "saindo": False}`.
8. `processar_comando` retorna novo dict e não muta o estado recebido.
9. `"b"` alterna `"curva"` para `"reta"`.
10. `"b"` alterna `"reta"` para `"curva"`.
11. `"s"` marca `saindo=True`.
12. Comandos diferentes de `"b"` e `"s"` não têm efeito.
13. Comandos são case-sensitive.
14. `renderizar_estado` delega usando `tipo_borda=estado["tipo_borda"]`.
15. `main()` permite demonstração controlada via stdin.
16. `printf 'b\ns\n' | python tela/demo.py` executa com exit `0`.
17. A demonstração produz render inicial curva e render reta após `"b"`.
18. O estado de borda é mantido somente em memória durante a execução.
19. Não há persistência de estado.
20. Não há escrita em arquivo pela demo.
21. Não há alteração de JSON/config.
22. Não há alteração de contratos, ADRs, NOMENCLATURA, índice, backlog ou issues.
23. Não há leitura de `config/estilo.json`.
24. Não há leitura de `config/barra_de_menus.json`.
25. Não há leitura de `config/layout_console.json`.
26. Não há leitura de `config/lancador.json`.
27. Comandos `"b"` e `"s"` são comandos internos da demo.
28. Comandos `"b"` e `"s"` não são bindings ativos do JSON.
29. Comandos `"b"` e `"s"` não são execução real de chips declarativos.
30. Não há lançador.
31. Não há abertura de tela de teste.
32. Não há navegação entre telas.
33. Não há registry de ações.
34. Não há dashboard real nem dados de dashboard.
35. Não há pop-up.
36. Não há tela de processamento.
37. Não há filtros, paginação funcional ou seleção.
38. Não há resize, largura dinâmica ou layout responsivo.
39. Não há uso de `curses`, `textual`, `rich` ou biblioteca de UI.
40. `tela/teste_demo.py` cobre alternância, saída, imutabilidade,
    case-sensitivity, subprocess e preservação do diagnóstico.
41. `python tela/diagnostico.py` continua imprimindo a saída default curva.
42. Testes anteriores continuam passando.
43. `docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md`
    existe e registra comandos/resultados.

## Achados

### Bloqueantes

Nenhum.

### Não bloqueantes

Nenhum.

## Avaliação dos pontos críticos

### API interna da demo

As quatro funções exigidas pelo handoff existem com os nomes esperados:
`criar_estado_inicial`, `processar_comando`, `renderizar_estado` e `main`.
O comportamento observado nos testes corresponde ao contrato congelado.

### Alternância em memória

A alternância de borda ocorre apenas no dict de estado local da demo.
Não há variável global mutável para persistir `tipo_borda`, nem escrita em
arquivo ou JSON.

### Comando de saída

O comando interno `"s"` define `saindo=True` e encerra o loop sem imprimir
novo render. O tipo de borda é preservado no estado retornado.

### Demonstração via stdin

`main()` itera sobre `sys.stdin`, usa `linha.strip()` e não chama `input()`.
A execução por pipe com `b\ns\n` é determinística, sem prompt, sem stderr e
com código de saída `0`.

### Preservação do diagnóstico

`diagnostico.py` continua sem `sys.stdin`, sem `input(` e sem loop
interativo. `python tela/diagnostico.py` imprime a tela curva default e
encerra com código `0`.

### Comandos locais vs ações declarativas

Os comandos `"b"` e `"s"` existem somente como comandos locais da demo. Não
há registry, ativação de bindings, navegação por `tela_destino` ou execução
real de chips declarativos.

### Ausência de funcionalidades fora de escopo

Não foi identificada implementação de lançador, tela de teste, navegação,
dashboard real, pop-up, processamento, filtros funcionais, paginação,
seleção, resize, largura dinâmica, layout responsivo, `curses`, `textual`,
`rich` ou biblioteca de UI.

As varreduras pontuais retornaram apenas ocorrências em docstrings,
comentários ou testes que afirmam a ausência dessas funcionalidades. Não
houve evidência de uso executável fora de escopo.

## Conclusão

A implementação adere estritamente ao handoff H-0008 e preserva os
invariantes de H-0001 a H-0007. A demo é mínima, controlável por stdin,
não persiste estado, não altera configuração e mantém clara a separação
entre comandos locais e arquitetura real de ações ainda não implementada.

## Recomendação

QA aprovado para o ciclo H-0008.
