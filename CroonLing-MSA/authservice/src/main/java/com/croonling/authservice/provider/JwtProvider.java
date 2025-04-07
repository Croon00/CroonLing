package com.croonling.authservice.provider;


import io.jsonwebtoken.JwtException;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Component;

import java.security.Key;
import java.util.Date;
import java.util.concurrent.TimeUnit;

@Component
public class JwtProvider {

    private final Key key;
    private final RedisTemplate<String, String> redisTemplate;

    public JwtProvider(@Value("${JWT_SECRET}") String secretKey, RedisTemplate<String, String> redisTemplate) {
        this.key = Keys.hmacShaKeyFor(secretKey.getBytes());
        this.redisTemplate = redisTemplate;
    }


    // Access Token 생성 (1시간 유효)
    public String generateAccessToken(String userId) {
        return Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + 3600000)) // 1시간 후 만료
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
    }

    // Refresh Token 생성 (7일 유효)
    public String generateRefreshToken(String userId) {
        String refreshToken = Jwts.builder()
                .setSubject(userId)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + 604800000)) // 7일 후 만료
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();

        // Redis에 저장 (7일 동안 유지)
        redisTemplate.opsForValue().set("refreshToken:" + userId, refreshToken, 7, TimeUnit.DAYS);
        return refreshToken;
    }

    // JWT 검증
    public boolean validateToken(String token) {
        try {
            Jwts.parserBuilder().setSigningKey(key).build().parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }

    // JWT에서 사용자 ID 가져오기
    public String getUserIdFromToken(String token) {
        return Jwts.parserBuilder()
                .setSigningKey(key)
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    // Redis에서 Refresh Token 검증
    public boolean validateRefreshToken(String userId, String refreshToken) {
        String storedToken = redisTemplate.opsForValue().get("refreshToken:" + userId);
        return refreshToken.equals(storedToken);
    }
}
