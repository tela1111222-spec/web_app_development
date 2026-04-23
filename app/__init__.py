# app/__init__.py
# Flask 應用程式套件

import os
from flask import Flask
from app.models import task


def create_app():
    """
    App 工廠函式：建立並設定 Flask 應用程式實例。

    - 設定 SECRET_KEY（用於 flash message）
    - 設定資料庫路徑（instance/database.db）
    - 註冊 Blueprint
    - 初始化資料庫
    """
    app = Flask(__name__,
                instance_relative_config=True)

    # 設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')

    # 確保 instance 資料夾存在
    os.makedirs(app.instance_path, exist_ok=True)

    # 初始化資料庫（建立資料表）
    task.init_db(app.config['DATABASE'])

    # 註冊 Blueprint
    from app.routes.task_routes import task_bp
    app.register_blueprint(task_bp)

    return app
