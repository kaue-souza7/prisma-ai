# Critérios de domínio e progressão — Fase 1

**Arquivo:** `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md`  
**Versão:** 1.0 — proposta técnica para validação de produto  
**Data:** 21/10/2026  
**Implementação:** `backend/app/modules/progress/service.py` e `backend/app/modules/journey/service.py`

> **Natureza desta decisão:** os critérios abaixo são explícitos, reproduzíveis
> e já estão implementados. A redação pedagógica e a intensidade dos limiares
> ainda precisam de aprovação formal do responsável de produto. Não são regras
> inventadas em tempo de execução: o backend é a autoridade e a IA não altera
> nenhum desses estados.

---

## 1. Princípios

1. **Conclusão de missão** exige evidência em todas as atividades ativas.
2. **Domínio de competência** exige evidência em todas as atividades ligadas
   àquela competência, não apenas participação.
3. **Erro não bloqueia para sempre**: o estudante pode tentar novamente.
4. **Reforço é um sinal pedagógico**, não uma punição.
5. **Pontuação e domínio são coisas diferentes**: a pontuação recompensa a
   constância; o domínio descreve a evidência de aprendizagem.
6. **A IA não concede pontos, conquistas ou desbloqueios.**

---

## 2. Conclusão de missão

Uma missão é concluída quando:

- todas as atividades ativas da missão tiverem evidência;
- atividades objetivas (`multiple_choice` e `simulation`) tiverem ao menos uma
  resposta correta;
- atividades abertas tiverem ao menos uma resposta registrada.

Ao concluir:

| Situação | Pontos |
|---|---:|
| Nenhuma resposta incorreta registrada na missão | 100 |
| Qualquer resposta incorreta registrada | 70 |

A pontuação da missão não é a soma de `activities.points_value`; os pontos das
atividades são apenas informativos na interface. A regra de 100/70 é única e
está em `calculate_mission_score()`.

**Nota mínima:** `missions.passing_score = 70`. Como uma missão concluída vale
no mínimo 70, a conclusão já representa a nota mínima. O campo permanece para
compatibilidade e futuras regras.

**Respostas abertas:** enquanto não houver IA, são registradas e contam para a
conclusão, mas não penalizam a pontuação. A avaliação qualitativa entra na
Etapa 2, sem alterar retroativamente pontos já concedidos.

---

## 3. Critérios por competência

### 3.1 Regra geral

| Status | Critério |
|---|---|
| `not_started` | Nenhuma evidência registrada nas atividades ligadas. |
| `developing` | Existe alguma evidência, mas falta resposta correta em atividade objetiva ou falta registro em resposta aberta. |
| `demonstrated` | Todas as atividades ligadas têm a evidência exigida: correta nas objetivas e registrada nas abertas. |

A competência é considerada **essencial** ou **complementar** pelo campo
`competencies.is_essential`. Os critérios de conclusão da missão já exigem todas
as atividades; a distinção fica registrada para o painel e para reforço.

### 3.2 Mapa da Fase 1

| Código | Competência | Essencial | Evidências |
|---|---|:---:|---|
| 1.1.1 | Distinguir salário bruto de líquido | sim | MC 1.1 + resposta aberta 1.1 |
| 1.1.2 | Identificar descontos do contracheque | não | MC 1.2 + resposta aberta 1.1 |
| 1.1.3 | Calcular salário líquido | sim | MC 1.3 |
| 1.2.1 | Diferenciar necessidades de desejos | sim | MC 2.1 + resposta aberta 2.1 |
| 1.2.2 | Priorizar gastos com renda limitada | sim | MC 2.3 + resposta aberta 2.1 |
| 1.2.3 | Reconhecer que o contexto muda a classificação | não | MC 2.2 + resposta aberta 2.1 |
| 1.3.1 | Distribuir a renda entre prioridades | sim | MC 3.1 + resposta aberta 3.1 + simulação 3.1 |
| 1.3.2 | Justificar prioridades pelas consequências | sim | resposta aberta 3.1 + simulação 3.1 |
| 1.3.3 | Reconhecer o valor de separar a reserva no início | não | MC 3.2 |

