package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.Intelligence;
import mil.af.kesselrun.commonservice.repository.IntelligenceRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * Intelligence Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class IntelligenceService {
    
    @Autowired
    private IntelligenceRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<Intelligence> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<Intelligence> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public Intelligence create(Intelligence entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public Intelligence update(Long id, Intelligence entity) {
        Optional<Intelligence> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("Intelligence not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
