# Spring Boot 3.0 Migration Guide

## Overview

This guide assists developers in upgrading applications from Spring Boot 2.x to Spring Boot 3.0.

## Before You Start

### Upgrade to Latest 2.7.x Version

Before you start the upgrade, make sure to upgrade to the latest available `2.7.x` to ensure you're building against the most recent dependencies.

### Review Dependencies

Compare dependency management between versions by reviewing the official documentation for both 2.7.x and 3.0.x to assess project impact.

### Spring Security

Spring Boot 3.0 uses Spring Security 6.0. Consider upgrading to Spring Security 5.8 first, then follow the migration guides for 5.8 to 6.0 transitions.

#### Dispatch Types

Spring Security 6.0 applies authorization to every dispatch type and Spring Boot now configures the security filter accordingly via the `spring.security.filter.dispatcher-types` property.

### Review System Requirements

**Spring Boot 3.0 requires Java 17 or later.** Java 8 is no longer supported, and Spring Framework 6.0 is required.

### Review Deprecations

Ensure your codebase doesn't call methods deprecated in Spring Boot 2.x, as these have been removed in 3.0.

## Upgrade to Spring Boot 3

### Configuration Properties Migration

A `spring-boot-properties-migrator` module analyzes your environment and temporarily migrates properties at runtime.

**Maven:**
```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-properties-migrator</artifactId>
	<scope>runtime</scope>
</dependency>
```

**Gradle:**
```
runtimeOnly("org.springframework.boot:spring-boot-properties-migrator")
```

Remove this module after migration is complete.

### Spring Framework 6.0

Review the official Spring Framework 6.x upgrade guide before continuing.

### Jakarta EE

Spring Boot 3.0 upgraded to Jakarta EE 10, using Servlet 6.0 and JPA 3.1 specifications.

Key changes:
- Use `jakarta.servlet:jakarta.servlet-api` instead of `javax.servlet:javax.servlet-api`
- Update import statements to use `jakarta` packages instead of `javax`

Migration tools available:
- OpenRewrite recipes for Jakarta EE migration
- Spring Boot Migrator project
- IntelliJ IDEA migration support

### Core Changes

#### Image Banner Support Removed

Image-based application banners has been removed and files like `banner.gif`, `banner.jpg`, and `banner.png` are now ignored. Use `banner.txt` instead.

#### Logging Date Format

The default logging date format changed to ISO-8601: `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`. Restore the previous format using `logging.pattern.dateformat` property if needed.

#### @ConstructorBinding

`@ConstructorBinding` is no longer needed at the type level on `@ConfigurationProperties` classes. Remove it unless disambiguating multiple constructors.

If autowiring dependencies into constructors, annotate with `@Autowired` to prevent property binding interpretation.

#### YamlJsonParser Removed

`YamlJsonParser` has been removed. Migrate to alternative `JsonParser` implementations.

#### Auto-configuration Files

Support for registering auto-configurations in `spring.factories` using `org.springframework.boot.autoconfigure.EnableAutoConfiguration` has been removed. Use `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` instead.

## Web Application Changes

### Spring MVC and WebFlux URL Matching

Trailing slash matching defaults to `false`. URLs ending in slashes no longer match by default:

```java
@GetMapping("/some/greeting")
public String greeting() {
  return "Hello";
}
```

This no longer matches `/some/greeting/`, returning HTTP 404 instead.

**Solution for Spring MVC:**
```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {
    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
      configurer.setUseTrailingSlashMatch(true);
    }
}
```

**Solution for Spring WebFlux:**
```java
@Configuration
public class WebConfiguration implements WebFluxConfigurer {
    @Override
    public void configurePathMatching(PathMatchConfigurer configurer) {
      configurer.setUseTrailingSlashMatch(true);
    }
}
```

### server.max-http-header-size

Previously treated inconsistently across web servers. The property now applies only to request header size. For response header limits, use `WebServerFactoryCustomizer`.

### Graceful Shutdown Phases

Graceful shutdown now begins in phase `SmartLifecycle.DEFAULT_PHASE - 2048` with the web server stopping at `DEFAULT_PHASE - 1024`. Update custom `SmartLifecycle` implementations accordingly.

### Jetty

Jetty doesn't yet support Servlet 6.0. Downgrade using the `jakarta-servlet.version` property.

### Apache HttpClient in RestTemplate

Apache HttpClient support was removed from Spring Framework 6.0. Update to `org.apache.httpcomponents.client5:httpclient5`. Check for transitive dependencies on the old `org.apache.httpcomponents:httpclient`.

## Actuator Changes

