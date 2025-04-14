package com.croonling.api_gateway.config;


import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {

    @Bean
    public OpenAPI croonlingOpenAPI(){
        return new OpenAPI()
                .info(new Info()
                        .title("CroonLing Gateway API Docs")
                        .description("CroonLing의 API 문서 통합")
                        .version("v1.0"));
    }
}
