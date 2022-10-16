import React, { useState } from "react";
import { TimePicker } from "@mui/x-date-pickers/TimePicker";
import { Button, InputBase, TextField } from "@mui/material";
import { useFormik } from "formik";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { Process } from "./processTable.component";

interface ProcessFormProps {
  addProcess: (values: Process) => void;
}

export const ProcessForm = ({ addProcess }: ProcessFormProps) => {
  const [name, setName] = useState("");
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [dependencies, setDependencies] = useState(null);
  const [duration, setDuration] = useState(0);

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      name: name,
      startTime: startTime,
      endTime: endTime,
      dependencies: dependencies,
      duration: duration,
    },
    onSubmit: (values) => {
      // console.log("values", values);
    },
  });
  return (
    <form onSubmit={formik.handleSubmit}>
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          backgroundColor: "white",
          justifyContent: "space-between",
          margin: "1rem",
        }}
      >
        <TextField
          label="Process name"
          placeholder="Enter process name"
          value={formik.values.name}
          onChange={(e) => setName(e.target.value)}
        ></TextField>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <TimePicker
            label="Start time"
            views={["hours"]}
            renderInput={(params) => <TextField {...params} />}
            value={formik.values.startTime}
            onChange={(newValue) => setStartTime(newValue)}
          ></TimePicker>
          <TimePicker
            label="End time"
            views={["hours"]}
            renderInput={(params) => <TextField {...params} />}
            value={formik.values.endTime}
            onChange={(newValue) => setEndTime(newValue)}
          ></TimePicker>{" "}
        </LocalizationProvider>
        <TextField
          id="duration"
          type="number"
          label="Duration (min)"
          placeholder="Enter duration in minutes"
          value={formik.values.duration}
          onChange={(e) => setDuration(Number(e.target.value))}
        />
        <AddCircleIcon
          fontSize="large"
          style={{ color: "#7FBDDC", alignSelf: "center" }}
          onClick={() => addProcess(formik.values)}
        />
      </div>
    </form>
  );
};
