import { Routes } from '@angular/router';
import { TaskListComponent } from './task-list/task-list.component';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
    { path: 'home', component: HomeComponent },
  { path: 'tasks', component: TaskListComponent },
  { path: '', redirectTo: '/home', pathMatch: 'full' }
  // Add other routes as needed
];