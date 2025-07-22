package mil.af.kesselrun.commonservice.repository;

import mil.af.kesselrun.commonservice.entity.RiskAssessment;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * RiskAssessment Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface RiskAssessmentRepository extends JpaRepository<RiskAssessment, Long> {
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM RiskAssessment e WHERE e.deletedAt IS NULL")
    List<RiskAssessment> findAllActive();
    
    /**
     * Find by custom criteria
     */
}
