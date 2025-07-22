package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.MissionPersonnel;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * MissionPersonnel Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface MissionPersonnelRepository extends JpaRepository<MissionPersonnel, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM MissionPersonnel e WHERE e.deletedAt IS NULL")
    List<MissionPersonnel> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
