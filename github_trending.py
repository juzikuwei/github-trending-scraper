#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
GitHub趋势项目爬虫
~~~~~~~~~~~~~~~~

这个脚本可以爬取GitHub趋势页面上的热门项目信息，
支持按日期和编程语言筛选，并可将数据导出为CSV或JSON格式。
"""

import os
import json
import argparse
import csv
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

import requests
from bs4 import BeautifulSoup
import pandas as pd


class GitHubTrending:
    """GitHub趋势项目爬虫类"""

    BASE_URL = "https://github.com/trending"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    }

    def __init__(self):
        """初始化GitHub趋势爬虫"""
        self.session = requests.Session()
        self.session.headers.update(self.HEADERS)

    def get_trending(self, period: str = "daily", language: str = None) -> List[Dict[str, Any]]:
        """
        获取GitHub趋势项目信息

        参数:
            period: 时间范围，可选值为 'daily'(今日)、'weekly'(本周)、'monthly'(本月)，默认为'daily'
            language: 编程语言，例如'python'、'javascript'等，默认为None(所有语言)

        返回:
            包含项目信息的字典列表
        """
        # 构建URL
        url = self.BASE_URL
        if language:
            url = f"{url}/{language}"
        
        # 添加时间范围参数
        period_mapping = {"daily": "daily", "weekly": "weekly", "monthly": "monthly"}
        if period in period_mapping:
            url = f"{url}?since={period_mapping[period]}"

        try:
            # 发送请求
            response = self.session.get(url)
            response.raise_for_status()  # 检查请求是否成功
            
            # 解析HTML
            return self._parse_html(response.text)
        
        except requests.RequestException as e:
            print(f"请求出错: {e}")
            return []

    def _parse_html(self, html_content: str) -> List[Dict[str, Any]]:
        """
        解析HTML内容，提取项目信息

        参数:
            html_content: HTML内容

        返回:
            包含项目信息的字典列表
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        repositories = []

        # 查找所有项目块
        article_blocks = soup.select('article.Box-row')
        
        for article in article_blocks:
            repo_info = {}
            
            # 提取项目名称和开发者
            repo_name_element = article.select_one('h2.h3.lh-condensed a')
            if repo_name_element:
                full_name = repo_name_element.text.strip().replace(" ", "").replace("\\n", "")
                if "/" in full_name:
                    developer, name = full_name.split('/', 1)
                    repo_info['developer'] = developer.strip()
                    repo_info['name'] = name.strip()
                else:
                    repo_info['name'] = full_name
                    repo_info['developer'] = ""
            
            # 提取项目URL
            if repo_name_element and repo_name_element.get('href'):
                repo_info['url'] = f"https://github.com{repo_name_element.get('href')}"
            
            # 提取项目描述
            description_element = article.select_one('p')
            repo_info['description'] = description_element.text.strip() if description_element else ""
            
            # 提取编程语言
            language_element = article.select_one('span[itemprop="programmingLanguage"]')
            repo_info['language'] = language_element.text.strip() if language_element else "未知"
            
            # 提取星标数
            stars_element = article.select('a.Link--muted')[0] if article.select('a.Link--muted') else None
            repo_info['stars'] = stars_element.text.strip().replace(",", "") if stars_element else "0"
            
            # 提取今日新增星标
            stars_today_element = article.select_one('span.d-inline-block.float-sm-right')
            stars_today = "0"
            if stars_today_element:
                stars_text = stars_today_element.text.strip()
                stars_today = ''.join(filter(str.isdigit, stars_text)) or "0"
            repo_info['stars_today'] = stars_today
            
            # 提取分叉数
            forks_element = article.select('a.Link--muted')[1] if len(article.select('a.Link--muted')) > 1 else None
            repo_info['forks'] = forks_element.text.strip().replace(",", "") if forks_element else "0"
            
            repositories.append(repo_info)
        
        return repositories

    def save_to_csv(self, data: List[Dict[str, Any]], filename: str) -> None:
        """
        将数据保存为CSV文件

        参数:
            data: 要保存的数据
            filename: 文件名
        """
        if not data:
            print("没有数据可保存")
            return
        
        try:
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存CSV文件时出错: {e}")

    def save_to_json(self, data: List[Dict[str, Any]], filename: str) -> None:
        """
        将数据保存为JSON文件

        参数:
            data: 要保存的数据
            filename: 文件名
        """
        if not data:
            print("没有数据可保存")
            return
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存JSON文件时出错: {e}")


def main():
    """主函数，处理命令行参数并执行爬虫"""
    parser = argparse.ArgumentParser(description='GitHub趋势项目爬虫')
    parser.add_argument('--period', type=str, default='daily',
                        choices=['daily', 'weekly', 'monthly'],
                        help='时间范围：daily(今日)、weekly(本周)、monthly(本月)')
    parser.add_argument('--language', type=str, default=None,
                        help='编程语言，例如python、javascript等')
    parser.add_argument('--output', type=str, default='github_trending.csv',
                        help='输出文件名')
    parser.add_argument('--format', type=str, default='csv',
                        choices=['csv', 'json'],
                        help='输出格式：csv或json')
    
    args = parser.parse_args()
    
    # 创建爬虫实例
    scraper = GitHubTrending()
    
    # 获取趋势项目
    print(f"正在获取GitHub {args.period} 趋势项目" + (f"（{args.language}）" if args.language else "..."))
    trending_repos = scraper.get_trending(period=args.period, language=args.language)
    
    if not trending_repos:
        print("未获取到任何数据")
        return
    
    print(f"获取到 {len(trending_repos)} 个项目")
    
    # 保存数据
    if args.format == 'csv':
        output_file = args.output if args.output.endswith('.csv') else f"{args.output}.csv"
        scraper.save_to_csv(trending_repos, output_file)
    else:
        output_file = args.output if args.output.endswith('.json') else f"{args.output}.json"
        scraper.save_to_json(trending_repos, output_file)


if __name__ == '__main__':
    main()