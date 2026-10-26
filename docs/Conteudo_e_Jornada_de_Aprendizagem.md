# Documento 5 — Conteúdo e Jornada de Aprendizagem

**Projeto:** ELL IBM — nome provisório do projeto  
**Versão:** 0.1  
**Status:** Proposta operacional baseada nas decisões confirmadas pelo usuário  
**Idioma:** Português (Brasil)  
**Escopo:** Onboarding, jornada educacional, missões, simulações, intervenções adaptativas de IA, avaliação e progressão do MVP.

---

## 1. Objetivo do documento

Este documento especifica como o usuário será recebido, conhecerá a plataforma, aprenderá conceitos financeiros, praticará decisões, receberá apoio dos agentes de IA e avançará ao longo da jornada.

O objetivo não é apenas apresentar conteúdos, mas estabelecer um processo de aprendizagem contínuo, personalizado e mensurável.

A experiência deverá combinar:

- Onboarding obrigatório, curto, conversacional e adaptativo.
- Seis fases educacionais organizadas como capítulos de uma história.
- Metas pessoais definidas pelo usuário.
- Missões, dilemas, exercícios e simulações financeiras.
- Intervenções proativas dos agentes de IA.
- Quizzes adaptativos criados durante conversas e revisões.
- Feedback educativo e novas tentativas.
- Avaliação por competências demonstradas.
- Reforço individualizado de dificuldades.
- Progressão persistente, sem punição por pausas ou inatividade.
- Ações práticas opcionais e seguras fora do aplicativo.

O resultado esperado é uma experiência em que cada usuário encontre um ponto de partida adequado, pratique o que aprendeu e receba ajuda nos momentos em que ela realmente fizer diferença.

## 2. Convenções de decisão

Este documento diferencia decisões confirmadas, propostas operacionais e pendências.

### 2.1 Decisões confirmadas pelo usuário

1. A jornada terá seis fases, precedidas por onboarding obrigatório.
2. O público terá diferentes níveis de conhecimento e experiência financeira.
3. A narrativa combinará história contínua e metas pessoais.
4. O onboarding será curto e conversacional, com adaptação às respostas.
5. Os agentes serão proativos e contextuais, evitando interrupções desnecessárias.
6. Ações reais serão opcionais e seguras.
7. Os conteúdos de investimento serão introdutórios, sem recomendação de produtos específicos.
8. A progressão dependerá de competências demonstradas, feedback e reforço.
9. A LLM deverá criar quizzes e perguntas de revisão durante a conversa, adaptar as atividades às dificuldades individuais e intervir quando identificar uma oportunidade pedagógica relevante.

### 2.2 Propostas deste documento

São propostas para tornar a experiência implementável, sujeitas a validação:

- Três missões principais por fase, totalizando 18 missões.
- Uma simulação central por fase, incorporada a uma das missões.
- Um desafio integrador ao final da jornada.
- Um ciclo pedagógico comum para todas as missões.
- Gatilhos definidos para intervenções dos agentes.
- Registro estruturado das competências demonstradas.
- Revisões adaptativas e quizzes gerados a partir de conteúdo educacional aprovado.
- Critérios verificáveis para conclusão de missões e fases.

As quantidades e os gatilhos específicos não devem ser considerados decisões definitivas até serem validados.

### 2.3 Pendências

- Duração ideal das missões.
- Número de tentativas por atividade, quando houver limite.
- Regras numéricas de pontuação e conquistas.
- Limiares e evidências exatas para domínio de cada competência.
- Frequência máxima das intervenções proativas.
- Quantidade e formato dos quizzes de revisão.
- Detalhamento final da narrativa, personagens e recursos visuais.
- Revisão e aprovação técnica do conteúdo financeiro.
- Atualização do PRD e da Arquitetura Técnica para refletir as seis fases.

## 3. Princípios pedagógicos

### 3.1 Aprender fazendo

O usuário deve tomar decisões em situações concretas, observar consequências e compreender por que uma alternativa é mais adequada em determinado contexto.

O conteúdo expositivo será utilizado para apoiar a compreensão, e não como única forma de aprendizagem.

### 3.2 Personalização baseada em evidências

A adaptação poderá considerar:

- Objetivos declarados pelo usuário.
- Conhecimentos demonstrados no diagnóstico.
- Respostas às atividades.
- Dificuldades recorrentes.
- Tentativas anteriores.
- Desempenho em quizzes e simulações.
- Competências já demonstradas.
- Preferências de interação declaradas.

Uma resposta isolada, ambígua ou incorreta não deverá ser suficiente para classificar definitivamente o conhecimento do usuário.

### 3.3 Autonomia e ritmo individual

O usuário poderá pausar, revisar conteúdos e retomar a jornada. A ausência de atividade não implicará perda de progresso, punição ou diminuição de recompensas já conquistadas.

### 3.4 Feedback educativo

O feedback deverá explicar o raciocínio, indicar o que pode ser melhorado e sugerir um próximo passo. Sempre que possível, deverá distinguir um erro conceitual de uma interpretação diferente ou de uma resposta insuficientemente clara.

### 3.5 Narrativa com propósito

A história deverá conectar as fases sem competir com os objetivos educacionais.

Personagens e situações poderão apresentar dilemas financeiros, enquanto o usuário define suas próprias metas e pratica decisões em cenários fictícios. A história não deverá presumir que todos tenham salário, emprego, dívidas ou as mesmas condições financeiras.

### 3.6 Segurança financeira

As atividades devem utilizar cenários fictícios por padrão. O aplicativo não deverá executar transações, solicitar credenciais bancárias ou incentivar decisões arriscadas para obter recompensas.

As ações opcionais na vida real serão educativas, seguras e não dependerão do compartilhamento de informações financeiras sensíveis.

---

## 4. Jornada geral do usuário

A experiência será organizada em oito momentos, incluindo onboarding, seis fases e encerramento integrador.

