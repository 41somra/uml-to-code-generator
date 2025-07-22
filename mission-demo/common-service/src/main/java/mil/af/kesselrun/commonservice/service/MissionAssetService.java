package mil.af.kesselrun.commonservice.service;

import mil.af.kesselrun.commonservice.entity.MissionAsset;
import mil.af.kesselrun.commonservice.repository.MissionAssetRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * MissionAsset Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class MissionAssetService {
    
    @Autowired
    private MissionAssetRepository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<MissionAsset> findAll() {
        return repository.findAllActive();
    }
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<MissionAsset> findById(Long id) {
        return repository.findById(id);
    }
    
    /**
     * Create new record
     */
    public MissionAsset create(MissionAsset entity) {
        return repository.save(entity);
    }
    
    /**
     * Update existing record
     */
    public MissionAsset update(Long id, MissionAsset entity) {
        Optional<MissionAsset> existing = repository.findById(id);
        if (existing.isPresent()) {
            entity.setId(id);
            return repository.save(entity);
        }
        throw new RuntimeException("MissionAsset not found with id: " + id);
    }
    
    /**
     * Delete record
     */
    public void delete(Long id) {
        repository.deleteById(id);
    }
}
