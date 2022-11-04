export interface Process {
  name: string;
  dependencies: number[] | null;
  duration: number;
  startTime: Date;
  endTime: Date;
}
export interface OPTIMIZE_DTO {
  type: string;
  processes: Process[];
  carbonRating: number;
}

export const FAKE_DATA: OPTIMIZE_DTO[] = [
  {
    type: "Without Optimizer",
    processes: [
      {
        name: "Process 1",
        dependencies: null,
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 1, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 2, 5)),
      },
      {
        name: "Process 2",
        dependencies: [0],
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 2, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 3, 5)),
      },
      {
        name: "Process 3",
        dependencies: [0, 1],
        duration: 120,
        startTime: new Date(Date.UTC(22, 11, 2, 3, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 5, 5)),
      },
    ],
    carbonRating: 300,
  },
  {
    type: "Optimizer",
    processes: [
      {
        name: "Process 1",
        dependencies: null,
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 5, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 6, 5)),
      },
      {
        name: "Process 2",
        dependencies: [0],
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 7, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 8, 5)),
      },
      {
        name: "Process 3",
        dependencies: [0, 1],
        duration: 120,
        startTime: new Date(Date.UTC(22, 11, 2, 8, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 10, 5)),
      },
    ],
    carbonRating: 100,
  },
  {
    type: "Minimum Value",
    processes: [
      {
        name: "Process 1",
        dependencies: null,
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 8, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 9, 5)),
      },
      {
        name: "Process 2",
        dependencies: [0],
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 10, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 11, 5)),
      },
      {
        name: "Process 3",
        dependencies: [0, 1],
        duration: 120,
        startTime: new Date(Date.UTC(22, 11, 2, 12, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 14, 5)),
      },
    ],
    carbonRating: 200,
  },
  {
    type: "Rule based",
    processes: [
      {
        name: "Process 1",
        dependencies: null,
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 3, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 4, 5)),
      },
      {
        name: "Process 2",
        dependencies: [0],
        duration: 60,
        startTime: new Date(Date.UTC(22, 11, 2, 5, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 6, 5)),
      },
      {
        name: "Process 3",
        dependencies: [0, 1],
        duration: 120,
        startTime: new Date(Date.UTC(22, 11, 2, 7, 5)),
        endTime: new Date(Date.UTC(22, 11, 2, 9, 5)),
      },
    ],
    carbonRating: 150,
  },
];
