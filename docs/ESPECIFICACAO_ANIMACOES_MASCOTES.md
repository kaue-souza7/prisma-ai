# Especificação de Expressões e Animações dos Mascotes — ELL IBM

**Versão:** 1.0  
**Status:** Proposta — pendente de validação com designers e animadores  
**Escopo:** Catálogo de expressões, animações, gatilhos de interação, máquinas de estados e diretrizes de implementação para os três mascotes 3D da plataforma.

> **Nota de governança:** Esta especificação descreve o comportamento expressivo dos mascotes com base nas personalidades, responsabilidades e eventos já aprovados nos documentos de Design System (Documento 3) e Especificação de Agentes (Documento 4). As artes finais dos personagens ainda devem ser projetadas e validadas por designers 3D conforme a diretriz do Design System. Lacunas de informação são sinalizadas ao longo do documento com a marcação **⚠ Lacuna identificada**.

---

## 1. Fundamentos do sistema

### 1.1 Princípios que regem o comportamento expressivo

1. **A expressividade apoia, não compete.** Nenhuma animação deve ocorrer durante leitura ativa de conteúdo, resposta de questões ou exibição de feedback textual importante.
2. **Sem julgamento, sem constrangimento.** Erros não geram decepção, vergonha ou expressões negativas direcionadas ao usuário. O mascote reage ao evento de forma neutra ou encorajadora.
3. **Consistência de personalidade.** Cada mascote tem um repertório que reflete sua função: o Mentor acolhe e explica, o Analista organiza e informa, o Catalisador energiza e celebra.
4. **Frequência controlada.** Animações de ociosidade têm intervalos mínimos para não distrair. Celebrações especiais são raras e, portanto, impactantes.
5. **Acessibilidade incorporada.** Quando `prefers-reduced-motion: reduce` estiver ativo, todas as animações contínuas são desativadas e animações de reação são substituídas por crossfades estáticos suaves (≤ 200 ms).
6. **Leveza de implementação.** Animações são implementadas como skeletal rigs com blendshapes, exportadas em formato leve (glTF/GLB) e controladas por máquina de estados no frontend.

### 1.2 Paleta cromática dos mascotes (conforme Design System aprovado)

| Mascote | Cores primárias | Nota |
|---|---|---|
| Mentor | `#2F80ED` → `#56CCF2` | Azul acolhedor a ciano claro |
| Analista de Progresso | `#11998E` → `#38EF7D` | Verde-teal a verde elétrico |
| Catalisador | `#FF6B6B` → `#FCA048` | Coral a laranja |

> As cores acima são as identidades cromáticas aprovadas. Sua aplicação nos materiais 3D (base, brilho, emissão, sombra) deve ser definida pelo designer 3D em alinhamento com a direção de arte.

### 1.3 Anatomia expressiva dos personagens

Com base na referência de mascotes triangulares 3D com prisma arredondado, os seguintes elementos são os vetores de expressão:

| Região | Graus de liberdade previstos |
|---|---|
| **Olhos** | Abertura (normal, semicerrado, arregalado), direção do olhar (frente, cima, lado, baixo), pálpebra superior (franzido), brilho dinâmico |
| **Sobrancelhas** | Altura (neutro, levantado, abaixado), inclinação interna/externa (preocupado, surpreso, determinado) |
| **Boca** | Fechada neutra, sorriso leve, sorriso largo, expressão "O" (surpreso), curva para baixo leve (preocupado), aberta explicando |
| **Braços e mãos** | Posição lateral neutra, levantado, apontando, palma aberta, polegar para cima, mãos cruzadas, movimento rítmico |
| **Corpo (prisma)** | Inclinação frontal (curiosidade), balanceio lateral suave (ocioso), leve expansão de escala (celebração), rotação leve (explicando) |

> **⚠ Lacuna L-01:** A especificação exata dos rigs (quantidade de bones, hierarquia, nomenclatura das blendshapes) deve ser definida pelo animador 3D. Esta especificação descreve a intenção expressiva e os parâmetros-alvo, não a implementação técnica do rig.

---

## 2. Catálogo de animações por mascote

### 2.1 Mentor

**Personalidade:** acolhedor, didático, paciente, encorajador. Aparece em tempo real durante atividades e chat.

#### Animações do Mentor

---

**M-01 — Ocioso (Idle)**
- **Descrição:** Estado de repouso em espera da interação do usuário.
- **Gatilho:** Nenhuma interação ativa por mais de 4 segundos.
- **Olhos:** Abertos, olhar levemente para frente; piscadas naturais a cada 3–5 s.
- **Sobrancelhas:** Posição neutra, levemente relaxadas.
- **Boca:** Fechada, curva neutra a levemente positiva.
- **Corpo:** Balanceio lateral suave e contínuo (amplitude: ±3°, ciclo: 3 s). Respiração simulada por expansão mínima do prisma (+2% escala Y, ciclo: 4 s).
- **Braços:** Soltos ao lado do corpo, leve balanço passivo.
- **Duração:** Loop contínuo.
- **Intensidade:** Muito baixa.
- **Velocidade:** Lenta (ease-in-out suave).
- **Estado seguinte:** Qualquer animação de reação ou transição interrompe o idle imediatamente.
- **Frequência:** Sempre que nenhuma outra animação estiver ativa.
- **Quando não usar:** Durante exibição de feedback, carregamento de conteúdo ou qualquer texto em destaque.

---

**M-02 — Saudação**
- **Descrição:** O Mentor acena ao aparecer na tela pela primeira vez na sessão ou ao iniciar um chat.
- **Gatilho:** Abertura da área do Mentor; início de nova conversa.
- **Olhos:** Arregalados levemente, olhar direto para o usuário.
- **Sobrancelhas:** Levantadas suavemente.
- **Boca:** Sorriso médio.
- **Corpo:** Inclina levemente para frente (+5°) e volta à posição neutra.
- **Braços:** Levanta o braço direito com a mão aberta em aceno suave; retorna à posição neutra.
- **Duração:** 1,8 s.
- **Intensidade:** Média.
- **Velocidade:** Média (ease-out no início do levantamento; ease-in no retorno).
- **Estado seguinte:** Idle.
- **Frequência:** Uma vez por sessão por agente, ou quando o usuário abre o chat após longa inatividade.
- **Quando não usar:** No meio de uma conversa já em andamento.

---

**M-03 — Pensativo**
- **Descrição:** O Mentor demonstra que está processando ou considerando uma resposta.
- **Gatilho:** Backend processando resposta do LLM (indicador de "digitando"); usuário fez uma pergunta complexa.
- **Olhos:** Semicerrados, olhar levemente para cima e para o lado.
- **Sobrancelhas:** Uma sobrancelha levemente levantada; a outra levemente franzida.
- **Boca:** Fechada, levemente franzida de um lado (expressão de consideração).
- **Corpo:** Inclinação leve para o lado (±5°), mantida durante o processamento.
- **Braços:** Um braço levado levemente à altura do tronco, mão semi-fechada (posição de "pensando").
- **Duração:** Loop de 2,5 s enquanto o estado durar; encerra com transição suave.
- **Intensidade:** Baixa a média.
- **Velocidade:** Lenta.
- **Estado seguinte:** M-08 (Explicando) quando a resposta chega; Idle se não houver resposta a exibir.
- **Frequência:** Sempre que o backend estiver processando.
- **Quando não usar:** Se o tempo de resposta for < 500 ms (transição direta para M-08).

---

**M-04 — Curioso**
- **Descrição:** O Mentor demonstra interesse genuíno na interação, incentivando o usuário a continuar.
- **Gatilho:** Usuário está digitando uma mensagem longa; início de uma resposta aberta; usuário retomou uma missão após pausa.
- **Olhos:** Arregalados, olhar ligeiramente inclinado para frente.
- **Sobrancelhas:** Ambas levantadas de forma suave.
- **Boca:** Sorriso leve, boca levemente aberta.
- **Corpo:** Inclinação frontal suave (+7°), mantida enquanto o usuário digita.
- **Braços:** Ligeiramente afastados do corpo, palmas levemente abertas para frente (posição de abertura).
- **Duração:** Loop enquanto o usuário digitar; encerra em 800 ms ao parar de digitar.
- **Intensidade:** Baixa.
- **Velocidade:** Transição de entrada lenta; saída suave.
- **Estado seguinte:** Idle ou M-03 (Pensativo).
- **Frequência:** Uma vez por sequência de digitação, sem repetir no mesmo turno.
- **Quando não usar:** Quando o usuário estiver em uma questão objetiva de múltipla escolha.

