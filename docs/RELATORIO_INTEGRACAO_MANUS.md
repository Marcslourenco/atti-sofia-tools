# RELATORIO_INTEGRACAO_MANUS

## 1. Objetivo
Adicionar uma camada cognitiva plugável ao sistema atual do avatar Sofia sem alterar backend, frontend ou pipeline de TTS já existente.

## 2. Princípio de integração
A inteligência deve entrar **antes do TTS** e **sobre** a estrutura atual.

Fluxo recomendado:
**input do usuário -> classificador leve de intenção/setor -> memória de sessão -> RAG -> gerador de resposta Sofia -> payload final -> TTS atual -> áudio ao frontend**

## 3. Onde conectar no backend atual
Endpoint atual informado:
`/api/avatar/speak`

### Recomendação prática
No handler do endpoint, antes da chamada ao TTS:
1. receber texto ou transcrição do usuário
2. carregar contexto da sessão
3. identificar intenção e setor
4. consultar RAG
5. montar resposta final em texto
6. enviar texto final ao TTS já existente
7. devolver payload compatível com o frontend atual

## 4. Pipeline detalhado
### Etapa A — Input
- texto vindo do frontend ou de STT
- session_id
- metadados opcionais: página, produto, estágio do funil

### Etapa B — Memória curta
Salvar no mínimo:
- intenção atual
- setor identificado
- entidades relevantes
- último tópico
- último CTA sugerido
- histórico curto de 3 a 6 turnos

### Etapa C — RAG
- usar `estrutura_chunks.json` como base documental
- usar `embeddings.json` como vetor inicial
- filtrar primeiro por setor quando possível
- recuperar top_k=4
- remontar contexto com no máximo 3 a 4 chunks finais

### Etapa D — Orquestração da resposta
Entradas:
- prompt de sistema
- regras conversacionais
- contexto recuperado
- memória da sessão
- intenção atual

Saídas desejadas:
- texto natural para voz
- emoção
- intenção dominante
- next_step opcional

### Etapa E — TTS
- usar o TTS atual sem mudança estrutural
- só trocar a qualidade do texto que entra no TTS

## 5. Formato de resposta esperado
```json
{
  "text": "...",
  "emotion": "friendly",
  "intent": "comercial",
  "audio": "base64"
}
```

## 6. Compatibilidade com o sistema atual
### O que permanece igual
- backend principal
- frontend
- endpoint `/api/avatar/speak`
- motor de TTS

### O que entra de novo
- classificador de intenção/setor
- camada de memória de sessão
- motor RAG
- política de variação de linguagem
- estratégia comercial da Sofia

## 7. Estratégia RAG recomendada
- chunk_size ideal: 420 caracteres
- overlap: 60 caracteres
- top_k: 4
- fallback: resposta curta + pergunta mínima de contexto
- filtro inicial por setor: saúde, automotivo, governo, comercial, institucional

## 8. Observação sobre embeddings
Este pacote já traz um `embeddings.json` funcional para smoke test e estruturação inicial do RAG. Em produção, recomenda-se substituir por embeddings semânticos multilíngues mais fortes, mantendo a mesma estrutura de documentos e metadados.

## 9. Melhorias futuras
1. memória de conversa persistente por usuário
2. personalização por segmento e conta
3. scoring de leads por comportamento conversacional
4. analytics de objeções e perdas
5. roteamento inteligente humano/avatar
6. avaliação contínua de qualidade das respostas

## 10. Roadmap sugerido
### Fase 1 — Plug-in cognitivo
Adicionar prompts, regras, memória curta e RAG no endpoint existente.

### Fase 2 — Piloto mensurável
Escolher um caso de uso prioritário e medir:
- taxa de conclusão
- conversão
- tempo de atendimento
- qualidade percebida

### Fase 3 — Escala
Expandir por setor, canal e jornada.
