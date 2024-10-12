import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Task } from '../models/task.model'; // Assuming you have a Task model defined
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-task-item',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './task-item.component.html',
  styleUrls: ['./task-item.component.scss']
})
export class TaskItemComponent {
  @Input() task: Task = {} as Task;
  @Output() deleteTask = new EventEmitter<number>();
  @Output() updateTask = new EventEmitter<Task>();

  editMode = false;
  editedTask: Task = {} as Task;

  onDelete(): void {
    this.deleteTask.emit(this.task.id);
  }

  onStatusChange(): void {
    this.task.done = !this.task.done;
    this.updateTask.emit(this.task);
  }

  onEdit(): void {
    this.editMode = true;
    this.editedTask = { ...this.task };
  }

  onSave(): void {
    this.updateTask.emit(this.editedTask);
    this.editMode = false;
  }

  onCancel(): void {
    this.editMode = false;
  }
}
