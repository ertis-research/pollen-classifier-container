import { Component, OnInit, ViewChild, Inject } from '@angular/core';
import { SharedService } from 'src/app/shared.service'

// Angular Material
import { MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialog, MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog'
import { MatSnackBar } from '@angular/material/snack-bar'
import { UserService } from 'src/app/user.service';

export interface deleteDialogData {
  AnalysisId: number;
}

@Component({
  selector: 'app-show-polen',
  templateUrl: './show-polen.component.html',
  styleUrls: ['./show-polen.component.css']
})

export class ShowPolenComponent implements OnInit {

  constructor(private service: SharedService,
              public dialog: MatDialog,
              private _userService: UserService) { }

  PolenList: any = [];
  dataSource: any;
  displayedColumns: string[] = ['AnalysisName', 'SampleDate', 'AnalysisDate', 
                                'AnalysisResult', 'Options']; // 'AnalysisResult2', 'Options'];

  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  ngOnInit() {
    this.refreshPolenList();
  }

  refreshPolenList() {
    this.service.getPolenList().subscribe(data => {
      this.PolenList = data;
      this.dataSource = new MatTableDataSource(this.PolenList);
      this.dataSource.sort = this.sort;
      this.dataSource.paginator = this.paginator;
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  deleteDialog(item: any): void {
    if (this._userService.checkIfStillValid()) {
      const deleteDialogRef = this.dialog.open(DeleteDialog, {
        data: { AnalysisId: item.AnalysisId }
      });

      deleteDialogRef.afterClosed().subscribe(_ => {
        this.refreshPolenList();
      });
    }
  }

  parseResultsToJSON(results: string) {
    let parsedResults = JSON.parse(results);

    // generate a html list with the results. "Key: Value"
    let htmlList = '<ul>';
    for (let key in parsedResults) {
      htmlList += '<li>' + key + ': ' + parsedResults[key] + '</li>';
    }
    htmlList += '</ul>';

    return htmlList;

  }


}

@Component({
  selector: 'delete-dialog',
  templateUrl: 'delete-dialog.html',
})

export class DeleteDialog {

  constructor(private service: SharedService, public dialogRef: MatDialogRef<DeleteDialog>,
    @Inject(MAT_DIALOG_DATA) public data: deleteDialogData,
    private _snackBar: MatSnackBar) { }

  onNoClick(): void {
    this.dialogRef.close();
  }

  deleteDialog() {
    this.service.deletePolenAnalysis(this.data.AnalysisId).subscribe()
    this._snackBar.open('Analysis deleted succesfully', 'Close', {
      horizontalPosition: 'end',
      verticalPosition: 'bottom',
      duration: 5 * 1000,
    });
    this.dialogRef.close();
  }

}
