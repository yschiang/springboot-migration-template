# cline-springboot-migration-demo

適用於 **Spring Boot 2 升級至 3 的程式碼審查** Cline skills + rules 工具包。

將此 repo 作為 Cline 的 context，指向目標 repo，即可獲得包含 Critical/Warn/Suggestion 問題、優先修復計畫與驗證指令的結構化審查報告 — 分兩步驟執行。

---

## 快速開始

現成的 Cline copy-paste prompt 位於：

```
docs/example-prompts/springboot-2-to-3-review-and-fix.md
```

將標有 `<- change this` 的欄位（分支名稱、建構工具）替換為你的專案資訊後，貼入 Cline 即可使用。

Prompt 分兩個受控步驟執行：
1. **Review（審查）** — AI 讀取目標 repo，產出報告後停止等待確認
2. **Fix（修復）** — 確認報告後，AI 依區域分別 commit 修復內容

---

## 專案結構

```
cline-springboot-migration-demo/
├── ai/
│   ├── clinerules/          # 行為規則 — 每次執行皆套用
│   │   ├── 02_evidence_first.md
│   │   ├── 03_severity.md
│   │   ├── 04_no_fluff.md
│   │   ├── 06_spring_migration_focus.md
│   │   ├── coding-style.md
│   │   └── security.md
│   │
│   ├── knowledge/           # AI 審查時參閱的知識庫
│   │   ├── spring-boot-3.0-migration-guide.md   [P0 — 權威來源]
│   │   ├── baeldung-spring-boot-3-migration.md  [P1 — 補充參考]
│   │   ├── severity_rubric.md                   [嚴重性定義]
│   │   └── examples.md                          [好壞程式範例，選用]
│   │
│   ├── skills/
│   │   ├── springboot_reviewer/          # 通用程式碼審查基準
│   │   │   └── SKILL.md                  #   入口點 — 正確性、安全性、可靠性
│   │   │
│   │   ├── springboot_engineer/          # 通用 Spring Boot 工程師
│   │   │   ├── SKILL.md                  #   入口點 — 角色、限制、工作流程
│   │   │   └── references/              #   按需載入
│   │   │       ├── web.md
│   │   │       ├── data.md
│   │   │       ├── security.md
│   │   │       ├── cloud.md
│   │   │       └── testing.md
│   │   │
│   │   └── springboot_migration/         # SB2→3 遷移（審查 + 修復 + 檢查清單）
│   │       ├── SKILL.md                  #   工程師入口 — 修復模式、修復順序
│   │       ├── reviewer.md               #   審查入口 — 合併通用 + 遷移檢查
│   │       └── checks.md                 #   遷移專項 7 步驟檢查清單
│   │
│   └── templates/
│       └── review_report_template.md            # 輸出格式（所有 skill 共用）
│
├── docs/
│   ├── USAGE_IN_CLINE.md    # Cline 設定說明
│   └── example-prompts/
│       └── springboot-2-to-3-review-and-fix.md  # 可直接貼入 Cline 的 prompt
├── examples/
│   └── example_review_report.md   # 範例輸出報告
└── README.md
```

---

## Skills

### 選擇哪個 Skill

| 目標 | Skill |
|---|---|
| 通用程式碼品質審查（任何專案） | `springboot_reviewer/SKILL.md` |
| Spring Boot 2→3 遷移審查（推薦） | `springboot_migration/reviewer.md` |
| 套用 SB2→3 遷移修復 | `springboot_migration/SKILL.md` |
| 通用 Spring Boot 開發 | `springboot_engineer/SKILL.md` |

完整 skill 架構說明請參閱 `ai/README.md`。

### Skill 組合方式

`springboot_migration/reviewer.md` 組合了：
- `springboot_reviewer/SKILL.md` — 正確性、安全性、可觀測性、建構可靠性
- `springboot_migration/checks.md` — Java 17、Jakarta、Security 6、HttpClient 5、Batch、設定屬性

兩個 skill 的問題會合併：重複問題合為一條，嚴重性取較高者。

---

## 程式碼審查流程

遷移 skill 依以下順序（ROI 由高至低）檢查目標 repo：

