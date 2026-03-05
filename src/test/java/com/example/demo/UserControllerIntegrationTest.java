package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class UserControllerIntegrationTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void publicEndpointShouldReturnHello() throws Exception {
        mockMvc.perform(get("/api/public/hello"))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.message").value("Hello from public endpoint"));
    }

    @Test
    @WithMockUser
    void createUserShouldValidateAndReturn() throws Exception {
        String json = "{\"name\": \"Alice\", \"email\": \"alice@example.com\"}";
        mockMvc.perform(post("/api/users")
                   .contentType(MediaType.APPLICATION_JSON)
                   .content(json))
               .andExpect(status().isOk())
               .andExpect(jsonPath("$.status").value("created"))
               .andExpect(jsonPath("$.name").value("Alice"));
    }

    @Test
    @WithMockUser
    void createUserShouldRejectInvalidEmail() throws Exception {
        String json = "{\"name\": \"Bob\", \"email\": \"not-an-email\"}";
        mockMvc.perform(post("/api/users")
                   .contentType(MediaType.APPLICATION_JSON)
                   .content(json))
               .andExpect(status().isBadRequest());
    }
}