1. Cadastro, verificação e acesso à conta.
2. Onboarding obrigatório e diagnóstico inicial.
3. Apresentação da jornada e definição de uma meta pessoal.
4. Fase 1 — Primeiro salário.
5. Fase 2 — Seu dinheiro no digital.
6. Fase 3 — Por que poupar.
7. Fase 4 — Juros: a favor e contra você.
8. Fase 5 — Onde o dinheiro rende.
9. Fase 6 — Proteção digital.
10. Desafio integrador e síntese das competências.

Os momentos 4 a 9 correspondem às seis fases educacionais. O desafio integrador poderá ser implementado como encerramento da Fase 6, sem criar uma sétima fase independente no mapa principal.

O usuário poderá visualizar as seis fases desde o início, mesmo que determinadas missões permaneçam bloqueadas até o atendimento dos critérios de progressão.

## 5. Onboarding obrigatório

### 5.1 Objetivo

O onboarding deverá acolher o usuário, explicar a proposta da plataforma, compreender suas necessidades e identificar um ponto de partida apropriado.

Não deverá funcionar como uma avaliação classificatória nem exigir conhecimento prévio de educação financeira.

### 5.2 Fluxo proposto

#### Etapa 1 — Boas-vindas

Apresentar, de maneira breve:

- O propósito educacional do aplicativo.
- A possibilidade de aprender por histórias, escolhas e simulações.
- A existência de agentes de IA que podem explicar conceitos, ajudar nas missões e propor revisões.
- A possibilidade de avançar no próprio ritmo.

O usuário deverá compreender que os agentes são assistentes educacionais e que suas respostas podem ter limitações.

#### Etapa 2 — Conhecer o usuário

O onboarding deverá coletar somente informações úteis à personalização inicial.

Exemplos de perguntas:

- Qual assunto financeiro você gostaria de entender melhor?
- Como você avalia sua familiaridade com orçamento, crédito e poupança?
- Você já costuma planejar objetivos financeiros ou ainda está começando?
- O que gostaria de conseguir fazer melhor depois de usar o aplicativo?

As perguntas serão adaptadas às respostas anteriores, evitando questionários extensos e repetitivos.

Não será necessário informar renda exata, saldo bancário, número de conta, senhas ou dados completos de cartões.

#### Etapa 3 — Diagnóstico conversacional

O sistema poderá apresentar pequenas situações para observar o conhecimento inicial.

Exemplo:

> Você recebeu um valor e quer comprar algo que deseja há algum tempo. Também possui despesas previstas para o mês. O que consideraria antes de decidir quanto gastar?

A resposta poderá ser aberta ou estruturada. O Mentor poderá pedir esclarecimentos ou apresentar uma segunda pergunta quando isso ajudar a distinguir uma lacuna de conhecimento de uma resposta incompleta.

O diagnóstico deverá avaliar conhecimentos iniciais, não a condição econômica ou o valor pessoal do usuário.

#### Etapa 4 — Definição de objetivo pessoal

O usuário poderá escolher uma meta ou indicar um interesse inicial.

Exemplos:

- Aprender a organizar meu dinheiro.
- Entender melhor o cartão de crédito.
- Começar a guardar dinheiro.
- Compreender juros e parcelamentos.
- Aprender a identificar golpes.
- Conhecer conceitos básicos de poupança e investimento.

A meta será utilizada para contextualizar exemplos e recomendações, sem restringir o acesso aos conteúdos essenciais.

#### Etapa 5 — Apresentação da jornada

Mostrar as seis fases, explicar a lógica de progressão e indicar a primeira atividade recomendada.

O Catalisador poderá apresentar uma recomendação contextual, deixando claro que se trata de uma sugestão e permitindo que o usuário continue no fluxo educacional previsto.

#### Etapa 6 — Primeira missão

O onboarding terminará com uma atividade curta, que demonstrará o ciclo de aprendizagem: contexto, decisão, feedback e próximo passo.

### 5.3 Requisitos do onboarding

- Ser obrigatório antes do acesso à primeira missão educacional.
- Ser curto e conversacional.
- Adaptar perguntas conforme as respostas.
- Permitir respostas simples e respostas abertas.
- Não exigir exposição de dados financeiros sensíveis.
- Explicar o papel e os limites da IA.
- Registrar preferências e resultados relevantes.
- Permitir que o usuário revise suas preferências posteriormente.
- Não bloquear o acesso a conteúdos básicos por desconhecimento prévio.
- Salvar o progresso do onboarding para permitir retomada em caso de interrupção.

A duração exata será definida após prototipação e testes com usuários.

---

## 6. Narrativa e metas pessoais

### 6.1 Estrutura narrativa

A proposta é utilizar uma história contínua organizada em seis capítulos. Personagens poderão enfrentar situações relacionadas a renda, pagamentos, objetivos, crédito, poupança, juros, investimentos e segurança digital.

Paralelamente, o usuário terá uma jornada própria, baseada em interesses e metas escolhidos por ele.

A narrativa deverá permitir que usuários com diferentes condições de vida se identifiquem com as situações apresentadas. O primeiro salário, por exemplo, será um cenário de aprendizagem, não uma condição obrigatória para participar.

### 6.2 Aplicação da meta pessoal

A meta pessoal poderá aparecer:

- Nos exemplos apresentados pelo Mentor.
- Nas recomendações de missões do Catalisador.
- Nas revisões sugeridas pelo Analista de Progresso.
- Em simulações de planejamento.
- Na síntese final da jornada.

O usuário poderá alterar sua meta ao longo do percurso. Essa alteração deverá influenciar as recomendações futuras sem invalidar as competências já demonstradas.

### 6.3 Limites da narrativa

A história não deverá:

- Pressionar o usuário a tomar decisões financeiras reais.
- Associar dificuldades financeiras a falhas morais.
- Premiar comportamentos arriscados.
- Exigir que todos tenham o mesmo objetivo.
- Criar prazos fictícios ou penalidades por inatividade.

---

## 7. Estrutura das seis fases

### Fase 1 — Primeiro salário

