import React, { useState } from "react";
import Select from "react-select";
import { Button, InputBase, TextField } from "@mui/material";
import { string, object, number } from "yup";
import { useFormik } from "formik";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { Process } from "./processTable.component";

const LocationOptions = [
  { name: "East US", value: "eastus" },
  {
    name: "Western Europe",
    value: "westeurope",
  },
];

interface ProcessFormProps {
  addProcess: (values: Process) => void;
}

export const ProcessForm = ({ addProcess }: ProcessFormProps) => {
  const [name, setName] = useState("");
  const [location, setLocation] = useState("");
  const [duration, setDuration] = useState("");

  const validationSchema = object().shape({
    type: string().required("Required!"),
    location: string().required("Required!"),
    duration: number().required().moreThan(0),
  });

  const formik = useFormik({
    enableReinitialize: true,
    initialValues: {
      name: name,
      location: location,
      duration: duration,
    },
    validationSchema: validationSchema,
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
          alignItems: "center",
          justifyContent: "space-around",
          margin: "1rem",
        }}
      >
        <TextField
          style={{
            fontSize: "12px",
          }}
          label="Process name"
          placeholder="Enter process name"
          value={formik.values.name}
          onChange={(e) => setName(e.target.value)}
        ></TextField>
        <Select
          placeholder="Select location"
          styles={{
            control: (provided) => ({
              ...provided,
              borderColor: "#AFDA63",
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
              color: "#AFDA63",
              minWidth: "50%",
            }),
          }}
          options={LocationOptions}
          getOptionValue={(option) => option.value}
          getOptionLabel={(option) => option.name}
          onChange={(selectedValues: any) => {
            setLocation(selectedValues.value);
          }}
        />
        <TextField
          id="duration"
          label="Duration (min)"
          placeholder="Enter duration in minutes"
          value={formik.values.duration}
          onChange={(e) => setDuration(e.target.value)}
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
