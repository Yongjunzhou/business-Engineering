# 新设备接入手册

**用途**：在一台新电脑上首次接入本仓库，完成克隆、双远端推送、防误推钩子与记忆加载点配置。
**适用对象**：在本机使用 Git 与 Claude Code 的操作者。
**仓库**：GitHub 侧 `Yongjunzhou/business-Engineering`，Gitee 侧 `mickeychow/business-engineering`。

本手册是[仓库维护手册](REPO-MAINTENANCE.md) §四的**可拷贝版本**：可以脱离仓库单独阅读和执行。远端拓扑的完整说明仍以维护手册为准。

---

## 〇、开工前确认

| 项目 | 要求 | 检查命令 |
|------|------|---------|
| Git | 已安装 | `git --version` |
| Node.js | 已安装（仓库工具与记忆配置需要） | `node --version` |
| 磁盘 | 至少约 300 MB | — |
| Git 身份 | 已配置用户名与邮箱 | `git config --global user.name`、`git config --global user.email` |

没有配置身份时先执行：

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱"
```

仓库体积较大（约 250 MB），首次克隆需要一些时间。

---

## 一、旧克隆处置（仅当本机已有旧仓时）

如果这台电脑上已经有旧的 `AOS` 克隆（旧仓 `AOS-system-design`），先检查并留档；没有则直接跳到 §二。

```bash
cd <旧仓库目录>
git status
git log --oneline -3
```

- 有未提交改动：先提交，或复制出来。
- 有独有提交：先推送到旧仓。
- 确认无需保留后，把旧目录改名留档：

```bash
cd ..
mv AOS AOS-旧仓档案-<日期>
```

Windows PowerShell 用：

```powershell
Rename-Item AOS AOS-旧仓档案-<日期>
```

**不要**从旧仓 `AOS-system-design` 拉取或推送；它是冻结的历史档案，与新仓是两套独立历史。

---

## 二、配置 SSH

### 2.1 生成密钥（本机没有时）

```bash
ssh-keygen -t ed25519 -C "你的邮箱"
```

一路回车即可；已有密钥则跳过。

### 2.2 把公钥加到两个平台

公钥文件：`~/.ssh/id_ed25519.pub`。Windows 下通常是 `C:\Users\<用户名>\.ssh\id_ed25519.pub`。

- GitHub：Settings → SSH and GPG keys → New SSH key
- Gitee：设置 → SSH 公钥

### 2.3 验证

```bash
ssh -T git@github.com
ssh -T git@gitee.com
```

看到 `successfully authenticated` 即成功。

> GitHub 的 `ssh -T` 在认证成功时**退出码是 1**，这是正常行为；判断标准是有没有 `successfully authenticated`。

---

## 三、克隆仓库

```bash
git clone git@github.com:Yongjunzhou/business-Engineering.git <目标目录>
cd <目标目录>
```

注意两点：

- GitHub 的规范名是 `business-Engineering`（**大写 E**），Gitee 是 `business-engineering`（小写）。
- 目标目录可以任选；记忆加载点会按本机实际路径写入，不需要沿用旧机器的目录名。

---

## 四、配置双推

克隆后 `origin` 默认只有一个推送地址。依次追加 GitHub 与 Gitee：

```bash
git remote set-url --add --push origin git@github.com:Yongjunzhou/business-Engineering.git
git remote set-url --add --push origin git@gitee.com:mickeychow/business-engineering.git

git remote add gitee git@gitee.com:mickeychow/business-engineering.git
git fetch gitee
```

验证：

```bash
git remote -v
```

应看到：

```
origin  git@github.com:Yongjunzhou/business-Engineering.git (fetch)
origin  git@github.com:Yongjunzhou/business-Engineering.git (push)
origin  git@gitee.com:mickeychow/business-engineering.git (push)
gitee   git@gitee.com:mickeychow/business-engineering.git (fetch)
gitee   git@gitee.com:mickeychow/business-engineering.git (push)
```

关键点：`origin` 一行 fetch、两行 push；如果少了一行 push，重新执行本节。

---

## 五、安装 pre-push 钩子

钩子在 `.git/hooks/` 里，**不进版本库**，克隆不会带过来。每台机器安装一次。

```bash
cat > .git/hooks/pre-push <<'EOF'
#!/bin/sh
# 阻止误推到历史归档仓（AOS-system-design）。
# 新仓为 business-Engineering；archive-github / archive-gitee 只读冻结。
remote="$1"
url="$2"

case "$url" in
  *AOS-system-design*)
    echo "拒绝推送：remote '$remote' 指向历史归档仓 $url" >&2
    echo "本项目只向 business-Engineering 推送；如需查阅归档请直接访问旧仓。" >&2
    exit 1
    ;;
esac

