package com.croonling.api_gateway.config;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpHeaders;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;



import javax.crypto.SecretKey;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    @Value("${JWT_SECRET}")
    private String SECRET_KEY;

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain filterChain) throws ServletException, IOException {
        String authHeader = request.getHeader(HttpHeaders.AUTHORIZATION);

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }

        String token = authHeader.replace("Bearer ", "");

        if (!validateToken(token)) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }

        // ✅ 인증 성공 후 SecurityContext 설정 (선택 사항)
        // Authentication auth = new UsernamePasswordAuthenticationToken(...);
        // SecurityContextHolder.getContext().setAuthentication(auth);

        filterChain.doFilter(request, response);
    }

    private boolean validateToken(String token) {
        try {
            SecretKey key = Keys.hmacShaKeyFor(SECRET_KEY.getBytes(StandardCharsets.UTF_8));
            Claims claims = Jwts.parserBuilder()
                    .setSigningKey(key)
                    .build()
                    .parseClaimsJws(token)
                    .getBody();
            return claims.getSubject() != null;
        } catch (Exception e) {
            return false;
        }
    }
}