**Objetivo:** compreender renda, prioridades e organização inicial do dinheiro.

**Competências esperadas:**

- Distinguir salário bruto de salário líquido em exemplos apropriados.
- Diferenciar necessidades, desejos e prioridades.
- Identificar despesas e objetivos concorrentes.
- Organizar uma distribuição inicial de recursos em um cenário fictício.

**Missão 1.1 — De onde vem o dinheiro?**

O usuário conhece um cenário de renda e identifica a diferença entre o valor bruto e o valor líquido, conforme os dados apresentados.

Atividade: interpretar um exemplo simples de remuneração e reconhecer o valor disponível para planejamento.

**Missão 1.2 — O que importa primeiro?**

O usuário recebe uma lista de necessidades, desejos e objetivos e precisa decidir como priorizá-los diante de recursos limitados.

Atividade: ordenar escolhas e explicar os principais critérios utilizados.

**Missão 1.3 — Meu primeiro plano**

O usuário distribui uma renda fictícia entre despesas, objetivos e recursos disponíveis.

Atividade: montar um plano inicial, identificar conflitos e revisar a distribuição após receber feedback.

**Simulação central:** administrar o primeiro pagamento fictício diante de despesas e objetivos concorrentes.

**Evidência de aprendizagem:** o usuário consegue construir uma distribuição coerente e justificar suas prioridades.

**Intervenção dos agentes:**

- Catalisador: relaciona o cenário ao objetivo pessoal do usuário.
- Mentor: explica renda disponível, necessidades e prioridades.
- Analista de Progresso: identifica dificuldades na classificação ou distribuição de recursos.

### Fase 2 — Seu dinheiro no digital

**Objetivo:** compreender meios de pagamento digitais, características básicas de débito e crédito e cuidados com transações.

**Competências esperadas:**

- Diferenciar débito e crédito.
- Compreender o papel de limite, fatura e parcelamento.
- Reconhecer que disponibilidade de limite não significa dinheiro disponível.
- Identificar cuidados básicos em transações digitais.

**Missão 2.1 — Como vou pagar?**

O usuário compara situações de pagamento por Pix, débito e crédito.

Atividade: escolher um meio de pagamento em diferentes cenários e explicar as consequências relevantes.

**Missão 2.2 — Entendendo o cartão**

O usuário interpreta um cenário fictício com limite, compras, fatura e vencimento.

Atividade: identificar o que foi gasto, o que deverá ser pago e quais informações precisam ser verificadas.

**Missão 2.3 — Antes de confirmar**

O usuário analisa situações de pagamento digital e identifica cuidados antes de concluir uma operação.

Atividade: reconhecer informações que precisam ser conferidas e sinais de uma solicitação suspeita.

**Simulação central:** gerenciar pagamentos fictícios ao longo de um período, observando seus efeitos sobre o orçamento.

**Evidência de aprendizagem:** o usuário diferencia os meios de pagamento e interpreta corretamente as principais consequências do cenário.

**Intervenção dos agentes:**

- Catalisador: recomenda atividades conforme as dúvidas demonstradas.
- Mentor: esclarece funcionamento de pagamentos e crédito.
- Analista de Progresso: identifica confusões recorrentes entre saldo, limite, compra e obrigação de pagamento.

### Fase 3 — Por que poupar

**Objetivo:** desenvolver a compreensão de objetivos financeiros, planejamento e preparação para imprevistos.

**Competências esperadas:**

- Definir objetivos financeiros claros.
- Planejar compras sem comprometer despesas essenciais.
- Compreender a importância de guardar recursos quando possível.
- Reconhecer a função de uma reserva de emergência.
- Ajustar planos diante de imprevistos.

**Missão 3.1 — Um objetivo que faz sentido**

O usuário escolhe ou recebe um objetivo fictício e identifica o que seria necessário para alcançá-lo.

Atividade: definir o objetivo, estabelecer prioridades e avaliar sua viabilidade no cenário apresentado.

**Missão 3.2 — Guardar sem perder o controle**

O usuário decide quanto poderia reservar em um cenário de orçamento limitado.

Atividade: equilibrar despesas, prioridades e objetivo, com possibilidade de revisar escolhas.

**Missão 3.3 — E se acontecer algo inesperado?**

O usuário enfrenta uma despesa inesperada em uma simulação.

Atividade: reorganizar recursos, comparar alternativas e avaliar o papel de uma reserva.

**Simulação central:** planejar um objetivo e lidar com um imprevisto sem ignorar as despesas essenciais.

**Evidência de aprendizagem:** o usuário propõe um plano coerente, identifica prioridades e explica como o imprevisto afeta sua decisão.

**Intervenção dos agentes:**

- Catalisador: ajuda a conectar o objetivo à jornada pessoal.
- Mentor: explica planejamento e reserva de emergência.
- Analista de Progresso: verifica se o usuário considera despesas essenciais e imprevistos no planejamento.

### Fase 4 — Juros: a favor e contra você

**Objetivo:** compreender como juros, tempo, atrasos e condições de crédito afetam o valor total de uma decisão financeira.

**Competências esperadas:**

- Distinguir juros simples e compostos em exemplos introdutórios.
- Interpretar cenários de crescimento de um valor ao longo do tempo.
- Comparar alternativas de crédito.
- Compreender o efeito de atrasos e do pagamento mínimo da fatura.
- Avaliar custo total, prazo e condições antes de comparar alternativas.

**Missão 4.1 — O tempo e os juros**

O usuário compara cenários numéricos simplificados e observa como os valores evoluem ao longo do tempo.

Atividade: interpretar resultados e identificar o efeito do tempo e da taxa utilizada.

**Missão 4.2 — Parcelas não contam a história inteira**

O usuário compara alternativas de pagamento com valores, prazos e condições explícitos.

Atividade: calcular ou interpretar o custo total e explicar por que uma parcela menor não significa necessariamente menor custo.

**Missão 4.3 — O que acontece quando a dívida cresce?**

