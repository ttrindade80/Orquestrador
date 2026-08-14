---
name: REL-QA-H0065-P01-vinculacao-candidato-estilo
description: "Auditoria documental independente do handoff H-0065 após P01"
metadata:
  type: relatorio_qa
  etapa_qa: QA_HANDOFF
  camada_auditada: HANDOFF
  status: H2_HANDOFF_PATCH_REQUIRED
  data: 2026-08-12
rastreabilidade:
  cadeia_raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
  predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P01.md
  handoff_origem: docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
  achados_tratados:
    - QA-H0065-001
    - QA-H0065-002
    - QA-H0065-003
---

# REL-QA-H0065-P01 — QA pós-patch

## 1. Identificação e status

```yaml
revisao: H-0065 — reteste documental pós-P01
etapa_qa: QA_HANDOFF
camada_auditada: HANDOFF
status_literal: H2_HANDOFF_PATCH_REQUIRED
status_normalizado: HANDOFF_PATCH_REQUIRED
proxima_categoria: PATCH_HANDOFF
perfil_gerente: GERENTE_DE_ADR_IMPLEMENTACAO
papel: auditor_documental_independente
contexto: LIMPO
```

## 2. Escopo e autoridades materiais

```yaml
objeto_auditado: docs/handoff/H-0065-vinculacao-escolha-candidato-estilo.md
autoridades_materiais:
  - docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
  - docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P01.md
  - docs/adr/ADR-0046-alteracao-aplicacao-estilo-global-runtime.md §§3–4, 7, 9
  - docs/contratos/contrato_estilo.md §3.8 e R-11/R-12
  - docs/handoff/H-0061-infraestrutura-estilo-runtime.md §§6–7
escopo:
  - reteste exclusivo de QA-H0065-001, QA-H0065-002 e QA-H0065-003
  - suficiência documental do protocolo P01 e de sua evidência local
fora_do_escopo:
  - implementação de H-0065
  - execução dos testes futuros de H-0065
  - alteração do handoff, ADR, contrato, código ou configuração
```

## 3. Verificações executadas

```yaml
verificacoes:
  - id: leitura_documental
    comando_ou_metodo: leitura integral do handoff, QA raiz e patch P01; leitura focal das autoridades materiais
    evidencia_focal: §§4.5–4.6, 7, 9, 12, 17 e 19 do H-0065 foram comparadas aos três achados raiz.
    resultado: OK
  - id: QA-H0065-001
    comando_ou_metodo: rastreio das fases A–D, fronteira de commit e caminho de falha
    evidencia_focal: §§7.1–7.2 e 17 fixam cópia → validação/materialização → commit do candidato → projeção; falha preserva o candidato anterior.
    resultado: OK
  - id: QA-H0065-002
    comando_ou_metodo: rastreio da autoridade semântica e de todos os pontos normativos de reconciliação
    evidencia_focal: §§9.1–9.4 fecham candidato como fonte única, mas não incluem a saída efetiva após §4.5/§12.2 entre os pontos de reconciliação.
    resultado: FALHA
  - id: QA-H0065-003
    comando_ou_metodo: rastreio do instante exato de saída e do estado transitório restaurado
    evidencia_focal: §§4.5, 12.2 e 19 fixam `candidato == baseline` imediatamente, mas não fixam o valor/limpeza de `estado["selecoes"]` nesse mesmo instante.
    resultado: FALHA
  - id: integracao_atual
    comando_ou_metodo: inspeção somente leitura do dispatcher atual e da integração F4/Esc
    evidencia_focal: `demo/demo.py:772–783` preserva `selecoes`; `:978–1011` efetiva a saída sem limpá-lo; `:862–874` só remove o console na reabertura F4.
    resultado: OK
  - id: higiene_documental
    comando_ou_metodo: `git diff --check --no-index /dev/null` nos artefatos auditados
    evidencia_focal: sem erro de whitespace; o relatório P01 declara `verificacoes_executadas: []`, portanto sua evidência local é incompleta, embora o reteste independente esteja registrado aqui.
    resultado: INCOMPLETA
```

