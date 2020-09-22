package com.techday.catvision.models;

import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Lob;

@Entity
public class ImageModel {

	
	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;
    private String name;
    private String timestamp;
    private String imgPath;
    

    public ImageModel(long id, String name, String timestamp, String imgPath) {
        super();
        this.id = id;
        this.name = name;
        this.timestamp = timestamp;
        this.imgPath = imgPath;
    }
    
    public ImageModel() {
        super();
    }

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    public String getImgPath() {
        return imgPath;
    }

    public void setImgPath(String imgPath) {
        this.imgPath = imgPath;
    }

    @Override
    public String toString() {
        return "Image [id=" + id + ", name=" + name + ", timestamp=" + timestamp + ", ImgPath=\" + ImgPath + \"]";
    }
}
