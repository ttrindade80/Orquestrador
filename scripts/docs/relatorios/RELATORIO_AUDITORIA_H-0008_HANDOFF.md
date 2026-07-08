# Relatório de Auditoria — H-0008 Handoff

## Status

AUDIT_APPROVED

## Escopo auditado

Foi auditado somente o handoff:

```text
docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
```

O ciclo auditado é exclusivamente:

```text
H-0008 — Aplicação demonstrável mínima com borda/sair
```

A auditoria verificou se o handoff está suficientemente fechado,
consistente e seguro para entrega ao GLM/OpenCode para implementação
estrita, sem antecipar H-0009 e sem autorizar implementação fora do
escopo delimitado.

## Arquivos lidos

Arquivos obrigatórios lidos:

```text
docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md
docs/handoff/H-0007-alternancia-bordas-memoria.md
docs/relatorios/IMP-0007-alternancia-bordas-memoria.md
docs/relatorios/RELATORIO_QA_H-0007_ALTERNANCIA_BORDAS_MEMORIA.md
tela/renderizador.py
tela/teste_renderizador.py
tela/diagnostico.py
tela/teste_diagnostico.py
config/telas/orquestrador.json
```

Arquivo adicional lido:

```text
/home/tiago/.codex/attachments/04c58d41-c5ed-485b-91d7-34c73af2c337/pasted-text.txt
```

Justificativa: o arquivo continha a solicitação desta auditoria, incluindo
escopo autorizado, lista restrita de leitura, pontos obrigatórios de
verificação e formato esperado deste relatório.

Não foram lidos contratos, ADRs, `NOMENCLATURA.md` nem configs fora de
`config/telas/orquestrador.json`.

## Verificações realizadas

- Conferida a aderência do H-0008 ao escopo positivo autorizado para
  aplicação demonstrável local mínima.
- Conferida a ausência de autorização para lançador, tela de teste,
  navegação, registry, bindings ativos, ações declarativas reais,
  dashboard real, pop-up, processamento, filtros, paginação, seleção,
  resize, largura dinâmica, layout responsivo ou biblioteca de UI.
- Conferida a preservação de `tela/diagnostico.py` como ponto de entrada
  não interativo, determinístico e com saída default curva.
- Conferido que o H-0008 consome a API H-0007
  `renderizar_tela(modelo, tipo_borda=...)`.
- Conferido que `tela/renderizador.py` já entrega a API H-0007 esperada e
  que o H-0008 proíbe sua alteração.
- Conferido que o H-0008 não exige alteração de `tela/modelo.py`,
  `tela/loader.py`, testes de loader/modelo/renderizador ou configs.
- Conferida a API interna congelada de `tela/demo.py`.
- Conferido o comportamento esperado da demonstração via stdin com
  `printf 'b\ns\n' | python tela/demo.py`.
- Conferida a separação entre comandos internos da demo (`b`, `s`) e os
  chips declarativos `[B] Borda` e `[Esc] Sair`.
- Conferida a lista de arquivos permitidos e proibidos.
- Conferidos os comandos finais obrigatórios exigidos para o relatório de
  implementação H-0008.
- Validado que `config/telas/orquestrador.json` continua JSON válido por:

```bash
python -m json.tool config/telas/orquestrador.json >/dev/null && echo "orquestrador.json OK"
```

Saída:

```text
orquestrador.json OK
```

## Achados

### Bloqueantes

Nenhum.

### Não bloqueantes

Nenhum.

## Avaliação dos pontos críticos

### API interna da demo

O handoff congela explicitamente a API interna de `tela/demo.py`:

```python
criar_estado_inicial() -> dict
processar_comando(estado: dict, comando: str) -> dict
renderizar_estado(estado: dict, modelo: ModeloTela) -> str
main() -> int
```

A especificação define estado inicial fechado:

```python
{"tipo_borda": "curva", "saindo": False}
```

Também define que `criar_estado_inicial()` retorna sempre novo dict,
sem estado global mutável e sem leitura de arquivo, JSON ou `sys.stdin`.

`processar_comando` está suficientemente fechado:

