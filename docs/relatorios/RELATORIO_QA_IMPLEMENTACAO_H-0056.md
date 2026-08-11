# Relatório QA de implementação — H-0056

```yaml
status: I2_IMPLEMENTATION_PATCH_REQUIRED
handoff: H-0056
```

## Evidências automatizadas

- Testes focais: `PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py -q` — **20 passed**, código 0.
- Suíte canônica: `PYTHONDONTWRITEBYTECODE=1 python -m pytest` — **1117 passed**, código 0.
- Demonstração non-TTY: fluxo `p`, tecla não declarada, `Esc`, `d`, `Esc`, `Esc` via `demo/demo.py` — código 0; a saída mostrou título `Mensagem`, texto `Exemplo de pop-up.`, chip `[Esc] Voltar`, preservação durante a tecla ignorada, retorno e encerramento.
- `git diff --check` — código 0. Nenhum arquivo staged foi identificado.

A implementação focal de configuração, chip, conteúdo runtime, overlay, captura modal, geometria simples e retorno `ABORTADO` está coberta pelos testes e pelas inspeções realizadas. A validação TTY não foi executada.

## Achados

### QA-H0056-IMP-001 — diff fora do manifesto

- Requisito violado: o manifesto do H-0056 autoriza somente os quatro arquivos novos de implementação, três arquivos alterados e o relatório de implementação; a QA também exige ausência de alteração incidental e de autoridade documental.
- Evidência: `git status --short` mostra, além dos arquivos autorizados, alterações em `docs/INDICE.md`, `docs/NOMENCLATURA.md`, `docs/backlog.md`, contratos e nomenclatura, e arquivos não rastreados em `docs/adr/`, `docs/contratos/`, `docs/handoff/`, `docs/nomenclatura/` e diversos relatórios.
- Esperado: diff restrito ao manifesto aprovado.
- Observado: documentação de autoridade e artefatos incidentais permanecem no worktree.
- Após correção, executar `git status --short`, `git diff --check` e novamente os testes focais.

### QA-H0056-IMP-002 — `popups: null` aceito como ausência

- Requisito violado: `popups` é um mapa/objeto; somente a ausência do campo e `popups: {}` são válidas.
- Evidência: `tela/renderizacao/popup.py:208-210` usa `raw.get("popups")` e retorna `{}` quando o valor explícito é `None`; a execução `validar_popups({"popups": None})` retornou `{}`.
- Esperado: rejeição com `PopupErro` para valor presente não-objeto.
- Observado: `null` é aceito pela validação geral.
- Após correção, acrescentar/executar teste focal que exija `PopupErro` para `validar_popups({"popups": None})`, preservando os casos de ausência e mapa vazio.

### QA-H0056-IMP-003 — resíduo de cache de testes

- Requisito violado: ausência de temporários não autorizados.
- Evidência: a auditoria encontrou o diretório persistente `.pytest_cache/`.
- Esperado: nenhum cache/temporário persistente no resultado QA.
- Observado: `.pytest_cache/` permanece no worktree; não foi removido, conforme instrução.
- Após correção, repetir a varredura de `__pycache__`, `.pyc` e temporários.
