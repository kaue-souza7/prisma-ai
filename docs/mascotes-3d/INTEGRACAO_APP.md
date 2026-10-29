# Integração dos mascotes 3D no Prisma.AI

**Status:** integrado ao backend e ao frontend existentes.

## 1. Arquitetura

- **Backend:** os GLBs e o manifesto ficam em `backend/app/static/mascotes/` e são servidos por `FastAPI` em `/static/mascotes`.
- **Frontend:** o palco Three.js e o controlador de animações vivem em `frontend/src/features/mascots/`.
- **Wrapper React:** `frontend/src/features/mascots/Mascot3D.tsx`.
- **Fallback:** em ambiente de teste, sem WebGL ou durante o carregamento, o componente usa o `PrismMascot` estático.

O Three.js é carregado sob demanda (dynamic import), então o bundle inicial do app não paga o custo de ~695 kB do viewer/Three.

## 2. Uso do componente

```tsx
import { Mascot3D } from '@/features/mascots/Mascot3D'

<Mascot3D
  agent="catalyst"   // catalyst | mentor | analyst
  animation="C-04"   // ID do catálogo
  priority={3}
  size={220}
/>
```

Mapeamento de agente para personagem:

| Agente do produto | Personagem 3D | GLB |
|---|---|---|
| `catalyst` | Catalisador | `catalisador.glb` |
| `mentor` | Mentor | `mentor.glb` |
| `analyst` | Analista de Progresso | `analista.glb` |

## 3. Onde está integrado

| Tela | Componente | Animação |
|---|---|---|
| Onboarding | `OnboardingPage` | `C-01` → `C-03` → `C-04` por resposta → `C-05` na revelação da trilha |
| Home | `StudentHome` | `C-03`, `C-07`, `C-10` ou `C-12` conforme a recomendação |
| Mentor e agentes | `MentorPage` | `M-01`; o chat envia `M-03` ao processar, `M-08` na resposta e `M-07` em erro |
| Aula — introdução | `LessonPlayerPage` | `M-02`, `A-02` ou `C-03` conforme o agente da etapa |
| Aula — feedback | `LessonPlayerPage` | `M-10` (acerto), `M-07` (erro) ou `M-08` (neutro) |
| Aula — resumo | `LessonPlayerPage` | `C-11` (missão) ou `C-12` (trilha) |
| Progresso | `ProgressPage` | `A-02`, `A-03` ou `A-05` conforme o insight do Analista |

## 4. Catálogo de animações

O catálogo completo fica em `frontend/src/features/mascots/core/catalog.js` e no inventário:

- `docs/mascotes-3d/INVENTARIO_ANIMACOES.md`

IDs principais:

- **Catalisador:** `C-01` idle, `C-03` ouvindo, `C-04` celebrando resposta, `C-05` revelação de trilha, `C-07` próximo passo, `C-10` encorajando, `C-11` missão concluída, `C-12` trilha concluída.
- **Mentor:** `M-01` idle, `M-02` nova missão, `M-03` processando, `M-04` digitando, `M-05` acerto difícil, `M-06` dificuldade recorrente, `M-07` erro, `M-08` explicando, `M-09` verificação, `M-10` acerto, `M-11` missão concluída.
- **Analista:** `A-01` idle, `A-02` painel aberto, `A-03` recomendação, `A-04` calculando, `A-05` progresso positivo, `A-06` atualização, `A-07` trilha concluída.

## 5. Acessibilidade e movimento reduzido

- O `MascotViewer` segue `prefers-reduced-motion` por padrão (`reducedMotion=null`).
- O wrapper usa `role="img"` e `aria-label` por agente.
- Se o navegador não suportar WebGL ou o GLB falhar, o SVG estático permanece visível.
- Em testes (`import.meta.env.MODE === 'test'`), o viewer nunca é inicializado.

## 6. Performance

- Cada GLB tem ~1,5 MiB; o carregamento é lazy por personagem.
- O piso escuro do demo foi desativado por padrão (`showFloor=false`), deixando o mascote transparente no tema do app.
- Sombras em tempo real são desativadas abaixo de 760 px no viewer original.
- O componente é desmontado e o `dispose()` é chamado ao sair da tela.

## 7. Como atualizar os assets

1. Substitua os GLBs em `backend/app/static/mascotes/` mantendo os nomes `catalisador.glb`, `mentor.glb` e `analista.glb`.
2. Atualize o `manifest.json` se os clipes mudarem.
3. Se novos IDs de animação forem adicionados, atualize `frontend/src/features/mascots/core/catalog.js` e os pontos de integração.
4. Rode `npm run build` no frontend e `pytest` no backend.

## 8. Créditos

- Modelos, rig e animações gerados pelo pipeline Three.js do pacote `identidade-agentes`.
- Three.js 0.186.1 (MIT). Veja `docs/mascotes-3d/THIRD_PARTY_NOTICES.md`.

## 9. Ajuste de expressão dos olhos

Os olhos foram ajustados para ficarem menos esbugalhados, mantendo o tamanho
geral do rosto e todas as 30 animações:

- o grupo visual de cada olho foi achatado em profundidade (`scale.z = 0.7`)
  e reduzido levemente em largura/altura (`0.92`);
- a íris, a íris interna e a pupila foram ampliadas para preencher melhor o
  branco do olho, reduzindo o aspecto de "olho de boneco".

O ajuste foi feito em `scripts/lib/model.js` no pipeline do pacote
`identidade-agentes` e os três GLBs em `backend/app/static/mascotes/` foram
regenerados. O pacote de origem permanece na raiz do projeto apenas como
referência e está ignorado pelo Git.
