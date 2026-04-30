from core.claude_client import ClaudeClient
from memory.vector_store import VectorStore

SYSTEM_PROMPT = """
You are JARVIS — a personal AI built exclusively for Anady.
You know everything about Anady over time.
You are direct, intelligent, and proactive.
You help with anything — coding, study, life, decisions.
You never say you can't do something without trying first.

You will be given relevant memories from past conversations at the start of each message.
Use them naturally — like you actually remember, not like you're reading from a file.
"""

class Brain:
    def __init__(self):
        self.client = ClaudeClient()
        self.memory = VectorStore()
        self.conversation_history = []

    def chat(self, user_input):
        # Search memory for anything relevant
        relevant_memories = self.memory.search(user_input)

        # Build context with memories injected
        if relevant_memories:
            memory_context = "Relevant memories:\n" + "\n".join(f"- {m}" for m in relevant_memories)
            augmented_input = f"{memory_context}\n\nUser says: {user_input}"
        else:
            augmented_input = user_input

        self.conversation_history.append({
            "role": "user",
            "content": augmented_input
        })

        response = self.client.think(
            messages=self.conversation_history, 
            system_prompt=SYSTEM_PROMPT
        )

        # Save both sides to memory
        self.memory.save(user_input, metadata={"role": "user"})
        self.memory.save(response, metadata={"role": "jarvis"})

        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })

        return response