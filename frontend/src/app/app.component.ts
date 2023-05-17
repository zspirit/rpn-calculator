import { Component } from '@angular/core';
import { PycalcService } from './services/pycalc.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  input:string = '';
  result:string = '';
  formula:string = ''

  constructor(private service:PycalcService) {}
   
  allClear() {
    this.result = '';
    this.input = '';
  }
 
  calcFormula() {
    console.log("zaz")
    let formula = this.input;
     
    this.service.calcFormula(formula).subscribe(response => {
      this.result  = response.result
    });
  }
 
  getAnswer(formula:string) {
    this.service.calcFormula(formula).subscribe(response => {
      this.result  = response.result
    });
    this.input = this.result;
    if (this.input=="0") this.input="";
  }
}
