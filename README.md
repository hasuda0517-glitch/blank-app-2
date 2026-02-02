
# 📝 Supabase Todo 管理アプリ

Streamlit と **Supabase（PostgreSQL）** を利用した、シンプルで永続化可能な Todo 管理 Web アプリケーションです。  
Todo の追加・完了・削除ができ、アプリがスリープ状態になってもデータはクラウド上に保存され続けます。

---

## URL

この URL で試すことができます（スリープ状態のときは青色の起動ボタンを押してください）：  
https://blank-app-bng6bjgiop.streamlit.app/

---

## 🌟 主な機能

- **Todo 追加**：新しい Todo を入力してデータベースに保存  
- **完了チェック**：チェックボックスで完了／未完了を切り替え  
- **削除機能**：不要になった Todo を削除  
- **自動 DB 連携**：Streamlit から Supabase に直接書き込み  
- **データ永続化**：アプリ停止・再起動後もデータ保持  

---

## 🛠 セットアップ方法

### 1. Supabase プロジェクトの作成（Free プラン）

1. https://supabase.com にアクセス  
2. Free プランで新規プロジェクトを作成  
3. 以下を控えておく  
   - Project URL  
   - anon public key  

---

### 2. データベーステーブルの作成

**todos テーブル**

| column | type |
|------|------|
| id | int8 (PK, identity) |
| task | text |
| is_done | bool (default: false) |
| created_at | timestamptz (default: now()) |

---

### 3. Row Level Security（RLS）

```sql
ALTER TABLE todos ENABLE ROW LEVEL SECURITY;

CREATE POLICY "allow all todos"
ON todos
FOR ALL
USING (true)
WITH CHECK (true);

