package com.techday.catvision.daos;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Objects;
import java.util.Optional;
import java.util.stream.Collectors;

import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.techday.catvision.dtos.ImageDto;
import com.techday.catvision.models.ImageModel;
import com.techday.catvision.repositories.ImageRepository;

@Component
public class ImageDAO implements Dao<ImageDto> {

	@Autowired
	ImageRepository imageRepository;

	@Autowired
	ModelMapper modelmapper;

	private List<ImageModel> imageModelList = new ArrayList<>();

	@Override
	public Optional<ImageDto> get(long id) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Collection<ImageDto> getAll() {
		return imageRepository.findAll().stream()
				.filter(Objects::nonNull)
				.map(image -> this.convertToDto(image))
				.collect(Collectors.toList());
	}

	@Override
	public long save(ImageDto t) {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public void update(ImageDto t) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void delete(ImageDto t) {
		// TODO Auto-generated method stub
		
	}
	
	private ImageDto convertToDto(ImageModel image) {
		return modelmapper.map(image, ImageDto.class);
	}
	
	private ImageModel convertToEntity(ImageDto imageDto) {
		return modelmapper.map(imageDto, ImageModel.class);
	}

}
