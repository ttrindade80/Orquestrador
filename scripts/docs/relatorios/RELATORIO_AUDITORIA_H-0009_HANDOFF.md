# Relatório de Auditoria — H-0009 Handoff

## Status

AUDIT_APPROVED_WITH_NOTES

## Escopo auditado

Foi auditado o handoff `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`, limitado ao ciclo H-0009 — Layout por dimensão do terminal e entrada sem echo.

A auditoria verificou se o handoff está fechado, consistente e seguro para entrega ao GLM/OpenCode em implementação estrita, sem antecipar dashboard real, lançador, navegação, registry, bindings declarativos ativos, leitura de configs de layout/lancador ou alteração de documentos normativos.

## Arquivos lidos

- `docs/handoff/H-0009-layout-terminal-entrada-sem-echo.md`
- `docs/contratos/contrato_processo_desenvolvimento.md`
- `docs/contratos/contrato_composicao_corpo.md`
- `docs/handoff/H-0008-aplicacao-demonstravel-borda-sair.md`
- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/diagnostico.py`
- `tela/teste_diagnostico.py`
- `config/telas/orquestrador.json`

Nenhum arquivo extra foi consultado. O contrato da barra de menus não foi consultado porque o handoff mantém `b`, `s` e `Esc` como comandos internos da demo, sem tentar alterar semanticamente chips ou executar ações declarativas.

## Verificações realizadas

- Conferência do escopo positivo e das proibições explícitas do H-0009.
- Conferência da compatibilidade da nova assinatura `renderizar_tela(modelo, tipo_borda="curva", largura=None)` com as chamadas H-0007/H-0008.
- Conferência do fallback determinístico de 42 caracteres.
- Conferência da divisão entre largura explícita para testes e largura real do terminal na demo.
- Conferência da remoção restrita de linhas vazias entre caixas, sem tentativa de resolver R-10.
- Conferência da preservação de `diagnostico.py` como não interativo.
- Conferência da entrada por tecla direta em TTY com `termios`/`tty`, sem Enter e sem echo.
- Conferência de `"\x1b"` como Esc real obrigatório.
- Conferência de modo sem TTY/pipe preservado para testes automatizados.
- Conferência dos arquivos autorizados e proibidos.
- Validação sintática de `config/telas/orquestrador.json` com `python -m json.tool`.

## Achados

### Bloqueantes

Nenhum achado bloqueante.

### Não bloqueantes

1. A confirmação de "sem echo" em TTY real depende de QA manual controlado. O handoff mitiga isso exigindo inspeção de código (`termios`, `tty`, `isatty`, ausência de `input(`) e uma demonstração manual obrigatória.
2. O contrato de composição prevê, para o compositor final, largura dinâmica em tempo real e parâmetros de layout em configs transicionais. O H-0009 delimita explicitamente uma correção mínima no renderer demonstrável atual, sem SIGWINCH, sem compositor completo e sem leitura de `config/layout_console.json` ou `config/lancador.json`. A ressalva é aceitável porque o handoff marca esses avanços como fora de escopo e orienta bloqueio se a implementação exigir decisão arquitetural.

## Avaliação dos pontos críticos

### Nova assinatura do renderer

A assinatura proposta é clara:

```python
renderizar_tela(modelo, tipo_borda="curva", largura=None)
```

Ela preserva as chamadas anteriores:

```python
renderizar_tela(modelo)
renderizar_tela(modelo, tipo_borda="curva")
renderizar_tela(modelo, tipo_borda="reta")
```

Não há quebra de compatibilidade aparente com H-0007/H-0008.

### Largura dinâmica com fallback determinístico

O handoff define `largura=None` como fallback determinístico para `TOTAL_WIDTH = 42`, preservando o diagnóstico e chamadas existentes. Também exige largura explícita nos testes e largura real do terminal na demo via:

```python
shutil.get_terminal_size(fallback=(80, 24)).columns
```

A largura fixa de 42 não é transformada em regra normativa final; é mantida apenas como fallback determinístico.

### Remoção de linhas entre regiões

O handoff remove somente os separadores `"\n\n"` entre caixas, substituindo-os por `"\n"`. A nota sobre R-10 é suficientemente segura: registra que R-10 trata de espaçamento interno, não da linha vazia entre regiões, e declara a correção de R-10 como fora de escopo.

### Entrada sem Enter e sem echo

O handoff define modo TTY com `termios`/`tty`, leitura de um caractere por vez e restauração do terminal em `finally`. Isso cobre a exigência técnica de tecla direta sem Enter e sem echo, com QA manual para a parte não totalmente automatizável.

### Esc real

O handoff exige `"\x1b"` como comando de saída, com `saindo=True` e preservação de `tipo_borda`. `s` é mantido apenas como atalho auxiliar para pipe/testes e não substitui Esc.

### TTY vs pipe

A divisão está clara:

- TTY: leitura por tecla única em modo raw.
- Não-TTY/pipe: leitura linha a linha preservada para subprocess e testes.

O handoff fornece estratégia automatizável para pipe e inspeção de código, além de QA manual para TTY real.

### Preservação do diagnóstico

`diagnostico.py` deve permanecer não interativo e chamar `renderizar_tela(modelo)` sem largura explícita. O handoff exige atualização apenas dos esperados de teste, não alteração de `diagnostico.py`.

### Comandos locais vs ações declarativas

O handoff é explícito: `b`, `s` e `Esc` são comandos internos da demo. Não cria registry, não ativa bindings declarativos do JSON e não executa chips reais.

### Ausência de funcionalidades fora de escopo

O handoff proíbe dashboard real, lançador, navegação, tela de teste, pop-up, processamento, filtros, paginação funcional, seleção, resize reativo completo, layout responsivo complexo, leitura de configs fora de escopo e bibliotecas externas de UI.

### Arquivos autorizados

O handoff restringe implementação aos arquivos:

- `tela/renderizador.py`
- `tela/teste_renderizador.py`
- `tela/demo.py`
- `tela/teste_demo.py`
- `tela/teste_diagnostico.py`
- `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md`

Também explicita que qualquer necessidade de alterar arquivo adicional deve parar com `ARCHITECTURE_REVIEW_REQUIRED`.

## Conclusão

O handoff H-0009 está suficientemente fechado para implementação estrita. Ele define APIs, comportamento, testes, modo TTY, modo pipe, arquivos permitidos, arquivos proibidos, critérios de aceite e comandos finais obrigatórios.

Não foram encontrados pontos que autorizem dashboard real, lançador, navegação, registry, bindings declarativos ativos, leitura de configs proibidas ou alteração documental/normativa.

## Recomendação

Liberar o H-0009 para implementação pelo GLM/OpenCode com status `AUDIT_APPROVED_WITH_NOTES`.

A implementação deve seguir estritamente o handoff e registrar no relatório `docs/relatorios/IMP-0009-layout-terminal-entrada-sem-echo.md` a evidência automatizada e a confirmação manual de TTY sem echo.
