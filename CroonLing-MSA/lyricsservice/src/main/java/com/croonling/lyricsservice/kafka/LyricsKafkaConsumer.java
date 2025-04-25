// LyricsKafkaConsumer.java
package com.croonling.lyricsservice.kafka;

import com.croonling.lyricsservice.model.dto.LyricsRequestDto;
import com.croonling.lyricsservice.service.LyricsService;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class LyricsKafkaConsumer {

    private final LyricsService lyricsService;
    private final ObjectMapper objectMapper;

    public LyricsKafkaConsumer(LyricsService lyricsService, ObjectMapper objectMapper) {
        this.lyricsService = lyricsService;
        this.objectMapper = objectMapper;
    }

    @KafkaListener(topics = "lyrics-events", groupId = "lyrics-service-group")
    public void consume(ConsumerRecord<String, String> record) {
        try {
            LyricsRequestDto dto = objectMapper.readValue(record.value(), LyricsRequestDto.class);
            lyricsService.saveFromKafka(dto);
            System.out.println("✅ Received and saved lyrics for songId: " + dto.getSongId());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
