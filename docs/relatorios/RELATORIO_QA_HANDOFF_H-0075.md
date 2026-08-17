# Relatório de QA do handoff H-0075

item: ITEM-0026
adr: ADR-0048
handoff: H-0075

regra_multiplos_consoles:
  classificacao: DECISAO_NOVA_NAO_AUTORIZADA
  evidencia: >-
    H-0074 confirma que os três consoles H-0072 compartilham o mesmo
    ConteudoExterno, mas mantêm selecoes por console. A ADR-0048 e o contrato
    §26 definem baseline/candidato por pai, sem precedência entre candidatos
    de consoles. A lista_foco é ordenada por travessia e declaração para
    navegação (contrato_console §22.2; nomenclatura 32 §4.5), não para vencer
    conflitos de escolha. H-0075 §4.8, contudo, manda persistir o primeiro
    console divergente e fixa console_h0072_texto como primeiro.

transporte_caminho:
  caminho_origem: >-
    Aceitável como detalhe runtime: o modelo atual preserva _raw, mas o
    loader descarta o caminho calculado. Transportar o Path não altera o
    schema JSON, não conflita com a fronteira loader/persistência e, congelado
    no snapshot, é suficiente para escrever o documento efetivamente carregado.
  override_estado: >-
    Não há padrão equivalente nos arquivos autorizados. É justificável como
    mecanismo isolado de cópia/teste/demonstração, desde que o override seja
    aplicado somente na carga, tenha a precedência canônica já descrita e o
    caminho efetivo seja congelado em caminho_origem; a persistência não deve
    reler esse slot. Assim não há segunda autoridade concorrente.

popup_estrutural:
  classificacao: DERIVADA_DE_AUTORIDADE_EXISTENTE
  evidencia: >-
    contrato_popup §3.1 exige popups[ID] no JSON estrutural e popup.py já
    valida tipo texto, chips Voltar/Confirmar e resultados ABORTADO/CONFIRMADO.
    Cada tela precisa declarar a entrada porque a resolução usa o modelo da
    tela aberta. O ID proposto e o envelope tipo texto não criam schema ou
    sistema novo.

## Achado QA-H0075-001

- requisito: o handoff deve fechar qual candidato persiste quando múltiplos
  consoles compartilham o mesmo pai/documento, sem deixar decisão ao
  implementador; `filho_default` continua a única autoridade persistida.
- evidência focal: H-0074 §8.3 registra três consoles H-0072 compartilhando
  um documento e H-0075 §4.8 declara escolhas separadas por console, mas
  escolhe o primeiro divergente da `lista_foco`, inclusive quando os valores
  divergem. Nenhuma regra equivalente existe na ADR-0048, no contrato ou na
  nomenclatura; a ordem vigente só governa foco/navegação.
- impacto: dois consoles podem produzir candidatos diferentes para o mesmo
  pai; a escrita depende de uma política nova não autorizada. O item 25 dos
  26 testes cobre H-0072, mas não prova o caso conflitante.
- correção necessária: fechar essa autoridade em documento normativo ou
  retirar a precedência do handoff e registrar a regra executiva autorizada.
  Acrescentar teste obrigatório que crie divergências distintas no mesmo pai
  em consoles compartilhados e verifique a regra então autorizada. O QA não
  escolhe o vencedor.

## Verificações de escopo

H-0075 não reimplementa H-0074, não cria schema público, não antecipa
ITEM-0023/0024, não altera apresentação/navegação geral nem publica Estilo.
Snapshot frozen com deepcopy, escrita preservadora em `_raw`, validação antes
de um único tempfile/os.replace, estados ABORTADO/CONFIRMADO/falha e promoção
da baseline estão fechados. A interceptação de Enter é restrita às telas
aplicáveis e preserva o fluxo de Estilo; os arquivos futuros listados são
materialmente justificáveis, e popup.py/estilo.py podem permanecer inalterados.
Os testes e a demonstração usam cópias temporárias e cobrem os demais
requisitos, ressalvada a lacuna do conflito acima.

status: H2_HANDOFF_PATCH_REQUIRED
