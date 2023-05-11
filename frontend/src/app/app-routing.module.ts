import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import {PolencounterComponent} from './polencounter/polencounter.component';

const routes: Routes = [
 {path: 'polen',component:PolencounterComponent},
 {path: '',component:PolencounterComponent},

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
