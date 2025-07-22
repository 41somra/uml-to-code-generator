package mil.af.kesselrun.api;

import mil.af.kesselrun.model.Intelligence;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * Intelligence Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface IntelligenceController {
    
    @GetMapping("/intelligences")
    ResponseEntity<Page<Intelligence>> listIntelligences(Pageable pageable);
    
    @GetMapping("/intelligences/{id}")
    ResponseEntity<Intelligence> getIntelligence(@PathVariable Long id);
    
    @PostMapping("/intelligences")
    ResponseEntity<Intelligence> createIntelligence(@Valid @RequestBody Intelligence entity);
    
    @PutMapping("/intelligences/{id}")
    ResponseEntity<Intelligence> updateIntelligence(@PathVariable Long id, @Valid @RequestBody Intelligence entity);
    
    @DeleteMapping("/intelligences/{id}")
    ResponseEntity<Void> deleteIntelligence(@PathVariable Long id);
}
