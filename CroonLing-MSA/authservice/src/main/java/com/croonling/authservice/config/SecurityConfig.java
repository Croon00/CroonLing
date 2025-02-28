package com.croonling.authservice.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig{

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf(csrf -> csrf.disable())
                .authorizeHttpRequests(auth -> auth
                        .requestMatchers("auth/login", "/auth/callback").permitAll()
                        .anyRequest().authenticated()
                )
                .oauth2Login(oatuh2 -> oatuh2
                        .defaultSuccessUrl("/auth/callback", true)
                );

        return http.build();
    }
}
