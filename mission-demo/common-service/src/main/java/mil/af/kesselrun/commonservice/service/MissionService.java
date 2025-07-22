package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.Mission;
import mil.af.kesselrun.commonservice.repository.MissionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * Mission Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class MissionService {
    
    @Autowired
    private MissionRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<Mission> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<Mission> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public Mission create(Mission entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public Mission update(Long id, Mission entity) {
        Optional<Mission> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("Mission not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
