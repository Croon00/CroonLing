package com.croonling.songservice.service;

import com.croonling.songservice.dto.SongRequestDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class SongKafkaConsumer {

    private final SongService songService;
    private final ObjectMapper objectMapper;

    public SongKafkaConsumer(SongService songService, ObjectMapper objectMapper) {
        this.songService = songService;
        this.objectMapper = objectMapper;
    }

    @KafkaListener(topics = "song-events", groupId = "song-service-group")
    public void consume(ConsumerRecord<String, String> record) {
        try {
            SongRequestDto songDto = objectMapper.readValue(record.value(), SongRequestDto.class);
            songService.saveSong(songDto);
            System.out.println("✅ Received and saved song: " + songDto);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