# 新仓只接收当前版本分支；旧历史分支与标签不得进入。
case "$url" in
  *business-[Ee]ngineering*)
    while read -r local_ref local_sha remote_ref remote_sha; do
      case "$local_ref" in
        refs/heads/archive-master|refs/tags/pre-skill-revision)
          echo "拒绝推送：$local_ref 含旧仓完整历史，不得进入新仓" >&2
          exit 1
          ;;
      esac
    done
    ;;
esac

exit 0
EOF

chmod +x .git/hooks/pre-push
```

检查语法：

```bash
sh -n .git/hooks/pre-push
```

临时撤销时删除 `.git/hooks/pre-push`。

---

## 六、配置记忆加载点（使用 Claude Code 时）

仓库记忆存放在 `.claude/memory/`，但 Claude Code 的加载点必须是**本机绝对路径**，所以这一步无法随 Git 同步，每台机器各跑一次：

```bash
node .ai-agent/tools/setup-memory.js
node .ai-agent/tools/setup-memory.js --check
```

- 脚本写入本机 `~/.claude/settings.json`，先自动备份，不改仓库内容。
- 写入后**重启会话**才生效。
- `--check` 显示已指向本机仓库即可。

---

## 七、验收

逐条执行，结果应与右列一致：

| 命令 | 期望结果 |
|------|---------|
| `git rev-parse HEAD` | 输出当前提交哈希 |
| `git ls-remote origin master` | 哈希与上一行相同 |
| `git ls-remote gitee master` | 哈希与上一行相同 |
| `git push --dry-run` | 两组 `Everything up-to-date` |
| `node .ai-agent/tools/check-projects.js` | `项目记忆校验：6 个条目全齐 ✓` |
| `node .ai-agent/tools/setup-memory.js --check` | 已指向本机仓库 |

`git push --dry-run` 若输出两组 `To ...` 而不是 `Everything up-to-date`，说明本地有未推送提交；这是正常的，执行一次 `git push` 即可。

---

## 八、日常使用

```bash
git add -A
git commit -m "修改摘要"
git push
```

`git push` 会同时推 GitHub 与 Gitee。若只有一组 `To ...` 成功，修好后重跑一次，它只补推落后的那一端。

工作约定：

- 主线工程任务：工作目录 = 仓库根或 `20-eos-engineering/`，读根 [`CLAUDE.md`](CLAUDE.md) 与 `.claude/memory/`。
- 独立项目任务：`cd <项目目录>`，读该目录的 `CLAUDE.md` 与 `claude-memory/`。
- 主线改动与各项目改动**分别 commit**，不混提。
- 开工前先读对应记忆库的 `MEMORY.md`，按索引展开相关记忆。

---

## 九、故障处理

| 现象 | 处理 |
|------|------|
| `Permission denied (publickey)` | 公钥未加到对应平台，或 `ssh-agent` 未加载；重做 §二 |
| `Repository not found` | 检查 URL 大小写与账号权限；GitHub 是 `business-Engineering` |
| `git push` 只推了一端 | `git remote -v` 检查 `origin` 是否缺一个 push 地址；重做 §四 |
| `non-fast-forward` 被拒绝 | `git pull --rebase origin master` 后再推；不要 force push |
| 钩子拒绝推送 | 检查目标 URL 与分支名；指向旧仓或旧历史引用时按设计拦截 |
| `setup-memory.js --check` 说未设置 | 运行不带 `--check` 的命令，写入后重启会话 |
| `node: command not found` | 安装 Node.js（nodejs.org），重新打开终端 |
| Windows 提示 `LF will be replaced by CRLF` | 正常现象，忽略；不要手工改行尾 |
| GitHub 提示 repository moved | 本手册已使用规范名；若仍出现，核对 URL 是否为 `business-Engineering` |

---

## 十、禁止事项

- 不使用 `git push --all`、`git push --mirror`、`git push --tags`。
- 不推送 `archive-master` 分支或 `pre-skill-revision` 标签。
- 不向 `AOS-system-design` 的两个归档远端推送。
- 不使用 force push。
- 不把 token、私钥或本机凭据写进仓库。

---

## 附：一页检查清单

- [ ] `git --version`、`node --version` 正常
- [ ] `git config --global user.name` / `user.email` 已设置
- [ ] GitHub、Gitee 的 `ssh -T` 均显示 `successfully authenticated`
- [ ] 已克隆 `business-Engineering`，并进入目标目录
- [ ] `git remote -v` 显示 `origin` 一行 fetch、两行 push，另有 `gitee`
- [ ] `.git/hooks/pre-push` 已安装且 `sh -n` 通过
- [ ] `setup-memory.js --check` 已指向本机仓库
- [ ] `git push --dry-run` 输出两组 `Everything up-to-date`
- [ ] `git ls-remote origin master` 与 `git ls-remote gitee master` 哈希一致
- [ ] `check-projects.js` 输出 6 个条目全齐