### JMX Endpoint Exposure

By default, only the health endpoint is exposed over JMX. Configure exposure using `management.endpoints.jmx.exposure.include` and `management.endpoints.jmx.exposure.exclude`.

### httptrace Endpoint Renamed

The `httptrace` endpoint is now called `httpexchanges` to avoid confusion with Micrometer Tracing. Related classes like `HttpTraceRepository` are renamed to `HttpExchangeRepository` in the `org.springframework.boot.actuate.web.exchanges` package.

### Actuator JSON

Responses from the actuator endpoints shipped with Spring Boot now use an isolated `ObjectMapper` for consistency. Set `management.endpoints.jackson.isolated-object-mapper` to `false` to use the application instance.

Custom endpoints should implement `OperationResponseBody` for proper serialization.

### Actuator Endpoints Sanitization

All values in `/env` and `/configprops` endpoints are masked by default. Configure visibility using:
- `management.endpoint.env.show-values`
- `management.endpoint.configprops.show-values`
- `management.endpoint.quartz.show-values`

Options: `NEVER`, `ALWAYS`, or `WHEN_AUTHORIZED`

## Micrometer and Metrics Changes

### Spring Boot 2.x Instrumentation Deprecated

Previous instrumentation filters and interceptors have been removed. Examples:
- `WebMvcMetricsFilter` replaced by Spring Framework's `ServerHttpObservationFilter`
- `MetricsRestTemplateCustomizer` replaced by `ObservationRestTemplateCustomizer`

Related `*TagProvider`, `*TagContributor`, and `*Tags` classes are deprecated.

### Tag Providers and Contributors Migration

Migrate custom metrics using observation conventions:

**Extending default conventions:**
```java
public class ExtendedServerRequestObservationConvention extends DefaultServerRequestObservationConvention {
  @Override
  public KeyValues getLowCardinalityKeyValues(ServerRequestObservationContext context) {
    return super.getLowCardinalityKeyValues(context).and(custom(context));
  }

  protected KeyValue custom(ServerRequestObservationContext context) {
    return KeyValue.of("custom.method", context.getCarrier().getMethod());
  }
}
```

**Implementing custom conventions:**
```java
public class CustomServerRequestObservationConvention implements ServerRequestObservationConvention {
  @Override
  public String getName() {
    return "http.server.requests";
  }

  @Override
  public String getContextualName(ServerRequestObservationContext context) {
    return "http " + context.getCarrier().getMethod().toLowerCase();
  }

  @Override
  public KeyValues getLowCardinalityKeyValues(ServerRequestObservationContext context) {
    return KeyValues.of(method(context), status(context), exception(context));
  }

  @Override
  public KeyValues getHighCardinalityKeyValues(ServerRequestObservationContext context) {
    return KeyValues.of(httpUrl(context));
  }
}
```

**Using ObservationFilter for post-processing:**
```java
public class ServerRequestObservationFilter implements ObservationFilter {
  @Override
  public Observation.Context map(Observation.Context context) {
    if (context instanceof ServerRequestObservationContext serverContext) {
      context.addLowCardinalityKeyValue(KeyValue.of("project", "spring"));
    }
    return context;
  }
}
```

### JvmInfoMetrics Auto-configuration

`JvmInfoMetrics` is now auto-configured. Remove manual bean definitions.

### Actuator Metrics Export Properties

Properties moved from `management.metrics.export.<product>` to `management.<product>.metrics.export`. Example: Prometheus properties moved from `management.metrics.export.prometheus` to `management.prometheus.metrics.export`.

### Mongo Health Check

MongoDB health checks now use `isMaster` instead of `buildInfo`, returning `maxWireVersion` as an integer instead of `version`.

## Data Access Changes

Review Spring Data 2022.0 release notes for important changes to repository interfaces.

### Data Properties Prefix

The `spring.data` prefix has been reserved for Spring Data, implying Spring Data is required on the classpath.

### Cassandra Properties

Configuration properties moved from `spring.data.cassandra.` to `spring.cassandra.`

### Redis Properties

Configuration properties moved from `spring.redis.` to `spring.data.redis.`

### Flyway

Spring Boot 3.0 uses Flyway 9.0 by default. Review Flyway release notes for impacts.

`FlywayConfigurationCustomizer` beans are now called after `Callback` and `JavaMigration` beans are added.

### Liquibase

Spring Boot 3.0 uses Liquibase 4.17.x by default. Some users reported problems; consider overriding the version if affected.

### Hibernate 6.1

Spring Boot 3.0 uses Hibernate 6.1 by default. Review Hibernate 6.0 and 6.1 migration guides.