O usuário analisa um cenário de atraso e outro envolvendo pagamento mínimo da fatura.

Atividade: identificar as consequências apresentadas e comparar alternativas de decisão.

**Simulação central:** comparar propostas fictícias de crédito com informações suficientes para avaliar custo total e condições.

**Evidência de aprendizagem:** o usuário compara corretamente os cenários e justifica a escolha considerando custo, prazo e riscos.

**Intervenção dos agentes:**

- Catalisador: identifica quando o usuário pode se beneficiar de uma revisão adicional.
- Mentor: explica os conceitos e orienta cálculos ou comparações.
- Analista de Progresso: verifica se o usuário compreende o custo total, e não apenas o valor da parcela.

### Fase 5 — Onde o dinheiro rende

**Objetivo:** introduzir a relação entre inflação, poder de compra, poupança e características básicas de alternativas de investimento.

**Competências esperadas:**

- Explicar, em termos introdutórios, como a inflação afeta o poder de compra.
- Distinguir poupar de investir.
- Reconhecer conceitos básicos de poupança e CDB.
- Compreender liquidez, risco, retorno e prazo.
- Comparar características de alternativas fictícias sem presumir que exista uma opção universalmente melhor.

**Missão 5.1 — O que meu dinheiro consegue comprar?**

O usuário compara preços em momentos diferentes em um cenário simplificado.

Atividade: identificar como a mudança de preços afeta o poder de compra.

**Missão 5.2 — Guardar ou investir?**

O usuário explora a diferença entre reservar dinheiro e buscar rendimento por meio de uma alternativa financeira.

Atividade: classificar situações e compreender que objetivos diferentes podem exigir características diferentes.

**Missão 5.3 — Rendimento, prazo e liquidez**

O usuário compara alternativas fictícias com condições explícitas de prazo, liquidez e risco.

Atividade: identificar diferenças e explicar quais características importam para cada objetivo do cenário.

**Simulação central:** comparar alternativas educacionais fictícias, observando rendimento apresentado, condições de acesso ao dinheiro, prazo e riscos descritos.

**Evidência de aprendizagem:** o usuário identifica características relevantes e reconhece que rendimento potencial, risco e liquidez devem ser analisados em conjunto.

**Intervenção dos agentes:**

- Catalisador: relaciona os conceitos ao objetivo declarado pelo usuário.
- Mentor: explica os conceitos introdutórios e as limitações dos exemplos.
- Analista de Progresso: identifica confusões entre rendimento, liquidez, risco e garantia de retorno.

**Limites do conteúdo:** a fase não deverá recomendar investimentos específicos ao usuário, prometer rendimentos ou apresentar cenários fictícios como ofertas reais.

### Fase 6 — Proteção digital

**Objetivo:** desenvolver a capacidade de reconhecer riscos digitais e tomar decisões seguras diante de possíveis fraudes financeiras.

**Competências esperadas:**

- Identificar sinais de phishing e mensagens suspeitas.
- Reconhecer riscos de falsas centrais bancárias e solicitações de Pix.
- Identificar ofertas com promessas de lucro garantido como sinais que exigem cautela.
- Reconhecer riscos financeiros associados a apostas online.
- Aplicar cuidados básicos com credenciais e dados pessoais.
- Saber que ações iniciais considerar diante de uma possível fraude.

**Missão 6.1 — A mensagem suspeita**

O usuário analisa mensagens fictícias com diferentes sinais de alerta.

Atividade: identificar indícios de fraude e explicar o que deveria ser verificado.

**Missão 6.2 — Antes de enviar um Pix**

O usuário recebe cenários com solicitações legítimas e suspeitas, incluindo situações de pressão ou falsa autoridade.

Atividade: decidir se deve prosseguir, verificar informações por um canal independente ou interromper a ação.

**Missão 6.3 — Protegendo meus dados**

O usuário analisa situações envolvendo credenciais, links, falsas centrais e ofertas financeiras suspeitas.

Atividade: selecionar práticas seguras e justificar a resposta.

**Simulação central:** investigar uma sequência fictícia de mensagens e solicitações, identificar os sinais de risco e escolher ações seguras.

**Evidência de aprendizagem:** o usuário identifica sinais de alerta e escolhe respostas coerentes com a prevenção de fraude.

**Intervenção dos agentes:**

- Catalisador: incentiva a prática de decisões seguras.
- Mentor: explica os sinais de risco e as alternativas de resposta.
- Analista de Progresso: identifica sinais de alerta que o usuário ainda não reconhece e propõe revisão.

O conteúdo sobre golpes deverá ser educativo e atualizado por meio de fontes revisadas. A plataforma não deverá solicitar que o usuário compartilhe credenciais para verificar se uma situação é legítima.

---

## 8. Ciclo padrão de aprendizagem de uma missão

Cada missão deverá seguir uma estrutura comum, com adaptações conforme o objetivo educacional.

### Etapa 1 — Contexto narrativo

Apresentar uma situação concreta, um personagem ou um dilema relacionado ao conteúdo da missão.

O contexto deverá ser curto e suficiente para a decisão.

### Etapa 2 — Decisão inicial

Solicitar que o usuário escolha uma alternativa, responda a uma pergunta ou explique o que faria.

Essa resposta inicial ajudará a identificar conhecimentos prévios e possíveis dificuldades.

### Etapa 3 — Aprender fazendo

Apresentar um exemplo, uma explicação ou uma simulação que permita explorar as consequências da decisão.

O conteúdo deverá estar alinhado ao objetivo educacional da missão.

### Etapa 4 — Feedback contextual

Explicar o que a resposta demonstra, o que precisa ser revisto e por quê.

O feedback deverá considerar o raciocínio apresentado, não apenas informar se uma alternativa está certa ou errada.

### Etapa 5 — Verificação da aprendizagem

Apresentar uma pergunta ou tarefa que permita verificar se o usuário compreendeu o conceito.

A verificação poderá ocorrer dentro da própria conversa com o Mentor ou em um componente interativo da missão.

