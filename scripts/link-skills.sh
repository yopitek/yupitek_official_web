#!/usr/bin/env bash
# link-skills.sh — 安裝 mattpocock/skills 到 Claude Code
# 執行一次即可，之後所有 subagent 共用同一個 skill pool
#
# 用法:
#   ./scripts/link-skills.sh
#   ./scripts/link-skills.sh --force

set -euo pipefail

SKILLS_DIR="$HOME/.claude/skills"
INSTALLED_SKILLS="$SKILLS_DIR/installed_skills.json"
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "=== mattpocock/skills 安裝腳本 ==="
echo ""

# Create skills directory if not exists
mkdir -p "$SKILLS_DIR"

# Check if mattpocock/skills is available
MATTPOCOCK_SKILLS="$HOME/.claude/skills/mattpocock"
if [[ ! -d "$MATTPOCOCK_SKILLS" ]]; then
    echo "Cloning mattpocock/skills..."
    git clone https://github.com/mattpocock/skills.git "$MATTPOCOCK_SKILLS" 2>/dev/null || {
        echo "  ⚠️  Could not clone mattpocock/skills (may already be linked)"
    }
fi

# Detect available skills
declare -a SKILLS=("grill-me" "grill-with-docs" "to-prd" "to-issues" "tdd" "diagnose" "triage")
declare -a SKILL_DESCS=(
    "Grill the AI on requirements"
    "Grill with documentation context"
    "Convert to product requirements"
    "Convert to issues/tasks"
    "Test-driven development (red-green-refactor)"
    "Diagnose and debug issues"
    "Triage incoming items"
)

echo "Detected ${#SKILLS[@]} mattpocock skills:"
for i in "${!SKILLS[@]}"; do
    echo "  ${SKILL_DESCS[$i]} → ${SKILLS[$i]}"
done

# Create or update installed_skills.json
if [[ "${1:-}" == "--force" ]] || [[ ! -f "$INSTALLED_SKILLS" ]]; then
    echo ""
    echo "Creating $INSTALLED_SKILLS..."
    cat > "$INSTALLED_SKILLS" << 'EOF'
{
  "skills": [
    {"name": "grill-me", "file": "~/.claude/skills/mattpocock/grill-me.md", "description": "Grill the AI on requirements"},
    {"name": "grill-with-docs", "file": "~/.claude/skills/mattpocock/grill-with-docs.md", "description": "Grill with documentation context"},
    {"name": "to-prd", "file": "~/.claude/skills/mattpocock/to-prd.md", "description": "Convert to product requirements"},
    {"name": "to-issues", "file": "~/.claude/skills/mattpocock/to-issues.md", "description": "Convert to issues/tasks"},
    {"name": "tdd", "file": "~/.claude/skills/mattpocock/tdd.md", "description": "Test-driven development (red-green-refactor)"},
    {"name": "diagnose", "file": "~/.claude/skills/mattpocock/diagnose.md", "description": "Diagnose and debug issues"},
    {"name": "triage", "file": "~/.claude/skills/mattpocock/triage.md", "description": "Triage incoming items"}
  ],
  "source": "github.com/mattpocock/skills",
  "installed_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
    echo "  ✅ Skills installed to $INSTALLED_SKILLS"
else
    echo "  ✅ Skills already installed at $INSTALLED_SKILLS"
    echo "  Run with --force to reinstall."
fi

echo ""
echo "=== 安裝完成 ==="
echo "Skills 位置: $SKILLS_DIR"
echo "安裝清單: $INSTALLED_SKILLS"
echo ""
echo "Subagent 可以透過 agent_affinity 綁定 skills:"
echo "  - web-optimizer: mattpocock, baoyu-skills"
echo "  - software-engineer: mattpocock, agent-skills"
echo "  - market-researcher: agent-skills, baoyu-skills"
echo "  - data-engineer: agent-skills, mattpocock"
echo "  - content-writer: hyperframes, huasheng_editor, guizang-ppt, baoyu-skills"
echo "  - kanban-sync: (none)"