Dependency management updated to use `org.hibernate.orm` group ID.

The `spring.jpa.hibernate.use-new-id-generator-mappings` property has been removed.

### Embedded MongoDB

Auto-configuration and dependency management for Flapdoodle embedded MongoDB have been removed. Use the Flapdoodle auto-configuration library or Testcontainers instead.

### R2DBC 1.0

Spring Boot 3.0 uses R2DBC 1.0. R2DBC no longer publishes a BOM. New version properties available:
- `oracle-r2dbc.version`
- `r2dbc-h2.version`
- `r2dbc-pool.version`
- `r2dbc-postgres.version`
- `r2dbc-proxy.version`
- `r2dbc-spi.version`

### Elasticsearch Clients and Templates

High-level REST client support removed. Auto-configuration added for Elasticsearch's new Java client and corresponding new templates.

`ReactiveElasticsearchRestClientAutoConfiguration` renamed to `ReactiveElasticsearchClientAutoConfiguration` and moved to `org.springframework.boot.autoconfigure.elasticsearch`.

### MySQL JDBC Driver

MySQL JDBC driver coordinates changed from `mysql:mysql-connector-java` to `com.mysql:mysql-connector-j`.

## Spring Security Changes

Spring Boot 3.0 uses Spring Security 6.0. Review the official migration guide.

### ReactiveUserDetailsService

A `ReactiveUserDetailsService` is no longer auto-configured in the presence of an `AuthenticationManagerResolver`. Define your own bean if needed.

### SAML2 Relying Party Configuration

Properties under `spring.security.saml2.relyingparty.registration.{id}.identity-provider` have been removed. Use `spring.security.saml2.relyingparty.registration.{id}.asserting-party` instead.

## Spring Batch Changes

Spring Boot 3.0 uses Spring Batch 5.0. Review the official migration guide.

### @EnableBatchProcessing

`@EnableBatchProcessing` is no longer required and should be removed for Boot's auto-configuration. Define a bean annotated with `@EnableBatchProcessing` or extending `DefaultBatchConfiguration` to disable auto-configuration and take complete control.

### Multiple Batch Jobs

Running multiple batch jobs is no longer supported. If multiple jobs exist, supply a job name via `spring.batch.job.name` property.

## Spring Session Changes

### Spring Session Store Type

Explicitly configuring the store type for Spring session via `spring.session.store-type` is no longer supported. A fixed order determines which `SessionRepository` auto-configures when multiple implementations exist. Define a custom bean to override this behavior.

## Gradle Changes

### Main Class Name Resolution

`bootJar`, `bootRun`, and `bootWar` now consistently resolve the main class from the main source set output. Configure using the `springBoot` DSL:

```gradle
springBoot {
    mainClass = "com.example.Application"
}
```

### Configuring Gradle Tasks

Tasks now use Gradle's `Property` support. Access values using `.get()`:

```gradle
bootBuildImage.imageName.get()
```

**Kotlin DSL example for disabling layering:**
```kotlin
tasks.named<BootJar>("bootJar") {
	layered {
		enabled.set(false)
	}
}
```

### Excluding Properties From build-info.properties

Use a name-based exclusion mechanism:

```gradle
springBoot {
	buildInfo {
		excludes = ['time']
	}
}
```

**Kotlin DSL:**
```kotlin
springBoot {
	buildInfo {
		excludes.set(setOf("time"))
	}
}
```

## Maven Changes

### Running Applications in Maven Process

The `fork` attribute on `spring-boot:run` and `spring-boot:start` deprecated in Spring Boot 2.7 has been removed.

### Git Commit ID Maven Plugin

Plugin coordinates changed from `pl.project13.maven:git-commit-id-plugin` to `io.github.git-commit-id:git-commit-id-maven-plugin`.

## Dependency Management Changes

### JSON-B

Dependency management for Apache Johnzon removed in favor of Eclipse Yasson. Specify versions explicitly if using Apache Johnzon.

### ANTLR 2

Dependency management for ANTLR 2 removed. Specify versions if needed.

### RxJava

Dependency management for RxJava 1.x and 2.x removed. RxJava 3 dependency management added.

### Hazelcast Hibernate

Dependency management removed. Specify versions or consider `org.hibernate.orm:hibernate-jcache`.

### Ehcache3

Ehcache modules now declared with `jakarta` classifier to support Jakarta EE 9+.

### Other Removals

Support removed for:
- Apache ActiveMQ
- Atomikos
- EhCache 2
- Hazelcast 3
- Apache Solr (Jetty 11 incompatible with its HTTP2 client)
