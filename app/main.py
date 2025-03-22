import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime
import plotly.express as px
from components import utils, ui

# 设置页面配置
st.set_page_config(
    page_title="考研调剂系统",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# 考研调剂系统\n调剂信息管理平台"
    }
)

# 加载CSS样式
ui.load_css()

# 确保数据目录存在
data_dir = utils.get_data_dir()
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# 检查数据文件是否存在，如果不存在则创建一个空文件
if not os.path.exists(utils.get_data_file()):
    utils.save_data([])

# 初始化会话状态
if 'schools_data' not in st.session_state:
    st.session_state.schools_data = utils.load_data()
if 'last_reload_time' not in st.session_state:
    st.session_state.last_reload_time = datetime.now()
if 'needs_rerun' not in st.session_state:
    st.session_state.needs_rerun = False

# 定义重新加载数据的函数
def reload_data():
    st.session_state.schools_data = utils.load_data()
    st.session_state.last_reload_time = datetime.now()

# 只在会话开始或明确需要时重新加载数据
if (datetime.now() - st.session_state.last_reload_time).total_seconds() > 60:
    reload_data()

# 数据变更后的回调函数，用于避免多次重新运行
def schedule_rerun():
    st.session_state.needs_rerun = True

# 检查是否需要重新运行
if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    reload_data()
    st.rerun()

# 侧边栏导航
st.sidebar.markdown('<h2 class="sub-header">考研调剂系统</h2>', unsafe_allow_html=True)
app_mode = st.sidebar.selectbox("选择功能", ["首页", "添加学校", "查看数据", "删除学校", "数据导入", "数据分析"])

# 首页
if app_mode == "首页":
    ui.page_header("考研调剂信息管理系统")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 欢迎使用考研调剂系统！")
    st.markdown("本系统可以帮助您管理和查询考研调剂信息，支持：")
    st.markdown("- ✅ 手动添加调剂学校信息")
    st.markdown("- ✅ 批量导入Excel/CSV数据")
    st.markdown("- ✅ 可视化展示历年分数线")
    st.markdown("- ✅ 高级筛选功能")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 系统信息")
        st.markdown(f"- 当前收录学校数量：**{len(st.session_state.schools_data)}**")
        st.markdown(f"- 最近更新时间：**{st.session_state.last_reload_time.strftime('%Y-%m-%d %H:%M:%S')}**")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 快速入门")
        st.markdown("1. 点击侧边栏的「添加学校」来手动添加学校信息")
        st.markdown("2. 点击侧边栏的「数据导入」来批量导入学校数据")
        st.markdown("3. 点击侧边栏的「查看数据」来浏览和搜索现有数据")
        st.markdown("4. 点击侧边栏的「数据分析」查看数据统计和可视化")
        st.markdown("</div>", unsafe_allow_html=True)

