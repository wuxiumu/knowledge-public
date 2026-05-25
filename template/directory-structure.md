# 新建会话目录模板

## 快速创建脚本

### Mac/Linux

```bash
#!/bin/bash

# 用法: ./new_session.sh "会话标题"

TITLE="$1"
DATE=$(date +%Y-%m-%d)

# 查找当天最大序号
LAST_NUM=$(ls -d ${DATE}_* 2>/dev/null | grep -oP "${DATE}_\K\d+" | sort -n | tail -1)
if [ -z "$LAST_NUM" ]; then
    NEW_NUM="001"
else
    NEW_NUM=$(printf "%03d" $((10#$LAST_NUM + 1)))
fi

FOLDER_NAME="${DATE}_${NEW_NUM}_${TITLE}"

# 创建目录结构
mkdir -p "$FOLDER_NAME"/{images,files}
touch "$FOLDER_NAME/conversation.md"
touch "$FOLDER_NAME/summary.md"

echo "已创建会话目录: $FOLDER_NAME"
```

---

## 目录结构示例

```
2026-05-25_001_Java微服务线程池调优/
├── conversation.md   # 多轮对话完整记录
├── images/           # 截图、配图、流程图
├── files/            # 附件：代码、配置、文档、PDF
└── summary.md        # 个人总结、落地步骤、待办
```

---

## 命名规范

**文件夹命名格式**：
```
YYYY-MM-DD_序号_会话简短标题
```

**示例**：
- `2026-05-25_001_Java微服务线程池调优`
- `2026-05-25_002_RAG私有知识库架构设计`
- `2026-05-25_003_全栈简历求职话术优化`

**说明**：
- `YYYY-MM-DD`: 日期
- `序号`: 当天的第几个会话，三位数字，如 001, 002
- `会话简短标题`: 用下划线连接的关键词

---

## 文件说明

### conversation.md
- 主文件，记录完整的多轮对话
- 按轮次组织，方便查看上下文
- 使用模板填写

### images/
- 本次会话的所有截图、配图、流程图
- 建议在图片文件名中包含描述，如 `architecture_diagram.png`

### files/
- 附件：代码片段、配置文件、文档、PDF、脚本等
- 保持原文件名或添加前缀描述

### summary.md
- 后期整理时填写
- 总结核心收获、关键知识点
- 列出可落地的步骤和待办事项
- 可补充延伸思考和相关链接
