package com.piaca.audit.service;

import com.piaca.audit.domain.AuditEvent;
import com.piaca.audit.domain.AuditUrlPattern;
import com.piaca.audit.repository.AuditEventRepository;
import com.piaca.audit.repository.AuditUrlPatternRepository;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.security.Keys;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.util.UUID;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

@Service
public class AuditIngestService {

    @Value("${jwt.secret}")
    private String jwtSecret;

    @Autowired private AuditUrlPatternRepository patternRepo;
    @Autowired private AuditEventRepository eventRepo;

    @Async
    public void record(String url, String method, String authHeader) {
        if (url == null || method == null) return;

        AuditUrlPattern matched = null;
        String entityId = null;

        for (AuditUrlPattern p : patternRepo.findAllByHttpMethod(method.toUpperCase())) {
            Matcher m = Pattern.compile(p.getUrlPattern()).matcher(url);
            if (m.matches()) {
                matched  = p;
                entityId = m.groupCount() >= 1 ? m.group(1) : null;
                break;
            }
        }

        if (matched == null) return;

        UUID userId = extractUserId(authHeader);

        String description = matched.getDescriptionTemplate()
                .replace("{{entity_id}}", entityId != null ? entityId : "desconhecido")
                .replace("{{user_id}}", userId != null ? userId.toString() : "anônimo");

        eventRepo.save(new AuditEvent(url, method.toUpperCase(), userId, matched.getEntityType(), entityId, description));
    }

    private UUID extractUserId(String authHeader) {
        if (authHeader == null || !authHeader.startsWith("Bearer ")) return null;
        try {
            Claims claims = Jwts.parser()
                    .verifyWith(Keys.hmacShaKeyFor(jwtSecret.getBytes(StandardCharsets.UTF_8)))
                    .build()
                    .parseSignedClaims(authHeader.substring(7))
                    .getPayload();
            return UUID.fromString(claims.getSubject());
        } catch (Exception e) {
            return null;
        }
    }
}