### Etapa 6 — Reforço adaptativo, quando necessário

Quando houver evidências de dificuldade, o sistema poderá propor uma explicação alternativa, um exemplo diferente ou um quiz adicional.

A repetição não deverá consistir apenas em reapresentar a mesma pergunta.

### Etapa 7 — Evidência e conclusão

Registrar a evidência de aprendizagem e aplicar as regras de conclusão definidas para a missão.

Se o domínio ainda não estiver demonstrado, o usuário poderá continuar aprendendo e tentar novamente conforme as regras da atividade.

### Etapa 8 — Próximo passo

O Catalisador poderá sugerir a próxima missão, uma revisão ou a continuidade da história.

O sistema deverá preservar o progresso e permitir que o usuário retome a experiência posteriormente.

---

## 9. Sistema de intervenções pedagógicas adaptativas da LLM

Esta seção estabelece um requisito central do MVP.

A LLM não deverá atuar apenas como um chat passivo. Ela poderá intervir durante a jornada quando houver uma oportunidade pedagógica relevante, criando perguntas, quizzes e revisões adequadas ao contexto individual.

### 9.1 Objetivos das intervenções

- Esclarecer uma dificuldade identificada.
- Verificar se um conceito foi realmente compreendido.
- Reforçar conhecimentos importantes.
- Retomar um conteúdo anterior quando ele for necessário para uma nova atividade.
- Identificar possíveis equívocos de interpretação.
- Ajudar o usuário a explicar seu raciocínio.
- Verificar se uma competência permanece compreendida após algum tempo ou em outro contexto.

### 9.2 Gatilhos de intervenção

A intervenção poderá ocorrer quando:

1. O usuário apresentar uma resposta incorreta em uma questão conceitual importante.
2. A resposta indicar uma possível confusão entre conceitos relacionados.
3. O usuário demonstrar dificuldade em uma etapa de uma simulação.
4. Houver erros recorrentes relacionados à mesma competência.
5. O usuário pedir uma explicação, revisão ou exemplo alternativo.
6. Uma nova missão depender de um conceito anterior que ainda não esteja bem demonstrado.
7. Uma revisão planejada indicar que é útil verificar novamente uma competência.
8. Uma resposta aberta for ambígua e exigir esclarecimento antes de ser avaliada.

A intervenção não deverá ocorrer automaticamente após qualquer erro. O sistema deverá considerar a relevância educacional, a confiança na interpretação e o contexto da interação.

### 9.3 Formatos de intervenção

**Explicação contextual**

O Mentor explica o conceito utilizando a própria situação em que surgiu a dificuldade.

**Pergunta orientadora**

O agente faz uma pergunta que ajuda o usuário a identificar o raciocínio necessário, sem fornecer imediatamente a resposta completa.

**Quiz curto na conversa**

A LLM apresenta uma ou mais perguntas, recebe as respostas e fornece feedback.

**Exemplo alternativo**

O agente utiliza números, personagens ou circunstâncias diferentes para esclarecer o mesmo conceito.

**Revisão de uma fase anterior**

O agente propõe uma atividade curta relacionada a um conceito anterior que seja relevante para a dificuldade atual.

**Aplicação em novo cenário**

O usuário demonstra se consegue transferir o conhecimento para uma situação diferente da que já resolveu.

### 9.4 Exemplo de intervenção adaptativa

Contexto: o usuário está comparando duas opções de parcelamento e escolhe aquela que tem a menor parcela, sem observar o custo total.

Intervenção do Mentor:

> Percebi que você priorizou o valor de cada parcela. Esse é um fator importante, mas vamos comparar também o custo total. Se uma opção tem parcelas menores, porém exige mais pagamentos, ela necessariamente custa menos?

A LLM poderá apresentar opções de resposta ou permitir que o usuário explique seu raciocínio.

Se a dificuldade persistir, o agente poderá montar um exemplo numérico simplificado e propor uma nova pergunta com valores diferentes.

Se o usuário demonstrar compreensão, o agente poderá retomar a missão original sem prolongar desnecessariamente a revisão.

### 9.5 Adaptação ao usuário

As intervenções poderão variar em:

- Complexidade da linguagem.
- Quantidade de explicações.
- Formato das perguntas.
- Tipo de exemplo.
- Quantidade de etapas de raciocínio.
- Necessidade de revisão de pré-requisitos.
- Contexto narrativo utilizado.

A adaptação deverá ser baseada em evidências observadas. O sistema não deverá presumir capacidade, comportamento ou condição financeira a partir de informações insuficientes.

### 9.6 Regras para quizzes gerados durante a conversa

Os quizzes gerados pela LLM deverão:

- Estar associados a um objetivo de aprendizagem identificado.
- Utilizar conteúdo educacional aprovado e coerente com a missão.
- Ter enunciados claros e adequados ao nível demonstrado.
- Utilizar alternativas plausíveis quando forem de múltipla escolha.
- Ter resposta esperada ou critério de avaliação documentado.
- Fornecer feedback explicativo após a resposta.
- Evitar perguntas ambíguas ou com múltiplas respostas válidas sem que isso esteja previsto.
- Permitir esclarecimento quando a resposta do usuário não puder ser interpretada com segurança.
- Registrar o resultado quando a atividade fizer parte da avaliação.
- Permitir que o usuário retome a missão após a intervenção.

Quando a LLM gerar uma pergunta aberta, o sistema deverá dispor de critérios de avaliação que permitam interpretar a resposta de forma consistente.

### 9.7 Revisão de conteúdos anteriores

O sistema poderá identificar competências importantes para revisão e oferecer atividades dentro da conversa.

Exemplo:

> Antes de avançarmos, vamos revisar rapidamente a diferença entre limite do cartão e dinheiro disponível. Vou apresentar uma situação curta e você me diz como interpretaria.

A revisão deverá utilizar um contexto novo quando isso ajudar a verificar compreensão real, em vez de apenas memorização da resposta anterior.

A frequência de revisões e os intervalos de repetição ainda deverão ser definidos e validados.

