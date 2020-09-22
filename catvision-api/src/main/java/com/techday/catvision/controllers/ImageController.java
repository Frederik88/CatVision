package com.techday.catvision.controllers;

import java.util.Collection;
import java.util.List;
import java.util.logging.Logger;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import com.techday.catvision.daos.ImageDAO;
import com.techday.catvision.dtos.ImageDto;
import com.techday.catvision.repositories.ImageRepository;

@RestController
@RequestMapping("/api/v1/image")
@CrossOrigin
public class ImageController {

	@Autowired
	ModelMapper modelmapper;
	
	@Autowired
	ImageDAO imageDAO;

	private static Logger logger = Logger.getLogger("ImageController.java");

	@GetMapping("/images")
	public Collection<ImageDto> getImages() {
		return imageDAO.getAll();
	}
}
