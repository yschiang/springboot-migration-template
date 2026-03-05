# Migrate Application From Spring Boot 2 to Spring Boot 3

> Source: https://www.baeldung.com/spring-boot-3-migration
> Last updated: December 3, 2025

---

## 1. Overview

In this tutorial, we'll learn how to migrate a Spring Boot application to version 3.0. To successfully migrate an application to Spring Boot 3, we have to ensure that its current Spring Boot version is 2.7, and its Java version is 17.

---

## 2. Core Changes

Spring Boot 3.0 marks a major milestone for the framework, bringing several important modifications to its core components.

### 2.1. Configuration Properties

Some property keys have been modified:

- `spring.redis` has moved to `spring.data.redis`
- `spring.data.cassandra` has moved to `spring.cassandra`
- `spring.jpa.hibernate.use-new-id-generator` is removed
- `server.max.http.header.size` has moved to `server.max-http-request-header-size`
- `spring.security.saml2.relyingparty.registration.{id}.identity-provider` support is removed

To identify those properties, add the `spring-boot-properties-migrator` in `pom.xml`:

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-properties-migrator</artifactId>
    <scope>runtime</scope>
</dependency>
```

This dependency generates a report at start-up time of deprecated property names, and temporarily migrates the properties at runtime.

### 2.2. Jakarta EE 10

The new version of Jakarta EE 10 brings updates to the related dependencies of Spring Boot 3:

- Servlet specification updated to version 6.0
- JPA specification updated to version 3.1

Update the JPA dependency:

```xml
<dependency>
    <groupId>jakarta.persistence</groupId>
    <artifactId>jakarta.persistence-api</artifactId>
    <version>3.1.0</version>
</dependency>
```

Update the Servlet dependency:

```xml
<dependency>
    <groupId>jakarta.servlet</groupId>
    <artifactId>jakarta.servlet-api</artifactId>
    <version>6.0.0</version>
</dependency>
```

In addition to changes in the dependency coordinates, Jakarta EE now uses `jakarta` packages instead of `javax`. After updating dependencies, import statements must be updated accordingly.

### 2.3. Hibernate

Update the Hibernate dependency:

```xml
<dependency>
    <groupId>org.hibernate.orm</groupId>
    <artifactId>hibernate-core</artifactId>
    <version>6.1.4.Final</version>
</dependency>
```

### 2.4. Other Changes

- **Image banner support removed**: only `banner.txt` is considered a valid banner file.
- **Logging date format**: the new default date format for Logback and Log4J2 is `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`. To restore the old format, set `logging.pattern.dateformat` in `application.yaml`.
- **`@ConstructorBinding` only at the constructor level**: no longer necessary at the type level for `@ConfigurationProperties` classes. If a class has multiple constructors, use `@ConstructorBinding` on the desired constructor.

---

## 3. Web Application Changes

### 3.1. Trailing Slash Matching Configuration

The new Spring Boot release deprecates trailing slash matching and sets its default value to `false`.

Example controller:

```java
@RestController
@RequestMapping("/api/v1/todos")
@RequiredArgsConstructor
public class TodosController {
    @GetMapping("/name")
    public List<String> findAllName(){
        return List.of("Hello","World");
    }
}
```

`GET /api/v1/todos/name/` no longer matches and returns HTTP 404.

To re-enable trailing slash matching for all endpoints:

```java
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        configurer.setUseTrailingSlashMatch(true);
    }
}
```

### 3.2. Response Header Size

`server.max.http.header.size` is deprecated in favour of `server.max-http-request-header-size`, which only checks the request header size. To also limit response header size, define a new bean:

```java
@Configuration
public class ServerConfiguration implements WebServerFactoryCustomizer<TomcatServletWebServerFactory> {

