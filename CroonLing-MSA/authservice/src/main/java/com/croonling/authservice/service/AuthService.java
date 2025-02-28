package com.croonling.authservice.service;

import com.croonling.authservice.model.dto.UserRequestDto;
import com.croonling.authservice.model.dto.UserResponseDto;
import com.croonling.authservice.provider.JwtProvider;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;

import java.util.Map;
import java.util.concurrent.TimeUnit;

@Service
public class AuthService {

    private final JwtProvider jwtProvider;
    private final RedisTemplate<String, String> redisTemplate;

    @Autowired
    public AuthService(JwtProvider jwtProvider, RedisTemplate<String, String> redisTemplate) {
        this.jwtProvider = jwtProvider;
        this.redisTemplate = redisTemplate;
    }

    // 로그인 후 Access Token + Refresh Token 발급
    public Map<String, String> generateTokens(String userId) {
        String accessToken = jwtProvider.generateAccessToken(userId);
        String refreshToken = jwtProvider.generateRefreshToken(userId);

        // Redis에 Refresh Token 저장 (7일 유지)
        redisTemplate.opsForValue().set("refreshToken:" + userId, refreshToken, 7, TimeUnit.DAYS);

        return Map.of(
                "access_token", accessToken,
                "refresh_token", refreshToken,
                "token_type", "Bearer"
        );
    }

    // Refresh Token을 사용하여 새로운 Access Token 발급
    public Map<String, String> refreshAccessToken(String userId, String refreshToken) {
        String storedToken = redisTemplate.opsForValue().get("refreshToken:" + userId);

        if (storedToken != null && storedToken.equals(refreshToken)) {
            String newAccessToken = jwtProvider.generateAccessToken(userId);
            return Map.of(
                    "access_token", newAccessToken,
                    "token_type", "Bearer"
            );
        } else {
            throw new RuntimeException("유효하지 않은 Refresh Token입니다.");
        }
    }

    // 로그아웃 (Refresh Token 삭제)
    public void logout(String userId) {
        redisTemplate.delete("refreshToken:" + userId);
    }


    // OAuth 2.0 로그인 처리
    public UserResponseDto loginWithOAuth(UserRequestDto userRequestDto) {
        String userId = userRequestDto.getProvider() + "_" + userRequestDto.getProviderId(); // OAuth 제공자 + ID 조합

        // Access Token & Refresh Token 발급
        String accessToken = jwtProvider.generateAccessToken(userId);
        String refreshToken = jwtProvider.generateRefreshToken(userId);

        // Redis에 Refresh Token 저장 (7일 유지)
        redisTemplate.opsForValue().set("refreshToken:" + userId, refreshToken, 7, TimeUnit.DAYS);

        return new UserResponseDto(userId, userRequestDto.getUsername(), userRequestDto.getEmail(), accessToken, refreshToken);
    }

}
