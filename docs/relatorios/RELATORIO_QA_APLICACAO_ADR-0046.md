# RELATORIO_QA_APLICACAO_ADR-0046

## Escopo e limites

QA semântico e normativo independente da aplicação documental da ADR-0046.
Não foram corrigidos documentos, implementado código, alterada configuração,
criado handoff, alterados backlog, histórico, ADR ou estado operacional, nem
realizados stage, commit ou push.

## Baseline e verificações mecânicas

- Projeto: Orquestrador.
- Branch: `master`.
- HEAD: `77bd8bf3772985325bc51a850f7c6d76d61ad573`.
- Stage: vazio na inspeção inicial; este relatório foi mantido fora do stage.
- `git diff --check`: **PASS**.
- Nenhum commit ou push foi realizado.
- A execução não foi bloqueada por baseline; portanto,
  `BLOCKED_QA_ADR_APPLICATION` não se aplica.

O worktree já continha, antes desta auditoria, o delta de `docs/backlog.md`,
a ADR, relatórios e os documentos normativos do ciclo. O diff da aplicação
documental é composto pelos sete documentos normativos previstos:

- `docs/nomenclatura/10_ESTILO.md`;
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`;
- `docs/nomenclatura/35_POPUP.md`;
- `docs/contratos/contrato_estilo.md`;
- `docs/contratos/contrato_barra_de_menus.md`;
- `docs/contratos/contrato_popup.md`.

`docs/nomenclatura/32_CONSOLE.md`,
`docs/contratos/contrato_console.md`, `config/estilo.json` e o código não
foram alterados. O delta de backlog e os demais relatórios/ADR já estavam no
worktree e não foram criados nem alterados por este QA.

## Fontes auditadas integralmente

- `docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md`;
- `docs/relatorios/RELATORIO_QA_ADR-0046.md`;
- `docs/relatorios/RELATORIO_APLICACAO_ADR-0046.md`;
- `docs/nomenclatura/10_ESTILO.md`;
- `docs/nomenclatura/02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md`;
- `docs/nomenclatura/31_BARRA_DE_MENUS_E_CHIPS.md`;
- `docs/nomenclatura/35_POPUP.md`;
- `docs/contratos/contrato_estilo.md`;
- `docs/contratos/contrato_barra_de_menus.md`;
- `docs/contratos/contrato_popup.md`;
- `docs/nomenclatura/32_CONSOLE.md`;
- `docs/contratos/contrato_console.md`.

Não foram explorados outros relatórios históricos.

## Resultado por critério

| Critério | Resultado | Evidência semântica |
|---|---|---|
| 1. Nomenclatura de estilo | **CONFORME** | `10_ESTILO.md` §4.8 separa configuração persistida, materialização global vigente, candidato e override; registra materialização inicial, unicidade global, substituição controlada após persistência e falha sem publicação. A validação, materialização integral e proibição de hardcode permanecem vigentes. |
| 2. Contrato de estilo | **CONFORME** | `contrato_estilo.md` §3.8 e R-4/R-10/R-11/R-12 ajustam a imutabilidade anterior, fecham as quatro camadas, a ordem persistência → publicação, a atomicidade observável pelos consumidores, a preservação em falha e o escopo dos quatro `preset_default`; nenhum mecanismo físico de escrita foi imposto. |
| 3. Artefatos e runtime | **CONFORME** | `02_ARTEFATOS_CONFIGURACAO_E_RUNTIME.md` §4.5 classifica candidato e override como runtime e mantém `config/estilo.json` como configuração concreta, sem estado vivo persistido; o comportamento remete ao contrato de estilo. |
| 4. Barra de menus | **CONFORME** | Os únicos acréscimos de integração são F4, `Enter/Aplicar` contextual por divergência da baseline e suspensão modal da barra subjacente. Não foram antecipados F1, F11, F2/F3/F5 nem ajuda declarativa dos chips. |
| 5. Pop-up | **CONFORME** | `35_POPUP.md` §6.1 e `contrato_popup.md` §9.1 reutilizam o pop-up genérico com conteúdo `texto`, override local do chamador, retorno somente `CONFIRMADO`/`ABORTADO` e sem persistência, publicação ou lógica de negócio. |
| 6. Console preservado | **CONFORME** | Os dois documentos de console não possuem diff. A política `dois_niveis_por_foco` já cobre pais, filhos, escolha exclusiva por pai, Espaço e independência entre cursor e escolha; não houve redesign nem lacuna criada para o ITEM-0010. |
| 7. Coerência ponta a ponta | **REPROVADO** | Há materialização inicial, candidato, override, decisão modal, persistência antes da publicação e fail-closed. Porém, a aplicação não materializa integralmente duas transições exigidas pela ADR: (a) `ABORTADO` preserva o candidato e retorna à seleção; (b) após sucesso, candidato e baseline persistida ficam equivalentes e `Enter/Aplicar` fica inativo. |
| 8. Escopo | **CONFORME** | O diff da aplicação não incorpora tiling por tela, tecla `|`, F1/Ajuda, F11, mapa F2/F3/F5, `cor_inativo`, `cor_alerta`, `indicadores.concluido`, ajuda declarativa, novo pop-up ou nova política de navegação. |
| 9. Diffs e preservações | **CONFORME** | Somente os sete documentos normativos da aplicação têm alterações; console, configuração e código permanecem sem alteração. O backlog, ADR e relatórios já estavam no worktree e foram preservados; nenhum handoff foi criado por este QA. |

## Não conformidades materiais

### NC-01 — `ABORTADO` não preserva normativamente o candidato

`contrato_popup.md` §9.1 registra o status `ABORTADO`, o override local e a
ausência de lógica de negócio, mas não define que, no consumidor de estilo,
esse resultado encerra a demonstração, retorna à seleção e preserva
integralmente o candidato. O contrato genérico apenas diz que alterações da
instância são provisórias até confirmação (`contrato_popup.md` §9), o que não
fecha a transição normativa específica exigida pela ADR-0046.

### NC-02 — Sucesso não equaliza candidato e baseline

`contrato_estilo.md` §3.8 e R-11 fecham persistência completa antes da
publicação e preservam os estados anteriores em falha, mas não registram a
transição pós-sucesso que torna a configuração aplicada a nova baseline,
equaliza candidato e baseline e desativa `Enter/Aplicar`. A regra da barra
(`contrato_barra_de_menus.md` §10.1/R-13) somente define a condição de
ativação por divergência; sem a equalização normativa, o fluxo não fecha a
consequência obrigatória da confirmação bem-sucedida.

As duas lacunas são semânticas e atingem o critério 7; não são diferenças
editoriais. A aplicação documental, portanto, não materializou integralmente
a ADR-0046.

## Conclusão terminal

`ADR_APPLICATION_REJECTED`

Nenhuma correção foi realizada nesta etapa. O único artefato materializado pelo
QA é este relatório obrigatório.
