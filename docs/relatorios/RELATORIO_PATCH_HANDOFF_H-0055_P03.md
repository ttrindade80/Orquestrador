# Relatório de patch de handoff — H-0055 P03

```yaml
relatorio: RELATORIO_PATCH_HANDOFF_H-0055_P03
raiz: docs/handoff/H-0055-dois-niveis-por-foco.md
etapa: PATCH_HANDOFF
patch: P03
predecessor_documental: H-0055_P02
predecessor_da_etapa: MANUAL_VALIDATION_FAILED
resultado: HANDOFF_PATCH_APPLIED
achados_tratados:
  - MV-H0055-001
  - MV-H0055-002
implementacao: nao_executada
qa: nao_executado
commit: nao_criado
```

## Delta materializado

- `MV-H0055-001`: o handoff fecha `[Esc] Voltar` no toroide de filhos e
  `[Esc] Sair` no toroide de pais. A mudança acompanha o nível ativo, preserva
  as escolhas e impede que a escolha exclusiva obrigatória acione
  `[Esc] Limpar`.
- `MV-H0055-002`: D23 passa a exigir na fixture H-0055 a política fixa
  `formato.excesso.politica_modo: somente_nao_verboso`, sem
  `formato.excesso.modo_inicial`, tecla `V`, chip de mudança de modo ou teste e
  critério manual de variação de verbosidade.
- `tela/carregamento/envelope_pre_adr_0028.py` foi incluído nominalmente na
  lista futura somente para a reconciliação focal D23 de H-0055: reconhecer a
  combinação fixa válida, preservar validação estrita e manter as rejeições
  vigentes.

## Preservações

- Permanecem inalterados hierarquia, redimensionamento, foco, cursor, escolha
  exclusiva obrigatória por pai, `ec`, `tg`, Espaço, toroides e paginação.
- Esc nos filhos continua retornando aos pais e Esc nos pais continua usando a
  saída vigente; ambas as ações preservam escolhas.
- O primeiro filho direto listado no JSON de dados permanece a escolha inicial
  de cada pai na entrada atual.
- A escolha em runtime não é persistida, o JSON de dados não é reescrito e a
  persistência futura continua pertencendo ao `ITEM-0026`.
- H-0052, H-0053, H-0054, contratos, nomenclaturas, ADRs, código, testes,
  fixtures e relatórios anteriores permanecem sem alteração neste patch.

## Verificações documentais

- O handoff identifica P03, o predecessor `MANUAL_VALIDATION_FAILED` e somente
  os achados `MV-H0055-001` e `MV-H0055-002`.
- Fixture futura, chips, preservações, critérios de aceite, testes,
  demonstração, negativos, exceção focal e bloqueios foram reconciliados com
  as duas decisões do usuário.
- O handoff mantém D23 obrigatório e fecha a combinação fixa
  `somente_nao_verboso` sem campo de modo inicial nem controle de mudança de
  modo.
- O handoff alterado e este relatório nominal P03 existem nos caminhos
  autorizados.

## Bloqueios

- Qualquer necessidade de alterar caminho não listado na seção 5 do handoff é
  bloqueio até autorização focal.
- Ampliar a exceção de `tela/carregamento/envelope_pre_adr_0028.py` além da
  reconciliação D23 de H-0055 é bloqueio.
- Criar campo, schema, enum, persistência, nova geometria, nova paginação,
  variação de verbosidade ou nova semântica de Esc é bloqueio.
- Implementação, QA, validação manual e commit permanecem fora desta etapa.
