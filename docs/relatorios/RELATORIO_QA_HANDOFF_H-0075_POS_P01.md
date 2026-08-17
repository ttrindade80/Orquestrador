# Relatório de QA pós-patch — H-0075 P01

```yaml
cadeia:
  raiz: H-0075
  predecessor_imediato: RELATORIO_PATCH_HANDOFF_H-0075_P01.md

achados_retestados:
  QA-H0075-001:
    resultado: NAO_RESOLVIDO
    evidencia: >-
      A precedência textual por primeiro console/foco foi removida, mas
      mapa_candidato_filho_default continua autorizado a ler de "qualquer"
      console aplicável sem exigir detecção de entradas divergentes. Como
      alternar sem modelo preserva a mutação autônoma por console, uma
      inconsistência ainda pode chegar ao mapa; nesse caso a travessia volta
      a escolher silenciosamente uma entrada. Os testes 26–35 não incluem
      prova fail-closed para esse estado divergente.

compartilhamento_runtime:
  identidade_documento: >-
    Confirmada: _propagar_conteudo_externo atribui a mesma referência a todos
    os consoles; não há cópia intermediária, e `is` separa objetos distintos.
  identidade_pai: >-
    Confirmada no conteúdo compartilhado: todos observam os mesmos NoConteudo;
    a validação torna os IDs inequívocos no documento.
  propagacao: >-
    Materialmente insegura como especificada: o destino exige somente presença
    em lista_foco e identidade de ConteudoExterno. Como o modelo propaga o
    conteúdo a todo console, um console focalizável com política diferente de
    dois_niveis_por_foco também receberia a lista exclusiva por pai, sobrescrevendo
    estado de seleção com outra semântica. H-0072 é homogêneo e não manifesta o
    defeito, mas a detecção estrutural declarada pelo handoff não o exclui.
  independencia_lista_foco: >-
    Não demonstrada sob inconsistência: sem rejeição explícita, a escolha de
    "qualquer console" depende do console consultado pela travessia.

novos_achados:
  - id: QA-H0075-002
    severidade: MATERIAL
    descricao: >-
      A propagação por identidade de documento não restringe os consoles de
      destino à mesma política aplicável, podendo contaminar estado de console
      indevido. O handoff deve fechar o predicado de destino e acrescentar teste
      executável negativo; não cabe ao implementador decidir essa regra.

escopo_preservado: >-
  caminho_origem, override runtime, popup, Enter/Aplicar, snapshot frozen,
  persistência fail-closed, schema público, fronteira H-0074 e exclusão de
  ITEM-0023/0024 permanecem preservados. A lista futura de arquivos continua
  suficiente; não é necessário autorizar arquivo novo.

status: H2_HANDOFF_PATCH_REQUIRED
```