### 9.8 Controle de frequência e interrupções

As intervenções deverão ser proativas, mas não excessivas.

Como proposta operacional:

- Priorizar dificuldades que afetem a compreensão de conceitos essenciais.
- Evitar interromper uma atividade para explicar algo que não seja necessário naquele momento.
- Não repetir uma explicação que o usuário já demonstrou compreender, salvo quando houver evidência posterior de dificuldade.
- Permitir que o usuário adie uma revisão opcional.
- Não utilizar culpa, urgência artificial ou pressão para continuar.
- Encerrar a intervenção quando houver evidência suficiente de compreensão ou quando for necessário oferecer outro tipo de apoio.

A frequência máxima de intervenções e as regras de adiamento ainda estão pendentes de validação.

### 9.9 Registro das intervenções

Quando uma intervenção fizer parte do processo de aprendizagem, o sistema deverá registrar, conforme as regras de privacidade:

- Competência relacionada.
- Motivo da intervenção.
- Tipo de atividade apresentada.
- Resposta do usuário.
- Feedback fornecido.
- Evidência obtida.
- Recomendação resultante.
- Estado da missão antes e depois da intervenção.

O registro deverá permitir que o usuário retome a atividade e que o Analista de Progresso identifique dificuldades recorrentes.

### 9.10 Limites da LLM

A LLM poderá gerar explicações, perguntas e recomendações pedagógicas, mas não deverá:

- Alterar diretamente pontuação ou desbloqueios.
- Inventar taxas, regras financeiras ou condições de produtos.
- Transformar uma interpretação incerta em erro confirmado.
- Substituir critérios de avaliação definidos para competências essenciais.
- Tratar participação ou tempo de conversa como prova de domínio.
- Solicitar credenciais bancárias ou dados sensíveis desnecessários.
- Apresentar recomendações personalizadas de investimento.

---

## 10. Responsabilidades dos agentes

Os três agentes deverão atuar de maneira coordenada, preservando suas especializações.

### 10.1 Catalisador — Personalização e motivação

**Responsabilidade principal:** ajudar o usuário a encontrar o próximo passo educacional mais adequado.

Atividades:

- Participar do onboarding e ajudar a identificar interesses.
- Relacionar a jornada às metas pessoais declaradas.
- Recomendar missões e atividades de reforço.
- Sugerir continuidade após uma missão.
- Reconhecer competências demonstradas.
- Incentivar o retorno sem pressionar.
- Ajudar o usuário a escolher entre opções educacionais disponíveis.

O Catalisador não deverá classificar definitivamente o conhecimento do usuário nem conceder pontos ou desbloqueios.

### 10.2 Mentor — Tutoria e aprendizagem

**Responsabilidade principal:** apoiar a compreensão e o raciocínio durante as atividades.

Atividades:

- Explicar conceitos financeiros.
- Responder dúvidas no contexto da missão.
- Apresentar exemplos alternativos.
- Criar quizzes e perguntas de verificação quando apropriado.
- Propor revisões durante conversas.
- Dar feedback sobre raciocínios e decisões.
- Ajudar o usuário a compreender consequências e alternativas.

O Mentor deverá priorizar conteúdo educacional aprovado e explicitar incertezas quando necessário.

### 10.3 Analista de Progresso — Avaliação e reforço

**Responsabilidade principal:** interpretar evidências de aprendizagem e identificar necessidades de revisão.

Atividades:

- Analisar respostas e resultados.
- Identificar dificuldades recorrentes.
- Diferenciar erro, ambiguidade e falta de evidência.
- Recomendar atividades de reforço.
- Acompanhar competências demonstradas ao longo das fases.
- Sugerir verificações de retenção ou aplicação em outro contexto.
- Produzir uma síntese compreensível da evolução do usuário.

O Analista não deverá substituir regras objetivas por julgamentos arbitrários nem controlar diretamente pontos ou desbloqueios.

### 10.4 Coordenação entre agentes

A coordenação deverá seguir o fluxo lógico:

1. Uma interação, resposta ou evento de aprendizagem ocorre.
2. O backend valida o usuário, a atividade e o contexto disponível.
3. A camada de orquestração identifica o tipo de apoio necessário.
4. O agente adequado recebe o contexto mínimo necessário.
5. Quando houver benefício claro, os agentes poderão colaborar.
6. A resposta gerada será validada antes de ser apresentada ou persistida.
7. O backend registra o resultado aplicável e executa as regras determinísticas.
8. A interface apresenta feedback, progresso e próximo passo.

Não será necessário chamar todos os agentes em todas as interações. A colaboração deverá ocorrer quando o problema exigir competências complementares.

---

## 11. Avaliação e evidências de aprendizagem

### 11.1 Princípio

A conclusão deverá depender de competências demonstradas, não apenas de atividades abertas, tempo gasto ou número de mensagens enviadas.

A avaliação deverá considerar o objetivo educacional de cada missão e as evidências que permitem demonstrar sua compreensão.

### 11.2 Tipos de evidência

**Respostas objetivas**

Questões de múltipla escolha, classificação, ordenação e cálculos com resultados verificáveis.

**Respostas abertas**

Explicações, justificativas e raciocínios avaliados por critérios documentados.

**Decisões em simulações**

Escolhas e ações em cenários fictícios, considerando consequências e restrições apresentadas.

**Transferência de conhecimento**

Aplicação de um conceito a um novo contexto.

**Revisões adaptativas**

Respostas a quizzes e atividades de reforço que permitam verificar se uma dificuldade foi superada.

### 11.3 Critérios por missão

Cada missão deverá documentar:

- Objetivo de aprendizagem.
- Competências esperadas.
- Evidências aceitáveis.
- Critérios para interpretar respostas.
- Erros conceituais relevantes.
- Situações que exigem esclarecimento.
- Feedback recomendado.
- Condições de conclusão.
- Alternativas de reforço.
- Regras de nova tentativa.

Os critérios exatos de cada missão deverão ser definidos durante a produção do conteúdo.

