package mil.af.kesselrun.api;

import mil.af.kesselrun.model.Mission;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * Mission Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface MissionController {
    
    @GetMapping("/missions")
    ResponseEntity<Page<Mission>> listMissions(Pageable pageable);
    
    @GetMapping("/missions/{id}")
    ResponseEntity<Mission> getMission(@PathVariable Long id);
    
    @PostMapping("/missions")
    ResponseEntity<Mission> createMission(@Valid @RequestBody Mission entity);
    
    @PutMapping("/missions/{id}")
    ResponseEntity<Mission> updateMission(@PathVariable Long id, @Valid @RequestBody Mission entity);
    
    @DeleteMapping("/missions/{id}")
    ResponseEntity<Void> deleteMission(@PathVariable Long id);
}
