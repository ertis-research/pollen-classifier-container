import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolencounterComponent } from './polencounter.component';

describe('PolencounterComponent', () => {
  let component: PolencounterComponent;
  let fixture: ComponentFixture<PolencounterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PolencounterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PolencounterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
