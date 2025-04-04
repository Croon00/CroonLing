package com.croonling.songservice.kafka;

import com.croonling.songservice.model.dto.SongRequestDto;
import com.croonling.songservice.service.SongService;
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
            songService.saveFromKafka(songDto);  // ✅ 여기서 변경
            System.out.println("✅ Received and saved song: " + songDto.getSongId());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
