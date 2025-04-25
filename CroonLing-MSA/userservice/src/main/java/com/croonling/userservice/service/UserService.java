package com.croonling.userservice.service;

import com.croonling.userservice.model.dto.UserRequestDto;
import com.croonling.userservice.model.dto.UserResponseDto;

public interface UserService {
    UserResponseDto registerUser(UserRequestDto requestDto);
    UserResponseDto getUserByProvider(String provider, String providerId);
}
