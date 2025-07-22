package mil.af.kesselrun.api;

import mil.af.kesselrun.model.MissionPersonnel;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * MissionPersonnel Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface MissionPersonnelController {
    
    @GetMapping("/missionpersonnels")
    ResponseEntity<Page<MissionPersonnel>> listMissionPersonnels(Pageable pageable);
    
    @GetMapping("/missionpersonnels/{id}")
    ResponseEntity<MissionPersonnel> getMissionPersonnel(@PathVariable Long id);
    
    @PostMapping("/missionpersonnels")
    ResponseEntity<MissionPersonnel> createMissionPersonnel(@Valid @RequestBody MissionPersonnel entity);
    
    @PutMapping("/missionpersonnels/{id}")
    ResponseEntity<MissionPersonnel> updateMissionPersonnel(@PathVariable Long id, @Valid @RequestBody MissionPersonnel entity);
    
    @DeleteMapping("/missionpersonnels/{id}")
    ResponseEntity<Void> deleteMissionPersonnel(@PathVariable Long id);
}
