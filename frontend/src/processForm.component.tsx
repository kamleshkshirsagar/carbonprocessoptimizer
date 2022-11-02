import React, { useState } from "react";
import { TimePicker } from "@mui/x-date-pickers/TimePicker";
import { TextField } from "@mui/material";
import Select from "react-select";
import { useFormik } from "formik";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { Process } from "./processTable.component";
import Typography from "@mui/material/Typography";

interface ProcessFormProps {
  addProcess: (event: any, values: any) => void;
  processes: Process[];
}

export const ProcessForm = ({ addProcess, processes }: ProcessFormProps) => {
  const [name, setName] = useState("");
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [dependencies, setDependencies] = useState(null);
  const [duration, setDuration] = useState<number>(0);
  const getDependencyOptions = () => {
    return processes.map((process: Process, index) => {
      return { name: process.name, value: index };
    });
  };

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      startTime: startTime,
      endTime: endTime,
      processes: { name: name, duration: duration, dependencies: dependencies },
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
          flexDirection: "column",
          marginBottom: "1rem",
        }}
      >
        <Typography
          style={{
            fontWeight: "bold",
            marginBottom: "1rem",
            textAlign: "center",
          }}
        >
          Select start and end window time for all processes
        </Typography>
        <div
          style={{
            display: "flex",
            backgroundColor: "white",
            marginBottom: "1rem",
            justifyContent: "space-around",
          }}
        >
          <LocalizationProvider dateAdapter={AdapterDayjs}>
            <TimePicker
              label="Optimization start window"
              views={["hours"]}
              renderInput={(params) => (
                <TextField {...params} style={{ width: "40%" }} />
              )}
              value={formik.values.startTime}
              onChange={(newValue) => setStartTime(newValue)}
            ></TimePicker>
            <TimePicker
              label="Optimization end window"
              views={["hours"]}
              renderInput={(params) => (
                <TextField {...params} style={{ width: "40%" }} />
              )}
              value={formik.values.endTime}
              onChange={(newValue) => setEndTime(newValue)}
            ></TimePicker>{" "}
          </LocalizationProvider>
        </div>
        <Typography
          style={{
            fontWeight: "bold",
            marginBottom: "1rem",
            textAlign: "center",
          }}
        >
          Add maximum 4 processes
        </Typography>
        <div style={{ display: "flex", flexDirection: "row" }}>
          <TextField
            label="Process name"
            placeholder="Enter process name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            style={{ marginRight: "1rem" }}
          ></TextField>
          <Select
            placeholder="Select dependencies"
            styles={{
              control: (provided: any) => ({
                ...provided,
                minHeight: "3.5rem",
              }),
              dropdownIndicator: (provided) => ({
                ...provided,
                color: "#AFDA63",
              }),
              menuPortal: (provided) => ({ ...provided, zIndex: 9999 }),
              menu: (base) => ({
                ...base,
                width: "max-content",
                minWidth: "50%",
              }),
            }}
            isMulti
            options={getDependencyOptions()}
            getOptionValue={(option: any) => option.value}
            getOptionLabel={(option: any) => option.name}
            onChange={(selectedValues: any) => {
              const selectedDependencies = selectedValues.map(
                (value: any) => value.value
              );
              setDependencies(selectedDependencies);
            }}
          />
          <TextField
            id="duration"
            type="number"
            label="Duration"
            placeholder="Enter in minutes"
            value={duration.toString()}
            onChange={(e) => setDuration(Number(e.target.value))}
            style={{ marginLeft: "1rem", width: "10rem" }}
          />
          <div
            style={{
              display: "flex",
              alignItems: "center",
              flexWrap: "wrap",
              marginLeft: "1rem",
              marginBottom: "1rem",
            }}
          >
            <AddCircleIcon
              fontSize="large"
              style={{
                color: "#7FBDDC",
                alignSelf: "center",
                marginRight: "0.5rem",
              }}
              onClick={(e) => addProcess(e, formik.values)}
            />
            {/*<span>Add new process</span>*/}
          </div>
        </div>
      </div>
    </form>
  );
};
