import { Component } from '@angular/core';
import { PetCard } from '../../shared/components/pet-card/pet-card';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { MOCK_PETS, PetCardInfo } from '../../shared/models/pet-card-info';

@Component({
  selector: 'app-pet-catalog',
  imports: [PetCard, NgbModule],
  templateUrl: './pet-catalog.html',
  styleUrl: './pet-catalog.scss',
})
export class PetCatalog {
  pets: PetCardInfo[] = MOCK_PETS;
}
