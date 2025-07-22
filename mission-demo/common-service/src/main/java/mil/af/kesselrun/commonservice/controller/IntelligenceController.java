package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.Intelligence;
import mil.af.kesselrun.commonservice.service.IntelligenceService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * Intelligence REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/intelligence")
@CrossOrigin(origins = "*")
public class IntelligenceController {
    
    @Autowired
    private IntelligenceService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<Intelligence>> getAll() {
        List<Intelligence> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Intelligence> getById(@PathVariable Long id) {
        Optional<Intelligence> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<Intelligence> create(@Valid @RequestBody Intelligence entity) {
        Intelligence created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<Intelligence> update(@PathVariable Long id, 
                                            @Valid @RequestBody Intelligence entity) {
        try {
            Intelligence updated = service.update(id, entity);
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
