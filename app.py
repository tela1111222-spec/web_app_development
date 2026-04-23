"""
app.py — 應用程式入口點

啟動 Flask 開發伺服器。
使用 App 工廠模式建立 Flask 實例。
"""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
