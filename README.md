ｖimport streamlit as st
from supabase import create_client

# =====================
# Supabase 接続設定
# =====================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# =====================
# UI
# =====================
st.title("📝 Supabase Todo 管理アプリ")

# ---------------------
# Todo 追加
# ---------------------
st.subheader("Todo を追加")

new_task = st.text_input("新しい Todo を入力してください")

if st.button("追加"):
    if new_task.strip() != "":
        supabase.table("todos").insert({
            "task": new_task,
            "is_done": False
        }).execute()
        st.success("Todo を追加しました")
        st.rerun()
    else:
        st.warning("Todo を入力してください")

# ---------------------
# Todo 一覧表示
# ---------------------
st.subheader("Todo 一覧")

response = supabase.table("todos").select("*").order("created_at").execute()

if response.data:
    for todo in response.data:
        col1, col2, col3 = st.columns([5, 1, 1])

        # 完了チェック
        checked = col1.checkbox(
            todo["task"],
            value=todo["is_done"],
            key=f"check_{todo['id']}"
        )

        # 状態更新
        if checked != todo["is_done"]:
            supabase.table("todos").update({
                "is_done": checked
            }).eq("id", todo["id"]).execute()
            st.rerun()

        # 削除ボタン
        if col3.button("🗑", key=f"delete_{todo['id']}"):
            supabase.table("todos").delete().eq("id", todo["id"]).execute()
            st.rerun()
else:
    st.write("まだ Todo がありません")