---

**M-05 — Surpreso**
- **Descrição:** Reação rápida a um evento inesperado — como uma resposta muito boa ou um acerto inesperado.
- **Gatilho:** Usuário acerta uma questão considerada difícil (definida por critério no backend); comportamento incomum positivo.
- **Olhos:** Totalmente arregalados.
- **Sobrancelhas:** Ambas saltam para cima rapidamente.
- **Boca:** Expressão "O" por 300 ms, depois transição para sorriso.
- **Corpo:** Leve recuo para trás (−4° de inclinação) seguido de retorno para frente.
- **Braços:** Elevam-se levemente e abrem para os lados em um flash rápido.
- **Duração:** 1,2 s (incluindo transição de saída).
- **Intensidade:** Média-alta.
- **Velocidade:** Rápida na entrada (overshoot); suave na saída.
- **Estado seguinte:** M-10 (Aprovando) ou M-11 (Incentivando).
- **Frequência:** Máximo 1× por missão; não repetir na mesma sessão.
- **Quando não usar:** Em contexto de erro ou dificuldade do usuário.

---

**M-06 — Preocupado**
- **Descrição:** Expressão de atenção cuidadosa — nunca de desaprovação. Indica que o Mentor está prestando atenção especial a uma dificuldade.
- **Gatilho:** Analista identificou dificuldade recorrente (2ª intervenção do Mentor); usuário tentou uma missão 3× ou mais.
- **Olhos:** Levemente semicerrados, olhar focado.
- **Sobrancelhas:** Ligeiramente franzidas e aproximadas ao centro, posição mediana.
- **Boca:** Fechada, curva neutra (não para baixo — evitar leitura de tristeza ou julgamento).
- **Corpo:** Inclinação frontal leve e mantida (+5°), postura de atenção.
- **Braços:** Cruzados levemente à frente do corpo ou mãos juntas (postura de concentração).
- **Duração:** Mantida enquanto a mensagem de atenção for exibida; no mínimo 2 s.
- **Intensidade:** Baixa a média.
- **Velocidade:** Lenta.
- **Estado seguinte:** M-08 (Explicando) imediatamente após.
- **Frequência:** No máximo 1× por missão.
- **Quando não usar:** Na primeira tentativa de erro; em contextos de celebração ou acerto.

---

**M-07 — Encorajador**
- **Descrição:** Reação de suporte após um erro — transmite "você consegue, vamos tentar de novo".
- **Gatilho:** Usuário erra uma questão (qualquer tentativa).
- **Olhos:** Abertos, olhar direto e caloroso.
- **Sobrancelhas:** Neutras a levemente levantadas (expressão aberta, não tensa).
- **Boca:** Sorriso leve e genuíno — não exagerado.
- **Corpo:** Leve inclinação frontal (+5°), postura de aproximação.
- **Braços:** Um braço levantado com polegar para cima suave ou palma aberta para frente (gesto de "continue").
- **Duração:** 1,5 s, depois transição para M-08 (Explicando).
- **Intensidade:** Média.
- **Velocidade:** Suave.
- **Estado seguinte:** M-08 (Explicando).
- **Frequência:** Em todos os erros, sem exceção; a resposta ao erro nunca deve ser Idle.
- **Quando não usar:** Nunca omitir em contexto de erro.

---

**M-08 — Explicando**
- **Descrição:** O Mentor está apresentando uma explicação ou respondendo ativamente.
- **Gatilho:** Mensagem do Mentor sendo exibida; feedback pedagógico ativo.
- **Olhos:** Abertos, olhar frontal e levemente animado.
- **Sobrancelhas:** Neutras a levemente expressivas, acompanhando o fluxo da fala (se houver narração futura).
- **Boca:** Aberta levemente, boca em movimento suave alternado (para uso futuro com TTS; no MVP, animação de "speaking" genérica).
- **Corpo:** Leve rotação alternada esquerda/direita (±3°), ritmo de 1 ciclo por 2 s — simula gestuação natural.
- **Braços:** Movimento suave e alternado: um braço aponta gentilmente ou faz gesto de abrir, o outro permanece semi-relaxado.
- **Duração:** Loop enquanto o texto estiver sendo exibido; encerra 500 ms após o texto completar.
- **Intensidade:** Média.
- **Velocidade:** Média, ritmo constante.
- **Estado seguinte:** Idle ou animação de reação ao próximo evento.
- **Frequência:** Sempre que o Mentor exibir texto.
- **Quando não usar:** Nunca omitir quando há texto ativo do Mentor.

---

**M-09 — Verificando compreensão**
- **Descrição:** O Mentor faz uma pergunta de verificação e aguarda a resposta do usuário com atenção e abertura.
- **Gatilho:** Mentor emitiu uma pergunta de verificação de compreensão (Decisão 30 — estratégia 4).
- **Olhos:** Arregalados levemente, olhar direto, piscada suave.
- **Sobrancelhas:** Levantadas de forma suave e simpática.
- **Boca:** Sorriso leve, boca semifechada.
- **Corpo:** Levemente inclinado para frente, aguardando (+5°).
- **Braços:** Um braço estendido com palma aberta para cima (gesto de "sua vez").
- **Duração:** Loop de 3 s por ciclo enquanto aguarda resposta; máximo 30 s antes de retornar ao idle.
- **Intensidade:** Baixa.
- **Velocidade:** Lenta.
- **Estado seguinte:** M-04 (Curioso) quando usuário começa a digitar.
- **Frequência:** Uma vez por verificação; não repetir até nova pergunta.
- **Quando não usar:** Em questões objetivas de múltipla escolha (não é o contexto de pergunta aberta).

---

**M-10 — Aprovando**
- **Descrição:** Confirmação calorosa de resposta correta.
- **Gatilho:** Usuário acerta uma questão.
- **Olhos:** Levemente cerrados em sorriso genuíno (olhos em meia-lua).
- **Sobrancelhas:** Levantadas levemente.
- **Boca:** Sorriso amplo.
- **Corpo:** Leve expansão de escala (+4%) e retorno; inclinação frontal breve (+5°).
- **Braços:** Polegar para cima com um braço, retorna à posição neutra.
- **Duração:** 1,2 s.
- **Intensidade:** Média.
- **Velocidade:** Rápida na entrada; suave na saída.
- **Estado seguinte:** Idle ou M-08 (Explicando) se houver mensagem de feedback.
- **Frequência:** Em todos os acertos; pode ser combinada com efeito de partículas/pontos da interface.
- **Quando não usar:** Nunca exibir após erro.

---

**M-11 — Incentivando (continuidade)**
- **Descrição:** O Mentor encoraja o usuário a avançar para o próximo passo.
- **Gatilho:** Conclusão de missão; usuário concluiu uma atividade e está na tela de resultado.
- **Olhos:** Abertos, brilhantes.
- **Sobrancelhas:** Levantadas.
- **Boca:** Sorriso amplo e caloroso.
- **Corpo:** Inclinação frontal + leve expansão (+3% escala) no ritmo do gesto.
- **Braços:** Movimento de "siga em frente" — braços abertos e levados para frente, palmas abertas.
- **Duração:** 1,8 s.
- **Intensidade:** Média-alta.
- **Velocidade:** Média, fluida.
- **Estado seguinte:** Idle.
- **Frequência:** Uma vez por conclusão de missão.
- **Quando não usar:** No meio de uma explicação; durante uma dificuldade ativa.

---

### 2.2 Analista de Progresso

**Personalidade:** observador, analítico, organizado, confiável. Aparece no painel de progresso e em recomendações de reforço. Opera majoritariamente em background; sua presença visual é mais discreta e focada.

> **Nota de função:** O Analista não aparece durante atividades em tempo real. Sua presença visual ocorre no painel de progresso, nos cards de recomendação de reforço e na síntese de competências ao final de trilha. As animações devem refletir isso — mais compostas, menos exuberantes que o Catalisador.

#### Animações do Analista de Progresso

---

