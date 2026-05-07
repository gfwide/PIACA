package com.piaca.audit.domain;

import jakarta.persistence.*;
import java.util.UUID;

@Entity
@Table(name = "audit_url_patterns")
public class AuditUrlPattern {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "url_pattern", nullable = false)
    private String urlPattern;

    @Column(name = "http_method", nullable = false, length = 10)
    private String httpMethod;

    @Column(name = "entity_type", nullable = false, length = 100)
    private String entityType;

    @Column(name = "description_template", nullable = false)
    private String descriptionTemplate;

    public String getUrlPattern() { return urlPattern; }
    public String getEntityType() { return entityType; }
    public String getDescriptionTemplate() { return descriptionTemplate; }
}
