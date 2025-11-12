import { GoogleGenAI } from "@google/genai";
import type { UserLocation, GroundingChunk } from "../types";

const API_KEY = import.meta.env.VITE_GEMINI_API_KEY;

if (!API_KEY) {
  throw new Error("VITE_GEMINI_API_KEY environment variable not set");
}

const ai = new GoogleGenAI({ apiKey: API_KEY });

const systemInstruction = `Você é um assistente de IA para a plataforma R-IoT, um sistema de monitoramento de gado. Sua função é responder a perguntas sobre o estado do rebanho com base nos dados fornecidos no contexto.
- O contexto sempre conterá um 'RESUMO GERAL' e um 'RESUMO POR REBANHO'. Use estas seções para responder a perguntas gerais sobre a fazenda ou rebanhos específicos. O resumo do rebanho agora inclui os nomes de animais com alertas importantes, como os que estão 'Fora da área'. Use esta informação para identificar animais específicos quando perguntado.
- Se nenhum animal estiver selecionado, suas análises devem ser amplas, considerando todos os animais e rebanhos com base nos resumos.
- Se um animal específico for selecionado, seus dados aparecerão na seção 'DADOS DO ANIMAL SELECIONADO'. Use esses dados para perguntas sobre este animal, mas lembre-se que você ainda tem o contexto geral para responder sobre outros animais ou rebanhos.
- Analise o histórico de 7 dias de um animal para identificar tendências, como uma queda nos passos ou um aumento gradual da temperatura, quando relevante.
- Seja conciso e direto. Você está auxiliando um fazendeiro ou gerente de fazenda a entender os dados em tempo real. Não responda a perguntas que não sejam sobre os dados fornecidos.`;

export async function askQuestion(
  prompt: string,
  context: string,
  userLocation: UserLocation | null
): Promise<{ text: string, sources: GroundingChunk[] }> {
  try {
    const fullPrompt = `${context}\n\nPERGUNTA DO USUÁRIO: ${prompt}`;

    const response = await ai.models.generateContent({
      model: "gemini-2.5-flash",
      contents: fullPrompt,
      config: {
        systemInstruction,
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

    return { text, sources: groundingChunks };
  } catch (error) {
    console.error("Error calling Gemini API:", error);
    return { 
      text: "Desculpe, não consegui processar sua pergunta. Verifique o console para mais detalhes.",
      sources: []
    };
  }
}