**A-01 — Ocioso (Idle)**
- **Descrição:** Estado neutro e atento no painel de progresso.
- **Gatilho:** Sem interação ativa.
- **Olhos:** Abertos, olhar frontal com movimentos sutis de varredura lateral (como alguém analisando dados).
- **Sobrancelhas:** Posição neutra, expressão serena.
- **Boca:** Fechada, curva levemente positiva (confiante, não necessariamente sorrindo).
- **Corpo:** Balanço vertical muito suave (expansão/compressão mínima, ciclo 4 s). Postura ereta.
- **Braços:** Soltos ao lado; ocasionalmente uma mão levada ao mento por 1 s a cada ~10 s (pose de análise).
- **Duração:** Loop contínuo.
- **Intensidade:** Muito baixa.
- **Velocidade:** Lenta.
- **Estado seguinte:** Qualquer animação de reação.
- **Frequência:** Sempre que na tela de progresso sem evento ativo.
- **Quando não usar:** Durante exibição de dados ou gráficos de progresso.

---

**A-02 — Apresentando dados**
- **Descrição:** O Analista está exibindo informações, gráficos ou o card de competências.
- **Gatilho:** Painel de progresso aberto; card "O que você demonstrou saber" exibido; síntese de trilha apresentada.
- **Olhos:** Abertos, olhar voltado levemente para o conteúdo exibido na interface (simula co-atenção).
- **Sobrancelhas:** Neutras.
- **Boca:** Fechada, neutra a levemente positiva.
- **Corpo:** Leve inclinação lateral em direção aos dados (±4°).
- **Braços:** Um braço estendido lateralmente apontando gentilmente para a área de dados; retorna após 2 s.
- **Duração:** 2,5 s para o gesto de apresentação; depois retorna para A-01 (Idle) enquanto dados permanecem visíveis.
- **Intensidade:** Baixa.
- **Velocidade:** Suave e controlada.
- **Estado seguinte:** A-01 (Idle).
- **Frequência:** Uma vez por abertura do painel ou card.
- **Quando não usar:** Se o painel já estiver aberto há mais de 5 s (não repetir o gesto de apresentação).

---

**A-03 — Identificando padrão**
- **Descrição:** O Analista comunica uma observação baseada em evidências — dificuldade recorrente identificada.
- **Gatilho:** Recomendação de reforço sendo apresentada ao usuário.
- **Olhos:** Levemente cerrados, olhar focado e direto (expressão de atenção analítica, não preocupação).
- **Sobrancelhas:** Uma ligeiramente mais alta que a outra (assimetria analítica).
- **Boca:** Fechada, neutra.
- **Corpo:** Postura levemente mais ereta, inclinação frontal mínima (+3°).
- **Braços:** Braços levemente cruzados à frente; um dedo indicador estendido em pose de "observação" — não acusação.
- **Duração:** Mantida enquanto a mensagem de recomendação for exibida; mínimo 2 s.
- **Intensidade:** Baixa.
- **Velocidade:** Transição lenta para esta expressão.
- **Estado seguinte:** A-05 (Confiante) ou A-01 (Idle).
- **Frequência:** Uma vez por recomendação de reforço.
- **Quando não usar:** Em contextos de celebração ou acerto.

---

**A-04 — Reflexivo/Pensativo**
- **Descrição:** O Analista processa antes de apresentar uma síntese.
- **Gatilho:** Backend calculando síntese de competências após conclusão de trilha.
- **Olhos:** Olhar levemente para cima, semicerrados com concentração.
- **Sobrancelhas:** Levemente franzidas — expressão de concentração, não preocupação.
- **Boca:** Fechada.
- **Corpo:** Leve inclinação lateral (±3°), postura reflexiva.
- **Braços:** Uma mão ao mento suavemente.
- **Duração:** Loop de 2 s enquanto o backend processa; encerra com A-02 ou A-05.
- **Intensidade:** Baixa.
- **Velocidade:** Lenta.
- **Estado seguinte:** A-02 (Apresentando) quando a síntese chega.
- **Frequência:** Apenas no momento de geração de síntese de trilha.
- **Quando não usar:** Em qualquer outro contexto.

---

**A-05 — Confiante / Validando**
- **Descrição:** Reação ao progresso positivo — o usuário demonstrou competência em uma área.
- **Gatilho:** Usuário acumulou evidências positivas em uma competência (registrado internamente pelo Analista); progresso significativo no painel.
- **Olhos:** Abertos, olhar frontal e calmo, com leve sorriso nos olhos.
- **Sobrancelhas:** Neutras a levemente levantadas.
- **Boca:** Sorriso contido e confiante (não exuberante — é o Analista, não o Catalisador).
- **Corpo:** Postura levemente mais expandida (+3% escala), ereta.
- **Braços:** Um polegar suave para cima ou braço levemente aberto com palma para frente.
- **Duração:** 1,5 s.
- **Intensidade:** Média-baixa.
- **Velocidade:** Suave.
- **Estado seguinte:** A-01 (Idle) ou A-02 (Apresentando).
- **Frequência:** Uma vez por sessão de abertura do painel de progresso quando há progresso positivo registrado.
- **Quando não usar:** Quando há dificuldade ativa a ser comunicada no mesmo painel.

---

**A-06 — Organizando / Curioso**
- **Descrição:** Expressão de foco organizado — o Analista "cataloga" uma nova informação.
- **Gatilho:** Usuário conclui uma nova atividade e o painel de progresso é atualizado em tempo real.
- **Olhos:** Olhar levemente para o lado (para onde os dados estão sendo atualizados na interface).
- **Sobrancelhas:** Levantadas suavemente.
- **Boca:** Levemente aberta (expressão de foco ativo).
- **Corpo:** Leve inclinação na direção dos dados; retorna à posição neutra.
- **Braços:** Movimento de "anotar" — um braço faz um gesto leve para frente como quem registra algo; retorna.
- **Duração:** 1,2 s.
- **Intensidade:** Baixa.
- **Velocidade:** Rápida no gesto; suave no retorno.
- **Estado seguinte:** A-01 (Idle).
- **Frequência:** Uma vez por atualização visível no painel.
- **Quando não usar:** Quando o painel não estiver aberto; quando a atualização for silenciosa em background.

---

**A-07 — Celebração analítica (síntese de trilha)**
- **Descrição:** Reação especial ao final de uma trilha — o Analista comemora de forma discreta e sólida, coerente com sua personalidade.
- **Gatilho:** Conclusão de trilha; exibição do card "O que você demonstrou saber".
- **Olhos:** Abertos, expressão de satisfação genuína.
- **Sobrancelhas:** Levantadas.
- **Boca:** Sorriso médio e confiante — mais caloroso que o usual para ele.
- **Corpo:** Expansão leve de escala (+5%) e retorno suave; postura orgulhosa.
- **Braços:** Ambos os braços levantados levemente, palmas para cima — gesto de "conseguiu".
- **Duração:** 2 s.
- **Intensidade:** Média.
- **Velocidade:** Suave, com ease-out.
- **Estado seguinte:** A-02 (Apresentando síntese) → A-01 (Idle).
- **Frequência:** Uma vez por conclusão de trilha, após o Catalisador já ter celebrado.
- **Quando não usar:** Antes da celebração do Catalisador; não deve ocorrer no mesmo instante que C-12.

---

### 2.3 Catalisador

**Personalidade:** energético, motivador, celebrativo. Aparece no onboarding, na Home (próximo passo), nas celebrações de conquista e no retorno após inatividade.

> **Nota de função:** O Catalisador é a voz da jornada — ele é o primeiro e o mais frequente contato emocional do usuário. Suas animações devem ser as mais expressivas e celebrativas da plataforma, mantendo coerência com o tom respeitoso e sem pressão definido nas decisões aprovadas.

#### Animações do Catalisador

---

**C-01 — Ocioso (Idle)**
- **Descrição:** Estado de espera vibrante — o Catalisador está sempre "pronto para entrar em ação".
- **Gatilho:** Nenhuma interação ativa.
- **Olhos:** Abertos e brilhantes, olhar animado levemente voltado para o usuário.
- **Sobrancelhas:** Levantadas em posição neutra-positiva.
- **Boca:** Sorriso leve e natural.
- **Corpo:** Balanceio lateral mais evidente que os outros mascotes (±5°, ciclo 2,5 s); leve "pulsar" de escala (+3%, ciclo 2 s) — energia contida.
- **Braços:** Balanço suave, mãos ocasionalmente abrindo e fechando levemente.
- **Duração:** Loop contínuo.
- **Intensidade:** Baixa a média.
- **Velocidade:** Média, ritmo de energia contida.
- **Estado seguinte:** Qualquer animação de reação.
- **Frequência:** Sempre no idle; se `prefers-reduced-motion` estiver ativo, substituir por postura estática com apenas piscadas.
- **Quando não usar:** Durante exibição de texto do Catalisador.

