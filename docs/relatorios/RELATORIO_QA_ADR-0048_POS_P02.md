# Relatório de QA pós-patch — ADR-0048 / P02

```yaml
cadeia:
  raiz: ADR-0048
patch_auditado: P02
origem_material: QA-APP-0048-001
decisao_auditada: D-0026-12
status: ADR_APPROVED
```

D-0026-12 fecha suficientemente o contrato público: o literal é exatamente
`filho_default`, obrigatório em cada pai aplicável, contendo o ID estável de
exatamente um filho direto existente na coleção `filhos` daquele pai. Cada pai
mantém referência própria; não há campo global nem mapa paralelo normativo.
Índice ordinal, primeiro filho e fallback são excluídos. Ausência, referência
inexistente, referência a outro pai e ambiguidade por IDs duplicados tornam o
documento inválido segundo as regras de identidade vigentes.

O valor carregado forma a baseline. Edição runtime altera apenas o candidato;
persistência confirmada e bem-sucedida substitui o `filho_default`; `ABORTADO`
e falha de persistência preservam o valor persistido; nova execução restaura a
escolha a partir dele.

A analogia com `preset_default` é apenas estrutural: coleção local, referência
local, baseline, candidato e atualização após aplicação confirmada. Não atribui
autoridade ao Estilo, não copia schema de aparência e não cria dependência com
`dois_niveis_por_foco`.

D-0026-12 preserva D-0026-01 a D-0026-11 e as fronteiras declaradas, incluindo
`Pai: filho_ativo`, promoção visual, geometria, paginação, navegação, ITEM-0023,
ITEM-0024 e detalhes executivos de escrita. Não há novos achados nem decisão de
schema indispensável antes da reconciliação documental posterior dos contratos.

status_final: ADR_APPROVED
