@echo off
echo 正在启动考研调剂系统...
echo 请确保已安装所需依赖，如未安装，请运行：pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

streamlit run app/main.py

pause 