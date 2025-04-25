package com.croonling.userservice.model.dto;

import com.croonling.userservice.model.entity.User;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;

@Getter
@NoArgsConstructor
@AllArgsConstructor
public class UserResponseDto {


    private String provider;
    private String providerId;
    private String username;
    private String email;

    @Builder
    public UserResponseDto(User user) {
        this.provider = user.getProvider();
        this.providerId = user.getProviderId();
        this.username = user.getUsername();
        this.email = user.getEmail();
    }
}
