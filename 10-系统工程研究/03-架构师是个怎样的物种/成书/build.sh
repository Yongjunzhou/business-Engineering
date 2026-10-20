#!/usr/bin/env bash
# build.sh — 《架构师是个怎样的物种？》成书构建单入口
#
# 用法：
#   bash build.sh                 全书：架构师-打印版.pdf + 架构师-电子版.epub
#   bash build.sh --no-front      赠阅版：去《序言》与《致谢》→ 架构师成长之路.pdf / .epub
#   bash build.sh --tblimg        另出「表格转图版」EPUB（不认 table 的阅读器用）
#   bash build.sh --rerender      强制重渲全部 mermaid 图（默认图在库则跳过）
#   可组合：bash build.sh --no-front --tblimg
#
# ★ 2026-10-20：加 --no-front／--tblimg 两开关，并把「表格转图版」收进本脚本
#   （此前是支线：build.sh 不建它，产物容易跟不上正文改动）。
set -euo pipefail
cd "$(dirname "$0")"

RERENDER=0
TBLIMG=0
EDITION=full
for a in "$@"; do
  case "$a" in
    --rerender) RERENDER=1 ;;
    --no-front) EDITION=colleague ;;
    --tblimg)   TBLIMG=1 ;;
    -h|--help)  sed -n '2,12p' "$0"; exit 0 ;;
    *) echo "未知参数：$a（可用：--no-front / --tblimg / --rerender）"; exit 2 ;;
  esac
done

# 产物命名：全书沿用旧名；赠阅版统一为《架构师成长之路》（2026-10-20 用户定）
if [ "$EDITION" = "colleague" ]; then
  FRONT=0
  PDF="架构师成长之路.pdf"
  EPUB="架构师成长之路.epub"
  TBEPUB="架构师成长之路-表格转图.epub"
else
  FRONT=1
  PDF="架构师-打印版.pdf"
  EPUB="架构师-电子版.epub"
  TBEPUB="架构师-电子版-表格转图.epub"
fi

# 工具链 PATH（pandoc/typst 由 winget 安装，非系统 PATH）
export PATH="/c/Users/HUAWEI/AppData/Local/Pandoc:/c/Users/HUAWEI/AppData/Local/Microsoft/WinGet/Packages/Typst.Typst_Microsoft.Winget.Source_8wekyb3d8bbwe/typst-x86_64-pc-windows-msvc:$PATH"
# 图1-5 蛇形渲染依赖 puppeteer-core（随 mmdc 下载在 npx 缓存里）
# 注：find 目标为 Windows 专有路径；在非 Windows 上 find 会返回非 0，pipefail 下触发 set -e 退出——
# 加 `|| true` 使跨平台安全（Windows 路径存在时正常、不存在时无害跳过）。
PPC="$(find /c/Users/HUAWEI/AppData/Local/npm-cache/_npx "$HOME/.npm/_npx" -maxdepth 4 -type d -name puppeteer-core 2>/dev/null | head -1 || true)"
if [ -n "$PPC" ]; then
  export NODE_PATH="$(dirname "$PPC")${NODE_PATH:+:$NODE_PATH}"
fi

OUT=build
mkdir -p "$OUT/.mmd" "$OUT/figs" "$OUT/assets"

echo "[1/8] 预处理（版次=$EDITION / 剔版本记录 / mermaid 提取 / .unlisted 归一化）"
BOOK_EDITION="$EDITION" node "$OUT/preprocess.mjs" .. "$OUT"

echo "[2/8] mermaid → PNG"
# 浏览器可执行文件：按平台探测，写一份本机配置（不进 git）；探不到则用库内那份（Windows 机上的路径）
PCFG="$OUT/puppeteer.json"
if [ -z "${CHROME_PATH:-}" ]; then
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "$HOME"/.cache/puppeteer/chrome/*/chrome-mac-arm64/"Google Chrome for Testing.app"/Contents/MacOS/"Google Chrome for Testing" \
    "$HOME"/.cache/puppeteer/chrome/*/chrome-mac-x64/"Google Chrome for Testing.app"/Contents/MacOS/"Google Chrome for Testing" \
    "/usr/bin/google-chrome" "/usr/bin/chromium" "/usr/bin/chromium-browser" \
    "/c/Users/HUAWEI/.cache/puppeteer/chrome/"*"/chrome-win64/chrome.exe" ; do
    if [ -x "$c" ]; then export CHROME_PATH="$c"; break; fi
  done
fi
if [ -n "${CHROME_PATH:-}" ] && [ "$CHROME_PATH" != "$(sed -n 's/.*"executablePath": "\(.*\)",/\1/p' "$OUT/puppeteer.json" 2>/dev/null)" ]; then
  printf '{\n  "executablePath": "%s",\n  "args": ["--no-sandbox", "--disable-gpu"]\n}\n' "$CHROME_PATH" > "$OUT/.puppeteer.local.json"
  PCFG="$OUT/.puppeteer.local.json"
  echo "  浏览器：$CHROME_PATH"
