#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理聊天记录，按知识库规范生成会话目录（按年月层级归档）

目录结构：
archive/
├── 2026/
│   ├── 05/
│   │   ├── 2026-05-25_001_标题/
│   │   └── 2026-05-25_002_标题/
│   └── 06/
│       └── 2026-06-01_001_标题/

用法: python3 batch_process_chat.py [源目录] [目标目录]
默认: python3 batch_process_chat.py knowledge-private/tmp knowledge-private/archive
"""

import os
import sys
import re
import shutil
from datetime import datetime
from pathlib import Path


def sanitize_filename(filename):
    """将文件名转换为目录名格式（中文保留，空格和特殊字符转下划线）"""
    # 去掉 .md 后缀
    name = filename.replace('.md', '')
    # 替换特殊字符为空格
    name = re.sub(r'[\/:*?"<>|]', ' ', name)
    # 多个空格替换为单个下划线
    name = re.sub(r'\s+', '_', name)
    # 去掉多余的下划线
    name = re.sub(r'_+', '_', name)
    # 去掉首尾下划线
    name = name.strip('_')
    return name


def get_date_paths(archive_path, date_str):
    """
    根据日期生成层级目录路径
    返回: (year_path, month_path, full_archive_path)
    示例: date_str='2026-05-25' 返回 ('.../2026', '.../2026/05', '.../2026/05')
    """
    year = date_str[:4]      # '2026'
    month = date_str[5:7]    # '05'
    
    year_path = os.path.join(archive_path, year)
    month_path = os.path.join(year_path, month)
    
    return year_path, month_path, month_path


def get_next_sequence(month_path, date_str):
    """获取当天下一个序号（在年月目录下查找）"""
    existing = []
    if os.path.exists(month_path):
        for item in os.listdir(month_path):
            # 检查是否是目录且以日期开头
            item_path = os.path.join(month_path, item)
            if os.path.isdir(item_path) and item.startswith(date_str):
                try:
                    # 提取序号部分 (2026-05-25_001_xxx -> 001)
                    parts = item.split('_')
                    if len(parts) >= 2 and parts[1].isdigit():
                        existing.append(int(parts[1]))
                except:
                    pass
    
    if not existing:
        return 1
    return max(existing) + 1


def extract_summary(content, max_lines=20):
    """从内容中提取摘要（前20行或前500字）"""
    lines = content.strip().split('\n')
    summary = []
    total_chars = 0
    
    for line in lines:
        if total_chars + len(line) > 500:
            break
        summary.append(line)
        total_chars += len(line)
    
    return '\n'.join(summary)


def check_duplicate_by_title(month_path, title):
    """检查是否已存在相同标题的会话目录"""
    if not os.path.exists(month_path):
        return None
    
    # 将标题转换为目录名格式
    folder_suffix = sanitize_filename(title)
    
    for item in os.listdir(month_path):
        item_path = os.path.join(month_path, item)
        if os.path.isdir(item_path):
            # 提取标题部分（去掉日期和序号）
            # 格式: 2026-05-25_001_标题
            parts = item.split('_', 2)  # 分割成 [日期, 序号, 标题]
            if len(parts) >= 3:
                existing_title = parts[2]
                if existing_title == folder_suffix:
                    return item
    
    return None


def process_single_file(src_file, month_path, date_str, seq_num, skip_duplicate=True):
    """处理单个聊天记录文件"""
    filename = os.path.basename(src_file)
    
    # 读取内容
    try:
        with open(src_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ 读取失败: {filename} - {e}")
        return False
    
    # 生成标题和目录名
    title = filename.replace('.md', '')
    folder_suffix = sanitize_filename(title)
    
    # 检查是否已存在相同标题（去重）
    if skip_duplicate:
        existing = check_duplicate_by_title(month_path, title)
        if existing:
            print(f"⚠️  检测到重复，跳过: {title} (已存在: {existing})")
            return False
    
    # 构建目录名: YYYY-MM-DD_序号_标题
    seq_str = f"{seq_num:03d}"
    folder_name = f"{date_str}_{seq_str}_{folder_suffix}"
    folder_path = os.path.join(month_path, folder_name)
    
    # 检查目录是否已存在（兜底）
    if os.path.exists(folder_path):
        print(f"⚠️  目录已存在，跳过: {folder_name}")
        return False
    
    # 创建目录结构
    try:
        os.makedirs(folder_path)
        os.makedirs(os.path.join(folder_path, 'images'))
        os.makedirs(os.path.join(folder_path, 'files'))
    except Exception as e:
        print(f"❌ 创建目录失败: {folder_name} - {e}")
        return False
    
    # 创建 conversation.md
    conversation_content = f"""# 会话主题：{title}

