package com.piaca.audit.controller;

import com.piaca.audit.repository.AuditEventRepository;
import com.piaca.audit.service.AuditIngestService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
public class AuditController {

    @Autowired private AuditIngestService ingestService;
    @Autowired private AuditEventRepository eventRepo;

    @PostMapping("/ingest")
    public ResponseEntity<Void> ingest(HttpServletRequest request) {
        ingestService.record(
                request.getHeader("X-Forwarded-Uri"),
                request.getHeader("X-Forwarded-Method"),
                request.getHeader("Authorization")
        );
        return ResponseEntity.ok().build();
    }

    @GetMapping("/audit")
    public Page<AuditLogResponse> getLogs(
            @RequestParam(required = false) UUID userId,
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size
    ) {
        PageRequest pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "occurredAt"));
        return (userId != null
                ? eventRepo.findByUserId(userId, pageable)
                : eventRepo.findAll(pageable)
        ).map(AuditLogResponse::from);
    }
}
