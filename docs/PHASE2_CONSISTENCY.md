# ProxyRules 第二阶段：五客户端规则一致性保护

在当前 Go 生成器不做任何改动的前提下，增加**只读、离线、生成后**校验。

## 权威来源

- `Base/Rules/PolicyConfig.yaml`：策略组定义及顺序
- `Base/Rules/RemoteRules.yaml`：远程规则源、继承关系、分流策略及顺序

## 检查范围

1. Mihomo/Stash：策略组顺序、30 条规则 ID 与策略绑定、provider 清单及最后两条 fallback。
2. Loon：策略组顺序、30 条远程规则的策略顺序、GEOIP/FINAL fallback。
3. Surge：策略组顺序、30 条远程规则策略顺序。识别 Surge 独有内置 `RULE-SET,LAN,DIRECT`。
4. Egern：IPv6/IPv4 两份模板的策略组顺序、30 条规则文件名及策略绑定、URL 来源和最终默认规则。
5. 区别对待 `GLOBAL`（Mihomo 独有）和 `Proxies`（Surge 独有），不要求五个客户端原生语法相同。

## 执行顺序

脚本插入 PR workflow 的 `Verify generated configurations` 前和每日 workflow 的
`Check for changes` 前。任何失败都会阻断后续发布提交。

## 限制

- 检查的是生成文件中的映射、覆盖率及顺序，不验证设备实机的规则命中和运行时网络行为。
- 目前未逐条等价比较各上游规则内容，也不验证 Loon/Surge 的 URL 是否在线。
- 每次源规则扩展后，此检查依据 Base 文件自动更新预期，不需写死数量。

## 操作

```bash
git switch main
git pull --ff-only origin main
git switch -c feat/cross-client-consistency
unzip -o ~/Downloads/Archives/proxyrules_phase2_consistency.zip -d /tmp/
python3 /tmp/proxyrules_phase2/install_phase2.py

uv run --with pyyaml python scripts/test_cross_client.py
uv run --with pyyaml python scripts/validate_cross_client.py
git diff --check
git status --short
```

仅暂存本次 5 个文件，别提交 `egern_coverage.py`：

```bash
git add .github/workflows/auto_generate.yml .github/workflows/pr_validate.yml \
  scripts/validate_cross_client.py scripts/test_cross_client.py docs/PHASE2_CONSISTENCY.md
git commit -m "feat(ci): validate cross-client policy and rule consistency"
git push -u origin feat/cross-client-consistency
gh pr create --repo luluape/ProxyRules --base main --head feat/cross-client-consistency \
  --title "feat(ci): validate cross-client policy and rule consistency" \
  --body "Add offline, read-only checks for policy group coverage and ordered rule mappings across Mihomo, Stash, Loon, Surge, and Egern."
```
