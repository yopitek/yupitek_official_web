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
#
# 7 欄位: Backlog, Plan, Todos, Doing, QA, Review, Done

set -euo pipefail

# Configuration
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MASTER_BOARD="${PROJECT_ROOT}/../../10_kanban/master-board.md"
TASKS_DIR="${PROJECT_ROOT}/../../10_kanban/tasks"

# WIP limits
WIP_DOING=2
WIP_QA=3

# ─── Helper Functions ───────────────────────────────────────────────

# Count cards in a column section
count_in_column() {
    local column_name="$1"
    local icon marker

    case "$column_name" in
        Backlog)  icon="📥"; marker="- \[" ;;
        Plan)     icon="📋"; marker="- \[" ;;
        Todos)    icon="✅"; marker="- \[" ;;
        Doing)    icon="🔄"; marker="- \[" ;;
        QA)       icon="🧪"; marker="- \[" ;;
        Review)   icon="👀"; marker="- \[" ;;
        Done)     icon="✔️";  marker="- \[x\]" ;;
    esac

    local in_section=0
    local count=0

    while IFS= read -r line; do
        # Check if we hit the section header
        if echo "$line" | grep -q -- "^## ${icon}"; then
            in_section=1
            continue
        fi
        # Check if we hit next section
        if [[ $in_section -eq 1 ]] && echo "$line" | grep -q -- "^## "; then
            break
        fi
        # Count cards in section
        if [[ $in_section -eq 1 ]] && echo "$line" | grep -q -- "$marker"; then
            count=$((count + 1))
        fi
    done < "$MASTER_BOARD"

    echo "$count"
}

# Move a card from one column to another
move_card() {
    local task_id="$1"
    local from_column="$2"
    local to_column="$3"

    echo "Moving [[${task_id}]] from ${from_column} to ${to_column}"

    # Check WIP limits for target column
    case "$to_column" in
        Doing)
            local count
            count=$(count_in_column "Doing")
            if (( count >= WIP_DOING )); then
                echo "  ⚠️  WIP limit: ${count}/${WIP_DOING} (Doing)"
            else
                echo "  ✅ WIP ok: ${count}/${WIP_DOING} (Doing)"
            fi
            ;;
        QA)
            local count
            count=$(count_in_column "QA")
            if (( count >= WIP_QA )); then
                echo "  ⚠️  WIP limit: ${count}/${WIP_QA} (QA)"
            else
                echo "  ✅ WIP ok: ${count}/${WIP_QA} (QA)"
            fi
            ;;
    esac
}

# Show status of a specific task
show_task_status() {
    local task_id="$1"
    local task_file="${TASKS_DIR}/${task_id}.md"

    echo "=== Status: ${task_id} ==="

    if [[ ! -f "$task_file" ]]; then
        echo "Task file not found: ${task_file}"
        return 1
    fi

    # Extract frontmatter
    echo "Status: $(grep '^status:' "$task_file" | head -1 | sed 's/status: *//')"

    echo "Ratings:"
    grep -E '^\s+(slice_size|test_quality|domain_alignment|rework_count|blocked_minutes):' "$task_file" | sed 's/^/  /'
}

# List all cards
list_cards() {
    local filter="${1:-}"

    echo "=== 7-Column Kanban Board ==="
    echo ""
    echo "Columns: Backlog → Plan → Todos → Doing → QA → Review → Done"
    echo "WIP: Doing=${WIP_DOING}, QA=${WIP_QA}"
    echo ""

    local columns=("Backlog" "Plan" "Todos" "Doing" "QA" "Review" "Done")
    local icons=("📥" "📋" "✅" "🔄" "🧪" "👀" "✔️")

    for i in "${!columns[@]}"; do
        local col="${columns[$i]}"
        local icon="${icons[$i]}"

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

        printf "  %s %-10s %d%s\n" "$icon" "$col:" "$count" "$wip_str"
    done
}

# Update task ratings in frontmatter
score_task() {
    local task_id="$1"
    local slice_size="${2:-4}"
    local test_quality="${3:-4}"
    local domain_alignment="${4:-4}"
    local rework_count="${5:-0}"
    local blocked_minutes="${6:-0}"

    local task_file="${TASKS_DIR}/${task_id}.md"

    if [[ ! -f "$task_file" ]]; then
        echo "Task file not found: ${task_file}"
        return 1
    fi

    echo "Scoring ${task_id}:"
    echo "  slice_size: ${slice_size}"
    echo "  test_quality: ${test_quality}"
    echo "  domain_alignment: ${domain_alignment}"
    echo "  rework_count: ${rework_count}"
    echo "  blocked_minutes: ${blocked_minutes}"

    # Update the task file frontmatter using sed
    local tmpfile
    tmpfile=$(mktemp)

    awk -v ss="$slice_size" -v tq="$test_quality" -v da="$domain_alignment" -v rc="$rework_count" -v bm="$blocked_minutes" '
        /^---$/ && !header_done { header_done=1; in_fm=1; next }
        in_fm && /^---$/ { print; in_fm=0; print; next }
        in_fm && /slice_size:/ { print "  slice_size: " ss; next }
        in_fm && /test_quality:/ { print "  test_quality: " tq; next }
        in_fm && /domain_alignment:/ { print "  domain_alignment: " da; next }
        in_fm && /rework_count:/ { print "  rework_count: " rc; next }
        in_fm && /blocked_minutes:/ { print "  blocked_minutes: " bm; next }
        { print }
    ' "$task_file" > "$tmpfile"

    mv "$tmpfile" "$task_file"
}

# Check WIP limits across all columns
wip_check() {
    echo "=== WIP Limits Check ==="
    echo ""

    local doing_count qa_count
    doing_count=$(count_in_column "Doing")
    qa_count=$(count_in_column "QA")

    echo "Doing: ${doing_count}/${WIP_DOING} $(( doing_count > WIP_DOING ? 1 : 0 ))"
    echo "QA: ${qa_count}/${WIP_QA} $(( qa_count > WIP_QA ? 1 : 0 ))"
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
    help|*)
        echo "7-Column Kanban Workflow Script"
        echo ""
        echo "Usage:"
        echo "  $0 move <task-id> <from> <to>       Move a card between columns"
        echo "  $0 status <task-id>                  Show task status & ratings"
        echo "  $0 list [--column <column>]           List all cards"
        echo "  $0 score <task-id> <ss> <tq> <da> <rc> <bm>  Update ratings"
        echo "  $0 wip-check                          Check WIP limits"
        echo ""
        echo "7 Columns:"
        echo "  📥 Backlog → 📋 Plan → ✅ Todos → 🔄 Doing → 🧪 QA → 👀 Review → ✔️ Done"
        echo ""
        echo "WIP Limits: Doing=${WIP_DOING}, QA=${WIP_QA}"
        ;;
esac
