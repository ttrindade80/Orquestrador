# Relatório QA — Handoff H-0064

```yaml
rastreabilidade:
  etapa: QA_HANDOFF
  objeto: H-0064
  item: ITEM-0010
  adr: ADR-0046
  artefato_auditado: docs/handoff/H-0064-amostras-visuais-presets-estilo.md
  predecessor: H-0063
  papel: auditor_documental_independente
  contexto: LIMPO

resultado:
  status: H2_HANDOFF_PATCH_REQUIRED
  verificacoes_executadas:
    - leitura integral de H-0064 e do relatório de criação do handoff
    - leitura integral da ADR-0046, com foco na seção 2
    - leitura de H-0063 e da classificação final da validação manual do predecessor
    - leitura focal de contrato_estilo.md §§3.1–3.3 e regras R-2, R-6, R-7
    - leitura focal de nomenclatura/10_ESTILO.md §§4.2–4.4
    - leitura focal de contrato_console.md §§13.5–13.6 e 22.16–22.17
    - leitura focal de contrato_barra_de_menus.md §§4.3, 8.2.1 e 8.3
    - leitura focal de H-0055 §3.3 e da fixture estrutural H-0063
    - inspeção somente leitura do caminho atual de projeção/renderização e ANSI
    - conferência somente leitura do estado Git e do stage
  achados:
    - id: H0064-QA-001
      natureza: contradicao_documental
      requisito_violado: >-
        Preservar a Barra vigente de H-0063 e, simultaneamente, preservar a
        paginação canônica do Console com politica_paginacao: com.
      evidencia_focal: >-
        H-0064 §13 (linhas 191–194) enumera somente [Esc], [✥], [␣] e [?].
        A fixture H-0063 declara politica_paginacao: com e o chip
        [PgUp][PgDn] Páginas (linhas 37 e 59–64 do JSON). H-0064 §12 e os
        critérios 10–11 exigem que paginação continue funcionando. H-0055
        §3.3 e contrato_console §22.17 tornam PageUp/PageDown e a
        representação [PgUp][PgDn] parte da política vigente.
      impacto: >-
        O implementador pode remover o chip de paginação para obedecer à
        sequência literal de §13, quebrando a capacidade herdada, ou pode
        mantê-lo e deixar a especificação literal sem atendimento. O handoff
        não fecha qual comportamento é aceito.
      correcao_necessaria: >-
        Corrigir §13 para explicitar a Barra efetivamente preservada por H-0063,
        incluindo [PgUp][PgDn] Páginas na posição declarada pela fixture, e
        afirmar que não há chip novo nem reordenação introduzida por H-0064.

    - id: H0064-QA-002
      natureza: requisito_visual_subespecificado
      requisito_violado: >-
        A amostra de chip deve consumir cor_texto, cor_fundo e caixa_alta e
        distinguir visualmente presets que diferem somente por cor.
      evidencia_focal: >-
        H-0064 §7 (linhas 114–129) exige os cinco campos, mas não define o
        conteúdo textual interno sobre o qual caixa_alta e as cores serão
        aplicadas. No catálogo atual, Destaque Texto e Destaque Fundo usam
        caractere_esquerdo e caractere_direito iguais a espaço e diferem
        somente em cor_texto/cor_fundo (config/estilo.json, linhas 82–94).
        Uma amostra formada apenas pelos delimitadores não expõe nenhum desses
        campos. Um texto fixo escolhido para preencher o chip pode violar a
        proibição de hardcode de §5.
      impacto: >-
        A implementação pode produzir duas amostras indistinguíveis, não
        demonstrar caixa_alta, ou introduzir um literal/mapa especial para
        obter um payload visual. O teste de diferença ANSI previsto não fecha
        por si só qual texto recebe foreground/background nem como a
        capitalização é observada.
      correcao_necessaria: >-
        Fechar no handoff a origem dinâmica do payload interno da amostra e a
        aplicação dos campos: onde cor_texto e cor_fundo incidem, em que texto
        caixa_alta atua e como o reset de ANSI evita vazamento. Acrescentar
        aceite/teste específico para caixa_alta e para diferenças de
        foreground/background usando payload sem literal de preset.

    - id: H0064-QA-003
      natureza: lacuna_de_autorizacao_e_composicao
      requisito_violado: >-
        A amostra deve passar pelo Console normal, preservar item lógico,
        suportar largura/resize/paginação e, quando visualmente colorida, ter
        largura física coerente sem criar renderer paralelo.
      evidencia_focal: >-
        H-0064 §§6, 10, 12 e 15 exigem miniatura de borda, composição normal,
        wrapping/expansão, resize e largura coerente, mas autorizam apenas a
        adaptação em tela/renderizacao/estilo.py, integração focal na fachada
        e ajustes mínimos de contexto/fixture. No estado predecessor,
        tela/renderizacao/estilo.py apenas associa ConteudoExterno ao Console;
        a composição hierárquica é feita por
        tela/renderizacao/conteudo_externo.py. O Console H-0063 está em modo
        não verboso, no qual o contrato exige uma linha física por nó e
        proíbe configuração de múltiplas linhas. Além disso, o caminho atual
        de truncamento conta len() sobre texto bruto, enquanto a largura ANSI
        é tratada por helpers separados em tela/renderizacao/texto_ansi.py.
      impacto: >-
        Sem uma extensão nominal do renderer normal ou uma representação
        explicitamente limitada ao contrato de uma linha, o implementador não
        consegue garantir simultaneamente miniatura, cores ANSI, largura,
        paginação e ausência de resíduo. Alterar um módulo não autorizado ou
        embutir ANSI em titulo sem ajuste de largura pode quebrar o quadro e o
        mapa físico dos itens.
      correcao_necessaria: >-
        Fechar a estratégia antes da implementação: ou especificar uma
        representação de amostra de uma linha compatível com o modo não
        verboso e um ponto de integração ANSI já existente, ou autorizar e
        delimitar a extensão mínima do renderer normal de conteúdo (incluindo
        contagem/truncamento ANSI e preservação de uma identidade lógica por
        filho). Não autorizar renderer paralelo nem alteração da política de
        navegação.
  bloqueios: []
```

## Síntese

H-0064 está bem delimitado quanto a categorias, origem dinâmica dos presets,
fronteira observacional, ausência de candidato/Aplicar/demonstração/popup,
e preservação de H-0063. A ausência de implementação H-0064, de testes
dedicados e de `IMP-0064` não é achado nesta etapa: são saídas posteriores de
`IMPLEMENTAR`.

O handoff, porém, não deve seguir para implementação no estado atual. É
necessário corrigir a sequência documental da Barra, fechar o payload e a
semântica visual da amostra de chip e tornar explícito o ponto de composição
ANSI/geométrica no renderer normal. O status aplicável é
`H2_HANDOFF_PATCH_REQUIRED`.

## Estado Git — somente leitura

```yaml
branch: master
HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
stage: vazio
config/estilo.json: sem delta
observacao: >-
  Há alterações não staged e artefatos não rastreados de etapas paralelas no
  worktree; foram preservados e não atribuídos a este QA.
acoes_desta_etapa:
  implementacao: nenhuma
  alteracao_do_handoff: nenhuma
  stage: nenhum
  commit: nenhum
  push: nenhum
```
