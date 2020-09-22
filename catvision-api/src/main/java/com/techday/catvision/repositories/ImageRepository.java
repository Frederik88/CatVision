package com.techday.catvision.repositories;

import org.springframework.data.jpa.repository.JpaRepository;

import com.techday.catvision.models.ImageModel;

public interface ImageRepository extends JpaRepository<ImageModel, Long>  {
}