- não modifica o dict recebido;
- retorna sempre novo dict com as chaves `"tipo_borda"` e `"saindo"`;
- `"b"` alterna `"curva"` para `"reta"` e `"reta"` para `"curva"`;
- `"s"` marca `saindo=True` sem alterar `tipo_borda`;
- comandos desconhecidos, inclusive string vazia, retornam cópia sem
  alteração;
- a semântica é case-sensitive, de modo que `"B"` e `"S"` não têm efeito;
- não chama `renderizar_tela` nem acessa modelo.

`renderizar_estado` está fechado como delegação direta para a API H-0007:

```python
renderizar_tela(modelo, tipo_borda=estado["tipo_borda"])
```

`main()` está definido de forma testável, com leitura de `sys.stdin` linha a
linha, sem `input()`, sem prompt, sem mensagem extra e com retorno `0`.

Conclusão: API interna aprovada para implementação estrita.

### Demonstração via stdin

O comando de demonstração é definido sem ambiguidade:

```bash
printf 'b\ns\n' | python tela/demo.py
```

O H-0008 especifica que a demo:

1. imprime a renderização inicial com borda curva antes de processar o
   primeiro comando;
2. processa `b`, alterna para borda reta e imprime a renderização reta;
3. processa `s`, marca saída e encerra sem nova renderização.

A saída esperada está definida como exatamente dois renders, sem separador:
`_EXPECTED_CURVA + _EXPECTED_RETA`. O handoff elimina a ambiguidade entre
"render inicial com borda curva", "renders apenas após b" e o comando
`printf 'b\ns\n'`.

Conclusão: demonstração via stdin aprovada.

### Comandos locais vs ações declarativas

O handoff afirma explicitamente que `b` e `s` são comandos internos de
`tela/demo.py`. Eles não são:

- bindings declarativos;
- registry de ações;
- ações genéricas;
- execução real dos chips `[B] Borda` e `[Esc] Sair`;
- transformação de campos do JSON em comportamento ativo.

Também define bloqueio explícito com `ARCHITECTURE_REVIEW_REQUIRED` caso o
executor entenda que `[B] Borda` ou `[Esc] Sair` devam ser transformados em
ações declarativas do JSON.

Conclusão: separação aprovada.

### Preservação do diagnóstico

O H-0008 declara que `tela/diagnostico.py` permanece não interativo e
determinístico, e proíbe sua alteração. O diagnóstico deve continuar chamando
`renderizar_tela(modelo)` sem `tipo_borda`, preservando a saída default curva
H-0006/H-0007.

O arquivo atual `tela/diagnostico.py` confirma esse desenho: não há loop,
não há leitura de `sys.stdin`, não há `input()`, e o modo executável imprime
o resultado com `print(resultado, end="")` e encerra com código `0`.

Conclusão: preservação aprovada.

### Arquivos autorizados

O handoff restringe a implementação aos seguintes arquivos:

```text
tela/demo.py
tela/teste_demo.py
tela/teste_diagnostico.py
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
```

`tela/teste_diagnostico.py` só pode ser alterado se necessário. O próprio
handoff declara preferência por nenhuma alteração.

A lista é exaustiva e sem exceção: caso qualquer outro arquivo precise ser
alterado, o executor deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

Conclusão: fronteira de arquivos aprovada.

### API H-0007 e renderizador

O H-0008 consome a API H-0007:

```python
renderizar_tela(modelo: ModeloTela, tipo_borda: str = "curva") -> str
```

O arquivo atual `tela/renderizador.py` contém essa assinatura, valida
`"curva"` e `"reta"`, preserva a saída default curva e não lê configuração.
O H-0008 proíbe alterar `tela/renderizador.py`.

Conclusão: dependência técnica aprovada.

### Diagnóstico default curva

O H-0008 inclui a saída curva H-0006/H-0007 como default e exige preservação.
Os relatórios H-0007 lidos registram `QA_APPROVED`, 58 verificações do
renderizador passando e 26 verificações do diagnóstico passando.

Conclusão: base herdada aprovada.

### Ausência de persistência

