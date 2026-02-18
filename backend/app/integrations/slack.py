"""
Slack Bot Integration
======================
Handles /ask slash command and feedback buttons.
Uses Slack Bolt SDK with FastAPI adapter.
"""

import os
from typing import Optional

from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from loguru import logger

from app.services.query_pipeline import QueryPipeline
from app.config import get_settings

settings = get_settings()


def create_slack_app() -> Optional[App]:
    """
    Create and configure the Slack Bolt app.
    Returns None if Slack tokens are not configured.
    """
    if not settings.SLACK_BOT_TOKEN or not settings.SLACK_SIGNING_SECRET:
        logger.warning(
            "Slack integration disabled — SLACK_BOT_TOKEN or "
            "SLACK_SIGNING_SECRET not configured"
        )
        return None

    app = App(
        token=settings.SLACK_BOT_TOKEN,
        signing_secret=settings.SLACK_SIGNING_SECRET,
    )

    pipeline = QueryPipeline()

    # ── Slash Command: /ask ──────────────────────────────────

    @app.command("/ask")
    async def handle_ask(ack, command, say):
        """Handle the /ask slash command."""
        await ack("🔍 Searching company docs...")

        user_id = command["user_id"]
        question = command["text"]

        if not question:
            await say("Please provide a question! Usage: `/ask What is the PTO policy?`")
            return

        try:
            result = await pipeline.process(
                question=question,
                user_id=user_id,
                user_role="general",  # Default for Slack; enhance with user mapping
            )

            blocks = _format_slack_response(result)
            await say(
                blocks=blocks,
                text=result["answer"],
                thread_ts=command.get("thread_ts"),
            )

        except Exception as e:
            logger.error(f"Slack query failed: {e}")
            await say(f"❌ Sorry, I encountered an error: {str(e)}")

    # ── Feedback Buttons ─────────────────────────────────────

    @app.action("feedback_helpful")
    async def handle_helpful(ack, body, action):
        """Handle positive feedback button click."""
        await ack()
        query_id = action["value"]
        logger.info(f"Positive feedback for query: {query_id}")

    @app.action("feedback_not_helpful")
    async def handle_not_helpful(ack, body, action):
        """Handle negative feedback button click."""
        await ack()
        query_id = action["value"]
        logger.info(f"Negative feedback for query: {query_id}")

    logger.info("✅ Slack bot initialized successfully")
    return app


def _format_slack_response(result: dict) -> list:
    """Format the RAG result into Slack Block Kit blocks."""
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*Answer:*\n{result['answer']}",
            },
        },
        {"type": "divider"},
    ]

    # Add sources
    if result.get("sources"):
        source_text = ", ".join(
            [f"📎 {s['title']} ({s['source']})" for s in result["sources"]]
        )
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*Sources:* {source_text}",
                }
            ],
        })

    # Add confidence badge
    confidence = result.get("confidence", "unknown")
    confidence_emoji = {"high": "🟢", "medium": "🟡", "low": "🔴"}.get(
        confidence, "⚪"
    )
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": (
                    f"{confidence_emoji} Confidence: *{confidence}* | "
                    f"⏱️ {result.get('response_time_ms', '?')}ms"
                ),
            }
        ],
    })

    # Add feedback buttons
    blocks.append({
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "👍 Helpful"},
                "action_id": "feedback_helpful",
                "value": result.get("query_id", "unknown"),
            },
            {
                "type": "button",
                "text": {"type": "plain_text", "text": "👎 Not Helpful"},
                "action_id": "feedback_not_helpful",
                "value": result.get("query_id", "unknown"),
            },
        ],
    })

    return blocks
