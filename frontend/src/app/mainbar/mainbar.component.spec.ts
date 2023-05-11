import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MainbarComponent } from './mainbar.component';

describe('MainbarComponent', () => {
  let component: MainbarComponent;
  let fixture: ComponentFixture<MainbarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MainbarComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MainbarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
