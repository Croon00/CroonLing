package com.croonling.userservice.controller;

import com.croonling.userservice.model.dto.UserRequestDto;
import com.croonling.userservice.model.dto.UserResponseDto;
import com.croonling.userservice.service.UserService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/users")
public class UserController {

    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    // OAuth 2.0 로그인 후 유저 정보 저장
    @PostMapping
    public ResponseEntity<UserResponseDto> register(@RequestBody @Valid UserRequestDto requestDto) {
        return ResponseEntity.ok(userService.registerUser(requestDto));
    }

    // OAuth 2.0 사용자 정보 조회
    @GetMapping("/{provider}/{providerId}")
    public ResponseEntity<UserResponseDto> getUser(
            @PathVariable String provider,
            @PathVariable String providerId) {
        return ResponseEntity.ok(userService.getUserByProvider(provider, providerId));
    }
}