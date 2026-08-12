# H-0059 — Confirmação, binding e integração da decisão do pop-up

**Projeto:** Orquestrador
**Atividade:** ITEM-0017 / ADR-0044
**Estado do handoff:** pronto para implementação
**Dependência:** H-0058 concluído no commit `0515986`

## 1. Capacidade coesa

Implementar a última capacidade da decomposição aprovada H-0056..H-0059:

- aceitar a confirmação por `Enter` nas aberturas de marcação que declarem
  regra de confirmação compatível;
- devolver o resultado literal `status: CONFIRMADO`;
- materializar em `valor` o payload lógico das marcações correntes;
- fechar a instância modal somente depois de o resultado ser produzido;
- entregar o resultado ao consumidor demonstrativo pelo binding de runtime;
- manter o pop-up sem ação de negócio: a decisão posterior continua sendo do
  chamador, conforme ADR-0044 e contrato.

Esta etapa não reabre a lista, as formações, o foco, a navegação toroidal, a
marcação ou o resize entregues em H-0056..H-0058.

## 2. Pré-condições da confirmação

As condições normativas são estas:

1. A declaração, o envelope de conteúdo e o contrato de resultado aceito pelo
   chamador devem ter sido validados antes da materialização da instância.
2. A instância deve estar aberta e possuir uma regra de confirmação declarada
   para a tecla física `Enter`. A entrada recebida pelo loop pode ser `\r` ou
   `\n`; ambas representam `Enter` e não devem criar dois resultados.
3. O estado navegável, por si só, não é confirmação: cursor e formação física
   apenas determinam a navegação e a apresentação.
4. O estado marcado é a marcação viva da `PopupInstancia`, por IDs; não é o
   campo `marcados` do envelope copiado nem uma posição física da grade.
5. Para `marcacao: exclusiva`, a condição válida é exatamente um ID marcado,
   pertencente à lista de itens. A confirmação devolve esse ID.
6. Para `marcacao: multipla`, a condição válida admite zero a N IDs marcados,
   todos pertencentes à lista. A lista vazia é válida e também pode ser
   confirmada.
7. Antes de formar `valor`, a implementação deve reconciliar a marcação viva
   por ID e na ordem lógica declarada, preservando a semântica já entregue.
   Não deve corrigir configuração ou envelope, fabricar item, usar índice
   físico ou converter estado inválido em valor confirmado.

Se `Enter` não estiver declarado, ou se a abertura não tiver compatibilidade
de confirmação, a tecla não confirma e a instância permanece aberta. Não se
inventa política para conteúdo textual ou para outro estado não definido pelas
autoridades: os pop-ups textuais demonstrativos continuam sem contrato de
payload confirmado nesta etapa; não devem receber um valor por inferência.

## 3. Semântica do retorno

O resultado confirmado é um envelope novo, independente do envelope de entrada
e da declaração:

```yaml
status: CONFIRMADO
valor: opcao_2
```

para `marcacao: exclusiva`, e:

```yaml
status: CONFIRMADO
valor:
  - opcao_2
  - opcao_4
```

para `marcacao: multipla`. Em modalidade múltipla, `valor: []` é válido. A
ordem de `valor` é a ordem lógica declarada dos itens, nunca a ordem temporal
de marcação, a ordem da grade, a coordenada ou o caminho do cursor.

O payload confirmado é, portanto, o campo literal `valor`; não criar uma
chave paralela `payload`. O resultado não inclui cursor, formação,
coordenadas, histórico de teclas, rótulo do chip ou posição física.

`Esc` continua produzindo exatamente:

```yaml
status: ABORTADO
```

sem `valor` e sem payload. A saída por `Esc` não confirma a escolha e não pode
reaproveitar marcações como resultado. `ABORTADO` continua distinto de
`valor: []`.

## 4. Binding e integração

### Origem e responsabilidades

- `PopupInstancia` é a origem da decisão: a declaração fornece a política e o
  envelope/runtime fornece os itens e a marcação viva.
- `tela/renderizacao/popup.py` interpreta `Enter`, valida a condição normativa
  e produz somente o envelope de resultado. Não fecha tela, não executa ação e
  não altera a declaração ou o envelope recebido.
