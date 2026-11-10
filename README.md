# 唐缝梁 · 学术主页 / Fengliang Tang

- 中文 https://tylerchn.github.io/
- English https://tylerchn.github.io/en/

## 内容维护 / Editing content

- 在 `data/publications.json` 中维护题名、年份、完整作者、期刊、作者角色与链接。`featured` 为代表作排序，`0` 表示不在代表作中展示。
- 在 `scripts/build.py` 中更新中英文简介、研究方向、教育、项目与联系方式。
- 更新内容后，从仓库根目录运行 `python scripts/build.py`，将生成的 `index.html` 和 `en/index.html` 一并提交。
- 样式在 `style.css`。`main.js` 保留旧版英文链接的跳转。
- 公开版简历为 `assets/fengliang-tang-cv.pdf`，可用新 PDF 替换。
- 本地预览可运行 `python -m http.server 8000`。
