import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { Button } from "@mui/material";
import { ProcessForm } from "./processForm.component";
import { ProcessList } from "./processList.component";

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
    // send request to backend
    console.log("processes", processes);
  };

  return (
    <ThemeProvider theme={theme}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          margin: "4rem",
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
        <ProcessList processes={processes} />
        <ProcessForm addProcess={handleAddProcess} processes={processes} />
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
    </ThemeProvider>
  );
};
