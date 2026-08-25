# Script — claude-eating-tokens

Your one-line question just re-read the entire conversation.

And the habits you use to save tokens are the ones making that expensive.

Here's why: Claude remembers nothing between messages. So every turn, Claude Code re-sends all of it — system prompt, project context, every reply, every tool result — just to answer the next line.

Caching is the only reason that's survivable: that re-read bills at roughly ten percent of the normal input rate.

But the match has to be exact. Change anything near the top, and everything after it is recomputed at full price.

So switching models mid-task does it. Changing effort does it. Toggling an MCP server does it.

And so does compact — the command people run to save tokens. To write that summary, Claude re-reads the whole thing it's summarizing, so on a session you've come back to cold, that's the most expensive compact you'll run.

Clear costs nothing.

So: check context before you optimize. Pick your model at the start. And between two unrelated tasks, clear — don't compact.
