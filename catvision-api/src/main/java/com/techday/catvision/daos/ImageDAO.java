package com.techday.catvision.daos;

import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Iterator;
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
import com.techday.catvision.utility.Utility;

@Component
public class ImageDAO implements Dao<ImageDto> {

	@Autowired
	ImageRepository imageRepository;

	@Autowired
	ModelMapper modelmapper;

	@Override
	public Optional<ImageDto> get(long id) {
		return Optional.ofNullable(
				convertToDto(imageRepository.findById(id).get())
				);
	}

	@Override
	public Collection<ImageDto> getAll() {
		return imageRepository.findAll().stream()
				.filter(Objects::nonNull)
				.map(image -> this.convertToDto(image))
				.collect(Collectors.toList());
	}
	
	public Collection<ImageDto> filterByDetection(boolean value) {
		return imageRepository.findAll().stream()
				.filter(Objects::nonNull)
				.filter(image -> image.getDetection() == value)
				.map(image -> this.convertToDto(image))
				.collect(Collectors.toList());
	}
	
	public Collection<ImageDto> deleteOlderThanWeek() {
		Collection<ImageDto> collection = filterOlderThanWeek();
		Iterator<ImageDto> iter = collection.iterator();
		while(iter.hasNext()) {
			delete(iter.next());
		}
		
		return collection;
	}
	
	
	
	public void checkForDeletion(long id) {
		Optional<ImageDto> img = Optional.ofNullable(
				convertToDto(imageRepository.findById(id).get())
				);
		
		LocalDate currentDate = LocalDate.now();
		LocalDate laterDate = Utility.convertToDate(img.get().getTimestamp());
		
		boolean checkForDeletion = Utility.checkDateOlderThanDays(currentDate, laterDate, 7);
		
		if(checkForDeletion) {
			delete(img.get());
		}
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
		ImageModel image = convertToEntity(t);
		imageRepository.deleteById(image.getId());
		
	}
	
	private Collection<ImageDto> filterOlderThanWeek(){
		return imageRepository.findAll().stream()
				.filter(Objects::nonNull)
				.filter(image -> Utility.checkDateOlderThanDays(LocalDate.now(), Utility.convertToDate(image.getTimestamp()), 7))
				.map(image -> this.convertToDto(image))
				.collect(Collectors.toList());
	}
	
	private ImageDto convertToDto(ImageModel image) {
		return modelmapper.map(image, ImageDto.class);
	}
	
	private ImageModel convertToEntity(ImageDto imageDto) {
		return modelmapper.map(imageDto, ImageModel.class);
	}

}