**会话时间**：{date_str}

**来源文件**：{filename}

---

## 会话背景

从文件导入的聊天记录，原始内容如下：

---

## 对话内容

{content}

---

## 总结与收获

*待补充...*

- 关键知识点：
- 可落地的步骤：
- 待办事项：
"""
    
    try:
        with open(os.path.join(folder_path, 'conversation.md'), 'w', encoding='utf-8') as f:
            f.write(conversation_content)
    except Exception as e:
        print(f"❌ 写入 conversation.md 失败: {folder_name} - {e}")
        return False
    
    # 创建 summary.md
    summary_preview = extract_summary(content)
    summary_content = f"""# 会话总结

**会话主题**：{title}

**会话时间**：{date_str}

---

## 核心收获

### 1. 关键知识点

- 知识点 1：
- 知识点 2：
- 知识点 3：

### 2. 可落地的步骤

1. 步骤一
2. 步骤二
3. 步骤三

---

## 内容预览

```markdown
{summary_preview}
```

---

## 待办事项

- [ ] 阅读并理解内容
- [ ] 提取关键知识点
- [ ] 制定落地计划

---

## 延伸思考

- 相关问题：
- 需要深入研究的方向：

---

## 相关链接

- 原始文件：{filename}
- 完整对话：conversation.md
"""
    
    try:
        with open(os.path.join(folder_path, 'summary.md'), 'w', encoding='utf-8') as f:
            f.write(summary_content)
    except Exception as e:
        print(f"❌ 写入 summary.md 失败: {folder_name} - {e}")
        return False
    
    # 可选：将原文件复制到 files 目录备份
    try:
        shutil.copy2(src_file, os.path.join(folder_path, 'files', filename))
    except Exception as e:
        print(f"⚠️  备份原文件失败: {filename} - {e}")
    
    print(f"✅ 已创建: {folder_name}")
    return True


def main():
    # 获取源目录和目标目录
    if len(sys.argv) >= 2:
        src_dir = sys.argv[1]
    else:
        src_dir = 'knowledge-private/tmp'
    
    if len(sys.argv) >= 3:
        archive_dir = sys.argv[2]
    else:
        archive_dir = 'knowledge-private/archive'
    
    # 判断是否为绝对路径
    if os.path.isabs(src_dir):
        src_path = src_dir
    else:
        # 相对路径，基于脚本所在目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        src_path = os.path.join(script_dir, src_dir)
    
    if os.path.isabs(archive_dir):
        archive_path = archive_dir
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        archive_path = os.path.join(script_dir, archive_dir)
    
    # 检查源目录
    if not os.path.exists(src_path):
        print(f"❌ 源目录不存在: {src_path}")
        print(f"提示：请将聊天记录文件放入 {src_dir} 目录")
        return 1
    
    # 确保目标目录存在
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)
        print(f"📁 创建目标目录: {archive_path}")
    
    # 获取所有 .md 文件
    md_files = [f for f in os.listdir(src_path) if f.endswith('.md')]
    
    if not md_files:
        print(f"⚠️  {src_dir} 目录下没有找到 .md 文件")
        return 0
    
    print(f"\n🚀 开始批量处理 {len(md_files)} 个聊天记录文件...")
    print(f"源目录: {src_path}")
    print(f"目标目录: {archive_path}")
    print(f"归档格式: archive/年/月/日期_序号_标题/\n")
    
    # 获取今天的日期
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 获取年月目录路径
    year_path, month_path, target_path = get_date_paths(archive_path, today)
    
    # 创建年月目录
    if not os.path.exists(year_path):
        os.makedirs(year_path)
        print(f"📁 创建年份目录: {year_path}")
    
    if not os.path.exists(month_path):
        os.makedirs(month_path)
        print(f"📁 创建月份目录: {month_path}")
    
    # 获取起始序号（在月份目录下）
    start_seq = get_next_sequence(month_path, today)
    print(f"📅 日期: {today}, 起始序号: {start_seq:03d}\n")
    
    # 处理每个文件
    success_count = 0
    skip_count = 0
    for i, filename in enumerate(md_files, start=start_seq):
        src_file = os.path.join(src_path, filename)
        result = process_single_file(src_file, month_path, today, i, skip_duplicate=True)
        if result:
            success_count += 1
        else:
            skip_count += 1
    
    print(f"\n✅ 完成！成功处理 {success_count}/{len(md_files)} 个文件")
    if skip_count > 0:
        print(f"⏭️  跳过 {skip_count} 个重复文件")
    print(f"📂 请查看: {target_path}\n")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
