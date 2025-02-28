package com.croonling.userservice.service;

import com.croonling.userservice.dto.UserRequestDto;
import com.croonling.userservice.dto.UserResponseDto;
import com.croonling.userservice.entity.User;
import com.croonling.userservice.exception.UserNotFoundException;
import com.croonling.userservice.repository.UserRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;

    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    // OAuth 2.0 로그인 후 사용자 정보 저장
    @Override
    @Transactional
    public UserResponseDto registerUser(UserRequestDto requestDto) {
        Optional<User> existingUser = userRepository.findByProviderAndProviderId(
                requestDto.getProvider(), requestDto.getProviderId()
        );

        User user = existingUser.orElseGet(() -> {
            User newUser = User.builder()
                    .provider(requestDto.getProvider())
                    .providerId(requestDto.getProviderId())
                    .username(requestDto.getUsername())
                    .email(requestDto.getEmail())
                    .build();
            return userRepository.save(newUser);
        });

        return new UserResponseDto(user);
    }

    // 사용자 정보 조회
    @Override
    @Transactional(readOnly = true)
    public UserResponseDto getUserByProvider(String provider, String providerId) {
        User user = userRepository.findByProviderAndProviderId(provider, providerId)
                .orElseThrow(() -> new UserNotFoundException("사용자를 찾을 수 없습니다."));
        return new UserResponseDto(user);
    }
}
