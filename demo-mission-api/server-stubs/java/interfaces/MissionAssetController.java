package mil.af.kesselrun.api;

import mil.af.kesselrun.model.MissionAsset;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * MissionAsset Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface MissionAssetController {
    
    @GetMapping("/missionassets")
    ResponseEntity<Page<MissionAsset>> listMissionAssets(Pageable pageable);
    
    @GetMapping("/missionassets/{id}")
    ResponseEntity<MissionAsset> getMissionAsset(@PathVariable Long id);
    
    @PostMapping("/missionassets")
    ResponseEntity<MissionAsset> createMissionAsset(@Valid @RequestBody MissionAsset entity);
    
    @PutMapping("/missionassets/{id}")
    ResponseEntity<MissionAsset> updateMissionAsset(@PathVariable Long id, @Valid @RequestBody MissionAsset entity);
    
    @DeleteMapping("/missionassets/{id}")
    ResponseEntity<Void> deleteMissionAsset(@PathVariable Long id);
}
