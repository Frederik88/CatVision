import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import {MatDialogModule} from '@angular/material/dialog';

import { AppComponent } from './app.component';
import { ImageComponent } from './_components/image/image.component';
import { GalleryComponent } from './_components/gallery/gallery.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import {ImagePopupComponent} from './_components/image-popup/image-popup.component';

@NgModule({
  declarations: [
    AppComponent,
    ImageComponent,
    GalleryComponent,
    ImagePopupComponent
   ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    MatDialogModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent],
  entryComponents: [ImagePopupComponent]
})
export class AppModule { }