- `demo/demo.py`, na ramificação modal de `processar_comando`, é o consumidor
  imediato. Enquanto `estado["popup"]` existir, toda tecla é capturada pelo
  pop-up; nenhum dispatcher de tela, console ou lançador deve receber a mesma
  tecla.
- O ponto de binding é o retorno de `consumir_tecla_popup` dentro dessa
  ramificação. Para `CONFIRMADO` ou `ABORTADO`, o consumidor deve limpar
  `estado["popup"]` e gravar o envelope exato em
  `estado["popup_resultado"]`.
- `tela/renderizacao/tela.py` permanece apenas como encaminhamento visual da
  instância para `sobrepor_no_corpo`; não é consumidor de decisão e não deve
  ser alterado por H-0059.

### Efeitos permitidos

Após confirmação, o pop-up deixa de capturar teclas, a tela subjacente volta a
receber interação e `popup_resultado` fica disponível ao chamador. A tela
subjacente, `tela_atual`, `pilha_telas`, foco, cursores, seleções e demais
camadas não relacionadas à decisão permanecem inalterados. O consumidor pode
interpretar o resultado, mas H-0059 não cria persistência, processo, mudança
de tela, ação de negócio, nova tela de resultado ou efeito global.

Após aborto, o mesmo fechamento e reativação ocorrem com o envelope
`ABORTADO` sem `valor`. Uma nova abertura deve limpar o resultado anterior,
como já faz o caminho demonstrativo.

## 5. Estado vivo

O cursor, as marcações e a formação continuam pertencendo ao `_estado` da
mesma `PopupInstancia`. A confirmação deve ler esse estado por IDs e manter a
identidade da instância durante navegação, marcação e resize. Não mutar:

- `modelo._raw["popups"]` ou qualquer declaração estrutural;
- `instancia.declaracao` como substituto de runtime;
- `instancia.conteudo` para transportar marcações provisórias;
- o envelope de entrada para anexar `valor` ou resultado.

O resultado é uma saída nova do consumidor; não é estado persistido na
configuração nem conteúdo de uma abertura futura.

## 6. Arquivos e diretórios autorizados para a futura implementação

Alterar somente os caminhos abaixo:

- `tela/renderizacao/popup.py` — regra de `Enter`, validação da regra de
  confirmação, formação de `CONFIRMADO` e preservação de `ABORTADO`.
- `tela/teste_popup.py` — testes focais de confirmação, payload, estados
  inválidos e regressão do aborto.
- `demo/demo.py` — consumo de ambos os resultados no binding modal e exposição
  de `popup_resultado` ao fluxo consumidor.
- `demo/teste_demo_popup.py` — testes de integração do retorno confirmado,
  payload consumido, fechamento modal e regressão de `Esc`.
- `config/telas/demo/demo.json` — declaração demonstrativa da confirmação nas
  duas listas H-0058, preservando os pop-ups textuais sem contrato de payload
  confirmado.
- `docs/relatorios/IMP-0059-popup-confirmacao-binding-integracao-decisao.md` —
  relatório factual obrigatório da implementação futura.

Não é necessária fixture H-0059 nova. Reutilizar, somente para leitura, as
fixtures runtime existentes de H-0058 em `demo/fixtures/` e os acionamentos
`e` e `m` já declarados no JSON. Não alterar essas fixtures.

O relatório da implementação futura deve ser criado no caminho nominal acima.

## 7. Alteração declarativa nominal

Nas declarações `popup_lista_exclusiva` e `popup_lista_multipla`, manter o
chip `Esc` atual e acrescentar um chip específico de `Enter`, na ordem
declarada depois do chip de aborto, com esta forma mínima:

```yaml
- id: popup_lista_exclusiva_confirmar  # ou o ID correspondente à lista múltipla
  tipo: especifico
  tecla: Enter
  texto: Confirmar
  referencia_regra:
    resultado:
      status: CONFIRMADO
  regra_existencia: sempre
  regra_ativo: sempre
  forma_exibicao: ativo
```

O ID deve ser único no pop-up. A validação deve continuar exigindo um único
chip `Esc` com `ABORTADO` sem payload e, para as declarações confirmáveis, um
único chip `Enter` com `CONFIRMADO`; teclas duplicadas e regras de retorno
incompatíveis devem falhar fechadamente. O chip não carrega valor estático:
o `valor` é produzido a partir do estado vivo.

## 8. Arquivos preservados

Preservar sem alteração:

