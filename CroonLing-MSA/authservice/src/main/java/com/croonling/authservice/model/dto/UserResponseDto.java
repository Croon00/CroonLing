package com.croonling.authservice.model.dto;

import lombok.Getter;

@Getter
public class UserResponseDto {

    private String userId;
    private String username;
    private String email;
    private String accessToken;
    private String refreshToken;

    public UserResponseDto(String userId, String username, String email, String accessToken, String refreshToken) {
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.accessToken = accessToken;
        this.refreshToken = refreshToken;
    }
}
