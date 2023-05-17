import { Inject, Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class PycalcService {

  private url = 'http://127.0.0.1:5000/';

  constructor(private httpClient: HttpClient) { 
    
  }

  calcFormula(formula: string){
    return this.httpClient.get<any>(this.url+formula)
  }
}
