import streamlit as st
import requests

# FastAPI backend URL
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Todo App", page_icon="✅", layout="centered")
st.title("✅ Todo App")

# Function to fetch all todos
def get_todos():
    try:
        response = requests.get(f"{API_URL}/")
        if response.status_code == 200:
            return response.json()
        return []
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure FastAPI server is running!")
        return []

# Function to create a new todo
def create_todo(title, description):
    try:
        payload = {
            "title": title,
            "description": description,
            "is_completed": False,
            "is_deleted": False
        }
        response = requests.post(f"{API_URL}/", json=payload)
        return response.status_code == 200
    except:
        return False

# Function to update a todo
def update_todo(todo_id, title, description, is_completed):
    try:
        payload = {
            "title": title,
            "description": description,
            "is_completed": is_completed,
            "is_deleted": False
        }
        response = requests.put(f"{API_URL}/{todo_id}", json=payload)
        return response.status_code == 200
    except:
        return False

# Function to delete a todo
def delete_todo(todo_id):
    try:
        response = requests.delete(f"{API_URL}/{todo_id}")
        return response.status_code == 200
    except:
        return False

# Add new todo section
st.subheader("➕ Add New Task")
with st.form("add_todo_form", clear_on_submit=True):
    title = st.text_input("Title", placeholder="Enter task title")
    description = st.text_area("Description", placeholder="Enter task description")
    submitted = st.form_submit_button("Add Task", use_container_width=True)
    
    if submitted:
        if title.strip():
            if create_todo(title, description):
                st.success("Task added successfully!")
                st.rerun()
            else:
                st.error("Failed to add task")
        else:
            st.warning("Please enter a title")

st.divider()

# Display todos
st.subheader("📋 Your Tasks")
todos = get_todos()

if not todos:
    st.info("No tasks yet. Add one above!")
else:
    for todo in todos:
        with st.container():
            col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
            
            with col1:
                is_completed = st.checkbox(
                    "Done",
                    value=todo.get("is_completed", False),
                    key=f"check_{todo['id']}",
                    label_visibility="collapsed"
                )
                # Update completion status if changed
                if is_completed != todo.get("is_completed", False):
                    update_todo(
                        todo["id"],
                        todo["title"],
                        todo.get("description", ""),
                        is_completed
                    )
                    st.rerun()
            
            with col2:
                if todo.get("is_completed"):
                    st.markdown(f"~~**{todo['title']}**~~")
                else:
                    st.markdown(f"**{todo['title']}**")
                if todo.get("description"):
                    st.caption(todo["description"])
            
            with col3:
                if st.button("🗑️", key=f"delete_{todo['id']}", help="Delete task"):
                    if delete_todo(todo["id"]):
                        st.rerun()
                    else:
                        st.error("Failed to delete")
            
            st.divider()

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About")
    st.write("A simple Todo app built with:")
    st.write("- **Backend:** FastAPI + MongoDB")
    st.write("- **Frontend:** Streamlit")
    
    st.divider()
    
    if st.button("🔄 Refresh", use_container_width=True):
        st.rerun()
    
    st.divider()
    st.caption(f"Total tasks: {len(todos)}")
    completed = sum(1 for t in todos if t.get("is_completed"))
    st.caption(f"Completed: {completed}/{len(todos)}")
