import axios from "axios";
import { Process } from "./processTable.component";
const api_key = "example";

export interface REQUEST_OPTIMIZE_DTO {
  location: string;
  startTime: Date | null;
  endTime: Date | null;
  processes: Process[];
}

export const fetchOptimizedProcesses = async ({
  location,
  startTime,
  endTime,
  processes,
}: REQUEST_OPTIMIZE_DTO) => {
  console.log(processes);

  const { data } = await axios.get(
    "https://optim.eastus.inference.ml.azure.com/score",
    {
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
        Authorization: "Bearer " + api_key,
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Methods":
          "GET, POST, OPTIONS, PUT, PATCH, DELETE",
      },
      params: {
        location: location,
        startTime: startTime,
        endTime: endTime,
        processes: JSON.stringify(processes),
      },
    }
  );
  return data;
};