---

**C-02 — Saudação de onboarding**
- **Descrição:** Primeira impressão — o Catalisador recebe o novo usuário com entusiasmo genuíno.
- **Gatilho:** Início do onboarding (primeira vez); primeira mensagem do Catalisador.
- **Olhos:** Totalmente abertos, brilhantes.
- **Sobrancelhas:** Levantadas.
- **Boca:** Sorriso largo.
- **Corpo:** Leve salto de entrada (+8% escala, 400 ms) com ease-out; inclinação frontal (+8°).
- **Braços:** Ambos os braços levantados em "V" de boas-vindas por 600 ms; depois retornam ao neutro.
- **Duração:** 2 s total.
- **Intensidade:** Alta.
- **Velocidade:** Rápida na entrada; suave na saída.
- **Estado seguinte:** C-06 (Explicando/Entusiasmado).
- **Frequência:** Uma vez na vida do usuário (onboarding); reutilizável para retorno após longa inatividade (> 30 dias), conforme D-C13.
- **Quando não usar:** No meio de conversas; após o onboarding já ter sido feito na mesma sessão.

---

**C-03 — Ouvindo com interesse**
- **Descrição:** O Catalisador demonstra interesse genuíno enquanto o usuário responde ao onboarding.
- **Gatilho:** Usuário está digitando ou selecionando resposta durante o onboarding.
- **Olhos:** Arregalados levemente, olhar de escuta ativa.
- **Sobrancelhas:** Levantadas suavemente.
- **Boca:** Sorriso leve, boca levemente aberta.
- **Corpo:** Inclinação frontal leve (+7°), postura de abertura.
- **Braços:** Levemente afastados do corpo, palmas parcialmente abertas.
- **Duração:** Loop enquanto o usuário digita.
- **Intensidade:** Baixa a média.
- **Velocidade:** Transição suave.
- **Estado seguinte:** C-04 (Celebrando resposta) ou C-06 (Explicando) após a resposta ser enviada.
- **Frequência:** Em cada pergunta do onboarding.
- **Quando não usar:** Após conclusão do onboarding.

---

**C-04 — Celebrando resposta (onboarding)**
- **Descrição:** O Catalisador reage com entusiasmo a cada resposta do usuário durante o onboarding, criando conexão emocional conforme D-C3.
- **Gatilho:** Usuário envia uma resposta durante o onboarding.
- **Olhos:** Olhos cerrados em sorriso ("olhos de lua").
- **Sobrancelhas:** Levantadas.
- **Boca:** Sorriso largo.
- **Corpo:** Leve salto pequeno (+5% escala, 300 ms).
- **Braços:** Movimento de aplauso leve ou gesto de "isso mesmo!" com um braço.
- **Duração:** 1 s.
- **Intensidade:** Alta.
- **Velocidade:** Rápida.
- **Estado seguinte:** C-03 (Ouvindo) para a próxima pergunta ou C-05 (Revelação de trilha) ao final.
- **Frequência:** Toda resposta de onboarding — mas com variações para não repetir o mesmo gesto 18 vezes. Usar pool de 3–4 variações (⚠ Lacuna L-02: variantes a definir com o animador).
- **Quando não usar:** Fora do onboarding.

---

**C-05 — Revelação de trilha**
- **Descrição:** Momento de revelação personalizada da jornada — animação mais impactante do onboarding.
- **Gatilho:** Apresentação da narrativa personalizada e trilha recomendada ao final do onboarding (D-C4).
- **Olhos:** Abertos ao máximo, brilho intenso.
- **Sobrancelhas:** Levantadas ao máximo.
- **Boca:** Sorriso mais amplo do personagem.
- **Corpo:** Expansão de escala (+8%), rotação leve do corpo completo (±5°, balanço de celebração), postura mais ereta e imponente.
- **Braços:** Ambos os braços se abrem amplamente para os lados e depois direcionam-se para frente apontando para a tela (gesticulando para o conteúdo apresentado).
- **Duração:** 2,5 s.
- **Intensidade:** Muito alta.
- **Velocidade:** Rápida na entrada com overshoot; suave e longa na saída.
- **Estado seguinte:** C-06 (Explicando).
- **Frequência:** Uma vez por usuário (onboarding único).
- **Quando não usar:** Fora do onboarding.

---

**C-06 — Explicando / Entusiasmado**
- **Descrição:** O Catalisador apresenta informações com energia e engajamento.
- **Gatilho:** Texto do Catalisador sendo exibido; mensagem de "próximo passo" na Home; sugestão de revisão; retorno após inatividade.
- **Olhos:** Abertos, expressivos.
- **Sobrancelhas:** Levantadas moderadamente, acompanhando o conteúdo.
- **Boca:** Sorriso médio, boca levemente aberta (animação de fala genérica).
- **Corpo:** Rotação suave esquerda/direita (±4°, ciclo 2 s), mais ritmado que o Mentor.
- **Braços:** Gestos mais expressivos que o Mentor — braço aponta, abre, enfatiza, com mais amplitude e velocidade.
- **Duração:** Loop enquanto texto for exibido; encerra 600 ms após texto completar.
- **Intensidade:** Média a média-alta.
- **Velocidade:** Média-rápida.
- **Estado seguinte:** Idle ou animação de reação ao próximo evento.
- **Frequência:** Sempre que o Catalisador exibir texto.
- **Quando não usar:** Nunca omitir quando há texto ativo.

---

**C-07 — Incentivando (próxima missão)**
- **Descrição:** O Catalisador empurra o usuário para o próximo passo com entusiasmo.
- **Gatilho:** Exibição da recomendação de próximo passo na Home; após conclusão de missão.
- **Olhos:** Brilhantes, olhar direto para o usuário.
- **Sobrancelhas:** Levantadas.
- **Boca:** Sorriso amplo.
- **Corpo:** Inclinação frontal (+8°), leve expansão.
- **Braços:** Braço estendido para frente com o dedo ou palma apontando para o card de próxima missão.
- **Duração:** 1,5 s para o gesto; depois mantém postura de inclinação em loop suave.
- **Intensidade:** Alta.
- **Velocidade:** Média.
- **Estado seguinte:** C-01 (Idle).
- **Frequência:** Uma vez por exibição do card de próxima missão.
- **Quando não usar:** Quando o usuário acabou de errar e está em momento de feedback de erro.

---

**C-08 — Acolhimento após inatividade**
- **Descrição:** Retorno do Catalisador quando o usuário volta após ausência — acolhedor, sem cobrar (D-C13).
- **Gatilho:** Usuário retorna à plataforma após ausência; backend detecta retorno após inatividade.
- **Olhos:** Abertos, expressão calorosa e genuína.
- **Sobrancelhas:** Levantadas levemente, expressão amigável.
- **Boca:** Sorriso caloroso, médio.
- **Corpo:** Inclinação frontal suave (+5°).
- **Braços:** Aceno suave com um braço — gesto de "que bom te ver de volta".
- **Duração:** 1,8 s.
- **Intensidade:** Média.
- **Velocidade:** Suave e acolhedora.
- **Estado seguinte:** C-06 (Explicando) ao exibir a mensagem de retorno.
- **Frequência:** Uma vez por retorno detectado pelo backend.
- **Quando não usar:** Nunca mencionar tempo de ausência (conforme D-C13); não usar em retornos na mesma sessão.

---

**C-09 — Surpreso positivo (acerto inesperado)**
- **Descrição:** Reação viva a um desempenho acima do esperado.
- **Gatilho:** Usuário completa uma missão no modo Expresso com 100% de acerto; usuário acerta uma questão considerada difícil.
- **Olhos:** Totalmente arregalados, brilhantes.
- **Sobrancelhas:** Saltam para cima rapidamente.
- **Boca:** "O" de surpresa por 300 ms → sorriso largo.
- **Corpo:** Recuo rápido (−6°) → expansão para frente (salto de escala +8%).
- **Braços:** Abrem-se rapidamente para os lados em flash.
- **Duração:** 1,5 s.
- **Intensidade:** Muito alta.
- **Velocidade:** Rápida, com overshoot.
- **Estado seguinte:** C-11 (Celebrando conquista) ou C-06 (Explicando).
- **Frequência:** Máximo 1× por missão.
- **Quando não usar:** Em contextos de erro; não usar para acertos simples e rotineiros.

