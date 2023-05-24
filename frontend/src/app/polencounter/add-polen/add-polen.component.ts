import { Component, OnInit } from '@angular/core';
import { SharedService } from 'src/app/shared.service';
import { UserService } from 'src/app/user.service';
import { MatDialogRef } from '@angular/material/dialog'
import { MatSnackBar } from '@angular/material/snack-bar'

import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';

@Component({
  selector: 'app-add-polen',
  templateUrl: './add-polen.component.html',
  styleUrls: ['./add-polen.component.css'],
  providers: [{
    provide: STEPPER_GLOBAL_OPTIONS, useValue: { showError: true }
  }]
})
export class AddPolenComponent implements OnInit {


  constructor(private service: SharedService,
              private _formBuilder: FormBuilder,
              public dialogRef: MatDialogRef<AddPolenComponent>,
              private _snackBar: MatSnackBar,
              private _userService: UserService) { }

  imageFormGroup: FormGroup;
  nameFormGroup: FormGroup;
  dateFormGroup: FormGroup;
  selectImageFormGroup: FormGroup;

  clicked:boolean = false;

  PhotoFileName: string = "";
  PhotoFilePath: string = "";

  // Rebote de path para la selección de imagenes
  imageFileList: any = [];
  imagePaths: any = [];

  ngOnInit(): void {
    this.imageFormGroup = this._formBuilder.group({
      imageCtrl: ['', Validators.nullValidator]
    });
    this.nameFormGroup = this._formBuilder.group({
      nameCtrl: ['', Validators.required]
    });
    this.dateFormGroup = this._formBuilder.group({
      dateCtrl: ['', Validators.required]
    });
    this.selectImageFormGroup = this._formBuilder.group({
      selectedImageCtrl: ['', Validators.nullValidator]
    });
  }



  fileUploaded: boolean = false;
  imageSelectorReady: boolean = false;

  uploadVSIImage(event: any) {
    var file = event.target.files[0];
    const formData: FormData = new FormData();
    formData.append('uploadedFile', file, file.name);

    this.fileUploaded = true;

    this.service.UploadVSIPhoto(formData).subscribe((data: any) => {
      this.imageFileList = data.slice(1, data.length);
      this.imagePaths = data[0];
      this.imageSelectorReady = true;
    })
  }

  selectedRowIds: Set<number> = new Set<number>();

  onSelection(list: any) {
    this.selectedRowIds.clear();
    for (var i = 0; i < list.length; i++) {
      this.selectedRowIds.add(list[i]._value);
    }
  }

  addPolen() {
    this.clicked = true;
    let today = new Date().toISOString().slice(0, 10)
    let dateAux = new Date(this.dateFormGroup.value.dateCtrl);
    var val = {
      AnalysisId: "",
      UserId: this._userService.getCacheUser_Id(),
      AnalysisName: this.nameFormGroup.value.nameCtrl,
      AnalysisDate: today,
      SampleDate: dateAux.toISOString().slice(0, 10),
      PhotoFileName: this.imagePaths.filename,
      PhotoFilePath: this.imagePaths.unzip,
      SelectedRowsIds: Array.from(this.selectedRowIds)
    };

    this._snackBar.openFromComponent(LoadingAnalysisComponent, {
      horizontalPosition: 'center',
      verticalPosition: 'bottom',
    });


    this.dialogRef.close();

    this.service.analyseSelectedImages(val).subscribe(res => {
      if (res.toString() == "Analysis request accepted") {
        window.location.reload();
      } else {
        this._snackBar.dismiss();
        this._snackBar.open('Analysis Failed. Try to analyse later.', 'Close', {
          horizontalPosition: 'end',
          verticalPosition: 'bottom',
          duration: 5 * 1000,
        });
      };
    });

  }

}

@Component({
  selector: 'snackbar-loading',
  templateUrl: 'snackbar-loading.html'
})
export class LoadingAnalysisComponent { }