package com.example.demo;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import static org.assertj.core.api.Assertions.assertThat;

import com.techday.catvision.CatvisionGatewayApplication;

@SpringBootTest(classes = CatvisionGatewayApplication.class)
class CatvisionGatewayApplicationTests {


	@Test
	public void sampleTest(){
		Boolean test = true;

		assertThat(test).isTrue();
	}

}
