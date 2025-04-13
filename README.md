# GitHub趋势项目爬虫

一个简单但功能强大的Python爬虫，用于获取GitHub趋势页面上的热门项目信息。

## 功能特点

- 🔍 抓取GitHub趋势页面上的热门项目
- 🔢 支持按日期范围筛选（今天、本周、本月）
- 🌐 支持按编程语言筛选
- 📊 数据导出为CSV格式
- 📊 数据导出为JSON格式
- 🧩 模块化设计，易于扩展

## 安装

```bash
# 克隆仓库
git clone https://github.com/juzikuwei/github-trending-scraper.git

# 进入目录
cd github-trending-scraper

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基本用法

```python
from github_trending import GitHubTrending

# 创建爬虫实例
scraper = GitHubTrending()

# 获取今日趋势项目
today_trending = scraper.get_trending()

# 打印结果
for repo in today_trending:
    print(f"项目名称: {repo['name']}")
    print(f"开发者: {repo['developer']}")
    print(f"描述: {repo['description']}")
    print(f"星标数: {repo['stars']}")
    print(f"今日新增星标: {repo['stars_today']}")
    print(f"编程语言: {repo['language']}")
    print("------------------------")

# 保存为CSV文件
scraper.save_to_csv(today_trending, "github_trending.csv")

# 保存为JSON文件
scraper.save_to_json(today_trending, "github_trending.json")
```

### 高级用法

```python
# 获取本周Python语言的趋势项目
weekly_python_trending = scraper.get_trending(period="weekly", language="python")

# 获取本月JavaScript语言的趋势项目
monthly_js_trending = scraper.get_trending(period="monthly", language="javascript")

# 获取多个编程语言的趋势项目
multi_lang_trending = []
for lang in ["python", "javascript", "go"]:
    trend = scraper.get_trending(language=lang)
    multi_lang_trending.extend(trend)
    
# 保存为CSV文件
scraper.save_to_csv(multi_lang_trending, "multi_language_trending.csv")
```

## 命令行用法

该工具也支持命令行方式使用：

```bash
# 获取今日趋势项目并保存为CSV
python github_trending.py

# 指定时间范围和语言
python github_trending.py --period weekly --language python

# 自定义输出文件名
python github_trending.py --output my_trending_data.csv

# 输出为JSON格式
python github_trending.py --format json
```

## 依赖项

- Python 3.6+
- requests
- beautifulsoup4
- pandas

## 贡献

欢迎贡献代码、报告问题或提出新功能建议！请随时提交Pull Request或创建Issue。

## 许可证

MIT License