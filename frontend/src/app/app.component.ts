import { Component } from '@angular/core';
import { PycalcService } from './services/pycalc.service';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  result:string = ''

  constructor(private service:PycalcService) {}
 
  getAnswer(formula:string) {
    this.service.calcFormula(formula).subscribe(response => {
      this.result  = response.result
    });
  }
}
