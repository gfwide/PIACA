package com.piaca.audit.controller;

import com.piaca.audit.domain.AuditEvent;
import java.time.OffsetDateTime;

public record AuditLogResponse(
        String method,
        String entityType,
        String description,
        OffsetDateTime timestamp
) {
    public static AuditLogResponse from(AuditEvent e) {
        return new AuditLogResponse(e.getHttpMethod(), e.getEntityType(), e.getDescription(), e.getOccurredAt());
    }
}
