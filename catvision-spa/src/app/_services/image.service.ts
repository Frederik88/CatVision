import { Injectable } from '@angular/core';
import { Observer, Observable } from 'rxjs';
import {Image} from '../_models/image.model';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ImageService {
  baseUrl: string;

constructor(private http: HttpClient) {
  this.baseUrl = 'http://localhost:8080/api/v1/image';
 }

 public getFlowers(): Observable<Image[]>{
   return this.http.get<Image[]>(this.baseUrl + '/images');
 }

}