# 添加学校页面
elif app_mode == "添加学校":
    ui.page_header("添加调剂学校信息")
    
    with st.form("school_form"):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 基本信息")
        school_name = st.text_input("学校名称", key="name")
        school_address = st.text_input("学校地址", key="address")
        school_major = st.text_input("调剂专业", key="major")
        
        recruitment_input_type = st.radio(
            "招生人数输入方式",
            ["精确人数", "范围人数（如2-4）"],
            horizontal=True,
            key="recruitment_type"
        )
        
        if recruitment_input_type == "精确人数":
            recruitment_count = st.number_input("招生人数", min_value=0, value=0, step=1, key="count")
        else:
            recruitment_count = st.text_input("招生人数（如2-4）", key="count_range")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 历年调剂分数线")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 2024年")
            score_2024_max = st.number_input("2024年最高分", min_value=0, value=0, key="2024_max")
            score_2024_min = st.number_input("2024年最低分", min_value=0, value=0, key="2024_min")
            
            st.markdown("#### 2023年")
            score_2023_max = st.number_input("2023年最高分", min_value=0, value=0, key="2023_max")
            score_2023_min = st.number_input("2023年最低分", min_value=0, value=0, key="2023_min")
        
        with col2:
            st.markdown("#### 2022年")
            score_2022_max = st.number_input("2022年最高分", min_value=0, value=0, key="2022_max")
            score_2022_min = st.number_input("2022年最低分", min_value=0, value=0, key="2022_min")
            
            st.markdown("#### 2021年")
            score_2021_max = st.number_input("2021年最高分", min_value=0, value=0, key="2021_max")
            score_2021_min = st.number_input("2021年最低分", min_value=0, value=0, key="2021_min")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 联系方式")
        email = st.text_input("邮箱", key="email")
        phone = st.text_input("电话", key="phone")
        remark = st.text_input("备注（如分数范围：270-310分或300分左右）", key="remark")
        st.markdown("</div>", unsafe_allow_html=True)
        
        submit_button = st.form_submit_button("保存学校信息")
    
    if submit_button:
        if not school_name:
            st.error("学校名称不能为空！")
        else:
            # 创建新学校数据
            new_school = {
                "name": school_name,
                "address": school_address,
                "major": school_major,
                "recruitment_count": recruitment_count,
                "scores": {
                    "2024": {"max": score_2024_max, "min": score_2024_min},
                    "2023": {"max": score_2023_max, "min": score_2023_min},
                    "2022": {"max": score_2022_max, "min": score_2022_min},
                    "2021": {"max": score_2021_max, "min": score_2021_min}
                },
                "contact": {
                    "email": email,
                    "phone": phone
                },
                "remark": remark
            }
            
            # 添加到数据列表并保存
            utils.add_school(new_school, st.session_state.schools_data)
            schedule_rerun()
            
            st.success(f"成功添加学校：{school_name}")
            st.balloons()

