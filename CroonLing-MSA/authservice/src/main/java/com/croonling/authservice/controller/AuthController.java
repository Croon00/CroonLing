package com.croonling.authservice.controller;

import com.croonling.authservice.model.dto.UserRequestDto;
import com.croonling.authservice.model.dto.UserResponseDto;
import com.croonling.authservice.service.AuthService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

//    // 로그인 후 Access Token + Refresh Token 발급
//    @GetMapping("/callback")
//    public ResponseEntity<Map<String, String>> callback(@RequestParam String userId) {
//        return ResponseEntity.ok(authService.generateTokens(userId));
//    }

    // Refresh Token을 사용하여 새로운 Access Token 발급
    @PostMapping("/refresh")
    public ResponseEntity<Map<String, String>> refresh(@RequestParam String userId, @RequestParam String refreshToken) {
        return ResponseEntity.ok(authService.refreshAccessToken(userId, refreshToken));
    }

    // 로그아웃 (Refresh Token 삭제)
    @DeleteMapping("/logout")
    public ResponseEntity<String> logout(@RequestParam String userId) {
        authService.logout(userId);
        return ResponseEntity.ok("로그아웃 완료");
    }

//    // OAuth 2.0 로그인 (사용자가 Discord 또는 Google로 로그인하면 호출됨)
//    @PostMapping("/oauth/login")
//    public ResponseEntity<UserResponseDto> loginWithOAuth(@RequestBody UserRequestDto userRequestDto) {
//        return ResponseEntity.ok(authService.loginWithOAuth(userRequestDto));
//    }
}
