package mil.af.kesselrun.commonservice.controller;

import mil.af.kesselrun.commonservice.entity.MissionAsset;
import mil.af.kesselrun.commonservice.service.MissionAssetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * MissionAsset REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/missionasset")
@CrossOrigin(origins = "*")
public class MissionAssetController {
    
    @Autowired
    private MissionAssetService service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<MissionAsset>> getAll() {
        List<MissionAsset> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }
    
    /**
     * Get by ID
     */
    @GetMapping("/{id}")
    public ResponseEntity<MissionAsset> getById(@PathVariable Long id) {
        Optional<MissionAsset> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<MissionAsset> create(@Valid @RequestBody MissionAsset entity) {
        MissionAsset created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
    
    /**
     * Update existing record
     */
    @PutMapping("/{id}")
    public ResponseEntity<MissionAsset> update(@PathVariable Long id, 
                                            @Valid @RequestBody MissionAsset entity) {
        try {
            MissionAsset updated = service.update(id, entity);
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
