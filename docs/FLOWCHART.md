# 任務管理系統 — 流程圖文件

> **文件版本：** v1.0
> **建立日期：** 2026-04-09
> **對應文件：** [docs/PRD.md](./PRD.md) ｜ [docs/ARCHITECTURE.md](./ARCHITECTURE.md)

---

## 1. 使用者流程圖（User Flow）

以下流程圖描述使用者從進入網站到完成各項操作的完整路徑：

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁 - 任務列表]

    B --> C{要執行什麼操作？}

    %% 新增任務
    C -->|新增任務| D[點擊「新增任務」按鈕]
    D --> E[填寫任務表單\n名稱 / 描述 / 截止日期]
    E --> F{表單驗證}
    F -->|驗證失敗\n名稱為空| E
    F -->|驗證通過| G[儲存任務到資料庫]
    G --> B

    %% 編輯任務
    C -->|編輯任務| H[點擊任務的「編輯」按鈕]
    H --> I[載入編輯表單\n顯示現有資料]
    I --> J[修改任務資訊]
    J --> K{表單驗證}
    K -->|驗證失敗| J
    K -->|驗證通過| L[更新任務到資料庫]
    L --> B

    %% 刪除任務
    C -->|刪除任務| M[點擊任務的「刪除」按鈕]
    M --> N{確認刪除？}
    N -->|取消| B
    N -->|確認| O[從資料庫刪除任務]
    O --> B

    %% 標記完成
    C -->|標記完成/未完成| P[點擊任務的核取方塊]
    P --> Q[切換完成狀態]
    Q --> B

    %% 篩選任務
    C -->|篩選任務| R[選擇篩選條件\n全部 / 未完成 / 已完成]
    R --> B
```

### 流程說明

| 步驟 | 說明 |
|------|------|
| **進入首頁** | 使用者開啟網頁後，自動顯示所有任務列表 |
| **新增任務** | 點擊新增 → 填寫表單 → 驗證 → 儲存 → 回到列表 |
| **編輯任務** | 點擊編輯 → 載入現有資料 → 修改 → 驗證 → 更新 → 回到列表 |
| **刪除任務** | 點擊刪除 → 確認提示 → 確認後刪除 → 回到列表 |
| **標記完成** | 點擊核取方塊 → 即時切換狀態 → 列表更新 |
| **篩選任務** | 選擇篩選條件 → 列表重新載入對應任務 |

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊「新增任務」
    Browser->>Flask: GET /tasks/new
    Flask-->>Browser: 回傳新增表單頁面

    User->>Browser: 填寫名稱、描述、截止日期並送出
    Browser->>Flask: POST /tasks
    Flask->>Flask: 驗證表單資料

    alt 驗證失敗
        Flask-->>Browser: 回傳表單頁面（含錯誤訊息）
    else 驗證通過
        Flask->>Model: create_task(name, description, due_date)
        Model->>DB: INSERT INTO tasks VALUES(...)
        DB-->>Model: 成功
        Model-->>Flask: 回傳新任務
        Flask-->>Browser: 302 重導向到 /
        Browser->>Flask: GET /
        Flask->>Model: get_all_tasks()
        Model->>DB: SELECT * FROM tasks
        DB-->>Model: 回傳任務清單
        Model-->>Flask: 任務清單
        Flask-->>Browser: 渲染任務列表頁
    end
```

### 2.2 編輯任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「編輯」按鈕
    Browser->>Flask: GET /tasks/{id}/edit
    Flask->>Model: get_task_by_id(id)
    Model->>DB: SELECT * FROM tasks WHERE id = ?
    DB-->>Model: 回傳任務資料
    Model-->>Flask: 任務資料
    Flask-->>Browser: 回傳編輯表單（帶入現有資料）

    User->>Browser: 修改資料並送出
    Browser->>Flask: POST /tasks/{id}/update
    Flask->>Flask: 驗證表單資料

    alt 驗證失敗
        Flask-->>Browser: 回傳表單頁面（含錯誤訊息）
    else 驗證通過
        Flask->>Model: update_task(id, name, description, due_date)
        Model->>DB: UPDATE tasks SET ... WHERE id = ?
        DB-->>Model: 成功
        Model-->>Flask: 更新完成
        Flask-->>Browser: 302 重導向到 /
    end
```

### 2.3 刪除任務流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的「刪除」按鈕
    Browser->>Browser: 彈出確認對話框

    alt 使用者取消
        Browser-->>User: 關閉對話框，無操作
    else 使用者確認
        Browser->>Flask: POST /tasks/{id}/delete
        Flask->>Model: delete_task(id)
        Model->>DB: DELETE FROM tasks WHERE id = ?
        DB-->>Model: 成功
        Model-->>Flask: 刪除完成
        Flask-->>Browser: 302 重導向到 /
    end
```

### 2.4 切換完成狀態流程

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Task Model
    participant DB as SQLite

    User->>Browser: 點擊任務的核取方塊
    Browser->>Flask: POST /tasks/{id}/toggle
    Flask->>Model: toggle_task(id)
    Model->>DB: UPDATE tasks SET completed = NOT completed WHERE id = ?
    DB-->>Model: 成功
    Model-->>Flask: 切換完成
    Flask-->>Browser: 302 重導向到 /
    Browser-->>User: 任務狀態已更新
```

---

## 3. 功能清單對照表

| 功能 | URL 路徑 | HTTP 方法 | 說明 |
|------|---------|-----------|------|
| 瀏覽任務列表 | `/` | `GET` | 首頁，顯示所有任務，支援篩選 |
| 新增任務頁面 | `/tasks/new` | `GET` | 顯示新增任務的表單 |
| 提交新任務 | `/tasks` | `POST` | 接收表單資料，建立新任務 |
| 編輯任務頁面 | `/tasks/<id>/edit` | `GET` | 顯示編輯表單，帶入現有資料 |
| 更新任務 | `/tasks/<id>/update` | `POST` | 接收表單資料，更新任務 |
| 刪除任務 | `/tasks/<id>/delete` | `POST` | 刪除指定任務 |
| 切換完成狀態 | `/tasks/<id>/toggle` | `POST` | 切換任務的完成 / 未完成狀態 |

---

> **下一步：** 流程圖確認後，可進入資料庫設計（`/db-design`）階段，定義 SQLite 資料表結構。
