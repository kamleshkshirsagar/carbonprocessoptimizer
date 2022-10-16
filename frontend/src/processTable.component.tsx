import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button } from "@mui/material";
import { ProcessForm } from "./processForm.component";
import { ProcessGraph } from "./processGraph.component";
import { ProcessList } from "./processList.component";
import { fetchOptimizedProcesses } from "./process.service";
export interface Process {
  name: string;
  duration: number;
  startTime: string | null;
  endTime: string | null;
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
  const [processes, setProcesses] = useState<Process[]>([]);

  const handleAddProcess = (event: any, values: Process) => {
    event.preventDefault();
    setProcesses([...processes, values]);
  };

  const handleOptimize = () => {
    const hello = fetchOptimizedProcesses();
    console.log("processes", processes);
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
          Process Table ( EastUs )
        </Typography>
        <div
          style={{
            display: "flex",
            flexDirection: "row",
            alignItems: "center",
            marginTop: "3rem",
          }}
        >
          <ProcessGraph />
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <ProcessForm addProcess={handleAddProcess} processes={processes} />
            <Button
              sx={{ width: "40%", textAlign: "center" }}
              variant="contained"
              type="submit"
              color={"primary"}
              onClick={handleOptimize}
            >
              Optimize
            </Button>
          </div>
        </div>
        <div style={{ marginTop: "4rem", width: "75%" }}>
          <ProcessList processes={processes} />
        </div>
      </div>
    </ThemeProvider>
  );
};
