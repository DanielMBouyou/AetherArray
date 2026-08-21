#!/usr/bin/env bash
# Lightweight checks on the repository documentation.
# Deliberately minimal: these must stay fast and dependency free.
set -u
status=0

fail() { echo "FAIL: $*"; status=1; }

# 1. The em dash is banned (see CONVENTIONS.md, section 6).
if grep -rlP '\x{2014}' --include='*.md' . 2>/dev/null | grep -q .; then
  echo "Files containing an em dash:"
  grep -rlP '\x{2014}' --include='*.md' . 2>/dev/null
  fail "em dash present"
fi

# 2. Public documentation is written in English. This looks for a few very common
#    French function words as whole words. It is a tripwire, not a translator.
fr='\b(le|la|les|des|une|nous|pour|avec|dans|cette|qui|sont|donc|mais|sans|leur|peut|doit|etre|être|tres|très|ainsi|cela|chaque|entre|selon|aussi)\b'
if grep -rniEl "$fr" --include='*.md' . 2>/dev/null | grep -q .; then
  echo "Files with suspected French prose:"
  grep -rniE "$fr" --include='*.md' . 2>/dev/null | head -20
  fail "French prose detected in public documentation"
fi

# 3. Every decision record carries the mandatory sections.
for f in decisions/[0-9][0-9][0-9][0-9]-*.md; do
  [ -e "$f" ] || continue
  case "$f" in *0000-template.md) continue;; esac
  for section in "## Question" "## Options considered" "## Evidence" "## Decision" "## Known limitations" "## Conditions for reopening"; do
    grep -qF "$section" "$f" || fail "$f: missing section ($section)"
  done
done

# 4. Structural documents must exist.
for f in README.md CONVENTIONS.md ROADMAP.md docs/scope.md docs/uncertainties.md \
         research/state-of-the-art.md benchmarks/methodology.md experiments/plan.md; do
  [ -e "$f" ] || fail "$f: expected file is missing"
done

# 5. Main documents carry a status line.
for f in README.md docs/scope.md docs/uncertainties.md research/state-of-the-art.md; do
  [ -e "$f" ] || continue
  grep -qE '^-? ?Status' "$f" || fail "$f: no status line"
done

if [ "$status" -eq 0 ]; then echo "Documentation checks passed."; fi
exit "$status"
