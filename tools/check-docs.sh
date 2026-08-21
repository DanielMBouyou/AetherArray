#!/usr/bin/env bash
# Vérifications légères sur la documentation du dépôt.
# Volontairement minimal : ces contrôles doivent rester rapides et sans dépendance.
set -u
status=0

fail() { echo "ECHEC: $*"; status=1; }

# 1. Le tiret cadratin est interdit (convention du dépôt, voir CONVENTIONS.md).
if grep -rlP '\x{2014}' --include='*.md' . 2>/dev/null | grep -q .; then
  echo "Fichiers contenant un tiret cadratin :"
  grep -rlP '\x{2014}' --include='*.md' . 2>/dev/null
  fail "tiret cadratin présent"
fi

# 2. Chaque fiche de décision doit contenir les sections obligatoires.
for f in decisions/[0-9][0-9][0-9][0-9]-*.md; do
  [ -e "$f" ] || continue
  case "$f" in *0000-template.md) continue;; esac
  for section in "## Question posée" "## Options étudiées" "## Preuves utilisées" "## Décision" "## Limites connues" "## Conditions de réexamen"; do
    grep -qF "$section" "$f" || fail "$f : section manquante ($section)"
  done
done

# 3. Les documents structurants doivent exister.
for f in README.md CONVENTIONS.md ROADMAP.md docs/cadrage.md docs/incertitudes.md \
         research/etat-de-l-art.md benchmarks/methodologie.md experiments/plan.md; do
  [ -e "$f" ] || fail "$f : fichier attendu absent"
done

# 4. Les documents principaux portent un bloc de statut.
for f in README.md docs/cadrage.md docs/incertitudes.md research/etat-de-l-art.md; do
  [ -e "$f" ] || continue
  grep -qE '^-? ?Statut' "$f" || fail "$f : bloc de statut absent"
done

if [ "$status" -eq 0 ]; then echo "Documentation : contrôles passés."; fi
exit "$status"
