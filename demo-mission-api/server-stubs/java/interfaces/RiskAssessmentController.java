package mil.af.kesselrun.api;

import mil.af.kesselrun.model.RiskAssessment;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * RiskAssessment Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface RiskAssessmentController {
    
    @GetMapping("/riskassessments")
    ResponseEntity<Page<RiskAssessment>> listRiskAssessments(Pageable pageable);
    
    @GetMapping("/riskassessments/{id}")
    ResponseEntity<RiskAssessment> getRiskAssessment(@PathVariable Long id);
    
    @PostMapping("/riskassessments")
    ResponseEntity<RiskAssessment> createRiskAssessment(@Valid @RequestBody RiskAssessment entity);
    
    @PutMapping("/riskassessments/{id}")
    ResponseEntity<RiskAssessment> updateRiskAssessment(@PathVariable Long id, @Valid @RequestBody RiskAssessment entity);
    
    @DeleteMapping("/riskassessments/{id}")
    ResponseEntity<Void> deleteRiskAssessment(@PathVariable Long id);
}
