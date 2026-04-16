"""
Task Routes — 任務相關路由（Controller）

定義所有任務相關的 URL 路由與處理邏輯。
使用 Flask Blueprint 組織路由，與應用初始化分離。
"""

from flask import Blueprint

# 建立 Blueprint，所有任務路由的前綴為空（直接掛在根路徑）
task_bp = Blueprint('tasks', __name__)


@task_bp.route('/', methods=['GET'])
def index():
    """
    任務列表頁（首頁）

    功能：F-06 任務列表與篩選、F-07 到期提醒標示
    輸入：Query Parameter - filter（可選，值為 all / active / completed）
    處理：呼叫 task.get_all(db_path, status_filter) 取得任務清單
    輸出：渲染 index.html，傳入 tasks 與 current_filter
    """
    # TODO: 實作任務列表邏輯
    pass


@task_bp.route('/tasks/new', methods=['GET'])
def create_form():
    """
    新增任務頁面

    功能：F-01 新增任務
    輸入：無
    處理：無資料庫操作
    輸出：渲染 create.html，顯示空白表單
    """
    # TODO: 實作顯示新增表單
    pass


@task_bp.route('/tasks', methods=['POST'])
def create_task():
    """
    建立任務（處理表單提交）

    功能：F-01 新增任務、F-05 設定截止日期
    輸入：表單欄位 - title（必填）、description（選填）、due_date（選填）
    處理：
        1. 驗證 title 不為空
        2. 呼叫 task.create(db_path, title, description, due_date)
    輸出：
        - 成功：redirect('/') 重導向至首頁
        - 失敗：重新渲染 create.html，傳入錯誤訊息與已輸入的資料
    """
    # TODO: 實作新增任務邏輯
    pass


@task_bp.route('/tasks/<int:task_id>/edit', methods=['GET'])
def edit_form(task_id):
    """
    編輯任務頁面

    功能：F-02 編輯任務
    輸入：URL 參數 - task_id（任務 ID）
    處理：呼叫 task.get_by_id(db_path, task_id) 取得任務資料
    輸出：渲染 edit.html，傳入 task 資料
    錯誤：任務不存在時回傳 404
    """
    # TODO: 實作顯示編輯表單
    pass


@task_bp.route('/tasks/<int:task_id>/update', methods=['POST'])
def update_task(task_id):
    """
    更新任務（處理編輯表單提交）

    功能：F-02 編輯任務、F-05 設定截止日期
    輸入：URL 參數 - task_id；表單欄位 - title（必填）、description（選填）、due_date（選填）
    處理：
        1. 驗證 title 不為空
        2. 呼叫 task.update(db_path, task_id, title, description, due_date)
    輸出：
        - 成功：redirect('/') 重導向至首頁
        - 失敗：重新渲染 edit.html，傳入錯誤訊息與任務資料
    錯誤：任務不存在時回傳 404
    """
    # TODO: 實作更新任務邏輯
    pass


@task_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除任務

    功能：F-03 刪除任務
    輸入：URL 參數 - task_id（任務 ID）
    處理：呼叫 task.delete(db_path, task_id)
    輸出：redirect('/') 重導向至首頁
    備註：刪除確認在前端以 JavaScript confirm() 實作
    """
    # TODO: 實作刪除任務邏輯
    pass


@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務完成狀態

    功能：F-04 標記完成狀態
    輸入：URL 參數 - task_id（任務 ID）
    處理：呼叫 task.toggle_completed(db_path, task_id)
    輸出：redirect('/') 重導向至首頁
    """
    # TODO: 實作切換完成狀態邏輯
    pass
