import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PetCatalog } from './pet-catalog';

describe('PetCatalog', () => {
  let component: PetCatalog;
  let fixture: ComponentFixture<PetCatalog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PetCatalog],
    }).compileComponents();

    fixture = TestBed.createComponent(PetCatalog);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
