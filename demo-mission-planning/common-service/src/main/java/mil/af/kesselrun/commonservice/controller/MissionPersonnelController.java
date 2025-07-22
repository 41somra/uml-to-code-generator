package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.MissionPersonnel;
import mil.af.kesselrun.commonservice.service.MissionPersonnelService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * MissionPersonnel REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/missionpersonnel")
@CrossOrigin(origins = "*")
public class MissionPersonnelController {
    
    @Autowired
    private MissionPersonnelService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<MissionPersonnel>> getAll() {
        List<MissionPersonnel> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<MissionPersonnel> getById(@PathVariable Long id) {
        Optional<MissionPersonnel> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<MissionPersonnel> create(@Valid @RequestBody MissionPersonnel entity) {
        MissionPersonnel created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<MissionPersonnel> update(@PathVariable Long id, 
                                            @Valid @RequestBody MissionPersonnel entity) {
        try {
            MissionPersonnel updated = service.update(id, entity);
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