O H-0008 exige estado de borda somente em memória, sem persistir em arquivo,
config, JSON, variável global mutável ou preferência externa. Também exige
que uma segunda execução comece novamente com `"curva"`.

Conclusão: regra de ausência de persistência aprovada.

### Configs e documentos normativos

O handoff proíbe alterar qualquer arquivo em `config/` e proíbe leitura de:

```text
config/estilo.json
config/layout_console.json
config/lancador.json
config/barra_de_menus.json
```

Também proíbe alteração de contratos, ADRs, `NOMENCLATURA.md`, índice,
backlog, issues, handoffs anteriores e documentos normativos.

Conclusão: escopo documental aprovado.

### Testes automatizados

O H-0008 exige `tela/teste_demo.py`, sem `unittest`, sem `pytest` e sem
framework externo. A cobertura especificada inclui:

- estado inicial;
- imutabilidade e case sensitivity de `processar_comando`;
- `renderizar_estado` para curva e reta;
- integração por subprocess com `b\ns\n`;
- preservação de `config/telas/orquestrador.json`;
- preservação de `tela/diagnostico.py`;
- ausência de `sys.stdin` e `input(` no diagnóstico.

Conclusão: cobertura automatizada suficiente para o ciclo.

### Comando de demonstração

O comando final de demonstração é explícito:

```bash
printf 'b\ns\n' | python tela/demo.py
```

O handoff também exige verificação de EOF sem `s`:

```bash
printf '' | python tela/demo.py; echo "exit_code=$?"
```

Conclusão: comando demonstrável aprovado.

### Relatório de implementação

O H-0008 exige o relatório:

```text
docs/relatorios/IMP-0008-aplicacao-demonstravel-borda-sair.md
```

O formato esperado inclui status, arquivos criados/alterados, arquivos não
alterados, excertos da API implementada, saída real da demo, testes,
invariantes H-0001 a H-0007, diagnóstico, ausência de persistência, itens
fora de escopo preservados, comandos finais, nota sobre largura fixa e
resultado final.

Conclusão: relatório de implementação aprovado.

## Pontos obrigatórios de verificação

1. Autoriza apenas o H-0008, sem antecipar H-0009: aprovado.
2. Não implementa lançador, tela de teste nem navegação entre telas:
   aprovado.
3. Cria aplicação demonstrável local separada ou claramente delimitada:
   aprovado.
4. Preserva `tela/diagnostico.py` como não interativo e determinístico:
   aprovado.
5. Mantém saída default do diagnóstico igual à curva H-0006/H-0007:
   aprovado.
6. Usa a API H-0007 `renderizar_tela(modelo, tipo_borda=...)`: aprovado.
7. Não exige alteração de `tela/renderizador.py`, salvo justificativa
   objetiva: aprovado; a alteração é proibida.
8. Não exige alteração de `tela/modelo.py`, `tela/loader.py`, testes de
   loader/modelo ou configs: aprovado.
9. Define comandos locais mínimos da demo sem transformá-los em registry,
   bindings ou ações declarativas reais: aprovado.
10. Define estado de borda apenas em memória: aprovado.
11. Não persiste estado: aprovado.
12. Não altera JSON/config/contratos/ADRs/normativos: aprovado.
13. Não lê configs fora de `config/telas/orquestrador.json`: aprovado.
14. Não implementa resize, largura dinâmica ou layout responsivo: aprovado.
15. Define API interna de `tela/demo.py` de modo fechado e testável:
   aprovado.
16. Define testes automatizados em `tela/teste_demo.py`: aprovado.
17. Define comando de demonstração não ambíguo: aprovado.
18. Exige relatório de implementação `IMP-0008`: aprovado.
19. Exige os comandos finais obrigatórios: aprovado.

## Conclusão

O handoff H-0008 está suficientemente fechado, consistente e seguro para
entrega ao GLM/OpenCode para implementação estrita.

Não foram identificados bloqueantes nem ressalvas. A implementação deve
seguir exatamente os arquivos permitidos e parar com `ARCHITECTURE_REVIEW_REQUIRED`
se surgir necessidade de alterar qualquer arquivo fora da lista exaustiva.
