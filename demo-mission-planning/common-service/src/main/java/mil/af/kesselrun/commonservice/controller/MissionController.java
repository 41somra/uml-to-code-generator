package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.Mission;
import mil.af.kesselrun.commonservice.service.MissionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * Mission REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/mission")
@CrossOrigin(origins = "*")
public class MissionController {
    
    @Autowired
    private MissionService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<Mission>> getAll() {
        List<Mission> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<Mission> getById(@PathVariable Long id) {
        Optional<Mission> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<Mission> create(@Valid @RequestBody Mission entity) {
        Mission created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<Mission> update(@PathVariable Long id, 
                                            @Valid @RequestBody Mission entity) {
        try {
            Mission updated = service.update(id, entity);
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
