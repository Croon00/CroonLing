package com.croonling.authservice.handler;

import com.croonling.authservice.client.UserClient;
import com.croonling.authservice.model.dto.UserRequestDto;
import com.croonling.authservice.provider.JwtProvider;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class OAuth2SuccessHandler implements  AuthenticationSuccessHandler {
    private final JwtProvider jwtProvider;
    private final UserClient userClient;

    public OAuth2SuccessHandler(JwtProvider jwtProvider, UserClient userClient) {
        this.jwtProvider = jwtProvider;
        this.userClient = userClient;
    }

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication) throws IOException {
        OAuth2User oAuth2User = (OAuth2User) authentication.getPrincipal();


        String discordId = oAuth2User.getAttribute("id");
        String username = oAuth2User.getAttribute("username");
        String email = oAuth2User.getAttribute("email");

        // ✅ DTO 객체 생성
        UserRequestDto userRequestDto = new UserRequestDto("discord",discordId, username, email);


        // ✅ 사용자 저장 (UserService 호출)
        userClient.saveIfNotExists(userRequestDto);

        // ✅ JWT 생성
        String accessToken = jwtProvider.generateAccessToken(discordId);
        String refreshToken = jwtProvider.generateRefreshToken(discordId);
        // ✅ 프론트로 리디렉션 + 토큰 전달
        response.sendRedirect("http://localhost:3000/dashboard?access_token=" + accessToken + "&refresh_token=" + refreshToken);
    }
}

