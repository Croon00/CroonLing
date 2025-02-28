package com.croonling.userservice.dto;

import com.croonling.userservice.entity.User;
import lombok.Getter;

@Getter
public class UserResponseDto {

    private Long id;
    private String provider;
    private String providerId;
    private String username;
    private String email;

    public UserResponseDto(User user) {
        this.id = user.getId();
        this.provider = user.getProvider();
        this.providerId = user.getProviderId();
        this.username = user.getUsername();
        this.email = user.getEmail();
    }
}