- `docs/adr/ADR-0044-popup-modal-generico-de-decisao.md`;
- `docs/contratos/contrato_popup.md`;
- `docs/nomenclatura/35_POPUP.md`;
- `docs/backlog.md`;
- handoffs anteriores H-0056, H-0057 e H-0058;
- relatórios históricos e QAs históricos;
- `tela/renderizacao/tela.py`;
- as fixtures runtime existentes em `demo/fixtures/`;
- qualquer arquivo de código, configuração ou teste fora da lista nominal da
  seção 6.

Não registrar os dois trabalhos futuros no backlog durante H-0059. O registro
dos deferimentos só pode ocorrer no fechamento final do ITEM-0017.

## 9. Escopo negativo

É proibido nesta implementação:

- reabrir ou redesenhar qualquer capacidade de H-0058;
- alterar a política de resize ou promover formações antes do terminal pequeno
  como parte desta etapa;
- implementar composição ou justificação global de texto;
- criar antecipadamente item no backlog;
- criar nova modalidade de pop-up;
- criar arquitetura genérica adicional não exigida pela confirmação, pelo
  retorno ou pelo binding;
- executar ação de negócio, produtor de dados, loader, persistência ou
  processo a partir do pop-up;
- usar `seleção única` como nome da política `marcacao: exclusiva`.

## 10. Entradas, fixtures, temporários e saídas

- **Configuração declarativa:** `config/telas/demo/demo.json`, contendo apenas
  declarações estáveis, chips e regras de retorno; não recebe conteúdo,
  marcações runtime ou resultado.
- **Conteúdo/fixture runtime:** as fixtures H-0058 existentes fornecem o
  envelope pronto com itens e marcações iniciais; permanecem fora de alteração.
- **Estado runtime:** `PopupInstancia` mantém cursor, formação e marcações por
  ID; `popup_resultado` é o campo de sessão que o consumidor recebe após o
  encerramento.
- **Resultado do pop-up:** envelope novo com `status` e, somente em
  `CONFIRMADO`, `valor` conforme a modalidade.
- **Payload entregue:** o consumidor lê `popup_resultado["valor"]`; não deve
  ler a declaração, o envelope de entrada ou a grade para reconstruir a
  decisão.
- **Temporários:** preferir `tmp_path`/recursos temporários gerenciados pelo
  pytest. Remover arquivos temporários criados manualmente ao fim do caso;
  não deixar resíduos no repositório, em `demo/fixtures/` ou em `config/`.
- **Bytecode:** executar os comandos com `PYTHONDONTWRITEBYTECODE=1` quando
  aplicável.

## 11. Critérios de aceite

H-0059 estará implementado somente quando houver evidência focal de que:

1. `Enter` confirma uma instância de marcação com regra compatível.
2. O status é literalmente `CONFIRMADO`.
3. Exclusiva devolve exatamente um ID marcado e múltipla devolve a lista de
   IDs na ordem declarada, inclusive lista vazia.
4. O binding real fecha o pop-up, grava o resultado no consumidor e permite
   retomar a tela subjacente sem duplicar o comando.
5. `Esc` continua devolvendo `ABORTADO` sem `valor` e sem alterar escolha
   preexistente do chamador.
6. Foco por ID, marcação, navegação toroidal, formações, resize, conteúdo
   imutável e separação declaração/envelope/runtime de H-0056..H-0058 seguem
   preservados.
7. Não há antecipação da composição/justificação global nem do resize
   específico deferido, nem alteração de backlog.

## 12. Testes automatizados

Executar os alvos focais:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m pytest tela/teste_popup.py demo/teste_demo_popup.py
```

E executar a suíte canônica aplicável:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m pytest
```

Os testes focais devem incluir, no mínimo:

- confirmação exclusiva após navegação e transferência de marcação, com
  `valor` igual ao ID vivo;
- confirmação múltipla após marcações em ordem temporal diferente da ordem
  declarada, verificando a ordem lógica do `valor`;
- confirmação múltipla com marcação vazia, verificando `valor: []`;
- `\r` e `\n` como entradas equivalentes de `Enter`, sem resultado duplicado;
- Enter sem regra de confirmação e conteúdo textual sem contrato confirmado,
  mantendo a instância aberta e sem resultado;
- abertura exclusiva com zero ou múltiplas marcações rejeitada antes da
  interação;
