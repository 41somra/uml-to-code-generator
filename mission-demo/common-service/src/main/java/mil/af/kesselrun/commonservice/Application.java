package mil.af.kesselrun.commonservice;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * Common Service Application
 * Kessel Run Microservice for Air Force Mission Systems
 */
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
@EnableJpaRepositories
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