> A resposta aberta 1.1 é compartilhada por 1.1.1 e 1.1.2; a resposta aberta 2.1
> por 1.2.1, 1.2.2 e 1.2.3; a resposta aberta 3.1 e a simulação por 1.3.1 e 1.3.2.

---

## 4. Sinal de reforço

O campo `reinforcement_suggested` é recalculado a cada resposta:

- **2 atividades objetivas diferentes** com erro na mesma competência; ou
- **3 tentativas incorretas na mesma atividade**, quando a competência tem
  apenas uma evidência objetiva disponível.

O sinal é removido quando a competência passa a `demonstrated`.

Justificativa: a primeira regra segue a especificação dos agentes (dificuldade
em mais de uma atividade); a segunda evita que competências com uma única
atividade objetiva nunca recebam apoio. O limiar de 3 tentativas é uma proposta
para o MVP e deve ser validado com dados do piloto.

O reforço **não**:
- reduz pontos retroativamente;
- bloqueia a próxima missão;
- altera a conclusão da fase;
- aciona conteúdo gerado por IA nesta etapa.

---

## 5. Progressão e desbloqueio

### 5.1 Regras implementadas

1. A **Fase 1** começa disponível.
2. A primeira missão obrigatória da fase começa disponível.
3. Cada missão obrigatória seguinte é liberada quando **todas as missões
   obrigatórias anteriores da mesma fase** estiverem concluídas.
4. Missões opcionais (`is_required = false`) ficam disponíveis quando a fase
   está disponível e não bloqueiam a sequência.
5. Uma fase só é liberada quando **todas as missões obrigatórias da fase
   anterior** estiverem concluídas.
6. Uma fase sem missões obrigatórias **não** é considerada concluída; portanto,
   não libera a fase seguinte.
7. Os endpoints `start` e `submit` retornam **403** para missão bloqueada.

### 5.2 Fase 1

```
Fase 1 disponível
  └── Missão 1.1 disponível
        └── Missão 1.2 após concluir 1.1
              └── Missão 1.3 após concluir 1.2
                    └── Fase 2 após concluir 1.1, 1.2 e 1.3
```

As Fases 2–6 aparecem no mapa, mas permanecem bloqueadas e sem conteúdo até
serem produzidas. Isso é intencional: o mapa mostra o horizonte, não promete
conteúdo inexistente.

### 5.3 Conquistas

- `primeiro_passo`: onboarding concluído.
- `planejador_iniciante`: as três missões obrigatórias da Fase 1 concluídas.
- `sem_duvidas`: missão concluída sem nenhuma resposta incorreta.

A conquista de fase é concedida apenas quando **todas** as missões obrigatórias
existentes na fase estão concluídas. Com o conteúdo da migration `0002`, são
exatamente três na Fase 1.

---

## 6. Casos de teste obrigatórios

| Cenário | Resultado esperado |
|---|---|
| Abrir missão 1.2 sem concluir 1.1 | 403 e status `locked` |
| Concluir 1.1 | 1.2 passa a `available` |
| Acertar tudo na primeira tentativa | 100 pontos e `sem_duvidas` |
| Errar e depois acertar | 70 pontos, sem `sem_duvidas` |
| Refazer missão concluída | Não duplica pontos |
| Acertar atividade objetiva, sem responder a aberta ligada | Competência `developing` |
| Responder a aberta depois | Competência `demonstrated` |
| 3 erros na única atividade objetiva | `reinforcement_suggested = true` |
| Concluir as três missões | `planejador_iniciante` |
| Fase 2 antes da Fase 1 completa | Permanece bloqueada |

Cobertura automatizada:
`backend/tests/test_progression_api.py` (integração, requer PostgreSQL) e
`backend/tests/test_gamification.py` (unitário).

---

## 7. Aprovação pendente

- [ ] Produto validar os limiares de reforço (2 atividades / 3 tentativas).
- [ ] Produto validar que respostas abertas contam para conclusão sem IA.
- [ ] Produto validar a sequência obrigatória das três missões.
- [ ] Jurídico validar a base legal e o texto de consentimento do onboarding.
- [ ] Após o piloto, revisar os critérios com dados reais de aprendizagem.

Até a aprovação, os critérios estão implementados como **proposta versionada**,
não como decisão pedagógica final.