### 11.4 Critérios por fase

A conclusão de uma fase dependerá das competências consideradas essenciais para seus objetivos.

O sistema deverá verificar se existem evidências suficientes de aprendizagem antes de liberar a progressão. Caso contrário, poderá propor revisão, atividade alternativa ou nova tentativa.

As regras específicas de conclusão deverão ser explícitas e reproduzíveis.

### 11.5 Separação entre aprendizagem e gamificação

A avaliação pedagógica e a pontuação de gamificação são mecanismos diferentes.

A IA poderá interpretar respostas abertas conforme critérios documentados e recomendar reforços. O backend deverá aplicar as regras oficiais de conclusão, pontuação, conquistas e desbloqueios.

O usuário não deverá receber pontuação ou avançar apenas porque conversou por muito tempo com um agente.

---

## 12. Progressão e retomada

### 12.1 Estados de uma missão

Como proposta inicial, cada missão poderá assumir estados como:

- Disponível.
- Em andamento.
- Aguardando resposta.
- Em revisão.
- Concluída.
- Bloqueada por dependência educacional.

Os estados definitivos e suas transições serão detalhados na especificação técnica.

### 12.2 Regras de progressão

- O mapa deverá indicar claramente as fases e o progresso.
- Os objetivos educacionais de cada fase deverão estar visíveis.
- A progressão deverá depender dos critérios definidos para as competências essenciais.
- Erros deverão gerar oportunidades de aprendizagem, não punições desproporcionais.
- As novas tentativas deverão preservar o contexto relevante.
- O progresso deverá persistir entre sessões.
- Repetições ou retomadas não poderão duplicar recompensas.
- O usuário não perderá progresso por inatividade.
- A IA não poderá desbloquear fases por conta própria.

### 12.3 Retomada

Quando o usuário retornar, o sistema deverá recuperar:

- Fase e missão atual.
- Estado da atividade.
- Respostas relevantes já registradas.
- Feedback anteriormente apresentado.
- Revisões pendentes ou recomendadas.
- Meta pessoal e preferências pertinentes.
- Competências já demonstradas.

A experiência deverá permitir que o usuário continue sem refazer desnecessariamente atividades já concluídas.

---

## 13. Ações práticas opcionais

As ações fora do aplicativo deverão ajudar a conectar a aprendizagem à vida cotidiana, sem exigir dados sensíveis ou comprovação financeira.

Exemplos:

- Definir uma meta pessoal.
- Refletir sobre categorias de gastos sem compartilhar valores exatos.
- Comparar preços antes de uma compra.
- Revisar configurações de segurança de uma conta por iniciativa própria.
- Elaborar um plano fictício de poupança.
- Conversar com alguém de confiança sobre planejamento financeiro.

As ações serão opcionais e não deverão bloquear a progressão. O usuário poderá registrar que realizou uma atividade sem fornecer documentos ou evidências financeiras.

Não haverá integração bancária, execução de pagamentos ou transações pelo aplicativo.

---

## 14. Desafio integrador

Ao final das seis fases, o usuário enfrentará uma situação que combine competências desenvolvidas ao longo da jornada.

### Cenário proposto

O usuário recebe um orçamento fictício, precisa organizar despesas, planejar um objetivo, avaliar uma alternativa de crédito, considerar um imprevisto e reconhecer uma possível tentativa de fraude.

O cenário poderá ser adaptado para se relacionar à meta pessoal escolhida no onboarding, sem exigir que o usuário exponha sua situação financeira real.

### Competências integradas

- Organização de recursos.
- Priorização de despesas e objetivos.
- Compreensão de meios de pagamento e crédito.
- Comparação de custos e juros.
- Planejamento e reserva para imprevistos.
- Interpretação de características básicas de alternativas de poupança e investimento.
- Identificação de riscos digitais.

### Avaliação

O desafio deverá avaliar a coerência das decisões e a capacidade de justificar escolhas considerando as informações fornecidas.

O Mentor poderá apoiar o usuário durante o processo, mas a avaliação final deverá utilizar critérios previamente documentados. O Analista de Progresso poderá produzir uma síntese das competências demonstradas e indicar oportunidades de revisão.

O desafio integrador não deverá substituir a avaliação das competências essenciais de cada fase.

---

## 15. Conteúdo, revisão e governança educacional

Todo conteúdo utilizado nas missões e pelos agentes deverá estar relacionado a objetivos de aprendizagem documentados.

Cada unidade de conteúdo deverá possuir, conforme aplicável:

- Identificador.
- Fase e missão associadas.
- Objetivo educacional.
- Texto ou material de referência.
- Exemplos e atividades.
- Critérios de avaliação.
- Fontes utilizadas.
- Responsável pela revisão.
- Data ou versão do conteúdo.
- Estado de revisão e publicação.

O conteúdo educacional deverá passar por revisão antes de ser publicado.

A LLM poderá adaptar a forma de explicar e criar perguntas dentro dos limites definidos, mas não deverá substituir a base educacional aprovada por informações inventadas ou não verificadas.

Conteúdos que dependam de regras, taxas ou condições sujeitas a mudanças deverão possuir fontes apropriadas e processo de atualização.

O painel administrativo deverá permitir a gestão, revisão e publicação dos conteúdos conforme a ordem de implementação já estabelecida na Arquitetura Técnica.

---

## 16. Experiência de interface e acessibilidade

A jornada deverá respeitar os princípios do Design System e UX/UI do projeto:

- Experiência mobile-first.
- Clareza educacional acima de efeitos visuais.
- Mapa visual de progresso.
- Objetivos claros por fase e missão.
- Feedback compreensível após decisões e respostas.
- Continuidade entre sessões.
- Ausência de prazos obrigatórios e penalidades por inatividade.
- Contraste, legibilidade e navegação acessível.
- Alternativas às interações que dependam exclusivamente de elementos visuais ou áudio.
- Uso de animações e recompensas sem prejudicar a compreensão.

