import { GoogleGenAI } from "@google/genai";
import type { UserLocation, GroundingChunk } from "../types";

const systemInstruction = `Você é um assistente de IA para a plataforma R-IoT, um sistema de monitoramento de gado. Sua função é responder a perguntas sobre o estado do rebanho com base nos dados fornecidos no contexto.
- O contexto sempre conterá um 'RESUMO GERAL' e um 'RESUMO POR REBANHO'. Use estas seções para responder a perguntas gerais sobre a fazenda ou rebanhos específicos. O resumo do rebanho agora inclui os nomes de animais com alertas importantes, como os que estão 'Fora da área'. Use esta informação para identificar animais específicos quando perguntado.
- Se nenhum animal estiver selecionado, suas análises devem ser amplas, considerando todos os animais e rebanhos com base nos resumos.
- Se um animal específico for selecionado, seus dados aparecerão na seção 'DADOS DO ANIMAL SELECIONADO'. Use esses dados para perguntas sobre este animal, mas lembre-se que você ainda tem o contexto geral para responder sobre outros animais ou rebanhos.
- Analise o histórico de 7 dias de um animal para identificar tendências, como uma queda nos passos ou um aumento gradual da temperatura, quando relevante.
- Seja conciso e direto. Você está auxiliando um fazendeiro ou gerente de fazenda a entender os dados em tempo real. Não responda a perguntas que não sejam sobre os dados fornecidos.`;

interface GeminiConfig {
  apiKey: string;
  model: string;
  temperature: number;
}

export async function askQuestion(
  prompt: string,
  context: string,
  userLocation: UserLocation | null,
  config: GeminiConfig
): Promise<{ text: string, sources: GroundingChunk[] }> {
  try {
    console.log('geminiService - Configuração recebida:', {
      model: config.model,
      temperature: config.temperature,
      hasApiKey: !!config.apiKey,
      apiKeyPrefix: config.apiKey?.substring(0, 10) + '...'
    });

    if (!config.apiKey) {
      console.warn('geminiService - Chave da API não configurada!');
      return {
        text: "Por favor, configure uma chave da API do Gemini nas Configurações.",
        sources: []
      };
    }

    console.log('geminiService - Inicializando GoogleGenAI...');
    const ai = new GoogleGenAI({ apiKey: config.apiKey });
    const fullPrompt = `${context}\n\nPERGUNTA DO USUÁRIO: ${prompt}`;

    console.log('geminiService - Gerando conteúdo com modelo:', config.model);
    const response = await ai.models.generateContent({
      model: config.model,
      contents: fullPrompt,
      config: {
        systemInstruction,
        temperature: config.temperature,
        tools: [{ googleMaps: {} }],
      },
      ...(userLocation && {
        toolConfig: {
          retrievalConfig: {
            latLng: {
              latitude: userLocation.latitude,
              longitude: userLocation.longitude,
            },
          },
        },
      }),
    });

    const text = response.text;
    const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];

    console.log('geminiService - Resposta recebida com sucesso!');
    return { text, sources: groundingChunks };
  } catch (error) {
    console.error("geminiService - Erro ao chamar API do Gemini:", error);
    return {
      text: "Desculpe, não consegui processar sua pergunta. Verifique a chave da API e tente novamente. Erro: " + (error instanceof Error ? error.message : String(error)),
      sources: []
    };
  }
}