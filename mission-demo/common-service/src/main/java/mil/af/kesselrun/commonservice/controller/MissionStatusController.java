package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.MissionStatus;
import mil.af.kesselrun.commonservice.service.MissionStatusService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * MissionStatus REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/missionstatus")
@CrossOrigin(origins = "*")
public class MissionStatusController {
    
    @Autowired
    private MissionStatusService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<MissionStatus>> getAll() {
        List<MissionStatus> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<MissionStatus> getById(@PathVariable Long id) {
        Optional<MissionStatus> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<MissionStatus> create(@Valid @RequestBody MissionStatus entity) {
        MissionStatus created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<MissionStatus> update(@PathVariable Long id, 
                                            @Valid @RequestBody MissionStatus entity) {
        try {
            MissionStatus updated = service.update(id, entity);
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
