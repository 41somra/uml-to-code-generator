package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.Mission;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * Mission Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface MissionRepository extends JpaRepository<Mission, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM Mission e WHERE e.deletedAt IS NULL")
    List<Mission> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
