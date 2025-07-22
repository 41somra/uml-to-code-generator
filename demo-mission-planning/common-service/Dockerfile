FROM openjdk:11-jre-slim

# Kessel Run Air Force microservice
LABEL maintainer="Kessel Run <kessel.run@us.af.mil>"
LABEL service="common-service"
LABEL version="1.0.0"

# Create non-root user
RUN groupadd -r kesselrun && useradd -r -g kesselrun kesselrun

# Set working directory
WORKDIR /app

# Copy jar file
COPY target/common-service-1.0.0.jar app.jar

# Change ownership
RUN chown -R kesselrun:kesselrun /app

# Switch to non-root user
USER kesselrun

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
