import React from "react";
import {
  FormControl,
  FormControlLabel,
  FormLabel,
  Radio,
  RadioGroup,
} from "@mui/material";

interface OptimizationButtonsProps {
  selectedValue: string;
  setSelectedValue: (selectedValue: string) => void;
}

export const OptimizationButtons = ({
  selectedValue,
  setSelectedValue,
}: OptimizationButtonsProps) => {
  const handleChange = (event: any) => {
    setSelectedValue(event.target.value);
  };

  const controlProps = (item: any) => ({
    checked: selectedValue === item,
    onChange: handleChange,
    value: item,
    name: "color-radio-button-demo",
    inputProps: { "aria-label": item },
  });

  return (
    <div style={{ alignSelf: "center" }}>
      <FormControl>
        <RadioGroup
          row
          defaultValue="Without Optimizer"
          aria-labelledby="demo-customized-radios"
          name="customized-radios"
        >
          <FormControlLabel
            value="female"
            control={
              <Radio
                {...controlProps("Without Optimizer")}
                sx={{
                  color: "#3366CC",
                  "&.Mui-checked": {
                    color: "#3366CC",
                  },
                }}
              />
            }
            label="Without Optimizer"
          />
          <FormControlLabel
            value="Optimizer"
            control={
              <Radio
                {...controlProps("Optimizer")}
                sx={{
                  color: "#DC3912",
                  "&.Mui-checked": {
                    color: "#DC3912",
                  },
                }}
              />
            }
            label="Optimizer"
          />
          <FormControlLabel
            value="Minimum Value"
            control={
              <Radio
                {...controlProps("Minimum Value")}
                sx={{
                  color: "#FF9800",
                  "&.Mui-checked": {
                    color: "#FF9800",
                  },
                }}
              />
            }
            label="Minimum Value"
          />
          <FormControlLabel
            value="Rule based"
            control={
              <Radio
                {...controlProps("Rule based")}
                color="default"
                sx={{
                  color: "#109618",
                  "&.Mui-checked": {
                    color: "#109618",
                  },
                }}
              />
            }
            label="Rule based"
          />
        </RadioGroup>
      </FormControl>
    </div>
  );
};