---

**C-10 — Encorajando após dificuldade**
- **Descrição:** O Catalisador apoia o usuário após uma sequência de dificuldades — sem pressão, com sugestão de revisão (D-C9; D33 Nível 3).
- **Gatilho:** Backend aciona o Catalisador para sugerir atividade de reforço após limite de intervenções do Mentor.
- **Olhos:** Abertos, expressão gentil.
- **Sobrancelhas:** Levantadas de forma simpática (não franzidas).
- **Boca:** Sorriso encorajador, médio.
- **Corpo:** Leve inclinação frontal (+5°), postura de proximidade.
- **Braços:** Um braço estendido com palma aberta (gesto de oferecer ajuda, não de apontar o erro).
- **Duração:** 1,5 s.
- **Intensidade:** Média.
- **Velocidade:** Suave.
- **Estado seguinte:** C-06 (Explicando) ao apresentar a sugestão.
- **Frequência:** Uma vez por ativação do protocolo de escalonamento (D33 Nível 3).
- **Quando não usar:** Nunca exibir expressão de decepção, tristeza ou frustração. O Catalisador não reflete o erro — ele oferece suporte.

---

**C-11 — Celebrando conquista**
- **Descrição:** Celebração de conclusão de missão — animação de alta energia.
- **Gatilho:** Usuário conclui uma missão com sucesso.
- **Olhos:** Cerrados em sorriso de celebração.
- **Sobrancelhas:** Levantadas ao máximo.
- **Boca:** Sorriso máximo.
- **Corpo:** Sequência: expansão rápida (+10% escala) → rotação de comemoração (balanço ±8°, 2 ciclos rápidos) → retorno suave à posição neutra.
- **Braços:** Ambos levantados em "V" ou em gesto de comemoração aberta, depois retornam.
- **Duração:** 2,2 s.
- **Intensidade:** Muito alta.
- **Velocidade:** Rápida na entrada com overshoot; saída longa e suave.
- **Estado seguinte:** C-06 (Explicando) ao apresentar o próximo passo (D-C12).
- **Frequência:** Uma vez por conclusão de missão. Não repetir para conquistas menores (acertos simples).
- **Quando não usar:** Em contexto de erros; não utilizar quando o `prefers-reduced-motion` estiver ativo — substituir por sorriso estático com expansão mínima (< 3%).

---

**C-12 — Celebração de conclusão de trilha (especial)**
- **Descrição:** Animação mais longa e impactante — reservada para conclusão de trilha completa.
- **Gatilho:** Usuário conclui uma trilha inteira (D-C12).
- **Olhos:** Brilhantes, exuberantes.
- **Sobrancelhas:** Levantadas ao máximo.
- **Boca:** Sorriso máximo, boca aberta de celebração.
- **Corpo:** Loop de comemoração completo: expansão (+12%) → rotação lateral rápida (3 ciclos) → retorno lento e orgulhoso; corpo se projeta levemente para frente ao final como quem se aproxima do usuário para parabenizar.
- **Braços:** Movimento amplo de comemoração: braços sobem, abrem, fazem gesto de vitória; posição de aplausos rítmicos (2 batidas); finaliza apontando para frente (para o usuário).
- **Duração:** 3,5 s (animação mais longa do sistema).
- **Intensidade:** Máxima.
- **Velocidade:** Rápida nos picos; lenta e fluida no retorno.
- **Estado seguinte:** C-06 (Explicando) ao apresentar síntese e próxima trilha.
- **Frequência:** Uma vez por conclusão de trilha; não reutilizável dentro da mesma sessão.
- **Quando não usar:** Quando `prefers-reduced-motion` estiver ativo — substituir por C-11 (versão reduzida); não usar para conclusão de missão individual.

---

## 3. Tabela consolidada de animações

| # | Personagem | Estado/Animação | Evento disparador | Expressão facial | Gesto corporal | Duração | Intensidade | Estado seguinte | Prioridade MVP |
|---|---|---|---|---|---|---|---|---|---|
| M-01 | Mentor | Ocioso | Sem interação | Neutro, piscadas | Balanço suave | Loop | Muito baixa | Qualquer reação | P1 |
| M-02 | Mentor | Saudação | Abertura do chat | Sorriso médio, arregalado | Aceno, inclinação frontal | 1,8 s | Média | Idle | P1 |
| M-03 | Mentor | Pensativo | Backend processando | Semicerrado, olhar oblíquo | Inclinação lateral, mão próxima ao corpo | Loop 2,5 s | Baixa | Explicando | P1 |
| M-04 | Mentor | Curioso | Usuário digitando | Arregalado, boca aberta leve | Inclinação frontal | Loop | Baixa | Idle/Pensativo | P2 |
| M-05 | Mentor | Surpreso | Acerto difícil | "O", depois sorriso | Recuo + expansão | 1,2 s | Média-alta | Aprovando | P3 |
| M-06 | Mentor | Preocupado | Dificuldade recorrente | Focado, neutro | Postura de atenção | 2+ s | Baixa | Explicando | P1 |
| M-07 | Mentor | Encorajador | Após qualquer erro | Sorriso leve, olhar caloroso | Inclinação frontal, gesto de apoio | 1,5 s | Média | Explicando | P1 |
| M-08 | Mentor | Explicando | Texto ativo | Aberto, animado | Rotação leve, gestos ritmados | Loop | Média | Idle | P1 |
| M-09 | Mentor | Verificando compreensão | Após pergunta aberta | Sorriso leve, arregalado | Palma aberta, aguardando | Loop 3 s | Baixa | Curioso | P2 |
| M-10 | Mentor | Aprovando | Acerto de questão | Olhos em meia-lua, sorriso | Polegar, expansão leve | 1,2 s | Média | Idle/Explicando | P1 |
| M-11 | Mentor | Incentivando | Conclusão de missão | Sorriso amplo | Braços abertos para frente | 1,8 s | Média-alta | Idle | P2 |
| A-01 | Analista | Ocioso | Sem interação | Neutro-positivo, varredura sutil | Balanço mínimo, pose analítica | Loop | Muito baixa | Qualquer reação | P1 |
| A-02 | Analista | Apresentando dados | Painel aberto | Neutro, co-atenção | Braço apontando para dados | 2,5 s | Baixa | Idle | P1 |
| A-03 | Analista | Identificando padrão | Recomendação de reforço | Focado, analítico | Postura ereta, dedo em observação | 2+ s | Baixa | Confiante/Idle | P1 |
| A-04 | Analista | Reflexivo | Backend calculando síntese | Concentrado, olhar oblíquo | Mão ao mento | Loop 2 s | Baixa | Apresentando | P2 |
| A-05 | Analista | Confiante | Progresso positivo | Sorriso contido | Polegar leve, postura expandida | 1,5 s | Média-baixa | Idle/Apresentando | P2 |
| A-06 | Analista | Organizando | Atualização do painel | Foco lateral | Gesto de "anotar" | 1,2 s | Baixa | Idle | P3 |
| A-07 | Analista | Celebração analítica | Conclusão de trilha | Satisfação genuína | Braços levantados, postura orgulhosa | 2 s | Média | Apresentando | P2 |
| C-01 | Catalisador | Ocioso | Sem interação | Sorriso leve, brilhante | Balanço expressivo, pulsar de energia | Loop | Baixa-média | Qualquer reação | P1 |
| C-02 | Catalisador | Saudação de onboarding | Início do onboarding | Sorriso largo, arregalado | Salto, "V" de boas-vindas | 2 s | Alta | Explicando | P1 |
| C-03 | Catalisador | Ouvindo | Usuário digitando (onboarding) | Arregalado, escuta ativa | Inclinação frontal, palmas abertas | Loop | Baixa-média | Celebrando resp. | P1 |
| C-04 | Catalisador | Celebrando resposta | Resposta enviada (onboarding) | Olhos em meia-lua, sorriso largo | Salto leve, gesto de aprovação | 1 s | Alta | Ouvindo/Revelação | P1 |
| C-05 | Catalisador | Revelação de trilha | Final do onboarding | Sorriso máximo, brilho total | Expansão, braços abertos apontando | 2,5 s | Muito alta | Explicando | P1 |
| C-06 | Catalisador | Explicando | Texto ativo | Expressivo, animado | Rotação ritmada, gestos amplos | Loop | Média-alta | Idle | P1 |
| C-07 | Catalisador | Incentivando | Próxima missão recomendada | Sorriso amplo, brilhante | Braço apontando para o card | 1,5 s | Alta | Idle | P1 |
| C-08 | Catalisador | Acolhimento após inatividade | Retorno do usuário | Sorriso caloroso | Aceno gentil | 1,8 s | Média | Explicando | P1 |
| C-09 | Catalisador | Surpreso positivo | Acerto inesperado/100% no expresso | "O" → sorriso largo | Recuo + salto de escala | 1,5 s | Muito alta | Celebrando conquista | P3 |
| C-10 | Catalisador | Encorajando após dificuldade | Protocolo D33 Nível 3 | Sorriso gentil | Palma aberta, proximidade | 1,5 s | Média | Explicando | P1 |
| C-11 | Catalisador | Celebrando conquista | Conclusão de missão | Cerrado em celebração, sorriso máximo | Expansão + rotação + "V" | 2,2 s | Muito alta | Explicando | P1 |
| C-12 | Catalisador | Celebração de trilha (especial) | Conclusão de trilha | Máximo, exuberante | Loop completo de vitória, aplausos | 3,5 s | Máxima | Explicando | P2 |

