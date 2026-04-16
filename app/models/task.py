"""
Task Model — 任務資料模型

提供任務的 CRUD（建立、讀取、更新、刪除）操作。
使用 Python 內建的 sqlite3 模組直接操作資料庫。
"""

import sqlite3
from datetime import datetime


def get_db_connection(db_path):
    """
    建立資料庫連線。

    Args:
        db_path (str): SQLite 資料庫檔案路徑

    Returns:
        sqlite3.Connection: 資料庫連線物件，查詢結果以 dict 形式回傳
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # 讓查詢結果可以用欄位名稱存取
    return conn


def init_db(db_path):
    """
    初始化資料庫，建立 tasks 資料表（如果不存在）。

    Args:
        db_path (str): SQLite 資料庫檔案路徑
    """
    conn = get_db_connection(db_path)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            title        TEXT    NOT NULL,
            description  TEXT    DEFAULT '',
            due_date     TEXT    DEFAULT NULL,
            is_completed INTEGER DEFAULT 0,
            created_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            updated_at   TEXT    NOT NULL DEFAULT (datetime('now', 'localtime'))
        )
    ''')
    conn.commit()
    conn.close()


def create(db_path, title, description='', due_date=None):
    """
    建立新任務。

    對應功能：F-01 新增任務

    Args:
        db_path (str): 資料庫路徑
        title (str): 任務名稱（必填）
        description (str): 任務描述（選填，預設為空字串）
        due_date (str|None): 截止日期，格式 YYYY-MM-DD（選填）

    Returns:
        dict: 新建立的任務資料
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection(db_path)
    cursor = conn.execute(
        '''
        INSERT INTO tasks (title, description, due_date, is_completed, created_at, updated_at)
        VALUES (?, ?, ?, 0, ?, ?)
        ''',
        (title, description, due_date, now, now)
    )
    task_id = cursor.lastrowid
    conn.commit()

    # 回傳新建立的任務
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()
    return dict(task)


def get_all(db_path, status_filter=None):
    """
    取得所有任務，支援依完成狀態篩選。

    對應功能：F-06 任務列表與篩選

    任務排序規則：
    - 未完成的任務排在前面
    - 依截止日期排序（最近到期的排最前，無截止日期的排最後）

    Args:
        db_path (str): 資料庫路徑
        status_filter (str|None): 篩選條件
            - None 或 'all'：顯示所有任務
            - 'active'：僅顯示未完成的任務
            - 'completed'：僅顯示已完成的任務

    Returns:
        list[dict]: 任務清單
    """
    conn = get_db_connection(db_path)

    if status_filter == 'active':
        tasks = conn.execute(
            '''
            SELECT * FROM tasks
            WHERE is_completed = 0
            ORDER BY
                CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                due_date ASC,
                created_at DESC
            '''
        ).fetchall()
    elif status_filter == 'completed':
        tasks = conn.execute(
            '''
            SELECT * FROM tasks
            WHERE is_completed = 1
            ORDER BY updated_at DESC
            '''
        ).fetchall()
    else:
        tasks = conn.execute(
            '''
            SELECT * FROM tasks
            ORDER BY
                is_completed ASC,
                CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
                due_date ASC,
                created_at DESC
            '''
        ).fetchall()

    conn.close()
    return [dict(task) for task in tasks]


def get_by_id(db_path, task_id):
    """
    依 ID 取得單筆任務。

    Args:
        db_path (str): 資料庫路徑
        task_id (int): 任務 ID

    Returns:
        dict|None: 任務資料，若不存在則回傳 None
    """
    conn = get_db_connection(db_path)
    task = conn.execute(
        'SELECT * FROM tasks WHERE id = ?',
        (task_id,)
    ).fetchone()
    conn.close()

    if task is None:
        return None
    return dict(task)


def update(db_path, task_id, title, description='', due_date=None):
    """
    更新指定任務的資料。

    對應功能：F-02 編輯任務

    Args:
        db_path (str): 資料庫路徑
        task_id (int): 任務 ID
        title (str): 任務名稱（必填）
        description (str): 任務描述（選填）
        due_date (str|None): 截止日期，格式 YYYY-MM-DD（選填）

    Returns:
        dict|None: 更新後的任務資料，若任務不存在則回傳 None
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection(db_path)
    conn.execute(
        '''
        UPDATE tasks
        SET title = ?, description = ?, due_date = ?, updated_at = ?
        WHERE id = ?
        ''',
        (title, description, due_date, now, task_id)
    )
    conn.commit()

    # 回傳更新後的任務
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()

    if task is None:
        return None
    return dict(task)


def delete(db_path, task_id):
    """
    刪除指定任務。

    對應功能：F-03 刪除任務

    Args:
        db_path (str): 資料庫路徑
        task_id (int): 任務 ID

    Returns:
        bool: 是否成功刪除（True 表示有刪除資料，False 表示任務不存在）
    """
    conn = get_db_connection(db_path)
    cursor = conn.execute(
        'DELETE FROM tasks WHERE id = ?',
        (task_id,)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def toggle_completed(db_path, task_id):
    """
    切換任務的完成狀態（已完成 ↔ 未完成）。

    對應功能：F-04 標記完成狀態

    Args:
        db_path (str): 資料庫路徑
        task_id (int): 任務 ID

    Returns:
        dict|None: 更新後的任務資料，若任務不存在則回傳 None
    """
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    conn = get_db_connection(db_path)
    conn.execute(
        '''
        UPDATE tasks
        SET is_completed = CASE WHEN is_completed = 0 THEN 1 ELSE 0 END,
            updated_at = ?
        WHERE id = ?
        ''',
        (now, task_id)
    )
    conn.commit()

    # 回傳更新後的任務
    task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
    conn.close()

    if task is None:
        return None
    return dict(task)
