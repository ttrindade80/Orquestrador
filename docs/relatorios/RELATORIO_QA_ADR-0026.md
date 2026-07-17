# Relatório de QA da ADR-0026

## 1. Identificação

*   **Identificador do Relatório:** RELATORIO_QA_ADR-0026
*   **Data de Execução:** 2026-07-17
*   **Objeto de Auditoria:** ADR-0026 (Ficheiro: `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`)
*   **Autor da Auditoria:** Auditor Documental Independente (`opencode`)
*   **Status do Objeto:** `aceita`

---

## 2. Escopo da auditoria

Este relatório realiza a auditoria documental independente e rigorosa da proposta da `ADR-0026`. O escopo é estritamente limitado à validação da ADR em relação às decisões explícitas do usuário, às restrições do anexo externo, à coerência conceitual com o repositório, à compatibilidade com ciclos e decisões anteriores (`H-0035` e `ADR-0025`) e ao estado do repositório Git.

O escopo é estritamente negativo para código executável, implementação de scripts, aplicação documental real aos contratos ou alterações em JSONs de tela.

---

## 3. Evidências examinadas

Durante o processo de auditoria, foram lidos integralmente e analisados os seguintes documentos do repositório:

1.  `docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md` (Alvo da auditoria)
2.  `docs/adr/ADR-0025-distribuicao-matricial-configuravel-nivel-unico-conteudo-elementos.md` (Contrato anterior)
3.  `docs/adr/INDICE_ADR.md` (Índice geral ativo)
4.  `docs/NOMENCLATURA.md` (Glossário ativo de termos)
5.  `docs/contratos/contrato_tela_json.md` (Contrato geral do schema de tela)
6.  `docs/contratos/contrato_console.md` (Contrato de comportamento do console)
7.  `docs/contratos/contrato_json_console.md` (Contrato de schema/envelope do console)
8.  `docs/contratos/contrato_composicao_corpo.md` (Contrato de composição)
9.  `docs/contratos/contrato_json_dashboard.md` (Contrato do dashboard)
10. `docs/contratos/contrato_json_lancador.md` (Contrato do lançador)
11. `docs/contratos/contrato_lancador.md` (Contrato do comportamento do lançador)

Também foi considerada a autoridade externa conceitual descrita no anexo `ESTRUTURA_JSON_CONTEUDO_MATRICIAL_E_MULTINIVEL.md`.

---

## 4. Decisões explícitas do usuário

Foram verificadas as 10 decisões explícitas estabelecidas pelo usuário:

1.  **Separação de Origem:** A origem dos dados recebidos pelo console deve ser separada da configuração estrutural da tela.
2.  **Proibição de Codificação Direta:** Dados de runtime não devem permanecer codificados de forma estática no JSON estrutural da tela.
3.  **JSON Externo:** O console receberá esses dados por meio de um JSON externo.
4.  **Conformidade com o Anexo:** O documento externo seguirá os princípios de envelope definidos no anexo.
5.  **Foco em Multinível:** A capacidade inicialmente tratada é conteúdo de tipo `multinivel`.
6.  **Dados Estruturados:** Os dados devem chegar previamente adequados à apresentação multinível.
7.  **Sem Reconstrução/Inferência de Hierarquia:** O consumidor de dados não deve inferir ou descobrir a hierarquia a partir de dados de domínio não normalizados.
8.  **Produção por Script:** No sistema final, um script externo será responsável por produzir ou devolver esses dados ao fluxo de apresentação.
9.  **Protocolo Aberto:** O protocolo concreto de comunicação com o script permanece em aberto para decisão futura.
10. **Preservação do Renderizador:** O renderizador continuará responsável por calcular geometria, dimensões, posições, quebras, truncamentos, paginação e distribuição de espaço em runtime.

---

## 5. Verificação de fidelidade

