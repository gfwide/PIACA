package com.piaca.audit.domain;

import jakarta.persistence.*;
import java.time.OffsetDateTime;
import java.util.UUID;

@Entity
@Table(name = "audit_events")
public class AuditEvent {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "occurred_at", insertable = false, updatable = false)
    private OffsetDateTime occurredAt;

    @Column(name = "full_url", nullable = false)
    private String fullUrl;

    @Column(name = "http_method", nullable = false, length = 10)
    private String httpMethod;

    @Column(name = "user_id")
    private UUID userId;

    @Column(name = "entity_type", length = 100)
    private String entityType;

    @Column(name = "entity_id")
    private String entityId;

    @Column(name = "description")
    private String description;

    public AuditEvent() {}

    public AuditEvent(String fullUrl, String httpMethod, UUID userId, String entityType, String entityId, String description) {
        this.fullUrl = fullUrl;
        this.httpMethod = httpMethod;
        this.userId = userId;
        this.entityType = entityType;
        this.entityId = entityId;
        this.description = description;
    }

    public UUID getId() { return id; }
    public OffsetDateTime getOccurredAt() { return occurredAt; }
    public String getFullUrl() { return fullUrl; }
    public String getHttpMethod() { return httpMethod; }
    public UUID getUserId() { return userId; }
    public String getEntityType() { return entityType; }
    public String getEntityId() { return entityId; }
    public String getDescription() { return description; }
}
