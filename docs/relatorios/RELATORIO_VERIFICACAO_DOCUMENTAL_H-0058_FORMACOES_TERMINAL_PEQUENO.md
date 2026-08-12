# Verificação documental — H-0058: formações e terminal pequeno

## Contexto

Verificação documental factual focal sobre a relação entre as formações do
pop-up de marcação e o quadro de terminal pequeno. Este relatório materializa
uma conclusão já apurada, sem propor correção ou alteração de implementação.

## DOC-H0058-01 — Ordem normativa

As autoridades vigentes definem separadamente:

- a ordem das formações: `coluna → matriz → linha`;
- o cálculo geométrico do pop-up;
- a entrada no quadro de terminal pequeno quando a representação completa não
  couber.

Não definem explicitamente a precedência entre tentar a próxima formação e
acionar o quadro de terminal pequeno.

Resultado: `AMBIGUIDADE_DOCUMENTAL`.

## DOC-H0058-02 — Alcançabilidade

Não há regra documental suficiente para provar necessariamente:

- faixa dimensional em que coluna não cabe e matriz cabe;
- faixa dimensional em que coluna e matriz não cabem e linha cabe;
- que essas formações sejam tentadas antes do gate de terminal pequeno.

Resultado: `NAO_CONFIRMADO_PELA_DOCUMENTACAO`.

## DOC-H0058-03 — Demonstração obrigatória

H-0058 exige deterministicamente que `coluna`, `matriz` e `linha` existam e
sejam testadas. A demonstração em TTY exige navegação, resize, recomposição,
preservação de estado e retorno por `Esc`.

A documentação não exige explicitamente que uma única sessão TTY atravesse
obrigatoriamente as três formações por resize.

## DOC-H0058-04 — Contradição ou ambiguidade

Não foi encontrada contradição textual direta entre H-0057 e H-0058.

Existe, porém, uma lacuna material sobre a precedência entre a tentativa de
`coluna → matriz → linha` e o acionamento do quadro de terminal pequeno.

Classificação: `AMBIGUIDADE_DOCUMENTAL`.

## DOC-H0058-05 — Camada responsável

A evidência disponível não demonstra necessidade de alterar a ADR-0044 nem o
contrato antes de decidir o tratamento do critério manual.

A camada mínima relacionada à exigência excessiva introduzida na condução da
validação é o próprio H-0058, caso seja necessário reconciliar explicitamente
o texto de demonstração/aceite com a autoridade superior.

Registro: `HANDOFF_H0058`.

Nenhuma correção é aplicada nesta execução.

## Conclusão

1. As autoridades vigentes garantem as três formações como comportamento do
   componente.
2. Os testes determinísticos devem cobri-las.
3. Não está documentalmente comprovado que todas devam ser observáveis em uma
   mesma sessão TTY por resize antes do quadro de terminal pequeno.
4. A falha manual anterior não prova defeito do runtime apenas pela ausência
   visual de matriz/linha.
5. Existe ambiguidade documental sobre a precedência entre tentativa de
   formação e terminal pequeno.
6. Nenhuma alteração de implementação deve ser feita com base apenas nessa
   evidência.
7. Eventual reconciliação documental deve ocorrer primeiro na camada
   `HANDOFF_H0058`.