# 查看数据页面
elif app_mode == "查看数据":
    ui.page_header("查看调剂学校信息")
    
    if not st.session_state.schools_data:
        st.warning("当前没有学校数据，请先添加学校或导入数据。")
    else:
        # 搜索和筛选
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 搜索和筛选")
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            search_query = st.text_input("搜索学校名称", "")
        
        with col2:
            min_score = st.number_input("2024年最低分不低于", min_value=0, value=0)
        
        with col3:
            sort_option = st.selectbox(
                "排序方式",
                ["名称 (A-Z)", "名称 (Z-A)", "2024最高分 (高-低)", "2024最低分 (高-低)"]
            )
            
        with col4:
            # 添加显示删除按钮的选项
            show_delete = st.checkbox("显示删除", False)
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # 使用容器避免整页重载
        results_container = st.container()
        
        with results_container:
            # 过滤数据
            @st.cache_data(ttl=30, show_spinner=False)
            def filter_and_sort_schools(schools_data, search_query, min_score, sort_option):
                filtered_data = schools_data.copy()
                
                if search_query:
                    filtered_data = [
                        school for school in filtered_data
                        if search_query.lower() in school["name"].lower()
                    ]
                
                if min_score > 0:
                    filtered_data = [
                        school for school in filtered_data
                        if school["scores"]["2024"]["min"] >= min_score
                    ]
                
                # 排序数据
                if sort_option == "名称 (A-Z)":
                    filtered_data = sorted(filtered_data, key=lambda x: x["name"])
                elif sort_option == "名称 (Z-A)":
                    filtered_data = sorted(filtered_data, key=lambda x: x["name"], reverse=True)
                elif sort_option == "2024最高分 (高-低)":
                    filtered_data = sorted(filtered_data, key=lambda x: x["scores"]["2024"]["max"], reverse=True)
                elif sort_option == "2024最低分 (高-低)":
                    filtered_data = sorted(filtered_data, key=lambda x: x["scores"]["2024"]["min"], reverse=True)
                
                return filtered_data
            
            # 使用缓存过滤和排序
            filtered_data = filter_and_sort_schools(st.session_state.schools_data, search_query, min_score, sort_option)
            
            # 显示学校卡片
            if not filtered_data:
                st.info("没有找到符合条件的学校。")
            else:
                # 添加分页功能
                total_schools = len(filtered_data)
                schools_per_page = 6
                total_pages = (total_schools + schools_per_page - 1) // schools_per_page  # 向上取整
                
                # 初始化分页状态
                if 'current_page' not in st.session_state:
                    st.session_state.current_page = 1
                
                # 确保当前页码在有效范围内
                if st.session_state.current_page > total_pages:
                    st.session_state.current_page = 1
                
                # 显示找到的学校总数和当前页数
                st.markdown(f"### 找到 {total_schools} 所学校 (第 {st.session_state.current_page}/{total_pages} 页)")
                
                # 计算当前页的学校
                start_idx = (st.session_state.current_page - 1) * schools_per_page
                end_idx = min(start_idx + schools_per_page, total_schools)
                current_page_schools = filtered_data[start_idx:end_idx]
                
                # 每行显示2个学校卡片
                for i in range(0, len(current_page_schools), 2):
                    cols = st.columns(2)
                    
                    # 第一个卡片
                    if i < len(current_page_schools):
                        if show_delete:
                            ui.display_school_card_with_delete(current_page_schools[i], cols[0], st.session_state.schools_data)
                        else:
                            ui.display_school_card(current_page_schools[i], cols[0])
                    
                    # 第二个卡片
                    if i + 1 < len(current_page_schools):
                        if show_delete:
                            ui.display_school_card_with_delete(current_page_schools[i + 1], cols[1], st.session_state.schools_data)
                        else:
                            ui.display_school_card(current_page_schools[i + 1], cols[1])
                
                # 分页控制器 - 移到页面底部
                st.markdown("---")
                pagination_col1, pagination_col2, pagination_col3 = st.columns([2, 3, 2])
                with pagination_col2:
                    # 使用两列布局展示页面控制
                    page_col1, page_col2, page_col3, page_col4 = st.columns([1, 1, 1, 1])
                    
                    with page_col1:
                        if st.button("⏮️ 首页", disabled=st.session_state.current_page == 1):
                            st.session_state.current_page = 1
                            st.rerun()
                    
                    with page_col2:
                        if st.button("⬅️ 上一页", disabled=st.session_state.current_page == 1):
                            st.session_state.current_page -= 1
                            st.rerun()
                    
                    with page_col3:
                        if st.button("➡️ 下一页", disabled=st.session_state.current_page == total_pages):
                            st.session_state.current_page += 1
                            st.rerun()
                            
                    with page_col4:
                        if st.button("⏭️ 末页", disabled=st.session_state.current_page == total_pages):
                            st.session_state.current_page = total_pages
                            st.rerun()

