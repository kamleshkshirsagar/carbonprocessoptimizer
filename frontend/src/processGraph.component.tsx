import React from "react";
import { Chart } from "react-google-charts";

const data = [
  ["Hour", "W/o optimizer", "Optimizer", "Minimum Value", "Rule based"],
  ["08:00 AM", 1000, 400, 200, 100],
];

export const ProcessGraph = () => {
  const options = {
    title: "Carbon Rating for running the processes",
    // hAxis: {
    //   title: "Category 1",
    // },
    vAxis: {
      title: "Rating (scale of 1-10)",
    },
    bar: { groupWidth: "20%" },
    legend: { position: "bottom" },
  };
  return (
    <>
      <Chart
        chartType="ColumnChart"
        width="40rem"
        height="15rem"
        options={options}
        data={data}
      />
    </>
  );
};
