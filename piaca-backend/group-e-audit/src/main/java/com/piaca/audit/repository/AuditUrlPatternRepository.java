package com.piaca.audit.repository;

import com.piaca.audit.domain.AuditUrlPattern;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;
import java.util.UUID;

public interface AuditUrlPatternRepository extends JpaRepository<AuditUrlPattern, UUID> {
    List<AuditUrlPattern> findAllByHttpMethod(String httpMethod);
}
