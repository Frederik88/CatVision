import { Injectable } from '@angular/core';
import { Observer, Observable } from 'rxjs';
import {Image} from '../_models/image.model';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  baseUrl: string;
  httpOptions: any;

constructor(private http: HttpClient) {
  this.baseUrl = 'http://localhost:8080/api/v1/image';
 }

 public getImages(): Observable<Image[]>{
   return this.http.get<Image[]>(this.baseUrl + '/images');
 }

 public getLatestImages(): Observable<Image[]>{
  return this.http.get<Image[]>(this.baseUrl + '/images/latest');
}

public getFilteredImages(value: any): Observable<Image[]>{
  return this.http.get<Image[]>(this.baseUrl + '/images/detection/' + value);
}

 public getImageJpeg(id: any): Observable<any>{
   return this.http.get(this.baseUrl + '/jpeg/' + id, {responseType: 'blob'});
 }

}
