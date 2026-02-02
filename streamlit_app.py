\import streamlit as st
from supabase import create_client

# ===== Supabase 接続 =====
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_ANON_KEY"]
supabase = create_client(url, key)

st.title("📝 Todoリスト（Supabase）")

# ===== Todo追加 =====
task = st.text_input("新しいTodo")

if st.button("追加"):
    if task:
        supabase.table("todos").insert({
            "task": task,
            "is_done": False
        }).execute()
        st.success("追加しました")
    else:
        st.warning("Todoを入力してください")

# ===== Todo一覧表示 =====
st.subheader("Todo一覧")

todos = supabase.table("todos").select("*").order("id").execute()

if todos.data:
    for todo in todos.data:
        col1, col2 = st.columns([4, 1])
        col1.write(todo["task"])
        col2.write("✅" if todo["is_done"] else "⬜")
else:
    st.write("まだTodoがありません")
