import streamlit as st
from supabase import create_client

# ========================
# Supabase 接続
# ========================
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_ANON_KEY = st.secrets["SUPABASE_ANON_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# ========================
# UI
# ========================
st.title("📝 Todoリスト管理アプリ（Supabase）")

# ------------------------
# Todo 追加
# ------------------------
st.subheader("Todoを追加")

new_task = st.text_input("新しいTodoを入力")

if st.button("追加"):
    if new_task.strip() != "":
        supabase.table("todo").insert({
            "task": new_task,
            "is_done": False
        }).execute()
        st.success("Todoを追加しました")
        st.rerun()
    else:
        st.warning("Todoを入力してください")

# ------------------------
# Todo 一覧
# ------------------------
st.subheader("Todo一覧")

response = supabase.table("todo").select("*").order("id").execute()

if response.data:
    for todo in response.data:
        col1, col2, col3 = st.columns([4, 1, 1])

        # 完了チェック
        checked = col1.checkbox(
            todo["task"],
            value=todo["is_done"],
            key=f"check_{todo['id']}"
        )

        # 更新
        if checked != todo["is_done"]:
            supabase.table("todo").update({
                "is_done": checked
            }).eq("id", todo["id"]).execute()
            st.rerun()

        # 削除
        if col3.button("🗑", key=f"del_{todo['id']}"):
            supabase.table("todo").delete().eq("id", todo["id"]).execute()
            st.rerun()
else:
    st.write("まだTodoがありません")
