# QA_IMPLEMENTACAO — H-0055

status: I2_IMPLEMENTATION_PATCH_REQUIRED

## Verificações

- Handoff, relatório de implementação, arquivos nominais, diff focal e buscas autorizadas foram auditados integralmente.
- O comando focal obrigatório foi tentado, mas o pytest não iniciou por falta de diretório temporário gravável no ambiente. Com captura em memória (`--capture=sys`), o resultado foi `92 passed`.
- A suíte canônica obrigatória também não iniciou pelo mesmo bloqueio ambiental. A tentativa com `--capture=sys` não produziu resultado canônico limpo: `923 passed`, `87 failed` e `86 errors`, com falhas/erros contaminados pelo uso de temporários e pela restrição de escrita do ambiente.
- O smoke não interativo obrigatório terminou com código 0 e exibiu H-0055, escolhas iniciais, `[PgUp][PgDn] Páginas` e a primeira de duas páginas.
- A implementação foi auditada semanticamente quanto à política explícita, dois níveis, toroides, entrada/retorno, escolha obrigatória por pai, cursor independente, compatibilidade declarativa de `politica_selecao`, preservações, D23, paginação, carregamento focal e runtime somente leitura.

## Estado semântico e achado material

Os testes focais e a inspeção dos arquivos nominais confirmam a materialização dos comportamentos H-0055, fixtures com 25 itens lógicos, cinco pais e quatro filhos diretos por pai, duas páginas, D23 iniciado em `nao_verboso`, escolhas iniciais derivadas do primeiro filho e ausência de persistência no JSON. A interação TTY real não foi executada.

Há, porém, um achado novo no desvio focal de `tela/carregamento/envelope_pre_adr_0028.py`: a combinação nominal H-0055/D23 é aceita antes da validação estrita dos campos de envelope. A classificação nominal válida retornou `True`, mas a mesma combinação com `politica_exibicao: []` também retornou `True`. A exceção não é fechada para variações inválidas de campo conhecido e pode enfraquecer rejeições existentes.

Impacto: o carregador não atende integralmente ao requisito de aceitar somente a combinação H-0055/D23 autorizada. Requer patch focal do carregador; nenhuma correção foi aplicada nesta etapa e PATCH_IMPLEMENTACAO não foi iniciado.

## Pendências

- A confirmação da suíte canônica permanece pendente até haver ambiente com temporário gravável.
- Requer validação manual em TTY real do percurso, Esc, foco, geometria, chips, modo e paginação visual/interativa.
