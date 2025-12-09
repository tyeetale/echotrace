import { OPENROUTER_API_KEY } from "$env/static/private";
import { createOpenRouter } from "@openrouter/ai-sdk-provider";

export const openrouter = createOpenRouter({
  apiKey: OPENROUTER_API_KEY,
});

// Choose your preferred free model
export const defaultModel = "z-ai/glm-4.5-air:free";
