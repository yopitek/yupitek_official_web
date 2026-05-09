#!/usr/bin/env bash
# kanban-workflow.sh — 7 欄位 Kanban 工作流程腳本
# 對應 mattpocock skills 的 7 階段狀態機
#
# 用法:
#   ./scripts/kanban-workflow.sh move <task-id> <from-column> <to-column>
#   ./scripts/kanban-workflow.sh status <task-id>
#   ./scripts/kanban-workflow.sh list [--column <column>]
#   ./scripts/kanban-workflow.sh score <task-id> <slice_size> <test_quality> <domain_alignment> <rework_count> <blocked_minutes>
#   ./scripts/kanban-workflow.sh wip-check
#   ./scripts/kanban-workflow.sh daily-init [YYYY-MM-DD]
#   ./scripts/kanban-workflow.sh daily-eod [YYYY-MM-DD]
#
# 7 欄位: Backlog, Plan, Todos, Doing, QA, Review, Done

set -euo pipefail

# ─── ANSI Colors ────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

err() { echo -e "${RED}❌ $*${NC}" >&2; }
ok()  { echo -e "${GREEN}✅ $*${NC}"; }
warn() { echo -e "${YELLOW}⚠️  $*${NC}"; }

# ─── Configuration ──────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
MASTER_BOARD="${PROJECT_ROOT}/../../10_kanban/master-board.md"
TASKS_DIR="${PROJECT_ROOT}/../../10_kanban/tasks"
DAILY_DIR="${PROJECT_ROOT}/../../10_kanban/daily"
ARCHIVE_DIR="${PROJECT_ROOT}/../../10_kanban/archive"

# WIP limits
WIP_DOING=2
WIP_QA=3

# ─── Helper Functions ───────────────────────────────────────────────

# Count cards in a column section (Bug fix #1: awk-based, no emoji dependency)
count_in_column() {
    local column_name="$1"
    awk -v col="$column_name" '
        /^## / { in_section = ($0 ~ col) ? 1 : 0; next }
        in_section && /^- \[/ { count++ }
        END { print count+0 }
    ' "$MASTER_BOARD"
}

# Check WIP limits for target column (returns 0 if OK, 1 if over)
check_wip_before_move() {
    local to_column="$1"
    local count

    case "$to_column" in
        Doing)
            count=$(count_in_column "Doing")
            if (( count >= WIP_DOING )); then
                warn "WIP limit: ${count}/${WIP_DOING} (Doing)"
                return 1
            fi
            ;;
        QA)
            count=$(count_in_column "QA")
            if (( count >= WIP_QA )); then
                warn "WIP limit: ${count}/${WIP_QA} (QA)"
                return 1
            fi
            ;;
    esac
    return 0
}

# Move a card from one column to another (Bug fix #2: actually modifies master-board.md)
move_card() {
    local task_id="$1"
    local from_column="$2"
    local to_column="$3"

    # Validate input
    if [[ -z "$task_id" || -z "$from_column" || -z "$to_column" ]]; then
        err "Usage: move <task-id> <from-column> <to-column>"
        return 1
    fi

    # WIP check for target column
    if ! check_wip_before_move "$to_column"; then
        return 1
    fi

    # Find the card line
    local card_line
    card_line=$(grep -E "\[.\].*${task_id}|${task_id}" "$MASTER_BOARD" | head -1)

    if [[ -z "$card_line" ]]; then
        err "Card not found: ${task_id}"
        return 1
    fi

    # Create temp file and rebuild
    local tmpfile
    tmpfile=$(mktemp)

    # Remove the card from source column
    grep -v -E "\[.\].*${task_id}|${task_id}" "$MASTER_BOARD" > "$tmpfile"

    # Insert card at end of target column
    awk -v col="$to_column" -v card="$card_line" '
        /^## / { in_section = ($0 ~ col) ? 1 : 0 }
        /^## / && in_section == 0 && prev_in { print card; prev_in=0 }
        { print; prev_in = in_section }
        END { if (in_section) print card }
    ' "$tmpfile" > "$MASTER_BOARD"

    rm -f "$tmpfile"
    ok "Moved [[${task_id}]]: ${from_column} -> ${to_column}"
}

