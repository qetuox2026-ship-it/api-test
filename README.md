# Restful Booker API 自动化测试

基于 Python、pytest 和 requests 搭建的接口自动化测试项目。

## 项目功能

- 酒店预订查询、创建、修改和删除
- Token 登录鉴权
- pytest fixture 测试数据管理
- 测试数据自动创建和清理
- JSON 测试数据驱动
- 多环境配置
- smoke 和 regression 测试分组
- 请求日志
- HTML 和 JUnit 测试报告

## 技术栈

- Python 3
- pytest
- requests
- pytest-html
- Git

## 项目结构

```text
api-test/
├── clients/             # 接口客户端
├── config/              # 环境配置
├── data/                # 测试数据
├── tests/               # 测试用例
├── utils/               # 日志等公共工具
├── conftest.py          # pytest fixture
├── pytest.ini           # pytest 配置
└── requirements.txt     # Python 依赖

python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

## Jenkins 持续集成

项目通过 Jenkins Pipeline 自动执行测试：

- 手动选择 smoke、regression 或 all
- GitHub 出现新提交后自动执行 smoke
- 每天凌晨自动执行 regression
- 使用 Jenkins Credentials 管理接口账号
- 自动生成 HTML 和 JUnit 测试报告
- 自动归档测试日志和报告