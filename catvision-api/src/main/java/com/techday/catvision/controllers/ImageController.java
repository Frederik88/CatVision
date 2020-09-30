package com.techday.catvision.controllers;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.logging.Logger;
import java.util.stream.Collectors;

import javax.imageio.ImageIO;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.CacheControl;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import org.apache.commons.io.IOUtils;
import org.modelmapper.ModelMapper;

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

	@GetMapping("/image/{id}")
	public ImageDto getImage(@PathVariable("id") long id) {
		return imageDAO.get(id).get();
	}
	
	@GetMapping("/images/latest")
	public ArrayList<ImageDto> getLatestImages(){
		ArrayList<ImageDto> images = new ArrayList<>(imageDAO.getAll());
		Collections.reverse(images);
		return images;
	}
	
	@GetMapping("/images/detection/{value}")
	public ArrayList<ImageDto> filterByDetection(@PathVariable boolean value){
		ArrayList<ImageDto> images = new ArrayList<>(imageDAO.filterByDetection(value));
		Collections.reverse(images);
		return images;
	}

	@GetMapping(value = "/jpeg/{id}", produces = "image/jpg")
	public ResponseEntity<byte[]> getImageJpeg(@PathVariable("id") long id) throws IOException {
		HttpHeaders headers = new HttpHeaders();
	    headers.setCacheControl(CacheControl.noCache().getHeaderValue());
	    
		ImageDto image = imageDAO.get(id).get();
		File file = new File(image.getImgPath());
		InputStream fileStream = new FileInputStream(file);
		byte[] media = IOUtils.toByteArray(fileStream);
        ResponseEntity<byte[]> responseEntity = new ResponseEntity<>(media, headers, HttpStatus.OK);
        return responseEntity;

	}
}