fi
if [ "$RERENDER" = "1" ] || [ -z "$(ls "$OUT/figs"/*.png 2>/dev/null)" ]; then
  for mmd in "$OUT"/.mmd/ch*.mmd; do
    base=$(basename "$mmd" .mmd)
    npx -y @mermaid-js/mermaid-cli@11.16 -i "$mmd" -o "$OUT/figs/$base.png" -b white -s 3 -p "$PCFG" -c "$OUT/mermaid.json"
  done
else
  echo "  图已存在（重渲请加 --rerender）"
fi

echo "[2.5/8] 图1-5 蛇形渲染（mermaid 子图方向失效 → 手绘 SVG 直渲）"
if [ "$RERENDER" = "1" ] || [ ! -f "$OUT/figs/ch01-fig05.png" ]; then
  node "$OUT/render-fig05-snake.cjs"
else
  echo "  图1-5 蛇形 PNG 已存在"
fi

echo "[3/8] 封面裁剪（书脊 60px → 前封 800×1132）"
if [ ! -f "$OUT/assets/cover-800x1132.png" ]; then
  powershell -ExecutionPolicy Bypass -File "$OUT/crop-cover.ps1" "../封面/封面-前封书脊.png" "$OUT/assets/cover-800x1132.png"
fi

echo "[4/8] 逐章 pandoc → typst + fix-typ（剥 label / 注入图宽）"
while IFS= read -r base; do
  pandoc -f markdown-smart -t typst "$OUT/$base.book.md" -o "$OUT/$base.typ"
done < "$OUT/manifest.txt"
node "$OUT/fix-typ.mjs" "$OUT"

echo "[5/8] typst compile → $PDF"
typst compile main.typ "$PDF" --input "front=$FRONT"

echo "[6/8] pandoc → $EPUB"
args=(); while IFS= read -r base; do args+=("$OUT/$base.book.md"); done < "$OUT/manifest.txt"
# ★ 2026-10-19：--include-in-header 把表格样式内嵌进每个 xhtml 的 head——
# 有些阅读器不加载外链 CSS，表格会退化成"只有文字没有框"（用户报）
pandoc -f markdown-smart -t epub3 "${args[@]}" \
  --metadata-file="$OUT/metadata.yaml" \
  --toc --toc-depth=3 --split-level=1 \
  --epub-cover-image="$OUT/assets/cover-800x1132.png" \
  --css="$OUT/assets/book.css" \
  --include-in-header="$OUT/table-inline.html" \
  --resource-path="$OUT" \
  -o "$EPUB"

if [ "$TBLIMG" = "1" ]; then
  echo "[7/8] 表格转图版 EPUB（表渲染成 PNG：给 WPS／FBReader 这类不认 table 的阅读器）"
  TBDIR="$OUT-tblimg"
  node "$OUT/make-table-images.mjs" .. "$OUT" "$TBDIR"
  # pandoc 的 --resource-path 分隔符随平台：Windows 用「;」，POSIX 用「:」
  case "$(uname -s)" in MINGW*|MSYS*|CYGWIN*) SEP=';' ;; *) SEP=':' ;; esac
  targs=(); while IFS= read -r base; do targs+=("$TBDIR/$base.book.md"); done < "$TBDIR/manifest.txt"
  pandoc -f markdown-smart -t epub3 "${targs[@]}" \
    --metadata-file="$OUT/metadata.yaml" \
    --toc --toc-depth=3 --split-level=1 \
    --epub-cover-image="$OUT/assets/cover-800x1132.png" \
    --css="$OUT/assets/book.css" \
    --include-in-header="$OUT/table-inline.html" \
    --resource-path="$TBDIR$SEP$OUT" \
    -o "$TBEPUB"
else
  echo "[7/8] 跳过表格转图版（加 --tblimg 出）"
fi

echo "[8/8] EPUB 出厂体检（每个 xhtml 能否被 XML 解析）"
# 这一步是 Apple Books 那笔账换来的：XHTML 按 XML 解析，table-inline.html 注释里
# 一个裸尖括号就让全书 26 个文件崩、而浏览器毫无反应。故每次出书都拿解析器过一遍。
if command -v python3 >/dev/null 2>&1; then
  # Windows 控制台默认 GBK：Python 打印「✓」与中文文件名会抛 UnicodeEncodeError，
  # 把"全过"误报成"不过"（2026-10-20 遇到）。check-epub.py 自己也 reconfigure 了，这里是双保险。
  export PYTHONIOENCODING=utf-8
  python3 "$OUT/check-epub.py" "$EPUB" || {
    echo "  ✗ EPUB 体检不过：优先查 build/table-inline.html 里有没有裸尖括号"
    exit 1
  }
  if [ -f "$TBEPUB" ] && [ "$TBLIMG" = "1" ]; then
    python3 "$OUT/check-epub.py" "$TBEPUB" || exit 1
  fi
else
  echo "  跳过：本机无 python3；若 Apple Books 报 XML 错误，先用 python3 跑 $OUT/check-epub.py"
fi

echo "════════ 完成（版次 $EDITION）════════"
ls -la "$PDF" "$EPUB"
[ -f "$TBEPUB" ] && ls -la "$TBEPUB" || true
