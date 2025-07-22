package mil.af.kesselrun.api;

import mil.af.kesselrun.model.MissionStatus;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * MissionStatus Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface MissionStatusController {
    
    @GetMapping("/missionstatuss")
    ResponseEntity<Page<MissionStatus>> listMissionStatuss(Pageable pageable);
    
    @GetMapping("/missionstatuss/{id}")
    ResponseEntity<MissionStatus> getMissionStatus(@PathVariable Long id);
    
    @PostMapping("/missionstatuss")
    ResponseEntity<MissionStatus> createMissionStatus(@Valid @RequestBody MissionStatus entity);
    
    @PutMapping("/missionstatuss/{id}")
    ResponseEntity<MissionStatus> updateMissionStatus(@PathVariable Long id, @Valid @RequestBody MissionStatus entity);
    
    @DeleteMapping("/missionstatuss/{id}")
    ResponseEntity<Void> deleteMissionStatus(@PathVariable Long id);
}
