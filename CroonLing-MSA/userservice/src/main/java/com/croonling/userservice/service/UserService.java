package com.croonling.userservice.service;

import com.croonling.userservice.dto.UserRequestDto;
import com.croonling.userservice.dto.UserResponseDto;

public interface UserService {
    UserResponseDto registerUser(UserRequestDto requestDto);
    UserResponseDto getUserByProvider(String provider, String providerId);
}