A `ADR-0026` registra com absoluta fidelidade cada uma das 10 decisões explícitas do usuário. 
*   Não foram inventadas políticas que extrapolassem as decisões de negócio ou de arquitetura propostas pelo usuário.
*   Nenhuma escolha alternativa foi imposta sem que houvesse uma decisão anterior documentada.
*   Nenhum detalhe de implementação (tais como nomes específicos de APIs, assinaturas de métodos, etc.) foi indevidamente normatizado.
*   O escopo permanece devidamente limitado ao console e ao formato de dados multinível.

---

## 6. Fronteiras de responsabilidade

A `ADR-0026` (seção 7) estabelece uma separação impecável das responsabilidades entre os componentes do fluxo de execução:
*   **Produtor Futuro:** Produz os dados semanticamente corretos e adequados ao formato, operando em runtime por meio de um script.
*   **Documento JSON Externo:** Transportador do conteúdo declarativo, incluindo tipo de conteúdo, formatação, políticas e dados.
*   **Configuração estrutural da tela:** Configuração pura da interface (composição de corpo), sem poluição por dados voláteis de runtime.
*   **Consumidor, Modelo e Loader:** Camada que gerencia o carregamento de ambos os JSONs separadamente. Suas definições de APIs, classes e assinaturas de métodos foram explicitamente deixadas em aberto (seção 7.4).
*   **Renderizador:** Focado na computação geométrica, quebras físicas, truncamento, posicionamento e reação SIGWINCH.

---

## 7. Estrutura declarativa do JSON externo

A `ADR-0026` estabelece com sucesso o princípio normativo fundamental:
> **O JSON declara intenção e conteúdo semântico. O renderizador calcula a representação física.**

Em perfeita sintonia com o anexo conceitual, a ADR garante que o JSON externo **não** contenha os resultados de cálculo físico de runtime, tais como:
*   Largura ou altura efetiva;
*   Linha ou coluna física calculada;
*   Posição ou coordenada física final;
*   Página calculada;
*   Quebra física pronta;
*   Truncamento já aplicado;
*   Geometria física final.

O envelope conceitual mínimo do arquivo externo registrado na ADR-0026 (seção 8) preserva a separação de forma precisa:
```json
{
  "tipo": "multinivel",
  "formato": {},
  "dados": []
}
```

---

## 8. Relação com conteúdo multinível

A `ADR-0026` formaliza que o foco inicial prioritário é o tipo `"multinivel"`.
*   Os níveis da hierarquia multinível devem ser explicitados nos dados;
*   A estrutura hierárquica não deve ser inferida automaticamente pelo consumidor;
*   Os dados de runtime chegam prontos para exibição sem necessidade de normalização reconstrutiva do lado do console;
*   A decisão não impõe uma forma visual restritiva única (como uma árvore rígida ou tabela particular), mantendo o renderizador livre para computar a distribuição física conforme as políticas que forem adotadas na aplicação documental futura.

---

## 9. Relação com o formato matricial

A `ADR-0026` (seção 9) trata de maneira cirúrgica a existência do formato `"matriz"` descrito no anexo externo.
*   A ADR reconhece a existência do tipo matricial no anexo e não o contradiz.
*   A ADR deixa explícito que o suporte ao formato matricial no mesmo mecanismo de dados externos permanece como possibilidade de expansão futura.
*   Não há inclusão forçada ou automática do formato matricial na primeira implementação decorrente deste ciclo de trabalho.
*   Não são introduzidos conflitos com a distribuição matricial de nível único regulada pela `ADR-0025`.

---

## 10. Compatibilidade com ADR-0025 e H-0035

O ciclo anterior e suas autoridades ativas permanecem integralmente preservados:
*   O handoff `H-0035` permanece fechado e seu commit `fb9e5be` intocado.
*   A `ADR-0025` continua válida e ativa sobre distribuição matricial configurável de nível único.
*   A `ADR-0026` trata exclusivamente da origem externa e da fronteira de transporte de dados de runtime do `console`.
*   Não há reabertura retroativa do ciclo.
*   Não há migração automática de dados históricos nem alteração indevida nas configurações de telas existentes no repositório.

---

## 11. Decisões corretamente deferidas

