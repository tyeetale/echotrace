import { defaultModel, openrouter } from "$lib/ai-config";
import { convertToModelMessages, streamText, type UIMessage } from "ai";
import type { RequestHandler } from "./$types";

export const POST: RequestHandler = async ({ request }) => {
  const { messages }: { messages: UIMessage[] } = await request.json();

  const result = streamText({
    model: openrouter(defaultModel),
    messages: convertToModelMessages(messages),
  });

  return result.toUIMessageStreamResponse();
};
