package com.croonling.authservice.exception;

public class OAuthException extends RuntimeException { // ✅ 반드시 RuntimeException을 상속해야 함
    public OAuthException(String message) {
        super(message); // ✅ 부모 클래스(RuntimeException)로 메시지 전달
    }
}
