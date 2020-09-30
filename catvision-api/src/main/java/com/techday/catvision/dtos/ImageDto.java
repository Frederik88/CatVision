package com.techday.catvision.dtos;

public class ImageDto {
	private long id;
	private String name;
	private String timestamp;
	private String imgPath;
	private boolean detection;

	public ImageDto(long id, String name, String timestamp, String imgPath, boolean detection) {
		super();
		this.setId(id);
		this.setName(name);
		this.setTimestamp(timestamp);
		this.setImgPath(imgPath);
		this.setDetection(detection);
	}

	public ImageDto() {
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
	
	public boolean getDetection() {
		return detection;
	}

	public void setDetection(boolean detection) {
		this.detection = detection;
	}

	@Override
	public String toString() {
		return "Image [id=" + id + ","
				+ " name=" + name + ","
				+ " timestamp=" + timestamp + ","
				+ " ImgPath=" + imgPath + ","
				+ " detection=" + detection;
	}



}
