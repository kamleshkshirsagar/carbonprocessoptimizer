import React from "react";
import Typography from "@mui/material/Typography";
import { Button, Slider, TextField } from "@mui/material";
import AddCircleIcon from "@mui/icons-material/AddCircle";

export const ProcessTable = () => {
  return (
    <div>
      <h1>Process Table</h1>
      <div className="flex flex-col">
        <Typography id="non-linear-slider" gutterBottom>
          Process name
        </Typography>
        <Slider
          value={50}
          min={0}
          step={0.1}
          max={6}
          scale={(x) => x ** 10}
          // getAriaValueText={valueLabelFormat}
          // valueLabelFormat={valueLabelFormat}
          // onChange={handleChange}
          valueLabelDisplay="auto"
          aria-labelledby="non-linear-slider"
        />
        <TextField id="duration-text" label="Process name" />{" "}
      </div>
      <>
        <form>
          <TextField id="process-name" label="Process name" />{" "}
          <TextField id="location" label="Location" />{" "}
          <TextField id="duration" label="Duration (min)" />
          <AddCircleIcon
            fontSize="large"
            style={{ color: "#7FBDDC" }}
            // onClick={clicked}
          />
          <div>
            <Button type="submit">Optimize</Button>
          </div>
        </form>
      </>
    </div>
  );
};
