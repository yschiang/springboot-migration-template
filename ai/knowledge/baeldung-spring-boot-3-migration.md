# Baeldung — Spring Boot 2 → 3 Migration (Supplementary Examples)

> Source: https://www.baeldung.com/spring-boot-3-migration
> Last updated: December 3, 2025
>
> **Scope:** Only content NOT already covered by the official migration guide (`spring-boot-3.0-migration-guide.md`).
> For core changes (Jakarta EE, config properties, trailing slash, actuator, security, batch), see the official guide.

---

## 1. Response Header Size — Tomcat Customizer

`server.max-http-request-header-size` only checks request headers. To also limit **response** header size:

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

---

## 2. HttpClient 4.x → 5.x Migration

Spring Boot 3 upgrades to Apache HttpClient 5.x (from 4.x). Classes have moved from the `org.apache.http.*` namespace to `org.apache.hc.*`.

### 2.1. Legacy Configuration (HttpClient 4.x — no longer works)

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

### 2.2. Why This Breaks in Spring Boot 3

- `HttpComponentsClientHttpRequestFactory` now expects a 5.x `CloseableHttpClient`.
- Timeout methods `setConnectTimeout()` and `setReadTimeout()` are deprecated or silently ignored.
- Runtime errors: `NoSuchMethodError`, `ClassNotFoundException`, `org.apache.http.*` incompatibilities.

### 2.3. Migrating to HttpClient 5.x (Before 5.4)

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

### 2.4. Migrating to HttpClient 5.4 and Later

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
