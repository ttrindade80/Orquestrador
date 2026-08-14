# Relatório — PATCH_HANDOFF H-0063 P01

```yaml
rastreabilidade:
  etapa: PATCH_HANDOFF
  objeto: H-0063
  patch: P01
  artefato_principal:
    docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  achados_tratados:
    - H0063-QA-001
    - H0063-QA-002

execucao:
  status: HANDOFF_PATCHED
  arquivos_alterados:
    - docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  arquivos_criados:
    - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0063_P01.md

resultado:
  delta_material:
    - "§4.4 reescrita: distingue estado navegacional canônico (pai corrente,
       filho corrente, filho escolhido por pai) de mutação de estilo
       (candidato, preset_default persistido, estilo global, publicação);
       fixa que a escolha de filho pertence ao primeiro plano e não executa
       o segundo."
    - "§5 reescrita: adiciona vocabulário formal filho corrente × filho
       escolhido; especifica que Espaço sobre filho transfere a escolha
       exclusiva sem alterar preset/candidato/estilo global; fecha rótulo
       contextual de Esc em cada nível ([Esc] Retornar aos pais nos filhos;
       dynamic Esc §9 nos pais)."
    - "§6.2 (Console): acrescenta politica_selecao: multipla como
       compatibilidade declarativa do mecanismo dois_niveis_por_foco, com
       ressalva explícita de que não reabre seleção múltipla genérica nem
       autoriza múltiplas escolhas por pai."
    - "§6.3 (Barra de Menus): substitui o chip inventado [␣] entrada no
       nível por [␣] Selecionar (identidade canônica de H-0055); fecha Esc
       contextual nos dois níveis; explicita que o mesmo Espaço cobre
       entrada no nível de filhos e transferência de escolha, sem chips
       concorrentes."
    - "§9 (Fora de escopo): adiciona nota de que a escolha exclusiva de
       filho não é 'Espaço escolhendo preset' e não está fora de escopo."
    - "§8 (Resize): bullet de reconciliação passa a citar explicitamente
       pai corrente, filho corrente e filho escolhido."
    - "§13 (Testes): subseção 'Navegação e fronteira de estado' reescrita
       com blocos de estado inicial, cursor, Espaço, Esc e barra, conforme
       achados."
    - "§14 (Demonstração): passos 4-5 reescritos para observar filho
       corrente, Espaço transferindo escolha e Esc preservando-a."
    - "§16 (Critérios de aceite): bullets acrescidos sobre distinção
       corrente/escolhido, Espaço/Esc e reconciliação em resize."
  verificacoes_executadas:
    - "rg -n sobre o arquivo patchado confirmando presença consistente de
       filho corrente, filho escolhido, Espaço, Selecionar, Retornar aos
       pais e Ajuda; confirmando que 'entrada no nível' só ocorre em duas
       menções negadas (registrando a remoção do rótulo inventado)."
    - "git status/git log no arquivo: H-0063 é artefato ainda não rastreado
       pelo git (criado nesta mesma linha de trabalho, nunca commitado);
       'git diff' não produz saída porque não há baseline em HEAD/index —
       não é um bloqueio, é decorrência do estado do repositório."
  achados_pendentes: []
  bloqueios: []
```

## Registro narrativo

O patch corrigiu exclusivamente H0063-QA-001 e H0063-QA-002, sem tocar em
H-0062, ADRs, contratos, nomenclatura, backlog, código ou testes.

**Distinção corrente × escolhido.** A §4.4 agora separa formalmente dois
planos: (A) estado navegacional canônico — pai corrente, filho corrente,
filho escolhido por pai, reutilizado literalmente de H-0055 e
`contrato_console.md` §§22.11–22.18 — e (B) mutação de estilo — candidato,
`preset_default` persistido, estilo global, publicação. A escolha de filho
pertence a A e nunca aciona B. Essa distinção foi propagada à §5
(vocabulário explícito), aos testes (§13) e aos critérios de aceite (§16).

**Escolha exclusiva observacional.** Ficou fechado que cada pai inicia com
exatamente um filho escolhido, projetado do `preset_default` como leitura
observacional, e que `Espaço` sobre um filho transfere essa escolha
exclusiva internamente ao pai — sem escrever `config/estilo.json`, sem tocar
candidato, sem materializar estilo global e sem publicar. Mover o cursor sem
Espaço nunca transfere a escolha.

**Espaço canônico.** O chip inventado `[␣] entrada no nível` foi removido e
substituído por `[␣] Selecionar`, a identidade já usada pela fixture
`config/telas/demo/h0055_dois_niveis_por_foco.json` (chip `selecionar`,
texto `Selecionar`). Ficou registrado que o mesmo Espaço cobre, conforme o
estado do cursor, tanto a entrada no toroide de filhos quanto a transferência
da escolha exclusiva — sem dois chips concorrentes.

**Esc contextual.** A barra e a §5 agora fecham os dois rótulos: no nível
dos filhos, `[Esc] Retornar aos pais`, preservando a escolha; no nível dos
pais, o rótulo dinâmico definido por `contrato_barra_de_menus.md` §9 (Sair
na tela raiz, Voltar nas demais), sem hardcodar um rótulo ambíguo único.

**Ausência de mutação de estilo.** Todas as seções tocadas reafirmam,
textualmente, que navegação, Espaço, Esc e resize não alteram preset
persistido, candidato, baseline, estilo global ou publicação — a fronteira
de H-0063 permanece exclusivamente estrutural/navegacional.

O objetivo estrutural aprovado pelo QA (tela normal, Cabeçalho, Console,
Barra de Menus, dois níveis, resize, F4, sem popup, sem Aplicar, sem
persistência/publicação) não foi reaberto.
