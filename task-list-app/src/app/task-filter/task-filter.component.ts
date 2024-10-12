import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';

@Component({
  selector: 'app-task-filter',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './task-filter.component.html',
  styleUrls: ['./task-filter.component.scss']
})
export class TaskFilterComponent implements OnInit {
  @Output() filterChanged = new EventEmitter<any>();
  @Output() sortChanged = new EventEmitter<string>();
  filterForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.filterForm = this.fb.group({
      status: [''],
      teamMember: [''],
      taskType: [''],
      entityName: [''],
      date: ['']
    });
  }

  ngOnInit() {
    this.filterForm.valueChanges.subscribe(values => {
      this.filterChanged.emit(values);
    });
  }

  onSortChange(criteria: string) {
    this.sortChanged.emit(criteria);
  }

  // Helper method to safely get form control value
  getControlValue(controlName: string): any {
    return this.filterForm?.get(controlName)?.value ?? '';
  }

  // Method to reset the form
  resetForm() {
    this.filterForm?.reset();
  }

  // Method to check if the form is valid
  isFormValid(): boolean {
    return this.filterForm?.valid ?? false;
  }
}