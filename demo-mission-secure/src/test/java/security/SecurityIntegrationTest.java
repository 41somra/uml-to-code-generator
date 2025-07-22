package mil.af.kesselrun.security;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Security Integration Tests for Kessel Run
 * Tests security configurations and authentication
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
public class SecurityIntegrationTest {
    
    @LocalServerPort
    private int port;
    
    private TestRestTemplate restTemplate = new TestRestTemplate();
    
    @Test
    public void testSecurityHeaders() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "http://localhost:" + port + "/actuator/health", String.class);
        
        // Check security headers
        assertTrue(response.getHeaders().containsKey("X-Content-Type-Options"));
        assertEquals("nosniff", response.getHeaders().getFirst("X-Content-Type-Options"));
        
        assertTrue(response.getHeaders().containsKey("X-Frame-Options"));
        assertEquals("DENY", response.getHeaders().getFirst("X-Frame-Options"));
        
        assertTrue(response.getHeaders().containsKey("X-XSS-Protection"));
        assertEquals("1; mode=block", response.getHeaders().getFirst("X-XSS-Protection"));
    }
    
    @Test
    public void testUnauthorizedAccess() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "http://localhost:" + port + "/api/v1/users", String.class);
        
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }
    
    @Test
    public void testCORSHeaders() {
        ResponseEntity<String> response = restTemplate.optionsForEntity(
            "http://localhost:" + port + "/api/v1/users", String.class);
        
        assertTrue(response.getHeaders().containsKey("Access-Control-Allow-Origin"));
        assertTrue(response.getHeaders().containsKey("Access-Control-Allow-Methods"));
    }
}
