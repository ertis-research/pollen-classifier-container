import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';
 
@Injectable()
export class UserService {
readonly APIUrl = window["env"]["API_SERVER_URL"] + "/";
 
  private httpOptions: any; 
  // http options used for making API calls
  public token: string = this.getCacheToken(); 
  // the actual JWT token
  public token_expires: Date = this.getCacheExpireDate(); 
  // the token expiration date
  public username: string = this.getCacheUser();
  // the username of the logged in user
  public user_id: number = this.getCacheUser_Id(); 
  // the user_id of the logged in user
  public errors: any = [];
  // error messages received from the login attempt
 
  constructor(private http: HttpClient, private _snackBar: MatSnackBar) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
  }
 
  private getCacheToken():string{
    let token = localStorage.getItem("userToken");
    if (token == null) return token;

    const token_parts = token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));

    let token_exp_date = new Date(token_decoded.exp * 1000);
    let currentDate = new Date();
    if(currentDate>token_exp_date){
        localStorage.removeItem("userToken");
        return null;
    }
    return localStorage.getItem("userToken");
  }

  private getTokenDecoded():any{
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    return token_decoded;
  }

  private getCacheExpireDate():Date{
    if(this.token==null){
        return null;
    } 
    return new Date(this.getTokenDecoded().exp * 1000);
  }

  private getCacheUser():string{
    if(this.token==null){
        return null;
    } 
    return this.getTokenDecoded().username;
  }

  public getCacheUser_Id():number{
    if(this.token==null){
        return null;
    } 
    return this.getTokenDecoded().user_id;
  }

  public checkIfStillValid():boolean{
      this.token = this.getCacheToken();
      if(this.token == null) return false;
      return true;
  }

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user:any) {
    this.http.post(this.APIUrl+'api-token-auth/', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
        this.updateData(data['access']);
      },
      err => {
        this.errors = err['error'];
        this._snackBar.open('Unable to log in with provided credentials', 'Close', {
          duration: 10000,
          horizontalPosition: "center",
          verticalPosition: "bottom"
        });
      }
    );
  }
 
  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http.post(this.APIUrl+'api-token-refresh/', JSON.stringify({token: 'Bearer '+this.token}), this.httpOptions).subscribe(
      data => {
        this.updateData(data['access']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  public logout() {
    this.token = null;
    this.token_expires = null;
    this.username = null;
    localStorage.removeItem("userToken");
  }
 
  public updateData(token:any) {
    this.token = token;
    this.errors = [];
 
    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;

    localStorage.setItem("userToken", token);
  }
 
}