# Show status of a specific task
show_task_status() {
    local task_id="$1"
    local task_file="${TASKS_DIR}/${task_id}.md"

    echo "=== Status: ${task_id} ==="

    if [[ ! -f "$task_file" ]]; then
        err "Task file not found: ${task_file}"
        return 1
    fi

    echo "Status: $(grep '^status:' "$task_file" | head -1 | sed 's/status: *//')"
    echo ""
    echo "Ratings:"
    grep -E '^\s+(slice_size|test_quality|domain_alignment|rework_count|blocked_minutes):' "$task_file" | sed 's/^/  /'
}

# List all cards
list_cards() {
    local filter="${1:-}"

    echo "=== 7-Column Kanban Board ==="
    echo ""
    echo "Columns: Backlog -> Plan -> Todos -> Doing -> QA -> Review -> Done"
    echo "WIP: Doing=${WIP_DOING}, QA=${WIP_QA}"
    echo ""

    local columns=("Backlog" "Plan" "Todos" "Doing" "QA" "Review" "Done")

    for col in "${columns[@]}"; do
        if [[ -n "$filter" && "$filter" != "$col" ]]; then
            continue
        fi

        local count
        count=$(count_in_column "$col")

        local wip_str=""
        if [[ "$col" == "Doing" ]]; then
            wip_str=" (WIP:${WIP_DOING})"
        elif [[ "$col" == "QA" ]]; then
            wip_str=" (WIP:${WIP_QA})"
        fi

        printf "  %-10s %d%s\n" "$col:" "$count" "$wip_str"
    done
}

# Update task ratings in frontmatter (Bug fix #4: fixed awk double-print bug)
score_task() {
    local task_id="$1"
    local slice_size="${2:-4}"
    local test_quality="${3:-4}"
    local domain_alignment="${4:-4}"
    local rework_count="${5:-0}"
    local blocked_minutes="${6:-0}"

    local task_file="${TASKS_DIR}/${task_id}.md"

    if [[ ! -f "$task_file" ]]; then
        err "Task file not found: ${task_file}"
        return 1
    fi

    ok "Scoring ${task_id}:"
    echo "  slice_size: ${slice_size}"
    echo "  test_quality: ${test_quality}"
    echo "  domain_alignment: ${domain_alignment}"
    echo "  rework_count: ${rework_count}"
    echo "  blocked_minutes: ${blocked_minutes}"

    local tmpfile
    tmpfile=$(mktemp)

    awk -v ss="$slice_size" -v tq="$test_quality" -v da="$domain_alignment" \
        -v rc="$rework_count" -v bm="$blocked_minutes" '
        BEGIN { in_fm=0; header_done=0 }
        /^---$/ && !header_done { header_done=1; in_fm=1; print; next }
        in_fm && /^---$/ { in_fm=0; print; next }
        in_fm && /^\s*slice_size:/      { print "  slice_size: " ss; next }
        in_fm && /^\s*test_quality:/    { print "  test_quality: " tq; next }
        in_fm && /^\s*domain_alignment:/ { print "  domain_alignment: " da; next }
        in_fm && /^\s*rework_count:/    { print "  rework_count: " rc; next }
        in_fm && /^\s*blocked_minutes:/ { print "  blocked_minutes: " bm; next }
        { print }
    ' "$task_file" > "$tmpfile"

    mv "$tmpfile" "$task_file"
}

# Check WIP limits across all columns (Bug fix #5: friendly output format)
wip_check() {
    echo "=== WIP Limits Check ==="

    local doing_count qa_count
    doing_count=$(count_in_column "Doing")
    qa_count=$(count_in_column "QA")

    local doing_status="OK"
    local qa_status="OK"
    (( doing_count > WIP_DOING )) && doing_status="OVER LIMIT"
    (( qa_count > WIP_QA ))     && qa_status="OVER LIMIT"

    printf "  Doing : %d/%d  %s\n" "$doing_count" "$WIP_DOING" "$doing_status"
    printf "  QA    : %d/%d  %s\n" "$qa_count" "$WIP_QA" "$qa_status"
}

# ─── Daily Board Functions ─────────────────────────────────────────

