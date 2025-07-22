package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.RiskAssessment;
import mil.af.kesselrun.commonservice.service.RiskAssessmentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * RiskAssessment REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/riskassessment")
@CrossOrigin(origins = "*")
public class RiskAssessmentController {
    
    @Autowired
    private RiskAssessmentService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<RiskAssessment>> getAll() {
        List<RiskAssessment> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<RiskAssessment> getById(@PathVariable Long id) {
        Optional<RiskAssessment> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<RiskAssessment> create(@Valid @RequestBody RiskAssessment entity) {
        RiskAssessment created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<RiskAssessment> update(@PathVariable Long id, 
                                            @Valid @RequestBody RiskAssessment entity) {
        try {
            RiskAssessment updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        } catch (RuntimeException e) {
            return ResponseEntity.notFound().build();
        }
    }
    
    /**
     * Delete record
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        service.delete(id);
        return ResponseEntity.noContent().build();
    }
}
