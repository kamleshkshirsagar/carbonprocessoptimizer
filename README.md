# Carbon Optimized Process Scheduler

Carbon Optimized Process Scheduler is an API Service with an UI application which uses the Carbon Aware SDK to optimize job/process scheduling with the goal of minimizing carbon emissions.

# Running the web application

The frontend application is done by React and Typescript. To run the project you should navigate to frontend folder and run the following commands:

* npm install 
* npm run start

After that you will see the main page where you can enter the following data:

- Optimization start window
- Optimization end window
- Process name
- Process duration
- Dependencies (optional)

For now the optimization is only done for the Eastern US zone. But in the future, our goal is adding more zones.

After adding all processes, click optimize button to request to the optimization service for the results. Then you can see the results for 3 different optimization methods in a graph to compare their Co2 emissions (tons) and the time to execute processes.






