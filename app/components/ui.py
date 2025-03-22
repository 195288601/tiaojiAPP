import streamlit as st
import pandas as pd
import plotly.express as px
from . import utils

# 自定义CSS样式
def load_css():
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1E3A8A;
            text-align: center;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #2563EB;
            margin-bottom: 1rem;
        }
        .card {
            background-color: #F3F4F6;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .success-text {
            color: #10B981;
            font-weight: bold;
        }
        .warning-text {
            color: #F59E0B;
            font-weight: bold;
        }
        .info-icon {
            font-size: 1.5rem;
            margin-right: 0.5rem;
        }
        .stButton>button {
            background-color: #2563EB;
            color: white;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #1E40AF;
            color: white;
        }
        .delete-button>button {
            background-color: #EF4444;
            color: white;
            font-weight: bold;
        }
        .delete-button>button:hover {
            background-color: #DC2626;
            color: white;
        }
        .delete-all-button>button {
            background-color: #991B1B;
            color: white;
            font-weight: bold;
        }
        .delete-all-button>button:hover {
            background-color: #7F1D1D;
            color: white;
        }
        .warning-box {
            background-color: #FECACA;
            border-left: 5px solid #DC2626;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# 添加页面标题
def page_header(title):
    st.markdown(f'<h1 class="main-header">{title}</h1>', unsafe_allow_html=True)

# 显示学校卡片
@st.cache_data(ttl=300, show_spinner=False)
def _prepare_school_card_data(school):
    """准备学校卡片展示所需的数据"""
    # 招生人数处理：可能是整数或字符串（如"2-4"）
    recruitment_display = ""
    recruitment_count = school['recruitment_count']
    if isinstance(recruitment_count, int):
        recruitment_display = f"👨‍🎓 **招生人数**: {recruitment_count}人"
    else:
        recruitment_display = f"👨‍🎓 **招生人数**: {recruitment_count}"
    
    # 分数数据
    score_data = {
        "年份": ["2024", "2023", "2022", "2021"],
        "最高分": [
            school["scores"]["2024"]["max"],
            school["scores"]["2023"]["max"],
            school["scores"]["2022"]["max"],
            school["scores"]["2021"]["max"]
        ],
        "最低分": [
            school["scores"]["2024"]["min"],
            school["scores"]["2023"]["min"],
            school["scores"]["2022"]["min"],
            school["scores"]["2021"]["min"]
        ]
    }
    
    return {
        "name": school['name'],
        "address": school['address'],
        "major": school.get('major', '未提供'),
        "recruitment_display": recruitment_display,
        "score_data": score_data,
        "email": school['contact']['email'],
        "phone": school['contact']['phone'],
        "remark": school.get("remark", ""),
        "id": school.get("id")
    }

def display_school_card(school, col):
    with col:
        # 准备数据
        card_data = _prepare_school_card_data(school)
        
        # 显示卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### {card_data['name']}")
        st.markdown(f"📍 **地址**: {card_data['address']}")
        st.markdown(f"📚 **调剂专业**: {card_data['major']}")
        st.markdown(card_data['recruitment_display'])
        
        st.markdown("#### 历年分数线")
        df = pd.DataFrame(card_data['score_data'])
        st.dataframe(df, hide_index=True)
        
        st.markdown("#### 联系方式")
        st.markdown(f"📧 **邮箱**: {card_data['email']}")
        st.markdown(f"📞 **电话**: {card_data['phone']}")
        
        # 显示备注字段，如果有备注内容则显示
        if card_data["remark"]:
            st.markdown(f"📝 **备注**: {card_data['remark']}")
            
        st.markdown("</div>", unsafe_allow_html=True)

# 显示学校卡片（带删除按钮）
def display_school_card_with_delete(school, col, schools_data):
    with col:
        # 准备数据
        card_data = _prepare_school_card_data(school)
        
        # 显示卡片
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f"### {card_data['name']}")
        st.markdown(f"📍 **地址**: {card_data['address']}")
        st.markdown(f"📚 **调剂专业**: {card_data['major']}")
        st.markdown(card_data['recruitment_display'])
        
        st.markdown("#### 历年分数线")
        df = pd.DataFrame(card_data['score_data'])
        st.dataframe(df, hide_index=True)
        
        st.markdown("#### 联系方式")
        st.markdown(f"📧 **邮箱**: {card_data['email']}")
        st.markdown(f"📞 **电话**: {card_data['phone']}")
        
        # 显示备注字段，如果有备注内容则显示
        if card_data["remark"]:
            st.markdown(f"📝 **备注**: {card_data['remark']}")
            
        # 添加删除按钮
        from components import utils
        delete_col1, delete_col2 = st.columns([4, 1])
        with delete_col2:
            st.markdown('<div class="delete-button">', unsafe_allow_html=True)
            if st.button("删除", key=f"delete_{card_data['id']}"):
                if utils.delete_school(card_data['id'], schools_data):
                    st.success(f"已删除：{card_data['name']}")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)

