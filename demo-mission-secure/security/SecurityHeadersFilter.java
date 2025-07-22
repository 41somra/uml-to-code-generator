package mil.af.kesselrun.security;

import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Security Headers Filter for Kessel Run
 * Adds DoD-required security headers
 */
@Component
public class SecurityHeadersFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        // DoD Security Headers
        httpResponse.setHeader("X-Content-Type-Options", "nosniff");
        httpResponse.setHeader("X-Frame-Options", "DENY");
        httpResponse.setHeader("X-XSS-Protection", "1; mode=block");
        httpResponse.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
        httpResponse.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
        httpResponse.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
        
        // Content Security Policy
        httpResponse.setHeader("Content-Security-Policy", 
            "default-src 'self'; " +
            "script-src 'self' 'unsafe-inline'; " +
            "style-src 'self' 'unsafe-inline'; " +
            "img-src 'self' data:; " +
            "connect-src 'self'; " +
            "font-src 'self'; " +
            "object-src 'none'; " +
            "media-src 'self'; " +
            "frame-src 'none';");
        
        chain.doFilter(request, response);
    }
}
