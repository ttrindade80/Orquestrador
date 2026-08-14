# Relatório QA — Handoff H-0063

```yaml
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0063
  artefato_auditado: docs/handoff/H-0063-tela-estilo-estrutura-navegacao-dois-niveis.md
  papel: auditor_independente_handoff_substituto
  contexto: LIMPO

resultado:
  status: H2_HANDOFF_PATCH_REQUIRED
  verificacoes_executadas:
    - leitura integral de H-0063
    - leitura focal de contrato_console.md §22.16–22.18
    - leitura focal de contrato_barra_de_menus.md §§7–9 e 8.2/8.2.1
    - leitura focal de contrato_json_console.md §7.1 e campos obrigatórios
    - leitura focal de H-0055 (política canônica) e fixture h0055_dois_niveis_por_foco.json
    - confirmação de API vigente carregar_configuracao_estilo / projeção de presets
    - confirmação documental da substituição H-0062→H-0063 já aprovada
  achados:
    - id: H0063-QA-001
      requisito_violado: >-
        Reutilizar literalmente politica_navegacao.tipo: dois_niveis_por_foco
        (contrato_console.md §22.16; H-0055), inclusive Espaço nos filhos e
        seleção exclusiva obrigatória de filho por pai, sem criar política
        paralela.
      evidencia_focal: >-
        H-0063 §5 exige reutilizar literalmente dois_niveis_por_foco e descreve
        Espaço somente sobre pai (“entrar/expor o toroide dos filhos”); no
        nível dos filhos afirma “setas somente movem o cursor; não há escolha
        de preset”. §4.4 diz que H-0063 “não implementa Espaço escolhendo
        preset”. O contrato §22.16 exige Espaço sobre filho transferindo a
        escolha exclusiva, distinta do cursor; Esc preserva o filho escolhido.
        H-0055 fecha o mesmo mecanismo e declara politica_selecao: multipla
        apenas como compatibilidade declarativa do chip/Espaço.
      impacto: >-
        O implementador não consegue obedecer simultaneamente “reutilizar
        literalmente” e omitir/neutralizar Espaço nos filhos. O risco é criar
        variante ad hoc da política, ou acoplar indevidamente a escolha
        canônica à mutação de estilo/candidato — exatamente a fronteira que
        H-0063 pretende isolar.
      correcao_necessaria: >-
        Separar explicitamente (a) filho escolhido da política canônica —
        inicializado a partir de preset_default, transferido por Espaço nos
        filhos, preservado no Esc de retorno, sem chamar mutação de
        candidato/preset_default/estilo global — de (b) mutação de estilo,
        candidata a handoff posterior. Exigir politica_selecao: multipla no
        shell apenas como compatibilidade declarativa vigente (como H-0055/
        H-0062), sem reabrir seleção múltipla genérica. Corrigir o vocabulário
        que confunde “filho corrente” (cursor) com “filho escolhido”.
    - id: H0063-QA-002
      requisito_violado: >-
        Barra de Menus deve usar identidades/rótulos canônicos de chips
        (contrato_barra_de_menus.md §§7–8; fixture H-0055), sem inventar
        semântica própria para [␣].
      evidencia_focal: >-
        H-0063 §6.3 declara a sequência
        “[Esc] Sair/Voltar → [✥] Navegar → [␣] entrada no nível → [?] Ajuda”.
        O rótulo “entrada no nível” não é identidade canônica; em
        dois_niveis_por_foco a tecla Espaço cobre entrada nos filhos e
        transferência da escolha exclusiva, e a fixture H-0055 materializa o
        chip com texto “Selecionar” (rótulo dinâmico do mecanismo vigente).
        O handoff também não fecha o rótulo dinâmico de [Esc] no toroide de
        filhos (“Retornar aos pais”), já normatizado no contrato §9.
      impacto: >-
        A implementação pode declarar chip com texto/semântica inventados,
        desalinhados do renderer e dos testes da política vigente, e omitir a
        cobertura de Espaço no nível dos filhos.
      correcao_necessaria: >-
        Substituir “[␣] entrada no nível” pela identidade canônica do chip
        Espaço já usada por dois_niveis_por_foco (compatível com H-0055),
        cobrindo entrada e escolha exclusiva observacional; explicitar
        [Esc] com rótulos dinâmicos Sair/Voltar vs Retornar aos pais; manter
        [?] Ajuda obrigatório, sempre ativo e último.
  bloqueios: []
```

## Síntese

H-0063 está coeso no objetivo estrutural (tela normal + dois níveis + resize),
delimita corretamente a ausência de aplicação/mutação de estilo, autoriza
arquivos nominais suficientes, aponta testes/demonstração/TTY e não reabre
popup/Aplicar. A substituição documental H-0062→H-0063 está pré-aprovada e
fora do escopo deste QA.

O handoff **não** está aprovado para `IMPLEMENTAR`: a fronteira “política
canônica literal × sem escolha” permanece contraditória e a Barra inventa
rótulo/semântica de `[␣]`. Corrigir somente o handoff (`PATCH_HANDOFF`) antes
de novo `QA_HANDOFF`.

## Git (somente leitura)

```yaml
branch: master
HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
stage: vazio
```

Nenhuma alteração de implementação, patch de handoff, stage, commit ou push
foi executada nesta etapa.
