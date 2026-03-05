package com.example.demo.controller;

import com.example.demo.dto.CreateUserRequest;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.annotation.PostConstruct;
import javax.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;   // migrated to jakarta

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class UserController {

    @PostConstruct
    public void init() {
        // initialisation logic
    }

    @GetMapping("/public/hello")
    public ResponseEntity<Map<String, String>> hello(HttpServletRequest request) {
        Map<String, String> body = new LinkedHashMap<>();
        body.put("message", "Hello from public endpoint");
        body.put("remoteAddr", request.getRemoteAddr());
        return ResponseEntity.ok(body);
    }

    @PostMapping("/users")
    public ResponseEntity<Map<String, String>> createUser(@Valid @RequestBody CreateUserRequest req) {
        Map<String, String> body = new LinkedHashMap<>();
        body.put("status", "created");
        body.put("name", req.getName());
        return ResponseEntity.ok(body);
    }

    // Trailing-slash variant — path matching semantics differ in SB3
    @GetMapping("/users/")
    public ResponseEntity<Map<String, String>> listUsers() {
        return ResponseEntity.ok(Map.of("users", "[]"));
    }
}
