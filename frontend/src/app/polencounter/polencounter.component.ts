import { Component, OnInit } from '@angular/core';
import { UserService } from '../user.service';

@Component({
  selector: 'app-polencounter',
  templateUrl: './polencounter.component.html',
  styleUrls: ['./polencounter.component.css']
})
export class PolencounterComponent implements OnInit {

  constructor(public _userService: UserService) { }

  ngOnInit(): void {
    this._userService.checkIfStillValid()
  }

}
