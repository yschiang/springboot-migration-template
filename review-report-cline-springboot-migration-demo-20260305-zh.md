# 審查報告 — cline-springboot-migration-demo

## 目錄
- [概覽](#概覽)
- [發現問題](#發現問題)
  - [嚴重 Critical](#嚴重-critical)
  - [警告 Warning](#警告-warning)
  - [建議 Suggestion](#建議-suggestion)
- [優點](#優點)
- [優先修復計畫](#優先修復計畫)
- [驗證清單](#驗證清單)
- [假設與待確認事項](#假設與待確認事項)

---

## 概覽

| 欄位              | 值                                                                 |
|-------------------|--------------------------------------------------------------------|
| **倉庫**          | `cline-springboot-migration-demo`                                  |
| **提交 / 分支**   | `feature/sb2-to-sb3-broken-migration`                             |
| **建置工具**      | Maven                                                              |
| **Boot 版本**     | `3.2.5`（parent POM）                                             |
| **Java 目標版本** | `11`（pom.xml 中的 `java.version` 屬性）                          |
| **Web 類型**      | Servlet（spring-boot-starter-web）                                 |
| **建議**          | **`NO-GO`** — 6 個嚴重問題；專案無法編譯或啟動                    |

### 摘要

| 嚴重性     | 數量    | 說明              |
|------------|---------|-------------------|
| Critical   | `6`     | 合併前必須修復    |
| Warning    | `1`     | 儘快修復          |
| Suggestion | `1`     | 非必要，有助品質  |
| **合計**   | **`8`** | —                 |

---

## 發現問題

### 嚴重 Critical

---

#### [CRITICAL] C1 — Java 工具鏈目標為 Java 11（Spring Boot 3 需要 17+）

**位置**
- 檔案：`pom.xml`
- 區段：`<java.version>` 屬性，第 23 行

**證據**
```xml
<properties>
    <!-- TODO: update java.version - skipping for now -->
    <java.version>11</java.version>
</properties>
```

**問題影響**
- Spring Boot 3.x / Spring Framework 6.x 最低要求 Java 17。使用 Java 11 編譯或執行不被支援，將導致建置失敗。TODO 注解確認此問題為刻意延後處理。

**建議修復**
```xml
<properties>
    <java.version>17</java.version>
</properties>
```
同時確認本地 JDK 及 CI 工具鏈也升級至 JDK 17+。

**待辦事項**
- [ ] 將 `pom.xml` 中的 `<java.version>` 改為 `17`
- [ ] 確認 `JAVA_HOME` 及 CI 流水線使用 JDK 17+

**參考資料**
- [SB3 遷移指南 — 系統需求](ai/knowledge/spring-boot-3.0-migration-guide.md#review-system-requirements)

---

#### [CRITICAL] C2 — pom.xml 中宣告了舊版 javax.* 依賴

**位置**
- 檔案：`pom.xml`，第 55–67 行

**證據**
```xml
<dependency>
    <groupId>javax.servlet</groupId>
    <artifactId>javax.servlet-api</artifactId>
    <version>4.0.1</version>
    <scope>provided</scope>
</dependency>

<dependency>
    <groupId>javax.validation</groupId>
    <artifactId>validation-api</artifactId>
    <version>2.0.1.Final</version>
</dependency>
```

**問題影響**
- Spring Boot 3 搭載 Tomcat 10（`jakarta.servlet`）與 `jakarta.validation`。顯式宣告 `javax.*` 對應套件會在 classpath 上產生重複且衝突的類別，導致執行期 `ClassCastException` 或 `NoClassDefFoundError`。Spring Boot BOM 已透過 starter 自動管理正確的 Jakarta 版本，這兩個依賴應直接移除。

**建議修復**
- 直接刪除這兩個依賴區塊，無需替換。

**待辦事項**
- [ ] 從 `pom.xml` 移除 `javax.servlet:javax.servlet-api`
- [ ] 從 `pom.xml` 移除 `javax.validation:validation-api`

**參考資料**
- [SB3 遷移指南 — Jakarta EE](ai/knowledge/spring-boot-3.0-migration-guide.md#jakarta-ee)

---

#### [CRITICAL] C3 — Springfox 2.x 與 Spring Boot 3 不相容

**位置**
- 檔案：`pom.xml`，第 69–79 行
- 檔案：`src/main/java/com/example/demo/DemoApplication.java`，第 5 行與第 8 行

**證據**
```xml
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger2</artifactId>
    <version>2.9.2</version>
</dependency>
<dependency>
    <groupId>io.springfox</groupId>
    <artifactId>springfox-swagger-ui</artifactId>
    <version>2.9.2</version>
</dependency>
```
```java
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@SpringBootApplication
@EnableSwagger2
public class DemoApplication {
```

**問題影響**
- Springfox 2.x 與 `javax.*` 及 Spring MVC 5 內部 API 強耦合，不支援 Spring Framework 6 / Spring Boot 3。應用程式將因 `BeanCreationException` 無法啟動。移除 Springfox 後，`@EnableSwagger2` 也將無法編譯。

**建議修復**
1. 從 `pom.xml` 移除兩個 Springfox 依賴。
2. 從 `DemoApplication.java` 移除 `@EnableSwagger2` 及其 import。
3. 以 SB3 相容的 `springdoc-openapi-starter-webmvc-ui` 取代：

```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.5.0</version>
</dependency>
```

修復後的 `DemoApplication.java`：
```java
@SpringBootApplication
public class DemoApplication {
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}
```

**待辦事項**
- [ ] 從 `pom.xml` 移除 Springfox 兩個依賴
- [ ] 從 `DemoApplication.java` 移除 `@EnableSwagger2` 及其 import
- [ ] 若需要 Swagger UI，加入 `springdoc-openapi-starter-webmvc-ui`

---

#### [CRITICAL] C4 — 原始碼中使用 javax.* Import

**位置**
- 檔案：`src/main/java/com/example/demo/config/SecurityConfig.java`，第 10 行
- 檔案：`src/main/java/com/example/demo/controller/UserController.java`，第 7–8 行
- 檔案：`src/main/java/com/example/demo/dto/CreateUserRequest.java`，第 3–5 行

**證據**
```java
// SecurityConfig.java:10
import javax.servlet.http.HttpServletRequest;

// UserController.java:7-8
import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletRequest;

// CreateUserRequest.java:3-5
import javax.validation.constraints.Email;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Size;
```

**問題影響**
- Spring Boot 3 / Jakarta EE 10 將所有 `javax.*` API 移至 `jakarta.*` 命名空間。移除 C2 的舊版 jar 後，這些 import 將導致編譯失敗。即使暫時保留 jar，執行期使用 `jakarta.*` 型別，仍會在過濾器鏈呼叫時發生 `ClassCastException`。

**建議修復**

`SecurityConfig.java`：
```java
import jakarta.servlet.http.HttpServletRequest;
```

`UserController.java`：
```java
import jakarta.annotation.PostConstruct;
import jakarta.servlet.http.HttpServletRequest;
// 第 9 行的 jakarta.validation.Valid 已正確
```

`CreateUserRequest.java`：
```java
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
```

**待辦事項**
- [ ] 將三個檔案中所有 `javax.*` import 替換為 `jakarta.*`

**參考資料**
- [SB3 遷移指南 — Jakarta EE](ai/knowledge/spring-boot-3.0-migration-guide.md#jakarta-ee)

---

#### [CRITICAL] C5 — antMatchers() 在 Spring Security 6 中已移除

**位置**
- 檔案：`src/main/java/com/example/demo/config/SecurityConfig.java`，第 21–23 行

**證據**
```java
.authorizeHttpRequests(auth -> auth
    .antMatchers("/api/public/**").permitAll()
    .antMatchers("/api/users/").permitAll()
    .antMatchers("/actuator/health").permitAll()
    .anyRequest().authenticated()
)
```

**問題影響**
- `antMatchers()` 在 Spring Security 6 的 `AuthorizationManagerRequestMatcherRegistry` 中已被移除。呼叫此方法會產生**編譯錯誤**（`cannot find symbol`），專案無法建置。

**建議修復**
```java
.authorizeHttpRequests(auth -> auth
    .requestMatchers("/api/public/**").permitAll()
    .requestMatchers("/api/users").permitAll()
    .requestMatchers("/actuator/health").permitAll()
    .anyRequest().authenticated()
)
```
注意：`/api/users/` 的尾斜線已一併移除，詳見 C6。

**待辦事項**
- [ ] 將 `SecurityConfig.java` 中所有 `.antMatchers(...)` 替換為 `.requestMatchers(...)`

**參考資料**
- [Spring Security 6 遷移指南](https://docs.spring.io/spring-security/reference/migration/index.html)

---

#### [CRITICAL] C6 — 尾斜線路由導致確定性 HTTP 404 與安全規則失效

**位置**
- 檔案：`src/main/java/com/example/demo/controller/UserController.java`，第 40 行
- 檔案：`src/main/java/com/example/demo/config/SecurityConfig.java`，第 22 行

**證據**
```java
// UserController.java:40
@GetMapping("/users/")
public ResponseEntity<Map<String, String>> listUsers() { ... }

// SecurityConfig.java:22
.antMatchers("/api/users/").permitAll()
```

**問題影響**
- Spring Boot 3 / Spring MVC 6 **預設停用尾斜線匹配**，產生兩個確定性的執行期故障：
  1. `GET /api/users` 返回 **HTTP 404** — 路由 `/users/` 不再匹配無尾斜線的請求。
  2. 安全規則 `.requestMatchers("/api/users/")` **不匹配** `GET /api/users`，該請求落入 `.anyRequest().authenticated()`，使原本應為公開的端點**靜默地要求認證** — 安全行為退化。
- 兩個後果皆為確定性，非機率性。依更新後的嚴重性規則評定為 Critical。

**建議修復**

`UserController.java`：
```java
@GetMapping("/users")
public ResponseEntity<Map<String, String>> listUsers() { ... }
```

`SecurityConfig.java`（配合 C5 修復後）：
```java
.requestMatchers("/api/users").permitAll()
```

**待辦事項**
- [ ] 將 `UserController.java` 中的 `@GetMapping("/users/")` 改為 `@GetMapping("/users")`
- [ ] 將 `SecurityConfig.java` 中的安全規則路徑從 `/api/users/` 改為 `/api/users`

**參考資料**
- [SB3 遷移指南 — 尾斜線匹配](ai/knowledge/spring-boot-3.0-migration-guide.md#spring-mvc-and-webflux-url-matching)
- [更新後的嚴重性規則](ai/knowledge/severity_rubric.md)

---

### 警告 Warning

---

#### [WARN] W1 — application.yml 中使用已移除或更名的屬性

**位置**
- 檔案：`src/main/resources/application.yml`，第 8–13、15–19、27–32 行

**證據**
```yaml
spring:
  mvc:
    pathmatch:
      use-suffix-pattern: true             # SB3 已移除
      use-registered-suffix-pattern: true  # SB3 已移除

  redis:
    host: localhost                        # 已更名為 spring.data.redis.*
    port: 6379
    timeout: 2000ms

management:
  metrics:
    export:
      prometheus:
        enabled: true                      # 已更名為 management.prometheus.metrics.export.*
        step: 1m
```

**問題影響**
- `spring.mvc.pathmatch.use-suffix-pattern` 和 `use-registered-suffix-pattern` 在 SB3 中已移除，後綴模式匹配不再支援，這些屬性被靜默忽略。
- `spring.redis.*` 已更名為 `spring.data.redis.*`，Redis 將無法正確設定，連線在啟動時或首次使用時靜默失敗。
- `management.metrics.export.prometheus.*` 已移至 `management.prometheus.metrics.export.*`，Prometheus 抓取將被靜默停用。

**建議修復**
```yaml
spring:
  # 完全移除 spring.mvc.pathmatch — SB3 已不支援後綴匹配

  data:
    redis:
      host: localhost
      port: 6379
      timeout: 2000ms

management:
  prometheus:
    metrics:
      export:
        enabled: true
        step: 1m
```

**待辦事項**
- [ ] 移除 `spring.mvc.pathmatch.use-suffix-pattern` 和 `use-registered-suffix-pattern`
- [ ] 將 `spring.redis.*` 更名為 `spring.data.redis.*`
- [ ] 將 `management.metrics.export.prometheus.*` 更名為 `management.prometheus.metrics.export.*`

**參考資料**
- [SB3 遷移指南 — Redis 屬性](ai/knowledge/spring-boot-3.0-migration-guide.md#redis-properties)
- [SB3 遷移指南 — Actuator 指標匯出屬性](ai/knowledge/spring-boot-3.0-migration-guide.md#actuator-metrics-export-properties)

---

### 建議 Suggestion

---

#### [SUGGESTION] S1 — 加入 maven-enforcer-plugin 防止 Java 版本退化

**位置**
- 檔案：`pom.xml`
- 區段：`<build><plugins>`

**證據**
```xml
<!-- 無 enforcer plugin；java.version 被靜默保留為 11，儘管 SB3 要求 17+ -->
```

**問題影響**
- 無 enforcer 規則時，`java.version` 可能被不小心降至 17 以下而不會立即報錯。此分支的 C1 即為直接後果。

**建議修復**
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-enforcer-plugin</artifactId>
    <executions>
        <execution>
            <id>enforce-java</id>
            <goals><goal>enforce</goal></goals>
            <configuration>
                <rules>
                    <requireJavaVersion>
                        <version>[17,)</version>
                    </requireJavaVersion>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

**待辦事項**
- [ ] 加入帶有 `requireJavaVersion >= 17` 規則的 `maven-enforcer-plugin`

---

## 優點

- `SecurityConfig.java` 已正確使用 `SecurityFilterChain` Bean 模式，`WebSecurityConfigurerAdapter` 已被正確替換。
- `UserController.java` 第 9 行的 `jakarta.validation.Valid` 已正確 — Jakarta 遷移已部分完成。
- 整合測試已涵蓋公開端點、認證路徑及驗證拒絕情境（`@SpringBootTest` + MockMvc）。
- Actuator 端點曝露已限縮（僅 `health`、`info`、`prometheus`）。

---

## 優先修復計畫

### P0 — 必須修復（Critical）
> 影響：建置失敗 / 應用程式無法啟動或行為異常

| # | 問題 | 檔案 | 預估工時 |
|---|------|------|----------|
| 1 | Java 11 → 17（C1） | `pom.xml` | 5m |
| 2 | 移除 javax.* 依賴（C2） | `pom.xml` | 10m |
| 3 | 以 springdoc 取代 Springfox（C3） | `pom.xml`、`DemoApplication.java` | 30m |
| 4 | javax.* import → jakarta.*（C4） | `SecurityConfig.java`、`UserController.java`、`CreateUserRequest.java` | 15m |
| 5 | antMatchers → requestMatchers（C5） | `SecurityConfig.java` | 5m |
| 6 | 移除路由與安全規則中的尾斜線（C6） | `UserController.java`、`SecurityConfig.java` | 5m |

### P1 — 儘快修復（Warning）
> 影響：執行期靜默設定錯誤

| # | 問題 | 檔案 | 預估工時 |
|---|------|------|----------|
| 1 | 更名/已移除的設定屬性（W1） | `application.yml` | 15m |

### P2 — 待辦（Suggestion）
> 影響：防止未來退化

| # | 問題 | 預估工時 |
|---|------|----------|
| 1 | 加入 maven-enforcer Java 版本檢查（S1） | 10m |

---

## 驗證清單

- 建置：
  - `mvn -q clean package -DskipTests`
- 單元測試：
  - `mvn -q -DskipTests=false test`
- 冒煙啟動：
  - `mvn spring-boot:run`（確認啟動時無 `BeanCreationException`）
- 依賴檢查：
  - `mvn -q dependency:tree | rg "javax\."` → 必須零結果
  - `mvn -q dependency:tree | rg "jakarta\."` → 應顯示 Jakarta 套件

---

## 假設與待確認事項

- `application.yml` 中宣告了 Redis 設定，但 `pom.xml` 中不存在 `spring-boot-starter-data-redis`。若 Redis 確實有使用，必須加入該 starter；若為複製貼上的殘留設定，應整塊移除。
- Springfox Swagger UI 的路徑為 `/swagger-ui.html`；springdoc 的路徑為 `/swagger-ui/index.html`。任何指向舊路徑的 API gateway 規則或書籤必須一併更新。