# (Bug fix #3: daily board init function)
daily_init() {
    local today="${1:-$(date +%Y-%m-%d)}"
    local yesterday="${2:-$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)}"

    local daily_board="${DAILY_DIR}/${today}.md"

    mkdir -p "$DAILY_DIR"

    if [[ -f "$daily_board" ]]; then
        echo "Daily board already exists: ${daily_board}"
        return 0
    fi

    # Build sections from yesterday or use defaults
    local sections=""

    if [[ -f "${DAILY_DIR}/${yesterday}.md" ]]; then
        for col in "Backlog" "Plan" "Todos" "Doing" "QA" "Review"; do
            local cards
            cards=$(awk -v col="$col" '
                /^## / { in_section = ($0 ~ col) ? 1 : 0; next }
                in_section && /^- \[ \]/ { print }
            ' "${DAILY_DIR}/${yesterday}.md")

            if [[ -n "$cards" ]]; then
                sections+="## ${col}

${cards}

"
            else
                sections+="## ${col}


"
            fi
        done
    else
        for col in "Backlog" "Plan" "Todos" "Doing" "QA" "Review"; do
            sections+="## ${col}


"
        done
    fi

    cat > "$daily_board" << BOARD_EOF
---
kanban-plugin: board
date: ${today}
inherited_from: ${yesterday}
wip-limits:
  Doing: 2
  QA: 3
---

${sections}## Done


%% kanban:settings
\`\`\`
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false,false,false],"date-display-format":"YYYY-MM-DD","show-checkboxes":true}
\`\`\`
%%
BOARD_EOF

    ok "Daily board created: ${daily_board}"
    echo "Inherited from: ${yesterday}.md"
}

# End-of-day: archive + statistics
daily_eod() {
    local today="${1:-$(date +%Y-%m-%d)}"
    local month=$(date +%Y-%m)

    local daily_board="${DAILY_DIR}/${today}.md"
    local archive_dir="${ARCHIVE_DIR}/${month}"

    mkdir -p "$archive_dir"

    if [[ ! -f "$daily_board" ]]; then
        err "Daily board not found: ${daily_board}"
        return 1
    fi

    # Count stats
    local done_count todo_remaining
    done_count=$(grep -c "^- \[x\]" "$daily_board" 2>/dev/null || echo 0)
    todo_remaining=$(grep -c "^- \[ \]" "$daily_board" 2>/dev/null || echo 0)

    echo "=== End-of-Day Report ${today} ==="
    echo "  Completed: ${done_count}"
    echo "  Remaining: ${todo_remaining} (will be inherited tomorrow)"

    cp "$daily_board" "${archive_dir}/${today}.md"
    ok "Archived: ${archive_dir}/${today}.md"
}

# ─── Main ───────────────────────────────────────────────────────────

case "${1:-help}" in
    move)
        move_card "${2:-}" "${3:-}" "${4:-}"
        ;;
    status)
        show_task_status "${2:-}"
        ;;
    list)
        filter=""
        if [[ "${2:-}" == "--column" ]]; then
            filter="${3:-}"
        fi
        list_cards "$filter"
        ;;
    score)
        score_task "${2:-}" "${3:-4}" "${4:-4}" "${5:-4}" "${6:-0}" "${7:-0}"
        ;;
    wip-check)
        wip_check
        ;;
    daily-init)
        daily_init "${2:-}"
        ;;
    daily-eod)
        daily_eod "${2:-}"
        ;;
    help|*)
        echo "7-Column Kanban Workflow Script"
        echo ""
        echo "Usage:"
        echo "  $0 move <task-id> <from> <to>       Move a card between columns"
        echo "  $0 status <task-id>                  Show task status & ratings"
        echo "  $0 list [--column <column>]           List all cards"
        echo "  $0 score <task-id> <ss> <tq> <da> <rc> <bm>  Update ratings"
        echo "  $0 wip-check                          Check WIP limits"
        echo "  $0 daily-init [date]                  Create daily board"
        echo "  $0 daily-eod [date]                   End-of-day archive"
        echo ""
        echo "7 Columns:"
        echo "  Backlog -> Plan -> Todos -> Doing -> QA -> Review -> Done"
        echo ""
        echo "WIP Limits: Doing=${WIP_DOING}, QA=${WIP_QA}"
        ;;
esac
