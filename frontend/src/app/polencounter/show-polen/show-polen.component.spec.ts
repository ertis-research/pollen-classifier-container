import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowPolenComponent } from './show-polen.component';

describe('ShowPolenComponent', () => {
  let component: ShowPolenComponent;
  let fixture: ComponentFixture<ShowPolenComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ShowPolenComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ShowPolenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
