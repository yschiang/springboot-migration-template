package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

import javax.servlet.http.HttpServletRequest;  // BROKEN: should be jakarta.servlet.http

@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                // BROKEN: antMatchers() removed in Spring Security 6 — use requestMatchers()
                .antMatchers("/api/public/**").permitAll()
                .antMatchers("/api/users/").permitAll()  // trailing-slash — path matching semantics changed in SB3
                .antMatchers("/actuator/health").permitAll()
                .anyRequest().authenticated()
            )
            .httpBasic(Customizer.withDefaults());
        return http.build();
    }

    // Unused parameter kept to represent copy-paste artifact from old filter
    private void logRequest(HttpServletRequest request) {
        System.out.println("Request from: " + request.getRemoteAddr());
    }
}
