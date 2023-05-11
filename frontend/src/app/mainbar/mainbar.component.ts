import { Component } from '@angular/core';
import { MatDialog } from '@angular/material/dialog'
import { AddPolenComponent } from '../polencounter/add-polen/add-polen.component';
import { UserService } from '../user.service'
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-mainbar',
  templateUrl: './mainbar.component.html',
  styleUrls: ['./mainbar.component.css']
})
export class MainbarComponent {

  constructor(public dialog: MatDialog, private _userService: UserService, private _snackBarManage: MatSnackBar) { }

  addPolen(): void {
    if (this._userService.checkIfStillValid()) {
      this.dialog.open(AddPolenComponent, {});
    }
  }

  logout() {
    this._snackBarManage.dismiss();
    this._userService.logout();
  }


}
