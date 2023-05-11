import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddPolenComponent } from './add-polen.component';

describe('AddPolenComponent', () => {
  let component: AddPolenComponent;
  let fixture: ComponentFixture<AddPolenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AddPolenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AddPolenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
