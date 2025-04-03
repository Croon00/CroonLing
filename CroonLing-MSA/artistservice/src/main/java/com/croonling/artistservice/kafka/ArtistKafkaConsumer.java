package com.croonling.artistservice.kafka;

import com.croonling.artistservice.model.dto.ArtistRequestDto;
import com.croonling.artistservice.service.ArtistService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class ArtistKafkaConsumer {

    private final ArtistService artistServiceImpl;


    public ArtistKafkaConsumer(ArtistService artistServiceImpl) {
        this.artistServiceImpl = artistServiceImpl;
    }

    @KafkaListener(topics = "artist-events", groupId = "artist-consumer-group")
    public void consume(String message) {
        System.out.println("🟢 Kafka 메시지 수신: " + message);

        // 예: JSON 파싱 → DTO 변환 → 서비스에 저장 위임
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            ArtistRequestDto dto = objectMapper.readValue(message, ArtistRequestDto.class);
            artistServiceImpl.saveFromKafka(dto);
        } catch (Exception e) {
            System.err.println("❌ Kafka 메시지 파싱 실패: " + e.getMessage());
        }
    }
}
