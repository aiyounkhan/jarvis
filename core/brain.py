from core.claude_client import ClaudeClient
from memory.vector_store import VectorStore
from ingestion.pc_monitor import PCMonitor

SYSTEM_PROMPT = """
You are JARVIS — a personal AI built exclusively for Anady.
You know everything about Anady over time.
You are direct, intelligent, and proactive.

RESPONSE LENGTH — this is critical:
- Match the length to what was asked. Short question = short answer.
- Conversational messages get 1-3 sentences max.
- Only go long when the task genuinely needs it — code, plans, explanations.
- Never use bullet points or numbered lists in casual conversation.
- Talk like a person, not a report.

VOICE — you speak out loud, so:
- Never use markdown. No asterisks, no bold, no headers.
- Write exactly how you'd say it out loud.
- Natural sentences only.

You will be given relevant memories from past conversations and 
Anady's current PC activity. Use both naturally in your responses.
"""

class Brain:
    def __init__(self):
        self.client = ClaudeClient()
        self.memory = VectorStore()
        self.monitor = PCMonitor()
        self.monitor.start()
        self.conversation_history = []

    def chat(self, user_input):
        # Get relevant memories
        relevant_memories = self.memory.search(user_input)

        # Get PC activity
        pc_summary = self.monitor.get_summary()

        # Build context
        context_parts = []

        if relevant_memories:
            memory_context = "Relevant memories:\n" + "\n".join(f"- {m}" for m in relevant_memories)
            context_parts.append(memory_context)

        context_parts.append(f"Current PC activity: {pc_summary}")
        context_parts.append(f"User says: {user_input}")

        augmented_input = "\n\n".join(context_parts)

        self.conversation_history.append({
            "role": "user",
            "content": augmented_input
        })

        response = self.client.think(
            messages=self.conversation_history,
            system_prompt=SYSTEM_PROMPT
        )

        self.memory.save(user_input, metadata={"role": "user"})
        self.memory.save(response, metadata={"role": "jarvis"})

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response