import streamlit as st
from supabase import create_client, Client

# --------------------
# Supabase 接続
# --------------------
supabase: Client = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.set_page_config(page_title="Gamified Todo", page_icon="🎮")
st.title("🎮 Gamified Todo App")

# --------------------
# Todo 追加
# --------------------
st.subheader("➕ 新しいTodo")

task = st.text_input("Todo内容")
category = st.selectbox("カテゴリ", ["勉強", "課題", "私用", "その他"])
priority = st.selectbox("優先度", ["低", "中", "高"])

priority_point = {"低": 1, "中": 3, "高": 5}

if st.button("追加する"):
    if task:
        supabase.table("todos").insert({
            "task": task,
            "category": category,
            "priority": priority,
            "point": priority_point[priority]
        }).execute()
        st.success("Todo を追加しました！")
    else:
        st.warning("Todoを入力してください")

# --------------------
# Todo 一覧
# --------------------
st.subheader("📋 Todo 一覧")

res = supabase.table("todos").select("*").order("created_at").execute()
todos = res.data

total_point = 0

for todo in todos:
    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        done = st.checkbox(
            f"{todo['task']}（{todo['category']} / {todo['priority']}）",
            value=todo["is_done"],
            key=f"check_{todo['id']}"
        )

    with col2:
        st.write(f"🎯 {todo['point']} pt")

    with col3:
        if st.button("🗑", key=f"del_{todo['id']}"):
            supabase.table("todos").delete().eq("id", todo["id"]).execute()
            st.experimental_rerun()

    if done != todo["is_done"]:
        supabase.table("todos").update({
            "is_done": done
        }).eq("id", todo["id"]).execute()
        st.experimental_rerun()

    if todo["is_done"]:
        total_point += todo["point"]

# --------------------
# スコア表示
# --------------------
st.divider()
st.subheader("🏆 今日のスコア")

st.metric("獲得ポイント", f"{total_point} pt")

if total_point >= 15:
    st.success("🔥 めっちゃ頑張ってる！")
elif total_point >= 5:
    st.info("👍 いいペース")
else:
    st.warning("😴 まだいける！")
