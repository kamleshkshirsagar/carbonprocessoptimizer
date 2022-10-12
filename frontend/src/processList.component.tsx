import React, { useState } from "react";
import Typography from "@mui/material/Typography";
import { Slider, TextField } from "@mui/material";
import { Process } from "./processTable.component";
import { useFormikContext } from "formik";

interface ProcessListProps {
  processes: Process[];
}

export const ProcessList = ({ processes }: ProcessListProps) => {
  const handleInputChange = (event: any) => {
    const newValue = event.target.value;
    // const newDefaultProcesses = defaultProcesses.map((process, index) => {
    //   console.log(index);
    //   console.log(event.target.id);
    //   if (index === event.target.id) {
    //     process.duration = newValue;
    //     return process;
    //   } else return process;
    // });
    // console.log("newDefaultProcesses", newDefaultProcesses);
    // setDefaultProcesses(newDefaultProcesses);
  };
  return (
    <div style={{ display: "flex", flexDirection: "column", margin: "1rem" }}>
      {processes.map((process: Process, index) => (
        <div style={{ display: "flex" }}>
          <div style={{ display: "flex", flexDirection: "column", flex: "2" }}>
            <Typography id="duration-slider">{process.name}</Typography>
            <Slider
              id={index.toString()}
              value={Number(process.duration)}
              onChange={handleInputChange}
              aria-labelledby="duration-slider"
            >
              {process.duration}
            </Slider>
          </div>
          <TextField
            id={index.toString()}
            value={Number(process.duration)}
            style={{
              border: "1px solid #979797",
              borderRadius: "5px",
              backgroundColor: "#FFFFFF",
              width: "5rem",
              color: "blue",
              marginLeft: "1rem",
            }}
            onChange={handleInputChange}
            inputProps={{
              style: {
                color: "#016D68",
                fontSize: "14px",
                textAlign: "center",
              },
              min: 0,
              step: 1,
              max: 240,
              type: "number",
              "aria-labelledby": "duration-slider",
            }}
          ></TextField>
        </div>
      ))}
    </div>
  );
};
