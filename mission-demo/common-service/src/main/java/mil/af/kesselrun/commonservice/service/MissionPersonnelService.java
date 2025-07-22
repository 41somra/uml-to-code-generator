package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.MissionPersonnel;
import mil.af.kesselrun.commonservice.repository.MissionPersonnelRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * MissionPersonnel Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class MissionPersonnelService {
    
    @Autowired
    private MissionPersonnelRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<MissionPersonnel> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<MissionPersonnel> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public MissionPersonnel create(MissionPersonnel entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public MissionPersonnel update(Long id, MissionPersonnel entity) {
        Optional<MissionPersonnel> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("MissionPersonnel not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