    @Override
    public void customize(TomcatServletWebServerFactory factory) {
        factory.addConnectorCustomizers(new TomcatConnectorCustomizer() {
            @Override
            public void customize(Connector connector) {
                connector.setProperty("maxHttpResponseHeaderSize", "100000");
            }
        });
    }
}
```

> If using Jetty instead of Tomcat, change `WebServerFactory` to `JettyServletWebServerFactory`. Other embedded web containers don't support this feature.

### 3.3. Other Changes

- **Graceful shutdown phases**: Spring now initiates graceful shutdown in phase `SmartLifecycle.DEFAULT_PHASE – 2048` and stops the web server in phase `SmartLifecycle.DEFAULT_PHASE – 1024`.

---

## 4. Actuator Changes

### 4.1. Actuator Endpoints Sanitization

Spring Boot 3 masks values for **all keys** by default on `/env` and `/configprops` endpoints. Configure with:

- `management.endpoint.env.show-values`
- `management.endpoint.configprops.show-values`

Values:
- `NEVER` — no values shown
- `ALWAYS` — all values shown
- `WHEN_AUTHORIZED` — shown only if the user is authorized

### 4.2. Other Changes

- **JMX Endpoint Exposure**: JMX handles only the `health` endpoint by default. Customize with `management.endpoints.jmx.exposure.include` and `management.endpoints.jmx.exposure.exclude`.
- **httptrace endpoint renamed**: `/httptrace` is now `/httpexchanges`.
- **Isolated ObjectMapper**: the `ObjectMapper` for actuator endpoint responses is now isolated. Disable with `management.endpoints.jackson.isolated-object-mapper=false`.

---

## 5. Spring Security

Spring Boot 3 is only compatible with Spring Security 6.

**Upgrade path**: Spring Boot 2.7 → Spring Security 5.8 → Spring Security 6 → Spring Boot 3.

Notable changes:

- **`ReactiveUserDetailsService` not autoconfigured**: in the presence of an `AuthenticationManagerResolver`, a `ReactiveUserDetailsService` is no longer autoconfigured.
- **SAML2 Relying Party Configuration**: properties under `spring.security.saml2.relyingparty.registration.{id}.identity-provider` are removed. Use `spring.security.saml2.relyingparty.registration.{id}.asserting-party` instead.

---

## 6. Spring Batch

### 6.1. `@EnableBatchProcessing` Discouraged

Using `@EnableBatchProcessing` (or defining a bean that implements `DefaultBatchConfiguration`) tells autoconfiguration to back off. Remove it to use Spring Boot's autoconfiguration.

### 6.2. Running Multiple Jobs

Running multiple batch jobs simultaneously is no longer supported. If multiple jobs are in the context, specify which to execute on startup via `spring.batch.job.name`. To run multiple jobs, create a separate application for each, or use a scheduler (Quartz, Spring Scheduler, etc.).

---

## 7. HttpClient Changes

Spring Boot 3 upgrades to Apache HttpClient 5.x (from 4.x). Classes have moved from the `org.apache.http.*` namespace to `org.apache.hc.*`.

### 7.1. Legacy Configuration (HttpClient 4.x — no longer works)

```java
@Configuration
public class RestTemplateConfiguration {
    @Bean
    public RestTemplate getRestTemplate() {
        CloseableHttpClient httpClient = HttpClients.custom().build();

        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory();
        requestFactory.setHttpClient(httpClient);
        requestFactory.setConnectTimeout(30000);
        requestFactory.setReadTimeout(30000);
        requestFactory.setConnectionRequestTimeout(30000);

        return new RestTemplate(requestFactory);
    }
}
```

### 7.2. Why This Breaks in Spring Boot 3

- `HttpComponentsClientHttpRequestFactory` now expects a 5.x `CloseableHttpClient`.
- Timeout methods `setConnectTimeout()` and `setReadTimeout()` are deprecated or silently ignored.
- Runtime errors: `NoSuchMethodError`, `ClassNotFoundException`, `org.apache.http.*` incompatibilities.

### 7.3. Migrating to HttpClient 5.x (Before 5.4)

Add dependency:

```xml
<dependency>
    <groupId>org.apache.httpcomponents.client5</groupId>
    <artifactId>httpclient5</artifactId>
</dependency>
```

Configuration:

```java
@Configuration
public class RestTemplateConfiguration {
    @Bean
    public RestTemplate restTemplate() {
        RequestConfig config = RequestConfig.custom()
          .setConnectTimeout(Timeout.ofSeconds(30))
          .setResponseTimeout(Timeout.ofSeconds(30))
          .setConnectionRequestTimeout(Timeout.ofSeconds(30))
          .build();
        CloseableHttpClient client = HttpClients.custom()
          .setDefaultRequestConfig(config)
          .build();
        return new RestTemplate(new HttpComponentsClientHttpRequestFactory(client));
    }
}
```

### 7.4. Migrating to HttpClient 5.4 and Later

```java
@Configuration
public class RestTemplateConfiguration {
    @Bean
    public RestTemplate restTemplate() {
        try {
            SocketConfig socketConfig = SocketConfig.custom()
              .setSoTimeout(Timeout.ofSeconds(30))
              .build();

            ConnectionConfig connectionConfig = ConnectionConfig.custom()
              .setConnectTimeout(Timeout.ofSeconds(30))
              .build();

            RequestConfig requestConfig = RequestConfig.custom()
              .setConnectionRequestTimeout(Timeout.ofSeconds(30))
              .build();

            PoolingHttpClientConnectionManager connectionManager =
              PoolingHttpClientConnectionManagerBuilder.create()
                .setMaxConnPerRoute(20)
                .setMaxConnTotal(100)
                .setDefaultSocketConfig(socketConfig)
                .setDefaultConnectionConfig(connectionConfig)
                .build();

            CloseableHttpClient httpClient = HttpClients.custom()
              .setConnectionManager(connectionManager)
              .setDefaultRequestConfig(requestConfig)
              .build();

            return new RestTemplate(new HttpComponentsClientHttpRequestFactory(httpClient));
        } catch (Exception e) {
            throw new IllegalStateException("Failed to configure RestTemplate", e);
        }
    }
}
```

Key shifts in 5.4+:
- **Timeouts**: configured via `Timeout` API in `SocketConfig`, `ConnectionConfig`, and `RequestConfig`.
- **Connection pooling**: use `PoolingHttpClientConnectionManagerBuilder` (builder pattern).
- **Builder-based configuration**: better separation of concerns and extensibility.

---

## 8. Conclusion

To migrate from Spring Boot 2.7 to Spring Boot 3, the key changes are:

1. Java 17+
2. Jakarta EE: `javax.*` → `jakarta.*`
3. Updated configuration property keys
4. Spring Security 6 (remove `WebSecurityConfigurerAdapter`)
5. Spring Batch autoconfiguration changes
6. Apache HttpClient 4.x → 5.x
7. Actuator endpoint sanitization and renaming
