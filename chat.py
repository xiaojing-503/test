from skeleton.sql_value import extract_values
from skeleton.mapping import get_table_column_value
from utils.get_sql_schema_prompt import format_database_schema
from skeleton.sql_skeleton import get_sql_schema, get_sql_skeleton
import streamlit as st
import sqlite3
import json
from datetime import datetime
from streamlit.components.v1 import html  # 新增导入
from openai import OpenAI
import os

# 连接 SQLite 数据库
DB_FILE = "/root/Schema-Value/code/chat_history.db"
DB_PATH = '/root/Schema-Value/data/bird/bird/dev/dev_databases'

def get_db_connection():
    """建立数据库连接并创建表"""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT,
            title TEXT,
            messages TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

conn, cursor = get_db_connection()

# 读取历史记录
def load_history():
    cursor.execute("SELECT id, time, title, messages FROM history ORDER BY id DESC")
    return [{"id": row[0], "time": row[1], "title": row[2], "messages": json.loads(row[3])} for row in cursor.fetchall()]

# 保存历史记录
def save_history(title, messages):
    cursor.execute("INSERT INTO history (time, title, messages) VALUES (?, ?, ?)", 
                   (datetime.now().strftime("%m/%d %H:%M"), title, json.dumps(messages, ensure_ascii=False)))
    conn.commit()

# 删除单条历史记录
def delete_history(record_id):
    cursor.execute("DELETE FROM history WHERE id=?", (record_id,))
    conn.commit()

# 清空所有历史记录
def clear_history():
    cursor.execute("DELETE FROM history")
    conn.commit()

# 从数据库加载历史记录
st.session_state.history = load_history()

# Streamlit 页面设置
st.set_page_config(page_title="简洁聊天助手", page_icon="💬", layout="centered")

# 新增滚动到底部函数
def scroll_bottom():
    js = """
    <script>
        setTimeout(function() {
            var target = window.parent.document.querySelector('section.main');
            if (target) {
                target.scrollTo(0, target.scrollHeight);
            }
        }, 100);
    </script>
    """
    html(js)

# 侧边栏：对话历史
with st.sidebar:
    st.header("📋 对话历史")

    # 新建聊天按钮
    if st.button("➕ 新建聊天", use_container_width=True):
        if st.session_state.messages:
            chat_title = st.session_state.messages[0]["content"][:18] + "..." if len(st.session_state.messages[0]["content"]) > 20 else st.session_state.messages[0]["content"]
            save_history(chat_title, st.session_state.messages)
            st.session_state.history = load_history()
            st.session_state.messages = []

    st.divider()

    # 历史聊天记录
    for record in st.session_state.history:
        cols = st.columns([0.8, 0.2])

        # 加载聊天记录
        if cols[0].button(f"**{record['title']}**\n{record['time']}", key=f"load_{record['id']}", use_container_width=True, help="点击加载该对话"):
            st.session_state.messages = record["messages"]

        # 删除按钮
        if cols[1].button("×", key=f"del_{record['id']}", help="删除该聊天"):
            delete_history(record["id"])
            st.session_state.history = load_history()

    # 清空所有历史记录
    if st.session_state.history and st.button("清空历史", use_container_width=True):
        clear_history()
        st.session_state.history = []

# 主界面标题
st.title("💬 SQL SQL")

# 显示当前对话内容
if "messages" not in st.session_state:
    st.session_state.messages = []

# 反向显示消息，确保最新的消息在底部
for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# 新增：显示消息后自动滚动
scroll_bottom()

st.markdown('<div class="fixed-container">', unsafe_allow_html=True)
st.divider()

# 初始化状态
if "show_input" not in st.session_state:
    st.session_state.show_input = False
if "selected_button" not in st.session_state:
    st.session_state.selected_button = None



# 读取 JSON 数据
DATA_PATH = "/root/Schema-Value/data/bird/dataset/bird_dev_copy2.json"

def load_data():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {item["id"]: item for item in data}  # 以 id 作为键，方便快速查找
    except Exception as e:
        st.error(f"加载数据失败: {e}")
        return {}
def show_sql_info(input):
    # 加载数据
    data_dict = load_data()
    # print(data_dict[input])
    # print(input)
    input_id = int(input)
    
    if input_id in data_dict:
        item = data_dict[input_id]
        # 存储 db_id 到 session_state
        st.session_state.db_id = item["db_id"]
        # 组合返回信息
        output_message = f"""
        **Question**: {item['question']}\n
        **evidence**: {item['evidence']}\n
        **Gold SQL**: {item['err_gold']}\n
        **Pred SQL**: {item['err_pred']}\n
        **error**: {item['err_type']}
        """
        
        return output_message  # 这里返回信息

    return "未找到该 SQL 相关信息, 请输入合法的id!"  # 如果输入不在数据中，返回提示

def parse_schema(sql):
    sql_schemas = get_sql_schema(sql) 
    values = extract_values(sql)

    schema_mapping = get_table_column_value(DB_PATH, st.session_state.db_id, sql_schemas, values)  

    # 假设format_database_schema是已定义的函数，用来格式化架构  
    new_schema = format_database_schema(schema_mapping)  
    
    return f"解析的 Schema 结果：{new_schema}"

def parse_skeleton(sql):
    skeleton = get_sql_skeleton(sql)
    return f"SQL Skeleton 解析结果：{skeleton}"



def get_deepseek_response(prompt):
    client = OpenAI(api_key="sk-eotrzevibhyamnthslaxmuzqvuemgsgwkiudtauwmfgwspyd", base_url="https://api.siliconflow.cn/v1")
    response = client.chat.completions.create(
        model='deepseek-ai/DeepSeek-V3',
        messages=[
                {"role": "user", "content": prompt},
            ],
        stream=False
    )
    return response.choices[0].message.content

def execute_sql(sql):
    """
    在子进程中执行 SQL 查询并返回结果。
    
    参数:
    database_name (str): SQLite 数据库路径。
    sql (str): SQL 查询语句。
    
    返回:
    list: 查询结果。
    """
    database_name = os.path.join(DB_PATH, st.session_state.db_id, f"{st.session_state.db_id}.sqlite")
    try:
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return f"执行 SQL 结果：{result}"
    except sqlite3.Error as e:
        return f"SQLite 错误: {e}"
    
def ask_llm(prompt):
    response = get_deepseek_response(prompt)
    return f"LLM 回答：{response}"

cols = st.columns(5)
button_labels = ["显示SQL信息", "解析schema", "解析skeleton", "执行SQL", "提问LLM"]
button_functions = [show_sql_info, parse_schema, parse_skeleton, execute_sql, ask_llm]

# 遍历按钮
for i in range(5):
    if cols[i].button(button_labels[i], key=f"btn_{i}"):
        st.session_state.show_input = True  # 显示输入框
        st.session_state.selected_button = i  # 记录点击的按钮

# 只有点击按钮后，才显示输入框
if st.session_state.show_input:
    prompt = st.chat_input(button_labels[st.session_state.selected_button]+"....")
    
    if prompt:  # 只有在用户输入后才记录消息
        # 先显示用户输入
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

        # 处理输入并生成输出
        output_message = button_functions[st.session_state.selected_button](prompt)
        st.session_state.messages.append({"role": "assistant", "content": output_message})
        
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(output_message)

        # 输入完成后，隐藏输入框
        st.session_state.show_input = False

