import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Task } from '../models/task.model';

@Injectable({
  providedIn: 'root'
})
export class TasksApiService {
  private API_URL = 'http://127.0.0.1:5000'; // Ensure this matches your backend

  constructor(private http: HttpClient) { }

  getTasks(): Observable<Task[]> {
    return this.http.get<Task[]>(`${this.API_URL}/tasks`);
  }

  addTask(task: Task): Observable<Task> {
    return this.http.post<Task>(`${this.API_URL}/tasks`, task);
  }

  deleteTask(id: number): Observable<any> {
    return this.http.delete(`${this.API_URL}/tasks/${id}`);
  }

  updateTask(task: Task): Observable<Task> {
    return this.http.put<Task>(`${this.API_URL}/tasks/${task.id}`, task);
  }
}
