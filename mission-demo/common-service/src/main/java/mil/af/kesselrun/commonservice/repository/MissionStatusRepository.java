package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.MissionStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * MissionStatus Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface MissionStatusRepository extends JpaRepository<MissionStatus, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM MissionStatus e WHERE e.deletedAt IS NULL")
    List<MissionStatus> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
