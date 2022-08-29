# Birds in the Area 🕊
Extracts daily bird data in the Los Angeles region to create a data report of birds seen and recorded by users of Cornell University's application, Merlin Bird ID.

## How It's Done
### **ETL**
A data pipeline is built that...

1. **extracts** data from the [eBird API](https://documenter.getpostman.com/view/664302/S1ENwy59),
2. **transforms** the data through basic cleansing and converts the pulled data to a csv file, and
3. **loads** the csv file to an AWS S3 bucket (created just for this project) to eventually load the csv file from the bucket to an Aurora MySQL database.

### **The Report**
The end result is a data report of the different types of birds seen in the LA region on the current day. It uses a combination of pymysql, pandas, and plotly to query for coordinates, (bird_name, frequency), and to plot these coordinates on a horizontal bar graph.

Daily data extractions are also stored in a second MySQL table. This table contains a collection of all daily data extracted and will be used to analyze weekly, monthly, and/or yearly bird data.

## Screenshot
![Alt Text](https://media.giphy.com/media/R8T0Cw1KD6nxByOkZJ/giphy.gif)

------

## TODO 📌
- Make data visualization more aesthetically pleasing and interactive.
- Add bird image and information when hovering over each bird in the bar chart.
- Use Docker and Airflow to run the project so that it emails the data report to the user on a daily basis.
- In addition to daily reports, also create weekly/monthly/yearly reports.