import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button, Grid, Slider, TextField } from "@mui/material";
import { ProcessForm } from "./processForm.component";
import { ProcessList } from "./processList.component";

export interface Process {
  name: string;
  duration: string;
  location?: string;
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
  const [processes, setProcesses] = useState<Process[]>([]);

  const handleAddProcess = (values: Process) => {
    setProcesses([...processes, values]);
    console.log("processes", processes);
  };

  console.log("processes", processes);
  const handleOptimize = () => {
    // send request to backend
    console.log("processes", processes);
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        style={{ margin: "6rem", backgroundColor: "white", minHeight: "80vh" }}
      >
        <h1 style={{ textAlign: "center" }}>Process Table</h1>
        <ProcessList processes={processes} />
        <ProcessForm addProcess={handleAddProcess} />
        <div style={{ display: "flex", justifyContent: "center" }}>
          <Button
            sx={{ width: "10%", textAlign: "center" }}
            variant="contained"
            type="submit"
            color={"primary"}
            onClick={handleOptimize}
          >
            Optimize
          </Button>
        </div>
      </div>
    </ThemeProvider>
  );
};