# 创建学校分数线趋势图
@st.cache_data(ttl=3600)
def create_score_trend_chart(school_data):
    # 准备数据
    years = ["2021", "2022", "2023", "2024"]
    max_scores = [
        school_data["2021最高分"],
        school_data["2022最高分"],
        school_data["2023最高分"],
        school_data["2024最高分"]
    ]
    min_scores = [
        school_data["2021最低分"],
        school_data["2022最低分"],
        school_data["2023最低分"],
        school_data["2024最低分"]
    ]
    
    # 创建DataFrame用于Plotly
    trend_df = pd.DataFrame({
        "年份": years + years,
        "分数": max_scores + min_scores,
        "类型": ["最高分"] * 4 + ["最低分"] * 4
    })
    
    # 创建折线图
    title = f"{school_data['学校名称']}"
    if '调剂专业' in school_data and school_data['调剂专业']:
        title += f" - {school_data['调剂专业']}"
    title += " 历年调剂分数线趋势"
    
    fig = px.line(
        trend_df, 
        x="年份", 
        y="分数", 
        color="类型",
        markers=True,
        title=title,
        color_discrete_map={"最高分": "#3B82F6", "最低分": "#10B981"}
    )
    
    fig.update_layout(
        height=500,
        legend_title_text="",
        xaxis_title="年份",
        yaxis_title="分数",
        hovermode="x unified"
    )
    
    # 优化渲染性能
    fig.update_layout(
        modebar_remove=['lasso2d', 'select2d'],
        hovermode='closest'
    )
    
    return fig

# 创建学校对比图
@st.cache_data(ttl=3600)
def create_school_comparison_chart(schools_df, selected_schools, compare_year):
    # 过滤选中的学校数据
    compare_df = schools_df[schools_df["学校名称"].isin(selected_schools)]
    
    # 准备对比数据
    compare_data = {
        "学校名称": compare_df["学校名称"].tolist(),
        f"{compare_year}最高分": compare_df[f"{compare_year}最高分"].tolist(),
        f"{compare_year}最低分": compare_df[f"{compare_year}最低分"].tolist()
    }
    
    # 如果存在调剂专业字段则添加
    if "调剂专业" in compare_df.columns:
        compare_data["调剂专业"] = compare_df["调剂专业"].tolist()
        
    compare_chart_df = pd.DataFrame(compare_data)
    
    # 创建学校专业标签
    if "调剂专业" in compare_chart_df.columns:
        compare_chart_df["显示名称"] = compare_chart_df.apply(
            lambda x: f"{x['学校名称']} - {x['调剂专业']}" if pd.notna(x['调剂专业']) and x['调剂专业'] else x['学校名称'], 
            axis=1
        )
    else:
        compare_chart_df["显示名称"] = compare_chart_df["学校名称"]
    
    # 重塑数据用于条形图
    chart_df = pd.melt(
        compare_chart_df, 
        id_vars=["显示名称"],
        value_vars=[f"{compare_year}最高分", f"{compare_year}最低分"],
        var_name="分数类型",
        value_name="分数"
    )
    
    # 创建条形图
    fig = px.bar(
        chart_df,
        x="显示名称",
        y="分数",
        color="分数类型",
        barmode="group",
        title=f"{compare_year}年调剂分数线学校对比",
        color_discrete_map={
            f"{compare_year}最高分": "#3B82F6", 
            f"{compare_year}最低分": "#10B981"
        }
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="学校",
        yaxis_title="分数"
    )
    
    # 优化渲染性能
    fig.update_layout(
        modebar_remove=['lasso2d', 'select2d'],
        hovermode='closest'
    )
    
    return fig, compare_chart_df

