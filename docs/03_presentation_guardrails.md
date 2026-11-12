# 支柱三：组会学术 PPTX 视觉自审与双字体规范 (`group-meeting-pptx`)

## 痛点背景
使用 `python-pptx` 构建学术幻灯片时，仅靠“代码跑通”极易翻车：
- 文本框膨胀遮挡配图或溢出底边；
- 强行全局刷字体破坏封面与致谢尾页的个性化设计；
- 在数据页顶部堆砌大号“结论横幅”与 `【结论短句】`，破坏组会直观读图体验；
- 化学式与离子电荷平铺（`CO2`、`Li+`），或直接硬设冲突的图片宽高导致拉伸变形。

---

## 防御性排版与退出码 `0` 门禁规范

### 1. 交付前 COM 导出真机视觉自审
- 生成 PPTX 后，必须先运行 `verify_group_pptx.py` 静态门禁（退出码 `0`），再调用 PowerPoint COM 自动化脚本（`scripts/export_slides.ps1`）导出全量幻灯片 PNG，并**亲自逐页视觉审阅**确认零溢出、零遮挡、零重叠：
  ```bash
  .venv/Scripts/python.exe skills/group-meeting-pptx/scripts/verify_group_pptx.py --pptx deck.pptx
  powershell -ExecutionPolicy Bypass -File scripts/export_slides.ps1 -InputPptx deck.pptx -OutputDir output_pngs
  ```

### 2. 双字体分离与首尾页双重豁免（Slide 0 & Slide -1）
- **正文内容页**统一显式声明双字体 XML：`<a:latin typeface="Times New Roman"/>`（英文、数字、符号）与 `<a:ea typeface="微软雅黑"/>`（中文）；
- **双重豁免红线**：全局字体遍历后处理**必须显式豁免封面页（`s_idx == 0`）与致谢尾页（`s_idx == -1`）**，保护标题字体、英文大字与专属配色不被覆盖；
- **封面与尾页对齐规范**：封面汇报人及日期须水平严格居中（`left = (slide_width - width) / 2`, `PP_ALIGN.CENTER`）；致谢尾页保持极简居中 `THANKS!`（如 `Arial Bold 58 pt #9C1D22`）与汇报人时间，**严禁添加“敬请各位老师、师兄师姐批评指正！”**。

### 3. 去提取标签与无横幅数据页体例
- 标题、卡片与备注严禁出现 `(Figure 4a-c)`、`Fig. S2` 等内部刮削标签；正文导向统一采用观众可视屏幕方位（如“左上图 a”、“右侧图 b”），**严禁跨页引用幽灵子图**；
- 实验室组会数据页**禁用顶部 `21 pt` 结论横幅与 `【结论短句】` 括注**；右侧解读区统一使用居中加粗 `图 X：表征/测试名称` 小标题 + 精炼短事实行。

### 4. 图片原比例锁与防御性卡片
- 插图必须锁定真实像素宽高比（调用 `add_picture_fit()` 单边缩放，禁止同时硬写冲突的 `width` 与 `height`）；
- 文本容器优先使用平直纯白矩形（`MSO_SHAPE.RECTANGLE`，微灰边框 `#CFD8DC`），顶部对齐（`MSO_ANCHOR.TOP`），底部预留 `20%–30%` 呼吸留白；
- 所有化学式（$\mathrm{CO_2}$、$\mathrm{Li_3N}$）、离子电荷（$\mathrm{Li}^+$、$\mathrm{TFSI}^-$）、科学记数法（$10^{-4}$）与物理量角标（$E_{\mathrm{a}}$、$t_{\mathrm{Li}^+}$）严格上下标。
