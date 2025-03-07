package com.croonling.artistservice.service;

import com.croonling.artistservice.dto.ArtistRequestDto;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;

@Service
public class ArtistKafkaConsumer {

    private final ArtistService artistService;
    private final ObjectMapper objectMapper;

    public ArtistKafkaConsumer(ArtistService artistService, ObjectMapper objectMapper) {
        this.artistService = artistService;
        this.objectMapper = objectMapper;
    }

    @KafkaListener(topics = "artist-events", groupId = "artist-service-group")
    public void consume(ConsumerRecord<String, String> record) {
        try {
            ArtistRequestDto artistDto = objectMapper.readValue(record.value(), ArtistRequestDto.class);
            artistService.saveArtist(artistDto);
            System.out.println("✅ Received and saved artist: " + artistDto);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
