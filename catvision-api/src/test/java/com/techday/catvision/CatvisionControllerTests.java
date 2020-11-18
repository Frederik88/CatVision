package com.techday.catvision;

import static org.assertj.core.api.Assertions.assertThat;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;


import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;
import org.springframework.web.context.WebApplicationContext;

import com.techday.catvision.controllers.ImageController;

@SpringBootTest
@AutoConfigureMockMvc
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class CatvisionControllerTests {

	@Autowired
	private WebApplicationContext webApplicationContext;

	@Autowired
	private MockMvc mockMvc;
	
	@Autowired
	private ImageController imageController;
	
	private String baseUrl;

	@BeforeEach
	public void setup() {
		this.mockMvc = MockMvcBuilders.webAppContextSetup(webApplicationContext).build();
		this.baseUrl = "/api/v1/image";
	}

	@Test
	public void contextLoads() throws Exception {
		assertThat(imageController).isNotNull();
	}

	@Test
	public void successfulGetImages() throws Exception {
		this.mockMvc.perform(get(baseUrl + "/images")).andExpect(status().isOk());
	}
	
	/*
	@Test
	public void successfulGetImage() throws Exception {
		Collection<ImageDto> images = imageDao.getAll();
		long id = images.iterator().next().getId();
		this.mockMvc.perform(get(baseUrl + "/image/" + id))
		.andExpect(status().isOk());
	}
	*/
}
