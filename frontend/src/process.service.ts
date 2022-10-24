import axios from "axios";
import { Process } from "./processTable.component";
const api_key = "IFB8pcdoRBhZGpb8t8IP8UKCAzcUND50";

export interface OPTIMIZE_DTO {
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
}: OPTIMIZE_DTO) => {
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
