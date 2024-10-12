export interface Task {
    id?: number; // Optional if not provided by the client
    description: string;
    entityName?: string;
    taskType?: string;
    date?: string;
    time?: string;
    contactPerson?: string;
    status?: string;
    note?: string;
    done: boolean;
}