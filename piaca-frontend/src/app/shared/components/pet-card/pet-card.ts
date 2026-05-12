import { Component, Input } from '@angular/core';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { PetCardInfo } from '../../models/pet-card-info';

@Component({
  selector: 'app-pet-card',
  imports: [NgbModule],
  templateUrl: './pet-card.html',
  styleUrl: './pet-card.scss',
  standalone: true,
})
export class PetCard {
  @Input() petInfo!: PetCardInfo;
}
