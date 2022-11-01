import React from "react";
import { Chart } from "react-google-charts";
import { FAKE_DATA, FAKE_DATA_TYPE } from "./fakeData";

const data = [
  ["Carbon Rate", "W/o optimizer", "Optimizer", "Minimum Value", "Rule based"],
  ["Carbon Rate", 1000, 400, 200, 100],
];

export const ProcessGraph = ({
  fetchedData,
}: {
  fetchedData: FAKE_DATA_TYPE | null;
}) => {
  const carbonRatings = FAKE_DATA.fakeData.map((data) => data.carbonRating); // should change with fetchedData
  const data = [
    [
      "Carbon Rate",
      "W/o optimizer",
      "Optimizer",
      "Minimum Value",
      "Rule based",
    ],
    ["Carbon Rate", ...carbonRatings],
  ];
  const options = {
    title: "Carbon Rating for running the processes",
    // hAxis: {
    //   title: "Category 1",
    // },
    vAxis: {
      title: "Rating (scale of 1-10)",
    },
    bar: { groupWidth: "20%" },
    legend: "none",
  };
  return (
    <>
      <Chart
        chartType="ColumnChart"
        width="30rem"
        height="15rem"
        options={options}
        data={data}
      />
    </>
  );
};
