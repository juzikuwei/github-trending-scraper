#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitHub趋势项目爬虫示例
~~~~~~~~~~~~~~~~~~~

这个脚本展示了如何使用GitHubTrending类来获取GitHub趋势项目信息，
并展示不同的数据处理方式。
"""

from github_trending import GitHubTrending


def basic_usage():
    """基本用法示例"""
    print("\n===== 基本用法示例 =====")
    
    # 创建爬虫实例
    scraper = GitHubTrending()
    
    # 获取今日趋势项目
    print("获取今日趋势项目...")
    today_trending = scraper.get_trending()
    
    # 显示前5个项目
    print(f"\n获取到 {len(today_trending)} 个项目，显示前5个：")
    for i, repo in enumerate(today_trending[:5], 1):
        print(f"\n--- 项目 {i} ---")
        print(f"项目名称: {repo['name']}")
        print(f"开发者: {repo['developer']}")
        print(f"URL: {repo['url']}")
        print(f"描述: {repo['description']}")
        print(f"星标数: {repo['stars']}")
        print(f"今日新增星标: {repo['stars_today']}")
        print(f"编程语言: {repo['language']}")
    
    # 保存为CSV文件
    scraper.save_to_csv(today_trending, "github_trending_today.csv")


def filter_by_language_and_period():
    """按语言和时间过滤示例"""
    print("\n===== 按语言和时间过滤示例 =====")
    
    # 创建爬虫实例
    scraper = GitHubTrending()
    
    # 获取本周Python语言的趋势项目
    print("获取本周Python语言的趋势项目...")
    python_trending = scraper.get_trending(period="weekly", language="python")
    
    print(f"\n获取到 {len(python_trending)} 个Python项目，显示前3个：")
    for i, repo in enumerate(python_trending[:3], 1):
        print(f"\n--- 项目 {i} ---")
        print(f"项目名称: {repo['name']}")
        print(f"开发者: {repo['developer']}")
        print(f"描述: {repo['description'][:100]}..." if len(repo['description']) > 100 else f"描述: {repo['description']}")
        print(f"星标数: {repo['stars']}")
    
    # 保存为JSON文件
    scraper.save_to_json(python_trending, "python_trending_weekly.json")


def multi_language_comparison():
    """多语言比较示例"""
    print("\n===== 多语言比较示例 =====")
    
    # 创建爬虫实例
    scraper = GitHubTrending()
    
    # 要比较的编程语言列表
    languages = ["python", "javascript", "go", "rust", "java"]
    
    # 收集所有语言的趋势项目
    all_trending = []
    
    print("获取多种编程语言的趋势项目...")
    for lang in languages:
        print(f"正在获取 {lang.capitalize()} 趋势项目...")
        lang_trending = scraper.get_trending(language=lang)
        for repo in lang_trending:
            repo['query_language'] = lang.capitalize()  # 添加查询使用的语言标记
        all_trending.extend(lang_trending)
    
    print(f"\n总共获取到 {len(all_trending)} 个项目")
    
    # 保存汇总数据
    scraper.save_to_csv(all_trending, "multi_language_trending.csv")
    print("多语言趋势数据已保存到 multi_language_trending.csv")


if __name__ == "__main__":
    print("GitHub趋势项目爬虫示例")
    print("=" * 50)
    
    # 运行所有示例
    basic_usage()
    filter_by_language_and_period()
    multi_language_comparison()
    
    print("\n所有示例已完成。请查看生成的CSV和JSON文件！")