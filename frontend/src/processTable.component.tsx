import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button } from "@mui/material";
import { ProcessForm } from "./processForm.component";
import { ProcessGraph } from "./processGraph.component";
import { ProcessList } from "./processList.component";
import { fetchOptimizedProcesses } from "./process.service";
import { OptimizationButtons } from "./optimizationButtons";
import { FAKE_DATA_TYPE } from "./fakeData";
export interface Process {
  name: string;
  duration: number | null;
  dependencies: number[] | null;
}

const theme = createTheme({
  palette: {
    primary: {
      main: "#AFDA63",
    },
    secondary: {
      main: "#016D68",
    },
  },
});

export const ProcessTable = () => {
  const location = "eastus";
  const [fetchedData, setFetchedData] = useState<FAKE_DATA_TYPE | null>(null);
  const [processes, setProcesses] = useState<Process[]>([]);
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [selectedOption, setSelectedOption] = useState("Without Optimizer");

  const handleAddProcess = (event: any, values: any) => {
    event.preventDefault();
    setStartTime(values.startTime);
    setEndTime(values.endTime);
    setProcesses([...processes, values.processes]);
  };

  const handleOptimizeOption = (selectedValue: string) => {
    setSelectedOption(selectedValue);
  };

  const handleOptimize = async () => {
    const fetchedOptimizationData = await fetchOptimizedProcesses({
      location,
      startTime,
      endTime,
      processes,
    });
    setFetchedData(fetchedOptimizationData);
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          margin: "2rem",
          backgroundColor: "white",
          minHeight: "80vh",
          borderRadius: "16px",
        }}
      >
        <Typography
          style={{
            textAlign: "center",
            paddingTop: "3rem",
            fontSize: "24px",
            fontWeight: "bold",
            color: "#016D68",
          }}
        >
          Process Optimizations - EastUs Zone
        </Typography>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            marginTop: "3rem",
          }}
        >
          <ProcessGraph fetchedData={fetchedData} />
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <ProcessForm addProcess={handleAddProcess} processes={processes} />
            <Button
              sx={{ width: "20%", textAlign: "center" }}
              variant="contained"
              type="submit"
              color={"primary"}
              onClick={handleOptimize}
            >
              Optimize
            </Button>
          </div>
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            marginTop: "4rem",
            width: "60%",
          }}
        >
          <OptimizationButtons
            selectedValue={selectedOption}
            setSelectedValue={handleOptimizeOption}
          />
          <ProcessList
            processes={processes}
            startTime={startTime}
            endTime={endTime}
            isComingFromForm={true}
            selectedOption={selectedOption}
            fetchedData={fetchedData}
          />
        </div>
      </div>
    </ThemeProvider>
  );
};
