# Trilha 12 — Desafio integrador

**phase_number:** 12  
**Origem:** Fase 6, missão 6.4 → expandida de 4 para 8 simulações em 4 missões  
**Seeds:** `trail_12_v1.py`  
**Data:** 2026-10-24

---

## 1. Objetivo geral e justificativa pedagógica

O Desafio integrador é a culminação da jornada. Não testa memorização, mas a
aplicação combinada de competências das 11 trilhas anteriores em cenários
realistas de decisão financeira.

Cada cenário envolve múltiplas decisões interdependentes. As consequências de
cada escolha afetam o estado financeiro do personagem fictício nas etapas
seguintes. Não existe uma única resposta certa sem considerar o contexto.

---

## 2. Pré-requisitos

- Conclusão das trilhas 1 a 11.
- A trilha 12 não pode ser desbloqueada antes das demais.

---

## 3. Competências integradas

Esta trilha não acrescenta competências novas. Avalia a aplicação de competências
das trilhas 1–11 em contexto integrado.

| Competências principais avaliadas | Trilhas de origem |
|---|---|
| Leitura de contracheque e cálculo de líquido | 1 |
| Orçamento e priorização | 2 |
| Escolha de meio de pagamento e conferência | 3 |
| Uso consciente do cartão de crédito | 4 |
| Reserva de emergência e metas | 5 |
| Hábito de poupar no recebimento | 6 |
| Cálculo de custo de crédito e CET | 7 |
| Interpretação de dívida crescente e saída | 8 |
| Inflação e rendimento real | 9 |
| Comparação de produtos de renda fixa | 10 |
| Reconhecimento de golpe e procedimentos | 11 |

---

## 4. Mapa de conteúdo

### Missão 12.1 — Cenário: primeiro salário

**Avalia competências das trilhas 1 e 2.**

**Contexto:** Lucas acabou de receber seu primeiro salário. Ele precisa conferir o
contracheque, organizar o orçamento, pagar as contas e guardar parte do dinheiro.

#### Simulações
1. Simulação: Lucas recebe o contracheque. Quais descontos estão corretos? O líquido bate? *(1.1.3)*
2. Simulação: Com o líquido calculado, distribua o orçamento de Lucas entre 5 categorias *(2.2.1)*

---

### Missão 12.2 — Cenário: decisão de pagamento

**Avalia competências das trilhas 3 e 4.**

**Contexto:** Ana precisa pagar 4 contas de formas diferentes e usa o cartão em
uma compra parcelada. O ciclo do cartão impacta o orçamento do mês seguinte.

#### Simulações
1. Simulação: Ana tem 4 contas. Qual meio de pagamento usar em cada uma e por quê? *(3.4.2)*
2. Simulação: Ana parcelou R$ 900 em 3× no cartão. Quanto compromete nos próximos 3 meses? *(4.2.3)*

---

### Missão 12.3 — Cenário: crise financeira

**Avalia competências das trilhas 5, 7 e 8.**

**Contexto:** Carlos perdeu o emprego. Ele tem uma reserva parcial, duas dívidas
em andamento e uma oferta de crédito pessoal para cobrir os próximos meses.

#### Simulações
1. Simulação: Carlos tem reserva de R$ 2.400 e gastos essenciais de R$ 1.800/mês. Quantos meses sobrevive sem renda? Deve usar a reserva? *(5.4.1)*
2. Simulação: Carlos tem dívida A (R$ 800, 4%/mês) e dívida B (R$ 2.000, 1,5%/mês). Com R$ 400 disponíveis, qual paga primeiro? *(8.3.1)*

---

### Missão 12.4 — Cenário: alerta de fraude

**Avalia competências das trilhas 11 e 3.**

**Contexto:** Camila recebe um comprovante de Pix suspeito e uma mensagem de
phishing no mesmo dia. Ela precisa tomar decisões rápidas e corretas.

#### Simulações
1. Simulação: Camila recebeu comprovante de Pix por WhatsApp antes de liberar o produto. O que ela faz? *(11.2.1)*
2. Simulação: Camila percebeu que enviou R$ 600 para o número errado. Quais são as próximas ações em ordem? *(11.4.1, 11.4.2)*

---

## 5. Critérios de avaliação

O Desafio integrador avalia:
1. A decisão tomada (correta ou não na maioria dos critérios)
2. O raciocínio apresentado nas respostas abertas (quando aplicável)
3. A coerência das escolhas com as consequências financeiras do cenário

As simulações têm consequências encadeadas: uma decisão ruim na simulação 1
afeta o contexto da simulação 2 do mesmo cenário.

---

## 6. Regras de implementação

- Apenas `simulation` como tipo de atividade (conforme D-T9).
- Cada simulação tem `scenario` detalhado, 2–4 opções e feedback explicativo para cada escolha.
- As decisões incorretas mostram consequências, não apenas "errado".
- As decisões corretas confirmam o raciocínio e conectam com a competência avaliada.
- Não existem alternativas "obviamente absurdas" — todas as opções representam escolhas reais que pessoas fazem.

---

## 7. Relações com outras trilhas

Esta trilha é a culminação de todas as anteriores. Não tem relações de expansão
futura; é avaliativa e integradora por natureza.
