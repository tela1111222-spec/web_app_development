"""
Task Routes — 任務相關路由（Controller）

定義所有任務相關的 URL 路由與處理邏輯。
使用 Flask Blueprint 組織路由，與應用初始化分離。
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from app.models import task

# 建立 Blueprint，所有任務路由的前綴為空（直接掛在根路徑）
task_bp = Blueprint('tasks', __name__)


def _get_db_path():
    """取得資料庫路徑（從 Flask app config 取得）。"""
    return current_app.config['DATABASE']


@task_bp.route('/', methods=['GET'])
def index():
    """
    任務列表頁（首頁）

    功能：F-06 任務列表與篩選、F-07 到期提醒標示
    輸入：Query Parameter - filter（可選，值為 all / active / completed）
    處理：呼叫 task.get_all(db_path, status_filter) 取得任務清單
    輸出：渲染 index.html，傳入 tasks 與 current_filter
    """
    db_path = _get_db_path()
    status_filter = request.args.get('filter', 'all')

    # 取得任務清單（依篩選條件）
    tasks = task.get_all(db_path, status_filter)

    return render_template('index.html', tasks=tasks, current_filter=status_filter)


@task_bp.route('/tasks/new', methods=['GET'])
def create_form():
    """
    新增任務頁面

    功能：F-01 新增任務
    輸入：無
    處理：無資料庫操作
    輸出：渲染 create.html，顯示空白表單
    """
    return render_template('create.html')


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
    db_path = _get_db_path()

    # 從表單取得輸入資料
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip() or None

    # 驗證必填欄位
    if not title:
        flash('任務名稱為必填欄位', 'error')
        return render_template('create.html', error='任務名稱為必填欄位', form_data={
            'title': title,
            'description': description,
            'due_date': due_date or ''
        })

    # 呼叫 Model 建立任務
    try:
        task.create(db_path, title, description, due_date)
        flash('任務建立成功！', 'success')
    except Exception as e:
        flash(f'建立任務時發生錯誤：{e}', 'error')
        return render_template('create.html', error=str(e), form_data={
            'title': title,
            'description': description,
            'due_date': due_date or ''
        })

    return redirect(url_for('tasks.index'))


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
    db_path = _get_db_path()

    # 取得任務資料
    task_data = task.get_by_id(db_path, task_id)

    if task_data is None:
        abort(404)

    return render_template('edit.html', task=task_data)


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
    db_path = _get_db_path()

    # 先確認任務存在
    task_data = task.get_by_id(db_path, task_id)
    if task_data is None:
        abort(404)

    # 從表單取得輸入資料
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    due_date = request.form.get('due_date', '').strip() or None

    # 驗證必填欄位
    if not title:
        flash('任務名稱為必填欄位', 'error')
        # 保留使用者輸入的資料，重新渲染編輯頁面
        task_data['title'] = title
        task_data['description'] = description
        task_data['due_date'] = due_date or ''
        return render_template('edit.html', task=task_data, error='任務名稱為必填欄位')

    # 呼叫 Model 更新任務
    try:
        result = task.update(db_path, task_id, title, description, due_date)
        if result is None:
            abort(404)
        flash('任務更新成功！', 'success')
    except Exception as e:
        flash(f'更新任務時發生錯誤：{e}', 'error')
        task_data['title'] = title
        task_data['description'] = description
        task_data['due_date'] = due_date or ''
        return render_template('edit.html', task=task_data, error=str(e))

    return redirect(url_for('tasks.index'))


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
    db_path = _get_db_path()

    try:
        deleted = task.delete(db_path, task_id)
        if deleted:
            flash('任務已刪除', 'success')
        else:
            flash('找不到指定的任務', 'error')
    except Exception as e:
        flash(f'刪除任務時發生錯誤：{e}', 'error')

    return redirect(url_for('tasks.index'))


@task_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務完成狀態

    功能：F-04 標記完成狀態
    輸入：URL 參數 - task_id（任務 ID）
    處理：呼叫 task.toggle_completed(db_path, task_id)
    輸出：redirect('/') 重導向至首頁
    """
    db_path = _get_db_path()

    try:
        task.toggle_completed(db_path, task_id)
    except Exception as e:
        flash(f'切換任務狀態時發生錯誤：{e}', 'error')

    return redirect(url_for('tasks.index'))
