package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.MissionStatus;
import mil.af.kesselrun.commonservice.repository.MissionStatusRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * MissionStatus Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class MissionStatusService {
    
    @Autowired
    private MissionStatusRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<MissionStatus> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<MissionStatus> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public MissionStatus create(MissionStatus entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public MissionStatus update(Long id, MissionStatus entity) {
        Optional<MissionStatus> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("MissionStatus not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