Os agentes deverão possuir identidades e comportamentos consistentes com as definições do projeto, sem tornar a interface excessivamente carregada.

---

## 17. Escopo proposto do MVP

A primeira versão deverá priorizar um fluxo completo e validável de aprendizagem.

### Escopo funcional proposto

- Onboarding obrigatório.
- Diagnóstico inicial adaptativo.
- Definição de meta pessoal.
- Mapa com seis fases.
- Dezoito missões principais como referência inicial, três por fase.
- Uma simulação central por fase, integrada a uma missão.
- Quizzes e revisões adaptativos dentro das conversas.
- Feedback contextual.
- Três agentes especializados e coordenados.
- Avaliação por competências.
- Reforço e novas tentativas.
- Persistência e retomada.
- Desafio integrador.
- Registro de progresso e competências.
- Conteúdo estruturado, revisado e versionado.

### Ordem de implementação recomendada

**Etapa A — Fluxo vertical inicial**

Implementar onboarding, uma missão representativa, interação com o Mentor, uma intervenção adaptativa, avaliação, feedback e persistência. Esse fluxo deverá demonstrar a experiência de ponta a ponta.

**Etapa B — Motor pedagógico adaptativo**

Implementar os gatilhos de intervenção, geração controlada de quizzes, avaliação de respostas, registro de evidências e recomendações de reforço.

**Etapa C — Expansão das seis fases**

Produzir e integrar as demais missões e simulações, preservando o mesmo padrão pedagógico e técnico.

**Etapa D — Progressão integrada**

Implementar as regras de conclusão, o mapa da jornada, as revisões entre fases e o desafio integrador.

**Etapa E — Validação**

Testar os fluxos com usuários, verificar a qualidade das intervenções da IA, validar critérios de avaliação, testar persistência e garantir que os agentes não alterem regras de negócio.

A sequência proposta não exclui a necessidade de planejar desde o início o conteúdo das seis fases.

---

## 18. Indicadores para validar a jornada

Os indicadores deverão medir aprendizagem e qualidade da experiência, não apenas participação.

### Indicadores educacionais

- Evolução por competência.
- Desempenho em atividades equivalentes antes e depois de reforços.
- Frequência de dificuldades recorrentes.
- Taxa de resolução após intervenção adaptativa.
- Capacidade de aplicar conceitos em novos cenários.
- Resultados do desafio integrador.

### Indicadores de experiência

- Conclusão do onboarding.
- Abandono durante o onboarding.
- Retomada de missões interrompidas.
- Uso das revisões sugeridas.
- Avaliação do feedback recebido.
- Frequência de intervenções adiadas ou ignoradas.
- Ocorrência de intervenções repetitivas ou desnecessárias.

### Indicadores de confiabilidade

- Falhas na geração ou avaliação de quizzes.
- Respostas de IA fora do conteúdo educacional autorizado.
- Erros na persistência das respostas.
- Duplicação de recompensas.
- Divergências entre a avaliação apresentada e as regras oficiais.
- Falhas no fluxo de coordenação dos agentes.

Os indicadores e suas metas numéricas deverão ser definidos após testes e coleta de evidências. Nenhuma meta arbitrária será tratada como requisito aprovado.

---

## 19. Critérios de aceite do Documento 5

A especificação será considerada pronta para orientar o desenvolvimento quando:

1. O onboarding obrigatório estiver descrito com entradas, saídas e regras de persistência.
2. As seis fases tiverem objetivos e competências documentados.
3. Cada missão possuir estrutura pedagógica e critérios de avaliação definidos.
4. As simulações tiverem cenários, decisões possíveis e evidências esperadas.
5. Os gatilhos e formatos das intervenções adaptativas estiverem especificados.
6. Os quizzes gerados pela LLM estiverem vinculados a objetivos e critérios verificáveis.
7. As responsabilidades dos três agentes estiverem delimitadas.
8. As regras de progressão, reforço e retomada estiverem documentadas.
9. A separação entre avaliação pedagógica e gamificação estiver garantida.
10. Os limites de segurança, privacidade e conteúdo financeiro estiverem descritos.
11. O desafio integrador possuir competências e critérios de avaliação.
12. As decisões aprovadas, propostas e pendências estiverem claramente identificadas.
13. A divergência entre a estrutura de cinco fases dos documentos anteriores e a nova estrutura de seis fases estiver registrada para atualização.

---

## 20. Pendências para fechamento

Antes de considerar o documento definitivo, deverão ser fechados ou validados:

- A quantidade final de missões e a duração média de cada uma.
- A redação final dos objetivos e critérios de cada competência.
- A política de frequência das intervenções proativas.
- A política de revisão adaptativa e repetição de quizzes.
- As regras de conclusão das missões e fases.
- As fontes e o processo de revisão dos conteúdos financeiros.
- O escopo final da narrativa, personagens e recompensas.
- Os indicadores e critérios de sucesso do MVP.
- A atualização do PRD e da Arquitetura Técnica para a jornada de seis fases.

## 21. Referências internas do projeto

Este documento utiliza como base os seguintes materiais:

- **PRD_ELL_IBM.md:** visão do produto, jornada educacional, onboarding, requisitos funcionais, avaliação e responsabilidades dos agentes.
- **Especificacao_Agentes_IA_ELL_IBM.md:** especialização dos agentes, coordenação, autonomia, contexto, limites e comportamentos adaptativos.
- **Arquitetura_Tecnica_ELL_IBM.md:** backend como autoridade sobre regras de negócio, persistência, coordenação dos agentes, conteúdo estruturado, continuidade e validação.
- **Design_System_UX_UI_ELL_IBM.md:** princípios de experiência, acessibilidade, feedback, progressão visual e aprendizagem no ritmo do usuário.

A estrutura de seis fases e as decisões específicas de personalização registradas neste documento refletem as decisões mais recentes do usuário e deverão ser propagadas aos documentos anteriores quando a atualização for aprovada.

---

**Fim do Documento 5 — versão 0.1.**
