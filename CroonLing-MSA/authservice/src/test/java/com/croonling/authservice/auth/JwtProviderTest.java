package com.croonling.authservice.auth;

import static org.junit.jupiter.api.Assertions.*;

import com.croonling.authservice.provider.JwtProvider;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class JwtProviderTest {

    @Value("${jwt.secret}")
    private String secretKey;

    private JwtProvider jwtProvider;

    @Test
    void generateAndValidateToken_Success() {
        jwtProvider = new JwtProvider(secretKey);
        String token = jwtProvider.generateToken("test-user");

        assertNotNull(token);
        assertTrue(jwtProvider.validateToken(token));
    }

    @Test
    void validateToken_Fail() {
        jwtProvider = new JwtProvider(secretKey);
        String invalidToken = "invalid.jwt.token";

        assertFalse(jwtProvider.validateToken(invalidToken));
    }
}
