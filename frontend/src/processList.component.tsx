import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { Process } from "./processTable.component";
import { animated, useTrail } from "react-spring";
import { Chart } from "react-google-charts";
import dayjs from "dayjs";

interface ProcessListProps {
  processes: Process[];
}
const columns = [
  { type: "string", label: "Process Index" },
  { type: "string", label: "Process Name" },
  { type: "date", label: "Start Date" },
  { type: "date", label: "End Date" },
  { type: "number", label: "Duration" },
  { type: "number", label: "Percent Complete" },
  { type: "string", label: "Dependencies" },
];

function daysToMilliseconds(days: number) {
  return days * 24 * 60 * 60 * 1000;
}

// const rows = [
//   [
//     "1",
//     "Find sources",
//     new Date(2015, 0, 1),
//     new Date(2015, 0, 5),
//     null,
//     100,
//     null,
//   ],
//   [
//     "Write",
//     "Write paper",
//     null,
//     new Date(2015, 0, 9),
//     daysToMilliseconds(3),
//     25,
//     "1,Outline",
//   ],
//   [
//     "Cite",
//     "Create bibliography",
//     null,
//     new Date(2015, 0, 7),
//     daysToMilliseconds(1),
//     20,
//     "1",
//   ],
//   [
//     "Complete",
//     "Hand in paper",
//     null,
//     new Date(2015, 0, 10),
//     daysToMilliseconds(1),
//     0,
//     "Cite,Write",
//   ],
//   [
//     "Outline",
//     "Outline paper",
//     null,
//     new Date(2015, 0, 6),
//     daysToMilliseconds(1),
//     100,
//     "1",
//   ],
// ];

export const ProcessList = ({ processes }: ProcessListProps) => {
  const options = {
    height: 275,
    gantt: {
      defaultStartDateMillis: new Date().toLocaleTimeString(),
    },
  };
  const rows = processes.map((process, index) => {
    return [
      index.toString(),
      process.name,
      dayjs(process.startTime).toDate(),
      dayjs(process.endTime).toDate(),
      process.duration * 60 * 1000,
      100,
      process.dependencies,
    ];
  });
  const data = [columns, ...rows];

  return (
    <>
      {rows.length > 0 && (
        <Chart
          chartType="Gantt"
          width="100%"
          height="100%"
          options={options}
          data={data}
        />
      )}
    </>
  );
};
