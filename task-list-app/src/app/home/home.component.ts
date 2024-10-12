import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { trigger, transition, style, animate } from '@angular/animations';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="home-container">
      <h1 [@fadeIn]>Welcome to Task Manager</h1>
      <p [@fadeIn]>Manage your tasks efficiently with our easy-to-use task management system.</p>
      <div class="actions">
        <button [@fadeIn] (click)="navigateToTasks()">View Tasks</button>
      </div>
    </div>
  `,
  styles: [`
    .home-container {
      padding: 2rem;
      max-width: 800px;
      margin: 0 auto;
      text-align: center;
    }

    h1 {
      color: var(--primary-color);
      margin-bottom: 1rem;
      font-size: 2.5rem;
    }

    p {
      color: var(--text-color);
      margin-bottom: 2rem;
      font-size: 1.1rem;
      line-height: 1.6;
    }

    .actions button {
      padding: 0.75rem 1.5rem;
      background-color: var(--primary-color);
      color: white;
      border: none;
      border-radius: 4px;
      font-size: 1rem;
      transition: background-color 0.3s ease;
    }

    .actions button:hover {
      filter: brightness(90%);
    }
  `],
  animations: [
    trigger('fadeIn', [
      transition(':enter', [
        style({ opacity: 0, transform: 'translateY(20px)' }),
        animate('0.5s ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
      ])
    ])
  ]
})
export class HomeComponent {
  constructor(private router: Router) {}

  navigateToTasks(): void {
    this.router.navigate(['/tasks']);
  }
}
