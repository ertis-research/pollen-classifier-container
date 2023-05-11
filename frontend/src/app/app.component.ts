import { Component, OnInit } from '@angular/core';
import { UserService } from './user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'Polen Analysis App';

  public user: any;
 
  constructor(public _userService: UserService) { }
 
  ngOnInit() {
    this.user = {
      username: '',
      password: ''
    };
    this._userService.checkIfStillValid()
  }
 
  login() {
    this._userService.login({'username': this.user.username, 
                             'password': this.user.password});
  }
 
  refreshToken() {
    this._userService.refreshToken();
  }
 
  logout() {
    this._userService.logout();
  }

}
