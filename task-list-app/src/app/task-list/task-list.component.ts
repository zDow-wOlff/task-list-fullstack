import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TaskService } from '../services/task.service';
import { Task } from '../models/task.model';
import { TaskFormComponent } from '../task-form/task-form.component';
import { TaskItemComponent } from '../task-item/task-item.component';
import { TaskFilterComponent } from '../task-filter/task-filter.component';
import { trigger, transition, style, animate, query, stagger } from '@angular/animations';

@Component({
  selector: 'app-task-list',
  standalone: true,
  imports: [CommonModule, TaskFormComponent, TaskItemComponent, TaskFilterComponent],
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.scss'],
  animations: [
    trigger('taskAnimation', [
      transition('* => *', [
        query(':enter', [
          style({ opacity: 0, transform: 'translateY(-20px)' }),
          stagger(100, [
            animate('0.3s ease-out', style({ opacity: 1, transform: 'translateY(0)' }))
          ])
        ], { optional: true })
      ])
    ])
  ]
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  filteredTasks: Task[] = [];

  constructor(private taskService: TaskService) {}

  ngOnInit() {
    this.loadTasks();
  }

  loadTasks() {
    this.taskService.getTasks().subscribe(
      (tasks) => {
        this.tasks = tasks;
        this.filteredTasks = tasks;
      },
      (error) => {
        console.error('Error fetching tasks:', error);
      }
    );
  }

  onTaskAdded(task: Task) {
    this.taskService.createTask(task).subscribe(
      (newTask) => {
        console.log('Task created successfully:', newTask);
        this.tasks.push(newTask);
        this.filteredTasks = [...this.tasks];
      },
      (error) => {
        console.error('Error creating task:', error);
        if (error.error instanceof ErrorEvent) {
        console.error('Client-side error:', error.error.message);
      } else {
        console.error('Server-side error:', error.status, error.error);
      }
      }
    );
  }

  onTaskDeleted(taskId: number) {
    this.taskService.deleteTask(taskId).subscribe(
      () => {
        this.tasks = this.tasks.filter(task => task.id !== taskId);
        this.filteredTasks = this.filteredTasks.filter(task => task.id !== taskId);
      },
      (error) => {
        console.error('Error deleting task:', error);
      }
    );
  }

  onTaskUpdated(updatedTask: Task) {
    this.taskService.updateTask(updatedTask).subscribe(
      (task) => {
        const index = this.tasks.findIndex(t => t.id === task.id);
        if (index !== -1) {
          this.tasks[index] = task;
          this.filteredTasks = [...this.tasks];
        }
      },
      (error) => {
        console.error('Error updating task:', error);
      }
    );
  }

  onFilterChanged(filters: any) {
    this.filteredTasks = this.tasks.filter(task => {
      if (filters.status && task.status !== filters.status) {
        return false;
      }
      if (filters.teamMember && !(task.contactPerson?.toLowerCase().includes(filters.teamMember.toLowerCase()) ?? false)) {
        return false;
      }
      if (filters.taskType && !task.taskType?.toLowerCase().includes(filters.taskType.toLowerCase())) {
        return false;
      }
      if (filters.entityName && !task.entityName?.toLowerCase().includes(filters.entityName.toLowerCase())) {
        return false;
      }
      if (filters.date && task.date !== filters.date) {
        return false;
      }
      return true;
    });
  }

  onSortChanged(sortCriteria: string) {
    this.filteredTasks.sort((a, b) => {
      switch (sortCriteria) {
        case 'date':
          return new Date(a.date || '').getTime() - new Date(b.date || '').getTime();
        case 'description':
          return a.description.localeCompare(b.description);
        case 'teamMember':
          return a.contactPerson?.localeCompare(b.contactPerson ?? '') ?? 0;
        case 'taskType':
          return a.taskType?.localeCompare(b.taskType ?? '') ?? 0;
        case 'entityName':
          return a.entityName?.localeCompare(b.entityName ?? '') ?? 0;
        default:
          return 0;
      }
    });
    this.filteredTasks = [...this.filteredTasks];
  }
}
