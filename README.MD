# 说明
pyweb助手，内置函数

win系统如需控制隐藏窗口，需安装pywin32

# 安装使用
`pip install easy-pyweb`

# 打包操作
需要安装包
pip install build twine

执行打包
python -m build

推送分支`[testpypi|pypi]`

python -m twine upload --repository testpypi dist/*