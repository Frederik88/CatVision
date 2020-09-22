package com.techday.catvision.dtos;

public class ImageDto {
	
    private String name;
    private String timestamp;
    private byte[] img;
    

    public ImageDto(String name, String timestamp, byte[] img) {
        super();
        this.name = name;
        this.timestamp = timestamp;
        this.img = img;
    }
    
    public ImageDto() {
        super();
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

    public byte[] getImg() {
        return img;
    }

    public void setImg(byte[] img) {
        this.img = img;
    }

    @Override
    public String toString() {
        return "Image [name=" + name + ", timestamp=" + timestamp + "]";
    }

}