Todas as decisões relativas a detalhes técnicos ou comportamentos secundários de runtime foram devidamente postergadas e registradas como pendências ou decisões futuras obrigatórias (seção 14):
*   Nomes específicos de campos de vínculo (como `origem_dados`, caminho da fonte ou identificadores);
*   O meio físico de transporte (`stdout`, pipes, arquivos, descritores, objeto em memória);
*   A assinatura de comando, argumentos, linguagem e localização física do script produtor;
*   Os códigos de saída e os protocolos de tratamento de erros;
*   O ciclo de vida da execução síncrona ou assíncrona;
*   Persistência, cache, atualização e diretórios de runtime;
*   Versionamento e compatibilidade entre produtor e consumidor de dados;
*   Políticas de segurança, integridade e confiança na fonte;
*   Mapeamento de comportamentos visuais como paginação interativa, recolhimento/expansão de níveis e navegação;
*   Modificações de código de classes ou arquivos concretos e escopo de futuros handoffs.

---

## 12. Documentos afetados e aplicação futura

A `ADR-0026` (seção 12) lista corretamente e com alta precisão os documentos que serão afetados pela sua aplicação futura (`APLICAR_ADR`), sem alterá-los de forma precoce nesta etapa.
*   **INDICE_ADR.md:** Registrar a ADR-0026 após QA;
*   **NOMENCLATURA.md:** Formalizar novos termos conceituais introduzidos;
*   **contrato_tela_json.md, contrato_console.md, contrato_json_console.md, contrato_composicao_corpo.md:** Reconciliar o vínculo com a fonte semântica externa e delimitar as fronteiras;
*   **contrato_json_dashboard.md, contrato_json_lancador.md, contrato_lancador.md:** Avaliar possíveis impactos para salvaguardar distinções normativas;
*   **config/telas/demo/ e demo/:** Adequar as instâncias de demonstração quando o fluxo estiver operacional.

Nenhum caminho arbitrário ou inexistente foi inventado. Os diretórios listados representam locais reais.

---

## 13. Coerência com autoridades ativas

Não foram encontradas quaisquer contradições normativas entre a `ADR-0026` e as decisões anteriores:
*   A separação de responsabilidades segue estritamente a arquitetura desacoplada de dados consolidada na `ADR-0008` (modelo de configuração por tela).
*   A fronteira do renderizador respeita perfeitamente as capacidades geométricas definidas na `ADR-0025` e `ADR-0017`.
*   A ADR-0026 reconhece de forma explícita que o estado contratual atual das telas deve ser mantido, agindo como norte conceitual e não operacional.

---

## 14. Estado Git e arquivos observados

A inspeção do repositório Git foi realizada com sucesso e retornou o seguinte estado documental:
*   A nova ADR (`docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md`) está presente no repositório.
*   Não há qualquer outro arquivo alterado, de stage ou pendência de commit no repositório.
*   O estado Git encontra-se perfeitamente limpo, em total conformidade com a declaração recebida do gerente.

---

## 15. Achados

Nenhum achado de severidade bloqueante, alta, média ou baixa foi identificado na proposta da `ADR-0026`. O documento é fiel, robusto, aderente a todas as restrições e conceitualmente correto.

---

## 16. Observações

A `ADR-0026` destaca-se pela excepcional precisão conceitual ao lidar com o anexo externo. Ela descreve de forma preventiva e categórica que o anexo é uma autoridade externa à etapa, evitando poluir o repositório com caminhos ou cópias físicas inapropriadas e salvaguardando a independência do motor em relação a regras não aplicadas.

---

## 17. Classificação final

```yaml
status_literal: ADR_APPROVED
status_normalizado: Aprovada sem correções necessárias
relatorio: docs/relatorios/RELATORIO_QA_ADR-0026.md
achados_bloqueantes: 0
achados_altos: 0
achados_medios: 0
achados_baixos: 0
observacoes: 0
arquivos_inesperados: []
git:
  untracked_not_staged_expected:
    - docs/adr/ADR-0026-fornecimento-externo-dados-console-json-multinivel.md
  dirty: false
proxima_categoria: APLICAR_ADR
```
