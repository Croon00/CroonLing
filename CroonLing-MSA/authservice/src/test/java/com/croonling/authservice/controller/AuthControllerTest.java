package com.croonling.authservice.controller;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.beans.factory.annotation.Autowired;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void oauth2Login_Success() throws Exception {
        mockMvc.perform(get("/auth/login/discord"))
                .andExpect(status().is3xxRedirection()) // Redirect 발생해야 함
                .andExpect(redirectedUrlPattern("https://discord.com/oauth2/authorize*"));
    }
}
