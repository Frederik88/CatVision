import { Component, OnInit, Input } from '@angular/core';
import { ImageService } from 'src/app/_services/image.service';
import { DomSanitizer } from '@angular/platform-browser';
import { Image } from 'src/app/_models/image.model';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { ImagePopupComponent } from '../image-popup/image-popup.component';

@Component({
  selector: 'app-image',
  templateUrl: './image.component.html',
  styleUrls: ['./image.component.css']
})
export class ImageComponent implements OnInit {
  imgUrl: any;
  @Input() image: Image;

  constructor(private imageService: ImageService, private sanitizer: DomSanitizer,
              private dialog: MatDialog) { }

  ngOnInit(): void{
    this.getImageJpeg(this.image.id);
  }

  public getImageJpeg(id: any): void {
    this.imageService.getImageJpeg(id).subscribe
      (response => {
        if (response) {
          const urlCreator = window.URL;
          this.imgUrl = this.sanitizer.bypassSecurityTrustUrl(urlCreator.createObjectURL(response));
        }
        else {
          console.log('No Image with id: ' + id + ' found');
        }
      });
  }

  public openPopup(): void{

    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    dialogConfig.data = {
      image: this.imgUrl
    };


    this.dialog.open(ImagePopupComponent, dialogConfig);
  }


}

