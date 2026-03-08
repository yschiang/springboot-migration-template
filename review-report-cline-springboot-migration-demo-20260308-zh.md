# Review Report — cline-springboot-migration-demo

## Table of Contents
- [Overview](#overview)
- [Findings](#findings)
  - [Critical](#critical)
  - [Warning](#warning)
  - [Suggestion](#suggestion)
- [Strengths](#strengths)
- [Priority Plan](#priority-plan)
- [Verification Checklist](#verification-checklist)
- [Assumptions / Open Questions](#assumptions--open-questions)

---

## Overview

| Field | Value |
|---|---|
| **Repo** | `/Users/johnson.chiang/Downloads/cline-springboot-migration-demo` |
| **Commit / Branch** | `1552a1bda0905ebf02593171f11a0a68743da542` |
| **Build** | `Maven` |
| **Boot Version** | `2.7.18` |
| **Java Target** | `11` (`pom.xml`) |
| **Web** | `Servlet` |
| **Reviewed** | `2026-03-08 07:49` → `07:57` (`8` min) |
| **Files Scanned** | `30` (`27` Java, `2` config, `1` build) |
| **Recommendation** | **`NO-GO`** |

### Summary

| Severity | Count | Description |
|---|---:|---|
| Critical | `14` | 必須先修復，否則 SB3 升級不可行 |
| Warning | `8` | 高機率行為差異或需同步調整 |
| Suggestion | `1` | 可提升遷移安全性與驗證效率 |
| **Total** | **`23`** | — |

---

## Findings

### Critical

#### [CRITICAL][MIGRATION] C1 — Java 目標版本仍為 11（SB3 需要 17+）

**Where**
- `pom.xml` (`<java.version>11</java.version>`)

**Evidence**
```xml
<properties>
  <java.version>11</java.version>
</properties>
```

**Why it’s a problem**
- Spring Boot 3 + Spring Framework 6 最低要求 Java 17，現況會在編譯/執行期直接阻塞。

**Recommended fix**
- 先升級 toolchain/JDK 到 17，再進行依賴與 API 遷移。

---

#### [CRITICAL][MIGRATION] C2 — `javax.persistence.*` 仍存在（需遷移 `jakarta.persistence.*`）

**Where**
- `src/main/java/org/springframework/samples/petclinic/model/BaseEntity.java`
- `src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java`
- `src/main/java/org/springframework/samples/petclinic/model/Person.java`
- `src/main/java/org/springframework/samples/petclinic/owner/Owner.java`
- `src/main/java/org/springframework/samples/petclinic/owner/Pet.java`
- `src/main/java/org/springframework/samples/petclinic/owner/PetType.java`
- `src/main/java/org/springframework/samples/petclinic/owner/Visit.java`
- `src/main/java/org/springframework/samples/petclinic/vet/Specialty.java`
- `src/main/java/org/springframework/samples/petclinic/vet/Vet.java`

**Evidence**
```java
import javax.persistence.Entity;
import javax.persistence.Table;
```

**Why it’s a problem**
- SB3/Jakarta EE 10 下 `javax.persistence` 不再是正確命名空間，編譯與執行都會失敗。

**Recommended fix**
- 全量改為 `jakarta.persistence.*`，並與 Hibernate 6/BOM 對齊。

---

#### [CRITICAL][MIGRATION] C3 — `javax.validation.*` 仍存在（需遷移 `jakarta.validation.*`）

**Where**
- `src/main/java/org/springframework/samples/petclinic/model/NamedEntity.java`
- `src/main/java/org/springframework/samples/petclinic/model/Person.java`
- `src/main/java/org/springframework/samples/petclinic/owner/Owner.java`
- `src/main/java/org/springframework/samples/petclinic/owner/Visit.java`
- `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`
- `src/main/java/org/springframework/samples/petclinic/owner/PetController.java`
- `src/main/java/org/springframework/samples/petclinic/owner/VisitController.java`

**Evidence**
```java
import javax.validation.Valid;
import javax.validation.constraints.NotBlank;
```

**Why it’s a problem**
- Bean Validation API 已切到 Jakarta，`javax.validation` 在 SB3 不相容。

**Recommended fix**
- 改為 `jakarta.validation.*`，並驗證 Controller 參數驗證流程。

---

#### [CRITICAL][MIGRATION] C4 — JAXB 仍使用 `javax.xml.bind` 與舊座標

**Where**
- `pom.xml` (`javax.xml.bind:jaxb-api`)
- `src/main/java/org/springframework/samples/petclinic/vet/Vet.java`
- `src/main/java/org/springframework/samples/petclinic/vet/Vets.java`

**Evidence**
```xml
<groupId>javax.xml.bind</groupId>
<artifactId>jaxb-api</artifactId>
```
```java
import javax.xml.bind.annotation.XmlElement;
```

**Why it’s a problem**
- JAXB 在 SB3 需使用 Jakarta 套件與座標；舊 `javax.*` 會造成類別不相容。

**Recommended fix**
- 依賴改為 `jakarta.xml.bind:jakarta.xml.bind-api`，程式碼改 `jakarta.xml.bind.annotation.*`。

---

#### [CRITICAL][MIGRATION] C5 — `javax.annotation.PostConstruct` 未遷移

**Where**
- `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`

**Evidence**
```java
import javax.annotation.PostConstruct;
```

**Why it’s a problem**
- 生命週期註解在 Jakarta 版為 `jakarta.annotation`。

**Recommended fix**
- 替換為 `jakarta.annotation.PostConstruct`。

---

#### [CRITICAL][MIGRATION] C6 — Security 6 移除 `WebSecurityConfigurerAdapter`

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/SecurityConfig.java`

**Evidence**
```java
public class SecurityConfig extends WebSecurityConfigurerAdapter {
```

**Why it’s a problem**
- Spring Security 6 已移除此 API，升級後將無法編譯。

**Recommended fix**
- 改為宣告 `SecurityFilterChain` bean + lambda DSL。

---

#### [CRITICAL][MIGRATION] C7 — `antMatchers()` 已移除

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/SecurityConfig.java`

**Evidence**
```java
.antMatchers("/", "/owners/find", "/owners/", "/vets/", "/vets.html").permitAll()
```

**Why it’s a problem**
- Security 6 僅支援 `requestMatchers()`，舊 API 在升級後直接失效。

**Recommended fix**
- 將 `authorizeRequests()/antMatchers()` 改為 `authorizeHttpRequests()/requestMatchers()`。

---

#### [CRITICAL][MIGRATION] C8 — Trailing slash 路由/安全規則在 SB3 預設會破壞匹配

**Where**
- `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java` (`@GetMapping("/owners/")`)
- `src/main/java/org/springframework/samples/petclinic/vet/VetController.java` (`@GetMapping({ "/vets", "/vets/" })`)
- `src/main/java/org/springframework/samples/petclinic/config/SecurityConfig.java` (`"/owners/", "/vets/"`)

**Evidence**
```java
@GetMapping("/owners/")
```
```java
.antMatchers("/", "/owners/find", "/owners/", "/vets/", "/vets.html").permitAll()
```

**Why it’s a problem**
- SB3 預設 `trailing slash match=false`，`/foo/` 與 `/foo` 不再等價，會導致 404 或保護規則失效。

**Recommended fix**
- 全面統一路徑（不帶尾斜線），並更新 security matcher 規則。

---

#### [CRITICAL][MIGRATION] C9 — Apache HttpClient 4.x 依賴與程式碼仍在

**Where**
- `pom.xml` (`org.apache.httpcomponents:httpclient`)
- `src/main/java/org/springframework/samples/petclinic/config/RestTemplateConfig.java`

**Evidence**
```xml
<groupId>org.apache.httpcomponents</groupId>
<artifactId>httpclient</artifactId>
```
```java
import org.apache.http.impl.client.CloseableHttpClient;
requestFactory.setConnectTimeout(30000);
requestFactory.setReadTimeout(30000);
```

**Why it’s a problem**
- SB3/SF6 需 HttpClient 5（`org.apache.hc.*`），舊命名空間與 timeout 設定方式不相容。

**Recommended fix**
- 換成 `org.apache.httpcomponents.client5:httpclient5`，並改用 HC5 `RequestConfig/Timeout` 設定。

---

#### [CRITICAL][MIGRATION] C10 — Springfox 不相容（已造成測試啟動失敗）

**Where**
- `pom.xml` (`io.springfox:springfox-boot-starter`)
- `src/main/java/org/springframework/samples/petclinic/PetClinicApplication.java` (`@EnableSwagger2`)
- `mvn -q -DskipTests=false test` 輸出

**Evidence**
```java
import springfox.documentation.swagger2.annotations.EnableSwagger2;
@EnableSwagger2
```
```text
Failed to start bean 'documentationPluginsBootstrapper'
... NullPointerException ... springfox ... PatternsRequestCondition
```

**Why it’s a problem**
- Springfox 與 Spring MVC 6 不相容，屬已知升級阻斷點。

**Recommended fix**
- 遷移到 `org.springdoc:springdoc-openapi-*`，移除 Springfox 與 `@EnableSwagger2`。

---

#### [CRITICAL][MIGRATION] C11 — Spring Batch 5 移除 `JobBuilderFactory/StepBuilderFactory`

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/BatchConfig.java`

**Evidence**
```java
import org.springframework.batch.core.configuration.annotation.JobBuilderFactory;
import org.springframework.batch.core.configuration.annotation.StepBuilderFactory;
```

**Why it’s a problem**
- Spring Batch 5 已移除上述 factory，升級後會編譯失敗。

**Recommended fix**
- 以 `JobBuilder`/`StepBuilder` + `JobRepository`/`PlatformTransactionManager` 改寫。

---

#### [CRITICAL][MIGRATION] C12 — Hibernate 仍使用舊 groupId `org.hibernate`

**Where**
- `pom.xml`

**Evidence**
```xml
<groupId>org.hibernate</groupId>
<artifactId>hibernate-core</artifactId>
```

**Why it’s a problem**
- Boot 3 生態需對齊 `org.hibernate.orm:hibernate-core`，舊座標會造成 BOM 對齊與版本解析風險。

**Recommended fix**
- 改為 `org.hibernate.orm:hibernate-core`，並與 Jakarta persistence import 一起驗證。

---

#### [CRITICAL][MIGRATION] C13 — MySQL 驅動仍使用舊座標 `mysql:mysql-connector-java`

**Where**
- `pom.xml`
- `mvn dependency:tree` 輸出（顯示 relocation warning）

**Evidence**
```xml
<groupId>mysql</groupId>
<artifactId>mysql-connector-java</artifactId>
```
```text
The artifact mysql:mysql-connector-java:jar:8.0.33 has been relocated to com.mysql:mysql-connector-j
```

**Why it’s a problem**
- 此座標已遷移；在 SB3 升級中屬明確需修復項。

**Recommended fix**
- 改為 `com.mysql:mysql-connector-j`。

---

#### [CRITICAL][MIGRATION] C14 — 已移除屬性 `spring.jpa.hibernate.use-new-id-generator-mappings`

**Where**
- `src/main/resources/application.properties`

**Evidence**
```properties
spring.jpa.hibernate.use-new-id-generator-mappings=true
```

**Why it’s a problem**
- 該屬性在 Boot 3 已移除，保留會造成配置錯誤與啟動風險。

**Recommended fix**
- 直接刪除此屬性，改以 Hibernate 6 預設行為為主並補回歸測試。

---

### Warning

#### [WARN][MIGRATION] W1 — `spring.redis.*` 屬性前綴需改為 `spring.data.redis.*`

**Where**
- `src/main/resources/application.properties`

**Evidence**
```properties
spring.redis.host=localhost
spring.redis.port=6379
spring.redis.timeout=2000ms
```

---

#### [WARN][MIGRATION] W2 — `server.max.http.header.size` 已改名

**Where**
- `src/main/resources/application.properties`

**Evidence**
```properties
server.max.http.header.size=65536
```

---

#### [WARN][MIGRATION] W3 — Metrics export 設定路徑已變更

**Where**
- `src/main/resources/application.properties`

**Evidence**
```properties
management.metrics.export.prometheus.enabled=true
management.metrics.export.prometheus.step=1m
```

---

#### [WARN][MIGRATION] W4 — `@EnableBatchProcessing` 在 Boot 自動配置場景不建議保留

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/BatchConfig.java`

**Evidence**
```java
@EnableBatchProcessing
```

---

#### [WARN][MIGRATION] W5 — 多個 `Job` bean 但未指定 `spring.batch.job.name`

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/BatchConfig.java` (`vetDataExportJob`, `visitReminderJob`)
- `src/main/resources/application.properties`（未見 `spring.batch.job.name`）

**Evidence**
```java
public Job vetDataExportJob() { ... }
public Job visitReminderJob() { ... }
```

---

#### [WARN][MIGRATION] W6 — `@ConstructorBinding` 型別層級標註需調整

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/AppProperties.java`

**Evidence**
```java
@ConstructorBinding
@ConfigurationProperties(prefix = "petclinic")
```

---

#### [WARN][MIGRATION] W7 — Maven plugin 座標已 relocation

**Where**
- `pom.xml`

**Evidence**
```xml
<groupId>pl.project13.maven</groupId>
<artifactId>git-commit-id-plugin</artifactId>
```

---

#### [WARN][BASELINE] W8 — `csrf().disable()` 需補強風險評估與條件限制

**Where**
- `src/main/java/org/springframework/samples/petclinic/config/SecurityConfig.java`

**Evidence**
```java
.csrf().disable();
```

**Why it’s a problem**
- 這是安全基線風險，若系統含 session/cookie 認證，需明確替代防護策略。

---

### Suggestion

#### [SUGGESTION][MIGRATION] S1 — 遷移過渡期可暫加 `spring-boot-properties-migrator`

**Where**
- `pom.xml`（目前未配置）

**Recommended fix**
- 過渡期加入 runtime 依賴以在啟動時提示舊屬性，完成遷移後移除。

---

## Completeness Self-Check

- Migration checks 覆蓋：
  - §1 Baseline detection：Boot `2.7.18`（N/A，已在建議升級路徑起點）
  - §2 Java toolchain：命中 C1
  - §3 Dependency blockers：命中 C4/C9/C10/C12/C13，plugin relocation 命中 W7
  - §4 Code-level breaks：命中 C2/C3/C4/C5/C6/C7/C8/C9/C10/C11
  - §5 Property changes：命中 C14/W1/W2/W3；SAML identity-provider 為 N/A（未出現）
  - §6 Spring Batch：命中 C11/W4/W5
  - §7 Packaging/runtime：N/A（jar 封裝，未見 WAR/外部容器設定）
  - §8 Cross-reference：`spring.factories` / `AutoConfiguration.imports` / `javax.inject` / `ErrorController` / `PathPatternParser` / 舊 Micrometer API 皆 N/A（未命中）
- Baseline categories（springboot_reviewer）：
  - Error handling：N/A（未發現新增遷移阻斷）
  - Resource handling：命中 C9（HTTP client/timeout API 不相容）
  - Config validation：命中 C14/W1/W2/W3/W5
  - Logging：N/A（未見遷移阻斷型問題）
  - Security：命中 C6/C7/C8/W8

---

## Strengths

- 掃描範圍完整，核心 `src` + `pom.xml` 均納入。
- 具備 `@SpringBootTest` 基礎整合測試入口，可作為升級回歸驗證起點。

---

## Priority Plan

### P0 — Must Fix (Critical)

1. 升級 Java 17（C1）
2. 完成 Jakarta import/依賴遷移：persistence/validation/xml.bind/annotation（C2~C5）
3. 安全設定重寫為 Security 6 DSL，處理 matcher 與尾斜線（C6~C8）
4. 遷移 HttpClient 5（C9）
5. 以 springdoc 取代 Springfox（C10）
6. 重寫 Batch 設定為 Batch 5 API（C11）

### P1 — Fix Soon (Warning)

1. 更新 properties 新鍵名（W1~W3）
2. 調整 Batch 啟動策略與 `@EnableBatchProcessing` 使用方式（W4~W5）
3. 調整 `@ConstructorBinding` 與 plugin relocation（W6~W7）
4. 針對 CSRF 禁用補上架構說明與防護策略（W8）

### P2 — Backlog (Suggestion)

1. 暫時導入 properties migrator 加速清點（S1）

---

## Verification Checklist

- Build/Test:
  - `mvn -q -DskipTests=false test` ❌（目前失敗，Springfox NPE）
- Dependencies:
  - `mvn dependency:tree` ✅（確認舊座標與舊命名空間仍存在）
- Migration scan:
  - `search_files` 已覆蓋 checks.md §1~§8 與核心交叉檢查項

---

## Assumptions / Open Questions

- `javax.servlet.*` 程式碼層面：N/A（本 repo 未出現 servlet import）。
- 打包相容性（WAR/外部容器）：N/A（`pom.xml` 為 `jar`，未見 WAR 打包設定）。
- `spring.factories` / `AutoConfiguration.imports` / `javax.inject` / `ErrorController` / `PathPatternParser` / Micrometer 舊 API：本 repo 目標程式碼未命中，列為 N/A。 
- `@GetMapping("/")`（WelcomeController）為根路徑，不屬 trailing-slash 破壞案例；C8 僅針對 `"/xxx/"` 路徑與對應 security matcher。
