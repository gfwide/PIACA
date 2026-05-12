import { Routes } from '@angular/router';
import { PetCatalog } from './features/pet-catalog/pet-catalog';

export const routes: Routes = [
    { path: '', redirectTo: '/pets', pathMatch: 'full' },
    { path: 'pets', component: PetCatalog },
];
