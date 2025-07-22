package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.RiskAssessment;
import mil.af.kesselrun.commonservice.repository.RiskAssessmentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * RiskAssessment Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class RiskAssessmentService {
    
    @Autowired
    private RiskAssessmentRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<RiskAssessment> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<RiskAssessment> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public RiskAssessment create(RiskAssessment entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public RiskAssessment update(Long id, RiskAssessment entity) {
        Optional<RiskAssessment> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("RiskAssessment not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
