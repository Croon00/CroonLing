package com.croonling.authservice.model.dto;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Getter;

@Getter
public class UserRequestDto {

    @NotBlank
    private String provider;  // OAuth 제공자 (discord, google 등)

    @NotBlank
    private String providerId;  // OAuth에서 제공하는 사용자 ID

    @NotBlank
    private String username;  // 사용자 이름

    @Email
    @NotBlank
    private String email;  // 이메일 주소
}
