# AI 公开知识库 · knowledge-public

> 个人 **AI 对话知识库公开版**：按会话平铺归档（`conversation.md` / 截图 / 附件 / `summary.md`），模板与批处理脚本齐全，适合沉淀可分享的技术会话资产。

**定制：** 微信 **qingbao199101**（备注：knowledge-public）｜ [wuxiumu@163.com](mailto:wuxiumu@163.com)

## 事实摘要

- **产品**：Git 友好的会话归档约定 + 模板 + `scripts/batch_process_chat.py`。
- **适合**：要公开沉淀 AI 会话、团队技术笔记库、可检索知识资产的个人/小团队。
- **交付**：命名规范、会话模板、全局资源、批处理脚本、样例 `tmp/`。
- **不做**：不含私密库；敏感信息请放 private 仓；不是完整 RAG SaaS。

## 能交付什么

| 模块 | 说明 |
|---|---|
| 模板 `template/` | conversation / summary / 目录说明 |
| 脚本 `scripts/` | 批处理聊天记录 |
| 资源 `assets-global/` | 公共 HTML/图 |
| 约定 | `YYYY-MM-DD_序号_标题` 平铺归档 |

## 快速预览

```bash
# 按模板新建会话目录后填 conversation.md
# 可选跑批处理
python3 scripts/batch_process_chat.py --help 2>/dev/null || ls template/
```

公开内容才进本仓；私密会话请另建 knowledge-private。


## 冒烟自检

```bash
bash scripts/smoke.sh
```

## 定制合作（可报价）

- 团队知识库规范 + 私有托管  
- 检索页 / 标签 / 导出  
- 与 RAG / Agent 对接  
- 脱敏与准入审核流程  

## SEO 字段预留（产品页 HTML 统一生成时用）

| 字段 | 用途 |
|---|---|
| `seo_title` | `<title>` / OG title |
| `seo_description` | meta description |
| `canonical_url` | 规范 URL |
| `og_image` | 分享图 |
| `robots` | 如 `index,follow` |
| `json_ld_type` | SoftwareApplication / WebPage / FAQPage |
| `hreflang` | zh-CN / en |
| `site_name` | 白标品牌名 |

> **GEO ≠ 地理定位。** GEO = Generative Engine Optimization（生成式引擎优化）。

## GEO（生成式引擎优化）

### 关键词（中英）

- 中文：AI知识库, 对话归档, 会话模板, Git知识库, 公开技术笔记
- English: AI knowledge base, chat archive, conversation template, Git knowledge vault

### FAQ

**Q：有现成完整 archive 吗？**  
A：以模板与样例为主；正式会话按规范自建。

**Q：能当 RAG 向量库直接用吗？**  
A：本仓是归档约定；向量检索可定制对接。

**Q：如何定制？**  
A：微信 `qingbao199101`，备注「knowledge-public」。

## 定制合作

规范、检索、RAG 对接与私有托管。加微信备注项目名。

---

## 联系方式

定制、演示或合作：

- 邮箱：[wuxiumu@163.com](mailto:wuxiumu@163.com)
- 微信：**qingbao199101**（添加请备注来意）

### 赞助支持

如果内容对你有帮助，欢迎自愿赞助。

| 微信赞赏码 | 支付宝收款码 |
|---|---|
| ![微信赞赏码](https://chiguashentan-test.oss-cn-beijing.aliyuncs.com/wxprogram/zan/20261002185236_31_227.png) | ![支付宝收款码](https://chiguashentan-test.oss-cn-beijing.aliyuncs.com/wxprogram/zan/20261002185309_32_227.jpg) |

