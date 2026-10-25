# 制作与复现

## 本地运行网页

在仓库根目录运行：

```sh
python3 -m http.server 4854
```

打开 http://localhost:4854/ 。网页无需构建。线上视频跳转建议使用支持 Range 的静态服务，例如 GitHub Pages。

## 视频流程

1. 核实 Lucian 的五种按钮，拆解观默 Bento Grid 的重排节奏。
2. 写 [分镜与出处](../film/treatment.md)，确定 2 秒开场、五段各 3 秒、3 秒总结。
3. 用 Canvas 的 `window.draw(t)` 确定性绘图，字体与脚本本地加载。
4. 输出九帧，两轮修改后用 Playwright 渲染 1,200 张 JPEG。
5. Python 合成 120 BPM 配乐与音效；FFmpeg 编码 H.264 Main、yuv420p、AAC，启用 faststart。
6. 检查抽帧、完整播放与跳转，见 [影片 QA](../film/QA.md)。

## 重新渲染

需要 Node.js、Python 3、NumPy、FFmpeg 和 Chrome：

```sh
cd film
npm install
python3 -m pip install numpy
python3 make_audio.py
node render.mjs
node render.mjs full
sh encode.sh
```

默认使用 macOS Chrome；其他路径设置 `CHROME_PATH`。影片操作由时间控制，交互网页由用户事件驱动，使用相同布局、文案和状态反馈。

## 交互实现

- `site/app.js`：指针、键盘、长按计时、取消、撤销、下载、发送和剪贴板。
- `site/style.css`：Bento 响应式布局、按钮状态、飞行动画与减少动态偏好。
- 长按使用浏览器时间计算 1.2 秒，提前松开、移出、失焦会取消。
- 下载用 2.8 秒模拟进度，完成后交给浏览器下载 `media/example-report.pdf`。本页不会把模拟进度当成真实网络进度。
- 消息只保留在当前页面，刷新后清空；没有外部消息服务。
- 复制等待 Clipboard API 成功后显示回执；失败则选中文字，提示手动复制。

## 发布

把仓库提交到 main。Settings → Pages → Deploy from a branch → main → /(root)。`.nojekyll` 保留静态目录，全部资源采用相对路径。

## 文件结构

- `index.html` / `site/`：可交互网页。
- `media/`：MP4、GIF、海报、源码 ZIP 与可下载的示例 PDF。
- `film/`：影片完整源工程。
- `docs/`：提示词与制作步骤。
