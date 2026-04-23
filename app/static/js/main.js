/**
 * main.js — 任務管理系統前端互動邏輯
 *
 * 包含：刪除確認對話框、到期提醒顏色標示
 */

document.addEventListener('DOMContentLoaded', function () {

    // ===== 1. 刪除確認對話框 =====
    const deleteForms = document.querySelectorAll('.delete-form');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const confirmed = confirm('確定要刪除這個任務嗎？此操作無法復原。');
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    // ===== 2. 到期提醒顏色標示（動態判斷） =====
    applyDueDateStyles();

});


/**
 * 根據任務的截止日期，動態加上 CSS class：
 * - task-overdue：已過期（紅色）
 * - task-due-soon：3 天內到期（橘色）
 */
function applyDueDateStyles() {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const soonDate = new Date(today);
    soonDate.setDate(soonDate.getDate() + 3);

    const taskItems = document.querySelectorAll('.list-group-item[id^="task-"]');

    taskItems.forEach(function (item) {
        // 如果已完成，不加到期樣式
        if (item.classList.contains('task-completed')) {
            return;
        }

        // 找到截止日期的文字
        const dueDateLabel = item.querySelector('.due-date-label');
        if (!dueDateLabel) {
            return;
        }

        // 從文字中擷取日期 (格式：截止：YYYY-MM-DD)
        const dateText = dueDateLabel.textContent.trim();
        const match = dateText.match(/(\d{4}-\d{2}-\d{2})/);
        if (!match) {
            return;
        }

        const dueDate = new Date(match[1] + 'T00:00:00');

        if (dueDate < today) {
            // 已過期
            item.classList.add('task-overdue');
        } else if (dueDate <= soonDate) {
            // 3 天內到期
            item.classList.add('task-due-soon');
        }
    });
}
