# Script — claude-eating-tokens

Your Claude bill is mostly input, not output.

Here's why: almost every token-saving skill you've seen cuts your cheapest tokens.

Anthropic's own docs explain it: the model remembers nothing between messages, so every turn re-sends your entire conversation.

That history is the input — and most of your bill.

So take caveman. A hundred thousand stars, and it does cut output — sixty-five percent on its own benchmark.

But its README has an "honest number warning."

The skill only shrinks output, input is untouched, and it adds one to one and a half thousand input tokens every turn.

It trims the cheapest half and adds to the expensive one.

So here are three that move the other half.

One: see it. Run ccusage, or put claude-hud in your status line. You can't cut what you can't measure.

Two: stop rebuilding what exists. Ponytail makes Claude check the standard library first.

Three: between two unrelated tasks, clear. Compact re-reads everything to summarise it. Clear costs nothing.

These run with your agent's permissions — read them first.

Start with the expensive half, not the cheapest.
