import { Component, OnInit, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-image-popup',
  templateUrl: './image-popup.component.html',
  styleUrls: ['./image-popup.component.css']
})
export class ImagePopupComponent implements OnInit {
  image: any;

  constructor(
    private dialogRef: MatDialogRef<ImagePopupComponent>,
    @Inject(MAT_DIALOG_DATA) data) {

    this.image = data.image;
    console.log(this.image);
    }
  ngOnInit(): void {
  }

  close(): void {
    this.dialogRef.close();
  }
}
