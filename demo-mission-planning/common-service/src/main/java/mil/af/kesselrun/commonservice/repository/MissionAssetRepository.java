package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.MissionAsset;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * MissionAsset Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface MissionAssetRepository extends JpaRepository<MissionAsset, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM MissionAsset e WHERE e.deletedAt IS NULL")
    List<MissionAsset> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
