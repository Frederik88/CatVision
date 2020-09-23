/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { LoadImageService } from './loadImage.service';

describe('Service: LoadImage', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LoadImageService]
    });
  });

  it('should ...', inject([LoadImageService], (service: LoadImageService) => {
    expect(service).toBeTruthy();
  }));
});
