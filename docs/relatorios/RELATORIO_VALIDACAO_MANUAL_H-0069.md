# Relatório de Validação Manual — H-0069

```yaml
rastreabilidade:
  etapa: VALIDACAO_MANUAL
  objeto: H-0069
  item: ITEM-0010
  adr: ADR-0046
  handoff: docs/handoff/H-0069-demonstracao-integrada-override-local-estilo.md

contexto_tecnico_anterior:
  qa_pos_patch_p01: I1_IMPLEMENTATION_APPROVED

execucao_informada:
  operador: usuário
  ambiente: TTY real
  comando:
    - 'cd "$(git rev-parse --show-toplevel)" || return 1'
    - 'python demo/demo.py'

percurso_factual:
  - usuário estava na tela Estilo
  - alterou o preset de borda
  - acionou Aplicar
  - abriu o popup de confirmação
  - pressionou Enter no popup
  - a confirmação iniciou a aplicação
  - a troca visual da borda chegou a ocorrer
  - imediatamente depois a execução terminou com traceback

observacao_literal_do_usuario: >
  ao aplicar com enter no pop-up a troca da borda

resultado:
  status: MANUAL_VALIDATION_FAILED

natureza:
  - falha_funcional
  - caminho_CONFIRMADO
  - crash_em_runtime

momento_da_falha:
  popup_confirmacao: aberto
  acao_usuario: Enter
  resultado_modal: CONFIRMADO
  observacao: troca visual da borda chegou a ocorrer antes do crash

efeito:
  retorno_normal_a_tela_Estilo: nao_concluido
  validacao_manual_H0069: FALHOU
  restante_do_roteiro_manual: nao_executado_por_interrupcao

traceback_da_execucao: |
  Traceback (most recent call last):
    File "/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/demo/demo.py", line 2912, in <module>
      sys.exit(main())
               ~~~~^^
    File "/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/demo/demo.py", line 2756, in main
      estilo_mudou = _estado_estilo_observavel(estado, modelo) != estilo_antes
                     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
    File "/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/demo/demo.py", line 422, in _estado_estilo_observavel
      em_filhos = navegacao.em_nivel_filhos(estado, console)
    File "/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/tela/navegacao.py", line 646, in em_nivel_filhos
      for _indice_pai, _pai, filhos in _indices_dois_niveis(console)
                                       ~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
    File "/home/tiago/Dropbox/UFRGS/Survey/versao_0_2/orquestrador/tela/navegacao.py", line 607, in _indices_dois_niveis
      for pai in elemento.conteudo_externo.nos:
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'nos'

fatos_tecnicos_comprovados_pelo_traceback:
  - demo/demo.py::_estado_estilo_observavel(estado, modelo) foi executado
  - essa função chamou navegacao.em_nivel_filhos
  - _indices_dois_niveis(console) tentou acessar elemento.conteudo_externo.nos
  - naquele momento elemento.conteudo_externo era None
  - ocorreu AttributeError

nao_declarado_como_fato:
  - qual modelo estava incorreto
  - que navegacao.py é a causa do defeito
  - que a origem da demonstração foi perdida
  - qual arquivo precisa ser corrigido

hipotese_para_investigacao:
  status: NAO_CONFIRMADA
  descricao: >
    Após CONFIRMADO, a avaliação pós-evento pode estar recebendo um modelo
    incompatível com a premissa de navegação em dois níveis usada por
    _estado_estilo_observavel.

gates:
  validacao_manual_H0069:
    status: MANUAL_VALIDATION_FAILED
  validacao_manual_final_ITEM_0010:
    status: NAO_INICIADA
    bloqueada_por: falha_funcional_H0069

nao_avaliado_nesta_execucao:
  - refinamentos visuais de chips

proxima_acao: PATCH_IMPLEMENTACAO_H0069_P02

nao_executado_nesta_etapa:
  - nova validação manual
  - testes automatizados
  - diagnóstico técnico
  - patch ou alteração de código
  - alteração de handoff, ADR, contratos, nomenclatura, backlog ou configuração
```

Registro documental da validação manual H-0069 executada pelo usuário em TTY
real com `python demo/demo.py`. O percurso chegou à tela Estilo, alteração do
preset de borda, Aplicar, popup de confirmação e Enter; o resultado modal foi
`CONFIRMADO` e a troca visual da borda chegou a ocorrer. Imediatamente depois
a execução terminou com `AttributeError: 'NoneType' object has no attribute
'nos'` em `_indices_dois_niveis`, após `_estado_estilo_observavel` chamar
`navegacao.em_nivel_filhos`. O retorno normal à tela Estilo não foi concluído.
O restante do roteiro manual, inclusive os refinamentos visuais de chips, não
foi executado por interrupção. Resultado: `MANUAL_VALIDATION_FAILED`. Próxima
ação: `PATCH_IMPLEMENTACAO_H0069_P02`.