| 步驟 | 檢查內容 | 預設嚴重性 |
|---|---|---|
| 1 | Spring Boot 版本 — 若 < 2.7.x，標記需兩步升級 | Warn / Critical |
| 2 | Java 工具鏈 — `maven-compiler-plugin`、parent POM、Gradle `sourceCompatibility` | < 17 則 Critical |
| 3 | 相依性阻礙 — `javax.*` 套件、`httpclient` 4.x、Security < 5.8、Hibernate group ID | Critical |
| 4 | 程式碼模式 — `javax.`、`org.apache.http.`、`WebSecurityConfigurerAdapter`、`antMatchers`、`@EnableBatchProcessing` | Critical / Warn |
| 5 | 設定屬性重新命名 — `spring.redis`、`spring.data.cassandra`、已移除的 JPA/SAML2 屬性 | Warn / Critical |
| 6 | Spring Batch — `@EnableBatchProcessing` 使用、多個 Job bean | Warn |
| 7 | 打包 / 執行環境 — WAR 部署於外部容器、Actuator、Security 影響 | Warn / Critical |

---

## 規則

`ai/clinerules/` 下的所有規則每次皆套用：

| 檔案 | 強制內容 |
|---|---|
| `02_evidence_first` | 每個問題必須引用檔案路徑與程式碼片段 |
| `03_severity` | Critical = 確定中斷 · Warn = 可能中斷 · Suggestion = 品質改善 |
| `04_no_fluff` | 建議必須具體可執行且針對該 repo — 不接受泛泛而談 |
| `06_spring_migration_focus` | 必須檢查全部 6 個 Spring 專項；若不適用需標記 N/A 並說明原因 |
| `coding-style` | 程式碼風格慣例與格式化規則 |
| `security` | 安全性相關行為約束 |

---

## 知識庫

| 檔案 | 優先級 | 用途 |
|---|---|---|
| `spring-boot-3.0-migration-guide.md` | **P0 — 權威來源** | 官方 Spring 遷移指南；衝突時優先採用 |
| `baeldung-spring-boot-3-migration.md` | P1 — 補充參考 | 實用範例、HttpClient 5.x 遷移細節 |
| `severity_rubric.md` | 參考 | 詳細嚴重性定義 |
| `examples.md` | 選用 | 好壞程式範例；撰寫修復片段時參閱 |

### P0 與 P1 已知衝突

| 主題 | P0（採用此版本） | P1（忽略） |
|---|---|---|
| JPA 屬性名稱 | `spring.jpa.hibernate.use-new-id-generator-mappings` | `spring.jpa.hibernate.use-new-id-generator`（缺少 `-mappings`） |
| Trailing slash | 預設值改為 `false`，仍可設定 | 描述為「已棄用」（不精確） |

---

## 報告格式

每次審查產出一份 Markdown 檔案，依照 `ai/templates/review_report_template.md`：

```
# Review Report — <repo>

## Overview          <- repo 基本資訊表 + GO / GO-with-fixes / NO-GO
## Summary           <- 計數表：Critical | Warning | Suggestion
## Findings
   ### Critical      <- [CRITICAL] ID — 標題
   ### Warning       <- [WARN] ID — 標題        每條問題包含：
   ### Suggestion    <- [SUGGESTION] ID — 標題    位置 · 證據 · 原因 · 修復方式 · 行動項目
## Strengths         <- 做得好的地方
## Priority Plan     <- P0 / P1 / P2 表格（含檔案與預估工時）
## Verification Checklist  <- 建構 · 測試 · 驗煙指令
## Assumptions / Open Questions
```

輸出檔名：`review-report-<repo-name>-<YYYYMMDD>.md`，儲存至專案根目錄。

完整範例報告請參閱 `examples/example_review_report.md`。

---

## 嚴重性參考

| 等級 | 意義 | 行動 |
|---|---|---|
| **Critical** | 確定造成建構或執行期中斷 | 合併前必須修復 |
| **Warn** | 可能中斷或行為變更，需驗證 | 盡快修復 |
| **Suggestion** | 程式碼品質改善 | 排入 Backlog / 建議採納 |

若在兩個等級之間猶豫，選擇較高者並說明理由。

---

## 客製化

此 repo 不含任何私有程式碼，可直接 fork 後調整：
- 在 `ai/clinerules/` 新增符合組織規範的規則
- 在 `ai/knowledge/` 新增知識文件，並在 skill 的 Knowledge Base 章節中登錄
- 在 `ai/knowledge/severity_rubric.md` 調整嚴重性閾值
- 在 `ai/templates/review_report_template.md` 擴充報告格式