- ausência de cursor, coordenada, formação ou histórico no resultado;
- `Esc` antes e depois de navegação/marcação, com `ABORTADO` sem `valor`;
- integração demonstrativa que verifica `popup is None`, resultado exato,
  tela/pilha preservadas e próxima tecla entregue à tela subjacente;
- regressão dos testes já existentes de H-0056, H-0057 e H-0058.

## 13. Demonstração reproduzível

Usar a configuração `config/telas/demo/demo.json`, os acionamentos `e` e `m`
e as fixtures runtime H-0058 existentes. A demonstração interativa pode ser
iniciada com:

```sh
PYTHONDONTWRITEBYTECODE=1 python demo/demo.py
```

Em TTY, pressionar `e`, opcionalmente `Espaço` para transferir a marcação e
`Enter`; o pop-up deve desaparecer e a sessão deve voltar à tela `demo`.
Para aborto, abrir novamente com `e` e pressionar `Esc`; o pop-up deve
desaparecer sem valor confirmado. `m` demonstra o retorno de lista múltipla.

Para tornar o binding observável sem depender de inspeção visual, executar um
harness determinístico sobre o mesmo carregamento demonstrativo:

```sh
PYTHONDONTWRITEBYTECODE=1 python -c 'from demo import demo; m=demo._carregar_modelo_por_id("demo"); s=demo.criar_estado_inicial(); s=demo.processar_comando(s,"e",m); s=demo.processar_comando(s," ",m); s=demo.processar_comando(s,"\r",m); print("CONFIRMACAO", s["popup"] is None, s["popup_resultado"]); a=demo.processar_comando(demo.processar_comando(demo.criar_estado_inicial(),"e",m),"\x1b",m); print("ABORTO", a["popup"] is None, a["popup_resultado"])'
```

O primeiro marcador deve mostrar `CONFIRMACAO True` e um resultado
`CONFIRMADO` com `valor: opcao_1`; o segundo deve mostrar `ABORTO True` e
`{'status': 'ABORTADO'}` sem `valor`. Esses campos provam que o retorno foi
consumido por `processar_comando`, e não apenas renderizado.

## 14. Validação manual

TTY real não é critério obrigatório se os testes automatizados e o harness
acima comprovarem as sequências e o binding. Caso a implementação altere a
leitura física de teclas de modo que os testes não consigam comprovar a
distinção entre `Enter` e `Esc`, realizar a verificação manual abaixo, sem
substituir os testes:

1. iniciar `python demo/demo.py` em TTY;
2. abrir `e`, mover/marcar e pressionar `Enter`;
3. confirmar que a moldura fecha e a tela subjacente permanece ativa;
4. abrir `e` novamente e pressionar `Esc`;
5. confirmar que o fechamento não produz payload confirmado.

O implementador deve registrar observações factuais no relatório de
implementação; não deve declarar aprovação de interação humana real por
inferência dos testes.

## 15. Relatório de implementação esperado

Criar, ao concluir a implementação:

`docs/relatorios/IMP-0059-popup-confirmacao-binding-integracao-decisao.md`

O relatório deve registrar factual e nominalmente:

- arquivos alterados, limitados à lista autorizada;
- comportamento implementado para `Enter`, `CONFIRMADO`, `valor` e binding;
- preservação de `Esc`/`ABORTADO` e dos comportamentos anteriores;
- comandos e resultados dos testes focais e da suíte canônica;
- demonstração executada e o efeito que provou o consumo do retorno;
- eventual validação TTY, se realizada;
- desvios explícitos e bloqueios reais, sem converter deferimentos em bloqueio.

## 16. Exceção operacional focal

Antes de alterar qualquer caminho, comparar o alvo com a lista nominal da
seção 6. Se a implementação exigir arquivo, diretório, fixture, contrato,
configuração ou outro artefato fora dessa lista, parar antes da alteração e
solicitar autorização nominal para o caminho e a finalidade. Não substituir a
solicitação por alteração aproximada em arquivo vizinho.

## 17. Bloqueios

Registrar somente bloqueios reais de execução, como incompatibilidade
objetiva entre contrato e código focal ou impossibilidade reproduzível de
executar a suíte. A composição/justificação global e o resize específico
deferidos não são bloqueios de H-0059 e não devem aparecer como falha ou
critério de aceite.
