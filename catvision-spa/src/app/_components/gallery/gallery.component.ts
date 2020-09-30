import { Component, OnInit } from '@angular/core';
import { ImageService } from 'src/app/_services/image.service';
import { Image } from 'src/app/_models/image.model';
import { CommonModule } from "@angular/common";

@Component({
  selector: 'app-gallery',
  templateUrl: './gallery.component.html',
  styleUrls: ['./gallery.component.css']
})
export class GalleryComponent implements OnInit {
  images: Image[];

  constructor(private imageService: ImageService) { }

  ngOnInit(): void {
    this.fetchImageModels();

  }

  fetchFilteredImages(value: any): void{
    this.imageService.getFilteredImages(value).subscribe
      (response => {
        if (response){
          this.images = response;
        }
        else{
          console.log('No Images available');
        }
      });
    }

  fetchImageModels(): void{
    this.imageService.getLatestImages().subscribe
      (response => {
        if (response){
          this.images = response;
        }
        else{
          console.log('No Images available');
        }
      });
    }

}
