export interface Process {
  name: string;
  dependencies: number[];
  duration: number;
  startTime: Date;
  endTime: Date;
}

export interface FAKE_DATA_TYPE {
  fakeData: {
    type: string;
    processes: Process[];
    carbonRating: number;
  }[];
}

export const FAKE_DATA: FAKE_DATA_TYPE = {
  fakeData: [
    {
      type: "Without Optimizer",
      processes: [
        {
          name: "Process 1",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 2",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 3",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
      ],
      carbonRating: 300,
    },
    {
      type: "Optimizer",
      processes: [
        {
          name: "Process 1",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 2",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 3",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
      ],
      carbonRating: 100,
    },
    {
      type: "Minimum Value",
      processes: [
        {
          name: "Process 1",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 2",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 3",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
      ],
      carbonRating: 200,
    },
    {
      type: "Rule based",
      processes: [
        {
          name: "Process 1",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 2",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
        {
          name: "Process 3",
          dependencies: [0],
          duration: 60,
          startTime: new Date(),
          endTime: new Date(),
        },
      ],
      carbonRating: 150,
    },
  ],
};
