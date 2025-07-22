package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.Intelligence;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * Intelligence Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface IntelligenceRepository extends JpaRepository<Intelligence, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM Intelligence e WHERE e.deletedAt IS NULL")
    List<Intelligence> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