---

## 4. Gatilhos de interação

Esta seção mapeia eventos reais da experiência do usuário para reações de cada mascote.

| Evento da UX | Catalisador | Mentor | Analista |
|---|---|---|---|
| Início do onboarding | C-02 (Saudação) → C-03 (Ouvindo) | — | — |
| Resposta durante onboarding | C-04 (Celebrando resposta) | — | — |
| Final do onboarding | C-05 (Revelação de trilha) | — | — |
| Início de nova missão | C-07 (Incentivando) | M-02 (Saudação) | — |
| Usuário começa a digitar | — | M-04 (Curioso) | — |
| Backend processando resposta | — | M-03 (Pensativo) | — |
| Mentor exibindo resposta/feedback | — | M-08 (Explicando) | — |
| **Acerto de questão** | — | M-10 (Aprovando) | — |
| **Erro em questão** | — | M-07 (Encorajador) → M-08 (Explicando) | — |
| Mentor faz pergunta de verificação | — | M-09 (Verificando compreensão) | — |
| Dificuldade recorrente (2ª intervenção) | — | M-06 (Preocupado) → M-08 (Explicando) | — |
| Protocolo D33 Nível 3 acionado | C-10 (Encorajando após dificuldade) | — | — |
| Usuário solicita ajuda/dúvida | — | M-02 (Saudação) / M-08 (Explicando) | — |
| Conclusão de missão com sucesso | C-11 (Celebrando conquista) | M-11 (Incentivando) | — |
| Painel de progresso aberto | — | — | A-02 (Apresentando dados) |
| Recomendação de reforço exibida | — | — | A-03 (Identificando padrão) |
| Atualização do painel em tempo real | — | — | A-06 (Organizando) |
| Acerto inesperado / 100% no expresso | C-09 (Surpreso positivo) | M-05 (Surpreso) → M-10 (Aprovando) | — |
| Backend calculando síntese de trilha | — | — | A-04 (Reflexivo) |
| Conclusão de trilha | C-12 (Celebração especial) | — | A-07 (Celebração analítica) |
| Síntese "O que você demonstrou saber" exibida | — | — | A-02 (Apresentando) → A-05 (Confiante) |
| Retorno após inatividade | C-08 (Acolhimento) | — | — |
| Progresso positivo visível no painel | — | — | A-05 (Confiante) |
| Desbloqueio de conquista/badge | C-11 (Celebrando conquista) | — | — |

### 4.1 Regras anti-reação

As seguintes situações **nunca devem disparar** animações comemorativas:

- Erros de questão não disparam C-11 nem M-10.
- Erros consecutivos não intensificam a expressão de preocupação — a animação M-06 ocorre uma vez, depois retorna ao neutro.
- O Analista não exibe A-03 quando há progresso positivo no mesmo painel; as reações são mutuamente exclusivas por sessão de abertura do painel.
- Nenhum mascote exibe tristeza, decepção, frustração ou expressão de julgamento em resposta a um erro do usuário.
- A sugestão de revisão do Catalisador (C-10) nunca vem acompanhada de expressão de preocupação ou frustração — apenas encorajamento.

---

## 5. Máquinas de estados

### 5.1 Mentor — Máquina de estados

```
┌─────────────────────────────────────────────────────────────────────┐
│                          MENTOR                                      │
│                                                                      │
│   [IDLE / M-01] ──────────────────────────────────────────────────┐ │
│       ↑  ↑                                                         │ │
│       │  └─── (texto encerrado; evento resolvido)                 │ │
│       │                                                            │ │
│   ┌───┴───────────────────┐                                        │ │
│   │  ENTRADA NA TELA      │ → M-02 (Saudação) → IDLE             │ │
│   └───────────────────────┘                                        │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  BACKEND PROCESSANDO   │ → M-03 (Pensativo) ──────────────→  │ │
│   └────────────────────────┘           │                          │ │
│                                        ↓                          │ │
│   ┌────────────────────────┐   M-08 (Explicando) → IDLE          │ │
│   │  USUÁRIO DIGITANDO     │ → M-04 (Curioso) → M-03 ou IDLE    │ │
│   └────────────────────────┘                                      │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ACERTO DE QUESTÃO     │ → M-10 (Aprovando) → IDLE/M-08     │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ERRO DE QUESTÃO       │ → M-07 (Encorajador) → M-08        │ │
│   └────────────────────────┘           │                          │ │
│                               M-08 (Explicando) → IDLE           │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  DIFICULDADE RECORRENTE│ → M-06 (Preocupado) → M-08 → IDLE │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  PERGUNTA VERIFICAÇÃO  │ → M-09 (Verificando) → M-04 → ... │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ACERTO DIFÍCIL        │ → M-05 (Surpreso) → M-10 → IDLE   │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  CONCLUSÃO DE MISSÃO   │ → M-11 (Incentivando) → IDLE       │ │
│   └────────────────────────┘                                       │ │
└─────────────────────────────────────────────────────────────────────┘
```

**Regras de prioridade do Mentor:**

| Prioridade | Tipo | Comportamento |
|---|---|---|
| 1 (mais alta) | Reação a erro | M-07 interrompe qualquer estado exceto M-07 em curso |
| 2 | Reação a acerto | M-10 interrompe Idle e M-04 |
| 3 | Explicando | M-08 interrompe M-03 e M-04 |
| 4 | Transição | M-03, M-06 interrompem Idle |
| 5 (mais baixa) | Ociosidade | M-01 só ativo quando nenhuma outra animação estiver em fila |

**Regra de conflito:** nenhuma animação de reação interrompe M-08 (Explicando) enquanto o texto ainda estiver sendo exibido. A nova animação entra na fila e executa ao final do texto.

---

### 5.2 Analista de Progresso — Máquina de estados

```
┌─────────────────────────────────────────────────────────────────────┐
│                     ANALISTA DE PROGRESSO                            │
│                                                                      │
│   [IDLE / A-01] ──────────────────────────────────────────────────┐ │
│       ↑                                                            │ │
│       └─── (evento concluído; painel fechado)                     │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  PAINEL ABERTO         │ → A-02 (Apresentando) → IDLE        │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  BACKEND CALCULANDO    │ → A-04 (Reflexivo) → A-02 → IDLE   │ │
│   │  SÍNTESE               │                                      │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  RECOMENDAÇÃO REFORÇO  │ → A-03 (Identificando) → A-05/IDLE │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  PROGRESSO POSITIVO    │ → A-05 (Confiante) → IDLE/A-02     │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ATUALIZAÇÃO DO PAINEL │ → A-06 (Organizando) → IDLE        │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  CONCLUSÃO DE TRILHA   │ → A-07 (Celebração analítica)       │ │
│   │                        │   → A-02 (Apresentando síntese)     │ │
│   │                        │   → IDLE                            │ │
│   └────────────────────────┘                                       │ │
└─────────────────────────────────────────────────────────────────────┘
```

