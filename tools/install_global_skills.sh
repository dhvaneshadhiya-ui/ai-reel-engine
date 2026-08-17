#!/usr/bin/env bash
# Reinstall the GLOBAL skills on a machine.
#
# They live in ~/.agents/skills — OUTSIDE this repo — so git cannot carry the
# INSTALLED copy and a sync bundle will never contain it. Everything else (the
# 29 in-repo skills) travels in the repo and needs nothing.
#
# Two kinds, installed differently:
#   REGISTRY  fetched from the skills registry by npx
#   LOCAL     hand-written by us; the SOURCE lives in skills-global/ inside the
#             repo so it DOES travel, and this script copies it into place.
#             Without that copy step a hand-written global skill silently fails
#             to exist on every other machine.
#
# Global is deliberate: they are advisory and useful in every project, not just
# this one. None is a router — none claims to be a default or a mandatory entry
# point — so none can contend with `news-reel` for a reel request. That was
# checked before each was installed; see CLAUDE.md.
#
#     bash tools/install_global_skills.sh
#
# Idempotent: re-running just refreshes them.
set -u

SKILLS=(
  "vercel-labs/skills@find-skills"                        # discover/install other skills
  "blader/humanizer@humanizer"                            # make an approved-shape script read human
  "jamditis/claude-skills-journalism@fact-check-workflow" # verify a claim before it becomes a beat
  "kostja94/marketing-skills@youtube-seo"                 # YouTube title / description / tags
  "social-media-skills/skills@thumbnail-design"           # the thumbnail BRIEF (we render it ourselves)
)

echo "== global skills =="
fail=0
for pkg in "${SKILLS[@]}"; do
  name="${pkg##*@}"
  printf '  %-22s ' "$name"
  if npx -y skills add "$pkg" -g -y >/tmp/gs.$$ 2>&1; then
    echo "ok"
  else
    echo "FAILED — see below"
    tail -5 /tmp/gs.$$
    fail=1
  fi
  rm -f /tmp/gs.$$
done

echo
echo "== local skills (source in skills-global/) =="
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOCAL=()
if [ -d "$REPO/skills-global" ]; then
  for src in "$REPO"/skills-global/*/SKILL.md; do
    [ -f "$src" ] || continue
    name="$(basename "$(dirname "$src")")"
    LOCAL+=("$name")
    printf '  %-22s ' "$name"
    dest="$HOME/.agents/skills/$name"
    if mkdir -p "$dest" && cp "$src" "$dest/SKILL.md"; then
      echo "ok"
    else
      echo "FAILED to copy"
      fail=1
    fi
  done
fi
[ "${#LOCAL[@]}" = "0" ] && echo "  (none)"

echo
echo "== verifying =="
missing=0
for pkg in "${SKILLS[@]}" "${LOCAL[@]:-}"; do
  [ -n "$pkg" ] || continue
  name="${pkg##*@}"
  if [ -f "$HOME/.agents/skills/$name/SKILL.md" ]; then
    printf '  ok    %-22s %s bytes\n' "$name" \
      "$(wc -c < "$HOME/.agents/skills/$name/SKILL.md" | tr -d ' ')"
  else
    printf '  MISS  %s\n' "$name"
    missing=1
  fi
done

echo
if [ "$missing" = "0" ] && [ "$fail" = "0" ]; then
  echo "all $(( ${#SKILLS[@]} + ${#LOCAL[@]} )) global skills present" \
       "(${#SKILLS[@]} registry, ${#LOCAL[@]} local)."
else
  echo "some skills did not install — read the errors above."
  exit 1
fi

cat <<'NOTE'

NOTE: one target may report
  "PromptScript does not support global skill installation"
That is a different agent runtime, not Claude Code. Claude Code installs fine
and the skill will work. Nothing to fix.
NOTE
