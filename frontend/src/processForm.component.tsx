import React, { useState } from "react";
import { TimePicker } from "@mui/x-date-pickers/TimePicker";
import { TextField } from "@mui/material";
import Select from "react-select";
import { useFormik } from "formik";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { Process } from "./processTable.component";

interface ProcessFormProps {
  addProcess: (event: any, values: Process) => void;
  processes: Process[];
}

export const ProcessForm = ({ addProcess, processes }: ProcessFormProps) => {
  const [name, setName] = useState("");
  const [startTime, setStartTime] = useState(null);
  const [endTime, setEndTime] = useState(null);
  const [dependencies, setDependencies] = useState(null);
  const [duration, setDuration] = useState(0);
  const getDependencyOptions = () => {
    return processes.map((process: Process, index) => {
      return { name: process.name, value: index };
    });
  };

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
        {/*<TextField*/}
        {/*  id="duration"*/}
        {/*  type="number"*/}
        {/*  label="Duration (min)"*/}
        {/*  placeholder="Enter duration in minutes"*/}
        {/*  value={formik.values.duration}*/}
        {/*  onChange={(e) => setDuration(Number(e.target.value))}*/}
        {/*/>*/}
        <AddCircleIcon
          fontSize="large"
          style={{ color: "#7FBDDC", alignSelf: "center" }}
          onClick={(e) => addProcess(e, formik.values)}
        />
      </div>
    </form>
  );
};
