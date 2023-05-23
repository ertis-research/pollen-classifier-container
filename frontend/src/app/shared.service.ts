import { Injectable } from '@angular/core';
import {HttpClient, HttpParams, HttpHeaders} from '@angular/common/http';
import { UserService } from './user.service';


@Injectable({
  providedIn: 'root'
})
export class SharedService {
  
readonly APIUrl = "http://127.0.0.1:8540/";
readonly PhotoUrl = "http://127.0.0.1:8540/media/"

  constructor(private http:HttpClient, private _userService:UserService) { }

    getHttpHeaders() {
      return new HttpHeaders({
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+ this._userService.token//'JWT ' + this._userService.token
        });
    }

    // ---------------------------------------------

    getPolenList(){
      return this.http.get<any[]>(this.APIUrl + 'polen/', {headers: this.getHttpHeaders()})
    }

    deletePolenAnalysis(val:any){
      return this.http.delete(this.APIUrl + 'polen/'+val, {headers: this.getHttpHeaders()})
    }

    UploadVSIPhoto(val:any){
      return this.http.post(this.APIUrl+'uploadVSI/', val,
      {headers: {'Authorization': 'Bearer ' + this._userService.token}})
    }

    analyseSelectedImages(val:any){
      return this.http.post(this.APIUrl+'analyse/', val, {headers: this.getHttpHeaders()})
    }

    //----------------------------------------------------

    getSixMonthData(){
      return this.http.get<any[]>(this.APIUrl + 'getSixMonthData/',
      {headers: this.getHttpHeaders()})
    }

    getRangeInformation(val:any){      
      let prm = new HttpParams().set('RangeId', val)
      return this.http.get<any[]>(this.APIUrl + 'getRangeInformation/', {params: prm, headers: this.getHttpHeaders()})
    }

    getDestributedPolenValues(val:any){
      let prm = new HttpParams().set('dateToCheck', val['dateToCheck'])
      return this.http.get<any[]>(this.APIUrl+'getDistrValues/',
      {params: prm, headers: this.getHttpHeaders()})
    }

    //----------------------------------------------------

    getPolinicRanges(){      
      return this.http.get<any[]>(this.APIUrl + 'range/', {headers: this.getHttpHeaders()})
    }

    addPolinicRange(val:any){
      return this.http.post(this.APIUrl + 'range/', val, {headers: this.getHttpHeaders()})
    }

    deletePolinicRange(val:any){
      return this.http.delete(this.APIUrl + 'range/'+val, {headers: this.getHttpHeaders()})
    }   

    //----------------------------------------------------

    getPolenTypeList(){      
      return this.http.get<any[]>(this.APIUrl + 'polenTypes/', {headers: this.getHttpHeaders()})
    }

    addPolenType(val:any){
      return this.http.post(this.APIUrl + 'polenTypes/', val, {headers: this.getHttpHeaders()})
    }

    deletePolenTypes(val:any){
      return this.http.delete(this.APIUrl + 'polenTypes/'+val, {headers: this.getHttpHeaders()})
    }  


}