# 删除学校页面
elif app_mode == "删除学校":
    ui.page_header("删除学校信息")
    
    if not st.session_state.schools_data:
        st.warning("当前没有学校数据，请先添加学校或导入数据。")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["单个删除", "批量删除", "全部删除"])
        
        with tab1:
            st.markdown("### 单个删除学校")
            st.markdown("请选择要删除的学校：")
            
            # 创建学校选择下拉框
            @st.cache_data(ttl=30, show_spinner=False)
            def get_school_options(schools_data):
                return [f"{school['id']} - {school['name']} - {school.get('major', '无专业')}" for school in schools_data]
            
            school_options = get_school_options(st.session_state.schools_data)
            selected_school = st.selectbox("选择要删除的学校", school_options)
            
            if selected_school:
                school_id = int(selected_school.split(" - ")[0])
                
                # 查找选中的学校详情
                selected_school_data = next((school for school in st.session_state.schools_data if school["id"] == school_id), None)
                
                if selected_school_data:
                    # 显示学校详情
                    st.markdown("#### 学校详情")
                    st.markdown(f"**学校名称**: {selected_school_data['name']}")
                    st.markdown(f"**专业**: {selected_school_data.get('major', '无专业')}")
                    st.markdown(f"**地址**: {selected_school_data['address']}")
                    
                    # 删除确认
                    if st.button("确认删除", key="single_delete"):
                        if utils.delete_school(school_id, st.session_state.schools_data):
                            st.success(f"已成功删除学校：{selected_school_data['name']}")
                            schedule_rerun()
                        else:
                            st.error("删除失败，请重试。")
        
        with tab2:
            st.markdown("### 批量删除学校")
            st.markdown("请选择要删除的学校：")
            
            # 创建学校多选框
            @st.cache_data(ttl=30, show_spinner=False)
            def get_school_options_dict(schools_data):
                return {f"{school['id']} - {school['name']} - {school.get('major', '无专业')}": school["id"] for school in schools_data}
            
            school_options_dict = get_school_options_dict(st.session_state.schools_data)
            selected_schools = st.multiselect("选择要删除的学校（可多选）", list(school_options_dict.keys()))
            
            if selected_schools:
                # 获取选中的学校ID列表
                selected_school_ids = [school_options_dict[school] for school in selected_schools]
                
                # 删除确认
                if st.button("确认批量删除", key="batch_delete"):
                    deleted_count = utils.batch_delete_schools(selected_school_ids, st.session_state.schools_data)
                    if deleted_count > 0:
                        st.success(f"已成功删除 {deleted_count} 所学校")
                        schedule_rerun()
                    else:
                        st.error("删除失败，请重试。")
            
            # 按条件批量删除
            st.markdown("### 按条件批量删除")
            
            # 将数据转换为DataFrame进行筛选
            schools_df = utils.json_to_dataframe(st.session_state.schools_data)
            
            col1, col2 = st.columns(2)
            with col1:
                min_score_filter = st.number_input("2024年最低分低于", min_value=0, value=0)
            with col2:
                max_score_filter = st.number_input("2024年最高分低于", min_value=0, value=0)
            
            if min_score_filter > 0 or max_score_filter > 0:
                # 筛选出符合条件的学校
                @st.cache_data(ttl=30, show_spinner=False)
                def filter_schools_by_score(schools_data, min_score_filter, max_score_filter):
                    filtered_schools = []
                    for school in schools_data:
                        if (min_score_filter > 0 and school["scores"]["2024"]["min"] < min_score_filter) or \
                           (max_score_filter > 0 and school["scores"]["2024"]["max"] < max_score_filter):
                            filtered_schools.append(school)
                    return filtered_schools
                
                filtered_schools = filter_schools_by_score(st.session_state.schools_data, min_score_filter, max_score_filter)
                
                if filtered_schools:
                    st.markdown(f"#### 符合条件的学校（共 {len(filtered_schools)} 所）")
                    
                    # 显示符合条件的学校列表
                    filtered_df = utils.json_to_dataframe(filtered_schools)
                    st.dataframe(filtered_df[["学校名称", "调剂专业", "2024最高分", "2024最低分"]], hide_index=True)
                    
                    # 获取符合条件的学校ID列表
                    filtered_school_ids = [school["id"] for school in filtered_schools]
                    
                    # 删除确认
                    if st.button("确认批量删除符合条件的学校", key="condition_delete"):
                        deleted_count = utils.batch_delete_schools(filtered_school_ids, st.session_state.schools_data)
                        if deleted_count > 0:
                            st.success(f"已成功删除 {deleted_count} 所学校")
                            schedule_rerun()
                        else:
                            st.error("删除失败，请重试。")
                else:
                    st.info("没有找到符合条件的学校。")
        
        with tab3:
            st.markdown("### 删除所有学校")
            st.markdown('<div class="warning-box">', unsafe_allow_html=True)
            st.markdown("⚠️ **警告：此操作将删除所有学校数据，且无法恢复！**")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # 显示当前学校总数
            st.markdown(f"**当前系统共有 {len(st.session_state.schools_data)} 所学校数据**")
            
            # 添加确认选项
            confirm_delete = st.checkbox("我已理解此操作的风险，并确认要删除所有学校数据", key="confirm_all_delete")
            
            if confirm_delete:
                st.markdown('<div class="delete-all-button">', unsafe_allow_html=True)
                if st.button("确认全部删除", key="delete_all_button"):
                    if utils.delete_all_schools():
                        st.success(f"已成功删除所有学校数据（共 {len(st.session_state.schools_data)} 所）")
                        # 清空本地变量
                        st.session_state.schools_data.clear()
                        schedule_rerun()
                    else:
                        st.error("删除操作失败，请重试。")
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# 数据导入页面
elif app_mode == "数据导入":
    ui.page_header("批量导入学校数据")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### 通过Excel/CSV文件导入数据")
    st.markdown("""
    您可以通过上传Excel或CSV文件批量导入学校数据。文件格式要求：
    
    1. 必须包含以下列：`学校名称`, `学校地址`, `招生人数`, `2024最高分`, `2024最低分`, `2023最高分`, `2023最低分`, `2022最高分`, `2022最低分`, `2021最高分`, `2021最低分`, `邮箱`, `电话`
    2. 第一行必须是列名
    3. Excel文件请保存为`.xlsx`或`.xls`格式，CSV文件请保存为`.csv`格式
    """)
    
    # 创建模板
    df_template = utils.create_template_data()
    
    # 创建一个临时Excel文件作为模板
    template_file = os.path.join(data_dir, "template.xlsx")
    df_template.to_excel(template_file, index=False)
    
    with open(template_file, "rb") as file:
        st.download_button(
            label="📥 下载导入模板",
            data=file,
            file_name="调剂学校数据导入模板.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # 文件上传
    uploaded_file = st.file_uploader("上传Excel/CSV文件", type=["xlsx", "xls", "csv"])
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # 尝试导入文件
        success, message, new_schools = utils.import_from_file(uploaded_file, st.session_state.schools_data)
        
        if not success:
            st.error(message)
        else:
            st.success(message)
            
            # 预览导入的数据
            if new_schools and len(new_schools) > 0:
                preview_df = utils.json_to_dataframe(new_schools)
                st.dataframe(preview_df.head(5), hide_index=True)
                
                if st.button("确认导入数据"):
                    # 添加到现有数据
                    st.session_state.schools_data.extend(new_schools)
                    
                    # 保存数据
                    utils.save_data(st.session_state.schools_data)
                    schedule_rerun()
                    
                    st.success(f"成功导入 {len(new_schools)} 所学校数据！")
                    st.balloons()

# 数据分析页面
elif app_mode == "数据分析":
    ui.page_header("调剂数据分析")
    
    if not st.session_state.schools_data:
        st.warning("当前没有学校数据，请先添加学校或导入数据。")
    else:
        # 转换为DataFrame进行分析
        schools_df = utils.json_to_dataframe(st.session_state.schools_data)
        
        # 分析TAB
        tab1, tab2, tab3 = st.tabs(["分数线趋势", "学校对比", "招生人数分析"])
        
        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 历年调剂分数线趋势")
            
            # 选择学校
            selected_school = st.selectbox(
                "选择学校查看历年分数线趋势",
                schools_df["学校名称"].tolist()
            )
            
            school_data = schools_df[schools_df["学校名称"] == selected_school].iloc[0]
            
            # 创建折线图
            fig = ui.create_score_trend_chart(school_data)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 学校分数线对比")
            
            # 选择多个学校进行对比
            selected_schools = st.multiselect(
                "选择要对比的学校 (最多5所)",
                schools_df["学校名称"].tolist(),
                max_selections=5
            )
            
            if selected_schools:
                # 选择对比的年份
                compare_year = st.selectbox(
                    "选择对比的年份",
                    ["2024", "2023", "2022", "2021"]
                )
                
                # 创建对比图表
                fig, compare_df = ui.create_school_comparison_chart(
                    schools_df, selected_schools, compare_year
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # 表格对比
                st.markdown("#### 详细数据对比")
                st.dataframe(compare_df, hide_index=True)
            else:
                st.info("请选择至少一所学校进行对比")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("### 招生人数分析")
            
            # 创建招生人数图表
            fig = ui.create_recruitment_chart(schools_df)
            st.plotly_chart(fig, use_container_width=True)
            
            # 招生人数统计
            st.markdown("#### 招生人数统计")
            ui.display_recruitment_stats(schools_df)
            
            st.markdown("</div>", unsafe_allow_html=True) 