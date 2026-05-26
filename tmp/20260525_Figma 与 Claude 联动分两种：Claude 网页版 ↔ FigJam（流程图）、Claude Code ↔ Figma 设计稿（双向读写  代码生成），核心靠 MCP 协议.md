Figma 与 Claude 联动分两种：**Claude 网页版 ↔ FigJam（流程图）**、**Claude Code ↔ Figma 设计稿（双向读写/代码生成）**，核心靠 **MCP 协议**。

---

### 一、Claude 网页版 × FigJam（快速出图）
适合：用自然语言生成流程图、脑图、甘特图。
1. 打开 claude.ai → Settings → Connectors → Browse connectors → 搜索 **Figma Connector** → Connect。

2. 授权 Figma 账号（权限选 files:read/write、comments:read）。
3. 聊天输入：
   ```
   帮我画一个用户注册流程图，包含手机号验证、短信验证码、密码设置、成功页
   ```
4. Claude 生成预览 → 点 **Open in FigJam** 直接打开编辑。

---

### 二、Claude Code × Figma（深度双向联动，推荐）
适合：**设计转代码、代码转设计、AI 直接改图**。
#### 1. 准备
- 安装 Claude Code：`npm install -g @anthropic-ai/claude-code`
- Figma 账号生成 **Personal Access Token**（权限：files:read/write、comments:read）
- 安装 Figma MCP 插件（Figma 桌面版）：
  - Plugins → Development → Import plugin from manifest → 选插件 `manifest.json`

#### 2. 连接 MCP（核心）
```bash
# 配置 Figma MCP（远程官方版，免费额度够用）
claude mcp add figma https://mcp.figma.com
# 或用本地插件版
claude mcp add figma http://localhost:3055
# 验证
claude mcp list
```


#### 3. 常用场景
##### 场景A：Figma 设计 → 代码（React/Vue/HTML）
```
请读取这个 Figma 文件 [粘贴链接]，把首页框架转成 React + Tailwind 组件，保留组件结构和样式变量
```
Claude 自动解析图层、组件、样式，生成像素级代码。

##### 场景B：Claude 生成代码 → Figma 可编辑设计（Code to Canvas）
```
用 React + Tailwind 做一个登录页，包含邮箱/密码输入、登录按钮、忘记密码链接
```
生成后输入：
```
把这个 UI 导出到我的 Figma 文件 [粘贴链接]，生成可编辑图层
```
Claude 调用 MCP 把代码转成 Figma 原生图层（非截图）。

##### 场景C：AI 直接改 Figma 设计
```
打开 Figma 文件 [链接]，把登录按钮颜色改成 #165DFF，字号 14px，圆角 8px
```
Claude 直接操作 Figma 画布，实时生效。

---

### 三、常见问题
- 权限报错：检查 Figma Token 权限（必须 files:read/write）。
- MCP 连接失败：重启 Figma 插件、Claude Code，或换远程 MCP（`https://mcp.figma.com`）。
- 代码生成不准：提示词加“**保留组件结构、自动布局、样式变量**”。

---

### 四、推荐组合
- 快速流程图：**Claude 网页版 + FigJam Connector**
- 设计开发一体化：**Claude Code + Figma MCP（远程）**

要不要我给你一份可直接复制的**提示词模板**，分别用于 FigJam 绘图、设计转代码、代码转设计和 AI 直接改图？