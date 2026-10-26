# Guia de produção de conteúdo

**Público:** responsável de produto, redatores e revisores pedagógicos.  
**Objetivo:** transformar uma missão escrita em conteúdo válido para o banco,
sem depender da IA e sem alterar o código de negócio.

---

## 1. Fontes e destino

| Etapa | Arquivo/ferramenta |
|---|---|
| Rascunho editorial em Markdown | `docs/fase-1-primeiro-salario.md` |
| Contrato dos campos | `docs/ESQUEMA_CONTEUDO_ATIVIDADES.md` |
| Conteúdo estruturado da Fase 1 | `backend/app/modules/content/seeds/phase_1_v1.py` |
| Carga no banco | migration `backend/alembic/versions/0002_phase_1_content.py` |
| Critérios pedagógicos | `docs/CRITERIOS_DOMINIO_E_PROGRESSAO_FASE_1.md` |

O Markdown é a referência editorial. O seed é a fonte executável. Os dois
precisam contar a mesma história.

---

## 2. Estrutura obrigatória de uma missão

1. **Número e nome** — ex.: `1.1 — De onde vem o dinheiro?`.
2. **Descrição** — uma frase sobre o que o estudante saberá fazer.
3. **Competências** — de 1 a 4, com código no padrão `fase.missão.n`.
4. **Conteúdo de apoio** — pelo menos uma explicação, um exemplo e uma dica.
5. **Atividades** — 3 a 5, incluindo uma resposta aberta.
6. **Critérios de avaliação da resposta aberta** — observáveis e curtos.
7. **Feedback** — correto e incorreto, explicando o raciocínio.

### Competências essenciais

Marque como essencial a competência sem a qual a missão perde o sentido. Cada
competência essencial precisa de pelo menos uma atividade objetiva. Uma
competência pode aparecer em mais de uma atividade.

### Atividades

| Tipo | Uso | Pontos |
|---|---|---:|
| `multiple_choice` | Verificar um conceito objetivo. | 10 |
| `simulation` | Decidir em um cenário realista. | 20 |
| `open_text` | Pedir explicação com as próprias palavras. | 0 |

A pontuação da missão continua sendo 100/70; os pontos por atividade são
informativos. Não prometa ao estudante que a soma das atividades é a nota.

---

## 3. Voz e pedagogia

- Fale com o estudante por **você**, em português brasileiro.
- Comece pelo concreto: salário, conta, mercado, transporte.
- Explique o "porquê", não só a regra.
- No feedback incorreto, nomeie o equívoco sem julgar a pessoa.
- Use valores fictícios e diga que são fictícios.
- Evite recomendação de investimento, produto bancário ou decisão pessoal.
- Não use medo, vergonha ou urgência artificial.
- Datas e valores legais precisam de fonte e revisão anual.

### Exemplo de feedback ruim

> Errado. A resposta era B.

### Exemplo de feedback adequado

> O salário bruto é o valor combinado antes dos descontos. O líquido é o que cai
> na conta depois de INSS, imposto e outros descontos. Por isso o valor recebido
> costuma ser menor.

---

## 4. Como transformar Markdown em seed

O conteúdo da Fase 1 fica em `PHASE_1_V1`, com esta forma:

```python
{
    "number": 1,
    "name": "De onde vem o dinheiro?",
    "description": "...",
    "order": 1,
    "is_required": True,
    "passing_score": 70,
    "competencies": [
        {"code": "1.1.1", "name": "...", "description": "...", "is_essential": True},
    ],
    "activities": [
        {
            "order": 1,
            "activity_type": "multiple_choice",
            "points_value": 10,
            "content": { ... },
        },
    ],
    "content_items": [
        {
            "content_type": "explanation",
            "title": "...",
            "order": 1,
            "body": "Markdown...",
        },
    ],
}
```

Ao criar uma nova versão:

1. copie `phase_1_v1.py` para `phase_1_v2.py`;
2. altere apenas o conteúdo revisado;
3. crie uma migration que chame `seed_phase_1(bind, PHASE_1_V2)`;
4. não edite a migration antiga.

O `seed_phase_1()` faz upsert por chave natural e preserva IDs de atividades
já respondidas.

---

## 5. Validação local

```bash
cd backend

# Contrato, competências e presença de conteúdo
python -m pytest tests/test_content_schema.py -q

# Toda a suíte unitária
python -m pytest -q

# Com PostgreSQL e conteúdo aplicado
docker compose exec backend alembic upgrade head
docker compose exec backend pytest -q
```

Antes de publicar, verifique também:

```bash
docker compose exec frontend npm test -- --run
docker compose exec frontend npm run build
```

---

## 6. Checklist de revisão

### Produto
- [ ] A missão conversa com o objetivo da fase.
- [ ] O nível de leitura é adequado ao público 18–24.
- [ ] A atividade aberta pede explicação, não decoreba.
- [ ] Os critérios de avaliação são observáveis.
- [ ] A carga horária estimada é compatível com uma sessão curta.

### Pedagógico
- [ ] Cada competência essencial tem evidência objetiva.
- [ ] Há feedback para acerto e para erro.
- [ ] O feedback incorreto explica o raciocínio.
- [ ] A simulação tem uma decisão e uma consequência claras.
- [ ] Não há ambiguidade entre duas alternativas corretas.

### Conteúdo financeiro
- [ ] Valores, alíquotas e regras estão datados.
- [ ] Fontes oficiais foram conferidas.
- [ ] O texto não recomenda produto ou investimento.
- [ ] Termos técnicos são explicados na primeira aparição.

### Privacidade e segurança
- [ ] Nenhum dado bancário é solicitado.
- [ ] Nenhum dado pessoal real aparece nos exemplos.
- [ ] O texto de consentimento está alinhado com a política vigente.

---

## 7. Publicação e correção

- O seed da migration `0002` insere os itens de conteúdo como publicados.
- O endpoint do estudante só retorna `content_items.is_published = true`.
- Para retirar um conteúdo do ar, use `PATCH /api/v1/content/{item_id}/publish`
  após a área administrativa estar disponível, ou uma migration de correção.
- Correções factuais devem gerar uma nova versão e registrar a data da revisão.

---

## 8. O que fica para a etapa com IA

- Avaliação automática de respostas abertas.
- Feedback personalizado do Mentor.
- Recomendação de reforço gerada pelo Analista.
- Perguntas adaptativas geradas em tempo real.

Nada disso muda o contrato acima: a IA lê `evaluation_criteria`, produz uma
análise e o **backend** continua decidindo pontos, conclusão e desbloqueio.
