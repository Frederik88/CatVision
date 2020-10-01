package com.techday.catvision;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.cloud.netflix.hystrix.EnableHystrix;
import org.springframework.context.annotation.Bean;

@SpringBootApplication
public class CatvisionGatewayApplication {

	public static void main(String[] args) {
		SpringApplication.run(CatvisionGatewayApplication.class, args);
	}

	@Bean
	public RouteLocator myRoutes(RouteLocatorBuilder builder) {
		return builder.routes()
				//Route for catvision-api
				.route(r -> r.path("/api/v1/image/**")
                        .uri("http://localhost:8080/")
                        .id("catvision-image-api"))
				
				//Route for capture-flask
				.route(r -> r.path("/api/capture")
                        .uri("http://192.168.178.41:8080/")
                        .id("capture-flask"))
				
				//Route for catvision-flask
				.route(r -> r.path("/api/v1/transfer")
                        .uri("http://localhost:5000/")
                        .id("catvision-flask"))
				
				.build();
	}

}