# 创建招生人数图表
@st.cache_data(ttl=3600)
def create_recruitment_chart(schools_df):
    # 复制DataFrame避免修改原始数据
    df = schools_df.copy()
    
    # 处理招生人数字段，为了排序需要创建数值列
    df['招生人数_排序'] = df['招生人数'].apply(lambda x: 
        int(x) if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
        else int(x.split('-')[0]) if isinstance(x, str) and '-' in x
        else 0
    )
    
    # 按招生人数_排序排序
    top_recruitment = df.sort_values(by="招生人数_排序", ascending=False).head(10)
    
    # 创建学校专业标签
    if "调剂专业" in top_recruitment.columns:
        top_recruitment["显示名称"] = top_recruitment.apply(
            lambda x: f"{x['学校名称']} - {x['调剂专业']}" if pd.notna(x['调剂专业']) and x['调剂专业'] else x['学校名称'], 
            axis=1
        )
    else:
        top_recruitment["显示名称"] = top_recruitment["学校名称"]
    
    # 创建条形图
    fig = px.bar(
        top_recruitment,
        x="显示名称",
        y="招生人数_排序",  # 使用数值列进行绘图
        title="调剂招生人数Top10学校",
        color="招生人数_排序",
        color_continuous_scale="Blues",
        text="招生人数"  # 显示原始招生人数字符串
    )
    
    # 自定义悬停文本
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>招生人数: %{text}<extra></extra>'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="学校",
        yaxis_title="招生人数"
    )
    
    # 优化渲染性能
    fig.update_layout(
        modebar_remove=['lasso2d', 'select2d'],
        hovermode='closest'
    )
    
    return fig

# 显示招生人数统计
@st.cache_data(ttl=3600)
def _calculate_recruitment_stats(schools_df):
    """计算招生人数统计数据，作为缓存函数"""
    # 复制DataFrame避免修改原始数据
    df = schools_df.copy()
    
    # 处理招生人数字段，为了计算需要创建数值列
    df['招生人数_数值'] = df['招生人数'].apply(lambda x: 
        int(x) if isinstance(x, int) or (isinstance(x, str) and x.isdigit())
        else int(x.split('-')[0]) if isinstance(x, str) and '-' in x
        else 0
    )
    
    # 计算统计值
    total_recruitment = df["招生人数_数值"].sum()
    avg_recruitment = df["招生人数_数值"].mean()
    max_recruitment = df["招生人数_数值"].max()
    min_recruitment = df["招生人数_数值"].min()
    
    # 获取最大和最小招生人数的原始值
    max_school = df.loc[df['招生人数_数值'] == max_recruitment, '招生人数'].iloc[0]
    min_school = df.loc[df['招生人数_数值'] == min_recruitment, '招生人数'].iloc[0]
    
    return {
        "total": total_recruitment,
        "avg": avg_recruitment,
        "max": max_school,
        "min": min_school
    }

def display_recruitment_stats(schools_df):
    # 获取缓存的统计数据
    stats = _calculate_recruitment_stats(schools_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总招生人数", f"{stats['total']}人")
    
    with col2:
        st.metric("平均招生人数", f"{stats['avg']:.1f}人")
    
    with col3:
        st.metric("最大招生人数", f"{stats['max']}")
    
    with col4:
        st.metric("最小招生人数", f"{stats['min']}") 