**Regras de prioridade do Analista:**

| Prioridade | Tipo | Comportamento |
|---|---|---|
| 1 | Celebração de trilha | A-07 não é interrompido após iniciado |
| 2 | Recomendação / padrão | A-03 interrompe Idle |
| 3 | Apresentação / síntese | A-02, A-04 interrompem Idle |
| 4 (mais baixa) | Ociosidade | A-01 só ativo quando nenhuma outra animação em curso |

**Regra de conflito:** A-03 e A-05 são mutuamente exclusivos na mesma abertura do painel. Se houver recomendação de reforço ativa, o Analista exibe A-03; A-05 só aparece quando não houver recomendação ativa na sessão.

---

### 5.3 Catalisador — Máquina de estados

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CATALISADOR                                  │
│                                                                      │
│   [IDLE / C-01] ──────────────────────────────────────────────────┐ │
│       ↑                                                            │ │
│       └─── (texto encerrado; evento resolvido)                    │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ONBOARDING INÍCIO     │ → C-02 → C-03 ⇄ C-04 → C-05 → C-06│ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  TEXTO ATIVO           │ → C-06 (Explicando) → IDLE          │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  PRÓXIMO PASSO (HOME)  │ → C-07 (Incentivando) → IDLE        │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  RETORNO INATIVIDADE   │ → C-08 (Acolhimento) → C-06 → IDLE │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ERRO COM PROTOCOLO D33│ → C-10 (Encorajando) → C-06 → IDLE │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  ACERTO INESPERADO     │ → C-09 (Surpreso) → C-11 → C-06    │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  CONCLUSÃO DE MISSÃO   │ → C-11 (Celebrando) → C-06 → IDLE  │ │
│   └────────────────────────┘                                       │ │
│                                                                    │ │
│   ┌────────────────────────┐                                       │ │
│   │  CONCLUSÃO DE TRILHA   │ → C-12 (Especial) → C-06 → IDLE    │ │
│   └────────────────────────┘                                       │ │
└─────────────────────────────────────────────────────────────────────┘
```

**Regras de prioridade do Catalisador:**

| Prioridade | Tipo | Comportamento |
|---|---|---|
| 1 (mais alta) | Celebração de trilha | C-12 não é interrompido após iniciado |
| 2 | Celebração de missão | C-11 interrompe C-01, C-03, C-06, C-07 |
| 3 | Onboarding (C-05) | C-05 não é interrompido após iniciado |
| 4 | Encorajamento / suporte | C-08, C-10 interrompem Idle |
| 5 | Explicando | C-06 interrompe Idle |
| 6 (mais baixa) | Ociosidade | C-01 só ativo quando nenhuma outra animação em curso |

**Regra de conflito:** C-11 e C-12 nunca ocorrem simultaneamente. Se uma conclusão de trilha for detectada, C-12 tem prioridade absoluta e C-11 não é acionado no mesmo evento. O Analista executa A-07 somente após C-12 ter iniciado a transição de saída (não simultaneamente).

---

## 6. Tipos de animação e classificação técnica

| Tipo | Descrição | Exemplos | Comportamento |
|---|---|---|---|
| **Contínua (loop)** | Executa indefinidamente até ser interrompida por evento | Idle (M-01, A-01, C-01); Pensativo (M-03); Ouvindo (C-03) | Interrompível a qualquer momento; fade-out de 200–400 ms |
| **Reação curta** | Duração fixa; executa uma vez e encerra | Aprovando (M-10), Surpreso (M-05), Celebrando (C-11) | Não interrompível enquanto em curso (exceto prioridade máxima) |
| **Transição** | Conecta dois estados; duração curta | Pensativo → Explicando; Encorajador → Explicando | Sempre segue de uma animação a outra; não tem idle entre elas |
| **Celebração especial** | Animação longa, única no contexto | C-12, C-05 | Não interrompível; executada uma vez por evento; desativada com `prefers-reduced-motion` |
| **Apresentação** | Acompanha exibição ativa de conteúdo | Explicando (M-08), Apresentando (A-02), Explicando (C-06) | Loop enquanto conteúdo visível; encerra com fade-out ao final do texto |

---

## 7. Diretrizes de implementação web

### 7.1 Formato e carregamento

- Modelos exportados em **glTF 2.0 / GLB** com skeletal rig e blendshapes.
- Cada mascote deve ter um único arquivo GLB com todas as animações nomeadas conforme os IDs desta especificação (ex.: `MENTOR_M01_IDLE`, `MENTOR_M08_EXPLAINING`).
- Utilizar **lazy loading por mascote** — o GLB do Analista não é carregado na tela de atividades; o GLB do Mentor não é carregado na tela de progresso.
- Resolução de textura: máximo 1024×1024 px para mobile; 2048×2048 para desktop. Usar compressão KTX2 (Basis Universal) quando possível.
- Renderização via **Three.js** ou biblioteca WebGL equivalente já utilizada no projeto.

> **⚠ Lacuna L-03:** A stack de renderização 3D da plataforma (Three.js, Babylon.js, R3F, ou outra) deve ser confirmada pela equipe de engenharia antes de definir a implementação do rig.

### 7.2 Máquina de estados no frontend

- Implementar um controlador de animação por mascote que:
  - Mantém o estado atual e a fila de estados.
  - Recebe eventos do sistema (acerto, erro, conclusão, etc.) via API de eventos da plataforma.
  - Executa fade-in/fade-out entre animações (blending de 150–300 ms por padrão).
  - Respeita as regras de prioridade definidas na seção 5.
  - Expõe método `triggerAnimation(id, priority)` para chamada pelos componentes da interface.

### 7.3 Acessibilidade e preferência por movimento reduzido

Quando `prefers-reduced-motion: reduce` estiver ativo:

| Tipo de animação | Comportamento alternativo |
|---|---|
| Idle contínuo (loop) | Desativado — personagem em pose estática |
| Reações curtas (M-10, M-07, C-11, etc.) | Substituído por crossfade de 200 ms para a pose-chave da expressão (sem movimento) |
| Celebrações especiais (C-12) | Substituído por pose estática de celebração com crossfade de 200 ms |
| Explicando / Apresentando | Pose de fala estática mantida enquanto o texto for exibido |
| Pensativo / Processando | Indicador de loading da interface substitui a animação do personagem |

- Todo feedback expressivo deve ter equivalente textual na interface (ex.: mensagem de encorajamento, confirmação de acerto) — a animação nunca é o único vetor de informação.
- O controle de intensidade de animações nas configurações da plataforma (conforme Design System, seção 3.5) deve mapear para: Normal (todas as animações), Reduzido (apenas reações curtas, sem loops e sem celebrações), Desativado (apenas poses estáticas).

### 7.4 Performance

- Budget de frames: animações dos mascotes não devem consumir mais de 2 ms de tempo de CPU por frame em dispositivos mobile de referência.
- Suspender loops de ociosidade quando o elemento do mascote não estiver visível na viewport (IntersectionObserver).
- Não executar animações durante scroll ativo ou carregamento de conteúdo pesado.

---

## 8. Lista priorizada de animações

### 8.1 MVP — Prioridade 1 (implementar antes do lançamento do piloto)

| ID | Mascote | Justificativa |
|---|---|---|
| M-01 | Mentor | Estado base obrigatório |
| M-02 | Mentor | Primeira interação do usuário com o Mentor |
| M-03 | Mentor | Feedback visual de processamento — essencial para percepção de resposta |
| M-06 | Mentor | Reação a dificuldade recorrente — contexto pedagógico crítico |
| M-07 | Mentor | Reação a erro — obrigatória para não deixar o erro sem resposta expressiva |
| M-08 | Mentor | Estado de explicação — onipresente no uso do chat |
| M-10 | Mentor | Confirmação de acerto — feedback positivo essencial |
| A-01 | Analista | Estado base obrigatório |
| A-02 | Analista | Único estado de apresentação do Analista — presente em toda abertura do painel |
| A-03 | Analista | Recomendação de reforço — função principal visível do Analista |
| C-01 | Catalisador | Estado base obrigatório |
| C-02 | Catalisador | Início do onboarding — primeiro contato do usuário com a plataforma |
| C-03 | Catalisador | Estado de escuta durante onboarding — cobre todo o fluxo de perguntas |
| C-04 | Catalisador | Celebração de resposta no onboarding — cria conexão emocional (D-C3) |
| C-05 | Catalisador | Revelação de trilha — momento mais impactante do onboarding |
| C-06 | Catalisador | Estado de explicação — onipresente no uso do Catalisador |
| C-07 | Catalisador | Incentivo para próxima missão — função primária na Home |
| C-08 | Catalisador | Acolhimento pós-inatividade (D-C13) |
| C-10 | Catalisador | Encorajamento pós-dificuldade (D33 Nível 3) |
| C-11 | Catalisador | Celebração de conclusão de missão — presente em toda jornada |

### 8.2 Pós-MVP — Prioridade 2 (fase seguinte ao piloto)

| ID | Mascote | Justificativa |
|---|---|---|
| M-04 | Mentor | Enriquece a percepção de atenção enquanto o usuário digita |
| M-09 | Mentor | Complementa o ciclo de verificação de compreensão |
| M-11 | Mentor | Incentivo pós-missão — o Catalisador já cobre este momento no MVP |
| A-04 | Analista | Feedback visual de processamento da síntese |
| A-05 | Analista | Reforço positivo no painel de progresso |
| A-07 | Analista | Celebração analítica ao final de trilha — ocorre após C-12 |
| C-12 | Catalisador | Celebração especial de trilha — grande impacto, mas requer produção mais custosa |

### 8.3 Backlog — Prioridade 3 (fases posteriores)

| ID | Mascote | Justificativa |
|---|---|---|
| M-05 | Mentor | Reação a acerto inesperado — específica e rara |
| A-06 | Analista | Atualização em tempo real do painel — detalhe de refinamento |
| C-09 | Catalisador | Reação a acerto inesperado — específica e rara |

---

## 9. Lacunas identificadas e recomendações

| ID | Lacuna | Impacto | Recomendação |
|---|---|---|---|
| L-01 | Especificação técnica do rig 3D (bones, blendshapes, nomenclatura) | Alto — bloqueia o animador | Definir em sessão com o animador 3D após validação desta especificação; usar como referência os parâmetros descritos na seção 1.3 |
| L-02 | Variações de C-04 (celebração de resposta no onboarding) para evitar repetição | Médio — prejudica naturalidade do onboarding | Produzir 3–4 variantes do gesto de aprovação para rotação aleatória; variantes precisam ser definidas com o animador |
| L-03 | Stack de renderização 3D do frontend (Three.js, Babylon.js, R3F, ou outra) | Alto — impacta toda a implementação | Confirmar com a equipe de engenharia antes de iniciar a implementação dos controladores de animação |
| L-04 | Cores exatas aplicadas nos materiais 3D dos mascotes (base, especular, emissão) | Alto — impacta identidade visual | O designer 3D deve receber os tokens de cor do Design System e definir o mapeamento de material antes da modelagem |
| L-05 | Definição dos eventos de API que disparam as animações (formato, payload) | Alto — impacta integração frontend/backend | A equipe de engenharia deve documentar o contrato de eventos antes do início da implementação do controlador de animação |
| L-06 | Comportamento dos mascotes em modo escuro vs. claro (reflexos, emissão de luz) | Baixo — detalhe visual | O designer 3D deve validar a leitura do personagem nos dois temas após definir os materiais (L-04) |
| L-07 | Tamanho e posicionamento dos mascotes por breakpoint (mobile, tablet, desktop) | Médio — impacta legibilidade expressiva em mobile | Definir grid de layout dos mascotes por breakpoint em colaboração com o designer UI |

---

## 10. Exemplos concretos de interação por personagem

### 10.1 Exemplo — Mentor em atividade de múltipla escolha

> **Cenário:** Usuário na Trilha 2, Missão 3. Responde uma questão sobre juros compostos de forma incorreta pela segunda vez.

1. **Usuário clica em uma alternativa errada.**
2. Backend registra o erro; identifica que é o segundo erro consecutivo na mesma competência → inclui flag no payload do Mentor.
3. Mentor recebe o payload. **M-07 (Encorajador)** é disparado: sorriso leve, inclinação frontal, gesto de apoio. Duração: 1,5 s.
4. Transição automática para **M-08 (Explicando)**: o Mentor exibe o feedback pedagógico da Decisão 32 (Tipo 1 — erro conceitual claro), com um exemplo alternativo.
5. Após o texto terminar, Mentor retorna para **M-01 (Idle)**.
6. Se for a 2ª intervenção da missão, o Analista aciona A-03 quando o painel de progresso for aberto na mesma sessão.

**O que não acontece:** nenhuma expressão de tristeza, decepção ou frustração. O mascote não recua nem demonstra desapontamento.

---

### 10.2 Exemplo — Catalisador no onboarding

> **Cenário:** Usuário novo na primeira abertura da plataforma.

1. Tela de onboarding carrega. **C-02 (Saudação)** inicia automaticamente: salto de escala, "V" de boas-vindas. Duração: 2 s.
2. Primeira pergunta exibida. Catalisador entra em **C-03 (Ouvindo)**: inclinação frontal, palmas abertas.
3. Usuário seleciona uma resposta. **C-04 (Celebrando resposta)** dispara: sorriso máximo, gesto de aprovação, escala +5%. Duração: 1 s.
4. Próxima pergunta — retorna para **C-03**. Ciclo C-03 ⇄ C-04 por cada resposta.
5. Ao final das perguntas, backend gera narrativa personalizada. **C-05 (Revelação de trilha)** dispara: expansão máxima, braços abrindo e apontando para a tela. Duração: 2,5 s.
6. Catalisador entra em **C-06 (Explicando)** ao exibir a narrativa personalizada e as trilhas.

---

### 10.3 Exemplo — Analista no painel de progresso

> **Cenário:** Usuário abre o painel de progresso após concluir 3 missões. O Analista identificou dificuldade recorrente em "leitura de extrato bancário".

1. Painel abre. **A-02 (Apresentando dados)** dispara: braço aponta para a área de dados. Duração: 2,5 s → retorna ao Idle.
2. Card de recomendação de reforço é exibido. **A-03 (Identificando padrão)** dispara: postura ereta, expressão analítica focada, dedo em pose de observação.
3. Mensagem exibida: *"Nas últimas atividades, o conceito de leitura de extrato apareceu com dificuldade. Que tal revisitar isso antes de avançar?"*
4. Após a mensagem, Analista transiciona para **A-01 (Idle)**.
5. Se o usuário aceitar a sugestão, o painel fecha e o Catalisador assume na Home com **C-07 (Incentivando)** para o card de revisão recomendada.

---

### 10.4 Exemplo — Catalisador na conclusão de trilha

> **Cenário:** Usuário conclui a Trilha 3 completa.

1. Backend confirma conclusão. **C-12 (Celebração especial)** dispara no Catalisador: loop de vitória completo, aplausos, projeção frontal. Duração: 3,5 s.
2. Durante a saída de C-12, o Analista inicia **A-07 (Celebração analítica)**: braços levantados, postura orgulhosa. Duração: 2 s. (Os dois mascotes podem estar visíveis em telas diferentes ou em sequência — ⚠ Lacuna L-07 sobre layout simultâneo.)
3. Catalisador transiciona para **C-06 (Explicando)** ao apresentar:
   - Síntese do Analista (D-A1): *"Nesta trilha você demonstrou domínio em [competência A] e [competência B]."*
   - Sugestão de próxima trilha com contexto personalizado (D-C12).
4. Catalisador retorna para **C-01 (Idle)**.

---

## 11. Governança do documento

Esta especificação é um documento vivo. Mudanças nos comportamentos dos agentes (Especificação de Agentes, Documento 4) que alterem gatilhos de interação devem ser refletidas aqui. Novas animações devem ser propostas neste documento antes de serem produzidas, garantindo consistência de personalidade e alinhamento com as decisões pedagógicas aprovadas.

**Próximos passos recomendados:**
1. Validar esta especificação com os designers 3D responsáveis pelos mascotes.
2. Resolver as lacunas L-01 a L-07 conforme prioridade antes de iniciar a produção de animações.
3. Produzir poses-chave (key poses) para as 20 animações de Prioridade 1 antes das poses de transição.
4. Definir o contrato de eventos de API (L-05) com a equipe de engenharia.
5. Validar o comportamento de `prefers-reduced-motion` com testes de usuário acessíveis.
```