## 4. Achados

| ID | Severidade | Requisito violado | Evidência focal | Impacto | Correção necessária |
|---|---|---|---|---|---|
| QA-H0065-002 | alto | `selecoes` deve ser projeção determinística e não pode divergir da fonte semântica candidato. | §9.3 enumera abertura, sucesso, falha, redraw e resize, mas não a saída efetiva. §4.5/§12.2 recriam o candidato da baseline e concluem a saída sem reconciliar ou remover a projeção. O fluxo atual carrega `selecoes` até a saída e só a remove na próxima abertura F4. | Pode existir, no estado imediatamente pós-saída, candidato igual à baseline com `selecoes` ainda refletindo a escolha abandonada; isso reabre a divergência que P01 declarou inválida. | No protocolo de saída efetiva, ordenar explicitamente a reconciliação de `selecoes` após `criar_candidato()` ou sua remoção controlada; definir e testar o estado de candidato e projeção no instante da saída, não somente após F4. |
| QA-H0065-003 | alto | Saída sem Aplicar deve descartar imediatamente a tentativa e restaurar o estado transitório da baseline no instante definido. | O reset imediato do candidato está fechado em §§4.5/12.2 e é testado em §19. Porém, o mesmo passo não define `estado["selecoes"]`; a asserção de `selecoes == A` aparece apenas depois da reabertura F4 (§19.757–763). | A garantia documental cobre o candidato, mas não o estado transitório completo; a saída pode deixar cache de seleção da visita abandonada até a reabertura. | Aplicar a mesma decisão de descarte/reconciliação à projeção navegacional e exigir a asserção imediatamente após Esc efetivo. O ajuste é o mesmo do QA-H0065-002. |

`QA-H0065-001` está resolvido: o P01 fecha a ordem candidato primeiro/projeção depois, não altera `selecoes` na preparação e exige retorno somente com os dois estados coerentes (§§7.1–7.2, 17).

## 5. Delta de QA pós-patch

```yaml
raiz: docs/relatorios/RELATORIO_QA_HANDOFF_H-0065.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0065_P01.md
achados_tratados:
  - QA-H0065-001
  - QA-H0065-002
  - QA-H0065-003
achados_resolvidos:
  - QA-H0065-001
achados_pendentes:
  - QA-H0065-002
  - QA-H0065-003
novos_achados: []
```

## 6. Testes, demonstração e validação manual

```yaml
testes_ou_metodos:
  - comando_ou_metodo: auditoria documental e inspeção somente leitura do caminho de estado
    resultado_compacto: não foram executados testes de implementação; H-0065 ainda está em READY_FOR_IMPLEMENTATION.
    prova_semantica: os testes futuros da §19 não substituem o fechamento documental da saída efetiva.
validacao_manual:
  necessaria: nao
  metodo_reproduzivel: null
  resultado: nao_aplicavel
  criterios_pendentes:
    - reconciliação/limpeza de `selecoes` no instante da saída efetiva
```

## 7. Estado Git e itens inesperados

```yaml
estado_git_compacto:
  branch: master
  HEAD: 77bd8bf3772985325bc51a850f7c6d76d61ad573
  staged: []
  unstaged: alteracoes preexistentes em codigo e documentacao, preservadas
  nao_rastreados: artefatos de H-0061–H-0065 e relatorios correlatos; preservados
itens_inesperados:
  - item: worktree diferente de limpo apesar do contexto declarado LIMPO
    origem: NAO_CONFIRMADA
    evidencia: git status --short no início da auditoria mostrou múltiplas alterações e arquivos não rastreados fora do escopo deste relatório.
```

## 8. Conclusão

P01 resolve documentalmente a atomicidade de `Espaço` (`QA-H0065-001`), mas não
fecha o ciclo de vida da projeção `estado["selecoes"]` na saída efetiva. Como
essa lacuna afeta tanto a unicidade semântica (`QA-H0065-002`) quanto a
restauração transitória no instante do `Esc` (`QA-H0065-003`), H-0065 não está
liberado para implementação. O status aplicável é
`H2_HANDOFF_PATCH_REQUIRED`.
