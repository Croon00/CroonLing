package com.croonling.authservice.client;

import com.croonling.authservice.model.dto.UserRequestDto;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

@FeignClient(name = "user-service", url = "http://user-service.msa.local")  // Gateway를 통해 연결 가능
public interface UserClient {

    @PostMapping("/users")
    void saveIfNotExists(@RequestBody UserRequestDto userRequestDto);
}