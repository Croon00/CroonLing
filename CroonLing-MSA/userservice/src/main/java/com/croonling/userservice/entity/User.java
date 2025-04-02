package com.croonling.userservice.entity;

import jakarta.persistence.*;
import lombok.*;

@Entity
@Table(
        name = "users",
        uniqueConstraints = {
                @UniqueConstraint(columnNames = {"provider", "providerId"})  // ✅ 중복 방지
        }
)
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor
@Builder
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String provider; // OAuth 제공자 (discord, google 등)

    @Column(nullable = false)
    private String providerId; // OAuth에서 제공하는 사용자 ID

    @Column(nullable = false)
    private String username; // 사용자 이름

    @Column(nullable = true)
    private String email; // 이메일 주소
}
