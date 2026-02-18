"""
LLM Generation Service
=======================
Generates citation-backed answers using OpenAI GPT-4.
Takes assembled context from retrieval and produces a structured response.
"""

from typing import List, AsyncGenerator

import openai
from loguru import logger

from app.config import get_settings

settings = get_settings()


# ── System Prompt ────────────────────────────────────────────

SYSTEM_PROMPT = """You are an internal company knowledge assistant.
Your job is to answer employee questions using ONLY the provided context.

RULES:
1. Answer ONLY based on the provided context
2. If the context doesn't contain enough information, say "I don't have enough information in the available documents to answer this question."
3. Always cite your sources using [Source N] format
4. Be concise but thorough
5. Never make up information not in the context
6. If multiple sources agree, synthesize the answer
7. Format your response using markdown for readability
"""


def build_prompt(context: str, question: str) -> list:
    """Construct the LLM prompt with system instructions, context, and question."""
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"""CONTEXT:
{context}

QUESTION: {question}

Provide a clear, accurate answer with source citations [Source N].
""",
        },
    ]


class LLMGenerator:
    """Generate answers using retrieved context and GPT-4."""

    def __init__(
        self,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        api_key: str = None,
    ):
        self.model = model or settings.LLM_MODEL
        self.temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE
        self.max_tokens = max_tokens or settings.LLM_MAX_TOKENS
        self.client = openai.OpenAI(
            api_key=api_key or settings.OPENAI_API_KEY
        )

    async def generate(self, context: str, question: str) -> dict:
        """
        Generate an answer from context.

        Args:
            context: Assembled context from retrieval (formatted chunks).
            question: The user's original question.

        Returns:
            Dict with answer, model info, and token usage.
        """
        messages = build_prompt(context, question)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )

            answer = response.choices[0].message.content
            usage = response.usage

            logger.info(
                f"LLM generated answer: {len(answer)} chars, "
                f"{usage.total_tokens} tokens used"
            )

            return {
                "answer": answer,
                "model": self.model,
                "tokens_used": {
                    "prompt": usage.prompt_tokens,
                    "completion": usage.completion_tokens,
                    "total": usage.total_tokens,
                },
            }

        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            raise

    async def generate_stream(
        self, context: str, question: str
    ) -> AsyncGenerator[str, None]:
        """
        Stream response token-by-token for real-time delivery.

        Yields:
            Individual tokens as they are generated.
        """
        messages = build_prompt(context, question)

        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            logger.error(f"LLM streaming failed: {e}")
            raise
