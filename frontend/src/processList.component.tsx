import React from "react";
import { Process } from "./processTable.component";
import { Chart } from "react-google-charts";
import dayjs from "dayjs";
import { FAKE_DATA, FAKE_DATA_TYPE } from "./fakeData";

interface ProcessListProps {
  processes: Process[];
  startTime: any;
  endTime: any;
  isFetchedData?: boolean;
  selectedOption: string;
  fetchedData: FAKE_DATA_TYPE | null;
}
const columns = [
  { type: "string", label: "Process Index" },
  { type: "string", label: "Process Name" },
  { type: "string", label: "Resource" },
  { type: "date", label: "Start Date" },
  { type: "date", label: "End Date" },
  { type: "number", label: "Duration" },
  { type: "number", label: "Percent Complete" },
  { type: "string", label: "Dependencies" },
];

export const ProcessList = ({
  processes,
  startTime,
  endTime,
  isFetchedData,
  selectedOption,
  fetchedData,
}: ProcessListProps) => {
  const options = {
    height: 275,
    gantt: {
      arrow: {
        color: "#016D68",
      },
      labelStyle: {
        fontName: "Arial, Helvetica, sans-serif",
        fontSize: 14,
        color: "#757575",
      },
      defaultEndDateMillis: dayjs(endTime).toDate(),
    },
  };

  const rows = !isFetchedData
    ? processes.map((process, index) => {
        return [
          index.toString(),
          process.name,
          process.name,
          dayjs(startTime).toDate(),
          null,
          process.duration !== null && process.duration * 60 * 1000,
          100,
          null,
        ];
      })
    : FAKE_DATA.fakeData // should change with fetchedData
        .filter((data) => data.type === selectedOption)
        .map((data) =>
          data.processes.map((process, index) => {
            console.log("here2");
            return [
              index.toString(),
              process.name,
              process.name,
              dayjs(process.startTime).toDate(),
              dayjs(process.endTime).toDate(),
              process.duration * 60 * 1000,
              100,
              process.dependencies !== null && process.dependencies.toString(),
            ];
          })
        );

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
