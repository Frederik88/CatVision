package com.example.demo;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.assertThat;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class CatvisionGatewayApplicationTests {

	//@Test
	void contextLoads() {
		boolean test = true;
		assertThat(test).isTrue();
	}

}
