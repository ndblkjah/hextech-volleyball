import streamlit as st
import random
from hextech_pool import HEXTECH_COLLECTION
# 【新增】用來鎖定當前抽到的海克斯選項
if 'current_hextechs' not in st.session_state: st.session_state.current_hextechs = []

st.set_page_config(page_title="專業賽事計分系統", layout="wide")

# --- 1. 狀態初始化 ---
if 'score_a' not in st.session_state: st.session_state.score_a = 0
if 'score_b' not in st.session_state: st.session_state.score_b = 0
# 新增：記錄兩隊目前的「得分率」，預設每球 1 分
if 'sets_a' not in st.session_state: st.session_state.sets_a = 0
if 'sets_b' not in st.session_state: st.session_state.sets_b = 0
if 'point_val_a' not in st.session_state: st.session_state.point_val_a = 1
if 'point_val_b' not in st.session_state: st.session_state.point_val_b = 1

# --- 2. 彈出視窗邏輯 ---
@st.dialog("✨ 觸發海克斯科技！請選擇一項增強效果 ✨")
def hextech_choice(team):
    st.markdown(f"### 🏐 為 **{team} 隊** 選擇你的命運：")
    
    available_keys = list(HEXTECH_COLLECTION.keys())
    choices = random.sample(available_keys, k=min(3, len(available_keys)))
    
    cols = st.columns(3)
    # 【關鍵修改】不再這裡隨機抽卡，而是讀取保險箱裡的選項
    
    for i, key in enumerate(st.session_state.current_hextechs):
        item = HEXTECH_COLLECTION[key]
        with cols[i]:
            ## 加了 team 變數在 key 裡，避免按鈕 ID 衝突
            if st.button(f"{item.name}\n({item.description})", use_container_width=True, key=f"btn_{team}_{key}"):
                
                # 【核心邏輯區分】
                if item.effect_type == "add_score":
                    # 立刻加減分數
                    if team == "A": st.session_state.score_a += item.effect_value
                    else: st.session_state.score_b += item.effect_value
                        
                elif item.effect_type == "modify_rate":
                    # 改變未來的得分率
                    if team == "A": st.session_state.point_val_a += item.effect_value #將=改為+=
                    else: st.session_state.point_val_b += item.effect_value           #將=改為+=
                
                st.success(f"已套用：{item.name}")
                st.rerun()
# --- 3. 視覺組件 ---
def draw_score_card(score, color, font_size):
    st.markdown(f"""
    <div style="background-color: #1E1E1E; color: {color}; font-size: {font_size}px; 
    font-weight: bold; text-align: center; border-radius: 8px; padding: 10px; 
    margin-bottom: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
    font-family: 'Courier New', Courier, monospace;">{score}</div>
    """, unsafe_allow_html=True)

# --- 4. 介面呈現 ---
st.title("🏐 賽事即時計分板")
c1, c3, c4, c2 = st.columns([4,1,1,4])

with c1:
    # 這裡會顯示目前的得分率，讓你知道狀態有沒有改變
    st.metric("隊伍 A 分數", st.session_state.score_a, delta=f"目前每球 +{st.session_state.point_val_a} 分")
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if st.button("➕ A 隊得分", use_container_width=True):
            # 不再是 +1，而是加上目前的 point_val_a
            #st.session_state.score_a += st.session_state.point_val_a
            st.session_state.score_a += 1
            st.rerun()
    with btn_col2:
        if st.button("➖ A隊扣分", use_container_width=True, key="minus_a"):
            st.session_state.score_a -= 1
            st.rerun()
            
    st.divider()
    if st.button("✨ 隊伍 A 觸發海克斯", use_container_width=True):
        # 【關鍵修改】只有按下的瞬間才抽卡，並存入保險箱
        available_keys = list(HEXTECH_COLLECTION.keys())
        st.session_state.current_hextechs = random.sample(available_keys, k=min(3, len(available_keys)))
        hextech_choice("A")

with c2:
    draw_score_card("隊伍 B 分數", st.session_state.score_b, delta=f"目前每球 +{st.session_state.point_val_b} 分")
    
    btn_col3, btn_col4 = st.columns(2)
    with btn_col3:S
        if st.button("➕ B 隊得分", use_container_width=True):
            # 不再是 +1，而是加上目前的 point_val_b
            #st.session_state.score_b += st.session_state.point_val_b
            st.session_state.score_b += 1
            st.rerun()
    with btn_col4:
        if st.button("➖ B隊扣分", use_container_width=True, key="minus_b"):
            st.session_state.score_b -= 1
            st.rerun()
            
    st.divider()
    if st.button("✨ 隊伍 B 觸發海克斯", use_container_width=True):
        # 【關鍵修改】只有按下的瞬間才抽卡，並存入保險箱
        available_keys = list(HEXTECH_COLLECTION.keys())
        st.session_state.current_hextechs = random.sample(available_keys, k=min(3, len(available_keys)))
        hextech_choice("B")
with c3:
    draw_score_card(st.session_state.sets_a, "#FF4136", 60)
    if st.button("A 贏此局", use_container_width=True):
        st.session_state.sets_a += 1
        st.session_state.score_a, st.session_state.score_b = 0, 0
        st.rerun()
with c4:
    draw_score_card(st.session_state.sets_b, "#FF4136", 60)
    if st.button("B 贏此局", use_container_width=True):
        st.session_state.sets_b += 1
        st.session_state.score_a, st.session_state.score_b = 0, 0
        st.rerun()
        
st.divider()

# --- 5. 控制中心 ---
ctrl1, ctrl2 = st.columns(2)
with ctrl1:
    if st.button("清空本局比數 (保留局數)", use_container_width=True):
        st.session_state.score_a = 0
        st.session_state.score_b = 0
        st.rerun()
with ctrl2:
    if st.button("全賽事重置 (全部歸零)", use_container_width=True):
        st.session_state.score_a = 0
        st.session_state.score_b = 0
        st.session_state.sets_a = 0
        st.session_state.sets_b = 0
        st.rerun()