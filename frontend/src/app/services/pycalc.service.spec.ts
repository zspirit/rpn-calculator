import { TestBed } from '@angular/core/testing';

import { PycalcService } from './pycalc.service';

describe('PycalcService', () => {
  let service: PycalcService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PycalcService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
