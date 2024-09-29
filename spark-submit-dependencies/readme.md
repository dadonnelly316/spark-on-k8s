This project expects to find the spark-submit executable in this directory. You still need the Spark binaries to run spark-submit locally to submit your spark job to the kubernetes cluster. This project comes with an image that contains Spark's dependancies, but the image cannot run spark-submit on itself.

If this folder is empty, please open your terminal and run the below command from this project's home directory to download the spark binaries.

```
bash ./get-spark-submit-dependencies.sh
```