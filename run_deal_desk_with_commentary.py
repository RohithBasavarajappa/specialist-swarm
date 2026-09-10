"""Run the Deal Desk with a live commentary agent beside the event stream."""

import os
from pathlib import Path
from typing import Any

from anthropic import Anthropic

from run_deal_desk import main as run_deal_desk


COMMENTARY_MODEL = "claude-haiku-4-5-20251001"
COMMENTARY_SKILL = Path("skills/swarm-commentary/SKILL.md")
COMMENTARY_EVENTS = {
    "session.thread_created",
    "session.thread_status_running",
    "agent.thread_message_sent",
    "agent.thread_message_received",
    "agent.tool_use",
    "session.status_idle",
}


class SwarmCommentator:
    def __init__(self) -> None:
        self.client = Anthropic()
        self.skill = COMMENTARY_SKILL.read_text()
        self.output_path = Path("outputs/swarm-commentary.txt")
        self.output_path.parent.mkdir(exist_ok=True)
        self.output_path.write_text("")
        self.last_reply_at: float | None = None
        self.roster_size = 0
        self.replies_seen = 0
        self.latency_joke_used = False

    def observe(self, event: Any, elapsed: float) -> None:
        event_type = event.type
        if event_type not in COMMENTARY_EVENTS:
            return

        if event_type == "session.thread_created":
            self.roster_size += 1
        elif event_type == "agent.thread_message_received":
            self.replies_seen += 1
            self.last_reply_at = elapsed

        summary = self._event_summary(event, elapsed)
        if not summary:
            return

        commentary = self.client.messages.create(
            model=COMMENTARY_MODEL,
            max_tokens=100,
            system=self.skill,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "Write the next live commentary line for this event. "
                        "Return only the line, or an empty response if nothing "
                        f"useful is happening.\n\n{summary}"
                    ),
                }
            ],
        )
        line = "".join(
            block.text
            for block in commentary.content
            if getattr(block, "type", None) == "text"
        ).strip()
        if line:
            print(f"\n  [commentary] {line}", flush=True)
            with self.output_path.open("a") as output:
                output.write(f"[{elapsed:6.1f}s] {line}\n")

    def _event_summary(self, event: Any, elapsed: float) -> str:
        event_type = event.type
        agent_name = getattr(event, "agent_name", None)
        if event_type == "agent.thread_message_received":
            agent_name = getattr(event, "from_agent_name", agent_name)
        if event_type == "agent.thread_message_sent":
            agent_name = getattr(event, "to_agent_name", agent_name)

        summary = (
            f"Event: {event_type}\n"
            f"Agent: {agent_name or 'unknown'}\n"
            f"Elapsed seconds: {elapsed:.1f}\n"
            f"Threads created: {self.roster_size}\n"
            f"Specialist replies received: {self.replies_seen}"
        )
        if (
            self.last_reply_at is not None
            and elapsed - self.last_reply_at > 20
            and not self.latency_joke_used
        ):
            self.latency_joke_used = True
            summary += (
                "\nThe coordinator has been synthesising for over 20 seconds "
                "since the latest specialist reply. Add one self-aware, gentle "
                "multi-agent latency joke."
            )
        return summary


if __name__ == "__main__":
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY before running.")
    commentator = SwarmCommentator()
    run_deal_desk(event_observer=commentator.observe)
    print(f"\nLive commentary saved to {commentator.output_path}")