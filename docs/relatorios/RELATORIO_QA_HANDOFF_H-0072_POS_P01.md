# RELATORIO_QA_HANDOFF_H-0072_POS_P01

```yaml
etapa: QA_HANDOFF
objeto: H-0072
patch_auditado: P01
cadeia_raiz: docs/handoff/H-0072-formatacao-generica-filhos-dois-niveis-por-foco.md
predecessor_imediato: docs/relatorios/RELATORIO_PATCH_HANDOFF_H-0072_P01.md
status: H1_HANDOFF_APPROVED
achados_materiais: nenhum
```

## Resultado

P01 é suficiente e executável. O handoff fecha `designador` como objeto
fechado: `tipo` obrigatório e restrito a `decimal_composto`,
`alfabetico_maiusculo` ou `nenhum`; `prefixo`/`sufixo` opcionais string, com
ausência equivalente a vazio nos tipos visuais; resultado
`prefixo + designador_base + sufixo`; e `nenhum` sem visual nem adornos.
Chaves desconhecidas são inválidas. Não introduz herança, `fonte`, `herdar`,
parsing externo ou política de navegação.

O menor delta nominal está materialmente correto. O defeito causal permanece
em `_validar_designador_filho`, hoje fechado somente em `tipo`; portanto o
loader é o único código a alterar. `tela/modelo.py` transporta integralmente o
dict `filho`; `conteudo_externo.py` passa `designador_cfg` integral a
`_texto_designador`; e `designadores.py` já implementa
prefixo+nucleo+sufixo e vazio para `nenhum`. Modelo, renderer, navegação,
seleção e demais arquivos declarados preservados não exigem mudança.

A fixture estrutural H-0072 pode acrescentar `"("`/`")"` somente ao console
tabular alfabético, produzindo `(A)`/`(B)`, sem perder caráter genérico. O
conteúdo externo permanece inalterado; decimal composto sem adornos e
`nenhum` sem adornos são preservados.

V-DNF-12..16 cobrem tipos inválidos dos adornos, chave desconhecida e
`nenhum` com cada adorno; V-DNF-01..11 permanecem. Os 15 testes adicionais
exigem adornos isolados/combinados, bases alfabética/decimal, cinco rejeições,
ausência/retrocompatibilidade e preservação de navegação, seleção,
texto/tabela, sem substituir a regressão original de 18 casos.

H-0055 aparece somente como capacidade `alfabetico_maiusculo + ")" -> A)`;
sua configuração não integra o patch. H-0073 permanece integralmente fora do
escopo e condicionado à sequência de QA e implementação declarada. O relatório
futuro tem nome próprio e não sobrescreve o histórico original.
\n