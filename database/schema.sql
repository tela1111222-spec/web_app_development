-- =============================================
-- 任務管理系統 — 資料庫 Schema
-- 資料庫引擎：SQLite
-- 建立日期：2026-04-16
-- =============================================

-- 任務資料表
-- 儲存所有使用者建立的任務
CREATE TABLE IF NOT EXISTS tasks (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,  -- 主鍵，自動遞增
    title        TEXT    NOT NULL,                    -- 任務名稱（必填）
    description  TEXT    DEFAULT '',                  -- 任務描述（選填）
    due_date     TEXT    DEFAULT NULL,                -- 截止日期（YYYY-MM-DD，選填）
    is_completed INTEGER DEFAULT 0,                  -- 完成狀態（0=未完成, 1=已完成）
    created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),  -- 建立時間
    updated_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))   -- 更新時間
);
